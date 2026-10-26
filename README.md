# LLM-driven scheduling

A semantic recognition layer for operating systems, validated on CPU scheduling. An LLM reads the names of the processes a machine is running, works out what the machine is being used for ("gaming, with a download the user is waiting on"), and that reading — never the LLM itself — configures an ordinary scheduler. The experiment measures whether knowing the *meaning* of a workload schedules better than the behavior-watching heuristics and hardcoded app lists shipping systems use today. Full story: [`docs/research-proposal.md`](docs/research-proposal.md).

## Repo structure

| tree | what lives there |
|---|---|
| [`dataset/`](dataset/) | the workload dataset: behavior library, authored timelines, the wlc compiler, compiled coresets (own README) |
| `simulator/` | the discrete-event simulator that plays workloads out under swappable scheduling policies |
| `daemon/` | the recognition side: telemetry → recognizer (LLM and baselines) → validated config schedules |
| `harness/` | the experiment harness: condition matrix, metrics from traces, plots |
| [`docs/`](docs/) | all prose — proposal, contracts, onboarding guides; index and reading paths in [`docs/README.md`](docs/README.md) |
| `_dev/` | team task tracker and working docs |

## Using the dataset without building it

`dataset/build/` and `dataset/generated/` are not committed; `make dataset variants generated` writes them ([`dataset/README.md`](dataset/README.md)). The [`dataset-build-2026-10-26`](https://github.com/logis11/LLM_driven_shceduling/releases/tag/dataset-build-2026-10-26) release holds both, built at `6dec33a0`. Download `dataset-build-2026-10-26.tar.gz` from it and, from the repo root at that commit or a later one whose manifests are unchanged:

```
tar -xzf dataset-build-2026-10-26.tar.gz -C dataset
make -C dataset check PY=python3.12
```

`check` confirms every unpacked file against the hashes the committed manifests pin (Python 3.12 with `dataset/tools/requirements.txt`).

New here? [`docs/README.md`](docs/README.md) has per-role reading paths; builders start with [`docs/background-guide.md`](docs/background-guide.md).
