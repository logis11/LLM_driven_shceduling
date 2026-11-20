# 11.3 — the training run's re-measurement: method (2026-11-20)

The campaign the finding step names (`../finding.json`): `cpu-batch`'s `python3` program, its run between voluntary blocks at the lower bound of its interval moving `c7-ml-train` across g alone. Its two exception-carried values — the run between voluntary blocks and the block per run — are re-measured by a fresh campaign at a count fixed before the launch (the 11.3 spec, decisions 5 to 7). Amended only by a dated entry in §5.

## 1. The method

The original campaign's, `meas-ci:background:2026-10-03` (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/method.md`, §1 to §6 with its 2026-10-03 amendments), unchanged: workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, app `mnist`, mode `full`, `work_root` `/`; the machine gate on the AMD EPYC 7763; the state at T0 = `20260922T170000Z`, the example at `pytorch/examples@acc295dc7b90714f1bf47f06004fc19a7fe235c4`, `torch` 2.14.0 and `torchvision` 0.29.0 from PyTorch's CPU index; the warm start, the probe, the cache check and the `mnist-train` phase; the instruments, the job's analysis and its validity list. The tooling is the repository's at the launch: the `mnist` job's commands in `dataset/tools/meas/background/run.sh`, its analysis in `analyze.py` and its pool in `pool.py` as they ran the original campaign's last repeat (commit `4c2e667d5f`), the later edits adding other jobs alone.

## 2. Runs

- **Tag.** `meas-ci:background:2026-11-20`.
- **Count.** 107 valid repeats: the count the stability rule projects at the pool as carried — over the original campaign's six repeats (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/results/pooled.json`, `needed`) 107 for the run between voluntary blocks at ±27.31 %, 19 for the block per run at ±10.77 %, the larger taken. The campaign stops at 107 whether or not the 5 % tolerance holds there.
- **Fresh repeats.** Indices 1 to 107, every one a new job; no repeat of the original campaign is pooled.
- **Launch.** The 107 together, one push.
- **Replacement.** A job the machine gate stops is relaunched at its index. A repeat left out under a validity rule of the original method is replaced by the next index from 108, its reason recorded. No repeat is left out for any other reason.
- **Release.** The raw records are a GitHub release, mapped in `dataset/meas-releases.yaml`.

## 3. Read at 107

Over the 107 valid repeats, by the original method's analysis and pool (`dataset/tools/meas/loop/pool_runs.py background/mnist --since <the launch's run number>`, the pool on the EPYC 7763 alone): the run between voluntary blocks and the block per run, each by its mean as the table carries it, with its 95 % half-width and range; the CPU total by its per-repeat values; the other values the pool reports, each beside the library's and inside its stated interval or not (the 11.3 spec, decision 8).

## 4. Differences the venue forces

- The workflow's push trigger names `main` beside `jioh/dataset-rebuild`; the job's steps unchanged. `daemon.yml`, `dataset.yml` and `harness.yml` leave a push changing `.github/campaign-background.json` alone, as one changing `.github/campaign.json`.
- The runner's image and kernel as each job records them.

## 5. Amendments

- 2026-11-20, the stop (runs #199–#208, launched at #199, 44723839046). The first two landings, repeats 17 and 29 (run 44723839046), drew the AMD EPYC 7763 under kernel `7.0.0-1017-azure` and `perf` 7.0.14, the kernel's transparent huge pages `always [madvise] never` before the phase; the original campaign's six ran under `6.17.0-1022-azure`, `perf` 6.17.13, and its validity asks `[always] madvise never` (the original method, §8, 2026-10-03, the first batch). The state's layer, the example and the installed versions as the original's. The job blocked in 9,585 and 11,083 uninterruptible waits, median 7 µs, against 9–22 a repeat, median 365 µs; the run between voluntary blocks 0.157 s against 69.49 s, the block per run 140.1 µs against 311.5 µs, the CPU total 1,619.2 s against 1,389.9 s. The venue changes what is measured: the campaign stopped for 인지오's decision (the 11.3 spec, decision 7) — the watch stopped and runs #199–#208 cancelled, their queued and measuring jobs with them. 121 draws stopped at the machine gate: 80 Intel Xeon 6975P-C, 22 AMD EPYC 9V74, 12 AMD EPYC 9V45, 5 Intel Xeon Platinum 8573C, 2 Intel Xeon Platinum 8370C. The two landed repeats are no repeats of the campaign. Record: `stop-2026-11-20/` — the two repeats' pooled record and its rendering (`dataset/tools/meas/loop/pool_runs.py background/mnist --since 199`), the runs and draws (`draws.json`).
