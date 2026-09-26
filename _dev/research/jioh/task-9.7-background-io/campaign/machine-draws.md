# Task 9.7 — the campaign's machine draws

Every `meas-background.yml` job of the 9.7 background campaign and the model it drew, from each job's own `report.kv` (`machine.model`, `gate`, `mode`, `repeat`). A hosted runner guarantees a shape, not a processor, and the campaign holds one model — the AMD EPYC 7763 — so a job on any other stops before measuring and is not a repeat (campaign workflow, 9.6 D11); a SteamCMD job on a runner with no accelerated-networking VF stops at the network gate (D27).

**105 of 190 jobs drew the EPYC 7763** (55.3 %). Of the 145 jobs in `full` mode, 78 drew the model — 71 landed and 7 were stopped by the network gate — and 67 were stopped by the machine gate: AMD EPYC 9V74 24, Intel Xeon Platinum 8573C 20, AMD EPYC 9V45 14, Intel Xeon 6973P-C 8, Intel Xeon Platinum 8370C 1. The rest of the jobs are the tooling's dry runs (runs #1–#9), the probes (#10–#16) and the SteamCMD diagnostics (`diag` #17, #18, #41–#43; `shapediag` #44–#46), none of them a repeat.

| program | archetype | runs | `full` jobs | landed | pooled | stopped by the machine gate | stopped by the network gate |
|---|---|---|---|---|---|---|---|
| `7z` | `file-archiver` | #19–#23 | 14 | 6 | 6 | 8 (EPYC 9V74 3, EPYC 9V45 2, Xeon 6973P-C 2, Xeon Platinum 8370C 1) | — |
| `borg` | `file-backup` | #24–#40 | 55 | 31 | 30 | 24 (EPYC 9V74 8, EPYC 9V45 7, Xeon Platinum 8573C 7, Xeon 6973P-C 2) | — |
| `steamcmd` | `game-download` | #47–#98 | 76 | 34 | 30 | 35 (EPYC 9V74 13, Xeon Platinum 8573C 13, EPYC 9V45 5, Xeon 6973P-C 4) | 7 |

| model | jobs |
|---|---|
| AMD EPYC 7763 64-Core Processor | 105 |
| AMD EPYC 9V74 80-Core Processor | 33 |
| INTEL(R) XEON(R) PLATINUM 8573C | 22 |
| AMD EPYC 9V45 96-Core Processor | 18 |
| Intel(R) Xeon(R) 6973P-C | 10 |
| Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 2 |

## Every job

