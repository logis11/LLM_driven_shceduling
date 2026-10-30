# Docs index

> Status: normative · Created 2026-08-27 · Updated 2026-10-30

Prose only, organized by domain — one `##` section per area below, the full index table at the bottom. Statuses: **normative** (states what is; kept current) · **draft** (content real, form not final) · **record** (append-only history; never rewritten) · **memo** (a point-in-time note; never rewritten, a later fact appended as a dated correction). The research guidebook (`guidebook/vol-*`) carries no status header; its rows in the full index give the state its README lists for each volume (완성 complete, 초고 draft). Decision history lives in `_dev/archive/`; machine-read files live outside `docs/` (see the placement rule in `CLAUDE.md`).

**New member (~40 min):** [research-proposal](research-proposal.md) → [background-guide](background-guide.md) → [terminology](terminology.md) → [research-claims](research-claims.md). That is the whole mental model; everything else is depth.

## Guidebook (`guidebook/`)

A textbook series that teaches the whole research from zero operating-systems background, in Korean with English terms. Self-contained: no status headers, no section-number cross references — a concept needed again is restated where it is needed. Volume list with each volume's state, and the in-text devices — three that connect the content, four that mark what is not yet settled, and vol-06's 재구축 이후 (after the rebuild): [guidebook/README.md](guidebook/README.md).

