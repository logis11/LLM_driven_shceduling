# Task 9.9 — the campaign's machine draws

Every `meas-session.yml` job of the 9.9 session campaign and the model it drew, from each job's own `report.json` (`machine.model`, `gate`). A hosted runner guarantees a shape, not a processor, and the campaign holds one model — the AMD EPYC 7763 — so a job on any other stops before measuring and is not a repeat (campaign workflow, 9.6 D11).

**39 of 77 jobs drew the EPYC 7763** (50.6 %), beside the 26 of 56 the 9.6 campaign recorded, the 22 of 45 of the released 9.5 campaign and the 55 of 96 of 9.8's. Of the 42 jobs in `full` mode, 24 landed on the model and were pooled and 18 were stopped by the gate; the rest of the jobs are the tooling's dry runs and the long-phase probes, neither of them a repeat.

| model | jobs |
|---|---|
| AMD EPYC 7763 64-Core Processor | 39 |
| AMD EPYC 9V74 80-Core Processor | 16 |
| INTEL(R) XEON(R) PLATINUM 8573C | 8 |
| Intel(R) Xeon(R) 6973P-C | 7 |
| AMD EPYC 9V45 96-Core Processor | 5 |
| Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 2 |

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
| 35798819217 | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
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
| 35934388525 | 50 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35934388525 | 51 | full | open | AMD EPYC 7763 64-Core Processor |
| 35938521032 | 52 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35939493589 | 53 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35940495385 | 54 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35940495385 | 55 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35940495385 | 56 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35941513123 | 57 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35941513123 | 58 | full | open | AMD EPYC 7763 64-Core Processor |
| 35941513123 | 59 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35941513123 | 60 | full | open | AMD EPYC 7763 64-Core Processor |
| 35945605366 | 61 | full | open | AMD EPYC 7763 64-Core Processor |
| 35945605366 | 62 | full | open | AMD EPYC 7763 64-Core Processor |
| 35945605366 | 63 | full | open | AMD EPYC 7763 64-Core Processor |
| 35945605366 | 64 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35948704522 | 65 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35948704522 | 66 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35948704522 | 67 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35948704522 | 68 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 69 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 70 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35948704522 | 71 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 72 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 73 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 74 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 75 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 76 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 77 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 78 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35948704522 | 79 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 80 | full | wrong-machine | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35948704522 | 81 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35948704522 | 82 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35948704522 | 83 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 84 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35948704522 | 85 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 86 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 87 | full | open | AMD EPYC 7763 64-Core Processor |
| 35948704522 | 88 | full | open | AMD EPYC 7763 64-Core Processor |
