# Harness changelog

The harness tree's own record of what its committed data files and programs changed, newest first. The scoring spec (`scoring/scoring-spec.yaml`) and the guard spec (`guards/guard-spec.yaml`) are frozen here (Phase 8 spec, decision 19): a change to either after its freeze is an entry below before any run reads it, and the RQ0 gate spec (`experiments/rq0-gate.yaml`) pins the frozen bytes by hash. The metrics doc and the data contracts keep their own changelogs.

## 2026-09-12 — freeze of the scoring spec and the guard spec (jioh 8.8)

- **Scoring spec frozen** as of this commit: 48 files, 78 terms, the weights and windows of Phase 6 with the Phase 7 bases and counterparts. Pinned by SHA-256 in the RQ0 gate spec. Frozen by 인지오 alone; team ratification follows in a team meeting.
- **Guard spec 0.1 → 1.0**: the eight guards and their thresholds unchanged, the `c2_pair` body-hash amendment of 2026-09-11 included. The `starvation_floor` threshold stays the stated assumption of 1 000 000 µs; 인경민's declared executor window replaces it as a new version here before any run.
- **RQ0 gate spec committed**, `experiments/rq0-gate.yaml`: the 25 judging files, K = 13, g = 0.5, N = 100, the nine-point boot-default sweep, the executor-rule assumptions, the failure procedure, the reporting lines, the one exemption, the pins. Its pending items (인경민's three answers, 박이안's confirmation of the `random` reading and N) are recorded there when they arrive; a changed value is an entry here before any run.
- **Boot defaults**: nine alternative files `boot-defaults/ostep-slice-<µs>us.json`, OSTEP's MLFQ with only the top slice changed, one per sweep point.
- **Per-experiment spec schema and RQ0 gate evaluator**: `statements` echoed verbatim into the report, per-point `reasons` on the `sensitivity` line, the `g_band` line, the `seed_standard_error` line; the report schema gains `statements` (8.7 spec, amendment of 2026-09-12).
