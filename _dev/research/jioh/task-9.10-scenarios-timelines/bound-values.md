# Task 9.10 — the timelines' bound values: source tags and labels (D32)

Every value a core-set timeline binds — `count`, `spawn_count`, `parallelism_cap`, `total_work`, `lane_share`, `member_names`, `child_name` and the bound `program` — with the `source: <id>:<locator>` or the label it carries under D32 (changelog D160). The source ids are `docs/references.md`'s; a `meas-ci` tag is written as the library writes it. The derived files (`c2-pairs`, `c4`, `c6` and `c7` variants) carry the value their variant op binds. The field and its lint are 9.13's.

## Measured values

| value | task (entry) | files | ground | decision |
|---|---|---|---|---|
| `total_work: 26.385s`, the job's CPU total | the unattended upgrade (`package-upgrade`) | `c7-browsing`, `c7-dev`, `c7-gaming`, `c7-idle`, `c7-mail`, `c7-media`, `c7-meeting`, `c7-office`, `c7-photo`, `c7-video-edit`, `c2-p2b` | `meas-ci:background:2026-10-01` | D45 |
| `total_work: 39.435s` | Tracker's index (`file-indexer`) | `c1-indexing`, `c7-indexing`, `c2-p1b` | `meas-ci:background:2026-10-02b` | D78, D81 |
| `total_work: 1389.885s` | MNIST training (`cpu-batch`) | `c1-ml-train`, `c7-ml-train`, `c2-p1a` | `meas-ci:background:2026-10-03` | D88–D90 |
| `program: python3` | as above | as above | `pytorch-examples`; `meas-ci:background:2026-10-03` | D12, D85 |
| `total_work: 2970.871s` | HandBrake's transcode (`video-transcoder`) | `c1-transcode`, `c7-transcode`, `c3-creation` | `meas-ci:background:2026-10-03b` | D98–D100 |
| `total_work: 16.545s` | Kdenlive's export (`cpu-batch`) | `c1-render`, `c7-render`, `c2-p3a` | `meas-ci:background:2026-10-03c` | D110, D111 |
| `program: kdenlive_render` | as above | as above | `kdenlive`; `meas-ci:background:2026-10-03c` | D105–D107 |
| `total_work: 165.668s` | Déjà Dup's incremental (`incremental-backup`) | `c1-backup`, `c7-backup`, `c2-p3b` | `meas-ci:background:2026-10-04` | D124, D125 |
| `total_work: 727.170s` | the game download (`game-download`) | `c2-p2a` | `meas-ci:background:2026-09-19` | D142 |
| `spawn_count: 2908` | the user's kernel build (`build-orchestrator`) | `c1-compile`, `c4-compile`, `c3-workday`, `c6-dual` | `meas-ci:build:2026-09-18` | D18, D141 |
| `child_name: cc1` | as above; the module rebuild (`module-build-orchestrator`) in `c7-compile` | as above, `c7-compile` | `meas-ci:build:2026-09-18`; `meas-ci:background:2026-10-02` | D25, D55 |
| `count: 4`, the hidden tabs' renderers (`renderer-hidden`) | Chrome's other four tabs | `c1-browsing`, `c1-office`, `c3-workday`, `c3-evening`, `c4-compile`, `c4-office`, `c6-spoof`, `c6-fold`, `c7-browsing`, `c7-office` | `glam`; `meas-ci:desktop:2026-10-04` | D15, D130, D131 |
| `member_names` | the game chain (`game-task-chain`) | `c1-gaming`, `c4-gaming`, `c7-gaming`, `c2-p2a`, `c2-p2b`, `c3-evening`, `c6-dual` | `lavd-ossna24`, slide 16 | D26 |

## Design values

| value | task | files | label | decision |
|---|---|---|---|---|
| `parallelism_cap: 8` | the kernel build; the module rebuild | `c1-compile`, `c4-compile`, `c3-workday`, `c6-dual`; `c7-compile` | design: the eight-thread desktop | 9.6 D4; D18, D50 |
| `lane_share`: 0.9, 0.95, 1.45, 0.6 | the game chain | 0.9 `c1-gaming`, `c4-gaming`, `c7-gaming`; 0.95 `c2-p2a`, `c2-p2b`; 1.45 `c3-evening`; 0.6 `c6-dual` | design: a calibration size | D31 |
| `total_work: 30s`, `program: spoof` | the `chrome`-named batch job | `c6-spoof` | design: by construction | 9.6 D7; D31 |
| `total_work: 6s` | the injected archive job, `7z` (`file-archiver`) | `c4-office` | design: the injection's size, part of 9.7's measured job (4,882–5,283 s of CPU, `meas-ci:background:2026-09-19`), an exception to D17 | D161 |