- [guidebook/vol-01-systems-and-scheduling.md](guidebook/vol-01-systems-and-scheduling.md) — 공부용 (Korean): processes and states, context switch cost, the performance metrics and why averages lie, FIFO / SJF / STCF / Round Robin / priority / MLFQ / lottery / fair-share / EDF worked by hand, periodic work and chains, what Linux, Windows and macOS actually ship, and the hand-written semantic tables inside them
- [guidebook/vol-02-related-work.md](guidebook/vol-02-related-work.md) — 공부용 (Korean): how to read a systems paper and what each of the four kinds of citation may support, the classics behind the algorithms with their verified quotes, then the four lines of work — policy-replaceable mechanisms, behavioural inference, learned schedulers, LLM agents for kernel policy — plus the shipped name tables measured file by file, the benchmark landscape and why the dataset had to be built, the two-axis map, and how a related-work section is constructed from the objections it absorbs. Every quote is read from the primary source, with the edition, version and access date given in place; where two versions of a paper differ, the volume says which one a sentence comes from, and no place is left marked 확인 필요 (to be checked)
- [guidebook/vol-03-the-research.md](guidebook/vol-03-the-research.md) — 공부용 (Korean): the research itself, in outline — what the hardcoded tables can and cannot express, the recognition layer as an architecture (shared signal, thin consumer drivers, the slow-loop/fast-loop split and why its floor is an ordinary scheduler), why the model is not handed subsystem configuration and the admission test that keeps the vocabulary shared, the four things a proposal may never do and the four provenance outcomes worked through one by one, the claim in its two forms and the two mechanisms a name table fails by, the seven-link chain (link 1–link 7) with a diagnosis procedure for reading a result table, RQ0–RQ5 with the pre-registered gate and the good-table/bad-table instrument check, what falsifies the claim and what is never claimed, the honest weaknesses including the single-lane record and the author overlap, and the three sub-claims a deployment argument would need. Marked open wherever the repo is open; nothing beyond RQ0 is stated as decided
- [guidebook/vol-04-experiment-design.md](guidebook/vol-04-experiment-design.md) — 공부용 (Korean): the apparatus that turns the claim into numbers — the floor-and-ceiling normalisation that makes a miss rate and a makespan comparable, holding the executor fixed and swapping only the recognizer, the eight conditions — the two name-table conditions among them — and what each isolates, the two measurement layers, what is counted and which four aggregates are actually scored, how a file's score is composed, the eight guards checked apart from any score, what the workloads must contain and the information asymmetry that defines them, why the simulator draws nothing at run time, and what is committed to a file before any result is seen
- [guidebook/vol-05-shared-vocabulary.md](guidebook/vol-05-shared-vocabulary.md) — 공부용 (Korean): the vocabulary's actual content — the one list four places read and why there is no mapping layer between them, the shape of one recognizer answer and which block is the contract, the sixteen modes with the chain from label to segment to scenario catalogue to cited source, the boundaries between neighbouring names and how the dataset drew them, the single attribute with its vacuous-true rule and its batch-mode reading, the ground-truth-only labels and what each does in grading, the admission test applied to real candidates including one that passed and was still rejected, four scenarios labelled by hand, and what freezing a vocabulary means with every change since ratification
- [guidebook/vol-06-archetypes-and-grounding.md](guidebook/vol-06-archetypes-and-grounding.md) — 공부용 (Korean): where the archetype numbers come from — a process as the scheduler sees it and what an archetype may not contain, the six primitives and why periodic work uses TIMER, the three-step definition and every schema field including the distribution language, the four grades of evidence, the twelve entries of the 2026-09-13 library (the current 29-entry library is the dataset guidebook's vol 2), existence closed by harvesting and sufficiency closed only by verification, counts as numbers, what meas-ci measured and how it corrected a model, `compiler-child` followed from source sentence to sampled event stream, and every weak spot gathered in one place. Each source sentence is quoted from the primary text with the copy and access date given in place; where the primary text disagrees with the repository's description of it, the volume follows the primary text and marks the gap rather than correcting the repository

## Dataset guidebook (`guidebook/dataset/`)

Eight volumes on the workload dataset alone, end to end, in Korean with English terms, for a reader new to operating systems: every decision with its recorded reason, every count checked against the tree when written (2026-10-14), and in the docs-correction task (9.15) each volume's corrections checked against the 2026-10-17 tree. Index and reading order: [guidebook/dataset/README.md](guidebook/dataset/README.md).

- [guidebook/dataset/01-the-big-picture.md](guidebook/dataset/01-the-big-picture.md) — 공부용 (Korean): what the dataset is for, the three layers, the tree and pipeline, the sets at a glance, where the numbers come from, how the consumers read it
- [guidebook/dataset/02-the-archetype-library.md](guidebook/dataset/02-the-archetype-library.md) — 공부용 (Korean): the 29 entries of `archetypes.yaml`, each field, each slice's entries with their measured values and decisions, the library's past and its stated limits
- [guidebook/dataset/03-timeline-to-canonical-workload.md](guidebook/dataset/03-timeline-to-canonical-workload.md) — 공부용 (Korean): the timeline and canonical formats field by field, the compiler traced by hand, seeds and determinism, demand, lints, the format's history
- [guidebook/dataset/04-the-coreset.md](guidebook/dataset/04-the-coreset.md) — 공부용 (Korean): the 32 cells, the seven groups, every one of the 51 files, the C7 derivation, the 78 variants, the coverage grid, 24 → 51
- [guidebook/dataset/05-the-generated-layer.md](guidebook/dataset/05-the-generated-layer.md) — 공부용 (Korean): why a generated layer, `grids.yaml` and the generator, the five sets cell by cell, the manifests' grid records, how a generated file is scored
- [guidebook/dataset/06-grounding-measurement-verification.md](guidebook/dataset/06-grounding-measurement-verification.md) — 공부용 (Korean): citations and tags, the verification standard, the `meas-ci` campaigns and the stability rule, the 2026-09-13 findings, the audits, the slices as research
- [guidebook/dataset/07-build-gate-manifests-ci-tests.md](guidebook/dataset/07-build-gate-manifests-ci-tests.md) — 공부용 (Korean): the seven manifests, blessing and pins, `make check` and the `--check` flags with worked failures, the `make` targets, CI and the runner, the test suites
- [guidebook/dataset/08-decision-chronicle.md](guidebook/dataset/08-decision-chronicle.md) — 공부용 (Korean): the decisions from the 2026-08-23 design meeting to 9.23 with their recorded reasons, the reversals, what is open

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
- [daemon/prior-table-pair-review.md](daemon/prior-table-pair-review.md) — the pre-execution check on the prior driver table: thirty-five written judgements (16 same-mode pairs, 3 C2 row-pairs, 16 C7 pairs) naming the knob, the scored term it moves, and the direction; its findings

## Workload (`workload/`)

How the dataset was designed and grounded. Reading order: building-plan → archetype-plan → interpretation-contract → the citation recipe in references.md. Developer README: `dataset/README.md`; machine registry: `dataset/sources.yaml`; release map (each measurement campaign's releases and their assets' hashes): `dataset/meas-releases.yaml`; the measurement tooling's map: `dataset/tools/meas/README.md`; licences: `LICENSE` (the code, MIT) and `dataset/LICENSE` (the dataset's data, CC-BY-NC-SA-4.0).

