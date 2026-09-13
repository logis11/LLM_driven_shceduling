# Task 9.4 — Gaming: scope card

Stage 1 of `_dev/research/jioh/research-slice-workflow.md`. Archetype: `game-task-chain` (`dataset/archetypes.yaml:339–405`). Repository state: `db19cd1` on `jioh/dataset-rebuild`. Drawn from `../2026-09-13-verification/claims.md` (C-lavd-1…20, Part 2(a) rows 28–38), `compare/K2.md`, `reads/R02-lavd.md`, `compiled-numbers-report.md`, and `docs/memos/2026-09-13-critical-findings.md` (A2, B1, the wineserver item).

Verdict vocabulary is K2's: SUPPORTED / WORDING-FIX / MISATTRIBUTED / NOT IN SOURCE / OURS-UNDER-SOURCE-TAG. Kind is decision 1's labelling: source claim / convention / arithmetic / placeholder / design.

## Boundary

**In 9.4**

- Every `params` entry of `game-task-chain`, its `pattern`, `scalable` rule, `validation_stats`, `modeling_notes`, `category_source`.
- Wineserver's place: the binding note in `system-daemon.modeling_notes` (`archetypes.yaml:513–516`) and the interpretation-contract §6 open item, since the question is whether wineserver is a member of the constructed graph.
- The lines of the `lavd-ossna24` registry entry (`dataset/sources.yaml:49–64`, `docs/references.md:168–172`) that describe archetype values.

**Out of 9.4**

- To 9.10 (timelines): the gaming task sets (`steam`, `steamwebhelper ×3`, `gamescope`, `discord`), the C2 download pair and `steam-downloads`, the S5/S9/S10 scenario rows, C-lavd-16 (companion apps), process names and their distro availability (`game.exe`, plain `wineserver`, `gamescope`), and the number of game tasks a timeline carries once `n_tasks` leaves the archetype.
- To the slice owning `video-playback`: the `gamescope → video-playback` approximation.
- To 9.9 (daemons): `system-daemon`'s own values.
- To 9.12 (prose): C-lavd-18, C-lavd-20, C-corbet-1's tier and citation-form findings; `grounding-sources.md:30, :74`.
- To 9.14: `prior.yaml:191` (EDF justification on the 16.7 ms period), the guard spec's `tick_count` chain check, the RQ0 gate spec's 831 µs and 1 470 µs lines.
- To 9.15: `coreset-guide.md:186–193, :291, :513`, `data-contracts.md:235`, `interpretation-contract.md:58, :62, :66`, `archetype-plan.md:61, :76`, `building-plan.md:59, :167`, `source-vetting.md`.
- `gamemode-docs`: grounds scenario claims only (S9, wanted/unwanted); no archetype value cites it. Not in 9.4.

## Items

### Parameters

