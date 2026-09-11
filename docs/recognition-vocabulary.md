# Recognition Vocabulary
> Status: normative · Created 2026-08-28 · Updated 2026-09-11

The shared vocabulary of the recognition signal — the one contract that the recognizer's output schema, the validator's menu, the driver table, and the Layer-1 grader all agree on. Ratified 2026-08-28 (인지오 · 인경민 · 박이안 — pending team review of this doc).

A recognizer's answer has two blocks, and this doc is organized around that division:

- **`system`** — the claim about the world: what the machine is being used for. Subsystem-neutral; every consumer reads it. Its vocabulary (modes + attributes) is identical to the dataset's ground-truth labels, so recognizer answers and ground truth are compared directly, with no mapping layer.
- **`subsystems`** — per-consumer configuration suggestions, one key per consumer. This project fills exactly one key, `cpu_scheduler`; its schema is the configuration language of the CPU driver.

These labels were not invented for this doc — they come out of the dataset itself. Every mode below appears as a segment label in the released coreset, and each labeled segment carries `scenario` tags keying it to the scenario catalog (`workload/scenario-catalog.md`), whose co-occurrence patterns are grounded in cited sources — desktop-usage taxonomies, workload-benchmark suites, and our own CI measurements — resolvable through `references.md`. The same holds for `background_wanted`: it is the intent axis the C2 pair files were authored around. Adopting the dataset's labels as the vocabulary therefore means every term the recognizer can answer is backed by the citations that justified authoring a workload for it.

---

## 1. The `system` block

### Modes

A **mode** is the label for what the machine is primarily being used for during a segment. The recognizer answers exactly one mode per query, from this closed menu of 16:

| Mode | The machine is being used for |
|---|---|
| `browsing` | web browsing as the main activity |
| `office` | documents, spreadsheets, presentations |
| `mail` | reading and writing email |
| `dev` | writing code in an editor/IDE |
| `photo` | photo editing |
| `meeting` | a live video call |
| `gaming` | playing a game in the foreground |
| `media` | media playback (video, music) |
| `video-edit` | interactive video editing |
| `compile` | building software |
| `ml-train` | a machine-learning training run |
| `render` | an offline 3D/graphics render |
| `transcode` | batch media conversion |
| `indexing` | file indexing / crawling |
| `backup` | a backup job |
| `idle` | no human present; maintenance only |

**`ambiguous` — ground truth only.** Ground-truth segments may carry the label `ambiguous` (equally-active dual foregrounds — the C6 boundary case). It is not on the recognizer menu: a recognizer must always commit to one of the 16, and `ambiguous` segments are excluded from accuracy scoring and reported separately as a scope boundary.

### Attributes

One graded attribute:

