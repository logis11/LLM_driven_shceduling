# What the Simulator Actually Does

**A plain-language companion to `RESEARCH_PROPOSAL.md` §4.7**

This note answers one question: *if we are not running real processes, what exactly is the simulator doing?* It assumes no operating systems background and contains no code. Readers who want the implementation details should go to the simulator design notes instead.

---

## The short answer

**We do not run processes. We draw a timetable.**

The simulator never executes any real work, never occupies a real CPU, and never lets real time pass. It is a program that fills in a table describing which process would have held the CPU at each moment.

---

## The bank counter

Picture a bank with exactly one open counter. Ten customers are waiting. The counter serves one person at a time, so somebody has to decide who gets called next. That decision rule is the scheduler.

If you want to compare two different decision rules, you have two options:

1. **Build a real bank.** Hire ten customers, open for a full day, measure what happens.
2. **Work it out on paper.** Write down "9:00 customer A, 9:03 customer B, 9:05 back to customer A…" and read the results off the schedule.

Our simulator is option 2.

In this picture, each process is a customer carrying a **pre-written script** — a fixed alternating sequence of "needs the counter for N minutes" and "steps away for M minutes."

```text
  Discord    = 3 min at counter -> away 20 min -> 2 min at counter -> away 15 min -> ...
  Compiler   = 8 hours at the counter, continuously
```

The critical property: **the script never changes.** Whatever the scheduler decides, Discord still needs the same total amount of counter time in the same sized pieces. What the scheduler changes is only **where those pieces land on the timetable.**

---

## What the simulator produces

The entire output of a simulation run is a timeline like this:

```text
          |          |                    |        |              |
  CPU     |  Discord |     Compiler       | Discord|   Compiler   |
          |          |                    |        |              |
          +----------+--------------------+--------+--------------+
          ^          ^                    ^        ^              ^
          moments when something happened

          ----------------- virtual time ----------------->
```

That is all of it. No computation is performed inside those blocks. No real seconds elapse. The simulator is simply deciding where each block starts and ends.

Two things are worth noticing about this picture.

**The clock jumps between the tick marks.** Nothing happens in the middle of a block, so there is nothing to compute there. The simulator moves directly from one interesting moment to the next. This is why a simulated minute finishes in well under a second of real time, and why we can afford to run the full experiment matrix many times over.

**The tick marks are the only decision points.** Every mark is a moment where the situation changed — a process finished its turn, a process woke up, a time slice ran out, a new configuration arrived. The scheduler is consulted at these moments and nowhere else.

---

## Where performance numbers come from

This is the part that feels strange at first. **The performance metrics are not measured by timing anything. They are computed by reading the timetable.**

| Metric | How it is read off the table |
|---|---|
| Response time | Gap between when a process arrived and when its first block begins |
| Turnaround time | Gap between arrival and the end of its final block |
| Deadline miss | A frame's block ends later than its deadline |
| Throughput | Total width of the blocks belonging to batch work |
| Starvation | Longest stretch during which some process holds no block at all |

Swap the scheduling algorithm and the blocks get arranged differently, so all of these numbers change. **What we are comparing is arrangement, not hardware.** Nothing about the speed of the machine running the simulator enters the result.

---

## Why this is a legitimate way to answer our question

Our research question is whether recognizing *what the machine is being used for* helps decide *what order to run things in*. Both halves of that question live entirely in the arrangement of blocks.

Building a real kernel would require booting, memory management, interrupt handling, device drivers — none of which contribute anything to that question, and all of which would consume the semester.

The simulator also gives us something a real machine cannot: **exact reproducibility.** Every condition in the experiment ladder faces a byte-identical workload. On real hardware, background noise, thermal throttling, and other tenants would introduce variation large enough to swamp the effect we are trying to measure. On paper, the only thing that differs between two runs is the thing we deliberately changed.

---

## What this design cannot tell us

The cost of drawing a timetable instead of running a machine is that anything not represented on the timetable is invisible to us:

- **Cache effects.** Real context switches discard cache locality; our blocks do not model that penalty faithfully.
- **Multi-core interaction.** The timeline above has one lane. Real contention across cores is a different problem.
- **Real kernel overhead.** Lock contention, interrupt storms, and scheduler implementation cost do not appear.

So the honest scope claim is narrow and worth stating in the paper exactly as written here:

> This work asks whether semantic context carries a usable signal for scheduling. That is a prerequisite for a real implementation, not a substitute for one.

---

## One sentence to remember

**The simulator does not imitate a computer. It draws the timetable a computer would have produced.**
