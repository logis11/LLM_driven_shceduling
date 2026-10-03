# Task 9.10 — the Tracker campaign's machine draws

Every `meas-background.yml` job of app `tracker` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #130–#140: 38 jobs, 18 drew the EPYC 7763 and landed (47.4 %), 20 were stopped by the machine gate** — AMD EPYC 9V74 16, Intel Xeon Platinum 8573C 1, Intel Xeon Platinum 8370C 1, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. Each of repeats 1–18 landed once; all 18 are pooled.

Before it: the three dry runs, runs #115–#121, 7 jobs, 3 on the EPYC 7763 (#118, #119, #121), 4 stopped (AMD EPYC 9V74 3, Intel Xeon Platinum 8573C 1); the first batch, runs #122–#125, 12 jobs, 7 landed (repeat 1 twice and repeat 3 twice, one push starting runs #124 and #125), 5 stopped (AMD EPYC 9V74 3, AMD EPYC 9V45 1, Intel Xeon Platinum 8573C 1), not pooled (changelog D75); the cold batch, runs #126–#129, 8 jobs, 5 landed, 3 stopped (AMD EPYC 9V74 2, Intel Xeon 6973P-C 1), not pooled (its cached fraction unrecorded, method §8).

| run | id | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|
| #115 | 37001389157 | 1 | dry | dry run | stopped by the gate | AMD EPYC 9V74 |
| #116 | 37001459962 | 1 | dry | dry run | stopped by the gate | AMD EPYC 9V74 |
| #117 | 37001546660 | 1 | dry | dry run | stopped by the gate | Intel Xeon Platinum 8573C |
| #118 | 37001819621 | 1 | dry | dry run | landed | AMD EPYC 7763 |
| #119 | 37002910488 | 1 | dry | dry run | landed | AMD EPYC 7763 |
| #120 | 37010356025 | 1 | dry | dry run | stopped by the gate | AMD EPYC 9V74 |
| #121 | 37010496980 | 1 | dry | dry run | landed | AMD EPYC 7763 |
| #122 | 37013699563 | 1 | full | first batch, not pooled (D75) | stopped by the gate | AMD EPYC 9V45 |
| #122 | 37013699563 | 2 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #122 | 37013699563 | 3 | full | first batch, not pooled (D75) | stopped by the gate | AMD EPYC 9V74 |
| #122 | 37013699563 | 4 | full | first batch, not pooled (D75) | stopped by the gate | AMD EPYC 9V74 |
| #122 | 37013699563 | 5 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #123 | 37013775432 | 1 | full | first batch, not pooled (D75) | stopped by the gate | Intel Xeon Platinum 8573C |
| #123 | 37013775432 | 3 | full | first batch, not pooled (D75) | stopped by the gate | AMD EPYC 9V74 |
| #123 | 37013775432 | 4 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #124 | 37014118970 | 1 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #124 | 37014118970 | 3 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #125 | 37014119153 | 1 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #125 | 37014119153 | 3 | full | first batch, not pooled (D75) | landed | AMD EPYC 7763 |
| #126 | 37075720148 | 1 | full | cold batch, not pooled (method §8) | landed | AMD EPYC 7763 |
| #126 | 37075720148 | 2 | full | cold batch, not pooled (method §8) | landed | AMD EPYC 7763 |
| #126 | 37075720148 | 3 | full | cold batch, not pooled (method §8) | stopped by the gate | Intel Xeon 6973P-C |
| #126 | 37075720148 | 4 | full | cold batch, not pooled (method §8) | landed | AMD EPYC 7763 |
| #126 | 37075720148 | 5 | full | cold batch, not pooled (method §8) | landed | AMD EPYC 7763 |
| #127 | 37075769024 | 3 | full | cold batch, not pooled (method §8) | stopped by the gate | AMD EPYC 9V74 |
| #128 | 37076024447 | 3 | full | cold batch, not pooled (method §8) | stopped by the gate | AMD EPYC 9V74 |
| #129 | 37076270628 | 3 | full | cold batch, not pooled (method §8) | landed | AMD EPYC 7763 |
| #130 | 37077613408 | 1 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #130 | 37077613408 | 2 | full | campaign | landed | AMD EPYC 7763 |
| #130 | 37077613408 | 3 | full | campaign | landed | AMD EPYC 7763 |
| #130 | 37077613408 | 4 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #130 | 37077613408 | 5 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #131 | 37077654870 | 1 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #131 | 37077654870 | 4 | full | campaign | landed | AMD EPYC 7763 |
| #131 | 37077654870 | 5 | full | campaign | landed | AMD EPYC 7763 |
| #132 | 37077892756 | 1 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 6 | full | campaign | stopped by the gate | Intel Xeon Platinum 8573C |
| #133 | 37079168920 | 7 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 8 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #133 | 37079168920 | 9 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 10 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #133 | 37079168920 | 11 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 12 | full | campaign | stopped by the gate | Intel Xeon Platinum 8370C |
| #133 | 37079168920 | 13 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 14 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #133 | 37079168920 | 15 | full | campaign | stopped by the gate | AMD EPYC 9V45 |
| #133 | 37079168920 | 16 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #133 | 37079168920 | 17 | full | campaign | landed | AMD EPYC 7763 |
| #133 | 37079168920 | 18 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #134 | 37079295954 | 6 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #134 | 37079295954 | 8 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #134 | 37079295954 | 10 | full | campaign | landed | AMD EPYC 7763 |
| #134 | 37079295954 | 12 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #134 | 37079295954 | 14 | full | campaign | landed | AMD EPYC 7763 |
| #134 | 37079295954 | 15 | full | campaign | landed | AMD EPYC 7763 |
| #135 | 37079532509 | 6 | full | campaign | landed | AMD EPYC 7763 |
| #135 | 37079532509 | 8 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #135 | 37079532509 | 12 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #135 | 37079532509 | 16 | full | campaign | landed | AMD EPYC 7763 |
| #136 | 37079763885 | 8 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #136 | 37079763885 | 12 | full | campaign | landed | AMD EPYC 7763 |
| #137 | 37079976338 | 8 | full | campaign | stopped by the gate | AMD EPYC 9V74 |
| #138 | 37080205717 | 8 | full | campaign | landed | AMD EPYC 7763 |
| #139 | 37080437629 | 18 | full | campaign | stopped by the gate | Intel Xeon 6973P-C |
| #140 | 37080669302 | 18 | full | campaign | landed | AMD EPYC 7763 |
