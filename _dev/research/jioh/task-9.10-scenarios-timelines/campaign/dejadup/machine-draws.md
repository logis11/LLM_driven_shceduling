# Task 9.10 — the Déjà Dup backup campaign's machine draws

Every `meas-background.yml` job of app `dejadup` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`), or its `report.kv` where a cancelled job wrote no `report.json`. The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #183–#198: 56 jobs, 30 drew the EPYC 7763 and landed (53.6 %), 26 were stopped by the machine gate** — AMD EPYC 9V74 11, AMD EPYC 9V45 7, Intel Xeon Platinum 8573C 4, Intel Xeon 6973P-C 3, Intel Xeon Platinum 8370C 1. Each of repeats 1–30 landed once; 28 are pooled, repeats 12 and 25 left out: the set's fetch returned a 12 KB page from mattmahoney.net in place of the archive, and their backups ran on an empty tree (the validity step's set pins).

Before it, the dry runs, runs #175–#182: 8 jobs, 4 on the EPYC 7763 and 4 stopped (AMD EPYC 9V74 3, AMD EPYC 9V45 1). #176 and #177 ran the first drivers, whose window was black and whose button went unread (method §8); #180 ran the whole job on the 100 MB subset, #182 on the 10 GB set, read for D119. None of them is a repeat. In all, 64 jobs: 34 on the EPYC 7763, 30 stopped by the gate.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #175 | 37171359617 | `dejadup` | 1 | dry | dry run, the 100 MB subset | stopped by the gate | AMD EPYC 9V74 |
| #176 | 37171455182 | `dejadup` | 1 | dry | dry run, the 100 MB subset: the assistant's window black, cancelled (method §8) | cancelled after the gate | AMD EPYC 7763 |
| #177 | 37173423412 | `dejadup` | 1 | dry | dry run, the 100 MB subset: the button unread (method §8) | ran, the first backup's driver failing | AMD EPYC 7763 |
| #178 | 37174134729 | `dejadup` | 1 | dry | dry run, the 100 MB subset | stopped by the gate | AMD EPYC 9V74 |
| #179 | 37174182910 | `dejadup` | 1 | dry | dry run, the 100 MB subset | stopped by the gate | AMD EPYC 9V74 |
| #180 | 37174202662 | `dejadup` | 1 | dry | dry run, the 100 MB subset, whole | landed | AMD EPYC 7763 |
| #181 | 37174950585 | `dejadup` | 2 | dry | dry run, the 10 GB set | stopped by the gate | AMD EPYC 9V45 |
| #182 | 37174980221 | `dejadup` | 2 | dry | dry run, the 10 GB set, read for D119 | landed | AMD EPYC 7763 |
| #183 | 37177580623 | `dejadup` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #183 | 37177580623 | `dejadup` | 2 | full | first batch | stopped by the gate | Intel Xeon Platinum 8573C |
| #183 | 37177580623 | `dejadup` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #183 | 37177580623 | `dejadup` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #183 | 37177580623 | `dejadup` | 5 | full | first batch | stopped by the gate | Intel Xeon Platinum 8370C |
| #184 | 37177612398 | `dejadup` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #184 | 37177612398 | `dejadup` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #184 | 37177612398 | `dejadup` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #184 | 37177612398 | `dejadup` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #185 | 37177756676 | `dejadup` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #186 | 37177897212 | `dejadup` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 6 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 7 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 8 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 9 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon 6973P-C |
| #187 | 37180238545 | `dejadup` | 10 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #187 | 37180238545 | `dejadup` | 11 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon Platinum 8573C |
| #187 | 37180238545 | `dejadup` | 12 | full | the batch to 30 (D122) | landed, left out: the set's fetch a 12 KB page | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 13 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 14 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #187 | 37180238545 | `dejadup` | 15 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 16 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon 6973P-C |
| #187 | 37180238545 | `dejadup` | 18 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 19 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #187 | 37180238545 | `dejadup` | 20 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 21 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #187 | 37180238545 | `dejadup` | 22 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon Platinum 8573C |
| #187 | 37180238545 | `dejadup` | 23 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 24 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #187 | 37180238545 | `dejadup` | 25 | full | the batch to 30 (D122) | landed, left out: the set's fetch a 12 KB page | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 26 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 27 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #187 | 37180238545 | `dejadup` | 28 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon Platinum 8573C |
| #187 | 37180238545 | `dejadup` | 29 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #187 | 37180238545 | `dejadup` | 30 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #188 | 37180281641 | `dejadup` | 9 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #188 | 37180281641 | `dejadup` | 10 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #188 | 37180281641 | `dejadup` | 11 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #189 | 37180430331 | `dejadup` | 9 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #189 | 37180430331 | `dejadup` | 11 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #190 | 37180843202 | `dejadup` | 14 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #191 | 37180982965 | `dejadup` | 14 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #192 | 37181471921 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #192 | 37181471921 | `dejadup` | 19 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #193 | 37181647319 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #193 | 37181647319 | `dejadup` | 19 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #193 | 37181647319 | `dejadup` | 21 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #193 | 37181647319 | `dejadup` | 22 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #194 | 37181804469 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V45 |
| #195 | 37181957085 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | AMD EPYC 9V74 |
| #196 | 37182111743 | `dejadup` | 17 | full | the batch to 30 (D122) | stopped by the gate | Intel Xeon 6973P-C |
| #197 | 37182261621 | `dejadup` | 17 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #197 | 37182261621 | `dejadup` | 24 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #198 | 37182754648 | `dejadup` | 27 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
| #198 | 37182754648 | `dejadup` | 28 | full | the batch to 30 (D122) | landed | AMD EPYC 7763 |
