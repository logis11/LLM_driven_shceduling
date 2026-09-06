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

**Answer to §4.1 of the notes.** Five of the six C1 files sit at 0.00–0.54 of one lane; `c1-gaming` is at 1.46, inside the oversubscribed window (the notes' suspicion about its `lane_share: 0.9` chain was right). **The RQ0 judging set is C2's 6 files, not 12**; all six sit inside the demand window; C1 stays reporting-only.

The inference in §4.1 — calibration implies low contention, therefore little random-vs-oracle separation — does not hold as stated. Demand bounds throughput headroom, not latency headroom: at 0.8 utilisation two tasks still become runnable at the same instant, and a keystroke arriving while a batch task holds the lane still waits a slice. C1 is excluded from judging because its designed role is the baseline where the whitelist scores perfectly (building-plan §3 C1), not because it has no headroom. Recorded so that nonzero C1 gap numbers are not read as a surprise when they come in.

**`c1-gaming` as an accidental natural experiment (decided).** At 1.46 it is the highest-demand file in the coreset and the only single-situation file inside the window, so it partly breaks the confound between family type and headroom: gap size can be read against demand level separately from family. Kept out of the judging set for two reasons, the second mattering more: it has no pair, so no attribute variation (C2 tests attribute recognition, this file tests mode recognition, with a different primary metric); and selecting the highest-demand file after reading demand numbers is selection along an axis correlated with expected gap size. Decision: a pre-registered **separate reporting line** in the Phase 7 gate spec, reason recorded in-file including that it was added after reading demand estimates and before execution. Recorded in the notes' §8 gate sketch on 2026-09-06 so the timing is in git.

Side findings: `c6-spoof` and `c6-fold` are declared `calibration` (0.95 and 0.45), `c6-dual` is `oversubscribed` (1.28); native and single modes differ only for `c1-gaming`/`c4-gaming` (1.23 native vs 1.46 single), every other file's lane scaling is the identity. The dataset README's demand-window sentence claimed every `-single` file must land in the window; corrected in the same commit to say `oversubscribed`-class files, `calibration` exempt.

**Follow-up check (user-raised).** `c1-gaming.timeline.yaml` carries no per-file window exception; `meta.demand` is the only per-file demand field the parser accepts, so the calibration class is the whole exemption. Its 1.46 decomposes as game chain + tail 1.06 (the frame-critical members are scaled to `lane_share: 0.9` by the compile pass, the near-idle tail adds the rest) + gamescope compositor 0.40; nothing checks the sum, so staying under 1.50 is not enforced. Building-plan §5a claimed every `-single` file lands in the window and never mentioned the calibration exemption; amended (§3 C1 and §5a) in this session, which pre-empts 3.4's building-plan item.

**C6 demand classes (user-raised check).** `c6-spoof` (0.95) and `c6-fold` (0.45) inherit `demand: calibration` from `c1-browsing` constructively — the test suite holds `c6-fold`'s task set identical, the coverage grid places `c6-spoof` at browsing/S2/tier 1. Consistent. Task-2.4 §3 requires "any per-file exception a visible authored declaration": the declaration is visible in the generated files but not authored — no variant spec in the coreset mentions `demand`; the deriver copies the base `meta` wholesale, so all eight C1-derived files (`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`) carry calibration by inheritance. `c6-spoof` is the notable case: authored to add demand, 0.95 sits just under the window floor, and the inherited class is what silences the lint. Unresolved — either an explicit `patch-meta: {demand: calibration}` per variant (deriver supports it) or amend the spec's sentence to admit inheritance. **Paper note:** C6 is internally mixed (two calibration, one oversubscribed); needs a footnote if demand class appears in the paper's dataset table.

## Task 3.2 — `c6-dual` finding

Read against `recognition-vocabulary` §1–§2, `daemon-guide` §3–§5, and the timeline. No daemon code exists; this is what the specs imply.

- **The file.** One 240 s segment, `mode: ambiguous`, `attributes: {dual_active: true}`, **no `background_wanted`**. Tasks: game chain (`lane_share: 0.6`), editor `code` (focused 2–238 s), `make` + 85 `cc1` from 10 s, wineserver. Two query points: t = 0 (game, code, wineserver) and t = 10 s (make with its children) — two and not three because spawned children appear in telemetry together with their parent, attributed to the parent's arrival (`data-contracts` §4 "children" entry; `daemon-guide` principle 2), so the first `cc1` birth is not a set change.
- **What the oracle reads.** At both query points the answer key gives a mode off the 16-mode menu, an attribute that is ground-truth-only, and no value for the one graded attribute. The vacuous-true convention does not rescue `background_wanted`: it applies to segments with no sustained background work, and this segment has a build.
- **What the validator does.** The five written rules cover the `cpu_scheduler` block only; the `system` block's handling is stated by the closed-vocabulary rule (outside the menu → rejected, never improvised) and `daemon-guide`'s `held` definition (unknown vocabulary → rejected). So the oracle's answer is rejected at t = 0; nothing usable has ever arrived, so the file runs on **`fallback`** for its whole length under the oracle condition. Whether the oracle *emits* an off-menu answer, emits nothing, or picks a foreground mode is unspecified — three different logs, same schedule.
- **Consequences.** (1) On `c6-dual`, oracle ≡ `fixed`; `random` draws legal answers and can beat the oracle. A guard that flags "random beats oracle" must not treat this file as a bug. (2) The provenance breakdown for the oracle condition will show 100% fallback on this file — correct, and the reason the breakdown accompanies every number. (3) Nothing in RQ0 is affected: `ambiguous` segments are excluded from accuracy scoring (vocabulary §1) and C6 is excluded from Layer-2 aggregation (notes §6). (4) 박이안's oracle needs a defined behaviour before it is built; one sentence now sits in `daemon-guide` under the condition table naming the gap and deferring it.
- **Not changed.** `recognition-vocabulary` is normative and untouched; deciding the oracle's behaviour is not this phase's call.

### Review of the 3.2 finding (user) — outcomes

1. **No-crash contract for the oracle** — added to `daemon-guide` beside the gap paragraph: terminate normally and emit a valid schedule and log for every coreset file; semantics on unusable ground truth stay undefined, failure is not permitted. Same principle as the driver table's unreachable-row defaults.
2. **Held proposals produce schedule entries** — settled in `data-contracts` §7 while still draft: every query point yields exactly one schedule entry; a rejected proposal repeats the config in force with provenance `held`, stamped at query point + latency; entries are never elided for an unchanged config. Consistent with `held` already being a schedule-entry provenance value and with archive Q3's decision that held/fallback must stay visible. On `c6-dual` the oracle's breakdown is therefore one `fallback` entry (t = 0) plus one `held` entry (t = 10 s), not "100% fallback" — the earlier wording above is superseded by this.
3. **`background_wanted` lint rule** — implemented in the timeline loader, test-first: every segment carries a boolean `background_wanted`; on `mode: ambiguous` it must be absent (the label itself is the explicit marker). **The coreset did not already pass**: `c1-idle` carried `attributes: {}`, against the vocabulary's vacuous-true convention — the oracle would have hit the same missing-attribute dead end on a C1 file in the run set. Fixed to `background_wanted: true`; `c1-idle`'s ground truth and its two artifact hashes changed; nothing derives from it. Test fixtures updated to carry the attribute.
4. **Guard exemptions as data** — `guard_exemptions` block added to the notes' §8 gate sketch with `c6-dual` exempt from `random-beats-oracle` and `fallback-share`, reason inline; Stage 4 audits the full guard list. Transcribed into the gate spec file in Phase 7.
5. **Query-point count** — verified against the pinned-events rule: two. Citation added above.
6. **Limits-section sentence (paper note)** — the vocabulary contract admits no legal expression for `c6-dual`'s situation, so the system degrades cleanly to no-recognition even when handed perfect information; the fail-safe path is exercised by construction rather than asserted.

## Task 3.3 — protocol freeze, contract by contract

Presented and approved one at a time; each froze with the clarifications below. Facts verified in-session are marked.

- **3a Run file — frozen.** Freezes an extraction rule (drop `ground_truth`, reduce `meta` to `workload_id`), not a format; every field inside is already under contract 3. Verified: today's `c1-idle` ground-truth fix left its run file byte-identical — a label correction must not change what the simulator runs, and the harness cache keyed on the run-file hash gets that for free. Recorded choice: thin `meta` means a trace is tied to a build via the manifest and the simulator version in its header, not via the run file.
- **3b Visible projection — frozen, one entry per canonical task instance, never folded.** The draft's closing sentence read as folding 13 `chrome` tasks into one entry with a count, a field the format did not show; two loaders would have disagreed. Per-instance entries keep separately-authored same-name tasks' distinct lifetimes; the telemetry builder aggregates by name anyway. Only `children` carry `count`.
- **4 Telemetry — frozen with five snapshot rules.** (1) The set is the name→count multiset, so count-only changes emit a snapshot. Verified from the build: under a names-only rule `c6-spoof` would have 1 query point instead of 3 — its spoofing `chrome` arriving among 13 existing ones would never be seen, turning the file into a second `c6-fold`; `c2-p2a` drops from 3 to 2 the same way. (2) One snapshot per timestamp. (3) `processes` sorted by name, for bit-identical reruns. (4) The terminal snapshot is emitted — verified: all 24 files have their last set change at the final instant, and the projection carries no duration, so the daemon cannot know it is the end; the resulting schedule entry lands at or after the end and is ignored downstream. (5) Nothing else emits. The example's first snapshot (59 s, "just before the 60-second mark") was wrong — nothing changed at 59 s — and moved to t = 0.
- **6 Config schedule — frozen with four mechanics rules.** Order: boot entry first, then sorted by `t_us`, ties by emission order, last applied in force — needed because zero-latency conditions (`oracle`, `random`) stamp their first answer at t = 0 alongside the boot entry. Sorting means a slow answer to an older snapshot can overwrite a newer one; the contract records that and defers any stale-answer policy to the daemon (visible in the log), which keeps the four-value provenance enum untouched and matches what a non-cancelling real daemon does. Payload is post-validation. The simulator rejects the whole file on a schema violation rather than repairing an entry. Entries at or after the end are ignored. Switch semantics (drain, carry-over) stay with the simulator guide.
- **7 Recognition log — envelope frozen; the `proposal` slot follows contract 5.** Rationale for freezing now: 박이안's Phase 1 milestone emits logs for `fixed`/`random`/`oracle`, whose proposals are only the `system` block, already fixed by the vocabulary; what is open in 5 is the LLM-facing `subsystems` part. Added because the prose promised them without a field: every condition fills `proposal.system` the same way, optional `source` for per-condition audit detail (grader ignores it), top-level `seed` for `random`, `proposal: null` + optional `raw` for unparseable answers (also the slot 3.2's oracle gap will need), `validation` mirrors the schedule's `provenance` sequence minus the boot entry (a free guard), grading scope (non-`ambiguous` covering segment required; terminal snapshot skipped), latency 0 for non-LLM and record-time latency in replay, `t_set_change` = snapshot `t_us`.
- **5 Proposal — stays draft**, with a lead-line note that it hardens with the driver-table contract in Phase 4.
- **Glossary `frozen`** no longer requires enforcing code as a precondition; enforcement follows the first consumer. **§12 Changelog** added, first entry this freeze. §11 and the intro rewritten from future to past tense.
- **Left for 3.4:** the doc-level `> Status: draft` header on data-contracts itself, and other docs' references to these contracts as drafts.

