# Task 9.5 — Interactive and typing: follow-ups

The follow-ups 9.5 carries after its D1–D20 fold-in. Parent: `_dev/TODO.md`, (jioh, 9.5); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`; decision record `_dev/research/jioh/task-9.5-interactive-typing/changelog.md`. Decided in the 2026-09-16 grill session.

## Scope

- The single-core re-measurement of the nine measured archetypes.
- Heavy-operation phases and the setup of the existing phases, per application.
- The stimulus-sensitivity comparison against the 136M Keystrokes data.
- The display and GPU literature search.
- The library-level scale limitation and the drop of the native compiled set, which arose from the same reasoning.

Out of scope: real-desktop validation captures. They stay deferred; the limitation is stated on each measured archetype.

## Locked decisions

### 1. All follow-ups stay in 9.5

The four follow-ups of the 2026-09-15 wrap-up gate 9.5; none is handed to another task or the backlog. The 9.5 TODO line carries them.

### 2. The observation is the application on one CPU

A measured archetype's observation is the application's process tree pinned to one CPU, matching the simulator's single lane. The pinned run replaces the unpinned one as each archetype's single observation; the unpinned figures stay in the campaign results for reference. The application tree is pinned; Xvfb, the replay driver and perf stay on the other vCPUs, and each archetype's scope says so.

### 3. Phase-wide: every runner measurement is single-core from now on

The pin and the wake definition of decision 4 go into the shared measurement tooling, so every campaign on the runner runs under them. The seven archetypes still carrying Phase 2 four-vCPU measurements (`build-orchestrator`, `compiler-child`; `background-crawler`, `io-stream`, `network-bulk`; `electron-comms`; `system-daemon`) are handed to 9.6, 9.7, 9.8 and 9.9; whether and when each slice re-runs is that slice's decision.

### 4. What counts as one wake

A wake is a schedule-in preceded by a wakeup event for that thread since its last sleep. A resume after preemption is not a wake: its run is added to the preceding wake's run, and the preempted time is neither run nor gap. The input-run rule (b) is unaffected. The definition is checked once against the existing unpinned data before the campaign.

### 5. One campaign at the end

The pinned campaign runs once, after the analysis fix, the heavy-operation work and the second stimulus stream are ready, covering idle, the existing driven phases, the operations and the sensitivity stream. One fold-in, one rebuild.

### 6. Setup states versus operations

VS Code with a project open and a language server running, and Writer with a large document, are the setup of the existing idle and driven phases, labelled design in scope; they change no structure. Operations are a separate kind.

### 7. Operations: three, under a stated criterion

An operation is the application's characteristic heavy work that typing does not already exercise: GIMP applying a filter to the open image; Kdenlive's timeline preview render (not its export, which the batch archetypes stand for); Chrome loading a scripted local page. Writer, VS Code and Thunderbird carry no operation; the players and the call have none. The criterion is recorded so any later addition is measured against it.

### 8. How an operation enters the archetype

A named operation carries its own per-thread components and a measured duration from trigger to completion, pooled from its scripted repeats. The timeline places it as a window at a point in time; the compiler draws the length from the duration table and swaps in the operation's components for that span. Completion is defined per operation in the campaign method.

### 9. What an operation does to the stream

From its start the operation's components replace whatever is active, idle or focus, for the measured duration; no input wakes are emitted during it; the previous state resumes when it ends. It runs to completion past the focus window. Whether it may start only inside a focus window, how often and where, is 9.10's.

### 10. Inputs come from the benchmark documentation first

The sizes and artifacts the setups and operations need (document, project, image and filter, clip, page) are taken from PCMark 10, SYSmark 30 and CpsMark+ where their workload descriptions state the corresponding input, cited as the ground for the choice of input; otherwise they are design and the scope says so. The cost and duration remain the campaign's observation.

### 11. Stimulus sensitivity is a pre-registered check

The 136M Keystrokes data is replayed as a second phase for the four typing-driven applications in the same campaign. The archetypes carry SWELL-KW whatever the result. The comparison lands in the campaign results and as one sentence per typing archetype's scope; a large difference is a stated limitation of D6, not a re-decision. The pre-registration is written before the campaign runs. The dataset is cited again under the citation rule, with its licence.

### 12. Display and GPU: a literature search that bounds the limitation

The search covers the four classes of phase decision 4 for two things: how a real refresh and GPU offload change a desktop application's CPU-side wake rate, run lengths and paint cadence on Linux; and what a compositor does per frame on a real GPU desktop. The first may add a cited direction-and-magnitude sentence to the scope of the display-paced archetypes (`video-player`, `video-editor`, `web-browser`, `code-editor`, `video-call`) or a recorded "not found"; the second is handed to 9.9. No archetype value changes: under phase decision 2 no literature figure is folded into a measured archetype.

### 13. Scale limitation at the composition seam

The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation. It is stated once at the library level. Handed to 9.14: a sensitivity check on the claims that depend on cross-archetype ratios, the demand-window rule and the prior-table rows. Handed to 9.16: the venue mix listed per timeline. A scale bridge, one benchmark figure both machines report, may be written into scope as the ratio, never applied to a value.

### 14. Native compiled set dropped

The dataset ships the single-lane set only. Handed to 9.13 for the build and to 9.15 for the docs.

## Invariants

- Phase decision 2 (one observation per archetype) and decision 3 (one observation per situation) are unchanged; the sub-task split carries no weight in them.
- Xvfb stays the observation venue; phase decision 5 (CI runners only) is unchanged.

## Open items

- Hand-off to 9.10: `thunderbird` is bound three ways across the coreset (`mail-client`, `network-bulk`, `electron-comms`); each non-identity binding needs a stated role now that Thunderbird is measured.
- Deferred, outside this task: real-desktop validation captures.
