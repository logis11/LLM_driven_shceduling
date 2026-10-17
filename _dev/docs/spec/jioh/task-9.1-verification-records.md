# Task 9.1 — Verification records

Persist the 2026-09-13 verification into the repository. Parent: `_dev/TODO.md`, (jioh, 9.1); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`, which leaves the format and location of the records and whether source copies are kept to this task.

## Scope

- The 2026-09-13 verification output: the claim inventory with the topics, bibliographic entries and reader inputs; the independent reads R01–R11; the comparisons K1–K5 with the Crossref records; the measurement audit; the compiled-number audit; the audit scripts and their outputs.
- The source copies and raw measurement data that verification read.

## Locked decisions

### 1. Location

The records live in `_dev/research/jioh/2026-09-13-verification/`. `_dev/research/jioh/` is the space for research files, and later research gets its own dated sibling folders.

### 2. What is committed

The text records and the audit scripts, with the scripts' text outputs and working data, are committed.

### 3. What stays local

The source copies and the raw measurement data stay local and gitignored, inside the same folder next to the records.

### 4. The names:2 artifacts

The copy of the `meas-ci:names:2` artifacts from Actions run 34466009254 is committed with the records, the one exception to decision 3. Where names:2 is preserved permanently stays with task 9.3.

### 5. Records copied unedited except paths

Paths pointing into the 2026-09-13 session scratchpad are rewritten to the matching paths in the new folder. Nothing else changes: passages, locators, verdicts and the known input errors that the comparisons already correct stay as they were.

### 6. Index

The folder carries a short index: each committed record and what it covers, and each gitignored local folder and where it came from.
