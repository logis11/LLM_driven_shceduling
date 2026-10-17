# Task 9.10 — the HandBrakeCLI campaign's machine draws

Every `meas-background.yml` job of app `handbrake` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #154–#156: 9 jobs, 5 drew the EPYC 7763 and landed (55.6 %), 4 were stopped by the machine gate** — AMD EPYC 9V74 4. Each of repeats 1–5 landed once; all 5 are pooled.

Before it, the probe (D93), runs #150–#151: 3 jobs, 2 on the EPYC 7763 (#151), 1 stopped (Intel Xeon Platinum 8370C); and the dry runs, both on the EPYC 7763: #152, D93's settings, superseded (D95), and #153, D95's (D97). None of them is a repeat. In all, 14 jobs: 9 on the EPYC 7763, 5 stopped by the gate.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #150 | 37100201579 | `handbrake` | 1 | probe | the probe (D93), never a repeat | stopped by the gate | Intel Xeon Platinum 8370C |
| #151 | 37100242887 | `handbrake` | 1 | probe | the probe (D93), never a repeat | landed | AMD EPYC 7763 |
| #151 | 37100242887 | `handbrake` | 2 | probe | the probe (D93), never a repeat | landed | AMD EPYC 7763 |
| #152 | 37103205438 | `handbrake` | 1 | dry | dry run of D93's settings, superseded (D95) | landed | AMD EPYC 7763 |
| #153 | 37105339193 | `handbrake` | 2 | dry | dry run (D97) | landed | AMD EPYC 7763 |
| #154 | 37109133562 | `handbrake` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #154 | 37109133562 | `handbrake` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #154 | 37109133562 | `handbrake` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #154 | 37109133562 | `handbrake` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #154 | 37109133562 | `handbrake` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #155 | 37109166427 | `handbrake` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #155 | 37109166427 | `handbrake` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #156 | 37109333265 | `handbrake` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #156 | 37109333265 | `handbrake` | 5 | full | first batch | landed | AMD EPYC 7763 |
