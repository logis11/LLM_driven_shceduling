# 9.5 untraced control — results and fold-in, implementation plan

**Goal:** Each archetype's control reading in its `modeling_notes` (decisions 2, 12, 20), from the control's committed results record, and the results pages in each slice's `campaign/` folder.

**Architecture:** `control_report.py` gains `control_notes(rep)`, the reading in the compact form (the counts, then each difference grouped by phase and component, then the lines stated for the archetype), and two tables of stated lines — `NOTES_STATED` (into the notes and the page) and `PAGE_STATED` (the page only). The report writes each archetype's `control_notes` into its record as `notes`. Each family's `fold_in.py` takes `--control <record>` and appends its archetype's `notes` to the entry's notes.

**Tech stack:** Python 3.12, pytest; `dataset/tools/meas/` (control_report, campaign/desktop/session fold_in).

**Spec:** `_dev/docs/spec/jioh/task-9.5-untraced-control.md` (decisions 2, 12, 16, 17, 20, 23). Analysis plan: `task-9.5-untraced-control-analysis.md`.

## Global constraints

- No carried value changes (decision 2); only `modeling_notes` gain the reading.
- The fold-in tests stay byte for byte over the committed records.
- Results per slice: `campaign/results-control.md`, `campaign/results-control/` (the record and the control's pools).

---

### Task 1: the notes' reading

- [x] `control_notes(rep)`: the jobs, the carried phases run twice traced and untraced, the interval and chance counts; each difference as `<component>` <quantity> <per-job mean> (<interval>), grouped by phase, the operation phase read over the whole phase (decision 23); a tree value by its name; none found stated; the archetype's `NOTES_STATED` line after.
- [x] `PAGE_STATED` and `NOTES_STATED` rendered under the archetype on the page; the reading kept in the record as `notes`.
- [x] Tests; commit.

### Task 2: the fold-ins

- [ ] `--control <record>` in `campaign/fold_in.py`, `desktop/fold_in.py`, `session/fold_in.py`; the reading appended to each entry's notes.
- [ ] The fold-in tests read the committed records; commit.

### Task 3: results and recompile

- [ ] The report over every landed control job per family, the pages and records committed under each slice's `campaign/`.
- [ ] The fold-ins run with `--control`, spliced; `tools/compile.py --allow-window`; the manifest hashes; full test suite; commit.
