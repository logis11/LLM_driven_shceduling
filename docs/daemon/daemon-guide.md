# Daemon Guide — what to build, what's fixed, what's yours
> Status: draft · Created 2026-08-28 · Updated 2026-08-28

The second half of the daemon builder's onboarding (read `../background-guide.md` first — this one assumes it). It's a spec, but a deliberately breathing one: the **contract surface** (inputs, the two outputs, the information rules, determinism) is fixed and stated here in full; the **inside of the machine** (language details, prompt engineering, code layout, model hosting choices) is yours. Fixed things say "must." Everything else is a suggestion you may overrule in your own tree.

---

## 1. The machine at a glance

```text
   visible projection                    ground_truth
   (names, counts, pinned times)         (oracle recognizer ONLY)
            │                                  │
            ▼                                  │
   ┌─────────────────────────────────────┐     │
   │  telemetry builder                  │     │
   │  walk pinned events → snapshots     │     │
   └───────────────┬─────────────────────┘     │
                   ▼   one snapshot per set change (query point)
   ┌─────────────────────────────────────┐     │
   │  recognizer  (pluggable — one per   │◀────┘
   │  condition: fixed / random /        │
   │  whitelist / llm_* / oracle)        │──▶ proposal (LLM conditions)
   └───────────────┬─────────────────────┘
                   ▼
   ┌─────────────────────────────────────┐
   │  validator                          │  closed vocabulary, bounds,
   │  reject / clamp / hold / fallback   │  provenance stamping
   └───────────────┬─────────────────────┘
                   ▼
   ┌─────────────────────────────────────┐
   │  driver table / config mapper       │  (mode, attributes) → config;
   │  + latency stamping                 │  variants A/B/C differ here
   └───────┬───────────────────┬─────────┘
           ▼                   ▼
   config schedule      recognition log
   (→ simulator)        (→ harness/grader)
```

The daemon is an **offline batch program**: for one workload and one experimental condition, it reads the workload's visible projection, replays the pinned set changes, consults its recognizer at each one, and writes two files. It never talks to the simulator — the config schedule is the only thing that crosses that boundary, as a file. Run it over all 24 workloads × all conditions and the entire recognition side of the experiment is done before a single simulation starts.

The deep design idea to hold onto: **every experimental condition is just a different recognizer plugged into this same machine.** The oracle, the random draw, the whitelist, and the LLM all flow through the same telemetry builder, the same validator, the same driver table, the same two output files. That's what makes the comparison between them fair — and it means the whole machine can be built and fully tested before any LLM is involved at all.

## 2. The non-negotiables

