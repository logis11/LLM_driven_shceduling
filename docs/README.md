# Docs index

> Status: normative · Created 2026-08-27 · Updated 2026-08-27

Every doc answers one question. Statuses: **normative** (states what is; kept current) · **draft** (content real, form not final) · **record** (append-only history; never rewritten) · **memo** (point-in-time communication). Decision history lives in `_dev/archive/`, machine-read files live outside `docs/` (see the placement rule in `CLAUDE.md`).

| doc | answers | status |
|---|---|---|
| [research-proposal.md](research-proposal.md) | what the project is, the system design, the experiment | draft |
| [research-claims.md](research-claims.md) | what we claim and what would falsify it | normative |
| [related-work.md](related-work.md) | how we position against prior work | draft |
| [references.md](references.md) | what we cite, in what form, for what claim — and the id-minting rule | normative |
| [terminology.md](terminology.md) | what our words mean | normative |
| [simulator/primer.md](simulator/primer.md) | what the simulator does and does not model | normative |
| [simulator/interpretation-contract.md](simulator/interpretation-contract.md) | how a canonical workload becomes scheduled tasks — the spec the simulator is built to | normative |
| [workload/building-plan.md](workload/building-plan.md) | how the dataset is built: two sets, four artifacts, build order | normative |
| [workload/archetype-plan.md](workload/archetype-plan.md) | how one process kind is specified and grounded | normative |
| [workload/scenario-catalog.md](workload/scenario-catalog.md) | which processes co-occur (S1–S18) and their taxonomy sources | normative |
| [workload/grounding-sources.md](workload/grounding-sources.md) | which source may justify which kind of claim (roles A–D) | normative |
| [workload/source-vetting.md](workload/source-vetting.md) | per-source verdicts and extracted numbers | record |
| [memos/](memos/) | point-in-time notes to the team | memo |

## Reading paths

**New member (~40 min):** research-proposal → simulator/primer → terminology → research-claims. That is the whole mental model; everything else is depth.

**Working on the workload dataset:** workload/building-plan → workload/archetype-plan → simulator/interpretation-contract → the citation recipe in references.md. Machine registry: `dataset/sources.yaml`.

**Working on the simulator:** simulator/interpretation-contract (the spec) → simulator/primer → workload/building-plan §5 (build order) .

**Writing the paper:** references.md (citations + roles) → workload/source-vetting (extracted numbers) → `_dev/archive/` (decision rationale).
