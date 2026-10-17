# 9.16 compiled-number audit — findings and proposed fixes

Every STALE, WRONG and UNNAMED verdict of `report.md`, grouped by cause.

- G1, F1 and F3 are WRONG. G1 and F1 each need a judgement, so they go to 인지오 as one question each, in chat (decision 4).
- The STALE fixes are wording on the current files.
- For a memo, the fix is a bullet in its existing "Correction (2026-10-17)" section.

## WRONG

**G1 — The `tick_count` guard fails by construction on c7-gaming, so the RQ0 verdict comes out `invalid`.**
- Location: `harness/guards/guard-spec.yaml:77–82, 177–186`. The same consequence reaches `rq0-gate.yaml:188`, the seg1-120s line's "expected unchanged".
- Why it fails:
  - c7-gaming's last consumed tick (26,383,861 µs) lies 1,139 µs before T_end, and its frame needs 14,999 µs.
  - So the tail is one iteration short on every run (`primitives.py:301–309`).
  - A failed guard on a primary-boot run of a judging file makes the verdict `invalid` (`evaluator.py:369–390`).
- The same happens on c3-evening and c6-dual (reporting), all six c7-gaming variants, and c2-p2a and c2-p2b @chain-x1.2, @chain-x1.4, @seg1-30s and @seg1-120s.
- c1-gaming, c4-gaming, c2-p2a and c2-p2b escape it by 468 µs and 773 µs.
- It is hidden today only because the simulator emits no arrival `ready(timer_tick)` line (item (a)).
- Proposed fix, a question for 인지오. Either:
  - (i) the chain check compares only the ticks whose frame could complete by T_end — leave out a consumed tick whose `tick + chain demand` exceeds T_end, or whose deadline falls after T_end — stated in the guard spec's `tick_count` grounding and in metrics doc §6.2; or
  - (ii) cut c7-gaming, and the listed variants, so that a whole frame fits after the last tick.
  - Option (i) touches no dataset byte. Option (ii) needs a rebuild and new pins.

**F1 — c2-p3b's backup finishes inside the file.**
- Locations: `harness/scoring/scoring-spec.yaml:204–205` ("about 162 s of its 165.7 s, and does not finish: progress") and `:168–172` ("the batch task … does not finish inside the file").
- Facts: replayed alone, the editor uses 99.8 s of 60–326 s. That leaves 166.2 s of idle lane against the backup's 165.67 s of CPU and 0.19 s of sleeps, so the backup ends about 0.3 s before T_end. The 162 s came from the manifest's even spread of the editor's CPU.
- By the header's rule (lines 30–32), a job that finishes under every row scores its turnaround.
- Proposed fix, a question for 인지오. Either:
  - (i) change c2-p3b's term to `bulk` turnaround at 0.25 (c1-backup already scores its backup's turnaround) and restate the comment; or
  - (ii) keep `cpu_delivered` and restate the comment as "about 166 s of idle lane, which finishes the backup about 0.3 s before T_end; progress kept because …".
- Either way, change `:171` to say P1 and P2 do not finish and P3's two jobs do.
- The file stays no headroom and reporting-only.
- The pair review's p3 row (`:46`) needs "about 166 s" in place of "about 162 s"; its conclusion holds.

**F3 — The batch-class memo's worked examples read the 2026-09 core set.**
- Location: `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`.
  - `:56` is WRONG: c2-p3b's background is now Déjà Dup, idle class, which no cap reaches.
  - `:21–29`, `:50/52/60`, `:54`, `:58`, `:60–63` and `:69` are STALE.
- Proposed fix: one Correction bullet saying the §2 and §4–§5 worked examples read the 2026-09 core set, and that on the rebuilt files:
  - the boot slice is 10 ms;
  - c2-p2b's background is the unattended upgrade, batch class over 92 % of its CPU, which the 0.05 cap reaches;
  - c2-p3b's is Déjà Dup, idle class, which no cap or share reaches;
  - no core file has a compositor;
  - the download's whole program is batch class over 74 % of its CPU, but the part the file delivers under EDF is not;
  - a keystroke costs VS Code about 80 ms and LibreOffice Writer about 3 ms, and Kdenlive has no keystroke stream;
  - rules B1 and B2 are unchanged.

## STALE

**F4 — "About a fifth" of the call's cycles reach the 10 ms slice; the true figure is about one in twenty.**
- Locations: `rq0-gate.yaml:30–32, 121, 240–248, 413–417`; `scoring-spec.yaml:66–68`; pair review `:59` and `:79` (finding 5).
- Facts: compiled 5.5 %; the measured table's p95 is 9,992 µs. "A fifth" reads the p95 knot as p80.
- Proposed fix: "about one cycle in twenty (5.5 % of the compiled cycles; the table's p95 is 9.99 ms)".
- The c7-meeting decision stands: in the simulator, the boot MLFQ misses 31.7 % and EDF 5.7 %.

**F5 — Percentile knots read as deciles.**
- `rq0-gate.yaml:127` and `:416`: "decile cuts 2.3 to 7.5 ms" → "deciles 2.8 to 5.4 ms (2.3 and 7.5 ms are the table's p1 and p99.9)".
- `:127`: "about seven in ten" → "about eight in ten" (82–83 % compiled).
- `:128`: "upper decile (7.5 ms)" → "upper decile (5.4 ms)".
- `:129` and `:417`: "12.2 ms ninth-decile" → "12.2 ms 99th-percentile (ninth decile 7.4 ms)".
- Name the 18.9 and 16.0 ms maxima as the measured tables' (the compiled maxima are 15.2 / 14.3 ms and 11.5 / 7.3 ms).

