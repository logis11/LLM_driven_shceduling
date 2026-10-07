# Task 9.11 — changelog

One entry per decision applied to the scheduler-side constants and their groundings (`docs/harness/metrics.md`, `docs/recognition-vocabulary.md`, `harness/guards/guard-spec.yaml`, `harness/experiments/rq0-gate.yaml`, and the registry lines they cite). Parameter, old value, new value, source id and locator or the label, commit. References are the search records' candidate ids (`search/candidates.md`).

## D1 — `T_interaction` stays 100 000 µs, grounded as a guideline with a measured cross-check (2026-10-07)

By 인지오's decision, scope-card item 1: the value is unchanged; its grounding is restated to what the sources are.

- **The guideline.** `miller-fjcc68` (S1-01), p. 271, Topic 1: control-activation feedback "No more than 0.1 second"; key-to-visual echo "no more than 0.1 to 0.2 seconds", "far too slow for skilled keyboard users". Miller calls his delays "the best calculated guesses by the author" and asks that they be accepted "as indicative rather than conclusive"; no subjects, no source for 0.1 s. It is the only candidate that names keyboard input, the dataset's only input kind (every stimulus stream carries `kinds: [key]`).
- **The restatement.** `nielsen-ue93` (S1-05) restates Miller 1968 and Card et al. 1991 (not read, HTTP 403) as "advice"; its role changes from "secondary grounding" to a restatement, not an independent grounding.
- **The measured cross-check.** `deber-chi15` (S1-11), minted: latency just-noticeable differences against a 0.98 ms reference, 14 participants, p. 1831 — dragging 11 / 55 ms and tapping 69 / 96 ms, direct / indirect, the indirect form a touchpad and screen. The authors place key typing among the indirect tapping tasks behind "the textbook threshold of 100 ms", which falls within the 95 % confidence interval of their 96 ms. The other measured thresholds — Jota et al. CHI 2013 tap 64 ms (S1-10), Annett GI 2014 inking 53 ms (S1-12), Forch 2017 mouse ≈ 60 ms, abstract only (S1-13) — measure touch, stylus and mouse and are not taken. No keyboard-echo measurement and no released threshold dataset was found in the four classes (`search/candidates.md`, Not found, T1).
- **Kept.** `shneiderman-csur84` (S1-07), p. 268: Long 1976's 0.1–0.5 s keystroke-to-print delays slowed typists, cited as Shneiderman's report.
- **What the constant reads.** `ready_wait` rows with `cause = wake` and `channel = input`. A `ready_wait` is the scheduler's share of a keystroke's response only, so `over_threshold` is a lower bound on the share of keystrokes answered later than 0.1 s — now stated in §10.

Applied: `docs/harness/metrics.md` §10 — the table row's status "grounded (`miller-fjcc68`, `nielsen-ue93`)" → "a guideline (`miller-fjcc68`), cross-checked against a measured detection threshold (`deber-chi15`)"; the paragraph restated; its sentence calling the constant "one input to the `c1-media` weighting question in the scoring spec" removed, since that weighting (audio 1.0 : video 0.5) is a stated assumption that does not read `T_interaction` (`harness/scoring/scoring-spec.yaml:32–33`). `docs/references.md` — `miller-fjcc68` and `nielsen-ue93` role and status lines; `shneiderman-csur84` status line; `deber-chi15` added (paper-only, no `dataset/sources.yaml` entry). Not added to `metrics.md` §13: no primitive, aggregate, constant or floor changed.

Verification: the four copies re-downloaded on 2026-10-07 into `sources/S1-01`, `S1-05`, `S1-07`, `S1-11` (local, gitignored); Miller, Shneiderman and Deber byte-identical to the search record's SHA-256, Nielsen's HTML page changed in bytes (121 941 against 120 613) with every quoted passage present; each passage re-read in the copy.

Compiled effect: none. No scored term reads `over_threshold` (the scoring spec's 78 terms: 39 `ready_wait` P99, 26 miss rates, 6 progress, 7 turnaround). `T_interaction` is also the comparison point in the `starvation_floor` grounding, scope-card item 28, decided there.

Hands to: none.
