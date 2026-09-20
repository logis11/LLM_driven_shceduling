# Handoff — task 9.7 Background and IO (2026-09-20, ~20:30 KST)

Branch `jioh/dataset-rebuild` (Phase 9 works on this branch only, `_dev/` included). Supersedes the 2026-09-19 handoff and `/tmp/handoff-9.7-steamcmd-operating-point-2026-09-20.md`, both stale. Campaign tag `meas-ci:background:2026-09-19`.

## Where 9.7 stands

| archetype | program | state |
|---|---|---|
| `file-backup` | `borg` | **done** — rule holds over 30 valid repeats |
| `file-archiver` | `7z` | **done** — rule holds over 6 repeats |
| `game-download` | SteamCMD | **method settled (D24, D25); first batch of 5 landed; pooling in flight** |

Read the committed results rather than re-deriving: `…/task-9.7-background-io/campaign/results-borg.md`, `results-7z.md`, `campaign/results/{borg,7z}-pooled.json`, and the 9.7 section of `_dev/research/jioh/measurement-campaign-record.md`.

## In flight

`pool_runs.py background/steamcmd --since 47 -- --tag meas-ci:background:2026-09-19`, started 19:42 KST. Artifacts are already downloaded to `~/.cache/meas-loop/pool/background-steamcmd-from47` (2.4 GB), so a re-run skips the download and goes straight to pooling. All five repeats landed (2,716–2,944 s): repeats 1, 2, 5 on run #47 `35502824537`, repeat 3 on #48 `35502868640`, repeat 4 on #49 `35503071794`.

**When it finishes:** read the validity lines first (gate on the EPYC 7763, every phase present, every SteamCMD phase reporting its install complete, one app build across repeats, every non-zero rc explained); then the rule on the three carried values of `steam-fresh-shaped` — run per wake, network wait, bytes per wake. D25 projects that five repeats suffice, but that projection came from three runner draws of the diagnostic, not from campaign repeats. Rule holds → fold-in. Does not hold → add repeats one at a time (no ceiling), relaunching gated indices.

## Decisions taken this session

- **D24** (`…/task-9.7-background-io/changelog.md`) — the shaped link's queue discipline tested before the campaign, the bar fixed beforehand at a cross-runner cv of 8 % on network wait and bytes per wake. Records what the connection-count diagnostic established: the count **can** be pinned (`@cMaxInitialDownloadSources 5 @cDefaultInitialDownloadSources 5 @fDownloadRateImprovementToAddAnotherConnection 99`, read back on 4 of 4 runners, six content hosts on each against 9/6/6/8 unpinned) and pinning does **not** make the values repeatable (pinned cv 22.5 % network wait, 19.1 % bytes per wake; 78 and 57 repeats projected).
- **D25** — the campaign shapes with an `htb` root at D11's unchanged 121.0 Mbps and an `fq_codel` leaf (kernel defaults, recorded per phase as `shape.<phase>.discipline`); the connection count is **not** pinned; `game-download`'s scope carries a link-model sensitivity sentence on 9.5 D23's pattern. Result over three runner draws: `fq_codel` network wait cv **1.9 %**, bytes per wake cv **1.6 %**, run per wake cv 4.4 % (5, 5 and 6 repeats) against the bucket's 20.5 %/18.1 %/8.9 % (65, 51, 15). The leaf is nearly insensitive to the connection count (+3.6 % from 6 to 9 servers, against +51 % from 6 to 10 under the bucket) and gives up no throughput (payload 115.4–115.9 Mbps, wall 760.8–783.1 s over all nine downloads).
- **Sensitivity to carry in `game-download`'s scope**: against the committed token bucket, network wait is 43 % higher (329.3 µs), bytes per wake 35 % higher (5,509 B), run per wake 17 % higher (185.5 µs).
- **9.5 D49** (`…/task-9.5-interactive-typing/changelog.md`) — the `send` attachment is the same size in every repeat and not the same bytes (43 repeats, `doc.bytes` 41,555,063 and `doc.pictures` 10 in all, 43 distinct `doc.sha256`); D31's 41,555,035 B is a container build, the runner's is 41,555,063 B; `appdefs.sh` now records the `.docx`'s member listing to `$OUT/doc.zip.txt` with `doc.crc_sha256`. 9.5's `thunderbird-send` pool is closed at 43 valid repeats.
- New citation `fqcodel-rfc18` in `docs/references.md` (RFC 8290, Experimental), cited for the discipline's stated purpose only — never for any consumer link's loss rate.

## Stated with the values, do not drop

`fq_codel` removes the spread **by construction**: CoDel holds queue delay at its target (5 ms as installed), so the per-wake pattern follows that setpoint rather than the runner's path. No source here establishes that consumer equipment manages its queue this way, so the emulated link is design, not population-representative. Its **delay is still the runner's own path to Valve's servers**, neither controlled nor recorded (D10's stated limitation).

## Traps

- **The trigger is in `full` mode** with `steam_diag_setting` empty (`.github/campaign-background.json`, attempt 47). A push changing that file starts the runs it names; nothing else does.
- **Machine gating ran hot today** — EPYC 9V74, 9V45 and Xeon 6973P-C draws; at one point six of seven draws were gated. A gated job exits in seconds and still reports **success**, so never read a status alone: check `report.json`'s `gate` and `machine.model`. Relaunch loop script (session-scoped, rewrite if needed): `campaign-relaunch.sh <since> "<indices>" <cycles>` in the session scratchpad; it relaunches a first batch's gated indices together in one push.
- **Shared tree.** 9.5, 9.6, 9.8 all push to this branch; one left an interactive rebase mid-conflict in `_dev/TODO.md` this morning. Pull first; stage only your own paths; `launch.py` pulls with `--autostash`.
- SteamCMD pools take ~45 min for five repeats (download plus per-phase analysis).

## Open items

- **RTT recording — held by 인지오.** D24's residual at a fixed connection count (drops 2.98–5.60 %, network wait ordering identically across four sites) is unattributed; round-trip time is a hypothesis and nothing measures it. Recorded in D25's "not taken". The cheap step, when wanted: measure TCP connect time to each content host after `shape_off`, outside the traced window.
- After the pool: fold-in (remove `io-stream`, `network-bulk`; add `file-backup`, `file-archiver`, `game-download`; rebind timelines; D17 registry changes) → hand-offs. `file-archiver`'s `modeling_notes` carry D23's two modes and the CPU-per-byte check; `file-backup`'s carry nothing new; `game-download`'s carry D25's sensitivity sentence.
- borg's repeat 3 stays excluded in every borg pool (`--exclude 3 --exclude-why "the 10 GB set's fetch returned a 12,108 B file in place of the 3.70 GB archive (set.archive_pin mismatch, extract rc 2, 0 files), so the phases ran on an empty tree"`).
- Belongs to 9.5, flagged to them, not written here: the episode-count spread (6–9 episodes per 600 s window against 10 cycles) that took `thunderbird-send`'s rule to 43 repeats rather than the projected 29.
- Belongs to 9.10 (D4, D12): whether the desktop client downloads while a game runs — c2-p2a's premise — rests on Valve pages not read.

## Working with 인지오

One question per message, plain chat, no question popups. Say what every label, decision number and source id means in the same sentence. Recommendations rest on a verified reference or the records — say so when a number has none. Never paraphrase their terms in docs; no chat-derived justification in docs; archives only on explicit request.
