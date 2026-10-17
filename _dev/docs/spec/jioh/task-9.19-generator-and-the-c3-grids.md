# 9.19 — Generator and the C3 grids

Sub-task 9.19 of Phase 9 (spec decision 9, the generated layer): the generator that composes the C1 task sets into grid files, the 2-segment transition grid, the 3-segment return grid, the flap-stress set, and the hold-time plan's step 3 (the precedent search), done in this spec session. Direction recorded in `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md` ("Direction taken on the open item", "Decision — focus enters the telemetry").

## Scope

- A generator composing the sixteen C1 task sets into grid files, each labelled design with no realism claim.
- The 2-segment transition grid over the 240 ordered mode pairs, in two forms.
- The 3-segment return grid A → B → A over the same pairs, the middle segment's length a variant (60 s, 10 s, 2 s).
- The flap-stress set, the hold time and hysteresis tuning and test material.
- One manifest per generated set; the tuning/measurement split recorded per file.
- The three authored C3 arcs kept as existence cases; the documents that describe the dataset's structure restated in this sub-task.
- The generated sets in the build gate and in CI, with one Linux CI run proving their manifests reproduce.
- Hold-time plan step 3, the precedent search for the debounce values real systems use (`_dev/docs/plan/jioh/hold-time-and-hysteresis.md`), done here; its result sets the flap-stress intervals.

## Locked decisions

### 1. Segments are a fixed 60 s; a batch job's size is bound to the span it must be alive in

Every grid segment is 60 s, the length of the interactive C1 files. A batch mode's job (`total_work` on `cpu-batch` kinds, `spawn_count` on the build orchestrator) is bound by the generator to the span of segments the job must be alive in — the segment alone where the mode's tasks depart at the boundary, the rest of the file where they stay — the value derived from the C1 binding's rate and labelled `source: design`. The job's CPU pattern is the archetype's measured one; only its total is design.

### 2. The transition grid's second form: B arrives at the boundary, the focus moves to B, A stays

Form 1 ("A departs and B arrives"): at 60 s A's tasks depart, B's arrive, the focus moves to B. Form 2 ("A stays and the focus moves to B"): at 60 s B's tasks arrive and the focus moves to B; A's tasks remain to the end of the file. A's input track exists only while A holds the focus; after 60 s the keystrokes go to B. Form 2 and the C4 cross-mode distractor cell of 9.20 ("B arrives, the focus stays on A") then share the multiset sequence and differ in the focus alone.

### 3. Layout of a C1 task set in a segment: 9.10 D44 as written

A segment's tasks are the mode's C1 tasks with their C1 arrive offsets, shifted to the segment's start; the segment's mode, `background_wanted`, `scenario` and familiarity are copied from the C1 segment; the focus holder is the C1's over the whole segment. The input window keeps the 2 s margins (start + 2 s to end − 2 s) and each operation sits at its fraction of the window, as 9.10 D44 places them. A segment of 4 s or less has no input window: the return grid's 2 s middle segment shows B for 2 s with no keystroke.

### 4. Generated timelines are not committed; the generator, its grid definition and the manifests are

The generator emits ordinary timeline YAML that the existing compiler compiles — no canonical artifact is produced directly. The timelines and their artifacts are build products, not committed; committed are the generator, its grid definition and each set's manifest. The generator is pure: its inputs are committed files only, its draws keyed, its output ordered. Each manifest's `inputs` pin by content the generator's sources, the sixteen C1 timelines, the library, the schema, the compiler and the streams, in 9.18's form; the gate regenerates, recompiles and compares with the committed manifests.

### 5. One manifest per generated set

The transition grid, the return grid and the flap-stress set each have their own manifest. The manifest is the set's pin; no experiment spec pins it yet (the RQ1 and RQ4 experiment specs will, as the RQ0 gate spec pins the core set's and the variants' manifests). The manifests' hashes are recorded in the sub-task changelog and handed to 9.16.

### 6. Tuning/measurement split: the return grid by pair, the flap-stress set by seed, recorded in the manifest

The return grid's 240 pairs are split 120/120 by keyed-hash rank of the pair id, a pair's three middle-length variants on the same side; the rule is design. Each flap-stress file is built under two seeds, one tuning and one measurement. The transition grid has no split. Each set's manifest records per file its grid coordinates (A, B, form or middle length) and `split: tuning | measurement`; the canonical schema's `meta` is unchanged.

### 7. Flap-stress set: intervals 2, 5, 10 and 30 s; 60 s lead-in plus eight alternations; three pairs; two seeds

Four intervals. 5 s, 10 s and 30 s are the values the precedent search found at the daemon-level switches comparable to ours — GameMode's `reaper_freq` (5 s), tuned's dynamic-tuning `update_interval` (10 s), systemd-oomd's `DefaultMemoryPressureDurationSec` (30 s) — each tagged with its source, each source entered in `docs/references.md` as a deployed-system entry; 2 s is a point below the range, labelled design. Each file is a 60 s lead-in on A followed by eight segments of the interval's length alternating A and B in form 1; the count eight is design. Three ordered pairs are drawn from the 240 by keyed hash. Three pairs × four intervals × two seeds: 24 files.

The precedent search (2026-10-11, primary sources read): three scales of debounce exist in shipped systems — hardware-state governors at 0.5 ms–80 ms (Linux cpufreq `schedutil`, `ondemand`, `conservative`; Android's `interactive` governor; the scheduler's `sysctl_sched_migration_cost`), daemon-level tuning switches at 5–30 s (GameMode, tuned, systemd-oomd), and capacity provisioning at 5–15 min (Kubernetes HPA and cluster autoscaler, AWS EC2 Auto Scaling cooldown, BGP route flap damping, RFC 2439). Windows processor power management states the hold form (increase/decrease times in units of the time-check interval) and publishes no default value. The daemon is a daemon-level switch; its range is 5–30 s. The full table with URLs and accessed dates goes to the sub-task changelog.

### 8. The authored arcs stay; the structure documents are restated in this sub-task

`c3-workday`, `c3-evening` and `c3-creation` are unchanged, their pins unchanged; their role is existence cases. The documents describing the dataset's structure are restated here: the building plan's C3 row and a generated-layer section, the dataset README, `docs/data-contracts.md` §14, the harness changelog. The proposal, the research-claims chain and the daemon guide are 9.15's.

### 9. The generated sets are in the build gate and in CI now

Each set has its make target (generate, compile, manifest); the three manifests join `check`'s manifest list under the existing rule that `build/` equals the union of every manifest; `dataset.yml` gains the step. One Linux CI run in this sub-task proves the three manifests reproduce; its id goes to the changelog. 9.21's CI-build-strategy item receives the measured size and time.

Measured in the spec session: a 60 s interactive C1 file compiles in 0.10–0.37 s, `c3-workday` in 3.7 s.

### 10. The return grid is form 1 only

A → B → A: A departs and B arrives at 60 s; B departs and A arrives again after the middle length. 240 pairs × three middle lengths = 720 files.

## Invariants

- Every generated file's seed is a keyed draw from its cell id, as the compiler's draws are keyed; no seed is chosen by hand.
- Every generated file's `source` map is the C1 files' as they stand, plus `design` on the values decision 1 scales.
- The schema, the lints, D44, 9.18's slice rule and the report sidecar are unchanged by this sub-task.
- The core set's and the variants' manifests and pins are unchanged.

## Open items

- A form-2 return grid (A stays, the focus moves to B and back) is not built; if the RQ4 experiment spec's session needs it, the grid is added then.
