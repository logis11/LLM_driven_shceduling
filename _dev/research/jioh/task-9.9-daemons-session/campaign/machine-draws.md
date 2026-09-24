# Task 9.9 — the campaign's machine draws

Every `meas-session.yml` job of the 9.9 session campaign and the model it drew, from each job's own `report.json` (`machine.model`, `gate`). A hosted runner guarantees a shape, not a processor, and the campaign holds one model — the AMD EPYC 7763 — so a job on any other stops before measuring and is not a repeat (campaign workflow, 9.6 D11).

**18 of 44 jobs drew the EPYC 7763** (41 %), in line with the 26 of 56 the 9.6 campaign recorded and the 22 of 45 of the released 9.5 campaign.

| model | jobs |
|---|---|
| AMD EPYC 7763 64-Core Processor | 18 |
| AMD EPYC 9V74 80-Core Processor | 12 |
| INTEL(R) XEON(R) PLATINUM 8573C | 6 |
| Intel(R) Xeon(R) 6973P-C | 4 |
| AMD EPYC 9V45 96-Core Processor | 3 |
| Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 1 |

## Every job

| run | repeat | mode | gate | model |
|---|---|---|---|---|
| 35729918486 | 2 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35729918486 | 6 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35735629925 | 9 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35742612282 | 17 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35742612282 | 18 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35742612282 | 19 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35742612282 | 20 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35742612282 | 21 | dry | open | Intel(R) Xeon(R) 6973P-C |
| 35795764108 | 22 | dry | open | Intel(R) Xeon(R) 6973P-C |
| 35795764108 | 23 | dry | open | Intel(R) Xeon(R) 6973P-C |
| 35795764108 | 24 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35795764108 | 25 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35797546428 | 1 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35798819217 | 1 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35814510341 | 26 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35814510341 | 27 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35816984839 | 28 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35816984839 | 29 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35816984839 | 30 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35816984839 | 31 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35835994906 | 32 | dry | session-not-up | INTEL(R) XEON(R) PLATINUM 8573C |
| 35835994906 | 33 | dry | session-not-up | AMD EPYC 7763 64-Core Processor |
| 35837872975 | 34 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35837872975 | 35 | dry | open | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35839696453 | 36 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35839696453 | 37 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35839696453 | 38 | probe | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35839696453 | 39 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35861267312 | 40 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35861267312 | 41 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35861267312 | 42 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35861267312 | 43 | probe | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35863364163 | 44 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35863364163 | 45 | probe | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35863364163 | 46 | probe | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35934388525 | 47 | full | open | AMD EPYC 7763 64-Core Processor |
| 35934388525 | 48 | full | open | AMD EPYC 7763 64-Core Processor |
| 35934388525 | 49 | full | open | AMD EPYC 7763 64-Core Processor |
| 35934388525 | 51 | full | open | AMD EPYC 7763 64-Core Processor |
| 35938521032 | 52 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35939493589 | 53 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35940495385 | 54 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35940495385 | 55 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35940495385 | 56 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
