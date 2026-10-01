# Task 9.10 — Scenarios and timelines: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — unreachable or paywalled references and literature are dropped (2026-10-01)

By 인지오's decision, given after stage 2: a reference or a work of literature whose copy is technically unreachable or paywalled is dropped — it is neither a candidate of this slice nor a ground of the dataset.

- `zhang-chb15` (Zhang, Sun, Chai and Aghajan, *Computers in Human Behavior* 49, 2015) has no reachable copy: closed access, ScienceDirect 403, Elsevier API 429, only publisher metadata saved (`2026-09-13-verification/reads/R10-task-switching.md`; K4, C-zhang-1…5 UNVERIFIABLE). Its `dataset/sources.yaml` entry and its `docs/references.md` entry leave. No archetype value or timeline cites it; `make lint` reports only the five demand-window files the branch carries until 9.14.
- Stage-2 candidates S1-58 (CpsMark+, abstract only), S3-05 (a Windows dataset not released) and S3-06 (a Linux field study with no released data) are marked dropped in their records; the works the searches met without a readable copy are listed under "Dropped" in `search/candidates.md`. The search logs keep the queries that met them.
- Checked and kept, each with a copy that answers on 2026-10-01: `cpsmark-tbench23` (the publisher PDF from the Wayback capture of ScienceDirect's `main.pdf`, re-fetched byte-identical, SHA-256 `04d9f106862dfaaa8188dedfe06479c9742a578b4dcfb9d4e4dbde687c90f067`, the copy `reads/R04-cpsmark.md` read); `sysmark25` and the SYSmark 2018 documents (the Wayback copies of the user guides and white papers `reads/R05-vendor-benchmarks.md` read, HTTP 200); `chang-chi21` (the publisher PDF, CC BY 4.0, from a Wayback capture, S1-36). The other registry and reference entries in the scope card's group H were read in full from the copies the 2026-09-13 reads or the stage-2 records name.

Hands to 9.15: the prose that cites `zhang-chb15` is rewritten without it — `docs/workload/building-plan.md:137` (the planned naturalistic generator's hub-and-spoke switching, whose only source it was), `docs/workload/source-vetting.md:75`, `docs/workload/grounding-sources.md:81`.

## D2 — the core set's task sets are design (2026-10-01)

By 인지오's decision, scope-card items 22–44 (the task sets of the 23 authored timelines, and through them the 27 derived files) and the Source column of the scenario catalog's rows (items 3–20): which programs share a segment of a core-set file is the experiment's composition, chosen for the claim the file makes, and is labelled design (phase decision 3). No core-set file presents its task set as how desktops behave. Grounds: the core set is built "one file per claim (coverage grid)", and "every file exists to make a specific measurement possible", with ecological validity assigned to the naturalistic set (`docs/workload/building-plan.md` §0, §3). The stage-2 search over the four classes found no observation of which programs run together on Linux desktops (`search/candidates.md`, "Not found across classes"). The nearest candidates: SWELL-KW (S3-01: a Windows 7 lab, 2012, prescribed tasks; {Outlook, Word, IE} open together 63.4 % of working time, reader's own), BEHACOM (S3-02: the foreground program per minute and the count of top-level windows, not the open set), and benchmark definitions (S2-14, S2-15: existence only).

Each of these stays a realism claim, decided at its own item:

- each program's existence on Ubuntu 24.04 under the name the file shows (items 64–66);
- a situation a file presents as happening — an unasked scan, a module rebuild after a kernel update, a scheduled or user-started job (items 67–71; the card's boundary call (a));
- the state each bound entry describes, against the state the file depicts (item 63);
- counts (items 50–55), the arcs' order (items 41–43) and the recipes' premises (items 45–49).

No binding or value changed; the timeline headers state calibration and lineage, not observed sets, and are unchanged.

Hands to 9.15:

- `docs/workload/building-plan.md` §3's C1 paragraph ("Task sets are lifted from the segment that already carried the mode, the source named in each file's header", and its per-mode sets) restated as design;
- the scenario catalog's Source column states existence only;
- the limitation stated beside the venue limitation (`docs/workload/measurement-overview.md` §11): the scheduling-benefit result holds on these compositions, which are not shown to be typical.
