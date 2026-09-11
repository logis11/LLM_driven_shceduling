# Task 8.1 — Boot default from OSTEP

Re-source the boot default configuration so that every scheduler parameter rests on one source or one stated rule. Decided in the 2026-09-11 session that opened the scorer's grill and found the boot default's slice unsourced. Parent: `_dev/TODO.md`, (jioh, 8), sub-task 8.1; phase spec `phase-8-harness-upper-half-through-pre-registration.md`.

## Scope

- The MLFQ boot default and the EDF and LOTTERY slices in the recognition vocabulary, with the provenance table and a changelog entry.
- Every duplicate of the boot default: the daemon's config-schema code, the prior driver table, the two MLFQ mock fixtures, the prose examples in the contracts, guides, and proposal.
- The latency floor's rule in the metrics doc, with a changelog entry.
- The pair-review finding on `c7-meeting` and `c7-media`, redone on the new residual slice, and every sentence that rests on it.
- A team memo recording the change and the research that grounds it.

Out of scope: the boot-default sensitivity pair (the team's, after this lands); the scorer (8.2); memos and archives already written (point-in-time, untouched).

## Locked decisions

### 1. Single source for the MLFQ boot default

The MLFQ boot default is OSTEP §8's worked example, whole: three queues, a 10 ms top slice, doubling per level, a 100 ms boost. Read in version 1.10 of the chapter on 2026-09-11. The provenance table cites the section and figure for each value and quotes OSTEP's own caveat on the boost ("likely too small of a value, but used here for the example"). A configuration whose four numbers come from one text is one claim; a collage of sources is rejected.

### 2. Allotment equal to slice

The vocabulary's MLFQ demotes on one fully consumed slice and has no allotment field. The boot default takes OSTEP's slice ladder and boost with the allotment equal to the slice, as in OSTEP's Example 1; that OSTEP's Figure 8.6 uses a two-slice allotment is stated in the provenance table as the one point where the model and the example differ.

### 3. Same-granularity rule for EDF and LOTTERY

EDF's residual slice and LOTTERY's slice equal the MLFQ slice, so all three become 10 ms. The rule is the project's own control rule, stated as such with no source claimed: dispatch tenure is held equal across algorithms so a difference between rows is the policy and the cap, never the quantum. Citing a second source for either slice is rejected as a montage, including Waldspurger's coinciding 10 ms quantum.

### 4. The latency floor untied

The latency floor stays at 1 000 µs as a plain stated assumption and no longer derives from the slice. The half-slice rule was Phase 5's stated assumption and is retired with a changelog entry. The RQ0 gate spec pre-registers a floor-sensitivity reporting line: the verdict count recomputed under a band of floors at scoring time, printed beside the primary.

### 5. The prior table follows by its own rule

The prior driver table's rows carry the boot values by the rule in its header, so every MLFQ, EDF, and LOTTERY entry takes the new numbers through that rule; no row is re-judged.

### 6. Fixtures stay consistent with their config lines

The two MLFQ fixtures keep the agreement between the scheduler their derivation states and the configuration their config lines carry, either by following the new boot default or by stamping their 2 ms configuration explicitly. Which, per fixture, is decided in the work.

### 7. Finding 5 redone in the open

The residual slice moving to 10 ms changes the arithmetic behind Phase 7 pair-review finding 5 (the cap axis unmeasurable on `c7-meeting` and `c7-media` because one 2 ms residual slice is under every tick tolerance). The arithmetic is redone on the new slice and shown before the dependent sentences are rewritten: the pair review, the scoring spec's expected no-headroom header, the coreset guide, the RQ0 preparation notes' judging notes. Keeping 2 ms to preserve the finding is rejected.

### 8. Sensitivity pair left to the team

The vocabulary's sensitivity paragraph no longer names the alternative pair (OSTEP's example is now the primary). The pair is set by the team before execution; the paragraph says so.

### 9. Team memo

A memo records the change for 인경민 and 박이안: the new boot entry and simulator default, the research that found no standard MLFQ configuration (every value verified against primary sources on 2026-09-11), and the rules above.

### 10. Research facts carried

No source read claims a standard MLFQ configuration (OSTEP §8.5; Arpaci-Dusseau's Solaris handout). The only shipped table-driven MLFQs with all values in source are illumos/Solaris TS (60 levels, 2 to 20 ms at the default 1 000 Hz clock, aging once per second) and MINIX 3 (16 queues, 200 ms flat, one-level rise every 5 s); neither is expressible in the frozen schema. OSTEP has no EDF treatment and states no lottery quantum length. These facts go into the memo; numbers not read in a primary text are not written anywhere.

## Invariants

- Every parameter value in the vocabulary is either read from a named section of one source or derived by a rule the vocabulary states as the project's own.
- Memos and archives already written are not edited.

## Open items

- The boot-default sensitivity pair: the team's decision after this sub-task lands.
