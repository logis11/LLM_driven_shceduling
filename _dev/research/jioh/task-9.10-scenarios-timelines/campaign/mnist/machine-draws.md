# Task 9.10 — the MNIST campaign's machine draws

Every `meas-background.yml` job of apps `mnist` and `mnist-madvise` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #143–#147: 8 jobs, 6 drew the EPYC 7763 and landed (75.0 %), 2 were stopped by the machine gate** — Intel Xeon 6973P-C 1, AMD EPYC 9V45 1. Each of repeats 1–6 landed once; all 6 are pooled.

Before it, the dry run, runs #141–#142: 2 jobs, 1 on the EPYC 7763 (#142), 1 stopped (AMD EPYC 9V45). Beside it, the check (D87), runs #146, #148, #149: 9 jobs, 5 landed on the EPYC 7763, 4 stopped (AMD EPYC 9V45 2, AMD EPYC 9V74 2); pooled apart, never into the campaign. In all, 19 jobs: 12 on the EPYC 7763, 7 stopped by the gate.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #141 | 37089106351 | `mnist` | 1 | dry | dry run | stopped by the gate | AMD EPYC 9V45 |
| #142 | 37089156376 | `mnist` | 1 | dry | dry run | landed | AMD EPYC 7763 |
| #143 | 37091275421 | `mnist` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #143 | 37091275421 | `mnist` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #143 | 37091275421 | `mnist` | 3 | full | first batch | stopped by the gate | Intel Xeon 6973P-C |
| #143 | 37091275421 | `mnist` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #143 | 37091275421 | `mnist` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #144 | 37091313419 | `mnist` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #145 | 37093551770 | `mnist` | 6 | full | added (D87) | stopped by the gate | AMD EPYC 9V45 |
| #146 | 37093570964 | `mnist-madvise` | 1 | full | the check (D87), never a repeat | landed | AMD EPYC 7763 |
| #146 | 37093570964 | `mnist-madvise` | 2 | full | the check (D87), never a repeat | landed | AMD EPYC 7763 |
| #146 | 37093570964 | `mnist-madvise` | 3 | full | the check (D87), never a repeat | stopped by the gate | AMD EPYC 9V45 |
| #146 | 37093570964 | `mnist-madvise` | 4 | full | the check (D87), never a repeat | stopped by the gate | AMD EPYC 9V74 |
| #146 | 37093570964 | `mnist-madvise` | 5 | full | the check (D87), never a repeat | stopped by the gate | AMD EPYC 9V74 |
| #147 | 37093607991 | `mnist` | 6 | full | added (D87) | landed | AMD EPYC 7763 |
| #148 | 37093612595 | `mnist-madvise` | 3 | full | the check (D87), never a repeat | stopped by the gate | AMD EPYC 9V45 |
| #148 | 37093612595 | `mnist-madvise` | 4 | full | the check (D87), never a repeat | landed | AMD EPYC 7763 |
| #148 | 37093612595 | `mnist-madvise` | 5 | full | the check (D87), never a repeat | landed | AMD EPYC 7763 |
| #149 | 37093781292 | `mnist-madvise` | 3 | full | the check (D87), never a repeat | landed | AMD EPYC 7763 |
