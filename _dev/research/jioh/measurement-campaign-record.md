# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the headline median, the repeats, the margin the stability rule reached, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`soffice`: `--since 38`); job counts are the campaign runs' jobs (`status.py`). Recorded 2026-09-19.

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign, `code`, `soffice`, `mpv-audio` and `webrtc` (the pools read for this record; the others' kernels are in their pooled records). Stability rule: 95 % confidence half-width of the across-repeat mean of each headline median at most 5 % (`dataset/tools/meas/stability.py`).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#12 (35328071379, 35328873409, 35337322204) | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |

## 9.5 — one headline median per archetype

| archetype | application | headline median | repeats (windows) | mean | spread (cv) | 95 % half-width | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|---|
| `office-writer` | `soffice` | `input_run` p50, keys only (D28) | 5 (1–5) | 3.327 ms | 3.13 % | ±3.89 % | the rule | 6 (1) | SWELL-KW Word, participants 1–2 |
| `code-editor` | `code` | `input_run` p50 | 22 (1–22) | 74.69 ms | 10.82 % | ±4.83 % | the rule | 35 (13) | SWELL-KW Word, participants 1–11 of 25 |
| `mail-client` | `thunderbird` | `input_run` p50 | 8 (1–8) | 4.325 ms | 10.13 % | ±8.47 % | the input's end (D26) | 11 (3) | SWELL-KW Outlook, all 25 participants |
| `web-browser` | `chrome` | page-load duration p50 | 5 (1–5) | 472.7 ms | 3.35 % | ±4.16 % | the rule | 11 (6) | SWELL-KW Internet Explorer, participants 1–5 |
| `image-editor` | `gimp` | unsharp-mask duration p50 | 4 (1, 2, 3, 5) | 2 365.0 ms | 1.14 % | ±1.81 % | the rule | 6 (2) | scripted pointer loop |
| `video-editor` | `kdenlive` | preview-render duration p50 | 4 (1, 2, 3, 5) | 11 486.4 ms | 1.02 % | ±1.62 % | the rule | 10 (6) | scripted pointer loop |
| `video-player` | `mpv-video` | play-phase CPU share | 3 (1, 2, 4) | 0.1235 | 1.59 % | ±3.96 % | the rule | 8 (5) | none |
| `audio-player` | `mpv-audio` | play-phase CPU share | 29 (1–29) | 0.0072 | 12.72 % | ±4.95 % | the rule | 53 (24) | none |
| `video-call` | `webrtc` | play-phase CPU share | 5 (1–5) | 0.4084 | 2.34 % | ±2.91 % | the rule | 7 (2) | none |

The four typing-driven applications also replay the 136M Keystrokes windows 1…k of their own repeats in the `driven-alt` phase (the pre-registered stimulus check).

- `office-writer`: five repeats of the first design (runs #10–#28, the stream's clicks, scrolls and drags replayed with the keys; `input_run` p50 8.67, 3.99, 5.91, 4.53, 4.21 ms, ±44 %) are superseded by D28 and not pooled; 11 jobs, 6 gated.
- `mail-client`: SWELL-KW's Outlook conditions hold 4 761 s of recorded time — eight windows, the eighth 561 s; the half-width is stated as it is.
- `code-editor`: windows 1–10 average 79.8 ms, windows 11–20 69.6 ms; the later participants type more keys per window.
- `audio-player`: the CPU share is 0.58–0.86 % of one CPU while the wake rate stays at 206–211 per second.
- `video-player`, `image-editor`, `video-editor`: the windows the gate stopped (3 and 5; 4; 4) were not retried once the rule held.

## 9.6 — seven headline medians, one campaign

Repeats 4, 5, 7, 8 (repeats 1, 2, 3, 6 gated); 8 jobs. Warm `-j8` build, CPU per process of the object job's roles and make's dispatch run (µs). Archetypes: `build-orchestrator`, `compiler-child`, `cpu-batch`.

| median | mean | spread (cv) | 95 % half-width |
|---|---|---|---|
| `cc1` CPU per process | 364 750 | 1.5 % | ±2.36 % |
| `as` CPU per process | 3 054.5 | 1.2 % | ±1.96 % |
| `gcc` CPU per process | 2 238.8 | 1.6 % | ±2.49 % |
| `sh` CPU per process | 825.0 | 1.9 % | ±3.09 % |
| `fixdep` CPU per process | 5 626.3 | 0.8 % | ±1.27 % |
| `rm` CPU per process | 1 025.0 | 0.9 % | ±1.46 % |
| make dispatch run | 673.3 | 1.1 % | ±1.66 % |

Full tables: `task-9.6-compile/campaign/results.md`, `campaign/results/pooled.json`.

## Machine draws

166 jobs across the three campaigns: 94 on the AMD EPYC 7763 (56.6 %), 72 stopped by the machine gate — AMD EPYC 9V74 32, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8573C 12, AMD EPYC 9V45 8, Intel Xeon Platinum 8370C 8.
