# Note for jioh — conformance status after the cap, and the loader blocker is fixed

> Status: memo · Created 2026-10-21 · Updated 2026-10-21
> Author: kyungmin. A status reply, not a question — four things you should know before the
> re-baseline, and three places where a document of yours is now behind the tree. Full detail is
> in `../memo/memo_261020.md` (Part F for the cap, Part G for the loader) and `../src/notes.md`.

---

## 1. (d) is met — `batch_bandwidth_cap` is in

Stage V, 2026-10-20. The cap is applied as a work-conserving ceiling on the behavioural batch
class. The accounting window you left to this tree is decision **D10**: a token bucket, rate =
cap, depth = one slice, so the implied window is slice/cap.

Measured: negative control (every cap `null`) byte-identical to `sim_u` on 24×2 runs; three
capped schedules 24×3 terminate and reproduce; `src/sim` == `steps/sim_v` on 96/96 plus 18 hand
runs. Positive: MLFQ cap 0.05 → 5.2 %, 0.2 → 17.0 %, 0.5 → 30.0 % (above the ceiling, so
unbinding); LOTTERY 0.05 → 4.42 %; FIFO 0.05 cuts the non-preemptive holder and takes the
periodic task from 0 to 99 jobs.

**Two consequences need your confirmation** (they are consequences, not requests —
`memo_261020.md` Part F4):

1. **Under FIFO the cap preempts.** A ceiling over a non-preemptive algorithm has no other
   lever, and the executor's class rules sit below the algorithm (batch memo §3, "identical
   across algorithms"). This is what moves the periodic task from 0 jobs to 99.
2. **A capped stretch opening mid-occupancy leaves a debt rather than re-arming the holder.**
   Re-arming would hand out a horizon the policy has not charged.

So the conformance tally is now **(c), (d), (f) met; (a), (b), (e), (g), (h) owed.**

## 2. The 2026-10-10 audit's blocker 1 is fixed — but it changes the order of the re-baseline

Your audit found that the loader resolved a `WAKE` target only among top-level `arrive` ids, so
the rebuilt build's make jobs — six member processes waking **each other** by spawn-table id
(9.6 D19), and the module build's trees of 6/6/8/10 (9.10 D53) — were rejected whole-file. That
rejected `c1-compile`, `c7-compile` (**both judging files**), `c3-workday`, `c4-compile`,
`c6-dual`, the 8 compile variants the gate spec runs, and 188 generated files.

Fixed on 2026-10-21 as stage **W**. Detail and controls: `../memo/memo_261020.md` Part G.

Three things about it worth your attention:

- **It is invisible on the local build.** The 2026-09-04 build predates the structure — its
  `c1-compile` has 100 spawn-table entries and **zero** child WAKE targets, against 17,448 with
  mutual wakes in the rebuilt one. So the fix and the rebuild have to land together; before the
  rebuild nothing looks wrong, and after the rebuild without the fix five core files do not load.
- **A wake has to be *held*, not just resolved later.** `fork_cap` is `parallelism_cap × 6` while
  the module build's trees are 8 and 10 members, so the cap falls mid-job; a job's root is forked
  first and starts with a RUN while every other member starts with its own WAIT, so the root can
  run and wake a member not yet forked. Measured on fixtures built from your own `_object_job`
  and `_tree_job`: dropping that wake leaves 6 of 13 and 10 of 19 tasks permanently unfinished —
  the job deadlocks. Holding it, 13/13 and 19/19 finish.
- **It is not one of the eight conformance items.** It sits beside them. If you want it carried
  as a ninth, or folded into (g), say which — I have recorded it as conformance-adjacent.

I also made the loader reject a spawn-table id that collides with a top-level id, and a duplicate
spawn-table id. Neither was checked before; your canonical lint already forbids both, so this is
only the loader catching up.

## 3. Where the daemon stands (you asked for the state, not the plan)

`daemon/daemon.py` exists in my working tree, **uncommitted**, 349 lines. The pipeline seats are
all there — visible projection → telemetry snapshots → recognizer → validator → config mapper —
and the three conditions that need no model work: `fixed`, `oracle`, `random`. The five that need
a recognizer (`shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`)
exit non-zero saying so; each is one function away, and the seat is a `RECOGNIZERS` map.

Not there: no LLM client, no record/replay store, no hold time or hysteresis, no clamping path.
The validator seat exists and the three conditions pass through it, but since they compose their
configurations from the driver table they are valid by construction, so only `unmodified` and
`fallback` are ever emitted.

Contract tests pass (52). **But the CLI does not run on this tree's dataset** — it needs
`declared_class`, and the local build has none, so it exits 1. The README's "verified over 25
workloads × 3 conditions × 2 telemetry, 150/150" does not reproduce here for the same reason.
Treat the daemon as verified against synthetic workloads only until the rebuild.

`daemon/` is 이안's Phase 1 in the TODO, so say who should own and commit this.

## 4. Three documents of yours are now behind the tree

- **`harness/experiments/rq0-gate.yaml`'s `simulator-conformance`** and the 9.16 exit-audit
  product `_dev/research/jioh/task-9.16-exit-audits/compiled/uncheckable-by-item.md` still carry
  **(d) as owed**. It is met as of 2026-10-20.
- **`docs/guidebook/dataset/01-the-big-picture.md` §6.6** ("열린 자리") lists (b), (d), (e), (g)
  as the items compiled-number statements hang on, and closes with "여섯이 모두 보여지기 전에는
  RQ0 run이 시작되지 않습니다". (d) should come out. The doc's `Updated` is 2026-10-20, the same
  day the cap landed, so this is a one-line miss, not a stale document.
- **`docs/guidebook/dataset/01-the-big-picture.md` §1.6** says "2026-10-14 현재 저장소의
  `daemon/`에는 driver table과 그 lint만 있고 실제 recognizer는 아직 없습니다". See §3 above.

For the record, §7.2 of that guidebook is where I first saw blocker 1 — your note that the audit
recommended telling me at once and that the notice was not sent is accurate: it reached me in the
2026-10-17 rebuild memo, after `memo_261001`, `memo_261010` and `memo_261020` Parts A–F were
written, which is why none of them carry it.

## 5. What I am not doing, so you can plan around it

- **The rebuild and the re-baseline are yours.** `make -C dataset dataset variants`. The local
  build is 0/51 against the committed manifest (23 stale, 28 missing). I have left it untouched;
  a copy of the 2026-09-04 build is kept outside the repository in case a baseline is wanted
  before it is overwritten.
- **W is not in the `steps/` ladder.** There is no `steps/sim_w.cpp`, so
  `src/sim == steps/sim_<last>` now holds only up to V. Whether a loader fix earns a rung is a
  convention call — tell me and I will either port it or write the exception into
  `steps/README.md`.
- **(a) + Q2 are the next pair I intend to take**, since they are the same principle and the same
  traces. (b) needs (a) first. (e) needs the rebuilt dataset.
