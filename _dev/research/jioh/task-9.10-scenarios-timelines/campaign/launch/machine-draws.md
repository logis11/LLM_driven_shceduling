# Task 9.10 — the launch campaign's machine draws

Every `meas-desktop.yml` job of the apps `launch-*` and the model it drew, from each job's own `report.json` (`gate`, `machine.model`). The campaign holds one model, the AMD EPYC 7763; a job on any other stops before any install, is not a repeat, and its index is launched again.

**The campaign, full mode, runs #81–#98: 86 jobs, 50 drew the EPYC 7763 and landed (58.1 %), 36 were stopped by the machine gate** — AMD EPYC 9V45 14, AMD EPYC 9V74 12, Intel Xeon Platinum 8370C 4, Intel Xeon Platinum 8573C 3, Intel Xeon 6973P-C 3. Each subject's repeats 1–5 landed once, and all fifty are pooled. Gate stops per subject: `launch-kdenlive` 7, `launch-chrome-hidden` 5, `launch-mpv-audio`, `launch-mpv-video`, `launch-thunderbird-send` and `launch-webrtc` 4 each, `launch-soffice` 3, `launch-chrome` and `launch-element` 2 each, `launch-steam` 1.

Before it, the dry runs, runs #77–#80, the gate open on any model as a dry run sets it: 18 jobs, 11 on the EPYC 7763. Seven of #77's ten and #78's Kdenlive stopped at the quit (method §8). None is a repeat. In all, 104 jobs: 61 on the EPYC 7763.

