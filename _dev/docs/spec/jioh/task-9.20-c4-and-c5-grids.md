# 9.20 — C4 and C5 grids, C5 → C6

Sub-task 9.20 of Phase 9 (spec decision 9, the generated layer): the C4 distractor grid and the C5 familiarity ladder generated over the sixteen C1 task sets, and the present C5 tier-3 file moved to C6. Direction recorded in `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md` ("C4 direction", "C5 direction", "Decision — focus enters the telemetry"); the generator and its composition rules are 9.19's.

## Scope

- The C4 distractor grid: the user keeps working in mode A and another process set appears beside it — the 240 cross-mode cells (another mode's task set) and the out-of-vocabulary cells (the library's measured programs that belong to no mode).
- The C5 familiarity ladder over the sixteen modes at tiers 3–5, the substituted names' carrier as an axis.
- The present C5 tier-3 file moved to C6 as the name-collision limit; the core set re-blessed and the RQ0 gate spec re-pinned.
- The two new generated sets in the build gate and in CI, one Linux CI run proving their manifests reproduce; the documents that describe the dataset's structure restated here.
- The unwanted-jobs measurement backlog given its timing.

## Locked decisions

### 1. The C4 cell is the transition grid's `focus` form with the focus kept on A

A C4 cell is two 60 s segments. A's C1 task set runs from the start; at 60 s B's set arrives by the generator's composition rules (9.19 decisions 1–3); the focus stays on A's holder to the file's end, A's input window runs to the file's end, and both segments are labelled A — the second segment's scenario list is A's with B's added, its `background_wanted` A's. The cell therefore has the same open programs as the transition grid's `focus` form for the same (A, B) and differs from it in the focus track, the input track and the labels alone. The TODO line's 30 s arrival is superseded by this shape.

### 2. One distractor set with two relations, no split

The C4 grid is one set, `distractor-grid`, 272 files. Cross-mode: the 240 ordered mode pairs, B's whole C1 task set arriving. Out-of-vocabulary: `element-desktop` (chat client, present to the file's end) and `7z` (file archiver, its `total_work` bound to the 60 s span, labelled design), each over the sixteen modes A, carrying the scenario tags the authored C4 files gave them. These two are the library's measured programs that belong to no mode's task set and leave the label unchanged; the library offers no third, and widening the list is a measurement backlog item, not this sub-task's. The set has no split: RQ1 tunes nothing on it. Each file's manifest record carries its relation, A and B (a mode or a program).

### 3. The 26 cells whose two focus holders share a name are built and annotated as pre-committed misses

Where A's and B's focus holders carry the same process name — `code` over dev, compile, ml-train and indexing; `kdenlive` over video-edit, render, transcode and backup; `chrome` over browsing and meeting — the C4 cell and the `focus` form produce the same telemetry (the focus holder is carried by name, telemetry rule 6), so the C4 label is unreachable. These 26 cells are built, their second segment annotated `pre_committed_miss: true`, and the manifest records the shared focus name per file.

### 4. The authored C4 files are existence cases

`c4-compile`, `c4-gaming` and `c4-office` are unchanged, their pins unchanged; their role is existence cases, as the C3 arcs are, not cells of the grid (their injection at 30 s within one segment is not the cell's shape). `c4-compile` is recorded as the authored precedent of the cell compile ← browsing.

### 5. The familiarity ladder: tiers 4 and 5 over the sixteen modes, the name's carrier an axis, no split

Each C1 file is generated with its names substituted at tier 4 (a nonexistent name whose words say what the program does) and tier 5 (a nonexistent name saying nothing), in three carrier forms — the focus holder's name alone, the other names alone, every name — with cells whose substituted name set coincides collapsed to one (a mode with a single program has one cell per tier; idle, with no focus holder, has one). The segment carries `familiarity: 4` or `5`; every file is `demand: calibration`. The set, `familiarity-ladder`, has no split; the manifest records each file's tier and carrier.

### 6. Tier 3: the two modes whose job ran under an opaque name in the measurement, beside the C1 files that already carry one

Tier 3 is the program's own real name that carries no meaning. The C1 files of compile (`cc1`), indexing (`tracker-miner-f`) and gaming (the chain's member names) already hold such names and are tier 3's cells as they stand. Two cells are generated where the campaign record shows the mode's job running under an opaque name of its own tree: render, `kdenlive_render` → `melt-7` (the child holding 99.6 % of the render's CPU), and backup, `deja-dup` → `duplicity` (57 % of the backup's CPU). Each name carries a source tag naming the campaign record. Helper processes that do not do the job's work (`oosplash`, `script-fu`, `RDD Process`, the session daemons' helpers) do not qualify.

### 7. How the substituted names are made

Tier 4 names come from a hand-written table in the grid definition, one name per real process name the C1 files use (the chain's member names included), each within the 15-character `comm` limit as written, never truncated; the table is design. Tier 5 names are keyed draws from the cell id and the real name, four lowercase letters, redrawn when the draw equals any real process name the dataset knows (every name in the timelines, the coverage tool's name table). Within a file one real name maps to one substitute, so name counts are preserved (`chrome × 5` stays × 5). A child name bound through the orchestrator's `child_name` is substituted by the same table and its `source` entry becomes `design`. The 15-character limit is grounded by the kernel's `TASK_COMM_LEN`, entered in `docs/references.md` as a deployed-system reference. Stated limit: the chain's `wineserver` member is named by the compiler, not the timeline, and keeps its real name in gaming's cells.

### 8. `c5-t3` becomes `c6-alias`

The recipe moves from the C5 recipe file to the C6 one under the id `c6-alias` — two players wearing indexers' names, the name-collision limit beside `c6-spoof`. Its segment drops `familiarity: 3` and gains `spoof: true` and `pre_committed_miss: true`; tasks, archetypes and seed are unchanged. `c5-t4` and `c5-t5` stay as authored, the existence cases of tiers 4 and 5. The core set is re-blessed; the RQ0 gate spec's reporting list names `c6-alias` in place of `c5-t3` and its dataset pin is re-pinned; the harness changelog records it.

### 9. The unwanted-jobs measurement stays in the backlog, with its timing stated

The attribute's `false` side rests on the sixteen C1–C7 pairs (the audit's C2 direction); today the ten interactive counterparts share one unwanted name, `unattended-upgr`. How many unwanted jobs the attribute claim needs is decided in the RQ1 experiment spec's session; the campaigns run after Phase 10's RQ0 run and before the RQ1 run. The backlog line is restated to say so.

### 10. Structure as 9.19

Each new set is an entry of the grid definition with its own manifest, built by the `generated` step, in `check`'s union of manifests and in the three workflows. One Linux CI run in this sub-task proves the manifests reproduce; its id goes to the changelog. The dataset README, the building plan (the C4, C5 and C6 rows and §3a), `docs/data-contracts.md` §14 and the harness changelog are restated here; the proposal, the research-claims chain and the daemon guide are 9.15's. The pins go to 9.16, the sets' size and build time to 9.21.

## Invariants

- Every generated file is design: it composes or renames the C1 task sets and claims nothing about how often desktops see the situation.
- Every seed and every tier-5 name is a keyed draw from the cell id; nothing is chosen by hand except the tier-4 table.
- The schema, the lints, 9.10 D44, 9.18's slice rule, the report sidecar and the compiler are unchanged.
- The 9.19 sets' artifacts are unchanged; their manifests move only where they pin the generator and the grid definition by content.
