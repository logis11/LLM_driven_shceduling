# Task 9.10 — the Kdenlive export campaign's machine draws

Every `meas-background.yml` job of app `kdenlive` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #162–#174: 56 jobs, 30 drew the EPYC 7763 and landed (53.6 %), 26 were stopped by the machine gate** — AMD EPYC 9V74 14, AMD EPYC 9V45 7, Intel Xeon Platinum 8370C 3, Intel Xeon Platinum 8573C 2. Each of repeats 1–30 landed once; all 30 are pooled.

Before it, the dry runs, runs #157–#161: 5 jobs, 3 on the EPYC 7763 and 2 stopped (AMD EPYC 9V74, AMD EPYC 9V45). #157 ran the first driver, whose shortcut opened no dialog; #160 and #161 ran the fixed driver, #161 launched again after #158's stop was read before #160 had landed. None of them is a repeat. In all, 61 jobs: 33 on the EPYC 7763, 28 stopped by the gate.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #157 | 37121829327 | `kdenlive` | 1 | dry | dry run, the shortcut opening no dialog (D105) | landed | AMD EPYC 7763 |
| #158 | 37122617500 | `kdenlive` | 2 | dry | dry run of the fixed driver | stopped by the gate | AMD EPYC 9V74 |
| #159 | 37122647962 | `kdenlive` | 2 | dry | dry run of the fixed driver | stopped by the gate | AMD EPYC 9V45 |
| #160 | 37122809400 | `kdenlive` | 2 | dry | dry run of the fixed driver | landed | AMD EPYC 7763 |
| #161 | 37123567963 | `kdenlive` | 2 | dry | dry run of the fixed driver, read for D105 | landed | AMD EPYC 7763 |
| #162 | 37124818629 | `kdenlive` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #162 | 37124818629 | `kdenlive` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #162 | 37124818629 | `kdenlive` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #162 | 37124818629 | `kdenlive` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #162 | 37124818629 | `kdenlive` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #163 | 37124854279 | `kdenlive` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #163 | 37124854279 | `kdenlive` | 5 | full | first batch | stopped by the gate | Intel Xeon Platinum 8573C |
| #164 | 37125022331 | `kdenlive` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 6 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 7 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 8 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #165 | 37125789856 | `kdenlive` | 9 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 10 | full | batch to the projection (D109) | stopped by the gate | Intel Xeon Platinum 8370C |
| #165 | 37125789856 | `kdenlive` | 11 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 12 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 13 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 14 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 15 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 16 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 17 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 18 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 19 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 20 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 21 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 22 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 23 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 24 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #165 | 37125789856 | `kdenlive` | 25 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 26 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 27 | full | batch to the projection (D109) | stopped by the gate | Intel Xeon Platinum 8370C |
| #165 | 37125789856 | `kdenlive` | 28 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #165 | 37125789856 | `kdenlive` | 29 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #165 | 37125789856 | `kdenlive` | 30 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #166 | 37125847561 | `kdenlive` | 6 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #166 | 37125847561 | `kdenlive` | 8 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #166 | 37125847561 | `kdenlive` | 10 | full | batch to the projection (D109) | stopped by the gate | Intel Xeon Platinum 8573C |
| #166 | 37125847561 | `kdenlive` | 11 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #166 | 37125847561 | `kdenlive` | 13 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #167 | 37126020125 | `kdenlive` | 6 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #167 | 37126020125 | `kdenlive` | 10 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #167 | 37126020125 | `kdenlive` | 13 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #168 | 37126535233 | `kdenlive` | 16 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #168 | 37126535233 | `kdenlive` | 20 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #169 | 37127022314 | `kdenlive` | 23 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #170 | 37127200770 | `kdenlive` | 23 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #170 | 37127200770 | `kdenlive` | 24 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #170 | 37127200770 | `kdenlive` | 25 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #170 | 37127200770 | `kdenlive` | 27 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #170 | 37127200770 | `kdenlive` | 28 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #171 | 37127379474 | `kdenlive` | 25 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V45 |
| #171 | 37127379474 | `kdenlive` | 27 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #172 | 37127557964 | `kdenlive` | 25 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #172 | 37127557964 | `kdenlive` | 27 | full | batch to the projection (D109) | stopped by the gate | Intel Xeon Platinum 8370C |
| #173 | 37127738977 | `kdenlive` | 25 | full | batch to the projection (D109) | stopped by the gate | AMD EPYC 9V74 |
| #173 | 37127738977 | `kdenlive` | 27 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
| #174 | 37127913545 | `kdenlive` | 25 | full | batch to the projection (D109) | landed | AMD EPYC 7763 |
