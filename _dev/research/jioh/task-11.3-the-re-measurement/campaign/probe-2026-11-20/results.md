# background campaign (9.7; 9.10's `upgrade`, `dkms`, `tracker`, `mnist`, `handbrake`, `kdenlive` and `dejadup`) — pooled results

Machine EPYC 7763; stopped by the machine gate 0; other-model repeats 0. Quantile tables are p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9, times in µs, bytes per wake in bytes; the spread is the per-repeat mean. Rules: method §5 and §9.

## mnist

Repeats [2, 5]; mode {2: 'probe', 5: 'probe'}; CPU {2: 'AMD EPYC 7763 64-Core Processor', 5: 'AMD EPYC 7763 64-Core Processor'}; kernel {2: '7.0.0-1017-azure', 5: '7.0.0-1017-azure'}; runs {2: '44731957133', 5: '44732389731'}.

- repeat 2: {'zpaq.version': 'dataset/tools/meas/background/run.sh: line 169: zpaq: command not found', 'perf.version': 'perf version 7.0.14', 'kernel': '7.0.0-1017-azure', 'mmdebstrap.version': 'mmdebstrap 1.4.3', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z'}
- repeat 5: {'zpaq.version': 'dataset/tools/meas/background/run.sh: line 169: zpaq: command not found', 'perf.version': 'perf version 7.0.14', 'kernel': '7.0.0-1017-azure', 'mmdebstrap.version': 'mmdebstrap 1.4.3', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z'}

### mnist-train

command s {2: 1438.886, 5: 1402.236}; rc {2: 0, 5: 0}; program CPU µs (perf) {2: 1438395277.0, 5: 1401887079.0}; (taskstats) {2: 1438346570.7, 5: 1401880118.2}; resumes merged {2: 9280, 5: 8610}; ENOBUFS {2: 0, 5: 0}; cached fraction {2: 1.0, 5: 1.0}

| threads | quantity | n | quantiles | spread (per-repeat mean) |
|---|---|---|---|---|
| all | run_us | 8447 | 3.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 2316 / 10058194 / 37948245 | {2: 294572.0412, 5: 393346.5429} |
| all | wait_us | 8445 | 1.0 / 2.0 / 3.0 / 5.0 / 8.0 / 19.0 / 70.6 / 241 / 1293 / 1481 | {2: 56.0635, 5: 54.9773} |
| all | uninterruptible_us | 8441 | 1.0 / 2.0 / 3.0 / 5.0 / 8.0 / 19.0 / 70.0 / 241 / 1293 / 1481 | {2: 56.0445, 5: 54.9719} |
| all | sleep_us | 4 | 29.2 / 38.2 / 49.5 / 83.2 / 102 / 102 / 103 / 103 / 103 / 103 | {2: 102.5, 5: 64.5} |
| all | batch_run_us | 8447 | 3.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 2316 / 10058194 / 37948245 | {2: 294572.0412, 5: 393346.5429} |
| all | batch_block_us | 8445 | 1.0 / 2.0 / 3.0 / 5.0 / 8.0 / 19.0 / 70.6 / 241 / 1293 / 1481 | {2: 56.0635, 5: 54.9773} |
| `python#1` | run_us | 8447 | 3.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 2316 / 10058194 / 37948245 | {2: 294572.0412, 5: 393346.5429} |
| `python#1` | wait_us | 8445 | 1.0 / 2.0 / 3.0 / 5.0 / 8.0 / 19.0 / 70.6 / 241 / 1293 / 1481 | {2: 56.0635, 5: 54.9773} |

- repeat 2: `python` [28830] /home/user/venv/bin/python threads 1; perf/taskstats CPU 1.0 (thread rows 1.0); disk {'d_state_ns': 273497000, 'blkio_ns': 0, 'coverage': 0.0, 'accounted': False}
- repeat 5: `python` [28291] /home/user/venv/bin/python threads 1; perf/taskstats CPU 1.0 (thread rows 1.0); disk {'d_state_ns': 195755000, 'blkio_ns': 0, 'coverage': 0.0, 'accounted': False}

### Stability rule (D18, D19)

**Does not hold yet** (each table on the list by its mean as the table carries it, count-weighted over the repeats — 9.5 D78; tolerance the larger of 5% and 1 µs for times, at least 5 repeats). Repeats needed at the spread of these repeats: 5.

| quantity | repeats | mean | cv | 95 % half-width | leave-one-out | needed at this spread | passes |
|---|---|---|---|---|---|---|---|
| mnist-train run between voluntary blocks (µs) | 2 | 336247.4673 | 20.3% | ±182.1% | 17.0% | 66 | no |
| mnist-train block per run (µs) | 2 | 55.6052 | 1.4% | ±12.1% | 1.1% | 5 | no |
| mnist-train CPU total (µs) | 2 | 1420141178.0 | 1.8% | ±16.3% | 1.3% | 5 | no |

### Also reported

- state: {2: {'upgrade.layer.packages': '1445', 'upgrade.layer.added': 'python3-venv', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z', 'upgrade.build.rc': '0', 'upgrade.build_s': '709', 'upgrade.t0.installed': '1449', 'upgrade.layer.missing': '0', 'upgrade.layer.extra': '4', 'upgrade.chroot_bytes': '2648678757', 'upgrade.run_systemd_system': 'absent', 'mnist.useradd.rc': '0', 'mnist.python.version': '3.12.3-1ubuntu0.17', 'mnist.venv_pkg.version': '3.12.3-0ubuntu2.1', 'mnist.example.main.py.pin': 'ok', 'mnist.example.README.md.pin': 'ok', 'mnist.example.requirements.txt.pin': 'ok', 'mnist.example.placed.rc': '0', 'mnist.venv.rc': '0', 'mnist.pip.rc': '0', 'mnist.pip_s': '28', 'mnist.torch.version': '2.14.0+cpu', 'mnist.torchvision.version': '0.29.0+cpu', 'mnist.pip-freeze.sha256': '71f26a8f2e000a43cd781a5523c0a153bba99a9a94cadd7a2de8d266300faa2e', 'mnist.venv_bytes': '986562537', 'mnist.warm.rc': '0', 'mnist.warm_s': '10', 'mnist.data.files': '8', 'mnist.data.sha256': 'a3e004ee720c641943c6fb17b1c30ca336461947512280ec620a9005918dfad8', 'mnist.probe.rc': '0', 'mnist.probe.threads': '1', 'mnist.probe.interop_threads': '1', 'cache.mnist-train.fraction': '1.0000', 'cache.mnist-train.torch_lib_fraction': '1.0000', 'mnist.thp_set.rc': '0', 'mnist.train.epochs': '14', 'mnist.train.log_lines': '1316', 'mnist.train.last_test': 'Test set: Average loss: 0.0256, Accuracy: 9916/10000 (99%)', 'mnist.checkpoint.bytes': '4803113', 'mnist.checkpoint.sha256': '18f1b8f519e65fc9cc695c4d2d726f110756061d783c450a4856a07516152d9e'}, 5: {'upgrade.layer.packages': '1445', 'upgrade.layer.added': 'python3-venv', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z', 'upgrade.build.rc': '0', 'upgrade.build_s': '518', 'upgrade.t0.installed': '1449', 'upgrade.layer.missing': '0', 'upgrade.layer.extra': '4', 'upgrade.chroot_bytes': '2648678182', 'upgrade.run_systemd_system': 'absent', 'mnist.useradd.rc': '0', 'mnist.python.version': '3.12.3-1ubuntu0.17', 'mnist.venv_pkg.version': '3.12.3-0ubuntu2.1', 'mnist.example.main.py.pin': 'ok', 'mnist.example.README.md.pin': 'ok', 'mnist.example.requirements.txt.pin': 'ok', 'mnist.example.placed.rc': '0', 'mnist.venv.rc': '0', 'mnist.pip.rc': '0', 'mnist.pip_s': '28', 'mnist.torch.version': '2.14.0+cpu', 'mnist.torchvision.version': '0.29.0+cpu', 'mnist.pip-freeze.sha256': '71f26a8f2e000a43cd781a5523c0a153bba99a9a94cadd7a2de8d266300faa2e', 'mnist.venv_bytes': '986562537', 'mnist.warm.rc': '0', 'mnist.warm_s': '12', 'mnist.data.files': '8', 'mnist.data.sha256': 'a3e004ee720c641943c6fb17b1c30ca336461947512280ec620a9005918dfad8', 'mnist.probe.rc': '0', 'mnist.probe.threads': '1', 'mnist.probe.interop_threads': '1', 'cache.mnist-train.fraction': '1.0000', 'cache.mnist-train.torch_lib_fraction': '1.0000', 'mnist.thp_set.rc': '0', 'mnist.train.epochs': '14', 'mnist.train.log_lines': '1316', 'mnist.train.last_test': 'Test set: Average loss: 0.0256, Accuracy: 9916/10000 (99%)', 'mnist.checkpoint.bytes': '4803113', 'mnist.checkpoint.sha256': '18f1b8f519e65fc9cc695c4d2d726f110756061d783c450a4856a07516152d9e'}}
- cached_fraction: {'mnist-train': {2: 1.0, 5: 1.0}}
