# Workload Grounding — Sources by Role

> Companion to Q7 and §5.5. The suite is synthetic by necessity (see "The negative result" below); this document lists what grounds each layer of the synthesis. Each source is annotated with *what it is allowed to justify* — do not cite a source outside its role.
>
> **Normative homes (2026-08-26):** citation strings, tiers, and per-entry role lines live in **docs/REFERENCES.md**; the machine registry is **docs/workload-dataset-sources.yaml**; the measurement campaign is **meas-ci** (WORKLOAD_DATASET_BUILDING_PLAN §7). The A–D role letters remain this document's vocabulary for *what kind of grounding* a source provides.

## Role A — Scenario taxonomy: "these situations are standard, not imagined"

Grounds the *choice of Families and modes*. These define what industry and academia already agree a desktop does. Use them to map each Family row to an external scenario category; none of them provide process timelines.

| source | what it is | what it justifies |
|---|---|---|
| PCMark 10 (UL Solutions) | Scenario benchmark: Essentials (web browsing, video conferencing, app start-up), Productivity (spreadsheets, writing), Digital Content Creation (photo/video editing, rendering); technical whitepaper documents each scenario's real applications | The office / browsing / creation / media mode categories; per-Family "corresponds to PCMark 10 X" mapping column in §5.5 |
| SYSmark 30 / 25 (BAPCo) | Scenario benchmark built from real commercial applications: Productivity (word processing, spreadsheets, software development, email), Creativity (photo/video, ML face recognition), Responsiveness | Same as PCMark, second independent taxonomy — two industry standards agreeing is stronger than one; SYSmark 25's inclusion of *software development* grounds the compile Family as a mainstream desktop scenario |
| UL Procyon | Newer UL suite: office productivity, photo/video editing, AI inference scenarios | Marginal; use only if a Family (e.g. local ML) needs a scenario precedent PCMark lacks |
| CpsMark+ (2023, ScienceDirect) | Academic scenario-oriented office desktop benchmark; compares against SYSmark 2018 and PCMark 10 as state of the art | The *methodological* precedent: "scenario-oriented workload definition for desktop evaluation" is an accepted academic move, not just industry practice |
| Windows Game Mode docs / ananicy catalog | Shipping systems' own categories (gaming; per-app priority classes) | That the *gaming* mode and the wanted/unwanted-background distinction are categories deployed systems already act on |

## Role B — Process behavior parameters: "each synthetic process behaves like the literature says"

Grounds the *pattern fields* of individual processes (burst, period, deadline, I/O mix). These are the sources the scheduler community recognizes on sight; calibrating our parameters to them converts "we made up the numbers" into "we instantiated the standard models."

| source | what it is | what it justifies |
|---|---|---|
| rt-app (ARM/Linaro) | Reproducible workload simulator; JSON specs of periodic tasks (period, runtime, deadline) | Our `pattern` schema is near-isomorphic to rt-app's task model — cite as the precedent for JSON-specified synthetic task behavior |
| interbench (Kolivas) | Emulates interactive tasks (audio, video, X, gaming) under background loads (Burn: CPU-bound threads; Write: streaming disk writes; compile-like), measuring latency, jitter, missed deadlines | Direct precedent for the *foreground-interactive + background-bulk* structure of Family 2; parameter values for audio/video/gaming interactivity |
| schbench (Mason, 2016) | Wakeup-latency benchmark reporting tail percentiles (P99) | Precedent for our latency metrics (tail-focused, not mean); also the messaging/wakeup-heavy process archetype |
| hackbench | Kernel-community load-balancing stressor (many communicating tasks) | The chat/IPC-heavy archetype's burst structure; recognizable stressor if we need a stress condition |
| LAVD design notes (LKML, LPC talks) | Characterization of gaming workloads: very short task durations, cross-layer task chains (game engine, Wine, graphics driver), tail latency perceived as stutter | Gaming Family parameters: burst lengths, chain structure, the 16ms-frame deadline; also the claim that desktop/gaming scheduling is a live production concern (Valve ships it; Meta adopted the scheduler server-side) |
| stress-ng | Configurable stressor collection | Fallback archetypes only (pure CPU hog, I/O hog); prefer the above where possible |
| kernel build (make -jN) | The de facto standard compile workload in every scheduler evaluation, including SchedCP's | The compile Family's fork-heavy, short-lived-children structure; also our canonicalization example (hundreds of cc1 children folding into one canonical app) |

## Role C — Segment structure and switching statistics: "the timeline shape is empirically grounded"

Grounds the *Q7 layer*: how long segments last, how often labels change, what within-segment churn looks like. This is HCI territory, not systems territory — these sources have app names and human timelines, which no systems trace provides.