**F6 — Chain ×1.4 lanes (`rq0-gate.yaml:176`).** "(1.14 and 1.26 lanes)" → "(1.33 and 1.26 lanes)".

**F7 — Judging lengths (`rq0-gate.yaml:182`).** "every other judging length is a job's measured CPU total" → "every other judging length follows from a job's measured CPU total (with the editor's beside it on the batch C1 bases and c2-p3a; c1-render's 60 s is design)".

**F8 — Counterpart keystrokes and the window end.**
- Pair review:
  - `:54`: 79 → 84, "85 … less the 6 inside the counterpart's page load" → "90 … less the 6 past 24.385 s".
  - `:55`: 91 → 101, 102 → 112.
  - `:57`: 47 → 49, both places.
  - `:84`: 79/91/47 → 84/101/49, and "less the ones inside the counterpart's own operations" → "less the ones past its input window's end at 24.385 s and inside its own operations".
  - `:50`: "its keystrokes are the base's over those seconds" → "… over 2 s to 24.385 s".
- RQ0 gate spec:
  - `:442–444`: "about a hundred keystrokes" → "49 to 101 keystrokes".
  - `:445–448`: "the base's first 26.385 s" → "the base's input window up to 24.385 s".

**F9 — The download is not batch class where the file delivers it.**
- Locations: `scoring-spec.yaml:51–54, 181–183`; `prior.yaml:214`; pair review `:45` and `:75`; final memo `:312`.
- Proposed fix: "the measured download's whole program is batch class over 74 % of its CPU, but the part a 26.385 s window gives it under EDF (about 1 s) is its launch phase of short runs, not batch class; either way no cap acts on it, and the boot MLFQ gives it more (3.0 s against 1.1 s)".

**F10 — Pair review demand column (`:54`, `:57`, `:63`, `:67`, `:71`).**
- browsing 1.02 → 1.03; dev 1.29 → 1.21; compile 1.11 → 1.19; indexing 1.10 → 1.09.
- `:71`: "just above one lane" → "between 1.03 and 1.56 lanes".
- `:71`: "the batch counterparts near their bases since a label flip adds no work" → "the batch counterparts above their bases (1.09–1.62 against 0.73–1.00), since each is cut to its job's CPU total".

**F11 — The browser's keystroke cost (`prior.yaml:39–41`; pair review `:83`).** "the browser next to nothing" → "the browser about 4 ms".

**F12 — The LOTTERY editor's share (`prior.yaml:292`, `:318`).**
- Add the qualifier the pair review's p1 row carries: the editor holds the stated remainder while its run since its last block is within one 10 ms slice — at the keystroke's wake, where the term is read.
- Past that it is batch class and shares the batch class's draws evenly:
  - c1-compile: with up to eight build members; 83 % of the editor's CPU;
  - c2-p1a: with the training run; 87.5 %.

**F13 — "MLFQ's textbook case" (`prior.yaml:336`, `:414`).** Restate on the header's reading: the editor here is VS Code, demoted within each keystroke, and its waits meet the job in the queue they share. For indexing/false, add that the intruder is idle class.

**F14 — The floor cap is not free to act on idle-class flips (`scoring-spec.yaml:276–279`).** Add: "except c7-indexing and c7-backup, whose flipped job is idle class (both reporting-only)".

**F15 — Dated memo bodies presented as current.**
- trace-clarifications `:38` "sixteen tasks" → 17 members (16 stages and wineserver).
- trace-clarifications `:68` "its 230 µs" → "its 0.2–0.9 ms".
- trace-clarifications `:76` → 1,389.885 s from 60 s in a file whose labels end at 99.435 s.
- timer-skip `:45` "26 of the scoring spec's 78 terms" → "22 of 75".
- declared-class `:9` → three entries, adding `game-download-idle` (compiled into c2-p2a-idle).

## UNNAMED

**F16 — Name the conformance item each simulator-dependent statement waits on.**
- Append "(RQ0 gate spec conformance item (x))" at each UNNAMED location in `uncheckable-by-item.md`. That is 10 rows:
  - item (e), the strict idle class: `rq0-gate.yaml:296–304`; `scoring-spec.yaml:36–43`, `:96–98`; `prior.yaml:30–34` and `:396/408/422/434`; pair review `:15/34/35/44/46/67/68/81`.
  - item (d), the cap: pair review `:21/24/54/83`.
  - item (b), the TIMER skip rule: `scoring-spec.yaml:62–65`.
  - item (g), `WAIT children:<id>`: `scoring-spec.yaml:30–32` at `:112/238`; pair review `:30`.
- Pair review `:83` should also drop the indexing files from the floor-cap reading, since their indexer is idle class.

## Noted, not a stated claim

- **c3-evening, reporting-only.** Under EDF the 1.45-lane chain saturates the lane, so the residual `chat` and `steam` wait for the whole 240 s gaming segment. The simulator shows `steam` waiting 240 s.
  - This fails `starvation_floor` (30 s) on every EDF-row run of the file. It does not invalidate the verdict, because the file is reporting-only.
  - It does fire the gate's longest-wait line by construction ("any run past 15 s reopens the executor-net question", `rq0-gate.yaml:448–450`).
  - Worth one line beside that statement, or an expected-exceedance note in the RQ0 gate spec.
- **Outside this audit's scope** (boot-default config, not the compiled workload): the algorithm-switch memo's 2,000 µs slices and `W_single` = 2,000 + 4,000 = 6,000 µs (`:26`, `:60`), and the batch-class memo's FIFO fallback of "the boot default's 2000 µs" (`:37`, `:81`). The boot slice is 10 ms (`harness/boot-defaults/ostep.json`).
