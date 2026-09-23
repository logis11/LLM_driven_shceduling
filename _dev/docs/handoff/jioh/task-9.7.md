# Handoff — task 9.7 Background and IO (2026-09-23, ~13:10 KST)

Branch `jioh/dataset-rebuild` (Phase 9 works on this branch only, `_dev/` included). Campaign tag `meas-ci:background:2026-09-19`.

## Where 9.7 stands

The campaign is closed and folded in. Only the raw-record release is unfinished.

| archetype | program | repeats | state |
|---|---|---|---|
| `file-backup` | `borg` | 30 valid of 31 landed | folded in (D31) |
| `file-archiver` | `7z` | 6 of 6 | folded in (D31) |
| `game-download` | `steamcmd` | 30 valid of 34 landed | folded in (D34) |

- `io-stream` is gone; `network-bulk` stays, bound only by the three `thunderbird` send tasks (D30).
- `interbench` and `ananicy-rules` left `dataset/sources.yaml`; `meas-ci`'s notes rewritten (D17).
- Rebuild verified: 100 artifacts, every file's demand estimate and class unchanged, lint reporting only the branch's five known `-single` demand-window files, derived files and grid checked, tests passing over every area this touched.

## In flight

**The release upload**, tmux session `meas97upload`, log `~/.cache/meas-loop/overnight-9.7/upload_release.log`. The release exists (`meas-ci-background-2026-09-19`); the script zips each landed repeat without the local `pool-cache/`, uploads it, deletes the zip, and skips assets already on the release — re-run `~/.cache/meas-loop/overnight-9.7/upload_release.sh` to resume after any interruption. Expect 71 repeat archives plus `gated-reports.zip`, about 11.3 GB, SteamCMD's 34 at ~490 MB each being the bulk. When it ends, check `UPLOAD DONE` in the log and the asset count, then tick 9.7's release sub-item in `_dev/TODO.md`.

## Next actions, in order

1. Confirm the upload finished and the release holds every archive.
2. Tick the release sub-item; 9.7 is then complete. Phase 9 stays `[WIP]` — 9.5, 9.8, 9.9 and 9.10–9.16 remain.

## Decisions taken since the last handoff (9.7 changelog)

- **D27** — SteamCMD's repeat 21 left out: its runner had no accelerated-networking VF, so the redirect sat on `eth0`'s clsact hook behind the runner's direct-action BPF program and 490 B of 10.5 GB went through `ifb0`; the shaped phases ran unshaped. Repeat 23 is not pooled: it was wrongly launched on the pool that still held 21. Tooling: a `gate=no-vf` network gate in `background/run.sh`, relaunched by `watch.py` like a machine-gate stop, and a validity check that flags any shaped phase whose `ifb0` bytes are under 90 % of the bytes received. The gate stopped 7 runners over the rest of the campaign.
- **D28** — `game-download`'s thread encoding: one task, one component, the process pooled (D22's form for `file-archiver`).
- **D29** — all three archetypes compile as `cpu-batch`'s `batch-loop`, carrying the program's runs between voluntary blocks and the block after each run; the per-wake tables are reported, not carried. A run-then-wait sequence of the per-wake tables reproduces `borg` but not the multi-threaded programs, whose pooled waits include their siblings' runs.
- **D30** — `network-bulk` stays for the three `thunderbird` send tasks until 9.5's `send` folds into `mail-client` and 9.10 places it; it leaves before 9.13.
- **D31** — the fold-in's first part: `file-backup` and `file-archiver` replace `io-stream`; registry lines and the compiler's single-table-set `batch-loop`.
- **D32, D33** — SteamCMD's repeats 32 and 33 fail the validity step and are left out (32's untraced and unshaped phases did not complete, `FAILED (No Connection)`; 33's unshaped `perf.data` is truncated, its timehist report exiting 242). Both measured phases were complete; the pre-registered step decides, and in both cases the excluded repeat would have tipped the borderline block per run over its 1 µs floor.
- **D34** — the fold-in's second part: `game-download` enters at 30 valid repeats and the c2-p2a download rebinds.

## Carried into the entries (do not drop)

- `game-download`'s scope states the region split: 14 west, 13 east, 3 central by the Steam site the runner drew, the region holding 64 % of the variance of network wait and 45 % of the block per run; the runner's path to Valve is neither controlled nor recorded.
- `game-download`'s notes carry D25's link-model sensitivity — against the committed token bucket, network wait +43 %, bytes per wake +35 %, run per wake +17 % — and D4's binding note for `steam`.
- `file-archiver`'s notes carry D22's flattening, D23's two modes and the thread check (eight threads cost 1.04–1.10 times the CPU per byte of one).

## Open items

- **The block per run is a marginal value.** It has sat between ±10.4 % and ±12.5 % against its 1 µs floor for a dozen repeats, its spread partly the runner's region. Whether it belongs under the rule's machine-spread exception (9.6 D29) was never put to 인지오.
- **The unshaped phase's `perf.data` truncation is undiagnosed** (repeat 33). That phase downloads at ~770 Mbps and writes the largest `perf.data` of the three.
- Not 9.7's: 9.5's `send` re-observation and 9.10's placement of the send tasks, which release `network-bulk`.

## Traps

- A gated job exits in seconds and still reports **success** — read `report.json`'s `gate` and `machine.model`, never the status alone.
- The trigger `.github/campaign-background.json` is in `full` mode. A push changing it starts the runs it names.
- **Loops must run under tmux**, not `nohup … & disown`: the harness kills the session's process tree, which killed the rule loop mid-pool on 2026-09-23.
- `launch.py` pulls with `--autostash`; the shared tree has been caught mid-rebase by a peer.

## Working with 인지오

One question per message, plain chat, no question popups. Say what every label, decision number and source id means in the same sentence. Recommendations rest on a verified reference or the records — and on the pre-registered step over the convenient reading: 인지오 rejected admitting a repeat that failed validity because its carried phase looked ordinary. Plain, literal English. Never paraphrase their terms in docs; no chat-derived justification in docs; archives only on explicit request.
