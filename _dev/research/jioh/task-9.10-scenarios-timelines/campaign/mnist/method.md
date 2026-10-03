# Task 9.10 — the MNIST training campaign: method (2026-10-03)

The observation behind the three training files, `c1-ml-train`, `c7-ml-train` and `c2-p1a`'s segment 1 (changelog D12, D82–D84), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `mnist` job of `run.sh`, which reuses the upgrade job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `mnist`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<launch date of the first batch>`, lettered if the workflow already holds a campaign of that date (D76); each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the example and the venv installed, the warm start run, the training run measured (§3). Identical work (D84), so an added repeat is the next index. Artifact `meas-background-mnist-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): over the job (§5), the run between voluntary blocks and the block per run, each tested by its mean as the table carries it (the ratio estimator), and the CPU total, tested by its per-repeat values (D17). Fixed with the entry's form after the dry run, by a dated entry in §8.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing, the packages added being `python3-venv`'s; `/run/systemd/system` absent in the chroot; the example's three files each matching its SHA-256; `torch` 2.14.0+cpu and `torchvision` 0.29.0+cpu installed, and one installed set (`pip3 freeze --all`) across the pooled repeats; the dataset's uncompressed files at least 0.99 cached at the start (D83); fourteen test passes in the run's output; the checkpoint written.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the venv's creation and pip's logs, the installed set, the venv's `bin/activate`, the warm start's output and duration, the dataset's files and their SHA-256, the probe's `torch` version, thread counts and parallel backend on the measured CPU, the cached fractions of the dataset and of the shared libraries, the run's own output, the checkpoint's size and SHA-256.

## 2. Inputs (D82, D83)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64), with `python3-venv` in the same build.
- **The user.** A non-root user with a home under `/home`, as the Tracker campaign's.
- **The example.** `pytorch/examples` at `acc295dc7b90714f1bf47f06004fc19a7fe235c4`, `mnist/main.py`, `mnist/README.md` and `mnist/requirements.txt`, fetched on the harness CPUs, each checked by its SHA-256 (S2-31), placed as `~/examples/mnist`, owned by the user.
- **The venv.** `python3 -m venv ~/venv` as the user; in it, PyTorch's command for Linux, pip and the CPU (S2-47), the versions pinned: `pip3 install torch==2.14.0 torchvision==0.29.0 --index-url https://download.pytorch.org/whl/cpu` (S2-48).
- **The dataset.** Placed by the warm start (§3): `torchvision`'s download into `~/examples/data/MNIST/raw` from its first mirror that answers (S2-49).
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| state | the user, the example, the venv and the pinned install (§2) | harness | none |
| warm start | `python main.py --dry-run --epochs 1` as the user, the venv activated, in `~/examples/mnist` (D83) | harness | none |
| probe | `python -c` printing `torch`'s version, intra-op and inter-op thread counts and `torch.__config__.parallel_info()` | measured | none |
| cache check | `fincore` over the dataset's uncompressed files and over the venv's shared libraries | harness | none |
| `mnist-train` | `python main.py --save-model` as the user in the chroot, the venv activated, in `~/examples/mnist`, `taskset` placing it on the measured CPU. The phase ends when the command exits; no cap of its own (the workflow's 330-minute job limit) | measured | §4 |

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D84).** Every process of the tree rooted at the process `taskset` executed into `chroot` (`launched_root`), from its first schedule-in on the measured CPU to its exit; the whole phase.
- **Form.** Fixed after the dry run by a dated entry in §8: `cpu-batch`'s `python3` program re-measured, or an entry of its own, by 9.6 D7's criterion — a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry.
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process and thread counts and CPU by thread; the job's span; the test passes' output; the checkpoint; the job's block-I/O delay and its `sched_stat_iowait` rows.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session. PyTorch's basic MNIST example at its defaults (S2-31), the checkpoint written, on `torch` 2.14.0's CPU build in D37's chroot built at 2026-09-22T17:00Z, from a warm start with the dataset local (D82–D84). The files show an actual training run; they do not claim that desktop users train MNIST, and GPU training is unobservable on the runner (D12).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

None yet.