| # | Param | Current value | Tag | Verdict (K2) | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 1 | `n_tasks` | constant 300 | `s12` | WORDING-FIX — slide 12's "around 300 tasks are scheduled while running a game" counts every scheduled task including the system tasks; game, machine, trace length unnamed | count held as a parameter, against `archetypes.yaml:24` and `archetype-plan.md:27` | constructor expands 300 tasks, all named `game.exe` (`compiler.py:311, 327, 340`) |
| 2 | `frac_long_lived` | constant 0.90 | `s12` | SUPPORTED ("around 90% are long-living tasks; only 10% of tasks are terminated") | source claim | read by no tool; compiled workload is 100 % segment-bound |
| 3 | `per_schedule_run` | lognormal, anchors 260 / 1 650 µs, per-task | `s13` | OURS-UNDER-SOURCE-TAG — 260 µs (wineserver) and 1.65 ms (a task worker) are two named examples, not range endpoints; lognormal family and the p05/p95 reading are ours; the slide-13 plot (≈128 tasks, one game) has median ≈0.04 ms and 260 µs near its 90th percentile; 1.65 ms exceeds the plot's maximum | source values under our distribution | median 655 µs, σ_log 0.562; 16 draws ≈10.5 ms; `-single` rescales the sum to `lane_share × frame_period` (`compiler.py:319–322`) |
| 4 | `frac_wakeups_from_wait` | uniform 0.70–0.75 | `s14` | bounds SUPPORTED; uniform is ours (borderline) | source claim under our distribution | read by no tool |
| 5 | `frame_period` | constant 16 667 µs | `lavd-ossna24`, no locator | NOT IN SOURCE — no slide states a frame budget, period or 60 FPS target; slide 27's "targeted latency (e.g., 15 msec)" is a scheduler time-slice window; the talk's benchmark ran uncapped at 33–41 average FPS with refresh rate 60 | arithmetic (1/60 s), no source | chain head TIMER (`compiler.py:329`); lane-scaling denominator (`:321`); per-member demand estimate (`:335`); the `game.chain.1` miss-rate period; the driver table's EDF reason |
| 6 | `chain_length` | constant 16 | `lavd-ossna24`, no locator | OURS-UNDER-SOURCE-TAG (borderline) — a point inside slide 12's "15-20 game-specific tasks"; "frame-critical band" is our term | design within a source range | chain of 16 members (`compiler.py:312`) |
| 7 | `tail_idle_gap` | lognormal median 500 000 µs, σ 0.5, per-task | `s12` | OURS-UNDER-SOURCE-TAG — placeholder by the entry's own note; the "mostly waiting" tail is NOT IN SOURCE (slide 12 implies only that the remaining tasks share ~5 % of scheduling; slide 17 says "majority of game tasks shows periodic behavior") | placeholder under a source tag | 284 tail tasks: `LOOP { SLEEP ≈0.5 s → RUN ≈200 µs }` (`compiler.py:338–349`); tails ≈0.155 lanes in c1-gaming |
| 8 | `tail_run` | lognormal median 200 µs, σ 0.5, per-task | `s12` | as 7 | placeholder under a source tag | as 7 |

### Structure

| # | Item | Current | Verdict (K2) | Kind today |
|---|---|---|---|---|
| 9 | `constructor: chain` — one linear relay of `chain_length` members, WAIT/WAKE | notes declare the linearisation ours | SUPPORTED as declared; the source's slide-16 graph is fan-in (four `Task worker thr` → `dxvk-cs`), a two-step chain (`dxvk-cs` → `dxvk-submit`), 2-cycles among `winepulse_*`/`pipewire*`, and slide 11 a hub around `wineserver`; slide 17 says most game tasks are individually periodic with "a stable execution time and a stable wait time" | design, disclosed |
| 10 | Head-only TIMER; stage names "input → engine → … → display" | `modeling_notes`, `interpretation-contract.md:62` | premise NOT IN SOURCE for named stages (slide 17 names only "a user input" and "display update" as an e.g.) | design; "engine" is ours |
| 11 | The 16 : 284 split | 16 chain + 284 tail | the source's split is top 30–40 (about half "system tasks — especially wine, graphics, and audio servers", 15–20 game-specific) vs the remaining ~260–270 | design |
| 12 | `scalable` rule and its "lane-scaling defense" | cites the concentration statistics (C-lavd-10, C-lavd-11) and "measured on multi-core machines" (C-lavd-15) | statistics SUPPORTED (a scheduling-frequency share, not CPU time; that it justifies scaling RUN is our inference); C-lavd-15 NOT IN SOURCE — no slide states the machine, core count or OS of the characterisation traces | design on a partly unsupported premise |
| 13 | `validation_stats: referee: none`, reason "circular" | — | design statement | design |
| 14 | `category_source: lavd-ossna24` | Tier-1 provenance claim | talk slides, footnote tier by the registry's own words | source claim (form) |
| 15 | `modeling_notes` wording | "frame-critical band"; "mostly waiting"; wine linkage tagged `s12` | WORDING-FIX; NOT IN SOURCE; MISATTRIBUTED (linkage is on slides 11, 16, 24; slide 12 files wine under system tasks) | — |

### Binding on the line

