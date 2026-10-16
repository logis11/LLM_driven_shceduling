# Archetype Library — Writing Plan
> Status: normative · Created 2026-08-25 · Updated 2026-10-17

> Expands §2 of docs/workload/building-plan.md, the archetype library, into a buildable specification for `dataset/archetypes.yaml`. Normative for the archetype library. Source ids reference `dataset/sources.yaml`; citations live in docs/references.md; execution semantics live in docs/simulator/interpretation-contract.md. Every value, scope and modeling note is the library's own; §4 names its entries.

## 1. What an archetype is

An archetype is a **generative model of one kind of program as the scheduler sees it**. To the scheduler a process has no name and no meaning — only an event stream: when it becomes runnable, how long it runs, what it blocks on, whom it wakes, when it forks and exits. An archetype is the rule-plus-parameters bundle that emits that stream: for most entries one task, a measured application's whole process tree merged into it; for `compiler-child` the six tasks of one object job; for `module-compiler-child` the members of one job's tree (an object job, a kbuild probe or a conftest test); for `game-task-chain` the members of the frame chain.

**Event grammar** (six primitives — semantics normative in interpretation-contract §3; rt-app cited as the schema precedent, including `timer{ref,period}` for TIMER):

```
RUN(duration)      burn CPU
SLEEP(duration)    voluntary relative wait
TIMER(period)      absolute periodic wake at t0+k·period — drift-free; periodic
                   tasks use TIMER, never SLEEP loops
WAIT(channel)      event wait (a timer component's wake, input, an upstream
                   chain member, a job member, an orchestrator's children)
WAKE(target)       make another task runnable
FORK / EXIT        consume next spawn-table entry / terminate
```

TIMER is the periodic entries' alone — the playback and call entries' medium cycles and the game chain's head. A measured application's own thread wakes are not periodic: each is a WAIT on the task's timer channel, woken at a time sampled from its measured gaps, with no deadline (9.5 D74).

**Defining an archetype is three steps:**
1. **Pattern selection** — transcribe the measured program's observed behaviour into the grammar: `audio-player`, mpv playing a track, becomes a TIMER/RUN loop at its measured 49,635 µs cycle; a measured application, one stream of its threads' timer wakes, its replayed keystrokes and its operations, merged at compile time; a batch job, a loop of its measured runs between voluntary blocks and the blocks after them.
2. **Parameter filling** — numbers enter as *distributions*, not point values: a measured table carried as observed (`dist: quantiles`, the ten pooled quantiles with the sample's extremes and each interval's mean, 9.5 D17), a lognormal between two anchors where a source gives only a span (`game-task-chain`'s per-schedule run), a constant where the quantity is one value (a cycle's period). Every numeric carries `source: <id>` or `<id>:<locator>`.
3. **Validation criterion** — an archetype's identity is not its code but the **statistics it must reproduce**, declared per entry in `validation_stats`: the referee, the campaign's run and repeats, the measured statistics, and the observation's scope. A measured entry's referee is its own campaign (`referee: meas-ci`); the compiled library keeps each measured table's quantiles and mean, and every measured entry compiles at the wake rate it carries (`dataset/tools/tests/test_measured_fidelity.py`). The `replay` sensitivity variants compile four judging files from one pooled repeat's observed stream — wakes, runs and the block after each, or cycles, as the entry compiles — in place of the sampled one (`dataset/variants.yaml`), so a verdict can be compared across the two. `game-task-chain` has no referee (`referee: none`): validation against LAVD would be circular — LAVD is also the parameter source — and the runner cannot observe a Proton game, as the entry states.

**Boundary rules (two sentences):** what the scheduler cannot observe cannot live in an archetype — process *names* (bound in the timelines), *counts* (§3), and *meaning* (segment-label concerns) are excluded by construction. And a `source:` tag justifies the *values and described structure*, never the *field names* — field names are our schema's invention, and every entry whose shape leans on a source records that derivation in `modeling_notes` (§5).

## 2. Two-tier grounding of the inventory

**Tier 1 — existence of each archetype: grounded by measurement.** Each entry's `category_source:` names what grounds its existence. 28 of the library's 29 entries carry `meas`: a behaviour class observed in our measurement of a named program, its campaign named in the entry's `validation_stats` (`game-download-idle` shares `game-download`'s measured tables). One entry keeps a published characterization: `game-task-chain`, from the LAVD talk's figures (`lavd-ossna24`), a Proton game the runner cannot observe (no GPU; Proton runs only under the Steam client). The linter requires the field on every entry.

