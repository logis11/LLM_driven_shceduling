# Task 9.16 — read record for outside-claims A-64: scx_lavd's slice boost to 500 ms

The claim (`docs/research-proposal.md:243`, `:844`): "scx_lavd 0.5–5 ms with a boost to 500 ms". The 0.5–5 ms already has a verbatim record (9.11 S2-11, `lavd.bpf.h:73–75` at `00fec1e`); this record holds the boost. Read 2026-10-17 by the 9.16 closing docs chunk F; not a blind read.

**Copy read.** The sched-ext/scx clone at `_dev/research/jioh/task-9.12-related-work-prose/sources/S2-09/audit-2026-10-09/scx/` (a nested git checkout, not committed in this repository): `HEAD` `c8728c6b6a3fde451f0f10b95f99aad7a32a750a`, tag `v1.1.3`, commit date 2026-08-19, remote `https://github.com/sched-ext/scx`; working tree clean. SHA-256 of the files read: `scheds/rust/scx_lavd/src/bpf/lavd.bpf.h` `724b3e160fe952118ede90750987018850173496bc51e7a44ec2c7a716acdb0f`; `scheds/rust/scx_lavd/src/main.rs` `a289632cb800a1e9009ea0f7e07244abdb65dc93b557c1793a734c9c068a45f3`; `scheds/rust/scx_lavd/src/bpf/main.bpf.c` `611f6870ad64821b5c876000f1465529f761b365bb86d34075f7c5d74f8d99ff`.

**Passages.**
- `lavd.bpf.h:74–77`:
  ```
  LAVD_SLICE_MIN_NS_DFL		= (500ULL * NSEC_PER_USEC), /* min time slice */
  LAVD_SLICE_MAX_NS_DFL		= (5ULL * NSEC_PER_MSEC), /* max time slice */
  LAVD_SLICE_BOOST_BONUS		= LAVD_SLICE_MIN_NS_DFL,
  LAVD_SLICE_BOOST_MAX		= (500ULL * NSEC_PER_MSEC),
  ```
- `main.rs:220–222`:
  ```
  /// Disable dynamic slice boost for long-running tasks.
  #[clap(long = "no-slice-boost", action = clap::ArgAction::SetTrue)]
  no_slice_boost: bool,
  ```
- `main.bpf.c:340–352` (the boost's use): "Even in this case, we want to limit the maximum time slice to LAVD_SLICE_BOOST_MAX (not infinite) because we want to revisit if the task is placed on the best CPU at least every LAVD_SLICE_BOOST_MAX interval." … `u64 s = taskc->avg_runtime_wall + LAVD_SLICE_BOOST_BONUS; taskc->slice_wall = clamp(s, slice_min_ns, LAVD_SLICE_BOOST_MAX);`

**Reading.** At `v1.1.3` scx_lavd's default slice runs 0.5–5 ms, and a long-running task's slice can be boosted to its average wall runtime plus 0.5 ms, clamped at `LAVD_SLICE_BOOST_MAX`, 500 ms; `--no-slice-boost` turns the boost off. The claim's wording holds; no doc change.
