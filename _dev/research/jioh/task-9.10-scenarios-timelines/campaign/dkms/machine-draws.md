# Task 9.10 — the DKMS campaign's machine draws

Every `meas-background.yml` job of app `dkms` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is relaunched (`../../../measurement-campaign-workflow.md`, the loop, steps 2–3).

**Full mode, runs #108–#114: 37 jobs, 26 drew the EPYC 7763 and landed (70.3 %), 11 were stopped by the machine gate** — AMD EPYC 9V74 6, Intel Xeon Platinum 8573C 3, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. One push (`a6f08f7e`) started runs #111 and #112 together, so repeats 7, 10 and 11 landed twice; every landing is pooled (changelog D58). The two dry runs (#106, run 36980404122; #107, run 36982322419) drew the EPYC 7763.

| run | id | repeat | outcome | model |
|---|---|---|---|---|
| #108 | 36984969195 | 1 | landed | AMD EPYC 7763 |
| #108 | 36984969195 | 2 | landed | AMD EPYC 7763 |
| #108 | 36984969195 | 3 | landed | AMD EPYC 7763 |
| #108 | 36984969195 | 4 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #108 | 36984969195 | 5 | landed | AMD EPYC 7763 |
| #109 | 36985028429 | 4 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 6 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 7 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #110 | 36987366998 | 8 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 9 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 10 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #110 | 36987366998 | 11 | stopped by the gate | AMD EPYC 9V45 96-Core |
| #110 | 36987366998 | 12 | stopped by the gate | Intel Xeon Platinum 8573C |
| #110 | 36987366998 | 13 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 14 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 15 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 16 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 17 | stopped by the gate | Intel Xeon Platinum 8573C |
| #110 | 36987366998 | 18 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 19 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #110 | 36987366998 | 20 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #110 | 36987366998 | 21 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #110 | 36987366998 | 22 | landed | AMD EPYC 7763 |
| #110 | 36987366998 | 23 | stopped by the gate | Intel Xeon Platinum 8573C |
| #111 | 36987468347 | 7 | landed | AMD EPYC 7763 |
| #111 | 36987468347 | 10 | landed | AMD EPYC 7763 |
| #111 | 36987468347 | 11 | landed | AMD EPYC 7763 |
| #111 | 36987468347 | 12 | stopped by the gate | Intel Xeon 6973P-C |
| #112 | 36987471634 | 7 | landed | AMD EPYC 7763 |
| #112 | 36987471634 | 10 | landed | AMD EPYC 7763 |
| #112 | 36987471634 | 11 | landed | AMD EPYC 7763 |
| #112 | 36987471634 | 12 | landed | AMD EPYC 7763 |
| #113 | 36989503010 | 17 | landed | AMD EPYC 7763 |
| #114 | 36989807453 | 19 | landed | AMD EPYC 7763 |
| #114 | 36989807453 | 20 | landed | AMD EPYC 7763 |
| #114 | 36989807453 | 21 | landed | AMD EPYC 7763 |
| #114 | 36989807453 | 23 | landed | AMD EPYC 7763 |
