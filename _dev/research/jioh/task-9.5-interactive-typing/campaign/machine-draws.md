# 9.5 campaign — CPU model per (application, repeat) (2026-09-18)

The observation's repeats as released in `meas-ci-2026-09-16`: `cpu_model` from each run folder's `spec.json` (`runner_spec.py`, `/proc/cpuinfo` model name), run identity from its `github_run`. Runs: `meas-interactive` 6 (35092593907) for `soffice`, `thunderbird`, `gimp`, `kdenlive`; 8 (35098829531) for `code`; 9 (35204260551) for `chrome` (`meas-interactive-chrome-run9.zip`); `meas-playback` 6 (35092593872) for `mpv-video`, `mpv-audio`, `webrtc`. Run 6's superseded `chrome` and `code` batches are not counted. Every repeat ran kernel `6.17.0-1022-azure`.

| application | r1 | r2 | r3 | r4 | r5 | on EPYC 7763 |
|---|---|---|---|---|---|---|
| `chrome` | EPYC 7763 | EPYC 7763 | EPYC 7763 | EPYC 7763 | EPYC 9V74 | 4 |
| `code` | EPYC 7763 | Xeon 6973P-C | EPYC 7763 | EPYC 9V74 | EPYC 9V45 | 2 |
| `gimp` | EPYC 7763 | EPYC 7763 | EPYC 7763 | EPYC 9V74 | EPYC 7763 | 4 |
| `kdenlive` | EPYC 7763 | EPYC 7763 | EPYC 7763 | Xeon Platinum 8573C | EPYC 7763 | 4 |
| `soffice` | EPYC 9V45 | EPYC 9V74 | EPYC 9V45 | EPYC 9V74 | EPYC 7763 | 1 |
| `thunderbird` | EPYC 7763 | EPYC 9V74 | EPYC 7763 | Xeon Platinum 8573C | EPYC 7763 | 3 |
| `mpv-audio` | EPYC 7763 | Xeon Platinum 8573C | Xeon Platinum 8573C | Xeon Platinum 8573C | EPYC 9V74 | 1 |
| `mpv-video` | EPYC 9V74 | EPYC 9V74 | EPYC 9V74 | EPYC 9V74 | EPYC 7763 | 1 |
| `webrtc` | Xeon Platinum 8573C | EPYC 9V74 | Xeon Platinum 8573C | EPYC 7763 | EPYC 7763 | 2 |

Jobs per model, 45 in all: AMD EPYC 7763 22, AMD EPYC 9V74 12, Intel Xeon Platinum 8573C 7, AMD EPYC 9V45 3, Intel Xeon 6973P-C 1. No application has its five repeats on one model; the most on one model is four (`chrome`, `gimp`, `kdenlive` on EPYC 7763; `mpv-video` on EPYC 9V74).