| source | what it is | what it justifies |
|---|---|---|
| Large-scale task-switching log studies (e.g. the 15M-log / ~3k-user computer interaction study; Mark et al.'s multitasking line; Czerwinski/Horvitz diary studies) | Empirical distributions of app-switching frequency, session lengths, interruption rates for knowledge workers | Segment duration ranges (minutes, not seconds) and label-change frequency per hour; the claim that app-granularity sets are stable while PID-granularity churns |
| SWELL-KW dataset | Public multimodal knowledge-worker dataset including computer logging (application usage, window switching) — one of the few public datasets with app names intact | Concrete, citable app-name sequences; sanity-check our authored segment orderings against real ones |
| DesktopBench (2026, arXiv) | Multitask desktop sessions with app names and window titles; evaluates context-switch robustness via A→B→A interruption splits (long creative task interrupted by short browsing) | Direct precedent for the within-segment distractor experiment (Q7): the interruption-and-resume timeline shape, with an unrelated app appearing mid-segment |

## Role D — Measured validation: "the synthesis matches reality"

Grounds the *appendix defense*. No external source; our own measurement campaign.

> **Superseded (2026-08-26):** the campaign is **meas-ci** — scripted re-enactments on public CI runners, workflow files released, anyone can re-run — normative in WORKLOAD_DATASET_BUILDING_PLAN §7, with its scope discipline (structural/shape claims only; machine-relative absolutes carry the runner spec). The team-desktop plan this section previously described is retired. User-behavioral parameters (input inter-arrival, tab counts, segment durations) are literature-grounded under Role C; **live-usage validation was not performed and is a stated limitation**, with the collection + privacy-scrub tool released as an open falsification invitation.

## The negative result — why the suite is synthetic (write this into §5.5's preamble)

State it as a finding, not an apology: **no public trace of desktop process timelines with process names exists.** What does exist, and why each fails:

| candidate | why it fails for us |
|---|---|
| Enterprise / VDI / cloud workload traces (Azure, Google cluster traces, VDI characterization studies) | Server/VM granularity; no consumer applications; process identity absent or hashed |
| Desktop trace studies (older workload characterization literature) | Aggregate statistics survive; raw timelines with names were never released, largely for privacy |
| HCI logging datasets (beyond SWELL) | App-level events without the process-level detail (children, cgroups) the executor needs |

The absence is structural: process names are exactly the field privacy review strips, and process names are exactly what this research is about. One paragraph stating this converts "why is your dataset synthetic?" from a weakness into the motivation for the four-role grounding above — and for releasing our suite as an artifact, which no prior work in the LLM-scheduling line has done (SchedCP's own evaluation notes that a complete benchmark remains future work).

## Anti-roles — sources that look relevant but must not be used as grounding

- **Phoronix Test Suite / UnixBench**: performance measurement of a machine, not scenario definitions; citing them as scenario grounding invites "you benchmarked the wrong thing."
- **Mobile app-usage datasets (launch prediction, screen-time)**: tempting for switching statistics, but mobile foreground-exclusivity makes the concurrency structure disanalogous to desktop multitasking; a reviewer who knows the dataset will catch it.
- **The SchedCP evaluation workloads**: cite as related-work context, not as grounding — reusing them would concede the desktop framing.

## Citation-tier rule (style for the paper)

> Normative home now **docs/REFERENCES.md** (each entry carries its tier and role line); the rule is restated here for the scope-discipline sentence.

Sources in this document fall into two citation tiers, and the paper must keep them visually and functionally separate:

1. **Scholarly citations** (numbered bibliography): peer-reviewed papers and archived preprints — CpsMark+, LAVD/LWN-covered work, Gloria Mark line, CNNIC study, SchedCP, FOCAL, kernel-build characterizations.
2. **Deployed-system citations** (footnotes, URL + accessed date + pinned version/commit): product and artifact documentation — Windows Game Mode (Microsoft Learn), Steam client settings (Valve), ananicy catalog, sched_ext kernel docs, interbench/rt-app/schbench/hackbench/stress-ng repos, PCMark/SYSmark guides.

Scope discipline: a deployed-system citation may support only *existence claims* ("this scenario/setting/category exists in shipped software") — never empirical, behavioral, or statistical claims. If a sentence makes a claim about how often, how much, or how users behave, it needs a tier-1 source or our own Role D measurement. This is the same artifact-scope rule as for interbench ("the community *models* interactivity this way", not "desktops *behave* this way"), applied uniformly.

## Standing verification tasks — resolved (2026-08-26)

1. ~~Task-switching study citation~~ — resolved: `zhang-chb15` (authors corrected from "Yun et al."; see REFERENCES.md).
2. ~~DesktopBench license/venue~~ — resolved: released on HuggingFace, restrictive data terms, MIT scripts; methodological reuse unrestricted; FOCAL still a preprint (`focal-arxiv26`).
3. Version pins — tracked as `to-pin` statuses in REFERENCES.md; pin at submission.
4. SWELL-KW — cited qualitatively (`swell-icmi14`, REFERENCES-only; not in the registry).
5. ~~Valve coordinates~~ — resolved: `steam-downloads` (Steam Support article 4F9E-6328-E9B8-47F9, accessed 2026-08-26).