- [workload/building-plan.md](workload/building-plan.md) — how the dataset is built: the core set and the generated layer, compiled in one lane-scaled mode (`single`), the naturalistic set in the backlog; build order
- [workload/archetype-plan.md](workload/archetype-plan.md) — how one kind of program is specified and grounded, and the library's 29-entry inventory
- [workload/measurement-overview.md](workload/measurement-overview.md) — how the measured archetypes' values are obtained: what each job runs and why, the stability rule and its exceptions, the checks, the literature, what the values claim
- [workload/scenario-catalog.md](workload/scenario-catalog.md) — the scenarios (S1–S18) and the process names the dataset's files bind, each grounded for its existence only
- [workload/grounding-sources.md](workload/grounding-sources.md) — which source may justify which kind of claim (roles A–D)
- [workload/source-vetting.md](workload/source-vetting.md) — per-source verdicts and extracted numbers
- [workload/coreset-guide.md](workload/coreset-guide.md) — 공부용 (Korean): the three layers, the 29 archetypes, how compile works, and all 51 core-set files with their compiled numbers

## Harness (`harness/`)

The experiment harness: trace → records → scores. Reading order: background-guide → harness-and-records-guide → metrics → data-contracts (trace, recognition log).

- [harness/metrics.md](harness/metrics.md) — every number the project reports: the primitives computed from traces and recognition logs, the records format, the aggregate list, normalisation and floors, the constants and their sources, the simulator assumptions
- [harness/harness-and-records-guide.md](harness/harness-and-records-guide.md) — 공부용 (Korean): what the harness reads and writes, every primitive with worked examples, three mock traces computed by hand, and the upper half — scores, guards, the Layer-1 grader, the mocks and the invocation contract, the per-experiment spec and the RQ0 gate evaluator, the runner. Each folder under `harness/` also has its own README

## Memos (`memos/`)

Point-in-time notes. A memo's text is never rewritten: a later fact is appended as a dated correction, and the line under its status header says whether it is open — its ask and its owner — or closed, with where its content now lives.

### Open

