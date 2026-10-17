# Task 9.12 — runner campaign `meas-ci:costs`: method

Fixed 2026-10-09 before the first gated batch (changelog D31), under `../../measurement-campaign-workflow.md`. Scope-card items 28 (the proposal's kernel quantities) and 29 (local inference latency). Workflow `.github/workflows/meas-costs.yml`, trigger `.github/campaign-costs.json`; tools `dataset/tools/meas/costs/` and `dataset/tools/meas/llm/`. Dry run: run 37859640740 (2026-10-08, no machine gate; two kernel repeats on the EPYC 7763, one LLM repeat on an EPYC 9V45).

## The machine

The dataset's: a 4-vCPU `ubuntu-24.04` runner on the AMD EPYC 7763 under the machine gate (`dataset/tools/meas/machine_gate.sh`); kernel 6.17.0-1022-azure in the dry run, `CONFIG_PREEMPT_VOLUNTARY`, `CONFIG_HZ=1000`, the image's mitigations (`kconfig.txt`, `vulnerabilities.txt` per repeat).

## Job `kernel` — what a repeat is

One job on a fresh runner, identical work. Every load is pinned to the measured CPU (`pin.sh`, CPU 3); the script runs on the others.

1. **Context-switch cost.** Five runs each, alternated, of 10⁶ round trips of `pingpong pair` (two processes passing one byte over two pipes: two switches and, over both processes, two writes and two blocking reads per round trip; the system's switch count over the loop recorded) and 10⁶ write+read pairs of `pingpong self` (one process, its own pipe, no switch). Five runs of `perf bench sched pipe -l 1000000`. lmbench `lat_ctx -P 1 -W 3 -N 11 -s <size> 2` at 0, 16 and 64 KB.
2. **The fair class's pick, per call.** ftrace's function-graph tracer on the measured CPU alone, one function hooked at a time (`set_ftrace_filter` and `set_graph_function` naming it, depth 1): `pick_next_task_fair` (`kernel/sched/fair.c:8771` at v6.17: the EEVDF selection, the put-previous and set-next bookkeeping, and when nothing is runnable, newidle balancing), `pick_task_fair` (the selection), `sched_balance_newidle`; each under three loads — 2·10⁵ ping-pong round trips, `perf bench sched messaging -p -g 2 -l 100` (80 processes), 5 000 sleeps of 1 ms. Calibration: `__task_pid_nr_ns` (getpid's work) under 5·10⁵ getpid calls. The ping-pong and getpid loads also run untraced, so the tracer's whole cost per call is the traced-minus-untraced time over the calls per round trip.
3. **Switch rates at idle.** Three 20 s windows with nothing of the job running: per-CPU context switches (`perf stat -a -A -e context-switches`) and schedule() calls and idle entries (`/proc/schedstat`, `kernel.sched_schedstats=1`).

## Job `llm` — what a repeat is

One job on a fresh runner, identical work. llama.cpp at `bd4eeaa047006cb1fe71999fbd11134b5836e167` (the commit search record S4-08 read), built with CMake, Release, native. Two GGUF files, each checked by its SHA-256: Qwen2.5-3B-Instruct Q4_K_M (`Qwen/Qwen2.5-3B-Instruct-GGUF` at `7dabda4d`, 2 104 932 768 bytes, `626b4a66…`) and Meta Llama 3.1 8B Instruct Q4_K_M (`bartowski/Meta-Llama-3.1-8B-Instruct-GGUF` at `bf5b95e9`, 4 920 739 232 bytes, `7b064f58…`) — the two models of LocalScore's records (S3-05). Per model, page cache dropped: `llama-server` with 4 threads on every CPU, `-c 4096 -np 1`; the time from start to `/health` answering; then `request.py` — the chat of `prompt.json` (a stand-in recognizer request: the menu and attribute of `docs/recognition-vocabulary.md` §1, and `c2-p2a`'s telemetry snapshot at its 60 s set change in the frozen shape of `docs/data-contracts.md` §4; 437 prompt tokens for the 3B and 454 for the 8B in the dry run) through the server's chat template, `POST /completion` with temperature 0, seed 1, `cache_prompt` false and a JSON schema: one warm-up, then five each of `schema.system.json` (the `system` block alone) and `schema.full.json` (`reasoning` and `situation`, then `system`), alternated. Then `llama-bench -t 4 -p 512 -n 64 -r 3`.

## The list

Each value is a per-repeat value tested by its per-repeat values (the workflow's rule: 95 % t half-width within 5 % of the mean, at least five EPYC 7763 repeats).

- `kernel`: `pair_ns_per_round_trip`, `self_ns_per_pair`, `switch_ns_direct` (= (pair − 2 × self) / 2), `perf_pipe_us_per_op`, `lat_ctx_us` at 0, 16 and 64 KB; per load, the median and mean duration of `pick_next_task_fair` and of `pick_task_fair`, and `sched_balance_newidle`'s under the sleeper; the calibration's median and the tracer's whole cost per call; at idle, the measured CPU's context switches and schedule() calls per second and the four CPUs' sum.
- `llm`: per model and schema, the mean over the five requests of the wall time, the prompt and generation times and the generated tokens; per model, the load time and llama-bench's prompt and generation rates.

## The smallest effect

None is reported: the values ground stated quantities and no two are compared. The tolerance is the workflow's 5 % (design).

## First batch

Twelve repeats of each job, indices 1–12. The EPYC 7763 was 26 of 56 and 22 of 45 recorded draws (the workflow's figures), about 45 %, so twelve draws land about five. Gated indices are replaced by new indices in one push (identical work); then one at a time until every value holds.

## Amendments

- 2026-10-09, four values leave the list (changelog D55, by 인지오's decision) — `kernel`'s measured CPU's context switches and schedule() calls per second at idle, the median of `pick_next_task_fair` under the sleeper and the mean of `sched_balance_newidle` under the sleeper leave the list: no stated quantity rests on them, and over the 19 repeats they held ±7.96 %, ±18.39 %, ±7.81 % and ±6.49 %, the pool projecting 45, 227, 43 and 31 repeats. `results.md` keeps them as observed ranges. The list's other 23 `kernel` values and the 30 `llm` values hold the rule.
