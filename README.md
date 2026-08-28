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

New here? [`docs/README.md`](docs/README.md) has per-role reading paths; builders start with [`docs/background-guide.md`](docs/background-guide.md).