- [memos/2026-09-07-trace-clarifications-for-the-simulator.md](memos/2026-09-07-trace-clarifications-for-the-simulator.md) — to 인경민: the `ready`-line rule, the §9 positions the harness assumes, frame latency for the chain, the workload's end. Open: §8 item 1 in one case, a FORK that takes a free slot, which writes no zero-wait `ready(cause = fork_slot)` line yet; owner 인경민. The rest of item 1, a `ready` line at every completion of a blocking primitive, at zero wait when it did not block (the RQ0 gate spec's simulator-conformance item (a)), is in the simulator since its stage X (2026-10-23)
- [memos/2026-09-07-repeat-samples-for-the-daemon.md](memos/2026-09-07-repeat-samples-for-the-daemon.md) — to 박이안: the repeat index run-to-run consistency needs from the recognition log. Open: §3's repeat index in the recognition log, which carries none yet; owner 박이안
- [memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md](memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md) — to 인경민: what happens to the task queue, the running task, and scheduler state when a config with a different algorithm lands mid-run, and how the MLFQ re-learning overhead is measured. Open: three of §6's simulator items — `x_mlfq_level` with levels on every demotion and boost, the settled rules in the simulator's semantics notes, the test that remaining demand is conserved across a switch; owner 인경민
- [memos/2026-09-09-batch-class-rule-for-the-simulator.md](memos/2026-09-09-batch-class-rule-for-the-simulator.md) — to 인경민: which tasks `batch_bandwidth_cap` applies to — the behavioural rule (one full slice since the last voluntary block; the periodic class never), worked task by task, and why a wrong rule flips the gaming rows. Open: §7 items 5 and 6, the semantics notes and the two unit tests; owner 인경민. §7 item 3, the cap (conformance item (d)), is in the simulator since stage V (2026-10-20)
- [memos/2026-09-11-invocation-contract.md](memos/2026-09-11-invocation-contract.md) — to 인경민, 박이안 (Korean): the invocation contract (data-contracts §11, contract 10) — the command line the harness starts the daemon and the simulator with, its flags and rules, and what each program must do to be run by the harness unchanged. Open: both programs run in that command shape — the daemon skeleton (`daemon/daemon.py`, 2026-10-21) takes the command's flags; the simulator takes `--workload`, `--schedule` and `--out-trace` and writes the trace to that file since 2026-10-28, but its trace header's `sim` is still the fixed string `src/sim`, not the version string the runner's machine configuration names; the simulator's side is owed before the RQ0 run (the RQ0 gate spec's simulator-conformance item (h)); owners 인경민 (simulator), 박이안 (daemon)
- [memos/2026-09-12-rq0-pre-registration.md](memos/2026-09-12-rq0-pre-registration.md) — to 인경민, 박이안 (Korean): the RQ0 gate spec is committed — what it fixes (K, g, N, the judging set, the boot-default sweep), the three executor rules committed as assumptions pending 인경민, the `random` reading and N pending 박이안, and what each owner must confirm before Phase 9. Open: §5's ask, the `random` reading and N = 100 confirmed on the daemon's side (the RQ0 gate spec's statement `random-reading`); owner 박이안
- [memos/2026-09-20-dataset-validity-review.md](memos/2026-09-20-dataset-validity-review.md) — the workload dataset read against what the two research claims need from it: the recognizer reads identity so the compile path carries the recognition claim while the campaign carries the benefit claim, what the stability rule establishes and what it does not, the stability ledger to publish, the demand window to state as a scoping decision, the bound the measurement venue puts on the benefit claim, and segment composition as the untouched axis. Closed: §3's stability ledger is in the measurement overview §7
- [memos/2026-10-08-declared-scheduling-class.md](memos/2026-10-08-declared-scheduling-class.md) — to 인경민, 박이안: the declared scheduling class — the workload field (policy, not nice; the entry's, never the task name's), the executor's strict idle rule under all four algorithms, the visible-projection question, and the contract change to agree. Open: §4 item 4, the formal reply the RQ0 gate spec's statement `executor-assumptions` asks for; owner 인경민. §4 item 1, the idle rule in the executor (conformance item (e)), is in the simulator since stage Z (2026-10-28)
- [memos/2026-10-17-workload-dataset-rebuild.md](memos/2026-10-17-workload-dataset-rebuild.md) — to 인경민, 박이안 (Korean): Phase 9's report of what the workload dataset rebuild added, changed and removed, each with its background, a before/after example and its impact — the rebuilt library and file sets, the declared class, the focus in the telemetry, the generated layer, no program running out, the config entries' drain and index order, the wider `render` gloss — with what each owner is asked, the answers to 인경민's questions, two proposals for the three owners, the memos still open, and the licences. Open: the simulator-conformance items (g), (h) before the RQ0 run with agreement to (g), and the regression check and EDF re-measurement on the rebuilt set (owner 인경민) — the loader's WAKE to a spawned child (stage W), (a), (b), (d) and (e) are in the simulator; the formatted prompt and the chat template's date in the recognition log (owner 박이안); the two proposals (owners 인경민, 박이안)
- [memos/2026-10-20-batch-class-and-cap.md](memos/2026-10-20-batch-class-and-cap.md) — to 인경민 (Korean): the batch class on one page — what it is, why the cap needs it, rules B1 and B2 and the declared idle rule, how they read on the rebuilt core set — and `batch_bandwidth_cap`: a work-conserving ceiling with no minimum, LOTTERY's `batch_share` equal to it, and how the prior driver table sets each row's value (the schema floor for unwanted rows, the batch term's share of the scoring weight for wanted rows, 0.5 where no batch term exists), with what those values rest on, and the concern that they are design — nine judging files on the cap-0.05 MLFQ rows — answered by a cap band line planned for the RQ0 gate spec. Closed 2026-10-21: the cap applied to the batch class (conformance item (d)) in the simulator's stage V, its accounting window 인경민's decision D10, a token bucket

### Closed

- [memos/2026-09-10-coreset-before-and-after-phase-7.md](memos/2026-09-10-coreset-before-and-after-phase-7.md) — to 인경민, 박이안 (Korean): the 2026-09-10 coreset change and why — 24 → 50 files, all 32 driver-table cells paired, C1 at sixteen, the new C7 group, pre-committed misses, the two EDF pairs the cap cannot reach, what stays the same for the simulator and the daemon. Closed: the current core set is in the coreset guide and `dataset/README.md`, the judging set in the RQ0 gate spec
- [memos/2026-09-11-boot-default-from-ostep.md](memos/2026-09-11-boot-default-from-ostep.md) — to 인경민, 박이안 (Korean): the boot default re-sourced whole from OSTEP's MLFQ example (slice 2 ms → 10 ms; EDF and LOTTERY slices follow by the same-granularity rule), the research that found no standard MLFQ configuration, what changes and what stays for each owner, two executor-rule questions for 인경민 that decide `c7-meeting` and `c7-media`. Closed: the values and their sources are in recognition-vocabulary §2 and `harness/boot-defaults/`, the sweep in the RQ0 gate spec; the formal reply to questions 1 and 2 is the declared-class memo's §4 item 4
- [memos/2026-09-13-critical-findings.md](memos/2026-09-13-critical-findings.md) — the archetype sources read against their primary texts: the 2,430-process workload is a DynamoRio build, the 16.7 ms frame budget is absent from the LAVD slides, Roeser's fluent value is a log-scale location, Coetzee's short-lived processes are `cp`/`mkdir`, `ananicy-rules` types are prescriptions; plus declared-but-unrealised archetype params, a placeholder spread under a measurement tag, the 16-vs-8 concurrency unit, sampling granularity, and stale prose after the measurement fold-in. Closed: what each finding changed is in the dataset guidebook's vol 6, the current values and grounds in `dataset/archetypes.yaml`, `dataset/sources.yaml` and references.md
- [memos/2026-09-13-dataset-rebuild-heads-up.md](memos/2026-09-13-dataset-rebuild-heads-up.md) — to 인경민, 박이안 (Korean): heads-up on the workload dataset rebuild — the findings in brief, what changes (dataset, the decisions built on it, citations outside it), what stays (the programs' input and output formats), what it means for each owner, and three executor questions to 인경민: LOTTERY's split when an editor's burst tail is batch-class, the EDF class of chain stages, a keystroke arriving while the editor runs. Closed: the format changes are in data-contracts §14, the rebuilt dataset in `dataset/README.md`; the three questions are answered
- [memos/2026-10-07-timer-skip-rule-for-the-simulator.md](memos/2026-10-07-timer-skip-rule-for-the-simulator.md) — to 인경민: TIMER skips missed ticks on its grid — the rule, a worked example against backlog, the trace lines it emits, and what the simulator and the contract change. Closed: the skip rule is in the simulator since its stage Y (2026-10-23; conformance item (b)), with the zero-wait `ready` line since stage X (item (a)); the rule is in the interpretation contract's TIMER row, ratified in §6's wording, and the simulator guide §4, the harness's reading in metrics §6.2

## Full index

| doc | answers | status |
|---|---|---|
| [research-proposal.md](research-proposal.md) | what the project is, the system design, the experiment | draft |
| [research-claims.md](research-claims.md) | what we claim and what would falsify it | normative |
| [related-work.md](related-work.md) | how we position against prior work | draft |
| [references.md](references.md) | what we cite, in what form, for what claim — and the id-minting rule | normative |
| [terminology.md](terminology.md) | what our words mean | normative |
| [background-guide.md](background-guide.md) | self-contained onboarding for both builders | normative |
| [data-contracts.md](data-contracts.md) | every data format in the project, with explained examples | normative |
| [recognition-vocabulary.md](recognition-vocabulary.md) | the shared vocabulary and the frozen config schema | normative |
| [simulator/simulator-guide.md](simulator/simulator-guide.md) | what the simulator must do; what's the builder's to decide | normative |
| [simulator/interpretation-contract.md](simulator/interpretation-contract.md) | how a canonical workload becomes scheduled tasks | normative |
| [daemon/daemon-guide.md](daemon/daemon-guide.md) | what the daemon must do; what's the builder's to decide | normative |
| [daemon/prior-table-pair-review.md](daemon/prior-table-pair-review.md) | pair review of the prior driver table: knob, scored term, direction per pair; findings | record |
| [workload/building-plan.md](workload/building-plan.md) | how the dataset is built | normative |
| [workload/archetype-plan.md](workload/archetype-plan.md) | how one kind of program is specified and grounded, and the library's 29-entry inventory | normative |
| [workload/measurement-overview.md](workload/measurement-overview.md) | how the measured archetypes' values are obtained, when their repeats stop, and what they claim | draft |
| [workload/scenario-catalog.md](workload/scenario-catalog.md) | which scenarios and process names the dataset uses, each grounded for its existence | normative |
| [workload/grounding-sources.md](workload/grounding-sources.md) | which source may justify which claim | normative |
| [workload/source-vetting.md](workload/source-vetting.md) | per-source verdicts and extracted numbers | record |
| [guidebook/README.md](guidebook/README.md) | 공부용: the research guidebook's volume list with each volume's state, and its in-text devices | — |
| [guidebook/vol-01-systems-and-scheduling.md](guidebook/vol-01-systems-and-scheduling.md) | 공부용: everything about scheduling needed before the research, from zero OS background | complete |
| [guidebook/vol-02-related-work.md](guidebook/vol-02-related-work.md) | 공부용: the four lines of prior work, what each achieved and where it stopped, and the empty quadrant | complete |
| [guidebook/vol-03-the-research.md](guidebook/vol-03-the-research.md) | 공부용: the gap, the recognition layer as an architecture, the claim's seven links (link 1–link 7), the research questions, and what would falsify it | complete |
| [guidebook/vol-04-experiment-design.md](guidebook/vol-04-experiment-design.md) | 공부용: the apparatus that produces the numbers — conditions, layers, scoring, guards, determinism, pre-registration | draft |
| [guidebook/vol-05-shared-vocabulary.md](guidebook/vol-05-shared-vocabulary.md) | 공부용: the shared vocabulary's content — the sixteen modes and where they came from, the boundaries between them, the one attribute, the ground-truth-only labels, the admission test applied, and what freezing it means | complete |
| [guidebook/vol-06-archetypes-and-grounding.md](guidebook/vol-06-archetypes-and-grounding.md) | 공부용: the archetype library's content and grounding — primitives, schema, evidence grades, the twelve entries of the 2026-09-13 library (the current one is the dataset guidebook's vol 2), harvesting and verification, counts, measurement, one entry traced end to end, and the weak spots | complete |
| [workload/coreset-guide.md](workload/coreset-guide.md) | 공부용: every coreset file explained, with compiled numbers | draft |
| [harness/metrics.md](harness/metrics.md) | primitives, records, aggregates, normalisation, constants — every reported number's definition | normative |
| [harness/harness-and-records-guide.md](harness/harness-and-records-guide.md) | 공부용: harness, records, primitives, mocks by hand, scores, guards, grader, mocks, evaluator, runner | draft |
| [memos/2026-09-07-trace-clarifications-for-the-simulator.md](memos/2026-09-07-trace-clarifications-for-the-simulator.md) | to 인경민: what the harness needs from the trace, and why | memo (open) |
| [memos/2026-09-07-repeat-samples-for-the-daemon.md](memos/2026-09-07-repeat-samples-for-the-daemon.md) | to 박이안: the repeat index consistency needs from the log | memo (open) |
| [memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md](memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md) | to 인경민: queue takeover, preemption, and measuring overhead at an algorithm switch | memo (open) |
| [memos/2026-09-09-batch-class-rule-for-the-simulator.md](memos/2026-09-09-batch-class-rule-for-the-simulator.md) | to 인경민: the batch-class rule the cap applies to, with worked examples and an action plan | memo (open) |
| [memos/2026-09-11-invocation-contract.md](memos/2026-09-11-invocation-contract.md) | to 인경민, 박이안 (Korean): the command line the harness invokes the daemon and the simulator with — flags, rules, exit code | memo (open) |
| [memos/2026-09-12-rq0-pre-registration.md](memos/2026-09-12-rq0-pre-registration.md) | to 인경민, 박이안 (Korean): the RQ0 gate spec committed — what is fixed, what each owner confirms before Phase 9 | memo (open) |
| [memos/2026-09-20-dataset-validity-review.md](memos/2026-09-20-dataset-validity-review.md) | what the dataset's grounding and measurement establish for each research claim, and the four things to carry into the paper | memo (closed) |
| [memos/2026-10-07-timer-skip-rule-for-the-simulator.md](memos/2026-10-07-timer-skip-rule-for-the-simulator.md) | to 인경민: the TIMER skip rule that replaces backlog, and what the simulator, the trace and the contract change | memo (closed) |
| [memos/2026-10-08-declared-scheduling-class.md](memos/2026-10-08-declared-scheduling-class.md) | to 인경민, 박이안: the declared-class field, the executor's idle rule, and the frozen-contract change they need | memo (open) |
| [memos/2026-10-17-workload-dataset-rebuild.md](memos/2026-10-17-workload-dataset-rebuild.md) | to 인경민, 박이안 (Korean): what the workload dataset rebuild changed, what each owner is asked, two proposals, the open memos, the licences | memo (open) |
| [memos/2026-10-20-batch-class-and-cap.md](memos/2026-10-20-batch-class-and-cap.md) | to 인경민 (Korean): what the batch class is, how the prior driver table sets each row's cap, and the concern that those values are design | memo (open) |
| [memos/2026-09-10-coreset-before-and-after-phase-7.md](memos/2026-09-10-coreset-before-and-after-phase-7.md) | to 인경민, 박이안 (Korean): the coreset before and after the 2026-09-10 change — what changed, why, and what it means for each owner | memo (closed) |
| [memos/2026-09-11-boot-default-from-ostep.md](memos/2026-09-11-boot-default-from-ostep.md) | to 인경민, 박이안 (Korean): the boot default from OSTEP — what changed, why, what it means for each owner, two rule questions for the simulator | memo (closed) |
| [memos/2026-09-13-critical-findings.md](memos/2026-09-13-critical-findings.md) | what the archetype sources' primary texts contradict in the repository's citations, and the dataset/tooling gaps found alongside | memo (closed) |
| [memos/2026-09-13-dataset-rebuild-heads-up.md](memos/2026-09-13-dataset-rebuild-heads-up.md) | to 인경민, 박이안 (Korean): the dataset rebuild ahead — what changes, what stays, three executor questions | memo (closed) |
| [guidebook/dataset/README.md](guidebook/dataset/README.md) | 공부용: the dataset guidebook's index, reading order and conventions | draft |
| [guidebook/dataset/01-the-big-picture.md](guidebook/dataset/01-the-big-picture.md) | 공부용: what the dataset is, its three layers, its tree, its sets, its consumers | draft |
| [guidebook/dataset/02-the-archetype-library.md](guidebook/dataset/02-the-archetype-library.md) | 공부용: the 29 archetype entries, their fields, values, decisions and limits | draft |
| [guidebook/dataset/03-timeline-to-canonical-workload.md](guidebook/dataset/03-timeline-to-canonical-workload.md) | 공부용: the two formats and the compiler, traced by hand | draft |
| [guidebook/dataset/04-the-coreset.md](guidebook/dataset/04-the-coreset.md) | 공부용: every core-set file, the variants, the coverage grid, the set's history | draft |
| [guidebook/dataset/05-the-generated-layer.md](guidebook/dataset/05-the-generated-layer.md) | 공부용: the generated layer's definition, generator, five sets, manifests and scoring | draft |
| [guidebook/dataset/06-grounding-measurement-verification.md](guidebook/dataset/06-grounding-measurement-verification.md) | 공부용: grounding, the measurement campaigns, the verification standard, the findings and audits | draft |
| [guidebook/dataset/07-build-gate-manifests-ci-tests.md](guidebook/dataset/07-build-gate-manifests-ci-tests.md) | 공부용: manifests, pins, the gate, make targets, CI, tests | draft |
| [guidebook/dataset/08-decision-chronicle.md](guidebook/dataset/08-decision-chronicle.md) | 공부용: the dataset's decisions in date order, reversals, open items | draft |
