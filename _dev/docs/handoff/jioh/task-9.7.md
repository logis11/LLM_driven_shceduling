# Handoff — task 9.7 Background and IO (2026-09-22, ~08:00 KST)

Branch `jioh/dataset-rebuild` (Phase 9 works on this branch only, `_dev/` included). Campaign tag `meas-ci:background:2026-09-19`.

## Where 9.7 stands

| archetype | program | state |
|---|---|---|
| `file-backup` | `borg` | **done** — rule holds over 30 valid repeats |
| `file-archiver` | `7z` | **done** — rule holds over 6 repeats |
| `game-download` | SteamCMD | **22 repeats landed, all downloaded; the pool at 22 has not run to completion** |

## SteamCMD campaign — status

- Repeats 1–22 all landed on the EPYC 7763 (runs #47–#54). At 12 repeats (runs 47–52, all valid) the rule did not hold: run per wake ±3.79 % holds; network wait ±7.48 % and bytes per wake ±6.44 % do not; the pool projected 22. Repeat 13 was added alone, 14–22 as one batch (D26). All artifacts are in `~/.cache/meas-loop/pool/background-steamcmd-from47`.
- **The pool at 22 never finished.** It ran 12 hours (2026-09-21 19:38 → 09-22 07:45 KST) swapping, and was stopped along with the two loops (`campaign_loop.sh`, `rule_loop.sh` in `~/.cache/meas-loop/overnight-9.7/`). Cause: `dataset/tools/meas/background/pool.py` analyses every phase of every repeat first and keeps every raw sample (Python lists) in memory until it pools; at 22 repeats that exceeds the Mac's 16 GB (swap 12.3 of 13.3 GB). The 12-repeat pool already swapped (3 h instead of ~2).
- **A fix is written but NOT verified and NOT committed** — `dataset/tools/meas/background/pool.py` is modified in the working tree (backup: `~/.cache/meas-loop/overnight-9.7/pool-fix/pool.py.fixed`, diff `pool-memory-fix.patch`). It must give byte-identical output to the committed version before it is used. What it does: each repeat's phase is analysed once and cached beside the repeat in `pool-cache/` (results as JSON, samples as float64 arrays per thread; "all" is rebuilt as the concatenation of the threads', as `analyze.py` builds it), keyed by a hash of the analysis code (`analyze.py`, `nettrace.py`, `build/analyze.py`, `stability.py`) and `CACHE_VERSION`; pooling loads one table at a time, sorts it once, releases it; `--jobs N` fills the cache in parallel. No number is meant to change.

## Next actions, in order

1. `git pull` first — 9.5, 9.6 and 9.8 all push to this branch (9.8 had uncommitted changes in the shared tree on 09-22).
2. **Verify the fix.** `~/.cache/meas-loop/overnight-9.7/pool-fix/make_inputs.sh` rebuilds the inputs (the six 7-Zip repeats and SteamCMD repeats 1–2, as symlinks); `regress.sh` runs the committed `pool.py` (`pool_old.py`, the HEAD copy) and the fixed one twice (cache cold, then warm) and `cmp`s the JSON, `results.md` and printed rule. Budget about an hour — the old version on two SteamCMD repeats is the slow part. All three must be IDENTICAL for both apps; if anything differs, find why before using it. A partial run was stopped on 09-22; some `pool-cache/` folders may already exist under the 7-Zip and SteamCMD pools — they are valid only for the same code hash, and the fix rebuilds them otherwise.
3. **Commit the fix** (`feat(jioh/phase-9): …`) once identical.
4. **Pool the 22 repeats:** `pool_runs.py background/steamcmd --since 47 -- --tag meas-ci:background:2026-09-19 --jobs 2`. The first run builds every repeat's cache (a few hours); later pools only analyse new repeats.
5. **Rule holds** → SteamCMD is done → fold-in. **Does not** → one repeat at a time from 23 (D26): `launch.py added background/steamcmd:23`, watch it (`watch.py background/steamcmd --since <run>`, relaunches if gated), pool, evaluate, repeat — no ceiling (인지오, 2026-09-20). With the cache, each cycle is about an hour. `rule_loop.sh` in `~/.cache/meas-loop/overnight-9.7/` automates this; before reusing it, change its pool call to pass `--jobs`.

## Decisions taken (9.7 changelog unless marked)

