# Note for jioh — TIMER backlog vs. frame-drop for periodic (game/video) work

> Status: memo · Created 2026-09-29 · Updated 2026-09-29
> Author: kyungmin. Raised while reading the `steps/` ladder (sim_k, TIMER). Not a spec change — a design question with a tentative resolution, left here for jioh to confirm or overrule.

## The question

`sim_k` (TIMER) consumes **missed grid ticks as backlog**: if a task is starved past
one or more ticks of its period grid (`t0 + k·P`), the overdue TIMERs each complete
*immediately*, one per loop iteration, so the task rattles off the overdue frames
back-to-back before a TIMER blocks again. The rationale in the docs is measurement
integrity: silently skipping missed ticks would **lower CPU demand exactly under a bad
scheduler**, masking the very damage the experiment wants to measure (same argument as
D2's mailbox for lost wakes).

The objection: **real games don't replay a late frame — they drop it** and render the
latest state once. So backlog looks like it models something a real engine doesn't do.

## What the docs already say (confirmed, quoted)

- `docs/simulator/simulator-guide.md:127` — TIMER ticks "regardless of how late previous
  iterations ran ... **which is what a 60 fps game actually does**. Late ticks
  **accumulate as backlog** ... missed frames turn into **pressure, not silence**."
- `docs/simulator/simulator-guide.md:129` — "a starved periodic task piles up pressure
  and fights to catch up — **like a real game engine** — instead of quietly skipping
  frames, which would *reduce* CPU demand exactly when the scheduler misbehaves and
  **mask the damage the experiment wants to see**."
- `docs/simulator/interpretation-contract.md:31,36` — TIMER "Late iterations accumulate
  as backlog; they are **not silently skipped**." Periodic tasks use TIMER never SLEEP:
  "relative sleeps drift under delay, **silently lowering demand exactly under bad configs**."
- `dataset/archetypes.yaml:505` — daemons use SLEEP **not** TIMER, "because stock daemons
  are not drift-free periodic." So backlog is scoped to genuinely grid-locked work, not
  applied blindly.
- The "how many frames were late/dropped" signal is **not lost**: it is measured as
  **deadline miss rate / P99 frame latency** (`simulator-guide.md:219`,
  `docs/harness/metrics.md:139,145`). `c1-gaming` emits 4,482 `deadline` lines.

So backlog is a **deliberate, documented, normative** decision, and the drop-count signal
the objection wants already exists via the `deadline` mechanism.

## The realism split (my assessment — not in the docs verbatim)

The doc's "like a real game engine" is true for **one layer only**:

- **Logic / physics ticks** — real engines use a fixed-timestep accumulator and *catch up*
  on missed ticks (Glenn Fiedler, "Fix Your Timestep"). Missed logic work is **not
  dropped**; it accumulates. → backlog is faithful here.
- **Render / present** — real engines **drop** the missed frame and present the latest
  state once. → backlog over-counts render work here.

The simulator models TIMER as *work-per-tick that must be done*, i.e. the logic-tick
layer. The present-layer lateness is folded into `deadline`/frame-latency, not into demand.

## The alternative that was proposed, and why it was not taken

Proposal A — "just use a periodic **deadline** instead of TIMER": **rejected.** A deadline
generates **zero CPU demand**; with no RUN work the game task competes for nothing, and the
scheduling experiment collapses. TIMER+RUN (load) and `deadline` (measurement) are
orthogonal and are *already both used together* — one is not a substitute for the other.

Proposal B — "grid-locked TIMER but **drop** the missed frame's work and generate a fresh
frame each tick" (the actual real-render model): **coherent and free of the masking
problem** (offered load stays constant, misses counted by `deadline`), but costs:

1. It **inverts a core invariant** — "a RUN's demand is preserved across preemption"
   (`run_left` conserved since sim_f). Drop-model needs "a RUN whose demand the next TIMER
   tick can void," a new semantics, not a small patch.
2. **Executed load becomes scheduler-dependent** (only *offered* load is constant), so
   aggregate metrics (turnaround, utilization) stop being directly comparable across
   schedulers unless always paired with a drop count. Backlog keeps executed == offered.
3. **Chains are ambiguous** — a game frame is a ~16-stage bucket brigade; dropping a frame
   mid-chain leaves "which stage's work is dropped?" undefined. Backlog says all stages
   catch up together.

## Tentative resolution (for jioh to confirm)

Keep **backlog** (current behavior). It is the cleaner *measurement* model: demand is
conserved so aggregates compare directly, quality loss is measured separately by
`deadline`, and it is faithful to the logic-tick layer. Proposal B is a legitimate
higher-render-fidelity alternative but trades measurement cleanliness and a core invariant
for it.

**Residual caveat worth a one-line doc fix:** the guide's "like a real game engine" reads
as if it covers presentation; strictly it is true only for the fixed-timestep logic layer.
For pure render work, backlog does over-count CPU demand. If jioh agrees, soften that line
to name the logic-tick layer explicitly.

## Open items for jioh

- [ ] Confirm backlog stays; or decide Proposal B is worth the invariant change.
- [ ] Consider softening `simulator-guide.md:127/129` "like a real game engine" to scope it
      to the logic-tick (fixed-timestep) layer, since render presentation does drop.
- [ ] No code change implied by this note unless the above is decided.
