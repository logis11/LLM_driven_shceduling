## Conventions

### Daily-work harness

The dev workflow (phases → sub-tasks, dispatch, branching, wrap-up) lives in the **`daily-work-harness` plugin** — its skills (`daily-work-harness:pick-up-task` / `:wrap-up` / `:rebase-with-main` / `:grill-to-spec`) and the `daily-workflow.md` reference doc they read. Operational rules it relies on:

- **`_dev/TODO.md` is the team-wide tracker.** One `##` section per person — 인지오 (`jioh`), 인경민 (`kyungmin`), 박이안 (`ian`) — each with its own `### Phase N` numbering; a phase is identified as `(person, N)`. The harness skills operate on 인지오's section only; the other sections are tracking.
- **Per-person namespacing.** Specs `_dev/docs/spec/<slug>/phase-<N>-*.md`, plans `_dev/docs/plan/<slug>/task-<N.M>-*.md`, handoffs `_dev/docs/handoff/<slug>/…`, worktree branches `<slug>/phase-<N>/<M>-<kebab>`. These override the un-namespaced paths in the plugin's `daily-workflow.md`.
- **`_dev/` lives on `main`.** `_dev/TODO.md` and everything under `_dev/docs/` is edited and committed on `main` only — never on a worktree/sub-task branch. Worktree branches carry implementation code only.
- **Decision sessions are archived.** Every decision-making session (grill, design discussion, spec session) leaves a history doc at `_dev/archive/<date>-<topic>.md`: the decisions with their rationale, and any facts verified during the session. Written at session end; source material for paper writing.
- **Citations.** `docs/references.md` owns every citation and the id-minting rule (as its own section). To add a source: read that rule, add the docs/references.md entry, then add a `dataset/sources.yaml` entry only if the dataset derives values or structure from it. Never write a citation that isn't verified against a primary source — unverified entries are marked, not invented.

### Docs

- **Placement.** `docs/` holds prose for humans only — anything a program reads lives with the program (`dataset/` for workload-dataset data + tools, simulator tree when it exists). Decision-session history goes to `_dev/archive/`, point-in-time notes to `docs/memos/<date>-<topic>.md`.
- **Naming.** lowercase-kebab filenames; no version/status suffixes (`_v2`, `_draft`, `_rev2`) — status lives in the header, revision history inside the doc.
- **Header.** Every doc under `docs/` opens with `> Status: <status> · Created <date> · Updated <date>` right after the H1. Statuses: normative · draft · record (append-only) · memo. Bump `Updated` in the same commit as any content change.
- **Index.** `docs/README.md` lists every doc with what it answers, plus onboarding reading paths. A new, renamed, or re-statused doc updates the index in the same commit.
- **Implementation plans go to `_dev/docs/plan/<slug>/`** as `task-<N.M>-<short>.md`.
- **Nightly routine.** A scheduled Claude cloud Routine drains `autonomous-ready` issues into labelled PRs per the harness's autonomous contract; triage with `daily-work-harness:review-nightly`. Labels must be provisioned on the repo.
- **Commit convention:** conventional commits — `<type>(<slug>/phase-<N>): …` for phase/sub-task work, bare `<type>: …` off-phase.