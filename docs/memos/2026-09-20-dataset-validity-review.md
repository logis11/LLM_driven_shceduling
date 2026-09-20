# Dataset validity for the recognition research — a review

> Status: memo · Created 2026-09-20 · Updated 2026-09-20
> A read of `dataset/archetypes.yaml`, its grounding documents and the 9.5 measurement method against what the research's two claims need from the workload dataset. Assessment only; nothing in the repository was changed.

**Verdict: sound for the recognition claim, bounded for the scheduling-benefit claim.**

## 1. The recognizer reads identity, not timing

The recognition layer's input is process identity — names, and the post-fold annotation such as `chrome (25 procs)`. It never sees a parameter distribution. So the campaign's per-microsecond fidelity does not carry the claim that inference over names reads a situation a curated name table cannot. What carries it is the compile path: same timeline, same library, same seed produces a byte-identical workload, and each intent pair's second file is produced by a derivation recipe from the first, so the two differ in exactly one segment and nothing else. That is a determinism property, not a measurement property.

The campaign is load-bearing for the other claim — that acting on the recognition changes scheduling outcomes. Tail wake latency, miss rate and makespan are direct functions of the measured burst and gap distributions.

## 2. What the measurement apparatus establishes

The stability rule is a t interval across independent same-machine repeats, evaluated after each landed repeat, with a five-repeat minimum and the observation held to one CPU model. Its three method references are read against their primary texts and carry the scope notes where our use departs from them: Georges et al. (OOPSLA '07) for the confidence-interval-over-runs form and the Student-t rule below thirty measurements, Kalibera & Jones (ISMM '13) for repetition at the highest level of random variation, on-line stopping, and the statement that counts below five cannot estimate the variance, Maricq et al. (OSDI '18) for holding an observation to one CPU model.

What it establishes is precision on one configuration. It does not establish representativeness across the dimensions the campaign holds fixed — machine, application version, document, user. The public CI campaign establishes reproducibility, which is a separate property from representativeness and should be claimed in a separate sentence.

## 3. Publish the stability ledger

`dataset/tools/meas/campaign/pool.py` already computes, per carried quantity, the confidence half-width, whether it met the tolerance, and the repeat count at which the present spread would hold. The compile-family entries already carry the result in prose — the four disk-bound values with their half-widths (`clamscan` 218.1 µs ±9.5 %, `python3` 220.0 µs ±14.0 %, `tracker` 17.6 µs ±15.1 %), the rule that no reported result may rest on a difference smaller than the stated half-width, and the statement that the rule held over the orchestrator's fourteen repeats.

Carry that to the whole library and report the summary: how many quantities met the tolerance, how many are carried under a stated exception, and the largest half-width carried. It is the evidence no comparable workload suite reports, and without it the stability rule reads as decoration.

## 4. State the demand window as a scoping decision

Every compiled single-lane file of the oversubscribed demand class is built to land in the ~100–150 % window by the static estimate, and a file outside it is redesigned rather than waved through. Below contention no scheduling policy differs, so the regime is the right one to measure in — but it is chosen, not found. Say so first, in the paper's own words, and scope the benefit claim to machines under contention.

## 5. The bound on the benefit claim

Every measured archetype's scope paragraph states it: the values are that software on that machine — a hosted runner under Xvfb with no display refresh, no GPU and no sound device, the application tree pinned to one core, no human — and not desktop truth. Real-desktop validation is deferred as a stated limitation.

That bounds the claim without blocking the research: the benefit number holds on these workloads, not on desktops. Either carry that scoping into the paper, or run one bounded comparison against a real desktop with a display and a GPU and report the offset, which converts the limitation from unbounded to measured.

## Untouched

Segment composition. Which application runs when, for how long, beside what, is authored from averages — about twelve minutes per working sphere and about three minutes per task (González & Mark, CHI 2004), with a power-law switching shape (Zhang et al., CHB 2015) — because no source publishes sampled per-user segment-duration distributions, which `docs/workload/source-vetting.md` names the highest-risk role. Desktop validation of per-application behaviour does not touch it. The pre-registered stimulus-sensitivity check of the 9.5 campaign is the template a segment-length sensitivity sweep would follow.
