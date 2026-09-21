# Handoff — task 9.8 Browser and comms (2026-09-22)

Stage 3 on `jioh/dataset-rebuild`. **Every entry holds the stability rule** under campaign
`meas-ci:desktop:2026-09-20`, all repeats on the AMD EPYC 7763, none excluded or superseded. Nothing is folded into
the dataset yet and no archetype value has changed.

| Entry | Repeats | Rule |
|---|---|---|
| chat client (`element`) | 17 | holds — run means under D17 |
| hidden renderer (`chrome-hidden`) | 11 | holds — run means under D17, residual under D21 |
| visible renderer (`chrome-visible`) | 11 | holds — run means under D17; `Chrome_ChildIOT`, `ThreadPoolForeg`, residual under D21 |
| Steam client (`steam`) | 12 | holds — run means under D18; `steamwebhelper`, `ThreadPoolForeg` under D23 |

Decisions this campaign: D15 phase lengths and settles, D16 the visible entry reads its no-timer phase, D17 run
means carried under the machine-spread exception, D18 D5 stated on the wake-rate ratio, D21 and D23 quiet or
between-session components carried under 9.5 D57. Fixes in pooling, analysis and download tooling only (D17, D19,
`52e4d5b`, `91b127d`); the measurement is unchanged since D15.

## Next, in order

1. **The final pooled set, tagged, once.** Pool all four subjects together with the campaign tag into
   `campaign/results/` (as 9.5 keeps `campaign/results/pool-<app>.json`). `pool_runs.py` does not pass `--tag`;
   run `desktop/pool.py <artifacts> <out.json> --md <out.md> --cpu-model "EPYC 7763" --tag meas-ci:desktop:2026-09-20`
   over the artifacts `pool_runs.py desktop/<app> --since 21` downloads under `~/.cache/meas-loop/pool/`.
2. **Each entry's row in `_dev/research/jioh/measurement-campaign-record.md`** — repeats, the values on the list and
   the widest half-width, what stopped it, jobs and gated draws; the excepted values with their half-widths.
3. **The raw-record release** — outward-facing: ask 인지오 first.
4. **The fold-in**, with scope-card items 6–10 and 15–16. Each entry's scope states: the exceptions and their
   half-widths and ranges (D17, D18, D21, D23), the within/between-run spreads (D20, D22), the renderer population
   (12 measured of 16 observed), the floor clause and `--no-sandbox` (§7), and that the renderer entries are
   majority `HangWatcher` (D16). Still open for the fold-in: the renderer wake alignment (D15) does not reach the
   rule — its unit is the repeat — but the scope's sample-count statement and, for 9.10, waking N placed hidden
   renderers together remain.

**Watch:** `probe/appdefs.sh` is shared with 9.5's live campaign and holds the two Chrome arms. Before any further
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
  and `~/.cache/meas-loop/probe-9.8/`, and are re-downloadable: `pool_runs.py` fetches every landed repeat from run 21 on.
- **The trigger carries five keys only** — `mode`, `attempt`, `cpu_model`, `apps`, `repeats`. Every design
  value is a constant in `run.sh` (D13); to change one, edit `run.sh` and bump `attempt` in the same push.
- **The branch is shared with other live sessions.** Push immediately after each commit.
- CI does not run on this branch. `make -C dataset test PY=python3.12`, about 8 minutes, currently 186 passed,
  1 skipped, 1 xfailed.
- Job lengths in `full`: about 23 minutes for the two renderer subjects and the chat client, about 42 for the
  Steam client. The EPYC 7763 draw rate has run near 40–50 %, so budget about two draws per landing.
- **Archives are written only when 인지오 explicitly asks.** Decisions go to the slice changelog.
