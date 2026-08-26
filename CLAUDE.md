## Conventions

### Daily-work harness

The dev workflow (phases → sub-tasks, dispatch, branching, wrap-up) lives in the **`daily-work-harness` plugin** — its skills (`daily-work-harness:pick-up-task` / `:wrap-up` / `:rebase-with-main` / `:grill-to-spec`) and the `daily-workflow.md` reference doc they read. Operational rules it relies on:

- **`_dev/` lives on `main`.** `_dev/TODO.md` and everything under `_dev/docs/` is edited and committed on `main` only — never on a worktree/sub-task branch. Worktree branches carry implementation code only.
- **Decision sessions are archived.** Every decision-making session (grill, design discussion, spec session) leaves a history doc at `_dev/archive/<date>-<topic>.md`: the decisions with their rationale, and any facts verified during the session. Written at session end; source material for paper writing.
- **Citations.** `docs/REFERENCES.md` owns every citation and the id-minting rule (as its own section). To add a source: read that rule, add the REFERENCES.md entry, then add a `docs/workload-dataset-sources.yaml` entry only if the dataset derives values or structure from it. Never write a citation that isn't verified against a primary source — unverified entries are marked, not invented.
- **Implementation plans go to `_dev/docs/plan/`** as `task-<N.M>-<short>.md`.
- **Nightly routine.** A scheduled Claude cloud Routine drains `autonomous-ready` issues into labelled PRs per the harness's autonomous contract; triage with `daily-work-harness:review-nightly`. Labels must be provisioned on the repo.
- **Commit convention:** conventional commits — `<type>(phase-<N>): …` for phase/sub-task work, bare `<type>: …` off-phase.