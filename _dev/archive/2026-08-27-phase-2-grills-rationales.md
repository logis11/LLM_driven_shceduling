# 2026-08-27/28 — Phase 2 grills: the rationales recovered

Decision record for the 2026-08-27 sessions (phase-2 grill; task-2.3 format grill) and the pre-2.5 2026-08-28 sessions (2.6 grill; 2.4 grill; batch-tag supersession; grid sign-off), whose rationale the 2026-08-28 archive recorded as not recoverable. Written 2026-10-16 from what 인지오 holds; the sessions' transcripts no longer exist. The decisions themselves are in `_dev/docs/spec/jioh/phase-2-workload-dataset-generation.md`, `task-2.3-timeline-compiler.md`, `task-2.4-core-timelines.md` and `task-2.6-meas-ci.md`.

## Rationales recovered

- **Task 2.4 decision 4 — the seed policy: refused, not warned.** The spec says variants inherit the base seed and "the deriver warns on an explicit override"; the deriver refuses ("variants may not change the seed", "patch-meta may not set the seed or id"). Rationale (인지오): the seed's inheritance is a rule — the one the paired byte-discipline of the derived files rests on — and a rule is enforced by refusal, not by a warning. The spec's "warns" is the misstatement. Verified: the deriver has refused since its first commit, `63c677dc` (2026-08-28).
- **Task 2.4 decision 3 — the lengths: design.** The default segment of 120 s and the C1 files' 60 s are dataset design: no source states how long a calibration file or a segment should run, so the values are not drawn from literature but chosen, and labelled design. Verified: twelve C1 files run 60 s (browsing, dev, gaming, idle, indexing, mail, media, meeting, office, photo, render, video-edit); the four batch C1 files run as long as their measured job, bound whole since 9.10 D17 (compile 1,594 s, ml-train 1,612 s, transcode 4,762 s, backup 277 s).
- **Task 2.3 decision 6 — the lockfile pattern.** The build is a derived output, reproduced byte for byte from its inputs (the timelines, the library, the streams, the compiler), so it is not kept in the repository; as a lockfile pins dependencies by hash in place of the installed tree, the committed manifest pins by hash what the build must produce, and CI rebuilds and compares. Its release clause ("Release artifacts publish from tagged CI builds") is superseded by 9.15's W-0733 (2026-10-16): the build is not published before submission; at submission a snapshot goes to a DOI-minting data repository.

## Rationale stated in the decision or another record

- **Task 2.3 decision 1 — three tracks:** the split mirrors the canonical file's `ground_truth`/`events` separation (the decision's text).
- **Task 2.3 decision 2 — the task entry:** `bind` is restricted to the keys an entry declares by the binding rule, numeric behaviour parameters living only in the library (`docs/workload/building-plan.md` §1).
- **Task 2.3 decision 5 — the seed and keyed substreams:** unrelated edits cannot shift another task's draws, and the C2 pairs' byte-identity holds by construction (the decision's text).
- **Task 2.4 decision 1 — declarative variants and one deriver:** a derived file provably differs from its base by exactly its ops (the decision's text).
- **Task 2.6 decision 2 — the data's home:** the artifacts expire, which makes archiving the raw data part of the fold-in (the decision's text); the raw records later moved to one GitHub release per campaign, made by hand (9.15's W-0732, 2026-10-16).

## Superseded — the later record carries its own reasons

- **Phase 2 decision 5 and task 2.3 decision 7 — the demand window** as a build gate: retired by 9.14 decision 4; its reason recorded by 9.15's W-0737 (2026-10-16): since 9.10 D17 binds every job whole as measured, a file's demand follows from the measurement, and holding it to the window would have meant bending measured lengths, so the demand is reported per file and per segment.
- **Task 2.3 decision 3 — the focus track:** 9.17 renamed the keystroke-window track `input` and added a `focus` track of pinned focus intervals, required on every timeline (`_dev/research/jioh/task-9.17-focus-in-the-telemetry/changelog.md`).
- **Task 2.4 decision 2 — the coverage grid's human sign-off:** superseded by Phase 7 decision 11 (the grid counts the driver-table cell against the tiers; an empty cell fails CI), as the spec's own note states.
- **Task 2.4 decision 3 — the demand classes:** amended by Phase 7 decision 7, as the spec's own note states; the window behind them retired as above.
- **Task 2.4 decision 5 — the name strings:** superseded by 9.10 D25 (a task's name is its kernel `comm`, as a campaign observed it).
- **Task 2.6 decisions 1, 3, 3a, 4, 5 and 6 — the sidecars, the N = 5 batches, the batch supersession, the kernel corpus, the Xvfb workflow and the name verification:** replaced by Phase 9's measurement campaigns — `perf sched record` over whole phases, repeats added until the stability rule holds, the campaign tag by the launch date of its first batch (`_dev/research/jioh/measurement-campaign-workflow.md`) — and, for the names, by 9.10 D25.

## Process decisions

Phase 2 decisions 1 (the phase boundary), 2 (the sub-task set), 3 (the format's ownership split), 4 (CI wiring in 2.3) and 6 (the hand-off sub-task's scope) organised the phase; their outcome is the phase's record.
