# Research-and-decision slices — workflow

How the Phase 9 research-and-decision sub-tasks (9.4–9.12) run. Fixed on 2026-09-13 while picking up 9.4. Parent: `_dev/TODO.md`, (jioh, 9); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Scope of a slice

- A domain slice (9.4–9.9) owns the archetypes of its domain: every parameter of each archetype, its bindings, its modeling notes, and the tags on its values.
- Timeline content — task sets, co-occurrence, order, counts, process names, scenario structure — belongs to 9.10, whichever domain the timeline depicts.
- A count held inside an archetype leaves the archetype by the domain slice's decision; the number the timelines then carry is 9.10's.
- A registry entry follows the claim it grounds: archetype value → the domain slice; scenario or timeline claim → 9.10.

## Stages

1. **Scope card.** The slice's item list, derived from the 2026-09-13 verification records (`2026-09-13-verification/claims.md`, `topics.md`, the memo's findings): per item its current value, current tag, the verification verdict, and its kind — source claim, convention, arithmetic, placeholder, design. Boundary calls against the other slices are written on the card. 인지오 reviews the card before any search.
2. **Search.** Per item, the four classes of phase decision 4: literature; project and vendor documentation and source; public traces and datasets; observability on a CI runner (a runner measurement follows `measurement-campaign-workflow.md`). Readers receive topics in the neutral form of `topics.md`, never the repository's current values. Each read records the copy used (URL or commit, version, date, local path), verbatim passages with locators, and a coverage statement against the item list. The search log records terms, venues and results. Source copies stay local and gitignored, as 9.1 decided.
3. **Decision session.** Items are brought to 인지오 one at a time in chat with their candidates, each candidate's coverage, and a recommendation with its reference. Each decision is applied as it lands: `dataset/archetypes.yaml` amended (value, tag or label, modeling note), the dataset recompiled, committed with its changelog entry. The changelog is the slice's decision record; no task spec is written.
4. **Hand-off.** The changelog is the interface to 9.10, 9.13, 9.14 and 9.15 (each entry names what it hands to which task); the search logs, reads and changelog are the interface to 9.16's exit audit.

## Records

- Each slice has its own folder `_dev/research/jioh/task-<N.M>-<domain>/`: scope card, search logs, reads, candidates, changelog.
- **Changelog** — one entry per amendment: parameter, old value, new value, source id and locator or the label, commit. It lives in the slice's research folder only.
- The public docs (`docs/`, `dataset/README.md`) carry no changelog of Phase 9 corrections and no account of the prior values. They describe the final state; 9.15 brings them there.

## CI on the branch

The window check may fail on `jioh/dataset-rebuild` when an amended value moves a file's demand, until 9.14 redoes the demand-window rule. The changelog entry that causes it says so.
