# Daemon Guide — what to build, what's fixed, what's yours
> Status: draft · Created 2026-08-28 · Updated 2026-08-28

The second half of the daemon builder's onboarding (read `../background-guide.md` first — this one assumes it, and only it). It's a spec, but a deliberately breathing one: the **contract surface** (inputs, outputs, the information rules, determinism) is fixed and stated here in full; the **inside of the machine** (language details, prompt engineering, code layout, model hosting choices) is yours. Fixed things say "must." Everything else is a suggestion you may overrule in your own tree.

One thing to know before anything else: the daemon is built by two people. The recognition machinery — everything from reading the input to validating a recognizer's answer — is 박이안's. One piece in the middle of the pipeline, the **driver table** (explained in §5), is 인지오's to build: its input side is the ratified vocabulary contract (`../recognition-vocabulary.md`) and its output side freezes jointly with the simulator. This guide marks the boundary clearly as it goes.

---

## 1. The machine at a glance

```text
   visible projection                      ground_truth
   (names, counts, pinned times)           (oracle recognizer ONLY)
            │                                    │
            ▼                                    │
   ┌─────────────────────────────────────┐       │
   │  telemetry builder                  │       │
   │  walk pinned events → snapshots     │       │
   └───────────────┬─────────────────────┘       │
                   ▼   one snapshot per set change (query point)     ─┐
   ┌─────────────────────────────────────┐       │                    │
   │  recognizer  (pluggable — one per   │◀──────┘                    │
   │  condition: fixed / random /        │                            │  박이안
   │  whitelist / llm_* / oracle)        │──▶ proposal (LLM ones)     │
   └───────────────┬─────────────────────┘                            │
                   ▼                                                  │
   ┌─────────────────────────────────────┐                            │
   │  validator                          │                            │
   │  check the answer, record verdict   │                           ─┘
   └───────────────┬─────────────────────┘
                   ▼                                                 ─┐
   ┌─────────────────────────────────────┐                            │  인지오 builds the
   │  driver table → config mapper       │                            │  table; the mapper
   │  + latency stamping                 │                            │  wires in after
   └───────┬───────────────────┬─────────┘                           ─┘  (owner TBD)
           ▼                   ▼
   config schedule      recognition log
   (→ simulator)        (→ harness/grader)
```

The daemon is an **offline batch program**. For one workload and one experimental condition, it reads that workload's visible projection, replays the moments where the process set changes, consults its recognizer at each one, and writes files. It never talks to the simulator while anything runs — the config schedule is the only thing that crosses that boundary, and it crosses as a file, produced before the simulator ever starts. Run the daemon over all 24 workloads × all conditions, and the entire recognition side of the experiment is finished before a single simulation begins.

The deep design idea to hold onto: **every experimental condition is just a different recognizer plugged into this same machine.** The oracle, the random draw, the whitelist, and the LLM all flow through the same telemetry builder, the same validator, the same mapper, and the same two output files. That is what makes comparing them fair — nothing differs between conditions except the box in the middle. It also means the whole machine can be built and fully tested before any LLM is involved at all.

## 2. The non-negotiables

Everything in this section is contract, not preference.