**Tier 2 — sufficiency of the set: closed by verification, not citation.** No universal taxonomy of process behavior exists, so completeness cannot be cited — and must not be claimed. The claim is weaker and falsifiable: **this inventory spans S1–S18** (§4, spanning check). The referee is the `meas-ci` campaign: if a CI-runnable scenario's measured statistics cannot be reproduced by any composition of the inventory, the inventory is insufficient and an entry is added. Each scenario the core set instances binds entries measured for its own programs, with two exceptions: the gaming scenario's frame chain (S9, `game-task-chain`), grounded in the LAVD talk's figures (Tier 1), and the download's `steam` (S10, `game-download`), which carries SteamCMD's numbers by stated approximation (§5).

**Observation venues.** The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation. The venues are two: the 28 measured entries, every value one AMD EPYC 7763 core of a GitHub-hosted runner (`category_source: meas`), and `game-task-chain`, from the `lavd-ossna24` talk's slides, lane-scaled. A scale bridge — one benchmark figure both machines report — may be written into scope as the ratio, never applied to a value. The sensitivity check is the venue variants `venue-x0.8` and `venue-x1.25` (`dataset/variants.yaml`; 9.14 decision 12): every RUN but the frame chain's scaled by 0.8 and by 1.25 over the judging files, the chain left as it is.

## 3. Multiplicity (counts are numbers too — they obey the reference-only rule)

Counts never appear in the scenario catalog. A count is bound in the timeline with a source — a task's `count` (how many tasks of one entry the file starts: `c1-browsing`'s `count: 4` hidden renderers) or a knob the entry's `binding_params` names (`build-orchestrator`'s `spawn_count` and `parallelism_cap`) — except the frame chain's `chain_length`, part of the topology the entry carries (`lavd-ossna24` s12). Two kinds, handled differently:

