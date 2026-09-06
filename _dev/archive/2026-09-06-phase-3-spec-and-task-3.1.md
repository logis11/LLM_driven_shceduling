# 2026-09-06 — Phase 3 spec session and task 3.1: demand estimate into the manifest

Decision session record for the Phase 3 (verification and protocol freeze) spec, plus the finding from sub-task 3.1. Source: `_dev/docs/rq0-preparation-notes.md` Stage 0. Decisions with rationale; facts verified in-session noted as such.

## Phase split (preceding the spec session)

- Stages 0 through 6 of the preparation notes became Phases 3–8, one per stage except two merges: Stages 1+2 (Layer 1 is decided by hand-writing the mock traces that are Stage 2's fixtures) and Stages 4+5 (the harness upper half ends at the committed gate spec, the point of no return). Stage 0 and Stage 0.5 stay separate phases by choice.
- No team signatures are required on the driver-table format; 인지오 decides it. This removed the sequencing concern that would otherwise have forced Stage 0.5 into a parallel sub-task (the harness dispatches phases strictly in order).
- Noted for transcription, not yet acted on: the notes' §10 gates Stage 4 on the simulator's algorithm extension (6.3), contradicting §7's "mocks unblock all of this"; in the phase list Phase 7 depends on Phase 6 only. The L1 grader had no stage item and is placed in Phase 7.

## Phase 3 decisions

- **Sweep scope: vocabulary and status audit bounded by the two freezes.** Grep `docs/` for the retired vocabulary and audit every status label. Rationale: the notes argue for periodic label audits as cheap insurance; a full consistency review would overlap Phase 4's proposal corrections. Verified in-session: the retired vocabulary has more sites than the notes name — the proposal's Part 5 workload-family tables assign `interactive` as a mode value in two rows; `has_realtime_encoder` has exactly one site (`terminology.md`).
- **Stale lines are fixed in Phase 3; design divergences are listed for Phase 4.** The variant-B account in `research-proposal` §5.2/§4.6 and `daemon-guide` §5 has no correct text until the table format is decided, so it waits. Everything stale against a ratified freeze has a known answer today.
- **Five contracts freeze**: run file, visible projection, telemetry, config schedule, recognition log. The proposal contract stays draft with a note pointing at Phase 4, because its `algorithm` field's semantics under variant B is what Phase 4 decides. Verified in-session: data-contracts §11 describes one protocol freeze covering all six drafts; the notes named only three.
- **Frozen by ratified decision**, the config-schema and trace precedent. Verified in-session: the glossary defines `frozen` as requiring code/CI enforcement, which no contract can meet before its consumer exists. The definition is amended rather than schemas written; schemas belong with the first consumer.
- **Changelog section in data-contracts**, first entry the freeze. Verified in-session: three docs require a changelog entry by rule and none has a changelog; the only revision-history precedent is source-vetting's append-only rev block. Other docs touched by the sweep bump `Updated` only.
- **Demand estimate becomes a build artifact** in `dataset/build.manifest.json` rather than an archive-only number, so the paper can cite a committed value. Verified in-session: the compiler computed utilization and demand class but printed them to stdout only; the manifest carried hashes alone.
- **`c6-dual` finding gets one sentence in daemon-guide** at the oracle spec. Rationale: 박이안 reads daemon-guide, not the archive, and would otherwise hit the undefined behaviour silently.
- **Four sub-tasks** (3.1 manifest, 3.2 `c6-dual`, 3.3 freeze, 3.4 sweep); 3.3 before 3.4 because the sweep audits labels against the freeze. Executed directly on `main` without worktree or plan at the user's direction.

## Task 3.1 — finding

Per-file static utilization now recorded under `demand` in the manifest (rounded to four places, with `demand_class`). Artifact hashes unchanged; `make check` verified. Coreset `-single` values:

| file | utilization | class |
|---|---|---|
| c1-browsing | 0.45 | calibration |
| c1-compile | 0.54 | calibration |
| c1-gaming | 1.46 | calibration |
| c1-idle | 0.00 | calibration |
| c1-media | 0.45 | calibration |
| c1-office | 0.50 | calibration |
| c2-p1a / p1b | 1.20 | oversubscribed |
| c2-p2a / p2b | 1.29 | oversubscribed |
| c2-p3a / p3b | 1.12 | oversubscribed |
| c3-creation / workday | 1.04 | oversubscribed |
| c3-evening | 1.11 | oversubscribed |
| c4-compile | 0.54 | calibration |
| c4-gaming | 1.46 | calibration |
| c4-office | 0.60 | calibration |
| c5-t3 / t4 / t5 | 0.45 | calibration |
| c6-dual | 1.28 | oversubscribed |
| c6-fold | 0.45 | calibration |
| c6-spoof | 0.95 | calibration |

**Answer to §4.1 of the notes.** `calibration` does mean low contention for five of the six C1 files: they sit at 0.00–0.54 of one lane, so a scheduler has nothing to trade off and no random-vs-oracle gap can appear by design. `c1-gaming` is the exception at 1.46, inside the oversubscribed window (the notes' suspicion about its `lane_share: 0.9` task chain was right). **The RQ0 judging set is C2's 6 files, not 12.** C1 stays reporting-only. `c1-gaming` (and its C4 sibling at the same 1.46) is worth flagging when Phase 7 fixes the gate spec, as the one single-situation file with real headroom.

Side findings: `c6-spoof` and `c6-fold` are declared `calibration` (0.95 and 0.45), `c6-dual` is `oversubscribed` (1.28); native and single modes differ only for `c1-gaming`/`c4-gaming` (1.23 native vs 1.46 single), every other file's lane scaling is the identity. The dataset README's demand-window sentence claimed every `-single` file must land in the window; corrected in the same commit to say `oversubscribed`-class files, `calibration` exempt.

**Follow-up check (user-raised).** `c1-gaming.timeline.yaml` carries no per-file window exception; `meta.demand` is the only per-file demand field the parser accepts, so the calibration class is the whole exemption. Its 1.46 decomposes as game chain + tail 1.06 (the frame-critical members are scaled to `lane_share: 0.9` by the compile pass, the near-idle tail adds the rest) + gamescope compositor 0.40; nothing checks the sum, so staying under 1.50 is not enforced. Building-plan §5a claimed every `-single` file lands in the window and never mentioned the calibration exemption; amended (§3 C1 and §5a) in this session, which pre-empts 3.4's building-plan item.
