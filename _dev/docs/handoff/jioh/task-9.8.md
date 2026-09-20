# Handoff — task 9.8 Browser and comms (2026-09-20, the first batch in flight)

Stage 3 on `jioh/dataset-rebuild`. **D1–D16 landed, the tooling is written and proven, the long-phase probe is
done, and the first batch is running.** Nothing is pooled yet and no archetype value has changed.

Next session: land whatever repeats are still outstanding, pool five per subject, and read the stability rule
for the first time. That verdict is what decides whether 9.8 goes to the fold-in or starts adding repeats.

## Read these first

| What | Where |
|---|---|
| The campaign method, §10 carrying the phase lengths and the settles | `_dev/research/jioh/task-9.8-browser-comms/campaign/method.md` |
| **D15** the probe, **D16** the visible entry's phase; D13 the tooling, D14 the dry run | `_dev/research/jioh/task-9.8-browser-comms/changelog.md` |
| The loop, the machine gate, the stability rule | `_dev/research/jioh/measurement-campaign-workflow.md` |

## Where the batch stands

Campaign tag `meas-ci:desktop:2026-09-20`, `mode: full`, held to the AMD EPYC 7763.

- **Repeat 1 — landed and checked for all four subjects.** Runs 35506753479 (`chrome-visible`), 35506838639
  (`element`), 35506882547 (`chrome-hidden`, `steam`). Every one: `gate=open`, no harness process in its tree,
  no non-zero return code, every phase present at 600 s, no part-phase renderer. All four pool.
- **Repeats 2–5 — pushed as sixteen jobs**, run 24 (35508871434) and the retry runs after it.

To see what is still outstanding and restart the retrying:

```
tail ~/.cache/meas-loop/batch-9.8/retry.log
bash ~/.cache/meas-loop/retry-batch-9.8.sh 24 chrome-hidden:2 … steam:5      # <since-run> <app:k>…
```

The driver relaunches only `wrong-machine` draws, reads each short job's report before calling it gated, and
stops rather than retrying on a failure or any other gate. It was started detached; it may or may not have
survived the session.

## What this session settled

- **The throttling gate was rejecting every valid hidden repeat** (fixed, `2c5225b`). `throttling_check` took
  the highest rate in `per_pid_wakes_per_s`, which is computed before the control tab is dropped — and the
  control tab is never throttled by design. It read 10.193 against a 0.5 limit while the worst measured
  renderer was 0.184. A five-repeat batch would have pooled nothing, with every job reporting `gate=open`.
  Repeat 1 confirms the fix in production: `(True, 0.155)`.
- **The phase lengths and settles** (D15): steady 600 s everywhere, N = 12, launch-settle 20 s for the two
  renderer subjects and the chat client and 900 s for the Steam client, hidden grace-settle 630 s. Two subjects
  were still settling inside what the method treated as steady.
- **The visible entry reads the no-timer phase** (D16), so its wake rate is an observation, 0.130 wakes/s per
  renderer, not our timer period.

## Open threads

- **The twelve throttled renderers wake together** — 243 bins of 1 s and 32 of 10 ms hold all twelve, against
  none under independence. Recorded in method §10 and D15. What it does to D14's decision to pool the N
  renderers of a job as N samples of one renderer is undecided, and it belongs to the fold-in.
- **D5's comparison has moved.** D14 recorded minimising the Steam client at 3.338× in CPU share from 45 s
  phases taken soon after launch; repeat 1, with the 900 s settle, reads 1.382× (0.01755 → 0.01270). The wake
  rate agrees — 1.225 now against 1.277. It still resolves above method §6's 10 % floor, so D5's direction
  stands, but the magnitude looks like an unsettled measurement. The five repeats will say.
- **The chat client's traffic phase** reads 4.0× idle at 600 s where the 45 s dry phase read 8.1×. It feeds no
  archetype (D11) but should not be carried into the results as the same measurement.
- **The pooled record says `renderers {1: '13'}`** where the analysis measured 12 — it takes
  `renderers.observed` rather than the count after the browser's own renderer is dropped. No carried value
  depends on it, but D14 hands to 9.13 that each entry's scope states the renderer population it was pooled
  from.
- **Automating the add-repeat loop** (인지오's proposal): mechanical by the workflow's step 5, which adds
  repeats one at a time with no ceiling until every value holds — but its step 6 is not, since a spread that
  follows the harness is a design decision, not more repeats. Guards to build in: stop on a failure or a gate
  that is not `wrong-machine`, stop on a repeat failing the validity checks, and stop when the widest
  half-width stops closing at roughly the 1/√n the rule implies.

## Operational notes

- Artifacts and helpers live under `~/.cache/meas-loop/batch-9.8/` and `~/.cache/meas-loop/probe-9.8/`
  (`size.py` sizes a phase from window spread; `align.py` tests wake coincidence across renderers).
- **The trigger carries five keys only** — `mode`, `attempt`, `cpu_model`, `apps`, `repeats`. Every design
  value is a constant in `run.sh` (D13); to change one, edit `run.sh` and bump `attempt` in the same push.
- **The branch is shared with other live sessions.** Push immediately after each commit.
- CI does not run on this branch. `make -C dataset test PY=python3.12`, about 8 minutes, currently 180 passed,
  1 skipped, 1 xfailed.
- Job lengths in `full`: about 23 minutes for the two renderer subjects and the chat client, about 42 for the
  Steam client. The EPYC 7763 draw rate has run near 40–50 %, so budget about two draws per landing.
- **Archives are written only when 인지오 explicitly asks.** Decisions go to the slice changelog.
