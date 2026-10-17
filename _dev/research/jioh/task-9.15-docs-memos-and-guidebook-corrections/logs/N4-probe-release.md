# N4 (Q1) — 9.5's long-phase probes released

인지오's answer (a), 2026-10-17, to N4's Q1 (`../work-list.md`): the five probe runs released before 2026-12-18 in `meas-ci-probes-2026-10-05`'s form, as `meas-ci-probes-2026-09-20`.

## Release

- Tag `meas-ci-probes-2026-09-20`, "meas-ci probes 2026-09-20 — 9.5 long-phase probes", target `15f74e1e` (`docs(jioh/phase-9): 9.15 — the unreleased settle probes question answered (a), release them`), published 2026-10-17T01:39:15Z, https://github.com/logis11/LLM_driven_shceduling/releases/tag/meas-ci-probes-2026-09-20.
- Form, as `meas-ci-probes-2026-10-05`'s: each landed job's artifact re-zipped, its files at the archive's root, as `<artifact>-<run id>.zip`; the gated jobs' `report.json` and `report.kv` in `gated-reports.zip`, one folder `<artifact>-<run id>/` each. The notes take `-10-05`'s sections: the observation and a probe | archive | phases table, what each archive holds, machine draws, reading them.
- Tag date: the probe releases are named by the day their probes ran (KST): `-10-05`'s runs all ran on 2026-10-05, the release made on 10-06; `-10-07` and `-10-07b` on 10-07; `-10-17`'s on 10-17. These five ran on 2026-09-19 (`thunderbird-send`) and 2026-09-20 (the other four); no precedent spans two days, so the answer's name stands.
- Target: `-10-05`, `-10-07` and `-10-07b` target the commit holding the probes' readings and the release's decision (`2ef25705`, 9.10 D158, "(release meas-ci-probes-2026-10-05)"; `9423206a`, 9.10 D173; `07af2d92`, 9.11 D6), not a run's commit; `-10-17` targets its run's launch commit `c130bef6`, its reading not yet committed. These five ran on five commits (below). `15f74e1e` records the answer to release them, and holds every reading (9.5 changelog D44–D94, `campaign/launch-work.md`), the method (9.5 `campaign/method.md` §9) and the reading tool (`dataset/tools/meas/campaign/slices.py`).

## Runs and apps

| run | workflow #, commit | job | app | gate | used |
|---|---|---|---|---|---|
| 35436084336 | `meas-long-probe` #2, `8b86d4b2` | `run (thunderbird-send, 1, 2000)` | `thunderbird-send` (`mail-client`) | open, AMD EPYC 7763 | archive |
| 35494199119 | #3, `feb1ac47` | `run (chrome, 1)` | `chrome` (`web-browser`) | open, AMD EPYC 7763 | archive |
| 35496094029 | #4, `da8b91d7` | `run (code, 1)`, `run (webrtc, 1)` | `code`, `webrtc` | both `wrong-machine`, Intel Xeon 6973P-C | `gated-reports.zip` |
| 35496163876 | #5, `0f373163` | `run (code, 1)`, `run (webrtc, 1)` | `code` (`code-editor`); `webrtc` | `code` open, AMD EPYC 7763; `webrtc` `wrong-machine`, Intel Xeon 6973P-C | `code`: archive; `webrtc`: `gated-reports.zip` |
| 35496212906 | #6, `78b68f3b` | `run (webrtc, 1)` | `webrtc` (`video-call`) | open, AMD EPYC 7763 | archive |

Each job's `report.kv` and `spec.json` (`app`, `gate`, `machine.model`, `GITHUB_RUN_ID`, `GITHUB_SHA`). Phases: `thunderbird-send` and `chrome` 30 s settle, 2,000 s idle; `code` 30 s settle, 1,400 s idle; `webrtc` 30 s settle, 2,000 s play.

## Artifacts

Downloaded through `gh api …/actions/artifacts/<id>/zip`; each zip's local `shasum -a 256` equals the API's `digest`.

| run | artifact | id | bytes | sha256 | expires |
|---|---|---|---|---|---|
| 35436084336 | `meas-long-probe-thunderbird-send-r1-probe` | 10583031053 | 10,839,585 | `7db54ea5016e03faa26a0b5ef9e0ce2957dea60d1ff6109888bf82568bb51cef` | 2026-12-18 |
| 35494199119 | `meas-long-probe-chrome-r1-probe` | 10599679746 | 12,976,973 | `fd25f03f84b9d4bcf65f37fdb221da643addf182f5fedbf1b4a63727e050f6e4` | 2026-12-19 |
| 35496094029 | `meas-long-probe-code-r1-probe` | 10600254652 | 1,162 | `db4887281c412b02cb24006b0c69bf7c03892da25a798a49abd92dc43fb10db6` | 2026-12-19 |
| 35496094029 | `meas-long-probe-webrtc-r1-probe` | 10600905058 | 1,163 | `ac623a5fe0df1130295b733b6966b5254f281347662b51dc28d72dee462f45ee` | 2026-12-19 |
| 35496163876 | `meas-long-probe-code-r1-probe` | 10600691752 | 12,335,897 | `4409ee1e4e731beee0f78d39cde324f2cfeb797cb9a253586a2b2b421ca8508e` | 2026-12-19 |
| 35496163876 | `meas-long-probe-webrtc-r1-probe` | 10600259870 | 1,165 | `b3daf50d728c9b2877a5eeba7851588a1150e2094a1d78572ec92777fec195bd` | 2026-12-19 |
| 35496212906 | `meas-long-probe-webrtc-r1-probe` | 10600742149 | 120,173,691 | `e8a269d152c1c24fe732477d84998a0490d49c19fe209e88de047a77938cf77f` | 2026-12-19 |

## Assets

Each landed archive's files, extracted again from the asset, are byte-identical to the artifact's (`diff -r`): `thunderbird-send` 23 files, `chrome` 18, `code` 19, `webrtc` 16 (no `phases.jsonl` in the runner's artifact). Each asset's local `shasum -a 256` and size equal GitHub's `digest` and `size`.

| asset | bytes | sha256 | run | app |
|---|---|---|---|---|
| `meas-long-probe-thunderbird-send-r1-probe-35436084336.zip` | 10,815,857 | `a72ff848316b3d9ae5debbeb93ea453946dc73a56703ffc36eb38be483971429` | 35436084336 | `thunderbird-send` |
| `meas-long-probe-chrome-r1-probe-35494199119.zip` | 12,941,809 | `015a798ceb24a983c0e4fe5107a1e64af581dabe2b9bae8368c9c592086da5ec` | 35494199119 | `chrome` |
| `meas-long-probe-code-r1-probe-35496163876.zip` | 12,311,655 | `e5635868b64ed21aa3456889271e33281f59b8f1aade1c9946d177aeec542f51` | 35496163876 | `code` |
| `meas-long-probe-webrtc-r1-probe-35496212906.zip` | 119,946,680 | `04dfb666db74c66102c62678a464f2bcd97f28554a33c65857f502492a6b39ae` | 35496212906 | `webrtc` |
| `gated-reports.zip` | 2,433 | `bc1076f1f9b639f64b917ba3093da08cef5dadea3433e2b2af0aaaa146bfbfc3` | 35496094029 (`code`, `webrtc`), 35496163876 (`webrtc`) | the gated jobs |

## Release map

`dataset/meas-releases.yaml`: not mapped. It maps the `meas-ci` campaign tags the data carries; no probe release is in it.