| run | # | program | repeat | mode | gate | model |
|---|---|---|---|---|---|---|
| 35425404685 | #1 | `7z` | 1 | dry | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35425404685 | #1 | `borg` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35425404685 | #1 | `steamcmd` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35425432178 | #2 | `7z` | 1 | dry | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35425490370 | #3 | `7z` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35426343360 | #4 | `7z` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35426343360 | #4 | `borg` | 1 | dry | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35426369940 | #5 | `borg` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35426597604 | #6 | `steamcmd` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35427212093 | #7 | `steamcmd` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35430102138 | #8 | `borg` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35430102138 | #8 | `steamcmd` | 1 | dry | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35430576648 | #9 | `steamcmd` | 1 | dry | open | AMD EPYC 7763 64-Core Processor |
| 35431588969 | #10 | `7z` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431588969 | #10 | `7z` | 2 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35431588969 | #10 | `7z` | 3 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431588969 | #10 | `borg` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431588969 | #10 | `borg` | 2 | probe | wrong-machine | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35431588969 | #10 | `borg` | 3 | probe | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35431588969 | #10 | `steamcmd` | 1 | probe | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35431588969 | #10 | `steamcmd` | 2 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431588969 | #10 | `steamcmd` | 3 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35431653597 | #11 | `7z` | 2 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431653597 | #11 | `borg` | 3 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35431653597 | #11 | `steamcmd` | 3 | probe | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35431681555 | #12 | `steamcmd` | 3 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35435649599 | #13 | `borg` | 2 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35435649599 | #13 | `steamcmd` | 1 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35435680013 | #14 | `borg` | 2 | probe | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35435736147 | #15 | `borg` | 2 | probe | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35435792623 | #16 | `borg` | 2 | probe | open | AMD EPYC 7763 64-Core Processor |
| 35444904353 | #17 | `steamcmd` | 1 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35475239657 | #18 | `steamcmd` | 1 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35475673566 | #19 | `7z` | 1 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35475673566 | #19 | `7z` | 2 | full | wrong-machine | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| 35475673566 | #19 | `7z` | 3 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35475673566 | #19 | `7z` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35475673566 | #19 | `7z` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35475673566 | #19 | `7z` | 6 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35475736076 | #20 | `7z` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35475892675 | #21 | `7z` | 1 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35475892675 | #21 | `7z` | 2 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35475892675 | #21 | `7z` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35475946669 | #22 | `7z` | 1 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35475946669 | #22 | `7z` | 2 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476102967 | #23 | `7z` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476102967 | #23 | `7z` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 1 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35476401518 | #24 | `borg` | 2 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476401518 | #24 | `borg` | 3 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35476401518 | #24 | `borg` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 8 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35476401518 | #24 | `borg` | 9 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476401518 | #24 | `borg` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 11 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35476401518 | #24 | `borg` | 12 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 13 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476401518 | #24 | `borg` | 14 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 15 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476401518 | #24 | `borg` | 16 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35476401518 | #24 | `borg` | 17 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35476401518 | #24 | `borg` | 18 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 19 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 20 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35476401518 | #24 | `borg` | 21 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35476401518 | #24 | `borg` | 22 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35476401518 | #24 | `borg` | 23 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476401518 | #24 | `borg` | 24 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476432132 | #25 | `borg` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476432132 | #25 | `borg` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476432132 | #25 | `borg` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476432132 | #25 | `borg` | 8 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35476432132 | #25 | `borg` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476590684 | #26 | `borg` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 13 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 15 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35476881396 | #27 | `borg` | 16 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 17 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 20 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35476881396 | #27 | `borg` | 21 | full | open | AMD EPYC 7763 64-Core Processor |
| 35476881396 | #27 | `borg` | 22 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35477031052 | #28 | `borg` | 15 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35477031052 | #28 | `borg` | 20 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35477182078 | #29 | `borg` | 15 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35477182078 | #29 | `borg` | 20 | full | open | AMD EPYC 7763 64-Core Processor |
| 35477182078 | #29 | `borg` | 24 | full | open | AMD EPYC 7763 64-Core Processor |
| 35477330157 | #30 | `borg` | 15 | full | open | AMD EPYC 7763 64-Core Processor |
| 35477330157 | #30 | `borg` | 22 | full | open | AMD EPYC 7763 64-Core Processor |
| 35478501325 | #31 | `borg` | 25 | full | open | AMD EPYC 7763 64-Core Processor |
| 35479018795 | #32 | `borg` | 26 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35479120587 | #33 | `borg` | 26 | full | open | AMD EPYC 7763 64-Core Processor |
| 35479531720 | #34 | `borg` | 27 | full | open | AMD EPYC 7763 64-Core Processor |
| 35479992656 | #35 | `borg` | 28 | full | open | AMD EPYC 7763 64-Core Processor |
| 35480602297 | #36 | `borg` | 29 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35480706292 | #37 | `borg` | 29 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35480807863 | #38 | `borg` | 29 | full | open | AMD EPYC 7763 64-Core Processor |
| 35481223770 | #39 | `borg` | 30 | full | open | AMD EPYC 7763 64-Core Processor |
| 35481632830 | #40 | `borg` | 31 | full | open | AMD EPYC 7763 64-Core Processor |
| 35489683204 | #41 | `steamcmd` | 1 | diag | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35489781888 | #42 | `steamcmd` | 1 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35492649723 | #43 | `steamcmd` | 1 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35492649723 | #43 | `steamcmd` | 2 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35492649723 | #43 | `steamcmd` | 3 | diag | open | AMD EPYC 7763 64-Core Processor |
| 35497985049 | #44 | `steamcmd` | 1 | shapediag | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35497985049 | #44 | `steamcmd` | 2 | shapediag | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35497985049 | #44 | `steamcmd` | 3 | shapediag | open | AMD EPYC 7763 64-Core Processor |
| 35498072437 | #45 | `steamcmd` | 1 | shapediag | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35498072437 | #45 | `steamcmd` | 2 | shapediag | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35498198482 | #46 | `steamcmd` | 1 | shapediag | open | AMD EPYC 7763 64-Core Processor |
| 35498198482 | #46 | `steamcmd` | 2 | shapediag | open | AMD EPYC 7763 64-Core Processor |
| 35502824537 | #47 | `steamcmd` | 1 | full | open | AMD EPYC 7763 64-Core Processor |
| 35502824537 | #47 | `steamcmd` | 2 | full | open | AMD EPYC 7763 64-Core Processor |
| 35502824537 | #47 | `steamcmd` | 3 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35502824537 | #47 | `steamcmd` | 4 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35502824537 | #47 | `steamcmd` | 5 | full | open | AMD EPYC 7763 64-Core Processor |
| 35502868640 | #48 | `steamcmd` | 3 | full | open | AMD EPYC 7763 64-Core Processor |
| 35502868640 | #48 | `steamcmd` | 4 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35503071794 | #49 | `steamcmd` | 4 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 6 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 7 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 8 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 9 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 10 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35509003684 | #50 | `steamcmd` | 11 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509003684 | #50 | `steamcmd` | 12 | full | open | AMD EPYC 7763 64-Core Processor |
| 35509045982 | #51 | `steamcmd` | 10 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35509241651 | #52 | `steamcmd` | 10 | full | open | AMD EPYC 7763 64-Core Processor |
| 35583900159 | #53 | `steamcmd` | 13 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584428409 | #54 | `steamcmd` | 14 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35584428409 | #54 | `steamcmd` | 15 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584428409 | #54 | `steamcmd` | 16 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584428409 | #54 | `steamcmd` | 17 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35584428409 | #54 | `steamcmd` | 18 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584428409 | #54 | `steamcmd` | 19 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35584428409 | #54 | `steamcmd` | 20 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584428409 | #54 | `steamcmd` | 21 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35584428409 | #54 | `steamcmd` | 22 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35584473283 | #55 | `steamcmd` | 14 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584473283 | #55 | `steamcmd` | 17 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35584473283 | #55 | `steamcmd` | 19 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35584871283 | #56 | `steamcmd` | 17 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584871283 | #56 | `steamcmd` | 19 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35584871283 | #56 | `steamcmd` | 21 | full | open | AMD EPYC 7763 64-Core Processor |
| 35584871283 | #56 | `steamcmd` | 22 | full | open | AMD EPYC 7763 64-Core Processor |
| 35585275567 | #57 | `steamcmd` | 19 | full | open | AMD EPYC 7763 64-Core Processor |
| 35686980811 | #58 | `steamcmd` | 23 | full | open | AMD EPYC 7763 64-Core Processor |
| 35729425641 | #59 | `steamcmd` | 24 | full | open | AMD EPYC 7763 64-Core Processor |
| 35736409534 | #60 | `steamcmd` | 25 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35736699472 | #61 | `steamcmd` | 25 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35736941629 | #62 | `steamcmd` | 25 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35737184634 | #63 | `steamcmd` | 25 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35737445169 | #64 | `steamcmd` | 25 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35737692964 | #65 | `steamcmd` | 25 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35737952780 | #66 | `steamcmd` | 25 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35738206567 | #67 | `steamcmd` | 25 | full | open | AMD EPYC 7763 64-Core Processor |
| 35745702827 | #68 | `steamcmd` | 26 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35745760752 | #69 | `steamcmd` | 26 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35746016906 | #70 | `steamcmd` | 26 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35746280613 | #71 | `steamcmd` | 26 | full | open | AMD EPYC 7763 64-Core Processor |
| 35753782786 | #72 | `steamcmd` | 27 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35753836288 | #73 | `steamcmd` | 27 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35754079731 | #74 | `steamcmd` | 27 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35754320041 | #75 | `steamcmd` | 27 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35754561085 | #76 | `steamcmd` | 27 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35754810326 | #77 | `steamcmd` | 27 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35755055492 | #78 | `steamcmd` | 27 | full | open | AMD EPYC 7763 64-Core Processor |
| 35761988583 | #79 | `steamcmd` | 28 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35762043308 | #80 | `steamcmd` | 28 | full | open | AMD EPYC 7763 64-Core Processor |
| 35768937357 | #81 | `steamcmd` | 29 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35768995976 | #82 | `steamcmd` | 29 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35769248102 | #83 | `steamcmd` | 29 | full | open | AMD EPYC 7763 64-Core Processor |
| 35775857984 | #84 | `steamcmd` | 30 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35776133966 | #85 | `steamcmd` | 30 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35776373555 | #86 | `steamcmd` | 30 | full | open | AMD EPYC 7763 64-Core Processor |
| 35783098091 | #87 | `steamcmd` | 31 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35783361577 | #88 | `steamcmd` | 31 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35783592135 | #89 | `steamcmd` | 31 | full | open | AMD EPYC 7763 64-Core Processor |
| 35790224174 | #90 | `steamcmd` | 32 | full | wrong-machine | AMD EPYC 9V74 80-Core Processor |
| 35790273177 | #91 | `steamcmd` | 32 | full | no-vf | AMD EPYC 7763 64-Core Processor |
| 35790487419 | #92 | `steamcmd` | 32 | full | wrong-machine | Intel(R) Xeon(R) 6973P-C |
| 35790695548 | #93 | `steamcmd` | 32 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35790902680 | #94 | `steamcmd` | 32 | full | wrong-machine | INTEL(R) XEON(R) PLATINUM 8573C |
| 35791107702 | #95 | `steamcmd` | 32 | full | wrong-machine | AMD EPYC 9V45 96-Core Processor |
| 35791310480 | #96 | `steamcmd` | 32 | full | open | AMD EPYC 7763 64-Core Processor |
| 35796976408 | #97 | `steamcmd` | 33 | full | open | AMD EPYC 7763 64-Core Processor |
| 35804093822 | #98 | `steamcmd` | 34 | full | open | AMD EPYC 7763 64-Core Processor |
