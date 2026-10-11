# Task 9.17 — Focus in the telemetry

The focus holder enters what the recognizer is shown, beside the name → count multiset. Decided in the 2026-10-11 grill, on the decision recorded in `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md` ("Decision — focus enters the telemetry"). Parent: `_dev/TODO.md`, (jioh, 9.17); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`, decision 10.

## Scope

- A window-focus track in the timeline, authored on every core-set timeline.
- The focus carried through compilation into the canonical workload and the visible projection; the run file unchanged.
- The telemetry rule that makes a focus change a set change, and the switch that shows or hides the field.
- The lints and tests the decisions imply; the mock daemon as the reference implementation of the rule and the switch.
- The rebuild, re-bless and re-pin the new field forces.
- `docs/data-contracts.md` — the timeline, workload, telemetry, recognition-log and invocation sections, with the changelog entry — and the dataset docs that describe the timeline's tracks. The proposal, the claims chain and the daemon guide are 9.15's; the final memo names the change.

## Locked decisions

### 1. A window-focus track, separate from the keystroke window

The timeline carries a track stating which task holds the window focus over which intervals. It is distinct from the existing track that places keystrokes: that track is a compile-time stimulus placement, and the window focus is the real-desktop signal the experiment measures. Every keystroke window lies inside a focus interval of the same task.

### 2. The focus holder is a process name

The snapshot carries the focus holder as a process name, `null` when no window holds the focus. The resolution is that of `/proc/<pid>/comm` on a real machine: the recognizer learns that one of the processes with that name holds the focus, not which instance. A focus move between two instances of the same name changes nothing in the snapshot and is not a query point. Only top-level tasks can hold the focus; spawn-table children cannot.

### 3. Where the focus lives

The canonical workload gains a top-level list of pinned focus intervals beside `meta`, `ground_truth` and `events`. The run file stays the events alone. The visible projection carries each task's focus intervals on its entry, as it carries its pinned arrival and departure. `ground_truth` does not change: the focus is shown to the recognizer, so it is not part of the answer key.

### 4. The authoring rule for the core set

The focus stays on the window the user last brought to the front, does not leave when typing stops, and is none only when no window exists.

- Single-mode files (C1, C2, C4, C5, C7 and their counterparts): the mode's foreground program holds the focus over its whole lifetime — `Troy.exe` for gaming, `mpv` for media, `chrome` for meeting.
- `c1-idle`: none.
- The `c2-p2a` family: the game throughout; the download's launch is carried by the segment's `initiated` attribute, not by a focus move.
- The C3 arcs: the focus moves to the next foreground program at the segment boundary. `c3-workday`: browser → writer → mailer, the writer holding through the compile segment. `c3-creation`: gimp → kdenlive, kdenlive holding through the transcode segment. `c3-evening`: browser → game → mpv.
- The C4 files: the focus stays on the running mode's program; the injected program arrives behind it.
- `c6-spoof`, `c6-fold`: their base's rule.
- `c6-dual`: the focus alternates between the game and the editor.

### 5. Telemetry shape is an axis orthogonal to the condition

Whether the snapshot shows the focus is a switch on the daemon, not a property of the condition: a flag in the invocation, a field in the recognition log stating the telemetry shape shown, a split key in the harness's experiment spec and records. Every condition runs under both shapes on the same files; the oracle and the random draw read no telemetry and must agree across the two.

### 6. Query points are defined on the full set

The set whose change is a query point is the name → count multiset together with the focus holder, whichever shape is shown. With the focus hidden, a focus-only change still emits a snapshot and a query point; the snapshot is identical to the one before it, and the recognizer's repeated answer is graded as any other.

### 7. Names

The keystroke-window track is renamed `input`. The window-focus track takes the name `focus`, so that the word has one meaning across the timeline, the workload, the projection and the telemetry.

### 8. The sub-task closes consistent

The new top-level key changes every artifact's hash. The set is rebuilt, re-blessed and re-pinned within this sub-task, so that `make check` passes at its close; 9.18's own re-bless follows.

## Invariants

- A focus interval names a top-level task, lies within that task's lifetime, and overlaps no other focus interval: one user, one attention track.
- Every `input` window lies inside a `focus` interval of the same task.
- Every timeline states its `focus` track, empty when no window exists.
- The run file is unchanged by this sub-task.
- The graded query-point counts the RQ0 gate pins are unchanged on the core set: every focus move in the authored rule coincides with an arrival except `c6-dual`'s alternation, and that file is outside grading.

## Open items

- The alternation period in `c6-dual`: taken from the window-switching sources 9.10 recorded (9.10 D169's entries) if one supplies a usable value; otherwise labelled design. Settled when the file is authored.
