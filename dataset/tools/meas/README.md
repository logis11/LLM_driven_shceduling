# dataset/tools/meas/

The measurement campaigns' tooling: what runs on a GitHub-hosted runner, and what turns a campaign's landed repeats into the library's values. A map — each tool's own docstring or header comment says what it does and which decisions it follows; the campaigns' design and results are described in `docs/workload/measurement-overview.md`.

A campaign runs in four stages:

- **run** — one job on the runner per program and repeat, run by the family's workflow (`.github/workflows/meas-<family>.yml`), a campaign's jobs started by a push of its trigger file (`.github/campaign*.json`) — `meas-probe.yml` and `meas-sched.yml` by a push of their own workflow or tool files instead (`meas-probe.yml` also by hand), `meas-names.yml` by hand alone; the job stopped by the machine gate if the runner drew another CPU model; the artifacts uploaded.
- **analysis** — one landed run directory read into its per-phase values.
- **pool** — a campaign's landed repeats pooled into the tables an entry carries, with the stability rule evaluated.
- **fold-in** — the pooled record written into `dataset/archetypes.yaml`, or into the stream files under `dataset/launch/` and `dataset/replay/`.

## Shared pieces (this folder)

| Tool | Stage | What it is |
|---|---|---|
| `pin.sh` | run | sourced by the campaigns' `run.sh` (all but `llm/run.sh`, whose server runs on every CPU): each measured load pinned to one CPU, the harness on the others |
| `phase.sh` | run | runs a command inside a named measurement phase, appending its start, end and return code to the phases file |
| `machine_gate.sh` | run | sourced: stops a job whose runner drew another CPU model before it measures anything |
| `runner_spec.py` | run | records the runner's spec beside each repeat |
| `proc_sampler.py` | run | the 1 s `/proc` sampler sidecar (per-process CPU, threads, optionally context switches) |
| `analyze.py` | analysis | the Phase 2 fold-in analysis of the `meas-cli` / `meas-gui` repeats (median and `sigma_log` fits) |
| `distribution.py` | pool | the measured table every campaign carries: ten quantiles, the extremes, the eleven interval means |
| `stability.py` | pool | the stability rule shared by the campaigns: each carried value's 95 % half-width within the tolerance |
| `stopping.py` | pool | the stability rule's stopping simulated at an observed spread |
| `windows.py` | pool | each carried phase read in time windows, per component (`campaign`, `desktop`, `session`) |
| `burstiness.py` | pool | the compiled streams' burstiness against the measured, per repeat (`campaign`, `desktop`, `session`) |
| `control.py`, `control_report.py` | pool | the untraced control's shared core and its report: each value traced and untraced, read per job |
| `batch_fold_in.py` | fold-in | the batch-loop and build tables (`cpu-batch`, `compiler-child`, `build-orchestrator`, `file-archiver`, `game-download`, `package-upgrade`, `module-build-orchestrator`, `module-compiler-child`, `file-indexer`, `video-transcoder`, `incremental-backup`) from their pooled records; `--check` |
| `replay_fold_in.py` | fold-in | the trace-replay streams under `dataset/replay/` from the raw releases; `--check` |
| `verify_names.py` | run | the name-verification instrument of `meas-names.yml`: per catalog name, the `comm`/cmdline strings observed and a verification level |

## Campaign families (subfolders)

| Folder | Campaign | Workflow | Run | Analysis | Pool | Fold-in |
|---|---|---|---|---|---|---|
| `campaign/` | 9.5's interactive and playback campaigns and their long-phase probes, 9.10's `video-editor` idle-phase campaign and span probes, 9.15's span probe | `meas-interactive.yml`, `meas-playback.yml`, `meas-long-probe.yml` | `run.sh` | `analyze.py`, `slices.py`, `span_probe.py`, `wake_check.py` | `pool.py`, `render_results.py`, `control.py`, `control_passes.py` | `fold_in.py` → `splice.py` |
| `build/` | 9.6's build-and-batch campaign | `meas-build.yml` | `run.sh` (with `clamav_db.sh`, `taskstats_listen.c`, `train.py`) | `analyze.py`, `shapes.py` | `pool.py` | `batch_fold_in.py` |
| `background/` | 9.7's background campaign and 9.10's background jobs (the upgrade, the DKMS build, Tracker, the MNIST training, the transcode, the Kdenlive export, Déjà Dup) | `meas-background.yml` | `run.sh` (with `tracker-session.sh`, `dejadup-session.sh`, `dejadup_first.py`, `dejadup_run.py`, `kdenlive_export.py`, `fileset.py`, `hippocamp.py`, `appinfo.py`, `inputs.json`, `upgrade-layer.txt`) | `analyze.py`, `nettrace.py`, `modbuild.py` | `pool.py` | `batch_fold_in.py` |
| `desktop/` | 9.8's desktop campaign and 9.10's launch subjects and tab set | `meas-desktop.yml` | `run.sh` (with `launch.sh`, `launch.py`, `tabs.py`, `traffic.py`, `close_window.py`) | `analyze.py`, `probe_windows.py`, `wake_alignment.py`, `window_spread.py`, `within_run.py` | `pool.py`, `control.py` | `fold_in.py`; `launch_fold_in.py` (→ `dataset/launch/`) |
| `session/` | 9.9's session campaign and 9.10's upgrade probe | `meas-session.yml` | `run.sh` (with `census.py`, `dm_stub.py`) | `analyze.py`, `causes.py`, `size_steady.py`, `within_run.py`, `upgrade_probe.py` | `pool.py`, `control.py` | `fold_in.py` |
| `costs/` | 9.12's kernel-cost campaign | `meas-costs.yml` | `run.sh` (with `pingpong.c`) | `analyze.py`, `graph_durations.py` | `pool.py` | — |
| `llm/` | 9.12's recognizer-latency campaign | `meas-costs.yml` | `run.sh` (with `request.py`, `prompt.json`, `schema.system.json`, `schema.full.json`) | — | — | — |
| `sched/` | 9.11's scheduler readings | `meas-sched.yml` (`tunables.sh`) | `tunables.sh`, the runner kernel's scheduler tunables; `classes.py`, every thread's policy, priority and nice over a job, a sidecar of `campaign/`, `desktop/` and `session/`'s `run.sh` | — | — | — |
| `probe/` | 9.5's runner probe; the applications' install and launch definitions and drivers the campaigns share | `meas-probe.yml` | `apps.sh`, `tools.sh`, `timing.sh`, `common.sh`; shared with the campaigns' `run.sh`: `appdefs.sh`, `snapshot.py`, `replay_stream.py`, `ops_driver.py`, `smtp_peer.py`, the pages (`feed.html`, `idle-page.html`, `webrtc-loopback.html`), `kdenlive_project.py`, `writer_doc.py` | `timing_report.py` | — | — |
| `loop/` | the campaign loop, run on the development machine | — | `launch.py` (writes the trigger file and pushes), `watch.py`, `status.py`, `cut_windows.sh` (the per-repeat input windows under `dataset/meas/streams/`) | — | `pool_runs.py` (downloads the landed repeats, checks each repeat's validity, runs the family's `pool.py`) | — |

The input streams: `probe/swell_streams.py` extracts SWELL-KW's uLog files (listed in `probe/swell-ulog-files.json`); `campaign/build_windows.py` and `probe/aalto_streams.py` cut the per-repeat windows the campaigns replay (SWELL-KW and 136M Keystrokes); `../stimulus/build_streams.py` writes the streams the compiler replays (`dataset/stimulus/`).
