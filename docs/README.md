# Docs index

> Status: normative · Created 2026-08-27 · Updated 2026-08-28

Prose only, organized by domain — one `##` section per area below, the full index table at the bottom. Statuses: **normative** (states what is; kept current) · **draft** (content real, form not final) · **record** (append-only history; never rewritten). Decision history lives in `_dev/archive/`; machine-read files live outside `docs/` (see the placement rule in `CLAUDE.md`).

**New member (~40 min):** [research-proposal](research-proposal.md) → [background-guide](background-guide.md) → [terminology](terminology.md) → [research-claims](research-claims.md). That is the whole mental model; everything else is depth.

## Research

The project itself: what it proposes, what it claims, how it is positioned, and the shared onboarding.

- [research-proposal.md](research-proposal.md) — the system design, research questions, experimental design, milestones
- [background-guide.md](background-guide.md) — self-contained onboarding for both builders: the experiment, the offline pipeline, the dataset, the vocabulary
- [research-claims.md](research-claims.md) — what we claim and what would falsify it
- [related-work.md](related-work.md) — how we position against prior work
- [references.md](references.md) — what we cite, in what form, for what claim — and the id-minting rule
- [terminology.md](terminology.md) — what our words mean

Writing the paper: references.md (citations + roles) → workload/source-vetting (extracted numbers) → `_dev/archive/` (decision rationale).

## Data contracts

The formats everything communicates through — the seams between the trees.

- [data-contracts.md](data-contracts.md) — every data format in the project, with explained examples and how they connect (includes the frozen trace format)
- [recognition-vocabulary.md](recognition-vocabulary.md) — the shared vocabulary: the 16-mode menu, `background_wanted`, the frozen `cpu_scheduler` config schema, the recognizer output schema

## Simulator (`simulator/`)

Reading order: background-guide → simulator-guide → data-contracts → interpretation-contract (the binding fine print).

- [simulator/simulator-guide.md](simulator/simulator-guide.md) — what the simulator must do, what's decided, what's the builder's to decide
- [simulator/interpretation-contract.md](simulator/interpretation-contract.md) — how a canonical workload becomes scheduled tasks — the spec the simulator is built to

## Daemon (`daemon/`)

Reading order: background-guide → daemon-guide → data-contracts.

- [daemon/daemon-guide.md](daemon/daemon-guide.md) — what the daemon must do, what's decided, what's the builder's to decide

## Workload (`workload/`)

How the dataset was designed and grounded. Reading order: building-plan → archetype-plan → interpretation-contract → the citation recipe in references.md. Machine registry: `dataset/sources.yaml`; developer README: `dataset/README.md`.

- [workload/building-plan.md](workload/building-plan.md) — how the dataset is built: two sets, four artifacts, build order
- [workload/archetype-plan.md](workload/archetype-plan.md) — how one process kind is specified and grounded
- [workload/scenario-catalog.md](workload/scenario-catalog.md) — which processes co-occur (S1–S18) and their taxonomy sources
- [workload/grounding-sources.md](workload/grounding-sources.md) — which source may justify which kind of claim (roles A–D)
- [workload/source-vetting.md](workload/source-vetting.md) — per-source verdicts and extracted numbers

## Harness (`harness/`)

Reserved — no docs yet; the experiment-harness docs land here when that work starts.

## Full index

| doc | answers | status |
|---|---|---|
| [research-proposal.md](research-proposal.md) | what the project is, the system design, the experiment | draft |
| [research-claims.md](research-claims.md) | what we claim and what would falsify it | normative |
| [related-work.md](related-work.md) | how we position against prior work | draft |
| [references.md](references.md) | what we cite, in what form, for what claim — and the id-minting rule | normative |
| [terminology.md](terminology.md) | what our words mean | normative |
| [background-guide.md](background-guide.md) | self-contained onboarding for both builders | draft |
| [data-contracts.md](data-contracts.md) | every data format in the project, with explained examples | draft |
| [recognition-vocabulary.md](recognition-vocabulary.md) | the shared vocabulary and the frozen config schema | normative |
| [simulator/simulator-guide.md](simulator/simulator-guide.md) | what the simulator must do; what's the builder's to decide | draft |
| [simulator/interpretation-contract.md](simulator/interpretation-contract.md) | how a canonical workload becomes scheduled tasks | normative |
| [daemon/daemon-guide.md](daemon/daemon-guide.md) | what the daemon must do; what's the builder's to decide | draft |
| [workload/building-plan.md](workload/building-plan.md) | how the dataset is built | normative |
| [workload/archetype-plan.md](workload/archetype-plan.md) | how one process kind is specified and grounded | normative |
| [workload/scenario-catalog.md](workload/scenario-catalog.md) | which processes co-occur and their sources | normative |
| [workload/grounding-sources.md](workload/grounding-sources.md) | which source may justify which claim | normative |
| [workload/source-vetting.md](workload/source-vetting.md) | per-source verdicts and extracted numbers | record |
