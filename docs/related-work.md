# Related Work — Draft
> Status: draft · Created 2026-08-25 · Updated 2026-08-27

> Draft v0. Structure follows the two-axis landscape: *what recognition reads* (behavior vs. meaning) × *what recognition produces* (generated policy vs. selected signal). Each subsection ends with an italicized note — the reviewer objection that paragraph exists to absorb, plus writing notes. Delete the notes before submission. Citation keys are placeholders; verify all arXiv versions at submission time (the SchedCP group iterates fast).

## Scheduling mechanisms: making policy replaceable

A line of systems work has made scheduling policy a replaceable component rather than a kernel constant. ghOSt delegates kernel scheduling decisions to userspace agents, motivated by the need to iterate on policy across a fleet without kernel rebuilds [ghost-sosp21]. sched_ext, merged in Linux 6.12, brings the same capability to mainline via eBPF: custom schedulers load at runtime with verifier-enforced safety and automatic fallback to the default scheduler [schedext]. Production schedulers built on it — scx_rusty, scx_layered, scx_lavd — demonstrate that non-default policies are deployable at scale [scx].

This work is complementary, not competing: it answers *how* a machine runs a chosen policy, and deliberately leaves open *how the machine knows which policy fits the current situation*. We target that open question. Our recognition layer produces the situational signal; mechanisms like sched_ext are how a consumer of that signal would take effect on a real system.

*Objection absorbed: "isn't sched_ext already this?" — No; it is the actuator, not the sensor. Note: this paragraph doubles as the honest framing for why our evaluation is simulator-based with sched_ext as future work — the mechanism layer is already proven, so simulating the executor forfeits less than it appears to.*

## Behavioral inference inside the scheduler

Where situational awareness exists in deployed schedulers today, it is inferred from runtime behavior. Classic interactivity heuristics — MLFQ's demotion by CPU consumption, and the sleep/wake accounting behind CFS and EEVDF — classify tasks by how they use the CPU [mlfq, eevdf]. The most developed recent instance is scx_lavd, which estimates each task's latency criticality from its wake/wait patterns and task-chain structure, and feeds that estimate into deadline assignment; it originated in gaming workloads, where mis-scheduling within a task chain surfaces as stutter [lavd].

Behavioral inference is cheap, private, and continuous, and we retain it wholesale: our executor is a behavioral scheduler. But behavior is a fundamentally limited channel for *intent*. Our load-bearing pair — an ML training run versus a file indexer, both manifesting as one CPU-saturating process beside an editor — is constructed so that the two situations are behaviorally indistinguishable in principle, yet demand opposite policies. No refinement of this quadrant can separate them; the distinguishing information exists only in what the processes *are*, not in what they *do*.

*Objection absorbed: "LAVD already infers latency sensitivity — why is that not enough?" — because it infers a task-level property, not a machine-level situation, and it reads behavior, which the F2 pair defeats by construction. Note: cite LAVD generously; we build on it rhetorically (Valve shipping it legitimizes 'desktop scheduling matters') and it is the strongest version of the position we argue against.*

## Learned schedulers

A second lineage replaces hand-written heuristics with learned policies. Decima learns cluster scheduling policies via RL over job DAGs [decima]; Firm learns SLO-driven resource management for microservices [firm]; Park generalizes the setting [park]. These systems learn a mapping from observed system state to scheduling actions, and their limits are by now well documented — including by later work in the LLM lineage: they require extensive per-workload retraining, and they operate inside a problem space a human has already formalized (features, knobs, objectives) [schedcp]. Closest to our architecture in shape, ASA recognizes workload patterns online — via time-weighted voting over behavioral signals — and routes to expert scheduling policies atop sched_ext [asa].

ASA shares our skeleton: recognize, then select among fixed policies rather than generate code. The difference is the recognition channel. ASA's recognizer, like the RL line, reads behavioral features and requires offline training per deployment context; ours reads process identity against world knowledge that requires no training on the target machine. The two channels fail differently: behavioral recognizers cannot see intent (§behavioral above), while identity-based recognition cannot see behavior it has no name for — a limit we scope explicitly (Family 5).

*Objection absorbed: "recognition-then-routing already exists (ASA)." — Yes; the contribution is not the skeleton but the channel, and we say so plainly. Note: do not overstate ASA's closeness in the intro and then minimize it here; reviewers diff those sections.*

## LLM agents for kernel policy

Recent work applies LLM agents to kernel policy directly. Kgent synthesizes kernel extensions from natural language [kgent]. SchedCP, the closest prior work, frames the same semantic gap we target — kernel policies cannot understand application needs — and answers it with an agentic control plane: a Workload Analysis Engine gives agents tiered access to profiling tools, and a multi-agent system analyzes the workload, then synthesizes or selects eBPF schedulers deployed via sched_ext, reporting up to 1.79× on kernel compilation [schedcp]. Adjacent efforts tune kernel parameters [tuneagent] and schedule HPC jobs [hpc-llm] with LLMs in the loop.