1. **Input is the visible projection only.** Names, counts, and pinned lifetimes — never the run file, never programs or burst durations, never `ground_truth`. The single exception is the **oracle recognizer**, whose entire job is to read `ground_truth`; isolate it so that no other recognizer could ever touch that path (a separate module the others can't import beats a shared flag).
2. **Query points are pinned events only.** The set of live names changes at arrivals and pinned departs, walked from the projection. Consequences, accepted deliberately: a finite task never *disappears* from telemetry (the recognizer reacts to launches and user-closes, not to background jobs finishing), and spawn children appear with their parent. No recognizer is consulted between query points — an unchanged set means an unchanged answer.
3. **Two outputs, same format from every condition.** A **config schedule** (for the simulator) and a **recognition log** (for the grader) — exact shapes in `../data-contracts.md`. A condition that can't fill the recognition log honestly (what was I shown, what did I answer, how long did I take) isn't done.
4. **Every schedule starts with a default entry at t = 0.** Plain MLFQ with the agreed default parameters — no recognition has happened yet at boot, and its provenance says `fallback`.
5. **Closed vocabulary, enforced in code.** A proposal with an unknown mode, attribute, or subsystem key is rejected (→ the previous config is `held`), never patched or guessed at. The validator's menu is data the three of us freeze — not something the prompt or the model can extend.
6. **Latency is part of the answer.** Each schedule entry takes effect at *query-point time + recognition latency* for that query. The oracle stamps zero delay; the LLM stamps what inference actually took (with reasoning tokens included). Faking a small latency would fake a headline result (RQ4), so latency handling deserves the same care as correctness.
7. **Deterministic reruns.** Given the same inputs, the daemon reproduces its outputs: `random` draws from a seeded PRNG whose seed is recorded in the log; LLM conditions replay from the record/replay cache (§6). "The model felt different today" must never be able to change a committed result.

## 3. The input, field by field

The visible projection, one file per workload. From `c1-compile`:

```jsonc
{ "workload_id": "c1-compile",
  "tasks": [
    { "name": "code", "t_arrive": 0, "t_depart": 60000000 },
    { "name": "make", "t_arrive": 2000000,
      "children": [ { "name": "cc1", "count": 100 } ] }
  ] }
```

In sentences: a process named `code` exists from 0 to 60 s — its depart is pinned (the user closes it), so the projection may know it. A process named `make` appears at 2 s with no known end: it's a finite task, its exit time is a scheduling outcome, so the projection *cannot* contain it — treat it as present to the end. Its `children` list is compile-time knowledge carried over from the workload's spawn table: one hundred processes named `cc1` will exist during the build, so they are visible for the parent's lifetime, without individual times. Counts are real signal — `chrome × 13` reads as a browser with tabs, `cc1 × 100` as a parallel build, `game.exe × 300` as a game engine's process swarm — and duplicates are the normal state of the data, not an anomaly.

Walking those pinned times produces the telemetry sequence — for `c1-compile`, exactly two snapshots:

```jsonc
{ "t_us": 0,       "processes": [ { "name": "code", "count": 1 } ] }
{ "t_us": 2000000, "processes": [ { "name": "code", "count": 1 },
                                  { "name": "make", "count": 1 },
                                  { "name": "cc1",  "count": 100 } ] }
```

Each snapshot is one query point: the recognizer is shown it and must answer. What the recognizer is *never* shown, because the projection doesn't contain it: PIDs, CPU or burst statistics, command lines or paths (canonical files carry bare names only — a frozen dataset decision), and labels. When results look ambiguous there will be a real temptation to "give the model a bit more context"; the frozen projection is what turns that from a silent experiment-invalidating tweak into a visible protocol change everyone signs off on.

## 4. The recognizer seat

Like the simulator's scheduler, the recognizer sits behind a narrow interface — *swapping it is the experiment*. One implementation per condition:

| Condition | What its recognizer does at a query point | Needs |
|---|---|---|
| `fixed` | nothing — the schedule stays at the default entry forever | — |
| `random` | draws a uniformly random `(mode, attributes)` | a seeded PRNG |
| `whitelist` | matches snapshot names against a hardcoded rule list — a faithful reproduction of what Game Mode does | your rule table |
| `llm_vocab` (A) | asks the model; **only its `system` block is used**, the driver table picks the config | prompt + model |
| `llm_algo` (B) | as A, plus the model's `algorithm` choice is honored; params still from the table | prompt + model |
| `llm_full` (C) | the model's whole `cpu_scheduler` block is used (post-validation) | prompt + model |
| `oracle` | reads the true `(mode, attributes)` for this instant from `ground_truth` | the answer key |

Downstream of the recognizer, everything is shared. The **validator** checks the answer against the closed vocabulary and per-algorithm bounds, and stamps what it did: `unmodified`, `clamped`, `held` (answer rejected — previous config carries forward), or `fallback`. The **driver table** is the fixed mapping `(mode, attributes) → config` — for variants A and the baselines it *is* the policy, which is why its contents are a three-person decision and effectively the executor's behavior specification. Then the config is stamped with the query's latency and appended to the schedule, and the whole exchange (snapshot, proposal, validation outcome, latency) is appended to the recognition log.

The prompt side of the LLM conditions — how to phrase telemetry, how to demand the `reasoning`-first structure, how to get schema-valid JSON out of a model — is entirely yours, and iterating on it is expected to be a daily activity. Two structural rules only: the model must produce its `reasoning` *before* its conclusions (it measurably improves the conclusions, and failure analysis depends on it), and whatever output-forcing tricks you use (JSON mode, constrained decoding), the validator still checks everything — belt and suspenders.

## 5. The outputs

Both are specified with examples in `../data-contracts.md`; in brief, per workload × condition:

- **Config schedule** — `{workload_id, condition, schedule: [{t_us, config, provenance}, …]}`. This is the only thing the simulator ever sees of your work; it must stand alone.
- **Recognition log** — `{workload_id, condition, queries: [{t_set_change, telemetry, proposal, validation, latency_us}, …]}`. This is where Layer-1 grading lives (mode accuracy, confusion matrix, attribute accuracy, consistency, familiarity splits), and where `reasoning` is preserved for failure analysis. Non-LLM conditions log their thinner equivalents (which whitelist rule fired; the oracle row read; the random draw and seed) so every condition is auditable the same way.

## 6. Record and replay

Running the full experiment matrix against a live model would be slow, expensive, and non-reproducible, so the LLM path runs in two modes. In **record** mode the daemon actually queries the model — once per *distinct* telemetry snapshot — and stores `(cache key → raw response, measured latency)`. In **replay** mode it serves answers from that cache with no model in the loop, which makes every later run fast, free, and bit-reproducible. The cache key is `(workload_id, snapshot hash, prompt version)` — so one recorded cache serves every variant and every rerun, and bumping the prompt version deliberately invalidates it. Plan for two hosting setups behind one client interface: a hosted API for fast prompt iteration, and a local quantized model for the measurements that go in the paper (the deployment story isn't credible if the process list leaves the machine, and local inference on short structured outputs is fast).

## 7. Milestone 0 — definition of done

No LLM anywhere in it: **the skeleton runs end-to-end with the trivial recognizers.** Concretely:

1. Read the visible projection for one C1 workload (or its `*.workload.json`, extracting only the projection's slice) and produce the correct telemetry sequence — snapshot count and contents verifiable by hand against the timeline.
2. Run the `fixed`, `random` (seeded), and `oracle` recognizers through the full machine — validator, driver table with a first-cut mapping, latency stamping (zero for all three) — and emit valid config schedules and recognition logs for all 24 workloads.
3. Rerun and diff: outputs bit-identical.

This milestone is not a warm-up — `fixed`, `random`, and `oracle` are the exact three conditions of the **RQ0 gate**, the project's first real experiment (is the random-to-oracle gap even measurable?). Your milestone 0 plus the simulator's milestone 0 *is* that experiment's machinery. The whitelist comes next (it needs your rule table but no model), and the LLM conditions after that, once record/replay exists to keep them cheap.

## 8. Yours to decide

Entirely your call, inside `daemon/`:

- **Language.** The proposal drafts Python (LLM SDKs live there, and prompts change dozens of times a day). Your call to confirm or argue.
- Prompt design, output formatting strategy, model choice and hosting details, the whitelist's actual rules.
- Internal architecture, file layout, testing approach; your tree owns its own Makefile and (eventually) a `daemon/README.md` in the spirit of `dataset/README.md`.
- The shape of the record/replay cache on disk.

## 9. Questions the contracts don't answer (yet)

Real ambiguities you'll hit; none has a decided answer today. When you hit one, raise it — most of these are protocol-freeze material:

1. **The vocabulary gap.** The dataset's ground-truth labels are finer than the proposal's draft five modes — the coreset uses `dev`, `ml-train`, `browsing`, `office`, `indexing`, `backup` and a dozen more. Does the driver table adopt the fine vocabulary, or does grading map fine labels onto coarse modes? This decision touches all three of us and gates the driver table's contents.
2. **The driver table itself.** The `(mode, attributes) → config` entries are effectively the executor's behavior spec and an §8.2 all-three decision — the daemon needs at least a first-cut table for milestone 0.
3. **Latency for the paper.** Recorded per-query latency from record mode, a fixed constant per model, or a distribution? (Affects RQ4's cleanliness.)
4. **Hold time / hysteresis.** In a live system you'd rate-limit config changes to prevent thrash. With pinned query points the daemon *can* still emit two configs seconds apart — does a minimum-hold rule apply, and is it a daemon policy or a config-schedule property?
5. **Config schema per algorithm.** The exact field lists for MLFQ/EDF/lottery/FIFO configs — freeze alongside the config schedule, jointly with the simulator side.

---

*The binding fine print behind this guide lives in `../data-contracts.md` (all shapes and examples) and, for what the workload files themselves mean, `../simulator/interpretation-contract.md`; this guide restates what the daemon needs, but if a discrepancy ever slips in, those win — and tell 인지오, since a discrepancy is a bug in this guide.*
