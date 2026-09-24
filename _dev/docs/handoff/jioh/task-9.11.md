# Handoff — task 9.11 Scheduler-side constants and groundings (2026-09-24)

Produced by the nightly research routine from issue #16. Stages 1 and 2 of `_dev/research/jioh/research-slice-workflow.md` are done; stage 3 (decisions) is 인지오's. Branch `jioh/dataset-rebuild`, everything committed and pushed.

## Files

- `_dev/research/jioh/task-9.11-scheduler-constants/scope-card.md` — boundary, 39 items in six groups (metrics constants; boot-default provenance; sweep backbone; guard groundings; Role B registry entries; hand-offs from 9.5 D11 and 9.6 D17), eleven neutral topics T1–T11.
- `search/input.md` — the reader input.
- `search/S1-literature.md` (19 candidates), `S2-project-docs.md` (28), `S3-traces-datasets.md` (10), `S4-ci-observability.md` (11; documentation and method only, nothing run on a runner).
- `search/candidates.md` — observations table, candidates per item, Not-found across classes.

Deviations from the routine: step 0 needed no edit, because the TODO line was already `[WIP] … (#16)` from `b29d1ec`. The four records landed in three commits as the readers finished, plus one commit for S2 and `candidates.md`, instead of one commit for all four. 9.9 was reopened upstream (`63a0f02`) while the card was being written, and the card was amended to say so.

## The one-observation situation

No single observation can ground the whole slice, and none is expected to. Most items are conventions, arithmetic or structural rules. The source-backed items rest on documents: one textbook example (OSTEP v1.10, S1-02, all four values quoted and confirmed), shipped-kernel constants read at tags (S2-01, S2-02, S2-08), and three guideline texts behind `T_interaction` (S1-01, S1-05, S1-07). Miller calls his 0.1 s value his own "best calculated guesses". The only measured perception thresholds are touch, stylus and mouse JNDs of 11–96 ms (S1-10 to S1-13), and none covers keyboard echo. Nothing was observed on a GitHub Actions runner.

Findings stage 3 should see first:
- Linux's EEVDF base slice has been 0.70 ms since v6.15, not 0.75 ms (S2-01). It is scaled by 1 + ilog2(min(ncpus, 8)), so the runner's 6.17 kernel is predicted to run at 2.1 ms.
- Every player and periodic tool found skips missed periods, or re-anchors after one. Only rt-app's non-default `absolute` mode catches up (S2-14 to S2-17).
- No source states interbench's 7 ms figure (S2-15).
- Waldspurger names no class ratio (S1-03).

## Stage 3's first question

Item 1, `T_interaction`: should the 0.1 s threshold stay grounded on Miller's guideline, now read as a stated guess, or on a measured JND, and for which input kind? A secondary question is whether it matters at all, since no scored term uses `over_threshold`. After that: item 26a (the 750 µs sweep point against the 0.70 ms and CPU-scaled base slice), then item 11/39 (the TIMER backlog rule against the skip behaviour every source shows).

## Flags from the readers

- Unreachable through the proxy (HTTP 403): github.com pages and api.github.com (raw.githubusercontent.com worked), lore.kernel.org, phoronix.com, openbenchmarking.org, ACM DL. Also HTTP 403: the OUP and Wiley copies of Field & Welsh, which was read from a third-party mirror. Springer and BMC served bot challenges. git.sesse.net and invent.kde.org returned 502, salsa.debian.org a credential redirect, manpages.ubuntu.com 503.
- Paywalled or not fetched: Ng et al. UIST 2012 (known only as others quote it), Card et al. 1991, Dietterich's journal version (the preprint was read), and Forch 2017 (abstract only).
- S3's GitHub-issue passages (S3-06, S3-08 to S3-10) came through WebFetch's rendered text. They are hashed as transcripts, not byte-exact copies.
- S2 read scx at HEAD `00fec1e`, not at a release tag. It also records a v7.2 mismatch: RT runtime is 1 000 000 in `rt.c` but 950 000 in the docs.
- The issue text calls the starvation window "question 3 of the heads-up memo". It is question 3 of memo 2026-09-11 §5, and the scope card records the discrepancy.
