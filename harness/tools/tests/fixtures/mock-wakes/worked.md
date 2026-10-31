# mock-wakes — worked derivation

One measured application, `app` (named `kdenlive`), whose own wakes come on its two channels by the origin of their measured wake chain (`_dev/docs/spec/jioh/timer-wakes-by-origin.md`; the interpretation contract's `WAIT(channel)` row): `timer:app`, whose mailbox holds one wake, the first, and drops a later one with a `wake_drop` line; `event:app`, which queues with depth as `input:` does. Condition `fixed`, no table. Scheduler: the lane is otherwise idle, so the task runs as soon as it is ready. All times µs. The RQ0 gate spec's conformance item (j), on a hand fixture.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `app` | `kdenlive` | 0 | 20000 | WAIT timer, RUN 4000, WAIT timer, RUN 1000, WAIT timer, RUN 1000, WAIT event, RUN 2000, WAIT event, RUN 1000, WAIT timer, RUN 1000, WAIT timer | 10000 |

Wake events: on `timer:app` at 1000, 2000, 3000 and 12000; on `event:app` at 4000 and 4500. The timer channel's WAITs pair one to one, in order, with the task's timer wakes: the first with 1000, the second with 2000, the third with 3000, the fourth with 12000; the fifth is the trailing WAIT. `T_end` = 20000 (the depart). No TIMER task, so no chains.

## What happens

| t | event |
|---|---|
| 0 | boot config applied. `app` arrives; its first instruction, a WAIT on `timer:app`, blocks in its arrival step: no `ready` line, no occupancy. |
| 1000 | timer wake 1 completes that WAIT → `ready(wake)`. `app` runs at once: `run_start`, RUN 4000. |
| 2000 | timer wake 2 comes while `app` is mid-burst, not blocked on its timer channel. The timer mailbox is empty: it holds the wake. No line. |
| 3000 | timer wake 3 comes while wake 2 is held: dropped → `wake_drop` at 3000. |
| 4000, 4500 | event wakes 1 and 2 come mid-burst. The event mailbox queues both. No line. |
| 5000 | RUN 4000 ends. The second timer WAIT completes at once on held wake 2 → `ready(wake)` at 5000 inside the occupancy. RUN 1000. |
| 6000 | RUN 1000 ends. The third timer WAIT is wake 3's, dropped: it and the RUN 1000 after it pass with no block, no work and no line. The first event WAIT completes at once on queued event wake 1 → `ready(wake)` at 6000 inside the occupancy. RUN 2000. |
| 8000 | RUN 2000 ends. The second event WAIT completes at once on queued event wake 2 → `ready(wake)` at 8000 inside the occupancy. RUN 1000. |
| 9000 | RUN 1000 ends. The fourth timer WAIT blocks: nothing held. `run_end(block, wait)`. One occupancy, 1000 to 9000. |
| 12000 | timer wake 4 completes it → `ready(wake)`, `run_start`, RUN 1000. |
| 13000 | RUN 1000 ends. The trailing timer WAIT blocks. `run_end(block, wait)`. |
| 20000 | `T_end`. `app` departs. |

## Rows

**`ready_wait`** — one per `ready` line, value = next `run_start` − t, or 0 inside the task's own occupancy; `channel` the kind of the WAIT it completes.

| t | value | why | channel |
|---|---|---|---|
| 1000 | 0 | `run_start` at 1000 | timer |
| 5000 | 0 | inside the occupancy 1000–9000 | timer |
| 6000 | 0 | inside the occupancy | event |
| 8000 | 0 | inside the occupancy | event |
| 12000 | 0 | `run_start` at 12000 | timer |

**`app_latency`** — one per timer or event wake, at its wake time (metrics doc §6.13). A served wake's value is the start of its service — its `ready` line's `run_start`, or the line itself inside the occupancy — minus the wake time. A dropped wake's value is the service start of the latest wake before it not dropped, the wake held when it came, minus its own time, `skipped` 1.

| t | channel | served by | value | skipped |
|---|---|---|---|---|
| 1000 | timer | `ready` 1000, `run_start` 1000 | 0 | 0 |
| 2000 | timer | `ready` 5000, inside the occupancy | 3000 | 0 |
| 3000 | timer | dropped; covered by wake 2's service at 5000 | 2000 | 1 |
| 4000 | event | `ready` 6000, inside the occupancy | 2000 | 0 |
| 4500 | event | `ready` 8000, inside the occupancy | 3500 | 0 |
| 12000 | timer | `ready` 12000, `run_start` 12000 | 0 | 0 |

None censored: every wake is served or covered before the depart.

**Window rows.** `arrival` 0 (the `task_arrive` line), `completed` 0 (no exit; it departs), `cpu_delivered` 9000 = 4000 + 1000 + 2000 + 1000 + 1000 (the dropped wake's RUN 1000 does no work), `demand` 10000 (the program's RUN total, the passed RUN included), `preempt_count` 0, lane `busy` 9000 = 8000 + 1000, the boot entry's `config_interval` from 0 for 20000.

**Guards.** None. On `timer:app` four wakes: three served (`ready` lines at 1000, 5000, 12000) and one dropped (`wake_drop` at 3000), the drop coming while wake 2 was held; on `event:app` two wakes, two served. At its end `app` is blocked on its trailing timer WAIT with every timer wake sent before then served or dropped: no wake lost.