| run | id | app | repeat | mode | batch | outcome | model |
|---|---|---|---|---|---|---|---|
| #77 | 37205258362 | `launch-chrome` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | AMD EPYC 7763 |
| #77 | 37205258362 | `launch-chrome-hidden` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | Intel Xeon Platinum 8573C |
| #77 | 37205258362 | `launch-element` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | AMD EPYC 7763 |
| #77 | 37205258362 | `launch-kdenlive` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | Intel Xeon 6973P-C |
| #77 | 37205258362 | `launch-mpv-audio` | 1 | dry | dry run (the ten subjects) | ran | AMD EPYC 7763 |
| #77 | 37205258362 | `launch-mpv-video` | 1 | dry | dry run (the ten subjects) | ran | AMD EPYC 9V74 |
| #77 | 37205258362 | `launch-soffice` | 1 | dry | dry run (the ten subjects) | ran | AMD EPYC 7763 |
| #77 | 37205258362 | `launch-steam` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | AMD EPYC 9V45 |
| #77 | 37205258362 | `launch-thunderbird-send` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | AMD EPYC 7763 |
| #77 | 37205258362 | `launch-webrtc` | 1 | dry | dry run (the ten subjects) | stopped at the quit (method §8) | Intel Xeon Platinum 8573C |
| #78 | 37205626346 | `launch-kdenlive` | 1 | dry | dry run 2 | stopped at the quit (method §8) | AMD EPYC 7763 |
| #78 | 37205626346 | `launch-soffice` | 1 | dry | dry run 2 | ran | AMD EPYC 9V45 |
| #79 | 37205972804 | `launch-kdenlive` | 1 | dry | dry run 3 | ran | AMD EPYC 9V74 |
| #80 | 37206212175 | `launch-chrome` | 1 | dry | dry run 4 | ran | AMD EPYC 7763 |
| #80 | 37206212175 | `launch-chrome-hidden` | 1 | dry | dry run 4 | ran | AMD EPYC 7763 |
| #80 | 37206212175 | `launch-element` | 1 | dry | dry run 4 | ran | AMD EPYC 7763 |
| #80 | 37206212175 | `launch-thunderbird-send` | 1 | dry | dry run 4 | ran | AMD EPYC 7763 |
| #80 | 37206212175 | `launch-webrtc` | 1 | dry | dry run 4 | ran | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-element` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #81 | 37206719313 | `launch-element` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-element` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #81 | 37206719313 | `launch-element` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-element` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-kdenlive` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-kdenlive` | 2 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #81 | 37206719313 | `launch-kdenlive` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #81 | 37206719313 | `launch-kdenlive` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #81 | 37206719313 | `launch-kdenlive` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #81 | 37206719313 | `launch-mpv-audio` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-mpv-audio` | 2 | full | first batch | stopped by the gate | Intel Xeon 6973P-C |
| #81 | 37206719313 | `launch-mpv-audio` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #81 | 37206719313 | `launch-mpv-audio` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-mpv-audio` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-mpv-video` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #81 | 37206719313 | `launch-mpv-video` | 2 | full | first batch | stopped by the gate | Intel Xeon Platinum 8573C |
| #81 | 37206719313 | `launch-mpv-video` | 3 | full | first batch | stopped by the gate | Intel Xeon Platinum 8573C |
| #81 | 37206719313 | `launch-mpv-video` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-mpv-video` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-soffice` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-soffice` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-soffice` | 3 | full | first batch | stopped by the gate | Intel Xeon Platinum 8370C |
| #81 | 37206719313 | `launch-soffice` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #81 | 37206719313 | `launch-soffice` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #82 | 37206775567 | `launch-element` | 1 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #82 | 37206775567 | `launch-element` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #83 | 37206957230 | `launch-kdenlive` | 2 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #83 | 37206957230 | `launch-kdenlive` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #83 | 37206957230 | `launch-kdenlive` | 4 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #83 | 37206957230 | `launch-kdenlive` | 5 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V45 |
| #84 | 37207069625 | `launch-steam` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #85 | 37207149111 | `launch-kdenlive` | 5 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #85 | 37207149111 | `launch-mpv-audio` | 2 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #85 | 37207149111 | `launch-mpv-audio` | 3 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #85 | 37207149111 | `launch-mpv-video` | 1 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #85 | 37207149111 | `launch-mpv-video` | 2 | full | first batch, gated indices retried | stopped by the gate | Intel Xeon Platinum 8370C |
| #85 | 37207149111 | `launch-mpv-video` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #86 | 37207337349 | `launch-kdenlive` | 5 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #86 | 37207337349 | `launch-mpv-audio` | 3 | full | first batch, gated indices retried | stopped by the gate | Intel Xeon Platinum 8370C |
| #86 | 37207337349 | `launch-mpv-video` | 2 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #86 | 37207337349 | `launch-soffice` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #86 | 37207337349 | `launch-soffice` | 5 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #87 | 37207517941 | `launch-kdenlive` | 5 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #87 | 37207517941 | `launch-mpv-audio` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #87 | 37207517941 | `launch-soffice` | 5 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome` | 2 | full | first batch | stopped by the gate | Intel Xeon Platinum 8573C |
| #88 | 37207775416 | `launch-chrome` | 3 | full | first batch | stopped by the gate | Intel Xeon 6973P-C |
| #88 | 37207775416 | `launch-chrome` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome-hidden` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome-hidden` | 2 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #88 | 37207775416 | `launch-chrome-hidden` | 3 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #88 | 37207775416 | `launch-chrome-hidden` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-chrome-hidden` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #88 | 37207775416 | `launch-thunderbird-send` | 1 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-thunderbird-send` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-thunderbird-send` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-thunderbird-send` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #88 | 37207775416 | `launch-thunderbird-send` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #88 | 37207775416 | `launch-webrtc` | 1 | full | first batch | stopped by the gate | AMD EPYC 9V74 |
| #88 | 37207775416 | `launch-webrtc` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-webrtc` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #88 | 37207775416 | `launch-webrtc` | 4 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #88 | 37207775416 | `launch-webrtc` | 5 | full | first batch | stopped by the gate | AMD EPYC 9V45 |
| #89 | 37207821709 | `launch-chrome` | 2 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #89 | 37207821709 | `launch-chrome` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #89 | 37207821709 | `launch-steam` | 1 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #90 | 37208009238 | `launch-steam` | 2 | full | first batch | landed | AMD EPYC 7763 |
| #90 | 37208009238 | `launch-steam` | 3 | full | first batch | landed | AMD EPYC 7763 |
| #90 | 37208009238 | `launch-steam` | 4 | full | first batch | landed | AMD EPYC 7763 |
| #90 | 37208009238 | `launch-steam` | 5 | full | first batch | landed | AMD EPYC 7763 |
| #91 | 37208042783 | `launch-chrome-hidden` | 2 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #91 | 37208042783 | `launch-chrome-hidden` | 3 | full | first batch, gated indices retried | stopped by the gate | Intel Xeon Platinum 8370C |
| #92 | 37208220326 | `launch-chrome-hidden` | 3 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V45 |
| #93 | 37208410569 | `launch-chrome-hidden` | 3 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #94 | 37208812995 | `launch-chrome-hidden` | 5 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #95 | 37209300555 | `launch-thunderbird-send` | 4 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V74 |
| #95 | 37209300555 | `launch-thunderbird-send` | 5 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #95 | 37209300555 | `launch-webrtc` | 1 | full | first batch, gated indices retried | stopped by the gate | Intel Xeon 6973P-C |
| #96 | 37209487694 | `launch-thunderbird-send` | 4 | full | first batch, gated indices retried | stopped by the gate | AMD EPYC 9V45 |
| #96 | 37209487694 | `launch-webrtc` | 1 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #97 | 37209685884 | `launch-thunderbird-send` | 4 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #98 | 37209874800 | `launch-webrtc` | 4 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
| #98 | 37209874800 | `launch-webrtc` | 5 | full | first batch, gated indices retried | landed | AMD EPYC 7763 |
