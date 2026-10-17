# 9.16 — 인지오's answers

## D1 — `c7-meeting` stays judging (2026-10-17)

Finding: handed F1 — the boot-default sweep read the `cycle_run` quantile tables (p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9) as deciles; the call consumes the 10 ms boot slice in about 1 in 20 cycles (4.9 % from the table, 5.5 % in the compiled `c1-meeting` and `c7-meeting`), not "about a fifth", the reason 9.14 spec decision 2 gave for its return to the judging set.

Answer: (a). `c7-meeting` stays judging; the reasons are restated to the true figures with their right labels — about 1 in 20 cycles, and in about 4 of 10 boost intervals (arithmetic: 1 − 0.95¹⁰, cycles taken as independent, 10 cycles per 100 ms boost) the call is demoted and waits behind the upgrade until the next boost. The scoring spec is re-pinned in the RQ0 gate spec; no dataset value moves.

## D2 — the "foreground window 우대" row cut to Windows (2026-10-17)

Finding: outside-claims C-14 — research guidebook vol-01's comparison row (`docs/guidebook/vol-01-systems-and-scheduling.md:3339`) marks foreground-window favour "Linux 부분적 / Windows 있음 / macOS 있음"; only the Windows cell has a record (the 9.12 related-work search, `A-audit.md:328`: "the scheduler boosts the priority class of the process associated with the foreground window").

Answer: (a). The row keeps the Windows cell with its record; the Linux and macOS cells are not stated. No source is added.

## Taken without a question (decision 1 of the 9.16 spec applied)

- The six measurement-method sources, `glean`, the three Ubuntu packaging sources, `gh-artifact-retention`, RFC 8290, the kernel's `sched_waking` placement and the kernel Makefile's `-pipe`, whose only passages sit in `docs/references.md`, written by the deciding sessions: the phase spec's decision 1 asks for an independent read, so they joined the blind re-read (`claims/extra-blind-topics.md`); its read records become their records.
- `parallelism_cap` 8's label (dataset claims D-F3-08): the recorded decision, 9.6 D4, says convention; the label follows it.

## D3 — the `tick_count` guard follows the window rule (2026-10-17)

Finding: compiled G1 — the guard's chain check (`harness/tools/harness/primitives.py:301–309`) counts consumed head ticks at or before `T_end` against tail completions at or before `T_end`; on `c7-gaming` the last consumed tick lies 1,139 µs before `T_end` and a frame needs 14,999 µs, so every run fails and the RQ0 verdict is `invalid` (`evaluator.py:369–390`). The same on `c3-evening`, `c6-dual`, the six `c7-gaming` variants, and the `c2-p2a`/`c2-p2b` variants @seg1-30s, @seg1-120s, @chain-x1.2, @chain-x1.4.

Answer: (ii). Iterations still running at `T_end` are not an error, as the metrics doc's window rule (§4: "A task alive at `T_end` is *not completed within the window*") has it; the guard fails only when the tail completed more iterations than the head consumed ticks. Its stated weakness: a wake the simulator drops mid-run is no longer caught by this guard. Code and docs only — `primitives.py`, the guard spec's `tick_count` grounding, metrics doc §6.2 — and the guard spec re-pinned in the RQ0 gate spec; no dataset byte changes.

## D4 — `c2-p3b`'s backup scores its turnaround (2026-10-17)

Finding: compiled F1 — replayed alone, `c2-p3b`'s editor uses 99.8 s of 60–326 s, leaving 166.2 s of idle lane against the backup's 165.67 s of CPU and 0.19 s of sleeps; the backup finishes about 0.3 s before `T_end` under every row. The scoring spec's comment (`scoring-spec.yaml:204–205`, "about 162 s of its 165.7 s, and does not finish: progress") came from the manifest's even spread of the editor's CPU.

Answer: (i). The header rule applies (`scoring-spec.yaml:30–32`, 9.14 decision 6: a job that finishes under every row scores its turnaround): the term becomes `bulk` turnaround at weight 0.25, as `c1-backup`'s; the comment restated to about 166 s, finishing about 0.3 s before the end; `:171` says P1's and P2's batch tasks do not finish and P3's two jobs do. The file stays reporting-only, no headroom. Re-pinned with D1's scoring-spec change.
