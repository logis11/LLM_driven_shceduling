# Hold time and hysteresis — plan

**Goal:** Decide whether the daemon needs flap protection, and if so fix the policy's form and values before the RQ4 run, with the values chosen on files disjoint from the ones measured and the result reported as a sweep over the values.

**Scope:** The daemon's post-recognition rule (daemon guide §9.3, open), the generated flap-stress set and the C3 return grid (audit record, 2026-10-11 direction), the RQ4 phase-shift family (research proposal, Family 4). Not scheduled to a phase line; the dataset prerequisites belong to the generated-layer work, the rest to the RQ4 line.

## Terms

- **Hold time** — after a configuration is applied, no new answer is applied for N seconds.
- **Hysteresis** — a new answer is applied only after it has been returned K consecutive times.
- **Flap** — a configuration applied and reverted within a short interval because of a transient or wrong answer.
- **Flap-stress file** — a generated workload whose process set changes several times at short intervals.

## Steps

1. **Measure the need with no rule.** Run the flap-stress set and the C4 files with hold time 0 and no hysteresis. Record (a) the number of wrong flips and (b) their Layer 2 cost. If the cost is below the measurement floor, no rule is adopted and the daemon guide §9.3 records the measurement; the plan ends here.
2. **Fix the policy's form.** Hold time N seconds and hysteresis K consecutive answers, applied by the daemon after validation and before the driver. Labelled design.
3. **Search precedent for the values.** The debounce intervals real systems use for comparable switches (frequency governors, mode switches, scheduler migration damping), under the citation rule in `docs/references.md`. A found value gives the range N and K are chosen from; none found, the values are labelled design.
4. **Split tuning from measurement.** The flap-stress set and the 3-segment return grid are split by pair or by seed into a tuning half and a measurement half. N and K are chosen on the tuning half only, by a stated criterion (the Layer 2 cost summed over the tuning half, minimised).
5. **Freeze.** The chosen N and K are pre-registered in the RQ4 experiment spec before the run, the way the RQ0 gate spec pre-registers the boot default.
6. **Report as a sweep.** The RQ4 result is reported over a set of N values (and K where it matters), the frozen pair marked as the representative point, the way the RQ0 gate sweeps the boot default. The claim is read off the sweep, not the point.

## Dataset prerequisites

- The flap-stress set: a few generated files, each a chain of mode changes from the C1 task sets at short fixed intervals (several values), splittable by seed.
- The 3-segment return grid A → B → A over the 240 ordered mode pairs with the middle length as a variant (60 s, 10 s, 2 s), splittable by pair.
- Both carry no realism claim and are recorded as design.

## Hands to

- Daemon: steps 1, 2, 4, 5 (the rule's implementation, the tuning run).
- Harness: the flip count and its Layer 2 cost as aggregates; the sweep in the RQ4 experiment spec and report.
- Dataset: the two generated sets above.
- Docs: daemon guide §9.3 restated to the decision taken; the final memo names the plan.