- **Emergent (dynamic) multiplicity** — cc1 is the exemplar. Its count emerges from the orchestrator's behavior: `build-orchestrator` consumes a pre-sampled spawn table of `spawn_count` object jobs, six spawn-table entries a job (`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`), at most `fork_cap` = `parallelism_cap` × 6 entries in flight (9.6 D19), and the count time-series falls out of simulation. This keeps the build's churn — jobs starting and ending as slots free — which the executor schedules; the recognizer sees the spawn table's names and counts attributed to the parent's lifetime (data-contracts §4), never the churn. `spawn_count` binds the measured build's object jobs (2,908 for the kernel's defconfig build, `meas-ci:build:2026-09-18`); `parallelism_cap` binds 8, a design value — the `nproc` rule on an eight-thread desktop (9.6 D4), labelled `design` in each binding — overridable at binding time (OQ-4).
- **Static multiplicity** — the hidden tabs' renderers are the exemplar: a binding-time `count` with a source tag, as every value a timeline binds carries a `source:` entry — a registry tag, a list of tags, or one of the labels `design`, `convention`, `arithmetic` — linted against `dataset/sources.yaml` (9.10 D32; 9.18 D2). `c1-browsing`'s four hidden renderers cite `glam` (Firefox's Linux tab telemetry) and `meas-ci:desktop:2026-10-04` (the Chrome tab-set campaign); `renderer-hidden` is one renderer, one site under Chromium's site-per-process model.

Observation: counts matter to both consumers. The executor needs actual task counts to schedule; the recognizer sees each name with its count in the snapshot (data-contracts §5), and a change in a count alone is a set change that fires a query (rule 1).

## 4. The inventory (29 entries)

The library as it stands (`dataset/archetypes.yaml`, v0.2), grouped by how an entry compiles (`dataset/tools/wlc/compiler.py`). Each measured entry is one program observed on one pinned CPU of a GitHub-hosted runner, its campaign the `meas-ci` tag below; "shown as" is the name the core files bind it under.

### Measured applications and session processes — one merged event stream (16)

One task carries the program's whole process tree: its threads' timer wakes (`components`, in every entry but `image-editor` and the playback and call entries: one per process role, or instance, and thread comm (9.5 D67), the comms below the coverage cut pooled into one `residual`; each from its measured gap and run tables), and where the observation holds them the driven cadence inside focus windows (`focus_components`), a replayed keystroke stream (`stimulus`), named operations and rare heavy runs, merged into one explicit stream at compile time; where the entry carries an observed launch phase (`launch`, ten of these sixteen: not `code-editor`, `image-editor` or the four session entries), a task arriving after 0 s first replays it (9.10 D136). The playback and call entries carry instead one periodic job per medium cycle — a constant `period` and a measured per-cycle `cycle_run` — a TIMER/RUN loop.

| Entry | The program measured | Campaign (`meas-ci:`) | Shown as |
|---|---|---|---|
| `office-writer` | LibreOffice Writer typing at the end of a long document, SWELL-KW's Word stream | `interactive:2026-09-18` | `soffice.bin` |
| `code-editor` | Visual Studio Code on a TypeScript project, SWELL-KW's Word stream | `interactive:2026-09-25` | `code` |
| `mail-client` | Thunderbird, SWELL-KW's Outlook stream, a `send` operation | `interactive:2026-09-27` (the idle phase `2026-09-19`) | `thunderbird-bin` |
| `web-browser` | Google Chrome's tree with the page in use, SWELL-KW's Internet Explorer stream, a `page-load` operation | `interactive:2026-09-20` | `chrome` |
| `image-editor` | GIMP driven by a pointer loop, an `unsharp-mask` operation | `interactive:2026-09-18` | `gimp` |
| `video-editor` | Kdenlive scrubbing a clip, a `preview-render` operation | `interactive:2026-09-18` (the idle phase `2026-10-05`) | `kdenlive` |
| `video-player` | mpv playing a 30 fps video, a 33,348 µs cycle | `playback:2026-09-18` | `mpv` |
| `audio-player` | mpv playing the same file's audio, a 49,635 µs cycle | `playback:2026-09-18` | `mpv` |
| `video-call` | a loopback WebRTC call in Chrome, a 10,001 µs cycle | `playback:2026-09-20` | `chrome` |
| `renderer-hidden` | a hidden tab's renderer, one per site | `desktop:2026-10-05b` | `chrome` |
| `chat-client` | Element Desktop, idle in one room | `desktop:2026-09-20` | `element-desktop` |
| `game-client` | the Steam client, logged out, its window shown | `desktop:2026-09-20` | `steam` |
| `compositor-shell` | GNOME Shell with Mutter, the session in its terminal idle state | `session:2026-09-24` | `gnome-shell` |
| `audio-server` | the PipeWire stack (pipewire, wireplumber, pipewire-pulse) | `session:2026-09-24` | `pipewire` |
| `service-manager` | systemd, pid 1 and the user manager | `session:2026-09-24` | `systemd` |
| `message-bus` | dbus-daemon, the system and session buses | `session:2026-09-24` | `dbus-daemon` |

### Batch jobs — a loop of measured runs and blocks (8)

`constructor: batch-loop`: a run drawn from the bound program's measured runs between voluntary blocks, pooled over its threads or its processes, then the block that followed such a run, until `total_work` of CPU is spent; a file binds the job's measured CPU total, the whole job (9.10 D17).

| Entry | The program measured | Campaign (`meas-ci:`) | Shown as |
|---|---|---|---|
| `cpu-batch` | one dominant thread runnable for its whole job; the `program` binding chooses its tables — `python3`, PyTorch's basic MNIST example training on the CPU; `kdenlive_render`, Kdenlive's export with its `melt-7`; `spoof`, one uninterrupted RUN by construction (design) | `background:2026-10-03`, `background:2026-10-03c` | `python`, `kdenlive_render`; `chrome` in `c6-spoof` |
| `file-archiver` | 7-Zip archiving a 10 GB file set, eight threads | `background:2026-09-19` | `7z` |
| `game-download` | SteamCMD's fresh install of a dedicated-server depot, Team Fortress 2's | `background:2026-09-19` | `steam` |
| `game-download-idle` | `game-download`'s tables under the declared class `idle`, for `c2-p2a-idle` alone | `background:2026-09-19` | `steam` |
| `package-upgrade` | Ubuntu 24.04's stock unattended upgrade's install stage, 916 processes | `background:2026-10-01` | `unattended-upgr` |
| `file-indexer` | Tracker's first index of a home, declared `idle` | `background:2026-10-02b` | `tracker-miner-f` |
| `video-transcoder` | HandBrakeCLI's default preset on the 4K edition of Big Buck Bunny, whole, no dominant thread | `background:2026-10-03b` | `HandBrakeCLI` |
| `incremental-backup` | Déjà Dup's scheduled incremental with duplicity, declared `idle` | `background:2026-10-04` | `deja-dup` |

### Builds — an orchestrator and its spawned jobs (4)

| Entry | What it is | Campaign (`meas-ci:`) | Shown as |
|---|---|---|---|
| `build-orchestrator` | GNU make building linux-6.6 defconfig at `-j8`: one measured dispatch run (`dispatch_overhead`) before each object job's six FORKs, `fork_cap` = `parallelism_cap` × 6, then `WAIT children` and EXIT | `build:2026-09-18` | `make` |
| `compiler-child` | the six-member object job (`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`), wired by WAIT/WAKE in its order, one quantile table per (role, structural step) | `build:2026-09-18` | the members' names |
| `module-build-orchestrator` | DKMS's autoinstall of NVIDIA's open kernel module, run by the unattended upgrade: the build's jobs in the order it ran them, then its serial tail as a batch loop | `background:2026-10-02` | `dkms` |
| `module-compiler-child` | the module build's jobs — object, kbuild probe and conftest trees — one table per (kind, role, step) | `background:2026-10-02` | the members' names |

### The frame chain — a constructed topology (1)

`game-task-chain` (`constructor: chain`, `category_source: lavd-ossna24`) — the only entry whose *topology* is a parameter, expanded by the compiler (interpretation-contract §6). A chain of `chain_length` 16 members, a point inside the source's 15–20 game-specific tasks (s12): the head, named by the task and driven by a TIMER at the 16,667 µs frame period — a design value, the Steam Deck's 60 Hz refresh (`steamos-refresh`) — and the 15 members named by the timeline's `member_names` (`lavd-ossna24` s16). A `wineserver` member, its RUN `wineserver_run` 260 µs (s13), is woken right after the head and is outside that count, as the entry states. Every member after the head is a WAIT/RUN/WAKE loop woken by the one before it, and the last wakes none (WAIT/RUN). `per_schedule_run` is a lognormal anchored on the slide's two named examples, 260 µs and 1.65 ms (s13), one draw for each of the 16 members. **Lane scaling:** the chain's aggregate demand per frame is scaled to `lane_share` of the lane, defended by the source's concentration statistics (the top 30–40 tasks hold 95 % of scheduling; the 15–20 game-specific tasks 60–70 %, s12), scheduling-frequency shares — the calibration is ours. No task-count parameter: the source's ~300 tasks are scheduled system-wide (s12; 9.4 D3); the game's threads beyond the chain and `wineserver` are omitted, in the entry and in every timeline that binds it (9.10 D19). The source's long-lived share and its wake mix are notes, not parameters (9.4 D6, D7).

### Spanning check

S1–S18 all compose from these 29: office S1 `office-writer`; browsing S2 `web-browser` with `renderer-hidden`; the call S3 `video-call`; mail S4 `mail-client`; the chat companion S5 `chat-client`; photo S6 `image-editor`; video editing and its export S7 `video-editor` with `cpu-batch`'s `kdenlive_render`; transcode S8 `video-transcoder`; gaming S9 `game-task-chain` with `game-client`; the download S10 `game-download`; edit and compile S11 `code-editor` with `build-orchestrator` and `compiler-child`, or DKMS's rebuild, `module-build-orchestrator` and `module-compiler-child`; training S12 `cpu-batch`'s `python3`; playback S13 `video-player` and `audio-player`; indexing S14 `file-indexer`; backup S15 `incremental-backup`; the archive burst S16 `file-archiver`; S17, redefined from the malware scan to the unattended upgrade (9.10 D3), `package-upgrade`; the session baseline S18 the four session entries. Each scenario the core set instances binds entries measured for its own programs except the gaming scenario's frame chain, grounded in the LAVD talk's figures, and the download's `steam`, SteamCMD's numbers by stated approximation (§5). The spanning claim is provisional under the Tier-2 protocol: `meas-ci` failures add entries.

## 5. Schema fields (for `archetypes.yaml` + linter)

Per entry (the top-level key is its id): `category_source` (Tier-1 provenance), `declared_class` (the scheduling class the program declares for itself, `normal` or `idle`; 9.13), `pattern` (grammar program, with a `constructor` where the compiler expands the entry — `chain`, `batch-loop`, `module-build`), numeric params (each a distribution object with `source:` and `sampling` — per-instance, per-task or per-iteration, interpretation-contract §5; a measured entry's stream params — `components`, `focus_components`, `stimulus`, `operations`, `heavy_events`, `launch`), `lifetime` (segment-bound | finite | spawned), `spawns`/`spawned_by` (orchestration edges), `binding_params` (the knobs a timeline must bind, names only), `scalable` (fields the lane-scaling pass may transform, with rule), `validation_stats` (the referee, the campaign's run and repeats, the statistics and the scope, or the stated reason no referee exists), and **`modeling_notes`** — prose recording what our encoding invented on top of the sources: field names, structure linearizations, scaling defenses, binding choices. The registry's `notes` records what a source establishes; `modeling_notes` records what we built on it — together they are the paper-writing guardrail against over-claiming.

**Binding notes recorded in `modeling_notes` (decided):**
- *`wineserver` is a member of the constructed chain* (9.4 D4), named `wineserver`, right after the head, its RUN `wineserver_run`; the source draws it as the hub of the game's dispatcher threads (s11, s16), and the chain's relay stands in for its request/reply round trip.
- *A batch entry's tables are chosen by its binding, never by the task's name.* `cpu-batch`'s `program` binding selects `python3` or `kdenlive_render`; Tracker's index is its own entry, `file-indexer`, bound as `tracker-miner-f` in `c1-indexing`, `c2-p1b` and `c7-indexing`.
- *The `steam` download carries SteamCMD's numbers by stated approximation* (9.7 D4): the desktop client's download needs a logged-in account, and no Steam account is used.

Linter rules for the library (`dataset/tools/wlc/linter.py`, `make lint`): reject an entry missing `category_source`, `declared_class`, `pattern`, `params`, `lifetime`, `binding_params`, `scalable`, `validation_stats` or `modeling_notes`; reject a `lifetime` or `declared_class` outside its set and a spawned entry without `spawned_by`; reject a numeric param without a `source:`, with an id absent from the registry or a locator violating the id's `locator_pattern`, or with a bad `sampling`; reject a quantile table without ten non-decreasing values, or whose extremes and interval means do not fit them; reject a `stimulus`, `launch` or `replay` stream with no file beside the library; reject `meas-pending` under the freeze, which `make lint` runs; and fail a `meas-ci` campaign tag that `dataset/meas-releases.yaml` does not map to a release.

## 6. Open questions — resolutions

- **OQ-1 (GPU axis): resolved — no flag.** The simulator is CPU-only and single-lane; no `gpu_bound` field enters the schema, and every measured entry ran on the GitHub-hosted runner (§2, observation venues), which has no GPU, as the interactive entries' scopes state. CpsMark+ Table 4's hardware sensitivity per workload remains a citation about resource mixes, recorded in the `cpsmark-tbench23` registry note.
- **OQ-2 (video-conference split): resolved — measured.** Meetings bind `video-call`, a WebRTC call in Chrome measured as one periodic job per audio-frame cycle (`meas-ci:playback:2026-09-20`): a loopback call in one page with a synthetic camera and microphone, as its scope states.
- **OQ-3 (renderer reuse): resolved — split per program.** The browser's tree, the page in use included, is `web-browser`; each hidden tab's site is one `renderer-hidden` task, one renderer per site under Chromium's site-per-process model; the chat and game clients are their own entries, `chat-client` and `game-client`, with no heartbeat TIMER (9.8 D1, D25).
- **OQ-4 (parallelism default): resolved — 8, a design value** (`nproc` on an eight-thread desktop, 9.6 D4), overridable at binding time; each file's demand is recorded in the manifest.
- **OQ-5 (distribution families): resolved — as observed.** Measured distributions are carried as their quantile tables (9.5 D17); lognormal remains the convention where a source gives only a span (`game-task-chain`'s `per_schedule_run`, its anchors read as p05/p95).
- **OQ-6 (grammar completeness): resolved — TIMER.** The gap was absolute time, not IO bandwidth: TIMER closes it (drift-free periodic demand). IO bandwidth contention remains out of scope while the executor models CPU only.