1. **Input is the visible projection only.** Names, counts, and pinned lifetime times — never the run file, never task programs or burst durations, never `ground_truth`. Why so strict: the entire experiment measures whether *names alone* carry enough meaning to schedule better. If behavioral information leaks into the recognizer through any side door, a positive result becomes unpublishable, because a reviewer can no longer tell whether the model read the names or peeked at the behavior. The single exception is the **oracle recognizer**, whose entire job is to read the answer key — isolate it structurally (a separate module that other recognizers cannot even import is better than a shared code path with a flag).
2. **Query points are pinned events only.** The set of live process names changes at arrivals and at user-close times, both of which are pinned in the projection. Those changes — and only those — trigger recognizer consultations. Two consequences, accepted deliberately as scope decisions: a background job that *finishes on its own* never disappears from telemetry (the recognizer reacts to launches and to the user closing things, not to work completing), and spawned children appear together with their parent. Between query points, no recognizer is consulted: an unchanged process set means an unchanged answer, and re-asking would produce identical responses for nothing.
3. **Two outputs, same format from every condition.** A **config schedule** for the simulator and a **recognition log** for the grader — both shapes, with examples, live in `../data-contracts.md` and are summarized in §6. A condition that cannot fill the recognition log honestly ("what was I shown, what did I answer, how long did I take") is not done, no matter how good its schedule looks.
4. **Every schedule starts with a default entry at t = 0.** At the moment a machine boots, no recognition has happened yet, so the first configuration is always the agreed default (plain MLFQ with default parameters). This entry is not optional and not implicit — it is written into every schedule, so a schedule is always a complete, self-contained answer to "what settings were in force at every moment."
5. **Closed vocabulary, enforced in code.** The set of legal modes and attributes is fixed by `../recognition-vocabulary.md` — 16 modes plus the boolean `background_wanted`, nothing else — and the legal config fields freeze with the config schema (§9.4). If a recognizer's answer contains anything outside the menu — an invented mode, a misspelled attribute, an extra field — the validator rejects the whole answer, and the previous configuration simply stays in force. The model is never "helped" by patching its output into shape, because every patch would be our judgment silently substituting for the model's, which is exactly what the experiment must not do.
6. **Recognition speed is part of the answer.** An LLM takes real time to answer — hundreds of milliseconds — and during that time the *old* configuration is still what's running. So each schedule entry takes effect at *query-point time + how long that recognition actually took*. The oracle stamps zero delay (perfect recognition is defined as instant); the LLM conditions stamp their true measured inference time, with the reasoning text's tokens included, since we require the model to produce reasoning and must pay honestly for it. Faking a small latency here would directly fake one of the paper's headline results (§9.2 explains which), so latency handling deserves the same care as correctness.
7. **Deterministic reruns.** Given the same inputs, the daemon must reproduce its outputs bit-for-bit: the `random` condition draws from a seeded random-number generator whose seed is recorded in its log, and the LLM conditions replay recorded model answers from a cache (§7) rather than re-querying live. "The model felt different today" must never be able to change a committed result.

## 3. The input, explained field by field

The visible projection: one small JSON file per workload, derived from the canonical workload by stripping everything a recognizer isn't entitled to see. From `c1-compile` (a code editor plus a parallel software build):

```jsonc
{ "workload_id": "c1-compile",
  "tasks": [
    { "name": "code", "t_arrive": 0, "t_depart": 60000000 },
    { "name": "make", "t_arrive": 2000000,
      "children": [ { "name": "cc1", "count": 100 } ] }
  ] }
```

In sentences: a process named `code` (the editor) exists from time 0 to the 60-second mark — its closing time is pinned, because "the user closes the app" is scripted user behavior, so the projection is allowed to know it. A process named `make` appears at the 2-second mark with **no known end**: it's a job that ends whenever it finishes, and *when* it finishes depends on how the scheduler treats it — that's a result of the experiment, not an input — so the projection cannot contain it; treat the task as present through the end. The `children` list handles a subtlety: `make` will launch compiler worker processes as it runs. *Which* workers (a hundred processes named `cc1`) is fixed in the workload ahead of time, so they are visible here, attached to their parent's lifetime; *when* each individual worker starts and stops is emergent, so no times are given. Counts are real signal, not noise — `chrome × 13` reads as a browser with tabs open, `cc1 × 100` as a parallel build, `game.exe × 300` as a game engine's process swarm — and duplicated names are the normal state of this data, exactly as a real process list shows a dozen identical `chrome` entries.

The **telemetry builder** walks those pinned times in order and maintains the set of live names with counts. Every time the set changes, it emits one **snapshot** — and each snapshot is one **query point**, a moment the recognizer must answer. For `c1-compile` there are exactly two:

```jsonc
{ "t_us": 0,       "processes": [ { "name": "code", "count": 1 } ] }
{ "t_us": 2000000, "processes": [ { "name": "code", "count": 1 },
                                  { "name": "make", "count": 1 },
                                  { "name": "cc1",  "count": 100 } ] }
```

