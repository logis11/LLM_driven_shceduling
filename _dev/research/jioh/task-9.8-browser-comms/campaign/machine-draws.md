# Task 9.8 — the campaign's machine draws

Every `meas-desktop.yml` job of the 9.8 desktop campaign and the model it drew, from each job's own `report.kv` (`machine.model`, `gate`, `mode`, `repeat`). A hosted runner guarantees a shape, not a processor, and the campaign holds one model — the AMD EPYC 7763 — so a job on any other stops before measuring and is not a repeat (campaign workflow, 9.6 D11).

**71 of 132 jobs drew the EPYC 7763** (53.8 %). Of the 96 jobs in `full` mode (runs #21–#50), 55 landed on the model and were pooled and 41 were stopped by the gate: AMD EPYC 9V74 19, Intel Xeon Platinum 8573C 9, AMD EPYC 9V45 7, Intel Xeon 6973P-C 4, Intel Xeon Platinum 8370C 2. The rest of the jobs are the tooling's dry runs (runs #2–#15) and the long-phase probes (#17–#19), neither of them a repeat. Runs #1, #16 and #20 launched no measurement job.

| subject | archetype | runs | `full` jobs | landed and pooled | stopped by the gate |
|---|---|---|---|---|---|
| `chrome-hidden` | `renderer-hidden` | #21–#26, #31–#38 | 25 | 14 | 11 (EPYC 9V74 6, EPYC 9V45 2, Xeon 6973P-C 2, Xeon Platinum 8573C 1) |
| `chrome-visible` | `renderer-visible` | #21, #24, #26, #27, #31, #32, #39, #40 | 18 | 11 | 7 (EPYC 9V45 3, EPYC 9V74 3, Xeon Platinum 8573C 1) |
| `element` | `chat-client` | #21, #22, #24, #26–#29, #31, #40–#42, #46–#50 | 32 | 18 | 14 (Xeon Platinum 8573C 7, EPYC 9V74 4, Xeon 6973P-C 2, EPYC 9V45 1) |
| `steam` | `game-client` | #21–#24, #30, #43–#45 | 21 | 12 | 9 (EPYC 9V74 6, Xeon Platinum 8370C 2, EPYC 9V45 1) |

| model | jobs |
|---|---|
| AMD EPYC 7763 64-Core Processor | 71 |
| AMD EPYC 9V74 80-Core Processor | 25 |
| INTEL(R) XEON(R) PLATINUM 8573C | 17 |
| AMD EPYC 9V45 96-Core Processor | 10 |
| Intel(R) Xeon(R) 6973P-C | 6 |
| Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3 |

## Every job

| run | # | subject | repeat | mode | gate | model |
|---|---|---|---|---|---|---|
| 35495759446 | #2 | `chrome-hidden` | 1 | dry | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35495759446 | #2 | `chrome-visible` | 1 | dry | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35495759446 | #2 | `element` | 1 | dry | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35495759446 | #2 | `steam` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35495836182 | #3 | `chrome-hidden` | 1 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35495836182 | #3 | `chrome-visible` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35495836182 | #3 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35496352769 | #4 | `chrome-hidden` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35496352769 | #4 | `chrome-visible` | 1 | dry | open | AMD EPYC 9V45 96-Core Processor |
| 35496352769 | #4 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35496352769 | #4 | `steam` | 1 | dry | open | Intel(R) Xeon(R) 6973P-C |
| 35497325827 | #5 | `element` | 1 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35497325827 | #5 | `steam` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35498126190 | #6 | `element` | 1 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35498126190 | #6 | `steam` | 1 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35498534843 | #7 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35498720153 | #8 | `element` | 1 | dry | open | Intel(R) Xeon(R) 6973P-C |
| 35498754576 | #9 | `chrome-hidden` | 2 | dry | open | AMD EPYC 9V74 80-Core Processor |
| 35498754576 | #9 | `chrome-visible` | 2 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35499169413 | #10 | `chrome-hidden` | 3 | dry | open | AMD EPYC 9V45 96-Core Processor |
| 35499169413 | #10 | `chrome-visible` | 3 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35499169413 | #10 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35499461896 | #11 | `element` | 1 | dry | open | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35499616025 | #12 | `element` | 1 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35499782547 | #13 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35499977348 | #14 | `element` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35500297775 | #15 | `element` | 2 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35500297775 | #15 | `steam` | 2 | dry | open | INTEL(R) XEON(R) PLATINUM 8573C |
| 35501680255 | #17 | `chrome-hidden` | 1 | probe | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35501680255 | #17 | `chrome-visible` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35501680255 | #17 | `element` | 1 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35501680255 | #17 | `steam` | 1 | probe | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35501749098 | #18 | `chrome-hidden` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35501749098 | #18 | `element` | 1 | probe | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35501749098 | #18 | `steam` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35501788067 | #19 | `element` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35506753479 | #21 | `chrome-hidden` | 1 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35506753479 | #21 | `chrome-visible` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35506753479 | #21 | `element` | 1 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35506753479 | #21 | `steam` | 1 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35506838639 | #22 | `chrome-hidden` | 1 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35506838639 | #22 | `element` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35506838639 | #22 | `steam` | 1 | full | wrong-machine | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35506882547 | #23 | `chrome-hidden` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35506882547 | #23 | `steam` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `chrome-hidden` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `chrome-hidden` | 3 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35508871434 | #24 | `chrome-hidden` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `chrome-hidden` | 5 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35508871434 | #24 | `chrome-visible` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `chrome-visible` | 3 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35508871434 | #24 | `chrome-visible` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `chrome-visible` | 5 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35508871434 | #24 | `element` | 2 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35508871434 | #24 | `element` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `element` | 4 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35508871434 | #24 | `element` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `steam` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `steam` | 3 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35508871434 | #24 | `steam` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508871434 | #24 | `steam` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508896087 | #25 | `chrome-hidden` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35508896087 | #25 | `chrome-hidden` | 5 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35509010925 | #26 | `chrome-hidden` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509010925 | #26 | `chrome-visible` | 3 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35509010925 | #26 | `chrome-visible` | 5 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35509010925 | #26 | `element` | 2 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35509122608 | #27 | `chrome-visible` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509122608 | #27 | `chrome-visible` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509122608 | #27 | `element` | 2 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35509230804 | #28 | `element` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509947990 | #29 | `element` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35510066832 | #30 | `steam` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 6 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 10 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35585311256 | #31 | `chrome-hidden` | 11 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35585311256 | #31 | `chrome-visible` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-visible` | 7 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35585311256 | #31 | `chrome-visible` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `chrome-visible` | 9 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35585311256 | #31 | `chrome-visible` | 10 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35585311256 | #31 | `chrome-visible` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `element` | 6 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35585311256 | #31 | `element` | 7 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35585311256 | #31 | `element` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585311256 | #31 | `element` | 9 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35585545176 | #32 | `chrome-hidden` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585545176 | #32 | `chrome-hidden` | 10 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35585545176 | #32 | `chrome-hidden` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585545176 | #32 | `chrome-visible` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585759158 | #33 | `chrome-hidden` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585978825 | #34 | `chrome-hidden` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35586186257 | #35 | `chrome-hidden` | 10 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35586404781 | #36 | `chrome-hidden` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35586632429 | #37 | `chrome-hidden` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35586865270 | #38 | `chrome-hidden` | 10 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35587521689 | #39 | `chrome-visible` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35587769187 | #40 | `chrome-visible` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35587769187 | #40 | `element` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35587769187 | #40 | `element` | 7 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35587769187 | #40 | `element` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35588195326 | #41 | `element` | 7 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35588428093 | #42 | `element` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35592897185 | #43 | `steam` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35592897185 | #43 | `steam` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35592897185 | #43 | `steam` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35592897185 | #43 | `steam` | 9 | full | wrong-machine | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35592897185 | #43 | `steam` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35592897185 | #43 | `steam` | 11 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35592897185 | #43 | `steam` | 12 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35593126399 | #44 | `steam` | 9 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35593126399 | #44 | `steam` | 11 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35593126399 | #44 | `steam` | 12 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35593348663 | #45 | `steam` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35593348663 | #45 | `steam` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35593348663 | #45 | `steam` | 12 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594376695 | #46 | `element` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594376695 | #46 | `element` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594376695 | #46 | `element` | 12 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35594376695 | #46 | `element` | 13 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594376695 | #46 | `element` | 14 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35594376695 | #46 | `element` | 15 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35594376695 | #46 | `element` | 16 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594606756 | #47 | `element` | 12 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35594606756 | #47 | `element` | 14 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594606756 | #47 | `element` | 15 | full | open | AMD EPYC 7763 64-Core Processor |
| 35594819539 | #48 | `element` | 12 | full | open | AMD EPYC 7763 64-Core Processor |
| 35597073549 | #49 | `element` | 17 | full | open | AMD EPYC 7763 64-Core Processor |
| 35597185904 | #50 | `element` | 17 | full | open | AMD EPYC 7763 64-Core Processor |