We share two commitments with this line: the semantic gap as the problem, and LLM reasoning kept strictly out of the scheduling hot path. We differ in what the LLM's understanding becomes, and for whom. First, the output contract: SchedCP's agents produce *policy* — generated or selected scheduler code, per workload, through an agentic session with sandboxed profiling (reading source, running perf). Our model produces a *signal* — a small fixed vocabulary of modes and attributes describing the situation — from process identity alone, in a single inference, with all policy remaining in fixed, auditable drivers. Second, the setting: SchedCP optimizes a given server or batch workload; a desktop is not a workload to optimize but a stream of situations to track, where the same machine is a gaming rig at 8pm and a build box at 9pm. Third, and most consequential for evaluation: prior LLM-scheduling work measures end-to-end performance only. Because our recognizer emits a graded signal against ground-truth labels, we can measure recognition *itself* — accuracy, consistency, distractor robustness — separately from scheduling benefit, and we evaluate against the strongest non-LLM implementation of semantic recognition (a whitelist) rather than only against default schedulers.

*Objection absorbed: "this is SchedCP for desktops." — The rebuttal is the output contract + the measurement layer; lean on Layer 1 and the whitelist baseline, which SchedCP's evaluation has no analogue of. Note: check for a SchedCP conference-length successor before every submission; if one exists, this paragraph is rewritten against it, not against the workshop paper.*

## Semantic recognition shipped today: static name tables

Semantic recognition of desktop situations is not hypothetical — it ships, in degenerate form. Windows Game Mode reprioritizes resources when a foreground executable matches a curated list [gamemode]. On Linux, ananicy adjusts process priorities from a community-maintained catalog mapping process names to priority classes; the catalog is maintained by hand, and every entry is a human decision made in advance [ananicy]. These systems validate our premise — process identity carries actionable scheduling information — while embodying the two limits we measure: enumeration (a table over names cannot cover the combinatorial space of co-running sets, nor novel software) and staleness (each entry costs curator labor).

We treat this quadrant as our true baseline. Our whitelist condition is a faithful reconstruction of this design point, and our claim is precisely that LLM inference generalizes it: same inputs (names), same output kind (a situational judgment), with the lookup table replaced by world knowledge that covers combinations and software no curator enumerated. Where the whitelist wins — famous software, exact matches — we report it winning.

*Objection absorbed: "Game Mode already exists." — Yes, and it is our baseline, not our competitor; the paper's headline experiments are exactly the cases where a name table cannot follow. Note: ananicy is the citable open artifact (public catalog, reproducible); Game Mode is closed — cite Microsoft documentation but reconstruct from ananicy's design.*

## Positioning

Two axes organize this landscape: what recognition reads (runtime behavior vs. process identity and world knowledge), and what it produces (generated policy code vs. a selected signal over fixed policies). Mechanisms (ghOSt, sched_ext) underlie all quadrants. Behavioral heuristics and learned schedulers occupy the behavior-reading column and cannot see intent. The LLM-agent line reads meaning but spends it on per-workload policy synthesis for servers. The meaning-reading, signal-producing quadrant — where desktop situation awareness must live — is today occupied only by static name tables. This work fills that quadrant's dynamic slot: a recognition layer that reads what a whitelist reads, produces what a whitelist produces, and replaces the table with inference — evaluated, for the first time in this line, at the recognition layer itself.

*Note: this closing paragraph is the prose version of the quadrant figure; if the figure makes it into the paper (recommended, as Figure 2 in intro or here), trim this paragraph to two sentences and point at the figure.*

---

## Reference placeholders

| key | work | venue | verify |
|---|---|---|---|
| ghost-sosp21 | Humphries et al., ghOSt | SOSP '21 | — |
| schedext | sched_ext, Linux kernel docs | Linux 6.12 | — |
| scx | sched-ext/scx repository | — | pin commit |
| lavd | scx_lavd / LAVD design | LKML + LPC talks | find best citable form |
| mlfq | MLFQ (OSTEP or original) | — | — |
| eevdf | EEVDF, kernel docs / Stoica '96 | — | — |
| decima | Mao et al. | SIGCOMM '19 | — |
| firm | Qiu et al. | OSDI '20 | — |
| park | Mao et al. | NeurIPS '19 | — |
| asa | Adaptive Scheduling Agent (Mixture-of-Schedulers) | arXiv 2511.11628 | check for venue |
| schedcp | Zheng et al., SchedCP / sched-agent | MLforSystems '25, arXiv 2509.01245 | **check for successor** |
| kgent | Zheng et al., Kgent | eBPF workshop '24 | — |
| tuneagent | TuneAgent | arXiv '25 | verify id |
| hpc-llm | LLM HPC job scheduling | arXiv '25 | verify id |
| gamemode | Windows Game Mode | MS documentation | — |
| ananicy | ananicy / ananicy-cpp | GitHub | pin catalog commit |