What a snapshot deliberately never contains — because the projection doesn't: process IDs (real PIDs get recycled between unrelated processes, and we forbid per-instance rules anyway), CPU or timing statistics (that is the hidden behavioral ground truth the experiment tests *against*), command lines or file paths (the dataset froze a names-only decision), and of course labels (that is the answer). One warning from experience with experiments like this: when results come out ambiguous, there will be a genuine temptation to "just give the model a little more context." The frozen projection is the guardrail — adding a field to it is a visible protocol change all three of us sign off on, never a quiet tweak.

## 4. The recognizer seat — 박이안's core

Like the simulator's scheduler, the recognizer sits behind a narrow interface, because *swapping it is the experiment*. One implementation per experimental condition:

| Condition | What its recognizer does at a query point | Needs |
|---|---|---|
| `fixed` | nothing — the schedule keeps its default entry forever | — |
| `random` | draws a uniformly random `(mode, attributes)` answer | a seeded PRNG |
| `whitelist` | matches snapshot names against a hand-written rule list — a faithful reproduction of what Windows/macOS Game Mode does today | your rule table |
| `llm_vocab` (A) | asks the model, but **only its situation reading is used** — the driver table picks the actual settings | prompt + model |
| `llm_algo` (B) | as A, plus the model's choice of *algorithm* is honored; parameters still come from the table | prompt + model |
| `llm_full` (C) | the model's entire suggested configuration is used, after validation | prompt + model |
| `oracle` | reads the true `(mode, attributes)` for this instant straight from the answer key | `ground_truth` |

The three LLM variants exist to answer one of the project's central questions: *how much authority does the model deserve?* Variant A trusts it only to read the situation; variant C trusts it to tune scheduler constants for a machine it has never observed. If A performs close to C, the situation-reading alone was the valuable part — which is the architecture we hope for, because it keeps every future consumer of the signal thin.

For the LLM conditions, the model's raw answer is called a **proposal** — a JSON object with four parts (full example in `../data-contracts.md` §7): `reasoning`, free prose where the model must explain its reading *before* concluding; `situation`, a one-line human summary; `system`, the machine-readable claim — one mode plus attributes, in the closed vocabulary; and `subsystems`, optional per-consumer suggestions (only `cpu_scheduler` matters here, and only variants B/C ever read it). The reasoning-first structure is a requirement, not a style preference, for two reasons: models measurably decide better when made to articulate their reading first, and when a run goes wrong the reasoning is what tells us *which* of two very different things failed — the model didn't know what the software was (a limit of the whole approach), or it knew and drew the wrong conclusion (a fixable prompt or mapping problem). Without the reasoning, those two failures look identical in the data.

The **validator** sits after every recognizer, LLM or not, and gives each answer a verdict. Its checks are mechanical: is the mode on the menu? every attribute? if a configuration was proposed, is every field known and every value inside its legal bounds? Its verdict is recorded on everything downstream, and there are exactly four (the project calls this stamp **provenance** — the origin story of an applied setting):

- **unmodified** — the answer passed every check and was used exactly as given;
- **clamped** — the answer was usable but one or more numeric values fell outside legal bounds and were pulled to the nearest legal value (e.g. a proposed time slice of 0 becomes the minimum);
- **held** — the answer was rejected outright (unknown vocabulary, malformed output), so the previously active configuration simply stays in force;
- **fallback** — nothing usable has ever arrived, or failures have repeated enough that the daemon has retreated to the boot default for good.

Why this bookkeeping is non-negotiable: imagine a condition that scores wonderfully while 70% of its configurations were `held` or `fallback`. It didn't demonstrate good recognition — it demonstrated that the default scheduler is fine and the recognizer was mostly ignored. Every performance number in the paper is therefore reported next to the provenance breakdown of the schedule that produced it, and the breakdown is only computable because every entry carries its stamp.

Everything about *how* you get schema-valid JSON out of a model — JSON mode, constrained decoding, retry policies — is yours. Whatever tricks you use, the validator still checks everything; belt and suspenders.

