# 9.16 docs chunks — the brief every docs agent follows

Repo `/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling`, branch `jioh/dataset-rebuild`. Spec: `_dev/docs/spec/jioh/task-9.16-exit-audits.md` (decision 4: findings fixed in 9.16; docs after code and data). 인지오's answers: `decisions.md` (D1–D6) here.

Findings to apply (every one whose location is in your files):
- `claims/outside-findings.md`, `claims/dataset-findings.md` (the trace audit);
- `reads/B1-compare.md` … `reads/B4-compare.md` (the blind re-reads; their WORDING-FIX / CONTRADICTED / NOT IN SOURCE entries; an UNVERIFIABLE one stays as it is — its earlier record stands);
- `compiled/findings.md` (the parts outside `harness/` and `daemon/`, which H1 applied — see `logs/H1.md`);
- `handed/findings.md` (F1's doc mentions as restated by D1; F2; F3 as a label in `docs/workload/archetype-plan.md`);
- `meas/class-findings.md` (F3, F4, F5 doc parts — F5: state as a fidelity gap that the 12 hidden renderers wake together across processes in the measurement while the bound renderer tasks compile independently), `meas-new/proposed-text.md` (doc parts);
- the D2 row (research guidebook vol-01's foreground-window row: Windows cell only), and D-F4-45 (`docs/workload/measurement-overview.md:51`): restate the Steam-window sentence as a limitation the measurement did not test — Chromium on Linux computes no occlusion of its own and on X11 marks a window occluded when the X server reports it fully obscured; whether the depicted desktop delivers that report was not tested.
Where two findings disagree, the blind re-read's passage wins over a trace finding.

Not yours: anything in `dataset/` (archetypes, timelines, sources.yaml, grids.yaml, tools) — the data chunk applies those; `harness/` and `daemon/` (done in H1); pins and manifest hashes (a later propagation chunk updates them after the rebuild); `_dev/` outside this folder.

Rules:
- Restate to what the record or passage says; never add chat-derived justification or argue against alternatives; keep the users' own terms; match the file's language (the guidebooks are Korean with English terms) and style.
- Never a bare label (decision number, id, letter) without saying what it is.
- Every doc under `docs/` you change: bump `Updated` in its header to 2026-10-17.
- Do not commit. Write `logs/<chunk>.md`: per finding id, the file:line changed and how, or why skipped.