| # | Item | Current | Verdict (K2) | Compiled effect |
|---|---|---|---|---|
| 16 | Wineserver's place | `wineserver → system-daemon`, "provisional approximation" (`archetypes.yaml:513–516`, `archetype-plan.md:76`), decision deferred to constructor implementation | MISATTRIBUTED locator (`s12`); slide 13 names wineserver as a 260 µs coordination task; slide 11 shows it as the hub of `redDispatcher1–7` and `wine_xinput_hid` (pipe_read / epoll) | one `system-daemon` draw: SLEEP 1 225 s in c1/c4/c7-gaming, never runs in 60 s; 56 runs in 120 s in c2-p2a/p2b |

### Registry lines describing archetype values

| # | Location | Text | Verdict (K2) |
|---|---|---|---|
| 17 | `sources.yaml:53` | "~300 tasks per game" | WORDING-FIX |
| 18 | `sources.yaml:59`, `references.md:170` | "16.7 ms frame budget, 15 ms targeted latency" | NOT IN SOURCE (frame budget); targeted latency is a time-slice window |
| 19 | `references.md:170` | "per-schedule runtimes ~260 µs–1.65 ms" | WORDING-FIX (examples presented as a range) |
| 20 | `references.md:170` | "70–75% wakeups from waiting syscalls" | WORDING-FIX (unit is scheduling events) |
| 21 | `references.md:170, :175` | `corbet-lwn24` as "prose-citable secondary" for the numbers | WORDING-FIX — the LWN section is qualitative only and its "typically no more than 100µs" differs from slide 13 |

## What the source is, as one observation

`lavd-ossna24` is 30 talk slides. Its numbers on slides 12–14 come from an unnamed game on an unnamed machine; the trace figures use task IDs that differ between slides (wineserver `[5789/0]` on slide 11, `[3845/0]` on slide 15; the slide-16 graph uses group 7781), so the slides appear to draw on more than one trace, and they do not say how many. The slide-13 plot covers ≈128 tasks against the "around 300" of slide 12. Under decision 2 the deck counts as one source, but whether its figures are one observation is not established.

Local copy: `../2026-09-13-verification/sources/lavd-ossna24/` (PDF, SHA-256 e62d69cd…6402475; text layer; 30 page renders; hires crops of slides 11, 13, 14, 16, 29).

## Stage 2 topics

Neutral form, for the readers. Each is searched in the four classes of phase decision 4.

- **T1 Frame cadence.** For a game running through Proton on a Linux desktop or Steam Deck: what governs the frame period (display refresh, frame limiter, uncapped), what values are documented or observed, and whether any observation ties the frame cadence to the game's task wake structure.
- **T2 Task structure.** Any observation (trace, dataset, paper, tool output) of a Linux game's process and thread population: counts, which threads are the game's and which are Wine/DXVK/audio components, how they wake one another, and per-schedule runtime distributions. Includes the roles of `wineserver`, `dxvk-cs`, `dxvk-submit`, `winepulse_*` as their projects document them.
- **T3 Non-dominant tasks.** Any observation of what the tasks outside the most frequently scheduled set do (periodic, sleeping, terminated), with numbers.
- **T4 Lifetime and termination.** Any observation of how many of a game's tasks terminate during play and over what window.
- **T5 Platform of the LAVD characterisation.** Whether any document (later talks, LWN 1051430, scx repository, the "Lessons from creating a gaming-oriented scheduler" item named in `references.md:175`) states the machine, core count or game behind slides 12–14.
- **T6 CI observability.** Whether a GitHub Actions runner can run a game at all: an open-source native Linux game under Xvfb with software rendering, or Proton without a GPU; what a `/proc` sidecar could observe of it (thread population, wake gaps, per-schedule CPU), and what it cannot (the Proton/Wine structure, real frame cadence).

## Compiled numbers the decisions move

From `compiled-numbers-report.md`: c1-gaming demand 1.4557 lanes (chain 0.8999, compositor 0.4000, tails 0.1549, webhelpers 0.0008, steam 0.0001, wineserver 0.0000); `-single` and `-native` differ only in the 16 chain members' RUNs; chains in `-single`: c1/c4/c7-gaming sum 14 999 µs, slack 1 668, longest stage 1 470; c2-p2a/b sum 15 836, slack 831, longest 2 176. These are 9.14's inputs once 9.4's values land.