## 5. The driver table — 인지오's piece, and where the pipeline currently ends

After validation, an accepted situation reading has to become actual scheduler settings. That translation is a lookup table — the **driver table** — mapping each `(mode, attributes)` combination to one concrete configuration: "development with a wanted background job → MLFQ with these queue parameters and background capped at 15%," "gaming with a real-time encoder → deadline-first scheduling with these bounds," and so on, one row per situation the vocabulary can express. The table is deliberately *not* smart: it's a frozen artifact, identical across all conditions, so that the only thing differing between conditions is how well the recognizer lands on the right row. For variant A and all the baselines, the table is the entire policy.

**This table is 인지오's to build, not yours** — for a structural reason: its input side *is* the shared vocabulary (`../recognition-vocabulary.md`: 16 modes × `background_wanted`), and its output side is effectively the executor's behavior specification, which freezes jointly with 경민. Until it lands, the daemon pipeline runs **up to and including the validator**, and the config mapper + latency stamping stage is wired in afterward (tentatively also 박이안's, but that split may shift when the table arrives).

## 6. The outputs

Both are specified with full examples in `../data-contracts.md` (§5 and §6); in brief, per workload × condition:

- **Config schedule** — `{workload_id, condition, schedule: [{t_us, config, provenance}, …]}`: the finished list of "at virtual time T, the scheduler's settings become C," starting with the mandatory default entry at t = 0. This is the only thing the simulator ever sees of the daemon's work, so it must stand entirely alone. *Emitting these becomes possible once the driver table lands (§5).*
- **Recognition log** — `{workload_id, condition, queries: [{t_set_change, telemetry, proposal, validation, latency_us}, …]}`: one entry per query point, recording exactly what the recognizer was shown, everything it answered, the validator's verdict, and how long it took. This is where all recognition-quality grading happens — mode accuracy, the confusion matrix (which situations get mistaken for which), per-attribute accuracy, answer consistency across repeated runs, accuracy split by how famous the software is — all computed by comparing log entries against the answer key, with no simulator involved. It's also where `reasoning` is preserved for human failure analysis. Non-LLM conditions fill it with their thinner equivalents — the whitelist logs which rule matched, the oracle logs which answer-key row it read, `random` logs its draw and seed — so every condition's decisions are auditable in one uniform place. *This output needs nothing beyond the validator, so it's fully buildable now.*

## 7. Record and replay — how the LLM stays affordable and reproducible

Running the full experiment matrix live against a model would be slow, expensive, and — worse — non-reproducible, since models answer slightly differently across calls. So the LLM path runs in two modes. In **record** mode, the daemon actually queries the model, once per *distinct* telemetry snapshot, and stores each raw response together with its measured latency in a cache. In **replay** mode, it serves every answer from that cache with no model in the loop — fast, free, and bit-identical every time. The cache key is `(workload_id, snapshot hash, prompt version)`: one recorded pass serves every variant and every rerun, and bumping the prompt version deliberately invalidates the cache, so a prompt change can never silently mix old and new answers in one result.

Plan for two model hosting setups behind one client interface: a hosted API for fast day-to-day prompt iteration, and a locally hosted quantized model for the recorded runs that go into the paper — partly because a deployment story where the machine's process list is shipped to a remote server isn't credible, and partly because a local model on short structured outputs is fast enough to make the latency numbers meaningful.

## 8. Action plan and milestone

**박이안's scope, now:** telemetry builder → recognizer interface with the trivial recognizers → validator, plus the local LLM inference setup (hosting, client interface, record/replay skeleton) in parallel. Concretely, the first milestone — no LLM and no driver table anywhere in it:

1. Read the visible projection for one C1 workload (or the full `*.workload.json`, extracting only the projection's slice and discarding the rest at the parse boundary) and produce its telemetry sequence — snapshot count and contents checkable by hand against the timeline.
2. Run the `fixed`, `random` (seeded), and `oracle` recognizers through the machine as far as it exists — through the validator — and emit complete, valid **recognition logs** for all 24 workloads.
3. Rerun everything and diff: outputs bit-identical.

**인지오's scope, alongside:** build the driver table on the ratified vocabulary (`../recognition-vocabulary.md`). When it lands, the config mapper + latency stamping close the loop and the daemon starts emitting **config schedules** — at which point `fixed`/`random`/`oracle` become the exact three conditions of the **RQ0 gate**, the project's first real experiment (is the gap between random and perfect recognition even big enough to measure?). Your milestone plus the simulator's milestone 0 *is* that experiment's machinery. The whitelist comes next (needs your rule list, no model), and the LLM conditions after that, once record/replay keeps them cheap.

While building, expect two standing conversations: the **config schedule format with 경민** (it's the seam between your output and his input — 인지오 owns the contract, but you two are the ones who feel its friction) and the **recognition log format with 인지오** (it's the seam between your output and the grader).

## 9. Open questions, explained properly

These are the real unsettled decisions this guide cannot settle for you. Each entry says what the question actually is, why it matters, and where it stands.

### 9.1 The driver table's contents

Settled in ownership (§5: 인지오 builds it on the ratified vocabulary, with 경민 signing off the output side), but open in content: which situations map to which configurations is effectively the executor's behavior specification, and a badly filled table can make perfect recognition look worthless — if two different situations map to nearly identical settings, reading the difference between them buys nothing measurable. Filling it well, and *verifying* the filled table produces genuinely distinct behavior before running the full matrix, is its own piece of work.

### 9.2 Which latency number goes into the schedule

We record the true per-query latency at record time (that part is settled — it's in the recognition log). The open question is what to *stamp into config schedules on replay*: the raw measured latency of each original query (most realistic, but noisy — two recordings of the same run would produce slightly different schedules), one fixed constant per model (cleanest for the paper's headline claim, which has the shape "semantic scheduling pays off only when a situation persists at least N times the model's round-trip latency"), or draws from the measured distribution (realistic *and* smooth, but reintroduces randomness that must then be seeded). This is a small decision with a direct line to how quotable the RQ4 result is.

### 9.3 Hold time and hysteresis — do we need flap protection?

The problem in plain words: suppose the process set changes three times within a couple of seconds — an app opens, a helper appears, another app launches. The daemon would query three times and might emit three different configurations back-to-back, so the scheduler's settings flip, flip back, and flip again. Every switch is disruptive (tasks get reshuffled, a just-settled policy is thrown away), so a jittery recognizer could genuinely make the system *worse* than no recognition at all. Real systems guard against this with two rules: a **hold time** — "after applying a configuration, keep it for at least N seconds no matter what" — and **hysteresis** — "don't switch away until the new reading has stayed stable for a while," the way a thermostat refuses to toggle the heater over every 0.1° wobble. The open question is whether our experiment needs either rule at all: coreset segments are minutes apart, so flapping may simply never arise — but the C4 files deliberately inject a distractor process mid-segment, creating exactly one mid-situation query that could flip a configuration that *should* have been left alone. Current instinct: no rule for the coreset, revisit when the generated naturalistic set (with much denser process churn) arrives — but that should be decided consciously, not defaulted into.

### 9.4 Config schema per algorithm

Each algorithm has its own settings fields — MLFQ has queue counts and time slices, deadline scheduling has admission bounds, lottery has ticket shares — so validation branches per algorithm, and the exact field lists must be pinned down. In practice this schema falls out of the driver-table work (the table's *values* are configs, so building it forces the fields into existence — 인지오 will effectively write it). But it is not merely the table's private format: every field is a promise the simulator must honor (경민 implements what `timeslice_us` *does*), so the schema freezes jointly with the simulator side rather than following automatically. Expect it to be settled in the same conversations as the config schedule format.

---

*The binding fine print behind this guide lives in `../data-contracts.md` (all shapes and examples) and, for what the workload files themselves mean, `../simulator/interpretation-contract.md`; this guide restates what the daemon needs, but if a discrepancy ever slips in, those win — and tell 인지오, since a discrepancy is a bug in this guide.*
