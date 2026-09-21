# Handoff — task 9.8 Browser and comms (2026-09-21 night)

Stage 3 on `jioh/dataset-rebuild`. **Three of the four entries hold the stability rule; the Steam client's waits on
one decision (D22).** Nothing is folded into the dataset yet and no archetype value has changed.

## Morning summary (2026-09-21 → 22)

| Entry | Repeats (all valid, EPYC 7763) | Rule |
|---|---|---|
| chat client (`element`) | 17 | **holds** |
| hidden renderer (`chrome-hidden`) | 11 | **holds** — run means under D17, the residual under D21 |
| visible renderer (`chrome-visible`) | 11 | **holds** — run means under D17, `Chrome_ChildIOT`, `ThreadPoolForeg`, residual under D21 |
| Steam client (`steam`) | 12 | two gap means fail — **D22, open** |

**Your decision — D22:** the Steam client's `steamwebhelper` and `ThreadPoolForeg` gap means. Within one run they
move ±0.1 % and ±1.7 %; across the twelve repeats ±21.0 % and ±19.6 % — same threads, same wake rate, the wakes
spread differently from one launch to the next. That is 9.5 D57's case by all three of its tests, but
`steamwebhelper` carries 23.6 % of the client's wakes against D57's 6.5 %. Carry both with their half-widths under
D57, or add about 46 repeats (42 min each). Evidence in the changelog, D22.

**Fixed without asking (all in pooling/analysis — the measurement is unchanged since D15, every repeat recorded
the same settings, so nothing was superseded):**
- the rule tested one phase-average instead of each component and the residual (`c7b8a72`)
- the renderer residual merged all twelve renderers instead of describing one (`1f44041`, D19)
- the pooled record stated the observed renderer count instead of the measured one (`52e4d5b`)

**Decided today by you:** D17 (run means carried under the machine-spread exception), D18 (D5 stated on the
wake-rate ratio — now 1.225 ±0.5 % over twelve repeats — and the Steam client's run means excepted too), D21 (the
renderer quiet threads carried with their half-widths).

**Checked, not a defect:** the chat client's traffic phase reading 4.0× idle against the dry run's 8.1× — every
repeat's driver sent exactly 600 messages over the 600 s; the dry figure was a 45 s phase dominated by the first
messages.

**Next, once D22 is decided:** the final pooled set into `campaign/results/` with the campaign tag, each entry's row
in `measurement-campaign-record.md`, the raw-record release (outward — ask first), then the fold-in with scope-card
items 6–10 and 15–16. Still open for the fold-in: what the renderer wake alignment (D15) does to pooling N
renderers as N samples.

**Watch:** `probe/appdefs.sh` is shared with 9.5's live campaign and holds our two Chrome arms. Before any further
Chrome launch, diff those arms against `332f627` — any change supersedes the Chrome repeats.

## Read these first

| What | Where |
|---|---|
| The campaign method, §10 carrying the phase lengths and the settles | `_dev/research/jioh/task-9.8-browser-comms/campaign/method.md` |
| **D15–D22**: the probe, the phase lengths, the fixes, the exceptions, D22 open; D13 the tooling, D14 the dry run | `_dev/research/jioh/task-9.8-browser-comms/changelog.md` |
| The loop, the machine gate, the stability rule | `_dev/research/jioh/measurement-campaign-workflow.md` |

## Operational notes

- Pool and read the rule: `python3 dataset/tools/meas/loop/pool_runs.py desktop/<app> --since 21`. Retry driver
  for gated draws: `bash ~/.cache/meas-loop/retry-batch-9.8.sh <since-run> <app:k>…` (or the repository's
  `loop/watch.py`).
- `desktop/within_run.py` places a spread within a run against between runs (9.5 D57's test; `--tree` for the
  Steam client and the chat client).
- The two analyses behind method §10's figures are in the repository:
  `dataset/tools/meas/desktop/window_spread.py` (sizes a steady phase from a probe's window spread — the 3.7 %
  at 500 s that set the hidden renderer's settle) and `dataset/tools/meas/desktop/wake_alignment.py` (the 32
  bins of 10 ms holding all twelve renderers). Downloaded artifacts sit under `~/.cache/meas-loop/batch-9.8/`
  and `~/.cache/meas-loop/probe-9.8/`, and are re-downloadable from the run ids above.
- **The trigger carries five keys only** — `mode`, `attempt`, `cpu_model`, `apps`, `repeats`. Every design
  value is a constant in `run.sh` (D13); to change one, edit `run.sh` and bump `attempt` in the same push.
- **The branch is shared with other live sessions.** Push immediately after each commit.
- CI does not run on this branch. `make -C dataset test PY=python3.12`, about 8 minutes, currently 180 passed,
  1 skipped, 1 xfailed.
- Job lengths in `full`: about 23 minutes for the two renderer subjects and the chat client, about 42 for the
  Steam client. The EPYC 7763 draw rate has run near 40–50 %, so budget about two draws per landing.
- **Archives are written only when 인지오 explicitly asks.** Decisions go to the slice changelog.