- **D24** — the shaped link's queue discipline tested before the campaign, bar fixed at a cross-runner cv of 8 %. The connection count can be pinned (six hosts on 4 of 4 runners) but pinning does not make the values repeatable.
- **D25** — the campaign shapes with an `htb` root at D11's 121.0 Mbps and an `fq_codel` leaf (kernel defaults); the connection count is not pinned; `game-download`'s scope carries the sensitivity sentence on 9.5 D23's pattern: against the committed token bucket, network wait +43 %, bytes per wake +35 %, run per wake +17 %. Its five-repeat projection (from three diagnostic draws) proved about fourfold too optimistic; the discipline decision itself stands (the bucket projected 65 repeats where the leaf projects about 22).
- **D26** — SteamCMD's added repeats: 6–12 and 14–22 as batches, 22 being the pool's projection at 12; past 22, one at a time.
- **9.5 D49** — the `send` attachment is the same size every repeat, not the same bytes; `appdefs.sh` records the `.docx` member listing.
- Citation `fqcodel-rfc18` (RFC 8290, Experimental) in `docs/references.md`, for the discipline's stated purpose only.

## Findings to carry into the fold-in (not yet written anywhere)

- **The spread left under `fq_codel` follows the runner's region.** Over repeats 1–12, network wait by the Steam site the runner was sent to: west (sea1, lax1, lax2) 199 µs, central (ord1) 221 µs, east (iad1, atl3) 249 µs — 81 % of network wait's variance and 82 % of bytes per wake's lies between these groups (run per wake 31 %). The connection count no longer matters (6 → 221, 8 → 235, 9 → 197, 10 → 229 µs). The runner's region is not recorded — the Steam site is a proxy. 인지오 decided **not** to filter on region (no other campaign measures across the internet; more repeats converge); `game-download`'s scope should state the region split of its repeats.
- All 12 pooled repeats ran the `fq_codel` leaf (`shape.variant=aqm`, `htb` + `fq_codel` in every shaped phase). Full mode does not write `shape.<phase>.discipline` — only `shapediag` does; cosmetic.

## Stated with the values, do not drop

`fq_codel` removes the connection-count spread by construction — CoDel holds queue delay at its 5 ms target. No source here establishes that consumer equipment manages its queue this way, so the emulated link is design, not population-representative. Its delay is the runner's own path to Valve's servers, neither controlled nor recorded (D10's stated limitation).

## Traps

- A gated job exits in seconds and still reports **success** — read `report.json`'s `gate` and `machine.model`, never the status alone.
- The trigger `.github/campaign-background.json` is in `full` mode, `steam_diag_setting` empty. A push changing it starts the runs it names.
- Loops under `nohup caffeinate -i` do not survive the Mac sleeping or powering off.
- `launch.py` pulls with `--autostash`; the shared tree has been caught mid-rebase by a peer before — `rule_loop.sh` waits if `.git/rebase-merge` exists.

## Open items

- **RTT recording — held by 인지오** (D25 "not taken"). The region finding above now points at the path; the cheap step, when wanted, is TCP connect time to each content host after `shape_off`, outside the traced window.
- After the pool: fold-in (remove `io-stream`, `network-bulk`; add `file-backup`, `file-archiver`, `game-download`; rebind timelines; D17 registry changes) → hand-offs. `file-archiver`'s `modeling_notes` carry D23's two modes and the CPU-per-byte check; `game-download`'s carry D25's sensitivity sentence and the region split.
- borg's repeat 3 stays excluded in every borg pool (`--exclude 3 --exclude-why "the 10 GB set's fetch returned a 12,108 B file in place of the 3.70 GB archive (set.archive_pin mismatch, extract rc 2, 0 files), so the phases ran on an empty tree"`).
- Not 9.7's: 9.5's episode-count spread (flagged to 9.5); 9.10's question whether the desktop client downloads while a game runs (D4, D12). To check: whether 9.8's Steam client entry (9.8 D6, logged out) has measured values that include internet traffic, which would make them region-dependent too.

## Working with 인지오

One question per message, plain chat, no question popups. Say what every label, decision number and source id means in the same sentence. Recommendations rest on a verified reference or the records; don't substitute estimates for the method (the rule is on-line, one repeat at a time, unless 인지오 decides otherwise). Plain, literal English — say "filter", never "hold", for a gate. Never paraphrase their terms in docs; no chat-derived justification in docs; archives only on explicit request.
