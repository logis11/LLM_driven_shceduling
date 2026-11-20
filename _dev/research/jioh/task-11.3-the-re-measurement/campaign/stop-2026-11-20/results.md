# background campaign (9.7; 9.10's `upgrade`, `dkms`, `tracker`, `mnist`, `handbrake`, `kdenlive` and `dejadup`) — pooled results

Machine EPYC 7763; stopped by the machine gate 0; other-model repeats 0. Quantile tables are p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9, times in µs, bytes per wake in bytes; the spread is the per-repeat mean. Rules: method §5 and §9.

## mnist

Repeats [17, 29]; mode {17: 'full', 29: 'full'}; CPU {17: 'AMD EPYC 7763 64-Core Processor', 29: 'AMD EPYC 7763 64-Core Processor'}; kernel {17: '7.0.0-1017-azure', 29: '7.0.0-1017-azure'}; runs {17: '44723839046', 29: '44723839046'}.

- repeat 17: {'zpaq.version': 'dataset/tools/meas/background/run.sh: line 169: zpaq: command not found', 'perf.version': 'perf version 7.0.14', 'kernel': '7.0.0-1017-azure', 'mmdebstrap.version': 'mmdebstrap 1.4.3', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z'}
- repeat 29: {'zpaq.version': 'dataset/tools/meas/background/run.sh: line 169: zpaq: command not found', 'perf.version': 'perf version 7.0.14', 'kernel': '7.0.0-1017-azure', 'mmdebstrap.version': 'mmdebstrap 1.4.3', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z'}

### mnist-train

command s {17: 1628.652, 29: 1613.133}; rc {17: 0, 29: 0}; program CPU µs (perf) {17: 1627071870.0, 29: 1611402208.0}; (taskstats) {17: 1627041457.6, 29: 1611371013.5}; resumes merged {17: 7717, 29: 7750}; ENOBUFS {17: 0, 29: 0}; cached fraction {17: 1.0, 29: 1.0}

| threads | quantity | n | quantiles | spread (per-repeat mean) |
|---|---|---|---|---|
| all | run_us | 20674 | 2.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 4416 / 5066600 / 11237087 | {17: 169698.7766, 29: 145354.7003} |
| all | wait_us | 20672 | 1.0 / 2.0 / 3.0 / 5.0 / 7.0 / 32.0 / 405 / 744 / 2598 / 4204 | {17: 143.599, 29: 137.0075} |
| all | uninterruptible_us | 20668 | 1.0 / 2.0 / 3.0 / 5.0 / 7.0 / 32.0 / 405 / 744 / 2598 / 4204 | {17: 143.6085, 29: 137.014} |
| all | sleep_us | 4 | 95.2 / 95.8 / 96.5 / 98.8 / 101 / 102 / 102 / 102 / 102 / 102 | {17: 98.5, 29: 101.0} |
| all | batch_run_us | 20674 | 2.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 4416 / 5066600 / 11237087 | {17: 169698.7766, 29: 145354.7003} |
| all | batch_block_us | 20672 | 1.0 / 2.0 / 3.0 / 5.0 / 7.0 / 32.0 / 405 / 744 / 2598 / 4204 | {17: 143.599, 29: 137.0075} |
| `python#1` | run_us | 20674 | 2.0 / 3.0 / 3.0 / 3.0 / 3.0 / 4.0 / 4.0 / 4416 / 5066600 / 11237087 | {17: 169698.7766, 29: 145354.7003} |
| `python#1` | wait_us | 20672 | 1.0 / 2.0 / 3.0 / 5.0 / 7.0 / 32.0 / 405 / 744 / 2598 / 4204 | {17: 143.599, 29: 137.0075} |

- repeat 17: `python` [28924] /home/user/venv/bin/python threads 1; perf/taskstats CPU 1.0 (thread rows 1.0); disk {'d_state_ns': 1376486999, 'blkio_ns': 0, 'coverage': 0.0, 'accounted': False}
- repeat 29: `python` [28860] /home/user/venv/bin/python threads 1; perf/taskstats CPU 1.0 (thread rows 1.0); disk {'d_state_ns': 1518525999, 'blkio_ns': 0, 'coverage': 0.0, 'accounted': False}

### Stability rule (D18, D19)

**Does not hold yet** (each table on the list by its mean as the table carries it, count-weighted over the repeats — 9.5 D78; tolerance the larger of 5% and 1 µs for times, at least 5 repeats). Repeats needed at the spread of these repeats: 5.

| quantity | repeats | mean | cv | 95 % half-width | leave-one-out | needed at this spread | passes |
|---|---|---|---|---|---|---|---|
| mnist-train run between voluntary blocks (µs) | 2 | 156644.775 | 10.9% | ±98.2% | 8.3% | 21 | no |
| mnist-train block per run (µs) | 2 | 140.0644 | 3.3% | ±29.7% | 2.5% | 5 | no |
| mnist-train CPU total (µs) | 2 | 1619237039.0 | 0.7% | ±6.2% | 0.5% | 5 | no |

### Also reported

- state: {17: {'upgrade.layer.packages': '1445', 'upgrade.layer.added': 'python3-venv', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z', 'upgrade.build.rc': '0', 'upgrade.build_s': '702', 'upgrade.t0.installed': '1449', 'upgrade.layer.missing': '0', 'upgrade.layer.extra': '4', 'upgrade.chroot_bytes': '2648678757', 'upgrade.run_systemd_system': 'absent', 'mnist.useradd.rc': '0', 'mnist.python.version': '3.12.3-1ubuntu0.17', 'mnist.venv_pkg.version': '3.12.3-0ubuntu2.1', 'mnist.example.main.py.pin': 'ok', 'mnist.example.README.md.pin': 'ok', 'mnist.example.requirements.txt.pin': 'ok', 'mnist.example.placed.rc': '0', 'mnist.venv.rc': '0', 'mnist.pip.rc': '0', 'mnist.pip_s': '30', 'mnist.torch.version': '2.14.0+cpu', 'mnist.torchvision.version': '0.29.0+cpu', 'mnist.pip-freeze.sha256': '71f26a8f2e000a43cd781a5523c0a153bba99a9a94cadd7a2de8d266300faa2e', 'mnist.venv_bytes': '986562537', 'mnist.warm.rc': '0', 'mnist.warm_s': '12', 'mnist.data.files': '8', 'mnist.data.sha256': 'a3e004ee720c641943c6fb17b1c30ca336461947512280ec620a9005918dfad8', 'mnist.probe.rc': '0', 'mnist.probe.threads': '1', 'mnist.probe.interop_threads': '1', 'cache.mnist-train.fraction': '1.0000', 'cache.mnist-train.torch_lib_fraction': '1.0000', 'mnist.train.epochs': '14', 'mnist.train.log_lines': '1316', 'mnist.train.last_test': 'Test set: Average loss: 0.0256, Accuracy: 9916/10000 (99%)', 'mnist.checkpoint.bytes': '4803113', 'mnist.checkpoint.sha256': '18f1b8f519e65fc9cc695c4d2d726f110756061d783c450a4856a07516152d9e'}, 29: {'upgrade.layer.packages': '1445', 'upgrade.layer.added': 'python3-venv', 'upgrade.layer.sha256': 'b137960b535edc27c16e04454779edc65d0fdc2b32f9a55a6335f22031df87d9', 'upgrade.t0': '20260922T170000Z', 'upgrade.t1': '20260728T000000Z', 'upgrade.build.rc': '0', 'upgrade.build_s': '604', 'upgrade.t0.installed': '1449', 'upgrade.layer.missing': '0', 'upgrade.layer.extra': '4', 'upgrade.chroot_bytes': '2648678757', 'upgrade.run_systemd_system': 'absent', 'mnist.useradd.rc': '0', 'mnist.python.version': '3.12.3-1ubuntu0.17', 'mnist.venv_pkg.version': '3.12.3-0ubuntu2.1', 'mnist.example.main.py.pin': 'ok', 'mnist.example.README.md.pin': 'ok', 'mnist.example.requirements.txt.pin': 'ok', 'mnist.example.placed.rc': '0', 'mnist.venv.rc': '0', 'mnist.pip.rc': '0', 'mnist.pip_s': '28', 'mnist.torch.version': '2.14.0+cpu', 'mnist.torchvision.version': '0.29.0+cpu', 'mnist.pip-freeze.sha256': '71f26a8f2e000a43cd781a5523c0a153bba99a9a94cadd7a2de8d266300faa2e', 'mnist.venv_bytes': '986562537', 'mnist.warm.rc': '0', 'mnist.warm_s': '9', 'mnist.data.files': '8', 'mnist.data.sha256': 'a3e004ee720c641943c6fb17b1c30ca336461947512280ec620a9005918dfad8', 'mnist.probe.rc': '0', 'mnist.probe.threads': '1', 'mnist.probe.interop_threads': '1', 'cache.mnist-train.fraction': '1.0000', 'cache.mnist-train.torch_lib_fraction': '1.0000', 'mnist.train.epochs': '14', 'mnist.train.log_lines': '1316', 'mnist.train.last_test': 'Test set: Average loss: 0.0256, Accuracy: 9916/10000 (99%)', 'mnist.checkpoint.bytes': '4803113', 'mnist.checkpoint.sha256': '18f1b8f519e65fc9cc695c4d2d726f110756061d783c450a4856a07516152d9e'}}
- cached_fraction: {'mnist-train': {17: 1.0, 29: 1.0}}