## Task 3.4 — vocabulary and status sweep

**Retired vocabulary — fixed.** `terminology.md` Mode/Attribute paragraphs rewritten on the ratified vocabulary (16 modes, `ambiguous` ground-truth-only, one attribute `background_wanted`). `research-proposal` Part 5 tables: `interactive` → `office` (document work + mail) and → `indexing` (indexer + editor); the ML-training row said `compile` where the coreset file it describes (`c2-p1a`) is labelled `ml-train` — corrected to match the dataset. Repo-wide grep for `has_realtime_encoder`, `background_is_wanted`, `interactive`-as-mode and "modes only" is clean.

**Milestone table — fixed.** Part 9 Phase 1 no longer says "modes only, no attributes"; it runs on the full vocabulary through driver table v0, because the C2 judging set differs only in `background_wanted`. §7's matching prose rewritten. Phase 2's "full vocabulary" deliverable dropped (now Phase 1's); reads `whitelist` + driver table v1 on the throwaway tuning pool. Phase 1's gate text ("redesign before proceeding") left as is: the config-search-first failure procedure (notes §4.3) still needs agreement before it enters the proposal.

**Status headers — decided one by one.** data-contracts → normative (nine of ten contracts frozen; the open section is labelled at section level). daemon-guide → normative and simulator-guide → normative: a `draft` label on a builder guide is the §8.3 failure mode — it invites quiet deviation on the fixed parts — and a normative doc can state its open items (daemon-guide's oracle gap, simulator-guide §9). background-guide → normative (states what is, kept current). research-proposal and related-work stay draft, genuinely in progress. Index rows and `Updated` dates bumped; verified: all 16 headers match their index rows.

**Stale against the freeze — fixed.** simulator-guide's config-schedule input section gained the three mechanics the simulator must honour (ordering with same-time last-wins, whole-file rejection on schema violation, entries at/after end ignored), pointing the schedule-vs-task-event tie at §9.3.

**Design divergences — listed for Phase 4, not fixed:**
1. `research-proposal` §5.2, `llm_algo` row: "params from table" — cannot hold under validator rule 2 (notes §4.7).
2. `research-proposal` §4.6, the variant-B narrative.
3. `recognition-vocabulary.md` variant table, row B: "params and cap from the table".
4. `daemon-guide` §5: the config mapper presented as straightforward wiring once the table lands.
5. `data-contracts` §6 (proposal contract) — stays draft; its `subsystems` slot's meaning under variant B follows the table format.
6. Archive Q5's ceiling claim (A and B bounded above by the oracle) — needs settling before or with the format decision.

