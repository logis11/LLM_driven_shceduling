# S2 — primary project and vendor documentation and source code

Reader: S2. Topics in scope: T2 (lecture notes only), T3, T5, T6, T7, T8, T9. Access date for every copy: 2026-09-24. All copies were fetched by this reader; source copies sit under `sources/S2-NN/` (gitignored, will not survive the clone — the quoted passages and copy identifications below are the record). SHA-256 values are of the exact bytes fetched (for git clones: the blob as checked out at the named commit).

Fetch notes: `github.com/<o>/<r>/raw/<tag>/…` returned HTTP 403 through the proxy; `raw.githubusercontent.com/<o>/<r>/<tag>/…` and `git clone` over HTTPS worked. `api.github.com` returned 403. Linux tag list was taken with `git ls-remote`; the newest release tag on 2026-09-24 is `v7.2` (commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`, committed 2026-08-16).

## 1. Search log

| # | Date | Engine / venue | Exact query / request | Hits followed | Dead ends (status) |
|---|---|---|---|---|---|
| 1 | 2026-09-24 | github.com raw | `https://github.com/torvalds/linux/raw/{v6.5,v6.6,v6.12}/kernel/sched/fair.c` | — | 403 (proxy/host), all three |
| 2 | 2026-09-24 | raw.githubusercontent.com | `torvalds/linux/<tag>/kernel/sched/{fair,core,rt,deadline,ext,sched,debug}.{c,h}`, `include/linux/sched/{ext,prio}.h`, `Documentation/scheduler/sched-{bwc,rt-group,deadline,design-CFS,ext,eevdf}.rst` for tags v6.5, v6.6, v6.12, v7.2 | all 200 except below → S2-01…S2-06 | 404: `kernel/sched/ext.c`, `include/linux/sched/ext.h`, `sched-ext.rst`, `sched-eevdf.rst` at v6.5 and v6.6 (not yet in tree); 404 `kernel/sched/ext.c` at v7.2 (moved to `kernel/sched/ext/`) |
| 3 | 2026-09-24 | git (github.com) | `git ls-remote --tags https://github.com/torvalds/linux` | tag list; newest v7.2 | — |
| 4 | 2026-09-24 | raw.githubusercontent.com | `kernel/sched/fair.c` at v6.13…v7.1, grep `^unsigned int sysctl_sched_base_slice` | 750000 through v6.14, 700000 from v6.15 | — |
| 5 | 2026-09-24 | raw.githubusercontent.com | `kernel/sched/rt.c` and `deadline.c` at v6.8, v6.11, v6.13…v7.1, grep `sysctl_sched_rt_runtime`, count `fair_server` | runtime 950000 through v7.1; `fair_server` absent at v6.8/v6.11, present from v6.12 | — |
| 6 | 2026-09-24 | git (github.com) | `git clone --depth 1 --filter=blob:none --sparse -b v7.2 https://github.com/torvalds/linux`; sparse `Documentation/scheduler kernel/sched include/linux/sched` ; `grep -rl 'fair_server\|dl_server' Documentation` | `kernel/sched/ext/{ext.c,types.h,internal.h}` → S2-02; only `sched-rt-group.rst` mentions fair_server | no other doc on fair server defaults |
| 7 | 2026-09-24 | git (github.com) | `git clone https://github.com/illumos/illumos-gate` (blobless sparse, `usr/src/uts/common/{disp,conf,os,sys}`); `git log -- usr/src/uts/common/disp/ts_dptbl.c`; `git log -S'hires_tick = 1'` | S2-08 (master `6b5b8c9e2606b0efc5a90af41eefff9725bea618`), commit d96925c491 | raw `usr/src/man/man4/ts_dptbl.4` at master: 404 (moved to man5) |
| 8 | 2026-09-24 | illumos.org | `https://illumos.org/man/5/ts_dptbl` | 200 → S2-09 | — |
| 9 | 2026-09-24 | git (github.com) | `Stichting-MINIX-Research-Foundation/minix` HEAD raw files + sparse clone; `grep -rn DEFAULT_USER_TIME_SLICE` | S2-10 | — |
| 10 | 2026-09-24 | git (github.com) | `git clone --depth 1 https://github.com/sched-ext/scx`; grep `slice` in `scheds/rust/scx_{lavd,bpfland,rusty}` | S2-11, S2-12, S2-13 | — |
| 11 | 2026-09-24 | WebSearch | `site:pages.cs.wisc.edu remzi Solaris dispatch table MLFQ notes` | `pages.cs.wisc.edu/~remzi/solaris-notes.pdf` → S2-28 | — |
| 12 | 2026-09-24 | WebSearch | `Arpaci-Dusseau lecture notes Solaris time-sharing dispatch table "nobody knows"` | same PDF; no page with the literal "nobody knows" | literal phrase not found; the notes say "no one really knows" |
| 13 | 2026-09-24 | git (github.com) | `git clone --depth 1 https://github.com/scheduler-tools/rt-app` | S2-14 | — |
| 14 | 2026-09-24 | git (github.com) | `git clone https://github.com/ckolivas/interbench` | S2-15 | — |
| 15 | 2026-09-24 | git (github.com) | `git clone --sparse https://github.com/mpv-player/mpv` (`player DOCS/man video/out`) | S2-16 | — |
| 16 | 2026-09-24 | gitlab.freedesktop.org | `-/raw/<main>/subprojects/gstreamer/libs/gst/base/gstbasesink.c`, `…/gst-plugins-base/gst-libs/gst/video/gstvideosink.c`, `…/audio/gstaudiobasesink.c` | 200 → S2-17 | — |
| 17 | 2026-09-24 | git.kernel.org | `git clone https://git.kernel.org/pub/scm/linux/kernel/git/mason/schbench.git`; `git tag`; `git log -G'plist\[PLAT_LIST_MAX\] = '` | S2-18; one tag `v1.0` | — |
| 18 | 2026-09-24 | git (github.com) | `git ls-remote --tags https://github.com/masoncl/schbench`; `git clone` | S2-19; no tags on GitHub | — |
| 19 | 2026-09-24 | git.kernel.org | `git clone --depth 1 https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git` | S2-20 (HEAD = tag v2.11) | — |
| 20 | 2026-09-24 | git (github.com) | `git clone --sparse https://github.com/ColinIanKing/stress-ng` (`README.md stress-ng.1 stress-workload.c stress-cyclic.c`) | S2-21 | — |
| 21 | 2026-09-24 | gitlab.gnome.org | `git clone --depth 1 https://gitlab.gnome.org/GNOME/localsearch.git` (renamed tracker-miners); grep `SCHED_IDLE\|nice\|ioprio\|Nice=\|IOSchedulingClass` | S2-22 | — |
| 22 | 2026-09-24 | git.sesse.net | `git clone https://git.sesse.net/plocate`; `curl "https://git.sesse.net/?p=plocate;a=blob_plain;f=plocate-updatedb.service.in;hb=HEAD"` | — | CONNECT tunnel failed, 502 (both) |
| 23 | 2026-09-24 | salsa.debian.org | `git clone https://salsa.debian.org/debian/plocate.git`; raw `…/-/raw/master/plocate-updatedb.service.in` | — | clone asked for credentials (fatal); raw 302 (redirect to login) |
| 24 | 2026-09-24 | WebSearch | `plocate-updatedb.service IOSchedulingClass idle Nice` | sandboxdb.org summary (not used, secondary); one hit was this project's own GitHub issue — not opened, per the rule to read sources without the repository's description | — |
| 25 | 2026-09-24 | sources.debian.org | `api/src/plocate/`; `data/main/p/plocate/1.1.25-1/plocate-updatedb.service.in` | 200 → S2-23 | `…/debian/plocate.service` 404 (no such file) |
| 26 | 2026-09-24 | invent.kde.org | `git clone https://invent.kde.org/frameworks/baloo.git` | — | 502 |
| 27 | 2026-09-24 | git (github.com) | `git clone --depth 1 https://github.com/KDE/baloo` (KDE mirror); grep scheduling calls | S2-24 | — |
| 28 | 2026-09-24 | git (github.com) | `git clone --depth 1 https://github.com/Cisco-Talos/clamav`; `find -name '*.service*'`; grep `setpriority\|SCHED_IDLE\|SCHED_BATCH\|ioprio\|nice(` in `*.c *.h *.rs` | S2-25 (no hit in source) | — |
| 29 | 2026-09-24 | git (github.com) | `git clone --depth 1` of `borgmatic-collective/borgmatic`, `borgbackup/borg`, `restic/restic`; grep `setpriority\|SCHED_IDLE\|SCHED_BATCH\|ioprio\|os.nice\|Nice=\|IOSchedulingClass` | S2-26 (borgmatic sample unit); borg HEAD `507ff0dd06fceb618c50cfdd5be18c1237bb5762` and restic HEAD `6adedec6b48ae9ff0ffbc37bd675ccebd02c728f`: zero hits | — |
| 30 | 2026-09-24 | gitlab.gnome.org | `git clone --depth 1 https://gitlab.gnome.org/World/deja-dup.git`; grep `ionice\|nice\|SCHED_IDLE` | S2-27 | — |
| 31 | 2026-09-24 | git.kernel.org | `git ls-remote --tags …/docs/man-pages/man-pages.git` (newest `man-pages-6.19`); `plain/man/man7/sched.7?h=man-pages-6.19` | 200 → S2-07 | — |

## 2. Candidates

### S2-01 — Linux kernel, `kernel/sched/fair.c` (CFS at v6.5; EEVDF at v6.6, v6.12, v7.2)

- Citation: Linux kernel source, `kernel/sched/fair.c`, torvalds/linux.
- Copies read (raw.githubusercontent.com/torvalds/linux/<tag>/kernel/sched/fair.c, accessed 2026-09-24):
  - v6.5 (tag object 52e12027…, commit `2dde18cd1d8fac735875f2e4987f11817cc0bc2c`) — `sources/S2-01/fair.c@v6.5`, SHA-256 `c3b7ee0a0bc51b9f5c39c25c97490b5c5b220b5e456a7c5eeb678463d2886188`
  - v6.6 (commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa`) — `fair.c@v6.6`, `7d259d533ffb439992969e5d1d20b27dc64c9203f5c09e09f839047cbd4e40bb`
  - v6.12 (commit `adc218676eef25575469234709c2d87185ca223a`) — `fair.c@v6.12`, `48c485811e4d20cca0204ea75a24da71777e42a66b6ce158f8ece09132635d7d`
  - v7.2 (commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`) — `fair.c@v7.2`, `830ae44741cd322df8de5ae75be8fe2c5469fa6e9e1365fbc4233481e6f1fff0`
  - Point checks (not saved; grep of streamed file): v6.13, v6.14 `sysctl_sched_base_slice = 750000ULL`; v6.15, v6.16, v6.17, v6.18, v6.19, v7.0, v7.1 `= 700000ULL`.
- Verbatim passages:
  - `fair.c:59-73@v6.5`:
    ```
    /*
     * Targeted preemption latency for CPU-bound tasks:
     *
     * NOTE: this latency value is not the same as the concept of
     * 'timeslice length' - timeslices in CFS are of variable length
     * and have no persistent notion like in traditional, time-slice
     * based scheduling concepts.
     *
     * (to see the precise effective timeslice length of your workload,
     *  run vmstat and monitor the context-switches (cs) field)
     *
     * (default: 6ms * (1 + ilog(ncpus)), units: nanoseconds)
     */
    unsigned int sysctl_sched_latency			= 6000000ULL;
    static unsigned int normalized_sysctl_sched_latency	= 6000000ULL;
    ```
  - `fair.c:75-86@v6.5`:
    ```
    /*
     * The initial- and re-scaling of tunables is configurable
     *
     * Options are:
     *
     *   SCHED_TUNABLESCALING_NONE - unscaled, always *1
     *   SCHED_TUNABLESCALING_LOG - scaled logarithmical, *1+ilog(ncpus)
     *   SCHED_TUNABLESCALING_LINEAR - scaled linear, *ncpus
     *
     * (default SCHED_TUNABLESCALING_LOG = *(1+ilog(ncpus))
     */
    unsigned int sysctl_sched_tunable_scaling = SCHED_TUNABLESCALING_LOG;
    ```
  - `fair.c:88-102@v6.5`:
    ```
    /*
     * Minimal preemption granularity for CPU-bound tasks:
     *
     * (default: 0.75 msec * (1 + ilog(ncpus)), units: nanoseconds)
     */
    unsigned int sysctl_sched_min_granularity			= 750000ULL;
    static unsigned int normalized_sysctl_sched_min_granularity	= 750000ULL;

    /*
     * Minimal preemption granularity for CPU-bound SCHED_IDLE tasks.
     * Applies only when SCHED_IDLE tasks compete with normal tasks.
     *
     * (default: 0.75 msec)
     */
    unsigned int sysctl_sched_idle_min_granularity			= 750000ULL;
    ```
  - `fair.c:104-107@v6.5`: `* This value is kept at sysctl_sched_latency/sysctl_sched_min_granularity` … `static unsigned int sched_nr_latency = 8;`
  - `fair.c:115-125@v6.5`: `* SCHED_OTHER wake-up granularity.` … `* (default: 1 msec * (1 + ilog(ncpus)), units: nanoseconds)` / `unsigned int sysctl_sched_wakeup_granularity			= 1000000UL;`
  - `fair.c:244-272@v6.5` (identical text at `fair.c:205-233@v6.6` and `fair.c:184-212@v7.2`):
    ```
    /*
     * Increase the granularity value when there are more CPUs,
     * because with more CPUs the 'effective latency' as visible
     * to users decreases. But the relationship is not linear,
     * so pick a second-best guess by going with the log2 of the
     * number of CPUs.
     *
     * This idea comes from the SD scheduler of Con Kolivas:
     */
    static unsigned int get_update_sysctl_factor(void)
    {
    	unsigned int cpus = min_t(unsigned int, num_online_cpus(), 8);
    	unsigned int factor;

    	switch (sysctl_sched_tunable_scaling) {
    	case SCHED_TUNABLESCALING_NONE:
    		factor = 1;
    		break;
    	case SCHED_TUNABLESCALING_LINEAR:
    		factor = cpus;
    		break;
    	case SCHED_TUNABLESCALING_LOG:
    	default:
    		factor = 1 + ilog2(cpus);
    		break;
    	}

    	return factor;
    }
    ```
  - `fair.c:274-283@v6.5`: `#define SET_SYSCTL(name) \` / `(sysctl_##name = (factor) * normalized_sysctl_##name)` / `SET_SYSCTL(sched_min_granularity);` / `SET_SYSCTL(sched_latency);` / `SET_SYSCTL(sched_wakeup_granularity);`
  - `fair.c:717-731@v6.5`:
    ```
    /*
     * The idea is to set a period in which each task runs once.
     *
     * When there are too many tasks (sched_nr_latency) we have to stretch
     * this period because otherwise the slices get too small.
     *
     * p = (nr <= nl) ? l : l*nr/nl
     */
    static u64 __sched_period(unsigned long nr_running)
    {
    	if (unlikely(nr_running > sched_nr_latency))
    		return nr_running * sysctl_sched_min_granularity;
    	else
    		return sysctl_sched_latency;
    }
    ```
  - `fair.c:73-79@v6.6`:
    ```
    /*
     * Minimal preemption granularity for CPU-bound tasks:
     *
     * (default: 0.75 msec * (1 + ilog(ncpus)), units: nanoseconds)
     */
    unsigned int sysctl_sched_base_slice			= 750000ULL;
    static unsigned int normalized_sysctl_sched_base_slice	= 750000ULL;
    ```
    (`fair.c:76-77@v6.12`: same two assignments, `750000ULL`.)
  - `fair.c:237-242@v6.6`: `#define SET_SYSCTL(name) \` / `(sysctl_##name = (factor) * normalized_sysctl_##name)` / `SET_SYSCTL(sched_base_slice);`
  - `fair.c:1024-1034@v6.6`:
    ```
    	/*
    	 * For EEVDF the virtual time slope is determined by w_i (iow.
    	 * nice) while the request time r_i is determined by
    	 * sysctl_sched_base_slice.
    	 */
    	se->slice = sysctl_sched_base_slice;

    	/*
    	 * EEVDF: vd_i = ve_i + r_i / w_i
    	 */
    	se->deadline = se->vruntime + calc_delta_fair(se->slice, se);
    ```
  - `fair.c:74-80@v7.2`:
    ```
    /*
     * Minimal preemption granularity for CPU-bound tasks:
     *
     * (default: 0.70 msec * (1 + ilog(ncpus)), units: nanoseconds)
     */
    unsigned int sysctl_sched_base_slice			= 700000ULL;
    static unsigned int normalized_sysctl_sched_base_slice	= 700000ULL;
    ```
  - `fair.c:67@v7.2`: ` *   SCHED_TUNABLESCALING_LOG - scaled logarithmically, *1+ilog(ncpus)`; `fair.c:72@v7.2`: `unsigned int sysctl_sched_tunable_scaling = SCHED_TUNABLESCALING_LOG;`
  - T9 — wake-up preemption, `fair.c:8093-8101@v6.6` (same text at `fair.c:7969-7976@v6.5`):
    ```
    	/* Idle tasks are by definition preempted by non-idle tasks. */
    	if (unlikely(task_has_idle_policy(curr)) &&
    	    likely(!task_has_idle_policy(p)))
    		goto preempt;

    	/*
    	 * Batch and idle tasks do not preempt non-idle tasks (their preemption
    	 * is driven by the tick):
    	 */
    ```
  - T9 — `fair.c:9820-9840@v7.2` (in `wakeup_preempt_fair`; v6.12 has the same logic in `check_preempt_wakeup_fair`, `fair.c:8764ff@v6.12`, without the slice-protection line):
    ```
    	/*
    	 * Preempt an idle entity in favor of a non-idle entity (and don't preempt
    	 * in the inverse case).
    	 */
    	if (cse_is_idle && !pse_is_idle) {
    		/*
    		 * When non-idle entity preempt an idle entity,
    		 * don't give idle entity slice protection.
    		 */
    		preempt_action = PREEMPT_WAKEUP_SHORT;
    		goto preempt;
    	}

    	if (cse_is_idle != pse_is_idle)
    		return;

    	/*
    	 * BATCH and IDLE tasks do not preempt others.
    	 */
    	if (unlikely(!normal_policy(p->policy)))
    		return;
    ```
  - `fair.c:464-469@v6.12`: `static int se_is_idle(struct sched_entity *se)` / `if (entity_is_task(se))` / `return task_has_idle_policy(task_of(se));` / `return cfs_rq_is_idle(group_cfs_rq(se));`
- Coverage:
  - T3 covers. CFS (v6.5): `sysctl_sched_latency` normalized 6 000 000 ns, `sysctl_sched_min_granularity` normalized 750 000 ns, `sysctl_sched_wakeup_granularity` 1 000 000 ns, `sched_nr_latency` 8; each multiplied at boot by `factor`, default `SCHED_TUNABLESCALING_LOG` = 1 + ilog2(min(online CPUs, 8)), i.e. factor 1…4 (1 CPU → ×1, 2 → ×2, 4 → ×3, ≥8 → ×4); unit ns; not scaled by clock rate. EEVDF (v6.6, v6.12, v6.14): `sysctl_sched_base_slice` normalized 750 000 ns; v6.15 through v7.2: 700 000 ns; still multiplied by the same log factor at v7.2 (`SET_SYSCTL(sched_base_slice)`), so effective default = 0.70 ms × (1 + ilog2(min(ncpus, 8))) at v7.2. Scope: the value is the slice request r_i per entity (`se->slice`). The commit that changed 750000→700000 was not identified (only bracketed between tags v6.14 and v6.15).
  - T9 covers (source-level): SCHED_IDLE task on CPU is preempted at wake-up by any non-idle waking task (`goto preempt`); a waking SCHED_IDLE/BATCH task does not wake-up-preempt a normal task. At v6.5 a separate `sysctl_sched_idle_min_granularity` 0.75 ms applied when SCHED_IDLE competes with normal tasks.
  - Not an observation: source code, no machine/run.

### S2-02 — Linux kernel sched_ext: `include/linux/sched/ext.h`, `kernel/sched/ext.c` (v6.12), `kernel/sched/ext/*` (v7.2), `Documentation/scheduler/sched-ext.rst`

- Copies read (accessed 2026-09-24):
  - v6.12 raw.githubusercontent.com: `include/linux/sched/ext.h` → `S2-02/ext.h@v6.12` SHA-256 `16a04dd3aaeb97316250d980d93bc187830c5fbe433d10ee062308523940aa56`; `kernel/sched/ext.c` → `ext.c@v6.12` `bf0a60636ed46bc29c75bdbe2a5570952439b5b1efeadd8f3e90fd0723e576f4`; `Documentation/scheduler/sched-ext.rst` → `sched-ext.rst@v6.12` `b5a95750fb7e7d2778454b80e89c25d525ce739700b6528029ed7701613228e6`.
  - v7.2 (sparse clone at `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`): `include/linux/sched/ext.h` → `ext.h@v7.2` `a570147bc50059f23764ba831948caacce5d486af15ffaccf40b3a993414d137`; `kernel/sched/ext/ext.c` → `ext-ext.c@v7.2` `31d4b19b6c0ceefc4796626b1bf16e269d7e1aa6cc67977cb1ecb7589d941c09`; `kernel/sched/ext/types.h` → `ext-types.h@v7.2` `784306a7bd2e9ded7c51dd7cbeb4e0f9d24274a5ee5c2ddc7f1c6a8cef93639b`; `kernel/sched/ext/internal.h` → `ext-internal.h@v7.2` `9ef72db0c3f40d814db7261002efce55dbcefb7dcbc45209313ef8d351837734`.
- Verbatim passages:
  - `include/linux/sched/ext.h:17-22@v6.12`:
    ```
    enum scx_public_consts {
    	SCX_OPS_NAME_LEN	= 128,

    	SCX_SLICE_DFL		= 20 * 1000000,	/* 20ms */
    	SCX_SLICE_INF		= U64_MAX,	/* infinite, implies nohz */
    };
    ```
  - `include/linux/sched/ext.h:20-32@v7.2`:
    ```
    	/*
    	 * %SCX_SLICE_DFL is used to refill slices when the BPF scheduler misses
    	 * to set the slice for a task that is selected for execution.
    	 * %SCX_EV_REFILL_SLICE_DFL counts the number of times the default slice
    	 * refill has been triggered.
    	 *
    	 * %SCX_SLICE_BYPASS is used as the slice for all tasks in the bypass
    	 * mode. As making forward progress for all tasks is the main goal of
    	 * the bypass mode, a shorter slice is used.
    	 */
    	SCX_SLICE_DFL		= 20 * 1000000,	/* 20ms */
    	SCX_SLICE_BYPASS	=  5 * 1000000, /*  5ms */
    	SCX_SLICE_INF		= U64_MAX,	/* infinite, implies nohz */
    ```
  - `kernel/sched/ext.c:14@v6.12`: `SCX_WATCHDOG_MAX_TIMEOUT	= 30 * HZ,`; `kernel/sched/ext/types.h:20@v7.2`: `SCX_WATCHDOG_MAX_TIMEOUT	= 30 * HZ,`
  - `kernel/sched/ext.c:650-657@v6.12` (same text `kernel/sched/ext/internal.h:788-794@v7.2`):
    ```
    	/**
    	 * timeout_ms - The maximum amount of time, in milliseconds, that a
    	 * runnable task should be able to wait before being scheduled. The
    	 * maximum timeout may not exceed the default timeout of 30 seconds.
    	 *
    	 * Defaults to the maximum allowed timeout value of 30 seconds.
    	 */
    	u32 timeout_ms;
    ```
  - `kernel/sched/ext.c:5119-5122@v6.12`: `if (ops->timeout_ms)` / `timeout = msecs_to_jiffies(ops->timeout_ms);` / `else` / `timeout = SCX_WATCHDOG_MAX_TIMEOUT;`
  - `kernel/sched/ext/ext.c:3479-3487@v7.2`:
    ```
    		if (unlikely(time_after(jiffies,
    					last_runnable + READ_ONCE(sch->watchdog_timeout)))) {
    			u32 dur_ms = jiffies_to_msecs(jiffies - last_runnable);

    			__scx_exit(sch, SCX_EXIT_ERROR_STALL, 0, cpu_of(rq),
    				   "%s[%d] failed to run for %u.%03us",
    				   p->comm, p->pid, dur_ms / 1000,
    				   dur_ms % 1000);
    ```
  - `sched-ext.rst:16-19@v6.12`: `* The system integrity is maintained no matter what the BPF scheduler does.` / `The default scheduling behavior is restored anytime an error is detected,` / `a runnable task stalls, or on invoking the SysRq key sequence` / `:kbd:`SysRq-S`.`
- Coverage: T3 covers — `SCX_SLICE_DFL` = 20 ms (20 000 000 ns), a fixed constant, no CPU-count or clock scaling; used when the BPF scheduler does not set a slice; v7.2 adds `SCX_SLICE_BYPASS` 5 ms. T6 covers — watchdog: a runnable sched_ext task not run within `timeout_ms` (default and maximum 30 s = `30 * HZ` jiffies) aborts the BPF scheduler (`SCX_EXIT_ERROR_STALL`) and reverts tasks to the fair class; the bound is per task, from `runnable_at`. Not an observation.

### S2-03 — Linux `Documentation/scheduler/sched-bwc.rst` (CFS bandwidth control)

- Copy: raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/scheduler/sched-bwc.rst, accessed 2026-09-24, `sources/S2-03/sched-bwc.rst@v7.2`, SHA-256 `48a0d7601a8a63405de5ba3b80f0c0a8e02f6e573f427fbf4bb3f62db63ae523`. (v6.12 copy fetched too, 11048 bytes vs 11047; not diffed line by line.)
- Verbatim passages:
  - `sched-bwc.rst:5-18@v7.2`:
    ```
    .. note::
       This document only discusses CPU bandwidth control for SCHED_NORMAL.
       The SCHED_RT case is covered in Documentation/scheduler/sched-rt-group.rst

    CFS bandwidth control is a CONFIG_FAIR_GROUP_SCHED extension which allows the
    specification of the maximum CPU bandwidth available to a group or hierarchy.

    The bandwidth allowed for a group is specified using a quota and period. Within
    each given "period" (microseconds), a task group is allocated up to "quota"
    microseconds of CPU time. That quota is assigned to per-cpu run queues in
    slices as threads in the cgroup become runnable. Once all quota has been
    assigned any additional requests for quota will result in those threads being
    throttled. Throttled threads will not be able to run again until the next
    period when the quota is replenished.
    ```
  - `sched-bwc.rst:77-95@v7.2`:
    ```
    - cpu.cfs_quota_us: run-time replenished within a period (in microseconds)
    - cpu.cfs_period_us: the length of a period (in microseconds)
    - cpu.stat: exports throttling statistics [explained further below]
    - cpu.cfs_burst_us: the maximum accumulated run-time (in microseconds)

    The default values are::

    	cpu.cfs_period_us=100ms
    	cpu.cfs_quota_us=-1
    	cpu.cfs_burst_us=0

    A value of -1 for cpu.cfs_quota_us indicates that the group does not have any
    bandwidth restriction in place, such a group is described as an unconstrained
    bandwidth group. This represents the traditional work-conserving behavior for
    CFS.

    Writing any (valid) positive value(s) no smaller than cpu.cfs_burst_us will
    enact the specified bandwidth limit. The minimum quota allowed for the quota or
    period is 1ms. There is also an upper bound on the period length of 1s.
    ```
  - `sched-bwc.rst:72-75@v7.2`: `The cgroupfs files described in this section are only applicable` / `to cgroup v1. For cgroup v2, see` …
  - `sched-bwc.rst:120@v7.2`: `/proc/sys/kernel/sched_cfs_bandwidth_slice_us (default=5ms)`
- Coverage: T5 covers — limits maximum CPU time of a task group (cgroup, `CONFIG_FAIR_GROUP_SCHED`), SCHED_NORMAL only; quota µs per period µs; defaults period 100 ms, quota −1 (unlimited, work-conserving), burst 0; quota/period minimum 1 ms, period max 1 s; per-CPU silo transfer slice 5 ms. Entity: group/hierarchy, not a task or policy class. Not an observation.

### S2-04 — Linux RT throttling: `kernel/sched/rt.c` and `Documentation/scheduler/sched-rt-group.rst` (v6.12, v7.2)

- Copies (raw.githubusercontent.com, accessed 2026-09-24): `rt.c@v6.12` `7ce06c71ee32631462e305b2055db6add0d31bc278a50f0ab05fa77ed2d1fcb1`; `rt.c@v7.2` `94683b7c7291d4fe47692503bd90be45e42629fac4a12e63fae29cb82bfdad94`; `sched-rt-group.rst@v6.12` `853bdf8677747cb3ff208810ffb112b209a0479cb86ba6a934167b7e628bbd63`; `sched-rt-group.rst@v7.2` `c822e506021e8ee06ebc9be4e59b9d0dc52f12b6c2dd1ba3306f294b34ccadf6`. Point checks of `rt.c` (not saved): v6.5 `rt.c:19` `unsigned int sysctl_sched_rt_period = 1000000;`, `rt.c:25` `int sysctl_sched_rt_runtime = 950000;`; v6.8, v6.11, v6.13–v7.1 all `int sysctl_sched_rt_runtime = 950000;`.
- Verbatim passages:
  - `rt.c:10-21@v6.12`:
    ```
    /*
     * period over which we measure -rt task CPU usage in us.
     * default: 1s
     */
    int sysctl_sched_rt_period = 1000000;

    /*
     * part of the period that we allow rt tasks to run in us.
     * default: 0.95s
     */
    int sysctl_sched_rt_runtime = 950000;
    ```
  - `rt.c:14-24@v7.2`:
    ```
    /*
     * period over which we measure -rt task CPU usage in us.
     * default: 1s
     */
    int sysctl_sched_rt_period = 1000000;

    /*
     * part of the period that we allow rt tasks to run in us.
     * default: 1s
     */
    int sysctl_sched_rt_runtime = 1000000;
    ```
  - `sched-rt-group.rst:92-107@v7.2`:
    ```
    /proc/sys/kernel/sched_rt_runtime_us:
      A global limit on how much time real-time scheduling may use. This is always
      less or equal to the period_us, as it denotes the time allocated from the
      period_us for the real-time tasks. Without CONFIG_RT_GROUP_SCHED enabled,
      this only serves for admission control of deadline tasks. With
      CONFIG_RT_GROUP_SCHED=y it also signifies the total bandwidth available to
      all real-time groups.

      * Time is specified in us because the interface is s32. This gives an
        operating range from 1us to about 35 minutes.
      * sched_rt_period_us takes values from 1 to INT_MAX.
      * sched_rt_runtime_us takes values from -1 to sched_rt_period_us.
      * A run time of -1 specifies runtime == period, ie. no limit.
      * sched_rt_runtime_us/sched_rt_period_us > 0.05 inorder to preserve
        bandwidth for fair dl_server. For accurate value check average of
        runtime/period in /sys/kernel/debug/sched/fair_server/cpuX/
    ```
  - `sched-rt-group.rst:95-98@v6.12`: `period_us for the real-time tasks. Even without CONFIG_RT_GROUP_SCHED enabled,` / `this will limit time reserved to real-time processes. With` / `CONFIG_RT_GROUP_SCHED=y it signifies the total bandwidth available to all` / `real-time groups.`
  - `sched-rt-group.rst:113-117@v7.2` (identical at `:110-114@v6.12`):
    ```
    The default values for sched_rt_period_us (1000000 or 1s) and
    sched_rt_runtime_us (950000 or 0.95s).  This gives 0.05s to be used by
    SCHED_OTHER (non-RT tasks). These defaults were chosen so that a run-away
    real-time tasks will not lock up the machine but leave a little time to recover
    it.  By setting runtime to -1 you'd get the old behaviour back.
    ```
- Coverage: T5 covers — system-wide ceiling on RT (and, via admission, deadline) CPU time: runtime µs per period µs, default 950 000 / 1 000 000 µs (95 %) through v7.1; v7.2 source default runtime 1 000 000 (= period); the v7.2 doc text on defaults still says 950000 (doc/source disagree at v7.2 — reported as read). At v7.2 without `CONFIG_RT_GROUP_SCHED` the knob "only serves for admission control of deadline tasks". T6 covers — the 0.05 s per 1 s left to SCHED_OTHER through v7.1 is the RT-throttling starvation bound for non-RT tasks; v7.2 docs direct to the fair dl_server instead (S2-05). Not an observation.

### S2-05 — Linux deadline class and fair server: `kernel/sched/deadline.c`, `kernel/sched/debug.c`, `Documentation/scheduler/sched-deadline.rst`

- Copies (raw.githubusercontent.com, accessed 2026-09-24): `deadline.c@v6.12` `d353c1e6f336a8f6818443f804670318ba147e91a5616240a53b416fee5573cb`; `deadline.c@v7.2` `1d8e9d272f848a6849f1ad3a704bda29f70e9ecb11809412f7d3c13b89eeaddf`; `debug.c@v7.2` `49e9a698deca3684c1423c7477baac955cbcfe4f52a67e808f997db7524c33f4`; `sched-deadline.rst@v7.2` `1525a646181778a0e054731cf3785da7d3c42df93f0f6cfd09e08e6797a3b436`. Point checks: `grep -c fair_server kernel/sched/deadline.c` = 0 at v6.8 and v6.11, >0 from v6.12.
- Verbatim passages:
  - `deadline.c:1636-1644@v6.12`:
    ```
    	if (!dl_server(dl_se)) {
    		u64 runtime =  50 * NSEC_PER_MSEC;
    		u64 period = 1000 * NSEC_PER_MSEC;

    		dl_server_apply_params(dl_se, runtime, period, 1);

    		dl_se->dl_server = 1;
    		dl_se->dl_defer = 1;
    		setup_new_dl_entity(dl_se);
    ```
  - `deadline.c:1848-1865@v7.2` (`sched_init_dl_servers`): `for_each_online_cpu(cpu) {` / `u64 runtime =  50 * NSEC_PER_MSEC;` / `u64 period = 1000 * NSEC_PER_MSEC;` … `dl_se = &rq->fair_server;` … `dl_server_apply_params(dl_se, runtime, period, 1);` / `dl_se->dl_server = 1;` / `dl_se->dl_defer = 1;`; the same runtime/period are then applied to `dl_se = &rq->ext_server;` under `#ifdef CONFIG_SCHED_CLASS_EXT`.
  - `debug.c:620,631-632@v7.2`: `d_fair = debugfs_create_dir("fair_server", debugfs_sched);` … `debugfs_create_file("runtime", 0644, d_cpu, (void *) cpu, &fair_server_runtime_fops);` / `debugfs_create_file("period", 0644, d_cpu, (void *) cpu, &fair_server_period_fops);`; `debug.c:648@v7.2`: `debugfs_create_u32("base_slice_ns", 0644, debugfs_sched, &sysctl_sched_base_slice);`
  - `sched-deadline.rst:603-610@v7.2`: ` This means that, for a root_domain comprising M CPUs, -deadline tasks` / ` can be created while the sum of their bandwidths stays below:` / `   M * (sched_rt_runtime_us / sched_rt_period_us)` / ` It is also possible to disable this bandwidth management logic, and` / ` be thus free of oversubscribing the system up to any arbitrary level.` / ` This is done by writing -1 in /proc/sys/kernel/sched_rt_runtime_us.`
  - `sched-deadline.rst:651-656@v7.2`:
    ```
     The default value for SCHED_DEADLINE bandwidth is to have rt_runtime equal to
     950000. With rt_period equal to 1000000, by default, it means that -deadline
     tasks can use at most 95%, multiplied by the number of CPUs that compose the
     root_domain, for each root_domain.
     This means that non -deadline tasks will receive at least 5% of the CPU time,
    ```
- Coverage: T5 covers — SCHED_DEADLINE admission cap = M × runtime/period per root domain (doc default 95 %). T6 covers — fair server (from v6.12): a per-CPU deferred deadline server for fair tasks with runtime 50 ms per period 1000 ms (ns constants), tunable in debugfs `sched/fair_server/cpuX/{runtime,period}`; at v7.2 a second per-CPU `ext_server` for sched_ext tasks with the same 50 ms / 1000 ms. The doc does not state a latency bound in words; that the fair class gets ≥ 50 ms per 1 s under RT load is the reader's reading of the parameters. Not an observation.

### S2-06 — Linux nice weights and SCHED_IDLE weight: `kernel/sched/core.c`, `kernel/sched/sched.h`, `Documentation/scheduler/sched-design-CFS.rst`, `sched-eevdf.rst`

- Copies (raw.githubusercontent.com, accessed 2026-09-24): `core.c@v7.2` `957f657af1a2327c75dac495548eaa7bd1571a12a756c7f704e6f3195b156988`; `sched.h@v7.2` `44e7152a593bade4e4079d37f7947cb5e122c6241e3b5497e20a49c8d636cb50`; `sched-design-CFS.rst@v6.5` `0fba6eea1d658e4a6f0afbc6ba767600474cbfcf3ef3ec71c72485be7e7200e3`; `sched-design-CFS.rst@v7.2` `25a5fa2bf66e2a076aaac1492f306bd6c92d1c5b399976831e637c30072e76b7`; `sched-eevdf.rst@v7.2` `75b99048d738b7683d06c5844e150253e91d75ec46e774f7a96cf0e9d39056a0`. (Same `WEIGHT_IDLEPRIO 3` at `sched.h:2313@v6.12`.)
- Verbatim passages:
  - `core.c:10594-10615@v7.2`:
    ```
    /*
     * Nice levels are multiplicative, with a gentle 10% change for every
     * nice level changed. I.e. when a CPU-bound task goes from nice 0 to
     * nice 1, it will get ~10% less CPU time than another CPU-bound task
     * that remained on nice 0.
     *
     * The "10% effect" is relative and cumulative: from _any_ nice level,
     * if you go up 1 level, it's -10% CPU usage, if you go down 1 level
     * it's +10% CPU usage. (to achieve that we use a multiplier of 1.25.
     * If a task goes up by ~10% and another task goes down by ~10% then
     * the relative distance between them is ~25%.)
     */
    const int sched_prio_to_weight[40] = {
     /* -20 */     88761,     71755,     56483,     46273,     36291,
     /* -15 */     29154,     23254,     18705,     14949,     11916,
     /* -10 */      9548,      7620,      6100,      4904,      3906,
     /*  -5 */      3121,      2501,      1991,      1586,      1277,
     /*   0 */      1024,       820,       655,       526,       423,
     /*   5 */       335,       272,       215,       172,       137,
     /*  10 */       110,        87,        70,        56,        45,
     /*  15 */        36,        29,        23,        18,        15,
    };
    ```
  - `sched.h:2511-2512@v7.2`: `#define WEIGHT_IDLEPRIO		3` / `#define WMULT_IDLEPRIO		1431655765`
  - `core.c:1529-1535@v7.2`: `if (task_has_idle_policy(p)) {` / `lw.weight = scale_load(WEIGHT_IDLEPRIO);` / `lw.inv_weight = WMULT_IDLEPRIO;` / `} else {` / `lw.weight = scale_load(sched_prio_to_weight[prio]);`
  - `sched-design-CFS.rst:139-141@v7.2`: `  - SCHED_IDLE: This is even weaker than nice 19, but its not a true` / `    idle timer scheduler in order to avoid to get into priority` / `    inversion problems which would deadlock the machine.`
  - `sched-design-CFS.rst:98-108@v7.2`: `only one central tunable:` / `   /sys/kernel/debug/sched/base_slice_ns` / `which can be used to tune the scheduler from "desktop" (i.e., low latencies) to` / `"server" (i.e., good batching) workloads.  It defaults to a setting suitable` / `for desktop workloads.  SCHED_BATCH is handled by the CFS scheduler module too.` / `In case CONFIG_HZ results in base_slice_ns < TICK_NSEC, the value of` / `base_slice_ns will have little to no impact on the workloads.`
  - `sched-design-CFS.rst:95-97@v6.5`: `only one central tunable (you have to switch on CONFIG_SCHED_DEBUG):` / `   /sys/kernel/debug/sched/min_granularity_ns`
  - `sched-eevdf.rst:30-32@v7.2`: `reset. Finally, tasks can preempt others if their VD is earlier, and tasks` / `can request specific time slices using the new sched_setattr() system call,` / `which further facilitates the job of latency-sensitive applications.`
- Coverage: T9 covers — CPU-share weights: nice 0 = 1024, nice 19 = 15, SCHED_IDLE = 3 (dimensionless load weights); two CPU-bound tasks share by weight ratio (reader's arithmetic: SCHED_IDLE vs nice 0 → 3/1027 ≈ 0.3 %; nice 19 vs nice 0 → 15/1039 ≈ 1.4 %). Combined with S2-01 for preemption. T3 (partial) — doc names `base_slice_ns` as the tunable and warns that below the tick it has little effect. No wake-up-latency value is documented. Not an observation.

### S2-07 — Linux man-pages, `sched(7)`

- Copy: git.kernel.org/pub/scm/docs/man-pages/man-pages.git, `plain/man/man7/sched.7?h=man-pages-6.19` (tag commit `adb436b2e4471218021d86f188fb58dec3946eb8`), accessed 2026-09-24, `sources/S2-07/sched.7@man-pages-6.19`, SHA-256 `8d26147f08576c35d6d851f48779d62aa5baa79334fe195bfc8247f0e0639b16`.
- Verbatim passages:
  - `sched.7:520-531`: `.SS SCHED_IDLE: Scheduling very low priority jobs` / `(Since Linux 2.6.23.)` / `.B SCHED_IDLE` / `can be used only at static priority 0;` / `the process nice value has no influence for this policy.` / `.P` / `This policy is intended for running jobs at extremely low` / `priority (lower even than a +19 nice value with the` / `.B SCHED_OTHER` / `or` / `.B SCHED_BATCH` / `policies).`
  - `sched.7:473-483`: `With the advent of the CFS scheduler in Linux 2.6.23,` / `Linux adopted an algorithm that causes` / `relative differences in nice values to have a much stronger effect.` / `In the current implementation, each unit of difference in the` / `nice values of two processes results in a factor of 1.25` / `in the degree to which the scheduler favors the higher priority process.` / `This causes very low nice values (+19) to truly provide little CPU` / `to a process whenever there is any other` / `higher priority load on the system,` / `and makes high nice values (\-20) deliver most of the CPU to applications` / `that require it (e.g., some audio applications).`
  - `sched.7:699-719`: `.I /proc/sys/kernel/sched_rt_period_us` … `The default value in this file is 1,000,000 (1 second).` … `.I /proc/sys/kernel/sched_rt_runtime_us` / `The value in this file specifies how much of the "period" time` / `can be used by all real-time and deadline scheduled processes` / `on the system.` … `The default value in this file is 950,000 (0.95 seconds),` / `meaning that 5% of the CPU time is reserved for processes that` / `don't run under a real-time or deadline scheduling policy.`
- Coverage: T9 covers (SCHED_IDLE below nice 19; nice ratio 1.25 per step; no latency statement). T5/T6 covers (RT/deadline 95 % default, 5 % reserved for others, as documented in man-pages-6.19). Not an observation.

### S2-08 — illumos-gate TS class source: `ts_dptbl.c`, `ts.c`, `sys/ts.h`, `conf/param.c`

- Copies: `git clone --filter=blob:none --sparse https://github.com/illumos/illumos-gate` at master `6b5b8c9e2606b0efc5a90af41eefff9725bea618` (committed 2026-09-23), accessed 2026-09-24. `S2-08/ts_dptbl.c` (`usr/src/uts/common/disp/ts_dptbl.c`) `04e8bf7a6be4f95ee12e5e9782db8727cae504d45348c89fd9676ad50095f711`; `S2-08/ts.c` (`usr/src/uts/common/disp/ts.c`) `52dc668973b758f9a13d760cd3989498c00ada0bb6b3c5ac45362d91764e67d8`; `S2-08/ts.h` (`usr/src/uts/common/sys/ts.h`) `b16004f5b06da766c7c1a964f752a79210210f38be18efa331c62b897b75052f`; `S2-08/param.c` (`usr/src/uts/common/conf/param.c`) `7e876a808d523e51359d114e0d7d2a4d9f8e74937d64f07016cb47b8d54480ed`. History: `git log -- usr/src/uts/common/disp/ts_dptbl.c` → only `bbf215553c 2022-02-26 14443 resection manual pages per IPD4` and `7c478bd953 2005-06-14 OpenSolaris Launch`; hires tick default by `d96925c4917df4be0de8533ddaa487c9d915b8c5` (Richard Lowe, 2020-08-17, "11499 default to hires tick").
- Verbatim passages:
  - `ts_dptbl.c:96-160` (default table; excerpt of rows, all rows quoted by level range as in file):
    ```
    tsdpent_t	config_ts_dptbl[] = {

    /*	glbpri		qntm	tqexp	slprt	mxwt	lwt */

    	TSGPUP0+0,	20,	 0,	50,	    0,	50,
    ...
    	TSGPUP0+9,	20,	 0,	50,	    0,	50,
    	TSGPUP0+10,	16,	 0,	51,	    0,	51,
    	TSGPUP0+11,	16,	 1,	51,	    0,	51,
    ...
    	TSGPUP0+20,	12,	10,	52,	    0,	52,
    ...
    	TSGPUP0+30,	 8,	20,	53,	    0,	53,
    ...
    	TSGPUP0+40,	 4,	30,	55,	    0,	55,
    ...
    	TSGPUP0+58,	 4,	48,	58,	    0,	59,
    	TSGPUP0+59,	 2,	49,	59,	32000,	59
    };
    ```
    (Full: levels 0–9 qntm 20; 10–19 qntm 16; 20–29 qntm 12; 30–39 qntm 8; 40–58 qntm 4; 59 qntm 2. mxwt 0 for levels 0–58, 32000 for level 59. lwt 50 (0–9), 51 (10–19), 52 (20–29), 53 (30–34), 54 (35–39), 55 (40–44), 56 (45), 57 (46), 58 (47–48), 59 (49–59).)
  - `ts_dptbl.c:162-166`: `* config_ts_dptbl_server[] is an alternate dispatch table that may` / `* deliver better performance on large server configurations.`; `ts_dptbl.c:247-257`: `if (ts_dispatch_extended == -1)` / `ts_dispatch_extended = 0;` … `if (ts_dispatch_extended)` / `return (config_ts_dptbl_server);` / `else` / `return (config_ts_dptbl);`
  - `ts.h:46-57`:
    ```
    typedef struct tsdpent {
    	pri_t	ts_globpri;	/* global (class independent) priority */
    	int	ts_quantum;	/* time quantum given to procs at this level */
    	pri_t	ts_tqexp;	/* ts_umdpri assigned when proc at this level */
    				/*   exceeds its time quantum */
    	pri_t	ts_slpret;	/* ts_umdpri assigned when proc at this level */
    				/*  returns to user mode after sleeping */
    	short	ts_maxwait;	/* bumped to ts_lwait if more than ts_maxwait */
    				/*  secs elapse before receiving full quantum */
    	short	ts_lwait;	/* ts_umdpri assigned if ts_dispwait exceeds  */
    				/*  ts_maxwait */
    } tsdpent_t;
    ```
  - `ts.c:1668`: `if (--tspp->ts_timeleft <= 0) {` (in `ts_tick`, i.e. quantum counted in clock ticks)
  - `ts.c:1777-1780`: ` * Update the ts_dispwait values of all time sharing threads that` / ` * are currently runnable at a user mode priority and bump the priority` / ` * if ts_dispwait exceeds ts_maxwait.  Called once per second via` / ` * timeout which we reset here.`; `ts.c:1825`: `(void) timeout(ts_update, arg, hz);`
  - `ts.c:1856-1858`: `tspp->ts_dispwait++;` / `if (tspp->ts_dispwait <= ts_dptbl[tspp->ts_umdpri].ts_maxwait)` / `goto next;`; `ts.c:1868-1870`: `tspp->ts_cpupri = ts_dptbl[tspp->ts_cpupri].ts_lwait;` / `TS_NEWUMDPRI(tspp);` / `tspp->ts_dispwait = 0;`
  - `param.c:132-135`: ` * hz is 100, but we set hires_tick to get higher resolution clock behavior` / ` * (currently defined to be 1000 hz).  Higher values seem to work, but are not` / ` * supported.`; `param.c:159,165`: `#define	HIRES_HZ_DEFAULT	1000` … `int hires_tick = 1;`
- Coverage: T3 covers — default TS table: 60 levels (0–59); quantum in clock ticks: 20 (levels 0–9) … 2 (level 59); tick rate `hz` = 1000 by default (`hires_tick = 1` since commit d96925c, 2020), 100 if `hires_tick=0`. Reader's arithmetic, not stated in source: at hz 1000 the default quanta are 20 ms … 2 ms; at hz 100, 200 ms … 20 ms. Quanta therefore scale with tick rate (not with CPU count); the table itself is unchanged since the 2005 OpenSolaris import. T6 covers — aging: `ts_update` once per second increments `ts_dispwait`; if it exceeds `ts_maxwait` (0 s for levels 0–58, 32000 s for 59) the thread moves to `ts_lwait` (levels 50–59): i.e. a runnable TS thread at level ≤58 is raised after at most ~1–2 s of waiting (reader's reading of `>` with once-per-second increments). Not an observation.

### S2-09 — illumos manual page `ts_dptbl(5)`

- Copies (accessed 2026-09-24): `usr/src/man/man5/ts_dptbl.5` at illumos-gate `6b5b8c9e2606b0efc5a90af41eefff9725bea618` (raw.githubusercontent.com) → `S2-09/ts_dptbl.5`, SHA-256 `52e3eeeae4ffde6cffe194a9df1d003ba6208f32051f4438185a53ade1a796aa`, header `.TH TS_DPTBL 5 "Feb 17, 2023"`; `https://illumos.org/man/5/ts_dptbl` → `S2-09/ts_dptbl-illumos-org.html`, `d44f5d8f59c6f78f05b6327226f83898104a63f6d1459cb2192e0c1a0b50e8c6` (footer "illumos February 17, 2023", same text).
- Verbatim passages (`ts_dptbl.5` line numbers):
  - `:63-70`: `The length of the time quantum allocated to processes at this level in ticks` / `(\fBhz\fR).` / `.sp` / `In the default high resolution clock mode (\fBhires_tick\fR set to \fB1\fR),` / `the value of \fBhz\fR is set to \fB1000\fR.  If this value is overridden to` / `\fB0\fR then \fBhz\fR will instead be \fB100\fR; the number of ticks per` / `quantum must then be decreased to maintain the same length of quantum in` / `absolute time.`
  - `:102-109`: `A per process counter, \fBts_dispwait\fR is initialized to zero each time a` / `time-sharing or inter-active process is placed back on the dispatcher queue` / `after its time quantum has expired or when it is awakened (\fBts_dispwait\fR is` / `not reset to zero when a process is preempted by a higher priority process).` / `This counter is incremented once per second for each process on a dispatcher or` / `sleep queue. If a process' \fBts_dispwait\fR value exceeds the \fBts_maxwait\fR` / `value for its level, the process' priority is changed to that indicated by` / `\fBts_lwait\fR. The purpose of this field is to prevent starvation.`
  - `:196-213` (Example 1, "A Sample From a Configuration File"): `# Time-Sharing Dispatcher Configuration File RES=1000` … `500            0        10         5           10        # 0` … `50             49       59         5           59        # 59`
  - `:336-338` (Example 2 module source): `/*  glbpri  qntm  tqexp  slprt  mxwt  lwt  */` / `    0,      100,  0,     10,    5,    10,`
- Coverage: T3/T6 covers the units (ticks of `hz`; hz 1000 default; `ts_dispwait` +1 per second; `ts_maxwait` compared in seconds, purpose "to prevent starvation"). The man page's example tables (500 ms…50 ms, maxwait 5; and a module example 100…10 ticks) are samples and differ from the shipped `config_ts_dptbl` (S2-08); the man page does not print the shipped default table. Not an observation.

### S2-10 — MINIX 3 scheduler (`minix/servers/sched/schedule.c`, `minix/include/minix/config.h`, `minix/kernel/system.c`, `minix/servers/pm/schedule.c`)

- Copies: github.com/Stichting-MINIX-Research-Foundation/minix at HEAD `4db99f4012570a577414fe2a43697b2f239b699e` (raw + sparse clone), accessed 2026-09-24. `S2-10/sched-schedule.c` `8b6e0f193dcc57788f58b50c8295612b589c4bd6e3f9e42469b546eacffef1a0`; `S2-10/config.h` `d51c1a13db408f7756edbb2ecef1e3d4a693eb708c85676faf39a729597d6b55`; `S2-10/kernel-system.c` `862f934ba09262926c9f36b82a85c2bf1cf6fabd4f2c075d799836fca52e5b95`; `S2-10/pm-schedule.c` `56e2b3b7e312936caf72c2569f10213c306b80eda1e6fc8df8a19d5d1b471188`. (Tag v3.3.0 = `1ac531398bb6ab61a6ff5b18f73a75387053cbd9`; not read — HEAD read.)
- Verbatim passages:
  - `config.h:63-74`:
    ```
    /* Scheduling priorities. Values must start at zero (highest
     * priority) and increment.
     */
    #define NR_SCHED_QUEUES   16	/* MUST equal minimum priority + 1 */
    #define TASK_Q		   0	/* highest, used for kernel tasks */
    #define MAX_USER_Q  	   0    /* highest priority for user processes */   
    #define USER_Q  	  ((MIN_USER_Q - MAX_USER_Q) / 2 + MAX_USER_Q) /* default
    						(should correspond to nice 0) */
    #define MIN_USER_Q	  (NR_SCHED_QUEUES - 1)	/* minimum priority for user
    						   processes */
    /* default scheduling quanta */
    #define USER_QUANTUM 200
    ```
  - `sched-schedule.c:18`: `#define BALANCE_TIMEOUT	5 /* how often to balance queues in seconds */`; `:41`: `#define DEFAULT_USER_TIME_SLICE 200`
  - `sched-schedule.c:99-101`: `if (rmp->priority < MIN_USER_Q) {` / `rmp->priority += 1; /* lower priority */` / `}` (in `do_noquantum`)
  - `sched-schedule.c:338`: `balance_timeout = BALANCE_TIMEOUT * sys_hz();`
  - `sched-schedule.c:348-351`: `/* This function in called every N ticks to rebalance the queues. The current` / ` * scheduler bumps processes down one priority when ever they run out of` / ` * quantum. This function will find all proccesses that have been bumped down,` / ` * and pulls them back up. This default policy will soon be changed.`; `:360-361`: `if (rmp->priority > rmp->max_priority) {` / `rmp->priority -= 1; /* increase priority */`
  - `kernel-system.c:682-684`: `if (quantum != -1) {` / `p->p_quantum_size_ms = quantum;` / `p->p_cpu_time_left = ms_2_cpu_time(quantum);`
  - `pm-schedule.c:40-41`: `USER_Q, 		/* maxprio */` / `USER_QUANTUM, 		/* quantum */`
- Coverage: T3 covers — 16 queues (0 = highest); default user queue 7 (reader's arithmetic of `(15-0)/2+0`); user quantum 200 ms (unit from `p_quantum_size_ms`), fixed per process (no per-level growth, no CPU-count or clock scaling; converted to CPU time); on quantum expiry priority lowered by one queue; every 5 s (`BALANCE_TIMEOUT * sys_hz()` ticks) each bumped-down process is raised by one queue. Not an observation.

### S2-11 — scx_lavd (sched-ext/scx)

- Copies: `git clone --depth 1 https://github.com/sched-ext/scx` at `00fec1e7a755028718e4b371df97360cf66b3a62` (committed 2026-09-23; newest tag v1.1.3 not checked out), accessed 2026-09-24. `S2-11/main.rs` (`scheds/rust/scx_lavd/src/main.rs`) `930d8782faff4abba347442b62b2cce2c89d49a5ff975a64b370bd473356e552`; `S2-11/lavd.bpf.h` `94e44ecdb58898bb0e5bd263d66f3e405fef262cf539c6a4c4df25c554f6c536`; `S2-11/main.bpf.c` `bbce8fcd2703ae3474d838c780750a8494ed5dca1e6e9c898d502f3aadb1500e`; `S2-11/sys_stat.bpf.c` `1276bc87378cc3ad09f5075999b08f8c538908d6e50048fd7566c0964668b04c`; `S2-11/intf.h` `f0c729483dc43f1be206b122e18e4dda97f1a055cfcd3c647eb57adf62c95454`.
- Verbatim passages:
  - `lavd.bpf.h:73-75`: `LAVD_TARGETED_LATENCY_NS	= (10ULL * NSEC_PER_MSEC),` / `LAVD_SLICE_MIN_NS_DFL		= (500ULL * NSEC_PER_USEC), /* min time slice */` / `LAVD_SLICE_MAX_NS_DFL		= (5ULL * NSEC_PER_MSEC), /* max time slice */`
  - `main.rs:123-129`: `/// Maximum scheduling slice duration in microseconds.` / `#[clap(long = "slice-max-us", default_value = "5000")]` / `slice_max_us: u64,` / `/// Minimum scheduling slice duration in microseconds.` / `#[clap(long = "slice-min-us", default_value = "500")]`
  - `sys_stat.bpf.c:764-776`:
    ```
    	/*
    	 * Given the updated state, recalculate the time slice for the next
    	 * round. The time slice should be short enough to schedule all
    	 * runnable tasks at least once within a targeted latency using the
    	 * active CPUs.
    	 */
    	nr_q = sys_stat.nr_queued_task;
    	if (nr_q > 0) {
    		slice_wall = (LAVD_TARGETED_LATENCY_NS * sys_stat.nr_active) / nr_q;
    		slice_wall = clamp(slice_wall, slice_min_ns, slice_max_ns);
    	} else {
    		slice_wall = slice_max_ns;
    	}
    ```
  - `intf.h:70`: `u32	nr_active;	/* number of active CPUs */`
  - `main.bpf.c:2900`: `.timeout_ms		= 30000U,`
- Coverage: T3 covers — slice = 10 ms targeted latency × active CPUs ÷ queued tasks, clamped to [0.5 ms, 5 ms] (defaults; ns in BPF, µs on CLI); scales with number of active CPUs and queue length; not with clock rate; boosted slices for long-running/latency-critical tasks (`calc_time_slice`, `main.bpf.c:299ff`). T6: watchdog timeout set to 30 000 ms. Not an observation.

### S2-12 — scx_bpfland (sched-ext/scx)

- Copies: same scx commit `00fec1e7a755028718e4b371df97360cf66b3a62`, accessed 2026-09-24. `S2-12/main.rs` (`scheds/rust/scx_bpfland/src/main.rs`) `db6be026f236142fb7c2fa82f4e3a5771dd876b9c56991b86bb3ec01c725e2bd`; `S2-12/main.bpf.c` `dc1def7a90bebed25cb7d93ee49600b7cc3be9c7b2552cf398109636cf7d2aec`.
- Verbatim passages:
  - `main.bpf.c:10-13`: ` * Maximum time a task can wait in the scheduler's queue before triggering` / ` * a stall.` / ` */` / `#define STARVATION_MS	5000ULL`
  - `main.bpf.c:42-59`: `/*` / ` * Default task time slice.` / ` */` / `const volatile u64 slice_max = 1ULL * NSEC_PER_MSEC;` / … ` * Default minimum time slice.` / ` */` / `const volatile u64 slice_min;` / … `const volatile u64 slice_lag = 40ULL * NSEC_PER_MSEC;`
  - `main.bpf.c:729-736`: `	 * Adjust time slice in function of the task's priority and the` / `	 * amount of tasks waiting to be dispatched, but never assign a` / `	 * time slice smaller than @slice_min.` / `	 */` / `	slice = scale_by_task_weight(p, slice_max) / MAX(nr_wait, 1);` / `` / `	return MAX(slice, slice_min);`
  - `main.rs:95-107`: `/// Maximum scheduling slice duration in microseconds.` / `#[clap(short = 's', long, default_value = "1000")]` … `/// Minimum scheduling slice duration in microseconds (0 = no minimum time slice).` / `#[clap(short = 'L', long, default_value = "0")]` … `/// Maximum time slice lag in microseconds.` … `#[clap(short = 'l', long, default_value = "40000")]`
  - `main.bpf.c:1408`: `.timeout_ms		= STARVATION_MS,`
- Coverage: T3 covers — default max slice 1 ms, min 0, lag 40 ms; slice = weight-scaled 1 ms ÷ tasks waiting on the CPU/node DSQs (scales with queue length and task weight, not CPU count or clock). T6 covers — sched_ext watchdog timeout set to 5000 ms. Not an observation.

### S2-13 — scx_rusty (sched-ext/scx)

- Copies: same scx commit, accessed 2026-09-24. `S2-13/main.rs` `2b848536278341c9f07aca1215c645d7186dbdcf9fe6d5421299c9f9ba6675f5`; `S2-13/tuner.rs` `16108bb9809ff05c2fe3e7f69a886cf19dd981fda85fafd4196c88e09f47a6c3`; `S2-13/main.bpf.c` `d7542e68a73f19c57ff9bc608129e613bff85ee654a56afb36c4013e942d2af4`.
- Verbatim passages:
  - `main.rs:97-103`: `/// Scheduling slice duration for under-utilized hosts, in microseconds.` / `#[clap(short = 'u', long, default_value = "20000")]` / `slice_us_underutil: u64,` / `` / `/// Scheduling slice duration for over-utilized hosts, in microseconds.` / `#[clap(short = 'o', long, default_value = "1000")]`
  - `tuner.rs:139`: `self.fully_utilized = avg_util >= 0.99999;`; `tuner.rs:173-176`: `if self.fully_utilized {` / `self.slice_ns = self.overutil_slice_ns;` / `} else {` / `self.slice_ns = self.underutil_slice_ns;`
  - `main.bpf.c:2017`: `.timeout_ms		= 10000,`
- Coverage: T3 covers — 20 ms slice when the host is not fully utilized, 1 ms when average utilization ≥ 0.99999; no CPU-count or clock scaling. T6: watchdog timeout 10 000 ms. Not an observation.

### S2-14 — rt-app (`doc/tutorial.txt`, `src/rt-app.c`)

- Copies: `git clone --depth 1 https://github.com/scheduler-tools/rt-app` at `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e` (committed 2026-06-10), accessed 2026-09-24. `S2-14/tutorial.txt` `a3e8823ebae6fda9893327637a48ab195f98206b00ad857a8cc736414d9ee3e7`; `S2-14/rt-app.c` `61431c72171ee3234e8c7f0dfc2b7f7354beebd8d8850a4e30f5837616666eb8`.
- Verbatim passages:
  - `tutorial.txt:447-452`: `* timer : Object. Emulate the wake up of the thread by a timer. Timer differs` / `from sleep event by the start time of the timer duration. Sleep duration starts` / `at the beginning of the sleep event whereas timer duration starts at the end of` / `the last use of the timer. So Timer event are immunized against preemption,` / `frequency scaling and computing capacity of a CPU. The initial starting time of` / `the timer is set during the 1st use of the latter.`
  - `tutorial.txt:507-509`: `Timers can work with a "relative" or an "absolute" reference. By default they` / `work in "relative" mode, but this mode can also be explicitly specified as the` / `following:`
  - `tutorial.txt:518-522`: `"relative" mode means that the reference for setting the next timer event is` / `relative to the end of the current phase. This in turn means that if, for some` / `reason (i.e., clock frequency was too low), events in a certain phase took too` / `long to execute and the timer of that phase couldn't actually fire at all, the` / `next phase won't be affected. For example:`
  - `tutorial.txt:534-536`: `In this example character "o" denotes when phases finish/start. Third` / `activation of Timer0 is missed, since r0 executed for more that 20ms. However` / `the next phase is not affected as Timer0 was set considering the instant of` / `time when the misbehaving r0 finished executing.`
  - `tutorial.txt:548-553`: `"absolute" mode means that the reference for setting the next timer event is` / `fixed and always consider the starting time of the first phase. This means that` / `if, for some reason (i.e., clock frequency was too low), events in a certain` / `phase took too long to execute and the timer of that phase couldn't actually` / `fire at all, the next phase (and potentially other subsequent phases) _will_ be` / `affected. For example, considering again the example above:`
  - `tutorial.txt:565-569`: `Third activation of Timer0 is missed, since r0 executed for more that 20ms.` / `Even if 4th activation of r0 executes for 10ms (as specified in the` / `configuration), 4th Timer0 is still missed because the reference didn't change.` / `In this example 5th activation of r0 then managed to recover, but in general it` / `depends on how badly a certain phase misbehaves.`
  - `rt-app.c:582-597`:
    ```
    			rdata->res.timer.t_next = timespec_add(&rdata->res.timer.t_next, &t_period);
    			clock_gettime(CLOCK_MONOTONIC, &t_now);
    			t_slack = timespec_sub(&rdata->res.timer.t_next, &t_now);
    			if (opts.cumulative_slack)
    				ldata->slack += timespec_to_usec_long(&t_slack);
    			else
    				ldata->slack = timespec_to_usec_long(&t_slack);
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
- Coverage: T7 covers — on an overrun (now ≥ next activation) rt-app does not sleep; in "relative" mode (default) it re-anchors the next activation to "now" (the missed activation is skipped, no backlog); in "absolute" mode the reference stays on the original grid, so subsequent activations run back-to-back until caught up (backlog/catch-up); slack is recorded negative. Not an observation (the tutorial diagrams are illustrative).

### S2-15 — interbench (`interbench.c`, `interbench.8`, `readme`)

- Copies: `git clone https://github.com/ckolivas/interbench` at `e612a65ce941028ddea804e6b45ccde2750720d2` (committed 2016-10-24; tag `v0.31` exists), accessed 2026-09-24. `S2-15/interbench.c` `a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191`; `S2-15/interbench.8` `31bc88e508bb7f81cc01a4ef632fbee4f4acb908082140427acba11ca2ee92ee` (header `.TH interbench "8" "March 2006" "Interbench 0.31"`); `S2-15/readme` `a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29`.
- Verbatim passages:
  - `interbench.c:489-491`: `#define AUDIO_INTERVAL	(50000)` / `#define AUDIO_RUN	(AUDIO_INTERVAL / 20)` / `/* We emulate audio by using 5% cpu and waking every 50ms */`; `:510-512`: `/* We emulate video by using 40% cpu and waking for 60fps */` / `#define VIDEO_INTERVAL	(1000000 / 60)` / `#define VIDEO_RUN	(VIDEO_INTERVAL * 40 / 100)`
  - `interbench.c:398-411`:
    ```
    	current_time = get_usecs(&myts);
    	if (interval_usecs && current_time > deadline + interval_usecs) {
    		/* We missed the deadline even before we consumed cpu */
    		unsigned long intervals;

    		deadline += interval_usecs;
    		intervals = (current_time - deadline) /
    			interval_usecs + 1;

    		tb->missed_deadlines += intervals;
    		missed_latency = intervals * interval_usecs;
    		deadline += intervals * interval_usecs;
    		tb->missed_burns += intervals;
    		goto bypass_burn;
    	}
    ```
  - `interbench.c:418-436`:
    ```
    	/*
    	 * If we meet the deadline we move the deadline forward, otherwise
    	 * we consider it a missed deadline and dropped frame etc.
    	 */
    	deadline += interval_usecs;
    	if (deadline >= current_time) {
    		tb->deadlines_met++;
    	} else {
    		if (interval_usecs) {
    			unsigned long intervals = (current_time - deadline) /
    				interval_usecs + 1;
    	
    			tb->missed_deadlines += intervals;
    			missed_latency = intervals * interval_usecs;
    			deadline += intervals * interval_usecs;
    			if (intervals > 1)
    				tb->missed_burns += intervals;
    ```
  - `interbench.c:77`: `.duration = 30,`; `interbench.8:14`: `\fB\-t\fR     Seconds to run each benchmark (default: 30)`
  - `interbench.8:152-160`: `1. The average scheduling latency (time to requesting cpu till actually getting it) of deadlines met during the test period.` / `2. The scheduling jitter is represented by calculating the standard deviation of the latency` / `3. The maximum latency seen during the test period` / `4. Percentage of desired cpu` / `5. Percentage of deadlines met.`
  - `interbench.8:190-195`: `This means that some deadlines were so late (%deadlines met was low) that some` / `redraws were dropped entirely to catch up. In X terms this would translate into` / `jerky movement, in audio it would be a skip, and in video it would be a dropped` / `frame. Note that despite the massive maximum latency of >3seconds, the average` / `latency is still less than 30ms. This is because redraws are dropped in order` / `to catch up usually by these sorts of applications.`
  - `interbench.8:206-209` (identical at `readme:160-163`): `in window movement under X. The magnitude of these would be best represented by` / `the maximum latency. When the deadlines are actually met, the average latency` / `represents how "smooth" it would look. Average humans' limit of perception for` / `jitter is in the order of 7ms. Trained audio observers might notice much less.`
  - `interbench.8:168-182` (sample output): `Load    Latency +/- SD (ms)  Max Latency   % Desired CPU  % Deadlines Met` / `None      0.495 +/- 0.495         45             100             96` / … `Burn       27.9 +/- 28.1        3335            78.5             44`
- Coverage: T7 covers — audio 50 ms period, 5 % CPU; video 1/60 s period, 40 % CPU; a missed period is counted as missed deadline(s) and the deadline is advanced by whole intervals past "now" (skip to the next period on the original grid, no backlog; if missed before running, the burn is skipped). T8 covers — per benchmarked task × load: mean latency, SD (jitter), max latency, % desired CPU, % deadlines met; default 30 s per benchmark; states "Average humans' limit of perception for jitter is in the order of 7ms" with no source cited in the man page, readme or code (grep of `readme`, `readme.interactivity`, `interbench.c` found no reference). The man-page sample table is one run with machine, kernel and date not named. Documentation/source otherwise.

### S2-16 — mpv (`DOCS/man/options.rst`, `player/video.c`, `video/out/vo.c`)

- Copies: sparse clone of github.com/mpv-player/mpv at `2a4eb8067ca68ec19adf23daf8ccbb1a05afd6ed` (committed 2026-09-23; newest tag v0.41.0), accessed 2026-09-24. `S2-16/options.rst` `e78aabb4a03f4cc3dfcf3221cd499a792a5914fedc3f272b088d1023418084fd`; `S2-16/video.c` `3ccce2b694041ac12aab56fee803b06fba695ffb3f848f915e1acc7d2f5e632b`; `S2-16/vo.c` `8504b70c5ec07cb79f6fc4b5c7e332eb46376a97539feaaef2bfcd2e1adacbd1`.
- Verbatim passages:
  - `options.rst:1248-1265`: ``` ``--framedrop=<mode>`` ``` / `    Skip displaying some frames to maintain A/V sync on slow systems, or` / `    playing high framerate video on video outputs that have an upper framerate` / `    limit.` … `    <vo>` / `        Drop late frames on video output (default). This still decodes and` / `        filters all frames, but doesn't render them on the VO. Drops are` / `        indicated in the terminal status line as ``Dropped:`` field.` / `` / `        In audio sync. mode, this drops frames that are outdated at the time of` / `        display. If the decoder is too slow, in theory all frames would have to` / `        be dropped (because all frames are too late) - to avoid this, frame` / `        dropping stops  if the effective framerate is below 10 FPS.`
  - `vo.c:955-963`:
    ```
        // "normal" strict drop threshold.
        in->dropped_frame = duration >= 0 && end_time < now;

        in->dropped_frame &= !frame->display_synced;
        in->dropped_frame &= !(vo->driver->caps & VO_CAP_FRAMEDROP);
        in->dropped_frame &= frame->can_drop;
        // Even if we're hopelessly behind, rather degrade to 10 FPS playback,
        // instead of just freezing the display forever.
        in->dropped_frame &= now - in->prev_vsync < MP_TIME_MS_TO_NS(100);
    ```
  - `video.c:867-870`: `    // If we are too far ahead/behind, attempt to drop/repeat frames.` / `    // Tolerate some desync to avoid frame dropping due to jitter.` / `    if (drop && fabs(av_diff) >= 0.020 && fabs(av_diff) / vsync >= 1)` / `        drop_repeat = -av_diff / vsync; // round towards 0`
  - `video.c:338-340`: `        // try to drop as many frames as we appear to be behind` / `        mp_decoder_wrapper_set_frame_drops(vo_c->track->dec,` / `            MPCLAMP((mpctx->last_av_difference - 0.010) / frame_time, 0, 100));`
- Coverage: T7 covers — default `vo` mode: a frame whose end time is already past at display is dropped (skip, not rendered late), except it renders at least one frame per 100 ms (≥10 FPS floor); display-sync mode drops/repeats vsyncs when A/V difference ≥ 20 ms; decoder mode drops as many frames as behind (minus 10 ms). Not an observation.

### S2-17 — GStreamer base sink / video sink / audio base sink

- Copies: gitlab.freedesktop.org/gstreamer/gstreamer main `83e7df9168dd73f5dcd1caa60195a9d9dce558b4`, `-/raw/<commit>/…`, accessed 2026-09-24. `S2-17/gstbasesink.c` (`subprojects/gstreamer/libs/gst/base/gstbasesink.c`) `43a7223ce9ab63dc0bae4868f0660d6bf3e4e3201cf883eaee21cac2addd14c7`; `S2-17/gstvideosink.c` (`subprojects/gst-plugins-base/gst-libs/gst/video/gstvideosink.c`) `cbaceaada60cad03ecf75d397eb529d82ede5d15d5dd57cbdb7134e62b65c30c`; `S2-17/gstaudiobasesink.c` `fed32b304347841782073687305c63d81fd208509c4404dc870d25680656457b`.
- Verbatim passages:
  - `gstbasesink.c:118-129`: ` * The #GstBaseSink:max-lateness property affects how the sink deals with` / ` * buffers that arrive too late in the sink. A buffer arrives too late in the` / ` * sink when the presentation time (as a combination of the last segment, buffer` / ` * timestamp and element base_time) plus the duration is before the current` / ` * time of the clock.` / ` * If the frame is later than max-lateness, the sink will drop the buffer` / ` * without calling the render method.` / ` * This feature is disabled if sync is disabled, the` / ` * #GstBaseSinkClass::get_times method does not return a valid start time or` / ` * max-lateness is set to -1 (the default).`
  - `gstbasesink.c:300`: `#define DEFAULT_MAX_LATENESS        -1`
  - `gstbasesink.c:3213-3215`: `    /* !!emergency!!, if we did not receive anything valid for more than a` / `     * second, render it anyway so the user sees something */`
  - `gstvideosink.c:174-178`: `  /* 20ms is more than enough, 80-130ms is noticeable */` / `  gst_base_sink_set_processing_deadline (GST_BASE_SINK (videosink),` / `      15 * GST_MSECOND);` / `  gst_base_sink_set_max_lateness (GST_BASE_SINK (videosink), 5 * GST_MSECOND);` / `  gst_base_sink_set_qos_enabled (GST_BASE_SINK (videosink), TRUE);`
  - `gstaudiobasesink.c:98,102`: `#define DEFAULT_ALIGNMENT_THRESHOLD   (40 * GST_MSECOND)` / `#define DEFAULT_DRIFT_TOLERANCE   ((40 * GST_MSECOND) / GST_USECOND)`
- Coverage: T7 covers — base sink: late buffers dropped only if max-lateness ≠ −1 (base default −1 = never drop); video sinks set max-lateness 5 ms, processing deadline 15 ms, QoS on → frames later than 5 ms past their end are dropped (skip), with a 1 s "render anyway" floor. The comment "80-130ms is noticeable" is uncited. Not an observation.

### S2-18 — schbench, git.kernel.org `mason/schbench.git`

- Copies: `git clone https://git.kernel.org/pub/scm/linux/kernel/git/mason/schbench.git`, HEAD `6300b8f3a8922c61ea6bb2cdfa1901a42c0cc6fc` (2025-06-09); only tag `v1.0` → `ab22f3f8766e1bf8a3e8f481c205c8f153dd200d` (2023-04-17, "schbench: consistently use stderr for metric output"); 82 commits; accessed 2026-09-24. Files via `git show <rev>:<path>`: `README.md@v1.0` `b05bdfe9ca6f6e620dd31f476ff5fab9b4c2816b5d586b2febf845f6365bf5e4`; `schbench.c@v1.0` `2588404b0922e9a67133fef5440cbfcdcabe5b0954fd8943f635ec600a13da82`; `README.md@6300b8f` `8e8116358246212c5f1ce01ec5d1d14fbef711f9201620c7d04dcf05f6fcfb83`; `schbench.c@6300b8f` `36edab0e9b8eea4c2dc8473a24fddda2efdf3e6b8db41805a3fc06479fa5e31f`; `schbench.c@36d859a` (first commit, 2016-04-04) `9f0138f7e5f681644b0b77d24ef543b729cbea3c0b99de03a6cacfb7ac01ca82`; `schbench.c@00a2523` (2023-04-11) `f27823e96ce642a9a52e73184a1a0e0f5ec9ccb24081dfa230ef62966f20f169`.
- History of the percentile list (`git log -G'plist\[PLAT_LIST_MAX\] = '`): `36d859a 2016-04-04 schbench: measure scheduler wakeup latencies`; `00a2523 2023-04-11 schbench: record percentiles for RPS numbers`; `6809f4a 2023-04-11 schbench: print different percentiles for latency vs RPS`.
- Verbatim passages:
  - `schbench.c:59@36d859a`: `static double plist[PLAT_LIST_MAX] = { 50.0, 75.0, 90.0, 95.0, 99.0, 99.5, 99.9 };`
  - `schbench.c:88@00a2523`: `static double plist[PLAT_LIST_MAX] = { 50.0, 90.0, 99.0, 99.9 };`
  - `schbench.c:101-104@v1.0` (same text `schbench.c:121-124@6300b8f`): `#define PLIST_FOR_LAT (PLIST_50 | PLIST_90 | PLIST_99 | PLIST_999)` / `#define PLIST_FOR_RPS (PLIST_20 | PLIST_50 | PLIST_90)` / `` / `static double plist[PLAT_LIST_MAX] = { 20.0, 50.0, 90.0, 99.0, 99.9 };`
  - `schbench.c:1275-1285@v1.0`: `show_latencies(&wakeup_stats, "Wakeup Latencies",` / `"usec", runtime_delta / USEC_PER_SEC,` / `PLIST_FOR_LAT, PLIST_99);` / `show_latencies(&request_stats, "Request Latencies",` / … `show_latencies(&rps_stats, "RPS",` / `"requests", runtime_delta / USEC_PER_SEC,` / `PLIST_FOR_RPS, PLIST_50);`
  - `schbench.c:1748-1751@6300b8f`: `fprintf(stderr,` / `"sched delay: message %llu (usec) worker %llu (usec)\n",` / `message_thread_delay / 1000,` / `worker_thread_delay / 1000);`
  - `schbench.c:1-7@6300b8f`: `/*` / ` * schbench.c` / ` *` / ` * Copyright (C) 2016 Facebook` / ` * Chris Mason <clm@fb.com>` / ` *` / ` * GPLv2, portions copied from the kernel and from Jens Axboe's fio`
  - `README.md:12-19@v1.0`: `schbench uses messaging threads and worker threads.  Workers perform an artificial ` / `request comprised of two usleeps (simulating network/disk/locking) and some matrix math.  Messaging threads just queue up the work and wait for results.` / `` / `Results are recorded for three primary metrics:` / `` / `- Wakeup latency: messaging threads record the time a worker is posted, and workers compare this with the time when they start running.` / `- Request latency: time required to complete our fake request.` / `- Requests per second: total number of requests all the threads are able to complete.`
  - `README.md:48-56@v1.0` (example run): ` ./schbench -F 256 -n 5 --calibrate -r 10` / `setting worker threads to 52` / `...` / `Wakeup Latencies percentiles (usec) runtime 10 (s) (30212 total samples)` / `          50.0th: 7          (7806 samples)` / `          90.0th: 18         (8649 samples)` / `        * 99.0th: 175        (2590 samples)` / `          99.9th: 909        (271 samples)` / `          min=1, max=10224`
- Coverage: T8 covers — reports wakeup latency (µs), request latency (µs) and RPS percentiles; first version (2016) printed p50/75/90/95/99/99.5/99.9; since 2023-04-11 (so at v1.0 and HEAD) latency lines print p50/p90/p99/p99.9 (p99 starred) and RPS lines p20/p50/p90 (p50 starred); HEAD additionally prints scheduler delay of message and worker threads. Copyright 2016 Facebook, GPLv2 (source header; README has no copyright line). README example runs are single observations with machine unnamed (only "setting worker threads to 52").

### S2-19 — schbench, GitHub `masoncl/schbench`

- Copy: `git clone https://github.com/masoncl/schbench` at `24e32b8ef67cbafb0761aed68747d90a291767ae` (2025-12-23, "Merge pull request #10 from kkdwvd/split-ws"); `git ls-remote --tags` returned no tags; kernel.org HEAD 6300b8f is an ancestor (`git merge-base --is-ancestor` true); accessed 2026-09-24. `S2-19/schbench.c` `18720ce0a70b115f70fcae309ef9a70c98b005f6a7b0cdcf7a4fbf298b14795b`; `S2-19/README.md` `520c9f3a6e0ff737bdf365969b1d5e48d738864e1b8b54ad3489e7807b00460b`.
- Verbatim passages: `schbench.c:129-132`: `#define PLIST_FOR_LAT (PLIST_50 | PLIST_90 | PLIST_99 | PLIST_999)` / `#define PLIST_FOR_RPS (PLIST_20 | PLIST_50 | PLIST_90)` / `` / `static double plist[PLAT_LIST_MAX] = { 20.0, 50.0, 90.0, 99.0, 99.9 };`; `schbench.c:4`: ` * Copyright (C) 2016 Facebook`; `README.md:16-17`: `artificial request comprised of two usleeps (simulating network/disk/locking)` / `and some matrix math.  Messaging threads just queue up the work and wait for`.
- Coverage: T8 covers — GitHub repo continues the kernel.org history (12 further commits, e.g. riscv64/s390 support, private working-set option); same percentile sets; no tags. Not an observation.

### S2-20 — hackbench (rt-tests)

- Copy: `git clone --depth 1 https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git`, HEAD `62da2befac98f811af8e56f2b7992fb09faa33d6` = tag `v2.11` (tag object `711978b9…`), accessed 2026-09-24. `S2-20/hackbench.c` `36e5b4c86aee10fa7422e16c2a3cb218e7b040a364fe52f943ad8d68b167ac3e`; `S2-20/hackbench.8` `84fe7408e1d820ee88a4114fbeb60cef600ebc70f07d27814030d728e091f3fc`.
- Verbatim passages:
  - `hackbench.c:37-40`: `static unsigned int datasize = 100;` / `static unsigned int loops = 100;` / `static unsigned int num_groups = 10;` / `static unsigned int num_fds = 20;`; `:49`: `static unsigned int process_mode = PROCESS_MODE;`
  - `hackbench.c:504-507`: `printf("Running in %s mode with %d groups using %d file descriptors each (== %d tasks)\n",` / … `printf("Each sender will pass %d messages of %d bytes\n", loops, datasize);`; `:570`: `printf("Time: %lu.%03lu\n", diff.tv_sec, diff.tv_usec/1000);`
  - `hackbench.8:18-22`: `Hackbench is both a benchmark and a stress test for the Linux kernel` / `scheduler. It's main job is to create a specified number of pairs of` / `schedulable entities (either threads or traditional processes) which` / `communicate via either sockets or pipes and time how long it takes for` / `each pair to send data back and forth.`
  - `hackbench.8:66-72`: `user@host: ~ $ hackbench` / `Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)` / `Each sender will pass 100 messages of 100 bytes` / `Time: 0.890`
- Coverage: T8 covers — reports one number, total wall time (s, ms resolution); no latency percentiles; defaults 10 groups × 20 fds (40 per group, 400 tasks), 100 messages of 100 bytes, process mode, sockets. Man-page example is a single illustrative run, machine unnamed.

### S2-21 — stress-ng (`README.md`, `stress-ng.1`, `stress-workload.c`, `stress-cyclic.c`)

- Copy: sparse clone of github.com/ColinIanKing/stress-ng at `3ac9d7a8aed7048d73d3a308b829b07f30166198` (2026-09-23; newest tag V0.22.01), accessed 2026-09-24. `S2-21/README.md` `b7e6ff904fc8a2ee177f10443a587ac0000543c9ca699b05c3ea33cf5c29659f`; `S2-21/stress-ng.1` `0d8bc6227e1d93b54f6940a9a354b66c7fa456d6abf004e827c18f05e45bd243`; `S2-21/stress-workload.c` `cbbd8268ce52390290508881c6ac4e5e6423f3105e4f36aa93c24850aff8446f`; `S2-21/stress-cyclic.c` `64f0c536dc699ec51491330fd8a64adbb03f2eb6550865ebdead372ffc3bd006`.
- Verbatim passages:
  - `README.md:32-35`: `stress-ng can also measure test throughput rates; this can be useful to observe` / `performance changes across different operating system releases or types of` / `hardware. However, it has never been intended to be used as a precise benchmark` / `test suite, so do NOT use it in this manner.`
  - `stress-ng.1:11793-11809`: `.B \-\-workload N` / `start N workers that exercise the scheduler with items of work that` / `are started at random times with random sleep delays between work items. By` / `default a 100000 microsecond slice of time has 100 work items` / `that start at random times during the slice. The work items by default run` / `for a quanta of 1000 microseconds scaled by the percentage work load (default of 30%).` … `If a work item is already running when a new work item is scheduled to run then` / `the new work item is delayed and starts directly after the completion of the` / `currently running work item when running with the default of zero worker threads.` / `This emulates bursty scheduled compute, such as handling input packets where` / `one may have lots of work items bunched together or with random unpredictable` / `delays between work items.`
  - `stress-ng.1:11892-11894`: `.B \-\-workload\-threads N` / `use N process threads to take scheduler work items of a workqueue and run the` / `work item (default is 2).`
  - `stress-workload.c:536-539`: `uint32_t workload_load = 30;` / `uint32_t workload_slice_us = 100000;	/* 1/10th second */` / `uint32_t workload_quanta_us = 1000;	/* 1/1000th second */` / `uint32_t workload_threads = 2;		/* 0 = disabled */`
  - `stress-ng.1:2744-2752`: `.B \-\-cyclic N` / `start N workers that exercise schedulers` / `with cyclic nanosecond sleeps. Normally one would just use 1 worker instance` / `with this stressor to get reliable statistics. By default this stressor measures the` / `first 10 thousand latencies and calculates the mean, mode, minimum, maximum` / `latencies along with various latency percentiles for the just the first` / `cyclic stressor instance.`
  - `stress-cyclic.c:928-938`: `static const double percentiles[] = {` / `25.0,` / `50.0,` / `75.0,` / `90.0,` / `95.40,` / `99.0,` / `99.5,` / `99.9,` / `99.99,`
- Coverage: T8 covers — yes, `--workload` emulates timed work items (100 ms slice, 1 ms quanta, 30 % load, random/clustered start times, scheduling policy selectable incl. idle/ext); man page is internally inconsistent on the default thread count ("default of zero worker threads" vs "default is 2"; source says 2). `--cyclic` reports mean/mode/min/max and p25…p99.99 wake latencies. README disclaims use as a precise benchmark. Not an observation.

### S2-22 — GNOME LocalSearch (formerly tracker-miners), `src/indexer/tracker-main.c` and user unit

- Copy: `git clone --depth 1 https://gitlab.gnome.org/GNOME/localsearch.git` at `959f89d9914c71471cb4a8a0ddabcb9ae3b0ec8a` (2026-09-23; newest release tag 3.12.0 → `c1f1c74476b381608c9de15a0f29680a9ff5ce3b`, not checked out; repository history contains `tracker_0_5_*` tags, i.e. the renamed tracker/tracker-miners tree), accessed 2026-09-24. `S2-22/tracker-main.c` `bf0bf720467204e003ad50ccfdd5530211664574714755a3d37e342041d0bf5a`; `S2-22/tracker-miner-fs.service.in` `aef73d13f1229fd9a494385078e7595dfe55b542579da0b859ccac53da4d7eb4`.
- Verbatim passages:
  - `tracker-main.c:82-109`:
    ```
    	/* Set CPU priority */
    	TRACKER_NOTE (CONFIG, g_message ("Setting scheduler policy to SCHED_IDLE"));
    	if (pthread_getschedparam (pthread_self (), &policy, &sp) >= 0) {
    ...
    		if (pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp) < 0)
    			g_message ("Couldn't set idle scheduler policy: %m");
    	}

    	/* Set disk IO priority and scheduling */
    	ioprio = 7; /* priority is ignored with idle class */
    	ioclass = IOPRIO_CLASS_IDLE << IOPRIO_CLASS_SHIFT;
    	if (syscall (SYS_ioprio_set, IOPRIO_WHO_PROCESS, 0, ioprio | ioclass) < 0)
    		g_message ("Couldn't set ioprio idle priority: %m");
    #endif

    	TRACKER_NOTE (CONFIG, g_message ("Setting priority nice level to 19"));
    	if (nice (19) < 0)
    		g_message ("Couldn't set nice value to 19: %m");
    ```
  - `tracker-main.c:140-141`: `	/* This makes sure we don't steal all the system's resources */` / `	initialize_priority_and_scheduling ();`
  - `tracker-miner-fs.service.in:12`: `Slice=background.slice`
- Coverage: T9 covers — the file indexer (`localsearch-3`, formerly tracker-miner-fs-3) sets SCHED_IDLE on its main thread, idle I/O class, and nice 19 at startup, unconditionally on Linux; the user unit adds only `Slice=background.slice`. Not an observation.

### S2-23 — plocate `plocate-updatedb.service.in` (upstream file, via Debian source package 1.1.25-1)

- Copy: `https://sources.debian.org/data/main/p/plocate/1.1.25-1/plocate-updatedb.service.in` (Debian sid/forky source package 1.1.25-1; upstream git.sesse.net unreachable, see log #22), accessed 2026-09-24, `S2-23/plocate-updatedb.service.in`, SHA-256 `d8867da6abc3e7062679c51c8b7e46d8f9484c337b127a0efe97410e0bede5a7`.
- Verbatim passage `plocate-updatedb.service.in:1-9`: `[Unit]` / `Description=Update the plocate database` / `` / `[Service]` / `Type=oneshot` / `ExecStart=@sbindir@/@updatedb_progname@` / `LimitNOFILE=131072` / `IOSchedulingClass=idle` / `Nice=19`
- Coverage: T9 covers — ships nice 19 + idle I/O class; no `CPUSchedulingPolicy` (so SCHED_OTHER at nice 19, not SCHED_IDLE). Version 1.1.25 as packaged; upstream commit not identified. Not an observation.

### S2-24 — KDE Baloo (`src/file/priority.cpp`, `main.cpp`, `extractor/main.cpp`, `kde-baloo.service.in`)

- Copy: `git clone --depth 1 https://github.com/KDE/baloo` (KDE's GitHub mirror; invent.kde.org gave 502) at `cfa50f5b61f2e4ab4d112ae4c93a8cdb0de7f688` (2026-09-23; `KF_VERSION "6.31.0"` in CMakeLists.txt), accessed 2026-09-24. `S2-24/priority.cpp` `b6df2a1172131df3fec91fbf5fb254909dd6abe282b339b35f8b90739109d7d5`; `S2-24/main.cpp` `8eef78475cd3dad766137ef9efd2e73624b7f3de216463e459e9fed0dd788bab`; `S2-24/extractor-main.cpp` `69cf06518045f5c5b2d13c06f1678684faeb89542776c37c9955cdfa93e2acf9`; `S2-24/kde-baloo.service.in` `68da2312f10da6986108515e28001bc9d4f753cee0441f9dd71036f098ca44d3`.
- Verbatim passages:
  - `priority.cpp:42-45`: `bool lowerPriority()` / `{` / `    return !setpriority(PRIO_PROCESS, 0, 19);` / `}`; `:53`: `    return !sched_setscheduler(0, SCHED_BATCH, &param);` (in `lowerSchedulingPriority`); `:65`: `    return !sched_setscheduler(0, SCHED_IDLE, &param);` (in `setIdleSchedulingPriority`); `:27`: `    if (syscall(SYS_ioprio_set, IOPRIO_WHO_PROCESS, 0, ioprio_value(IOPRIO_CLASS_IDLE, 0, IOPRIO_HINT_NONE)) >= 0) {`
  - `main.cpp:28-30` (baloo_file daemon): `    lowerIOPriority();` / `    lowerSchedulingPriority();` / `    lowerPriority();`
  - `extractor-main.cpp:21-23`: `    lowerIOPriority();` / `    setIdleSchedulingPriority();` / `    lowerPriority();`
  - `kde-baloo.service.in:8-12`: `Slice=background.slice` / `ExecCondition=…` / `# We'll basically only want to consume resources if they aren't needed anywhere else, hence weights are way low.` / `CPUWeight=1` / `IOWeight=1`
- Coverage: T9 covers — baloo_file daemon: SCHED_BATCH + nice 19 + idle I/O; content extractor process: SCHED_IDLE + nice 19 + idle I/O; systemd user unit: CPUWeight=1, IOWeight=1, background.slice. Not an observation.

### S2-25 — ClamAV service units (`freshclam/clamav-freshclam.service.in`, `clamd/clamav-daemon.service.in`)

- Copy: `git clone --depth 1 https://github.com/Cisco-Talos/clamav` at `72cd48c9faed4fa4afc22bc4ed0b9b19f8d3f8f7` (2026-08-27; `project( ClamAV VERSION "1.6.0"`, devel suffix), accessed 2026-09-24. `S2-25/clamav-freshclam.service.in` `eaefe47e09e594d77c12c5c3d0f936f989d4db5976bf4cbaebfb48f43f3efdb1`; `S2-25/clamav-daemon.service.in` `e0bd83bb1bb454bdb7a374c276a4a840476a2525b9926bd771d8fa1741d241ff`.
- Verbatim passages: `clamav-freshclam.service.in:9-10`: `[Service]` / `ExecStart=@prefix@/bin/freshclam -d --foreground=true`; `clamav-daemon.service.in:9-13`: `[Service]` / `ExecStart=@prefix@/sbin/clamd --foreground=true` / `# Reload the database` / `ExecReload=/bin/kill -USR2 $MAINPID` / `TimeoutStartSec=420`.
- Coverage: T9 — negative evidence: upstream units set no `Nice=`, `CPUSchedulingPolicy=`, `IOSchedulingClass=` or weights; grep of `*.c *.h *.rs` for `setpriority|SCHED_IDLE|SCHED_BATCH|ioprio|nice(` returned nothing. Not an observation.

### S2-26 — borgmatic sample unit (and borg, restic: none)

- Copy: `git clone --depth 1 https://github.com/borgmatic-collective/borgmatic` at `77cc966693676b8c26530962f77890ab2005e0bf` (2026-09-23), accessed 2026-09-24, `S2-26/borgmatic.service` (`sample/systemd/borgmatic.service`) SHA-256 `fed26d7e54948b947aafe0c152113347330f18243a833d6ac636cfd94f998858`.
- Verbatim passage `borgmatic.service:65-70`: `# Lower CPU and I/O priority.` / `Nice=19` / `CPUSchedulingPolicy=batch` / `IOSchedulingClass=best-effort` / `IOSchedulingPriority=7` / `IOWeight=100`
- Coverage: T9 covers — borgmatic's sample unit (a sample the user installs, under `sample/`) uses SCHED_BATCH + nice 19 + best-effort I/O 7. borg (`507ff0dd…`) and restic (`6adedec6…`) HEAD: no scheduling-class code or unit (grep, log #29). Not an observation.

### S2-27 — Déjà Dup (`libdeja/CommonUtils.vala`)

- Copy: `git clone --depth 1 https://gitlab.gnome.org/World/deja-dup.git` at `e1d87252ebdb7e77b48dc8ad9e25afed5deda7fa` (2026-09-23; meson `version: '50.3'`), accessed 2026-09-24, `S2-27/CommonUtils.vala` SHA-256 `4963c2501f20e74c6b76c8b1d15ff9a0ac6af7e181c5896135ba5d79f273a010`.
- Verbatim passage `CommonUtils.vala:129-148`:
  ```
    // Check for ionice to be a good disk citizen
    if (Environment.find_program_in_path("ionice") != null) {
      // In Linux 2.6.25 and up, even normal users can request idle class
      if (utsname.sysname == "Linux" && meets_version(major, minor, micro, 2, 6, 25))
        cmd = {"ionice", "-t", "-c3"}; // idle class
      else
        cmd = {"ionice", "-t", "-c2", "-n7"}; // lowest priority in best-effort class
    }

    // chrt's idle class is more-idle than nice, so prefer it
    if (utsname.sysname == "Linux" &&
        meets_version(major, minor, micro, 2, 6, 23) &&
        Environment.find_program_in_path("chrt") != null) {
      cmd += "chrt";
      cmd += "--idle";
      cmd += "0";
    }
    else if (Environment.find_program_in_path("nice") != null) {
      cmd += "nice";
      cmd += "-n19";
    }
  ```
  (Used by `DuplicityInstance.vala:99` and `ToolInstance.vala:135`: `real_argv = DejaDup.nice_prefix(real_argv);`.)
- Coverage: T9 covers — backup tool runs its backend under `chrt --idle 0` (SCHED_IDLE) when available, else nice 19, plus idle I/O. Not an observation.

### S2-28 — A. Arpaci-Dusseau, "Multilevel Feedback Queue Schedulers" (CS 537 handout, Spring 2000), Solaris 2.6 TS scheduler

- Citation: A. Arpaci-Dusseau, *Multilevel Feedback Queue Schedulers* (handout), CS 537, Computer Sciences Department, University of Wisconsin-Madison, Spring 2000. 6 pp.
- Copy: `https://pages.cs.wisc.edu/~remzi/solaris-notes.pdf`, HTTP 200, accessed 2026-09-24, `sources/S2-28/solaris-notes.pdf`, SHA-256 `a36730ff584a7f5b56567aeb57b8f74753028879867b3310730c0e1b39ed22d3`. PDF metadata: Author "Remzi Arpaci-Dusseau", Producer "Mac OS X 10.6.4 Quartz PDFContext", CreationDate 2011-01-30 (scan/re-save date; text header says Spring 2000). Text extracted with pypdf.
- Verbatim passages:
  - p. 1: "In this handout, we give a brief overview of the behavior of the Solaris 2.6 Time-Sharing (TS) scheduler, an example of a Multilevel Feedback Queue scheduler."
  - p. 3, "Dispatch Table": "The durations of the time-slices, the changes in priorities, and the starvation interval are specified in a user-tunable dispatch table. The system administrator (or anyone with root privileges again) can change the values in this table, thus configuring how the time-sharing scheduler manages its jobs. While this has the noble intention of allowing different systems to tune the scheduler to better handle their workloads, in reality no one really knows how to configure these tables well. Therefore, we will focus on the default dispatch table."
  - p. 3: "ts_quantum: Length of the time-slice (in the actual table, this value is specified in 10ms clock ticks; in the output from running dispadmin, the value is specified in units of 1ms)."
  - p. 3: "A job begins at priority 29."; "In this table, the priority of jobs ranges from a high of 59 down to 0. Time-slices begin at 20ms at the highest priority and gradually increase in duration up to 200ms at the lowest priorities. Generally, the priority of a process decreases by 10 levels after it consumes its time-slice; the priority of" (p. 5) "a process is increased to 50 or above when the starvation timer expires."
  - p. 4, Table 2 "Default Solaris Time-Sharing Dispatch Table" (header and bounding rows): `# ts_quantum  ts_tqexp  ts_slpret  ts_maxwait ts_lwait  #PRIORITY LEVEL` / `200         0        50           0        50        #     0` / … / `40        48        58           0        59        #    58` / `20        49        59       32000     59        #    59`
  - p. 5: "ts_update(): called once a second to check the starvation qualities of each job."
  - p. 6, "Fairness": "However, due to the configuration of the default dispatch table (i.e., the starvation interval is set to zero), you will note that the priority of every process is raised once a second, regardless of whether or not it is actually starving. Thus, the allocation history of each process is erased every second and compute-bound processes tend to acquire more than their fair share of the resources."
- Coverage: T2 (lecture notes) covers — same authors' group (Andrea Arpaci-Dusseau), Solaris 2.6 TS: 60 levels, quanta 200 ms (level 0) … 20 ms (level 59) at 10 ms ticks, start priority 29, −10 levels on quantum expiry, boost to ≥50 once per second (maxwait 0), remark "no one really knows how to configure these tables well" (the literal phrase "nobody knows" was not found). T3/T6 corroborates S2-08 (same tick values 20…2 as illumos `ts_dptbl.c`, read there at hz 100). Documentation, not an observation (the `ps` listing on p. 2 is one machine "elaine1", date not given).

## 3. Not found

- **T2 lecture notes, literal "nobody knows" remark**: not found; searches #11–#12 led only to S2-28, which says "no one really knows how to configure these tables well". No other Arpaci-Dusseau Solaris-dispatch-table notes were located.
- **T3, commit that changed EEVDF base slice 750000→700000**: not identified; bracketed only by tag checks (#4: v6.14 = 750000, v6.15 = 700000). `api.github.com` (needed for a commit search without a full clone) returned 403 (#1 fetch notes); a full-history kernel clone was not attempted.
- **T3, scx release tags**: scx files read at HEAD `00fec1e…`, not at a release tag (v1.1.3 exists); per-tag values not checked.
- **T6, a documented fair-server latency bound in words**: `grep -rl 'fair_server\|dl_server' Documentation` at v7.2 (#6) found only the `sched-rt-group.rst` bullet; no document states the fair server's default runtime/period in prose — only the source constants (S2-05).
- **T7, VLC**: not searched (mpv and GStreamer covered the "at least one player" requirement).
- **T8, a source cited for interbench's ~7 ms jitter-perception figure**: none in `interbench.8`, `readme`, `readme.interactivity`, `interbench.c` (S2-15, grep for `7ms|7 ms|perception|jitter`).
- **T9, plocate upstream commit**: git.sesse.net 502 and salsa.debian.org credential prompt/302 (#22–#23); the file was read from the Debian source package instead (S2-23).
- **T9, measured wake-up latency of a periodic task beside a SCHED_IDLE or nice-19 hog**: no project doc or source states a value (S2-01, S2-06, S2-07 give weights and preemption rules only).
- **T9, borg and restic declared class**: none in source at HEAD (#29); clamav none (#28).
