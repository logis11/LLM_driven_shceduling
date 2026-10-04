# Task 9.10 — the Chrome tab-set campaign's machine draws

Every `meas-desktop.yml` job of app `chrome-tabs` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #74–#76: 9 jobs, 5 drew the EPYC 7763 and landed (55.6 %), 4 were stopped by the machine gate** — AMD EPYC 9V74 2, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. Each of repeats 1–5 landed once, and all five are pooled.

Before it, the dry runs, runs #72 and #73, the gate open on any model as a dry run sets it: #72 on an Intel Xeon Platinum 8370C, whose listing read every process as the browser (method §8), and #73 on the EPYC 7763, the tooling holding. Neither is a repeat. In all, 11 jobs: 6 on the EPYC 7763.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #72 | 37193532949 | `chrome-tabs` | 1 | dry | dry run: the listing read every process as the browser (method §8) | ran | Intel Xeon Platinum 8370C |
| #73 | 37193972113 | `chrome-tabs` | 1 | dry | dry run, the listing amended | ran | AMD EPYC 7763 |
| #74 | 37194324949 | `chrome-tabs` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #74 | 37194324949 | `chrome-tabs` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #74 | 37194324949 | `chrome-tabs` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #74 | 37194324949 | `chrome-tabs` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #74 | 37194324949 | `chrome-tabs` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #75 | 37194411845 | `chrome-tabs` | 1 | full | first batch, gated indices retried | stopped by the gate | Intel Xeon 6973P-C |
| #75 | 37194411845 | `chrome-tabs` | 3 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #76 | 37194576054 | `chrome-tabs` | 1 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #76 | 37194576054 | `chrome-tabs` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
