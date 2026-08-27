# Phase 1 — Post-grill documentation pass

Lands every decision from the 2026-08-26 workload-generation grill into the project docs. Parent: `## Phase 1` in `_dev/TODO.md`; full decision record with rationale and verified sources: `_dev/archive/2026-08-26-workload-generation-grill.md`.

## Scope

- Create the reference/registry pair (`docs/references.md`, `dataset/sources.yaml`) and the interpretation-contract doc.
- Rewrite `docs/workload/building-plan.md` and `docs/workload/archetype-plan.md` to the grilled decisions; touch up `source-vetting`, `OPEN_QUESTIONS`, `TERMINOLOGY`, project `CLAUDE.md`; clean up `docs/workload/`.
- Write the one-page team memo (last, linking to the finished docs).
- Docs and registry files only — no compiler, simulator, or archetype-content work.

## Locked decisions

### 1. Reference/registry split and ownership

`docs/references.md` is the master index: it owns the id-minting rule (as a section of itself), every citation string, and all citation-constituent fields (`cite`, `url`, `accessed`, `pinned_version`), including related-work-only bibkeys. `dataset/sources.yaml` is the machine registry for dataset derivation only: bare source-id keys with `type`, `locator_pattern`, `notes`. Subset relation, lint-checked: every yaml id must have a docs/references.md entry. Contributor recipe: read the id rule → add docs/references.md entry → add yaml entry only if the dataset derives from it.

### 2. Id minting

Entry unit = one citable artifact (one citation, one URL, one accessed date; e.g. LAVD is three artifacts). Derivation by type: scholarly → `<label>-<venue><yy>` bibkey style; deployed-system → project name, no year, `pinned_version` carries freshness; measurement → `meas-ci`. Raw arXiv numbers banned as ids. Locators are intra-artifact pointers validated by an optional per-entry `locator_pattern` regex; registry keys are bare source-ids.

### 3. Measurement naming and scope

`roleD` is retired from the key namespace: `meas-ci` for CI measurements, `meas-pending` for placeholders (rejected after freeze), `category_source: meas`. meas-ci supports structural/shape claims only; machine-relative absolutes carry the runner spec and rank as convention-informed-by-measurement; N-run spread reported; framed as characterization of software behavior, never desktop performance.

### 4. D-live dissolved; meas-live dropped

User-behavioral parameters are literature-grounded and reclassified to Role C (`dhakal-chi18`, `dubroy-chi10`, `chang-chi21`, Test Pilot 2010). meas-live is out of the research entirely; the sampler + privacy-scrub tool still ships, framed as an open falsification invitation; live-usage validation is a stated limitation. Every doc sentence of the form "Role D will validate X" must name its replacement (literature, meas-ci, sensitivity analysis, or stated limitation).

### 5. Notes split

Registry `notes:` record what a source establishes and its scope limits; archetype-side `modeling_notes:` record what our encoding invented on top. A source tag justifies values and described structure, never field names.

### 6. Timeline / workload terminology and pipeline

Authoring files are **timelines** (`*.timeline.yaml`); `archetypes.yaml + timeline (+ scenario catalog) + seed → workload` (canonical, experiment-ready — "workload" keeps its docs/terminology.md meaning). Core timelines hand-authored; the naturalistic generator emits timelines too — one compile path for both sets.

### 7. Interpretation contract (the simulator spec — written before the simulator exists)

Six primitives (RUN/SLEEP/TIMER/WAIT/WAKE/FORK+EXIT); canonical op set `{arrive, wake}` plus pinned departs for segment-bound tasks; finite/spawned tasks end via EXIT at emergent times; FORK stays a runtime primitive consuming pre-sampled spawn tables; governing principle, verbatim: *compile time resolves all randomness; run time resolves all timing that scheduling can influence.*

### 8. Single lane ratified; four release artifacts

OPEN_QUESTIONS Q1(i)+(ii) stands: single lane, oversubscription-regime workloads, with an explicit demand-budget rule (aggregate demand ~100–150% of the lane; per-file RQ0 admission test enforces). Four artifacts from one pipeline: 2 timeline sets × 2 compile modes → `coreset-native/-single`, `generalset-native/-single`; experiments exclusively on `-single`; `-native` released with an unexecuted-status line; lane scaling is a per-archetype declared compiler pass, never baked into archetype values; game-task-chain scaling defended via LAVD concentration stats in `modeling_notes`.

### 9. Naturalistic distribution posture

Means/switch-rates from literature (`mark-chi08`, corroborated by `zhang-chb15`); family choice is a stated assumption with headline generalset numbers reported under both lognormal and power-law; DesktopBench optionally as a secondary sanity check.

### 10. Build order

(0) docs/references.md + registry → (1) archetypes.yaml v0.1 → (2) contract + canonical JSON Schema → (3) compiler → (4) core timelines → (5) simulator Phase 0 to the contract → (6) RQ0 gate → (7) generator/generalset/matrix; meas-ci workflows as an independent parallel track. (Phase 1 of the TODO covers step 0 plus the doc rewrites; later steps are Backlog.)

### 11. Archetype-plan closures

OQ-1: no GPU flag (closed by fact). OQ-2: S3 stays `video-playback`, stated approximation. OQ-3: referee re-pointed to meas-ci. OQ-4: parallelism cap `-j8` by stated convention, overridable at binding time. OQ-5: lognormal by convention + sensitivity. OQ-6: closed by TIMER. Browser default: chrome, firefox only per coverage-grid fill; renderer multiplicity defined against the Chromium model. Dual-active labels: author-specifies + hub-defines + documented limit, shipped as a third C6 file. Binding notes to record: wineserver → system-daemon provisional; P1 tracker-miner → cpu-batch deliberate.

### 12. Corrections and verified sources

source-vetting's "Yun et al." is wrong — the task-switching study is Zhang, Sun, Chai & Aghajan, CHB 49 (2015). All standing-search items are resolved with full coordinates in the archive doc (Steam setting article, keystroke and tab-count citations, DesktopBench release + license status, FOCAL preprint status) and go into docs/references.md.

### 13. Ownership and the team memo

인지오 owns the contracts and workload dataset generation; today's decisions are binding. Teammates are informed via a one-page memo written after the docs exist, linking rather than restating, with per-owner impact sections (simulator side; recognition side).

## Invariants

- Every yaml registry id has a docs/references.md entry (subset lint).
- Citation strings exist in exactly one place (docs/references.md).
- No "Role D will validate X" sentence survives without a named replacement.
- One normative home per topic after the `docs/workload/` cleanup.

## Open items

- Wineserver's place in the game-task-chain topology: decided at topology-constructor implementation time (recorded as provisional in `modeling_notes` for now).
- Coverage-grid fill for the ~50 core segments: build-step work (Backlog step 4), not Phase 1.
