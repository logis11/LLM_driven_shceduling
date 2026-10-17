# 9.16 handed-over checks — findings

**F1 — the boot-default sweep reads the call's and the video player's quantile tables as deciles (9.14 decision 7).** Each `cycle_run` table holds ten percentiles, p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9 (`dataset/tools/wlc/sampling.py:75`; `video-call` at `dataset/archetypes.yaml:673`, `video-player` at `:623`). Checked with the compiler's sampler and the compiled cycles (6,000 in `c1-meeting`, 2,639 in `c7-meeting`, 1,800 in `c1-media`):
- the call past the 10 ms slice, "about a fifth" (`rq0-gate.yaml:31–32`, `:121`, `:242`, `:416–417`; `scoring-spec.yaml:67`): about one in twenty — 4.9 % from the table, 5.5 % in both meeting files;
- 12.2 ms "ninth decile" (`rq0-gate.yaml:129`, `:417`): the 99th percentile; the ninth decile is 7.4 ms;
- 14 ms demotes "under a tenth" (`:129`): 0.04 % of cycles;
- the video player's "decile cuts 2.3 to 7.5 ms" (`:127`, `:415`): the 1st and 99.9th percentiles; the deciles run 2.8 to 5.4 ms;
- 3 ms demotes "about seven in ten" (`:127`): about eight in ten (81.6 %; 82.4 % in `c1-media`);
- "upper decile (7.5 ms)" (`:128`): 5.4 ms.
Also quoted in `docs/daemon/prior-table-pair-review.md:59`, dataset guidebook `04-the-coreset.md:1720`, `08-decision-chronicle.md:1281`, `:1299`, `docs/memos/2026-09-12-rq0-pre-registration.md:55`. Every sweep point still falls on the side of the step its reason names. "About a fifth" is the stated reason `c7-meeting` re-entered the judging set (9.14 spec decision 2): a decision for 인지오.

**F2 — the `systemd-oomd` record reads a branch, not a release tag (9.19 decision 5).** `docs/references.md:591` cites `man/oomd.conf.xml` at `main` (263~devel), no commit. Fix: the cite and status at `:591`, `:593` to systemd v262.1, commit `73612ea502d53baf9b0df4336cfc296a7ee0d524` (published 2026-10-16), read 2026-10-17: lines 198–202 "Defaults to 30 seconds when unset or 0", lines 183 and 190 "10 second window", "Defaults to 60%". Same text at v255 (`db11bab38ccf1ed257f310d29070843d4c58ea01`, lines 85–88, 70, 77), the major version Ubuntu 24.04 ships (255.4). `dataset/sources.yaml:259–267` unchanged.

**F3 — `game-task-chain`'s `declared_class: normal` does not rest on the class census (9.13).** The census records "`game-task-chain` (9.4) is no measurement" (`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md:23`); its `normal` (`dataset/archetypes.yaml:1721`) is the 9.13 spec's default ("`normal` on every other entry", `task-9.13-rebuild.md:25`), unlabelled. Fix: label it design — the default, its source `lavd-ossna24` recording no class.
