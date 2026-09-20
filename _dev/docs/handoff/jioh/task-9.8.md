# Handoff — task 9.8 Browser and comms (2026-09-20)

Stage 3 of `_dev/research/jioh/research-slice-workflow.md` is under way on `jioh/dataset-rebuild`: **D1–D12 landed, campaign method written, tooling not started.** Next session: build the tooling, then run the campaign.

## What is decided

`electron-comms` — one entry carrying **125 coreset tasks** on two values the measurement audit classed X, the geometric centre between an unauthenticated Element's main process and its helpers, matching no process that was observed — is replaced by four measured entries. Every binding has a destination.

| Entry | Measured on | Takes |
|---|---|---|
| idle **hidden** renderer | Google Chrome, N site-locked origins backgrounded past the intensive-throttling grace | background-tab renderer tasks |
| idle **visible** renderer | the same page set, page still visible to Blink | `steamwebhelper` ×9, renderer tasks a timeline says are in front |
| Electron **chat client** | Element against Synapse on the harness, idle phase carried | `discord` ×3 |
| **Steam** desktop client | the client under Xvfb, logged out | `steam` ×6 |

`thunderbird` ×3 rebinds to `mail-client` (identity binding, closing its three-way split with 9.7 D3); the `zoom` helper ×2 is retired; the Discord `injected-overlay` role is withdrawn.

Four decisions rest on checks made this session rather than on the stage-2 record: cross-application window occlusion is Windows-only, so a covered renderer is never throttled and the visible state is terminal (D4); Steam ships its own `CMsgWasHidden` and a `background_throttling_disabled` field, so it controls throttling itself (D5); Discord's overlay is Windows-only by Discord's own support article (D7); and the Steam Subscriber Agreement forecloses any account use (D6).

## Next, in order

1. **Tooling** — `dataset/tools/meas/desktop/` (`run.sh`, `analyze.py`, `pool.py`), `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, loop family `desktop` in `loop/common.py`. `meas-gui.yml` retires with the entry, as 9.7 retired `meas-cli.yml`.
2. **Long-phase probe** (`long-probe` family) — sets each subject's phase length and N together, and shows whether throttled wakes coincide across renderers. Written into `campaign/method.md` §10 before the first batch.
3. **Dry run** — also settles whether the Steam client holds a stable state logged out; if it does not, D6's fallback retires that binding instead.
4. **First batch** — five repeats per subject, then one at a time under the stability rule.
5. **Pool → fold-in → hand-offs**, then scope-card items 6–10 and 15–16.

## Open threads

- **Phase lengths and N** trade against each other for sample count and both come from the probe. At one wake per minute a short phase gives too few wakes for a quantile table or for the half-width to converge (D10).
- **D5's probe question** — which CEF mode Steam uses, which switches it passes, and whether the helper's wakes change when the window is minimised. Read from `/proc/<pid>/cmdline` in the Steam job; its result replaces D5's inference if it lands before the fold-in.
- **The visible renderer's values depend on the stated page** and nothing throttles them; the hidden entry is protected by the cap, the visible one is not. Stated in its scope, not solved.

## Hands to other tasks

- **9.7** — D4's escape clause ("it runs only if 인지오 provides an account") is foreclosed and should be withdrawn; its "terms unchecked" parenthetical is now checked. No 9.7 value changes: its campaign uses `+login anonymous` throughout. This slice's Steam job also supplies the desktop client's process tree, which D4's binding note currently asserts without an observation.
- **9.10** — every `electron-comms` binding rebinds; the `injected-overlay` role goes; the meeting files lose the helper task; renderer counts are counts of *sites*, not tabs; a timeline binding a renderer states which of the two states it depicts; a just-switched-away tab is not covered by either entry.
- **9.13** — the four entries' fields follow the component form at the rebuild.

## Where things are

Changelog `_dev/research/jioh/task-9.8-browser-comms/changelog.md`; method `…/campaign/method.md`; search-log amendments in `…/search/S1-literature.md` §4, `S2-project-docs.md` §4–§5, `S3-traces-datasets.md` §4. Source copies under `…/sources/A-2026-09-20/` (gitignored, local to this clone).
