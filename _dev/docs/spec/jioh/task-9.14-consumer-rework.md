# Task 9.14 — Consumer rework

The one rework of what consumes the rebuilt workload dataset — the scoring spec, the guard spec, the prior driver table with its pair review, and the RQ0 gate spec — with one harness changelog entry and one re-pin, leaving the project where Phase 8 ended: the gate spec committed and ready for the RQ0 run. Decided in the 2026-10-09 grill. Parent: `_dev/TODO.md`, (jioh, 9.14); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`; decision record `_dev/research/jioh/task-9.14-consumer-rework/changelog.md`.

## Scope

- The scoring spec: terms, windows, weights, the no-headroom statements.
- The guard spec: the pair guard's reading, the pair list's lint, the condition lists, the version.
- The prior driver table's sentences and the pair review.
- The RQ0 gate spec: the judging set and K, the boot-default sweep, the executor assumptions, a simulator-conformance statement, the pre-registered sensitivity and reporting lines, the pins.
- The harness code the contract and the decisions imply: the `job` primitive and the reader, the mock simulator's fixtures and the mock daemon's projection, the evaluator's condition list and reporting-line types, the lints, the tests; `docs/harness/metrics.md` §6.2 and §11 where the hand-offs name them.
- The demand-window rule in the dataset compiler and the manifest's demand record.
- The variant builds the sensitivity lines read, and the tools that produce them.
- The hand-offs addressed to 9.14 in every slice changelog and scope card, including those the TODO line did not carry (the 2026-10-09 sweep), each folded in where its decision belongs.

Out of scope: any archetype value or timeline (the blessed set stands; a second bless follows only from the pre-registered contingency, in Phase 10). Prose under `docs/` other than the pair review, the metrics doc sections named above, and the building plan's demand-window paragraph — 9.15's. The exit audits — 9.16's.

## Locked decisions

### 1. Every consumer is written against the ratified contract, not the current simulator

Primitives, mocks, fixtures, scoring statements, pair review and gate spec read the simulator as the docs state it: the TIMER skip rule (9.11 D3, D17), the zero-wait `ready` line, a cold start into MLFQ, a same-algorithm entry letting the granted slice finish, the batch bandwidth cap, the strict idle class, and the frame chain in EDF's deadline class. The gate spec gains a conformance statement listing these behaviours as what the real simulator must show before the RQ0 run, checked by replaying the hand fixtures through it and comparing traces; 인경민's implementation is a named Phase 10 prerequisite. No reading is stated "as the current simulator's".

Consequences carried with it: the harness reads a consumed tick's index as the latest grid tick at or before its `ready(cause = timer_tick)` line; a skipped tick is a `job` row with no completion, counted as missed, so the miss rate is misses over ticks; the chain guard counts consumed ticks against tail iterations; the `deadline` cross-check pairs lines with rows by tick index and reads `met`, not the slack's sign; the reader's t₀ is the time of a task's first `ready(cause = timer_tick)` line, since the TIMER-first invariant fixes the first instruction and not the first dispatch; the mock-media fixture is re-derived by hand under the skip rule and the zero-wait line.

### 2. The judging set is 20 files; K is 11

The rule stands as Phase 7's 7.7 decided it: a file judges when it is one side of a label-varying pair and its scored term registers the rows' difference by design. Applied to the rebuilt files: the six files holding idle-class work (`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`) leave for reporting-only, because the executor's idle rule places the background task below every row and the cap is work-conserving, so no row reaches it, the same reason 7.7 gave the interactive C1 bases; their prediction and the depicted desktop's limitation (the indexer's slice at about 23 %) are stated. `c7-meeting` re-enters: the measured call's cycle runs consume the boot slice in about a fifth of its cycles, so the tie with the boot default that moved it out in 8.8 no longer holds, and it stands as `c7-gaming` always has — the gap reads EDF against the drawn algorithm, the cap axis inert. `c7-media` stays reporting-only on the redone arithmetic (a 32 ms worst case against a 33.3 ms period, a 1.3 ms margin stated). `c2-p2a`, `c2-p2b` and `c7-gaming` stay, their caveat restated to the deadline-class chain. K is restated to 11 by the existing majority reading; the `prior-table-structure` statement's duplicate-heavy class becomes 10 of 20; the re-entry condition tied to 인경민's executor answers is replaced by this data reason in the harness changelog entry.

### 3. Every outcome-dependent check is pre-registered, none is run in 9.14

No conforming simulator exists before Phase 10, so each check that asks whether something moves a scheduling outcome becomes a reporting line in the gate spec with its sweep values and reading rule fixed now, run with the RQ0 run. The re-measurement of the exception-carried values (pid 1's run mean and the system bus's three values, 9.9 D48; the editor's `utility/libuv-worker` wake rate and gap mean, 9.5 D99; the desktop slice's machine-speed exceptions, 9.8 D28) is a pre-registered contingency: if the half-width line moves any judging file across g, the verdict is reported as a range and that entry is re-measured at a count fixed in the spec from 9.9 D48's projections and 9.5 D88's stopping method, before the result is reported. The stated-precision caveats of 9.5 D88 are carried, not re-measured.

### 4. The demand window retires as a gate

The compiler records demand per file, as now, and per segment, newly, in the manifest, and never fails on it. The pair review reads each judging file's contended segment's demand where it reports the regime per pair. The building plan's §5a paragraph is restated: the `oversubscribed` class marks a file designed to hold contention, its demand a measured fact reported, not a window held. 9.5's spec decision 13, the scale check of "the demand-window rule and the prior-table rows" against the literature-grounded archetypes, keeps its second object; the one archetype still grounded in literature at another machine's scale is the game chain, so that check and 9.4 D9's chain-member RUN sweep are one line (decision 10).

### 5. Windows are numbers tied to segments by lint

The seven windowed terms are renumbered to 60 s and each file's end, and a lint rule requires every window's two bounds to coincide with ground-truth segment boundaries of the compiled file it names, so a window stale in either direction fails.

### 6. The terms on the rebuilt files

Three gaming files lose their `compositor` term and the two meeting files their `video` term, no file holding those tasks. `c2-p2a-idle` enters with `base: c2-p2a`. All 39 interaction-latency terms gain `channel: input`. The weights stand. `c2-p3a`'s render term becomes turnaround at weight 0.5, as its base's: the measured export finishes under every row, so its delivered CPU cannot move; `c2-p3b`'s backup keeps progress at 0.25, since under the idle rule it does not finish. `c3-evening`'s chain term stays scored, its 1.45 lane share design (9.10 D31) and its floor of about 0.31 missed under every policy stated. The no-headroom header is rewritten for the six idle files, `c7-media`, the periodic bases and the C5 ladder, `c2-p2a`'s download (batch class now; the residual under a 0.95 chain below any cap; the boot MLFQ hands it more through boost slices, a negative improvement) and `c3-creation`'s transcode.

### 7. The guard spec: the pair guard reads configuration sequences

`c2_pair` compares the two files' effective configuration over the differing segment, entry by entry: identical sequences fail under `oracle` and the recognition conditions; `fixed` and `random` are not applicable; the `fixed_identical` flag retires. The lint's rule for the pair list becomes: a C2 pair is a recipe variant that changes a segment's label, so the idle variant is not one and the list stays at three. The `whitelist` condition becomes two in every frozen list — `shipped_catalogue` and `strongest_name_table`. Version 1.0 → 1.1, carrying 9.11's three changes (the 30 s starvation floor, the provenance-share grounding, P1's flag), the grounding-kind labels of 9.11 D29, and the changes above.

### 8. The prior table and the pair review

No row's algorithm, cap or params changes. The row sentences are rewritten where they stand: the ten `clamscan` sentences to the unattended upgrade, the seven "2 ms quantum" phrases to the 10 ms boot value, the idle row's count to four daemons, the header's starvation net removed, the gaming rows and findings 1 and 5 to the deadline-class chain and the batch-class download, the indexing and backup rows to the idle rule with the depicted desktop's 23 % stated, the meeting and media rows to EDF rather than the cap, the editor-premise rows to the measured per-keystroke work, and the P-rows to the rebuilt pair. The pair review is rewritten in place, `Updated` bumped, a revision note at the top; it is a contract document, not an appended record. The restated gaming rows are the reply to 인경민's EDF chain-stage note, carried by 9.15's final memo.

### 9. The boot-default sweep has ten points

The 10 ms primary unchanged, with a note that it coincides with the voice task's demotion edge. Alternatives: 500 and 100 000 µs (the schema's bounds), 700 (Linux's base slice at one CPU, design; below the C2 pair's 834 µs chain slack with the Steam client's share stated), 900 (above that slack, below the gaming base's 1 668 µs; demotes the base's cluster of stages), 1 200 (above the 1 ms post-boost point, labelled arithmetic, and the cluster, below the base's longest stage, 1 436 µs), 2 000 (illumos; between the base's and the pair's longest stages), 3 000 (above every chain stage, inside the video job's cycle range), 5 000 (between the video job's median cycle and its upper decile; the compositor reason replaced), 14 000 (new: above the voice job's 12.2 ms ninth-decile cut, below its and the video job's maxima), 20 000 (sched_ext; above every periodic cycle). Each point's reason is on its line, the dead reasons (the compositor burst, the old frame slack) gone.

### 10. The pre-registered lines

As tabled in the grill: the venue factor (every measured RUN ×1/1.25 and ×1.25, a design bracket containing the ×1.144 huge-page ratio and the tracing overhead; the judging files, three conditions, the main N; the chain excluded); the chain scale (the chain's RUNs ×1.2 and ×1.4 on the three gaming judging files; the expected reading that the gaming verdicts depend on the one literature-grounded archetype's scale); the segment length (the C2 pairs' 60 s first segment at 30 s and 120 s on the four C2 judging files); the input-wake count each P99 rests on, printed per judging file; the carried half-widths (every D57-carried value at its interval's bounds, two corners, on the judging files holding those entries; a change triggers decision 3's contingency; 9.6 D29's rule stated with it); the trace replay (one pooled repeat's measured wake sequence replayed on `c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a`; agreement when each file's gap falls on the same side of g under both builds and differs by less than 0.17; disagreement stated as the compiled streams' ordering threat); the longest wait per run against the 30 s floor, any run past 15 s reopening the executor-net question with 인경민; the Layer-1 interval's caveat with no correction; the download bounding check on `c2-p2a` and `c2-p2a-idle`. A moving verdict count makes the verdict a range over that axis.

### 11. The Layer-1 and RQ4 items are hand-offs, not gate-spec content

The 9.12 items on the LLM conditions and the daemon — the recognizer run with and without `reasoning` and its key-order condition, Layer 1's hardware statement, RQ4's latency scope and the costs pool's keying, the two rule lists' build — are recorded as hand-offs: a section of this spec's changelog names each item and its destination, the TODO's Phase 10 line gains a bullet that the RQ1 to RQ4 experiment specs carry them, and the two recognition-log items (the formatted prompt kept, the template's date fixed or recorded) go to 박이안 through 9.15's final memo as a frozen-contract question.

### 12. The sensitivity variants are built in 9.14 and pinned

Taken under 인지오's delegation. The compiler gains the transforms as named modes (scale measured RUNs by a factor; scale the chain's RUNs; set the C2 first segment; set D57-carried values to a bound; replay named repeats, the launch-phase replay of 9.10 D136 extended to the carried phases); 9.14 builds each variant set over the files its line names and pins each variant manifest in the gate spec beside the main one; the runner reads them as further datasets.

### 13. The gate spec's other statements

g stays 0.5 with its band; N stays 100 with its cost clause; `executor-assumptions` restated on 인경민's current answers (a waking deadline task preempts at once; same-microsecond order is config first then insertion order; no executor window, the guard reading the watchdog's bound); the conformance statement of decision 1 added; the `judging-set` statement and the four file notes rewritten per decision 2; the failure procedure's form kept with its classes recounted; the re-pin takes the 2026-10-09 manifest as the compiler regenerates it with per-segment demand, the artifacts unchanged, beside the variant manifests.

### 14. Records and process

Taken under 인지오's delegation, by 9.13's conventions. A research folder `_dev/research/jioh/task-9.14-consumer-rework/` holds a changelog in the slices' form, each entry naming what it hands to 9.15 or 9.16. The TODO's 9.14 line is replaced by per-deliverable sub-bullets. All of 9.14 is committed on `jioh/dataset-rebuild`, no sub-worktree. The harness changelog entry and the re-pin are the closing step; the dataset and harness CI jobs are green at the end.

## Invariants

- Nothing is removed from or added to the judging set after any gap is seen; every change here is made before the first run and leaves a git trace.
- The scoring spec, guard spec, prior table and every manifest the gate spec reads are pinned by hash in the gate spec at the end of 9.14.
- A value no source states is labelled design, arithmetic or convention, as phase decision 1 asks.
