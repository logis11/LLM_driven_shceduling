# `meas-ci:costs:2026-10-08` — pooled results

Campaign of 9.12 (changelog D31; method `method.md`). Runs: dry run 37859640740 (not repeats); first batch 37860888052 (kernel 1–12, llm 1–12, launched 2026-10-08 23:42 UTC); added batches 37861874535 (kernel 13–36, llm 13–36) and 37864232540 (kernel 37–60). Machine gate: AMD EPYC 7763; every pooled repeat on kernel `6.17.0-1022-azure`. Pooled by `dataset/tools/meas/costs/pool.py ~/.cache/meas-loop/costs --cpu-model "EPYC 7763" --out <this folder>`; the full per-repeat record is `results/pooled.json`, the table below `results/pool.txt` verbatim. `±%` is the 95 % t half-width over the per-repeat values relative to their mean; `need` the first repeat count at which the present spread holds 5 %.

The llm job's `llama3.1-8b` values pool two prompts: Llama 3.1's chat template writes the day into its system header, so repeats 6 and 8 (2026-10-08 UTC) read "Today Date: 08 Oct 2026" and the other nine "09 Oct 2026" — the same length, a different input; the `full` answer is 79 tokens on the first and 71 on the second, identical within each.

```

== kernel: 19 repeats on the EPYC 7763 (11@37860888052, 13@37861874535, 19@37861874535, 24@37861874535, 27@37861874535, 2@37860888052, 36@37861874535, 3@37860888052, 41@37864232540, 42@37864232540, 46@37864232540, 47@37864232540, 48@37864232540, 49@37864232540, 50@37864232540, 53@37864232540, 54@37864232540, 57@37864232540, 9@37860888052)
value                                                  k         mean          min          max      ±%  need pass
__task_pid_nr_ns.getpid.median_ns                     19      260.947      260.000      261.000    0.04     5 yes
__task_pid_nr_ns.getpid.tracer_ns_per_call            19      576.089      571.565      578.829    0.14     5 yes
idle.cs_per_s.all_cpus                                19      319.825      278.656      384.247    3.54    11 yes
idle.cs_per_s.measured_cpu                            19       76.948       61.011      108.290    7.96    45 no
idle.schedule_per_s.measured_cpu                      19      329.851      117.065      567.225   18.39   227 no
lat_ctx_us_0k                                         19        2.382        2.240        2.440    1.17     5 yes
lat_ctx_us_16k                                        19        2.415        2.280        2.480    1.21     5 yes
lat_ctx_us_64k                                        19        2.441        2.280        2.530    1.30     5 yes
pair_ns_per_round_trip                                19     6454.194     6216.474     6553.167    0.74     5 yes
perf_pipe_us_per_op                                   19        5.625        5.415        5.709    0.78     5 yes
pick_next_task_fair.messaging.mean_ns                 19     1030.727      899.150     1126.010    2.46     7 yes
pick_next_task_fair.messaging.median_ns               19      892.000      811.000      972.000    2.14     6 yes
pick_next_task_fair.pingpong.mean_ns                  19      797.682      768.780      812.050    0.61     5 yes
pick_next_task_fair.pingpong.median_ns                19      795.579      771.000      811.000    0.64     5 yes
pick_next_task_fair.pingpong.tracer_ns_per_call       19      929.110      779.012      970.402    2.87     8 yes
pick_next_task_fair.sleep.mean_ns                     19      742.010      642.250      830.110    3.50    11 yes
pick_next_task_fair.sleep.median_ns                   19      810.579      481.000      902.000    7.81    43 no
pick_task_fair.messaging.mean_ns                      19      628.779      544.610      746.130    4.28    15 yes
pick_task_fair.messaging.median_ns                    19      547.842      501.000      621.000    3.07     9 yes
pick_task_fair.pingpong.mean_ns                       19      495.518      484.320      501.200    0.46     5 yes
pick_task_fair.pingpong.median_ns                     19      493.316      481.000      501.000    0.52     5 yes
pick_task_fair.pingpong.tracer_ns_per_call            19      962.779      838.681     1059.232    2.14     6 yes
pick_task_fair.sleep.mean_ns                          19      438.668      412.440      467.860    1.73     5 yes
pick_task_fair.sleep.median_ns                        19      438.632      411.000      460.000    1.59     5 yes
sched_balance_newidle.sleep.mean_ns                   19      700.208      470.800      842.490    6.49    31 no
self_ns_per_pair                                      19      813.501      808.946      818.808    0.16     5 yes
switch_ns_direct                                      19     2413.596     2294.787     2459.037    0.98     5 yes

== llm: 11 repeats on the EPYC 7763 (13@37861874535, 19@37861874535, 22@37861874535, 24@37861874535, 26@37861874535, 27@37861874535, 28@37861874535, 32@37861874535, 35@37861874535, 6@37860888052, 8@37860888052)
value                                                  k         mean          min          max      ±%  need pass
llama3.1-8b.bench.pp512_tps                           11       14.094       13.941       14.214    0.34     5 yes
llama3.1-8b.bench.tg64_tps                            11        7.463        7.201        7.584    1.24     5 yes
llama3.1-8b.full.parses                               11        1.000        1.000        1.000    0.00     5 yes
llama3.1-8b.full.predicted_ms                         11    10746.479    10246.916    11943.940    3.64     8 yes
llama3.1-8b.full.predicted_n                          11       72.454       71.000       79.000    3.00     6 yes
llama3.1-8b.full.prompt_ms                            11    32680.875    32515.022    32921.121    0.28     5 yes
llama3.1-8b.full.prompt_n                             11      454.000      454.000      454.000    0.00     5 yes
llama3.1-8b.full.wall_ms                              11    43429.953    42764.201    44745.240    0.92     5 yes
llama3.1-8b.load_ms                                   11    15251.182    15028.000    15677.000    0.68     5 yes
llama3.1-8b.system.parses                             11        1.000        1.000        1.000    0.00     5 yes
llama3.1-8b.system.predicted_ms                       11     3713.323     3602.109     3853.458    1.58     5 yes
llama3.1-8b.system.predicted_n                        11       26.000       26.000       26.000    0.00     5 yes
llama3.1-8b.system.prompt_ms                          11    32671.250    32484.819    32909.109    0.30     5 yes
llama3.1-8b.system.prompt_n                           11      454.000      454.000      454.000    0.00     5 yes
llama3.1-8b.system.wall_ms                            11    36387.333    36122.922    36623.330    0.31     5 yes
qwen2.5-3b.bench.pp512_tps                            11       35.210       35.029       35.439    0.24     5 yes
qwen2.5-3b.bench.tg64_tps                             11       17.205       16.826       17.557    1.08     5 yes
qwen2.5-3b.full.parses                                11        1.000        1.000        1.000    0.00     5 yes
qwen2.5-3b.full.predicted_ms                          11     4942.366     4837.303     5089.092    1.19     5 yes
qwen2.5-3b.full.predicted_n                           11       76.000       76.000       76.000    0.00     5 yes
qwen2.5-3b.full.prompt_ms                             11    12538.164    12439.123    12801.042    0.55     5 yes
qwen2.5-3b.full.prompt_n                              11      437.000      437.000      437.000    0.00     5 yes
qwen2.5-3b.full.wall_ms                               11    17484.150    17296.359    17691.282    0.46     5 yes
qwen2.5-3b.load_ms                                    11     6682.818     6490.000     6730.000    0.66     5 yes
qwen2.5-3b.system.parses                              11        1.000        1.000        1.000    0.00     5 yes
qwen2.5-3b.system.predicted_ms                        11     1567.212     1539.826     1613.703    1.10     5 yes
qwen2.5-3b.system.predicted_n                         11       25.000       25.000       25.000    0.00     5 yes
qwen2.5-3b.system.prompt_ms                           11    12526.733    12397.750    12704.434    0.42     5 yes
qwen2.5-3b.system.prompt_n                            11      437.000      437.000      437.000    0.00     5 yes
qwen2.5-3b.system.wall_ms                             11    14097.453    13984.363    14299.967    0.40     5 yes

not pooled (gate or model): 66
```