- **`background_wanted`** (boolean) — *is the sustained background work something the user asked for?* `true` for work the user deliberately initiated or is waiting on (a download, a kicked-off training run, a render); `false` for work nobody asked for right now (a scheduled scan, an indexer's rescan). **Convention: when a segment has no sustained background work at all, `background_wanted` is `true`** — nothing unwanted is running — keeping the attribute a plain boolean. In the batch modes (`compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`) the batch job is itself the sustained background work the attribute judges: `false` means that job is one nobody asked for (a module rebuild after a kernel update in place of the user's build, an indexer's scheduled rescan), not that a second job runs beside it.

### Ground-truth annotations (never recognizer-facing)

Ground-truth segments may carry additional descriptive keys used for grading splits and failure analysis only: `background` (what the background work is, e.g. `download`, `av-scan`), `initiated` (`user` | `scheduled`), `dual_active`, `spoof`, `pre_committed_miss` (`true` on a segment whose label no recognizer can reach from names and behaviour — the C6 resolution-limit case and the Phase 7 same-name intent flips; the segment is excluded from accuracy and reported separately, and the coverage grid marks its cell as instanced but recognition-limited). They are not part of the recognizer's output schema, not on the validator's menu, and not graded.

---

## 2. The `subsystems` block — `cpu_scheduler` config schema (frozen 2026-08-28)

The configuration language of the CPU driver: what a scheduler configuration may say. This is the value space of the driver table, the field list the validator enforces, and the exact surface the simulator implements. (`cpu_scheduler` is the only subsystem key this project defines; a future consumer would add its own key with its own schema, without touching this one.)

### Envelope

Every configuration, regardless of algorithm:

```jsonc
{
  "algorithm": "MLFQ" | "EDF" | "LOTTERY" | "FIFO",
  "params": { /* exactly the fields defined for that algorithm */ },
  "batch_bandwidth_cap": null | 0.05–0.95
}
```

`batch_bandwidth_cap` is the ceiling on the fraction of the lane the **batch class** may consume while non-batch work is runnable; `null` means no ceiling. The idea has a shipped counterpart, a per-class CPU bandwidth ceiling (`linux-sched-bwc`, existence only); the range, the floor, and the class rule below are ours. The batch class is determined behaviorally by the executor (observed CPU-bound behavior — the same evidence MLFQ demotion uses); the classification rule is identical across algorithms, frozen in the simulator's docs, and not configurable. Starvation protection is executor-owned and has no config field: every runnable task makes progress within a bounded window regardless of what any configuration says.

### MLFQ

| field | type / range | default | meaning |
|---|---|---|---|
| `num_queues` | int, 2–8 | 3 | number of priority levels |
| `timeslice_us` | int, 500–100000 | 2000 | the top queue's time slice |
| `timeslice_growth` | number, 1–8 | 2 | level *i*'s slice = `timeslice_us · timeslice_growth^i` |
| `boost_interval_us` | int, 10000–10000000 | 100000 | everything returns to the top queue this often |

Demotion on a fully consumed slice and stay-on-block are fixed MLFQ rules, not configuration. The defaults above, with `batch_bandwidth_cap: null`, are the **boot default configuration** — every config schedule's t = 0 entry.

### EDF

| field | type / range | default | meaning |
|---|---|---|---|
| `residual_timeslice_us` | int, 500–100000 | 2000 | round-robin slice for the residual (non-deadline) class |

The deadline class is the TIMER-driven tasks, behaviorally observed; each job's deadline is its next period boundary (period-implicit). Deadline tasks run earliest-deadline-first (ties broken by a fixed executor rule); the residual class round-robins in the remaining lane time. No admission control in v1.

### LOTTERY

| field | type / range | default | meaning |
|---|---|---|---|
| `batch_share` | number, 0.01–0.90 | 0.15 | target lane fraction for the batch class; the non-batch class holds the remainder |
| `timeslice_us` | int, 500–100000 | 2000 | one draw's tenure before the next draw |

Two classes, tickets split `batch_share : (1 − batch_share)`, equal tickets per task within a class. The draw PRNG is seeded by the simulator per run (derived from the workload id) — not a config field.

### FIFO

No fields: `"params": {}`. Run in arrival order until each task blocks or exits. The cap and the executor safety net still apply.

### Provenance of the boot default

The seven default values above are the **boot default configuration** and the `fixed` condition, so they are the floor every normalised score is measured against. None was measured; each is a **stated assumption**, and this table records how far a primary source bounds it (references in `references.md`). Values were not changed by this audit.

| field | default | grounding | status |
|---|---|---|---|
| MLFQ `num_queues` | 3 | `ostep` §8.2: the worked examples use "a three-queue scheduler". Shipped tables differ (`illumos-ts`: 60 levels). | assumption, matches OSTEP's example |
| MLFQ `timeslice_us` | 2000 | `ostep` §8.5: high-priority queues get "10 or fewer milliseconds"; `linux-sched-fair`: 0.75 ms base slice, 6 ms target latency (both scaled by 1 + ilog ncpus); `ostep` §8.5 on Solaris TS: 20 ms at the highest priority. 2 ms lies inside that range; no source names it. | assumption, bounded |
| MLFQ `timeslice_growth` | 2 | `ostep` Fig. 8.6: 10 ms / 20 ms / 40 ms per queue — doubling per level. | assumption, matches OSTEP's example |
| MLFQ `boost_interval_us` | 100000 | `ostep` Fig. 8.4: a boost "every 100 ms (which is likely too small of a value, but used here for the example)"; OSTEP names S a voo-doo constant. Shipped: `illumos-ts` ages once per second; `ostep` §8.5 "around every 1 second or so". | assumption, matches OSTEP's illustrative value; flagged by OSTEP itself |
| EDF `residual_timeslice_us` | 2000 | No source. Set equal to MLFQ `timeslice_us` so the residual class round-robins at the same granularity. | assumption, tied to `timeslice_us` |
| LOTTERY `batch_share` | 0.15 | No source names a batch-class share. `waldspurger-osdi94` defines shares as proportional to tickets and gives no ratio between classes. | assumption, unbounded |
| LOTTERY `timeslice_us` | 2000 | `waldspurger-osdi94` §2: prototype quantum 10 ms ("100 lotteries per second"), with "shorter time quanta can be used to further improve accuracy". Set equal to MLFQ `timeslice_us`. | assumption, bounded |

**Sensitivity check (planned, pre-registered in the RQ0 gate spec at Phase 8).** Because the floor is assumed, the `fixed` condition is re-run under two alternative boot defaults drawn from the cited sources' own values — OSTEP's example configuration (10 ms top slice, three queues, doubling, 100 ms boost) and a Linux-like short slice (0.75 ms base) — with the exact pair fixed before execution. If the RQ0 gap's sign or the ordering of normalised scores changes across the three floors, the floor is reported as a range rather than a point.

### Validation rules

1. `algorithm` outside the four-string menu → the config is rejected (previous config stays in force, `held`).
2. `params` must contain exactly the declared fields for the chosen algorithm — missing, extra, or wrongly typed fields reject the config (`held`).
3. Out-of-range numerics are pulled to the nearest bound (`clamped`), never rejected.
4. `batch_bandwidth_cap` is `null` or clamped into 0.05–0.95.
5. Cross-field: LOTTERY's `batch_share ≤ batch_bandwidth_cap` when the cap is non-null (`batch_share` clamps down).

---

## 3. The recognizer output schema

The machine-readable core of every proposal, putting the two blocks together:

```jsonc
{
  "system": {                       // §1 — always present, every consumer reads it
    "mode": "gaming",               // exactly one of the 16
    "background_wanted": true       // boolean, always present
  },
  "subsystems": {                   // §2 — optional suggestions, per consumer
    "cpu_scheduler": {
      "algorithm": "LOTTERY",
      "params": { "batch_share": 0.15, "timeslice_us": 2000 },
      "batch_bandwidth_cap": 0.20
    }
  }
}
```

`system` is mandatory and validated against §1: an answer whose `mode` is off the menu, whose `background_wanted` is missing or non-boolean, or which carries any other key inside `system`, is rejected. `subsystems` is optional. How much of it is *used* depends on the experiment variant, and the read scope is applied **before** validation: the five rules of §2 run on the composed configuration the simulator will receive, not on the raw block (so an `llm_algo` answer carrying only `algorithm` is not rejected by rule 2). Only under `llm_full` is the raw block itself validated:

| Variant | Reads from the answer |
|---|---|
| A (`llm_vocab`) — and all non-LLM conditions | `system` only; the driver table supplies the whole configuration |
| B (`llm_algo`) | `system` + the `algorithm` field; the driver table's entry for that algorithm in the selected row, with the row's cap |
| C (`llm_full`) | `system` + the full `cpu_scheduler` block, subject to §2's validation |

(The full proposal object also carries `reasoning` and `situation` — prose for logs and failure analysis, never validated, never consumed by any driver; see `data-contracts.md`.)

## 4. Extension rule

Adding or removing a mode, promoting an annotation to a graded attribute, changing an attribute's semantics, or changing the config schema (fields, ranges, algorithms) is an all-three decision, recorded here with a changelog entry and a statement of its re-labeling, re-grading, or re-implementation impact.

---

## 5. Changelog

- **2026-09-11 — the cap's shipped counterpart (jioh).** No value changed. §2's `batch_bandwidth_cap` paragraph now points to `linux-sched-bwc` (Linux CFS bandwidth control) as the existence reference for a per-class CPU bandwidth ceiling; what the class is, the range, and the floor remain this project's.
- **2026-09-10 — batch-mode reading of `background_wanted` (jioh 7.3).** No value changed. One clarifying clause in §1: in the six batch modes the batch job is itself the background work the attribute judges, so its `false` cell is that job unwanted, the reading `c2-p1b` already used. The C7 counterparts are built on it.
- **2026-09-10 — `pre_committed_miss` annotation (jioh 7.1).** No label or schema value changed. A fifth ground-truth annotation, `pre_committed_miss: true`, marks a segment whose label cannot be reached from names and behaviour; it is what the coverage grid reads to mark a driver-table cell as instanced but recognition-limited, and what the grader will read to exclude the segment from accuracy (Phase 8). Set first by `c1-indexing` (7.2), the user-initiated reindex.
- **2026-09-07 — boot-default provenance (jioh 4.1).** No value changed. The seven config-schema defaults now carry their grounding in §2 "Provenance of the boot default": three match OSTEP's worked-example values (`num_queues`, `timeslice_growth`, `boost_interval_us`), two are bounded by shipped or published quanta (`timeslice_us`, LOTTERY `timeslice_us`), two have no source (EDF `residual_timeslice_us`, LOTTERY `batch_share`). All seven are stated assumptions; a `fixed`-under-alternative-floors sensitivity check is planned for the RQ0 gate spec. New references: `linux-sched-fair`, `illumos-ts`, `waldspurger-osdi94`; `ostep` verified at Version 1.10.

