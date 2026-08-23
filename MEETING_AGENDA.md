# Design Meeting — Agenda

Six decisions. Full text and diagrams in `OPEN_QUESTIONS.md`, same numbering.

Read beforehand: `OPEN_QUESTIONS.md`, module sketch section.

---

## 1 — One core, or several?          5 min

Single core, or a multi-core model with load balancing and migration.

More cores shrink the effect being measured: with slack, the scheduler has
nothing to decide.

**Lean:** build single core; design workloads whose demand exceeds one core and
state the core count as a deliberate choice.

**Blocks:** the simulator. Decide first.

---

## 2 — Are the simulator and daemon ever alive at the same time?   20 min

```text
  A  live socket, measured latency injected into virtual time
  B  daemon runs first, emits a config schedule the simulator replays
```

Both produce identical numbers. A costs a protocol, async handling and failure
paths. B costs a file format.

B holds only while nothing feeds scheduling outcomes back into the workload.

**Lean:** B.

**Blocks:** the contract boundary and IPC work.

---

## 3 — What happens when a config lands mid-run?    10 min

Two independent halves: when the switch happens, and what carries across it.

**Lean:** drain to a slice boundary, then start the new algorithm cold. Only
MLFQ loses state, and it rebuilds within a few slices.

**Also decide:** log at both `t_return` and `t_apply`, so held and fallback
proposals stay visible in the trace.

---

## 4 — How is the driver table built?     25 min

The table cannot be tuned on the workloads the results are reported on, and no
tuned table can exist before the Phase 1 gate.

```text
  1  v0 written from theory
  2  Phase 1 gate runs on v0
  3  throwaway tuning workloads, placeholder names, ~3 per row
  4  search each row against those -> v1
  5  freeze v1, run the matrix on the evaluation workloads
```

**Decide:** whether to build twice, who writes the tuning pool, and how many
rows are actually reachable.

**Blocks:** Phase 2. Nothing can be tuned until this is settled.

---

## 5 — The ladder needs two ceilings      15 min

Sections 5.2 and 7 of the proposal use "oracle" for two different machines:
perfect recognition, and a search over configurations.

Variants A and B are bounded by the first. Variant C is bounded by the second.

**Decide:** whether both enter the paper, and reconcile the two uses of the
word.

---

## 6 — Grading across heterogeneous workloads    10 min

Each workload has a different primary metric, so raw values cannot be averaged.

**Proposal:** demote variant C to a subset diagnostic, grade everything against
perfect recognition, and split each condition's shortfall into
recognition-attributable and table-attributable.

---

## Not on this agenda

Section 8.2 lists six decisions requiring all three of us. These six are
separate from them and do not replace them.

```text
  the shared vocabulary        five modes, two attributes
  the two protocol schemas     telemetry out, proposal in
  the driver table's contents  twenty rows
  metric definitions
  workload scenarios           domain and familiarity balance
  what the model may see
```

Item 4 above decides how the table is built. Its contents remain a section 8.2
decision.
