# Task 9.10 — the unattended-upgrade campaign's machine draws

Every `meas-background.yml` job of app `upgrade` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is relaunched (`../../../measurement-campaign-workflow.md`, the loop, steps 2–3).

**Full mode, runs #100–#105: 15 jobs, 9 drew the EPYC 7763 and landed (60 %), 6 were stopped by the machine gate** — AMD EPYC 9V45 2, AMD EPYC 9V74 2, Intel Xeon Platinum 8370C 1, Intel Xeon Platinum 8573C 1. The dry run (#99, run 36843481310) drew the EPYC 7763.

| run | id | repeat | outcome | model |
|---|---|---|---|---|
| #100 | 36847096521 | 1 | stopped by the gate | AMD EPYC 9V45 96-Core |
| #100 | 36847096521 | 2 | landed | AMD EPYC 7763 |
| #100 | 36847096521 | 3 | landed | AMD EPYC 7763 |
| #100 | 36847096521 | 4 | stopped by the gate | AMD EPYC 9V45 96-Core |
| #100 | 36847096521 | 5 | stopped by the gate | Intel Xeon Platinum 8370C |
| #101 | 36847549673 | 1 | landed | AMD EPYC 7763 |
| #101 | 36847549673 | 4 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #101 | 36847549673 | 5 | landed | AMD EPYC 7763 |
| #102 | 36847641558 | 4 | stopped by the gate | AMD EPYC 9V74 80-Core |
| #103 | 36847970176 | 4 | stopped by the gate | Intel Xeon Platinum 8573C |
| #104 | 36848289469 | 4 | landed | AMD EPYC 7763 |
| #105 | 36851095354 | 6 | landed | AMD EPYC 7763 |
| #105 | 36851095354 | 7 | landed | AMD EPYC 7763 |
| #105 | 36851095354 | 8 | landed | AMD EPYC 7763 |
| #105 | 36851095354 | 9 | landed | AMD EPYC 7763 |
