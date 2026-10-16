# M6 — `video-editor`'s idle state re-probed over `c3-creation`'s span

인지오's answer (a), 2026-10-17, to K06's M6 question (`../work-list.md`): a Kdenlive idle probe at least 2,852 s past the 240 s settle, read on 9.10 D143's standard. Method: `../campaign/spans/method.md` (committed before the launch).

## Configuration and its ground

| item | value | ground |
|---|---|---|
| family, index | `long-probe`, `kdenlive` 13 | the next index after 9.10's `kdenlive` 10 (idle), 11 and 12 (driven); every index the trigger ever named, from its history: `kdenlive` 10, 11, 12 |
| mode | `probe`, plain idle, no input | 9.10 D146's idle phase runs before any input (no driver in `run.sh` mode `idle`); `kdenlive` 10, the probe behind D146, ran in `probe` |
| settle | 30 s | `run.sh`'s `probe` mode fixes `SETTLE=30`; it is the tooling's only long plain idle phase (`idle` runs `idle_for`'s 180 s; `probe-driven` adds driven windows). 9.10 D146 read `kdenlive` 10 past the 240 s settle by leaving out the phase's first 210 s; this reading does the same |
| `phase_s` | 3,100 s | the span past a 30 s settle is 210 + 2,851 = 3,061 s, rounded up to the next 100 s as 9.10 D143 set the first probes' lengths ("the span rounded up": 2,976 → 3,000 s, 1,429 → 1,500 s; 100 s is the finest unit consistent with both) |
| held past the 240 s settle | 2,890 s | 3,100 − 210; ≥ 2,852 s, margin 39 s over the 2,851 s span |
| dry run | none | 9.10 dry-ran only new modes (`probe-driven`, d24a91fd6; `probe-driven-reset`, f72b981b0); `kdenlive` 10 and `soffice` 10 (`probe`) and `kdenlive` 12 (a repeat of 11's mode) launched without one |
| machine | `cpu_model: EPYC 7763` | `machine_gate.sh`; gated jobs relaunched at the same index ("gated windows retried", cce91ceab) |

The span: `c3-creation` holds `video-editor` idle from 360.6 s (the 240.6 s launch replay from the 120 s arrival) to its 3,212 s depart (`dataset/timelines/coreset/c3-creation.timeline.yaml:29`), 2,851.4 s.

## Commits and runs

- `8d3f4aeb` — `docs(jioh/phase-9): 9.15 M6 — …: the method` (`campaign/spans/method.md` only).
- `c130bef6` — `chore(jioh/phase-9): campaign — span probe launched, not a repeat (kdenlive 13, 3,100 s idle; 9.15 M6, 9.10 D143)` (`.github/campaign-long-probe.json` only: `mode probe`, `attempt` 11 → 12, `apps [kdenlive]`, `repeats {kdenlive: [13]}`, `phase_s.kdenlive` 3,000 → 3,100). Pushed 2026-10-16T22:38Z.
- Run 38976976741 (`meas-long-probe` #13), job `run (kdenlive, 13)`: 22:38:55Z–23:33:33Z on 2026-10-16 UTC (2026-10-17 KST), 3,278 s, landed on the first draw. No gated job, so no retry.

## Validity (method §2)

- Gate open: `machine.model` AMD EPYC 7763 64-Core Processor, `gate=open`.
- `settle_s=30`, `idle_s=3100`, `mode=probe`; `perf.idle.record.rc=0`, `perf.idle.timehist.rc=0`; the phase 3,100.002 s in the trace (310 slices), `idle.wall_s=3103.16`.
- Screenshots after the settle and after the phase show Kdenlive holding the project (the clip on V1 with Sharp/Unsharp); `after-idle.png` is byte-identical to `kdenlive` 10's.
- Build: `kdenlive 4:23.08.5-0ubuntu4`, `melt 7.22.0-1build6` (apt log), as every carried campaign's; kernel 6.17.0-1022-azure, Ubuntu 24.04.5, 16 GB (`spec.json`), as `kdenlive` 10's.

## Artifact and release

- Actions artifact `meas-long-probe-kdenlive-r13-probe` (run 38976976741): 15,828,750 bytes, digest `sha256:bbab7f6bc905e00e6da424de740634021ceaa9416c11a49f6b209b1140f32603`, expires 2027-01-14.
- Release `meas-ci-probes-2026-10-17`, "meas-ci probes 2026-10-17 — 9.15 Kdenlive idle span probe", target `c130bef6`, https://github.com/logis11/LLM_driven_shceduling/releases/tag/meas-ci-probes-2026-10-17. In `meas-ci-probes-2026-10-05`'s form: the artifact's 17 files re-zipped as `<artifact>-<run id>.zip`; no `gated-reports.zip`, no job having stopped at the gate.
  - `meas-long-probe-kdenlive-r13-probe-38976976741.zip`: 15,796,143 bytes, sha256 `a0e6c258b87859f81c56269a8b3f8bdc4264cc145ac307f7ab547174c9397287` (local `shasum -a 256` and GitHub's `digest` agree).
- `dataset/meas-releases.yaml`: not mapped. The map holds the `meas-ci` campaign tags the data carries; no probe release (`meas-ci-probes-2026-10-05`, `-10-07`, `-10-07b`) is in it. `make -C dataset lint PY=python3.12`: `lint clean` (the default `python3` lacks `jsonschema_rs`).

## Check of the reading on `kdenlive` 10

The reading (`span_probe.py`'s `phase_slices` at 10 s, the first 21 slices left out, then `level_reading`) on `kdenlive` 10 (`meas-long-probe-kdenlive-r10-probe-37264996600.zip`, release `meas-ci-probes-2026-10-05`) over 2,790 s reproduces 9.10 D146's figures to the printed digit:

| phase | CPU placement, worst | wakes placement, worst | D146 |
|---|---|---|---|
| 120 s | −2.0 %, +5.5 % (at 1,110 s) | −0.4 %, +6.4 % (at 2,420 s) | −2.0 %, +5.5 %; −0.4 %, +6.4 % |
| 180 s | −1.1 %, +4.6 % (at 1,930 s) | −0.7 %, +3.9 % (at 2,410 s) | −1.1 %, +4.6 %; −0.7 %, +3.9 % |
| 300 s | −1.3 %, −2.9 % | +1.3 %, +3.3 % | −1.3 %, −2.9 %; +1.3 %, +3.3 % |

Level over 2,790 s: CPU 0.0651 ms/s, wakes 1.2136/s.

## The reading of `kdenlive` 13

`span_probe.py`'s `phase_slices(run, "idle", 10)`: 310 slices; the first 21 left out; 289 slices, 2,890 s past the 240 s settle. Then `level_reading(cpu[21:], wakes[21:], 10, 180, 2860)`: the span 2,851 s in whole slices (286). Output: `../campaign/spans/results/video-editor-idle.level.json`.

| phase | span | CPU ms/s: level, placement, worst | wakes/s: level, placement, worst | D143 (placement ≤ 5 %) | D146 / 9.5 D53 (placement and worst ≤ 5 %) |
|---|---|---|---|---|---|
| **180 s (carried)** | **2,860 s** | **0.0710, −0.3 %, +4.5 % at 920 s** | **1.2199, +2.9 %, +3.8 % at 370 s** | **holds** | **holds** |
| 180 s | 2,851 s (precedent form: 285 slices, 2,850 s) | 0.0710, −0.3 %, +4.5 % at 920 s | 1.2200, +2.9 %, +3.8 % at 370 s | holds | holds |
| 180 s | 2,890 s (the whole probe past the settle) | 0.0709, −0.3 %, +4.5 % at 920 s | 1.2197, +2.9 %, +3.85 % at 370 s | holds | holds |
| 120 s | 2,851 s | 0.0710, +0.8 %, +4.99 % at 980 s | 1.2200, +5.2 %, +6.6 % at 430 s | fails (wakes) | fails |
| 300 s | 2,851 s | 0.0710, −0.6 %, −3.0 % at 1,560 s | 1.2200, +2.7 %, +3.0 % at 250 s | holds | holds |

Placements and worst offsets are past the 240 s settle. Against `kdenlive` 10 over 2,790 s (level CPU 0.0651, wakes 1.2136): the wake level 0.5 % higher, the CPU level 9 % higher (0.290 s of tree CPU over 3,100 s against 0.240 s over 3,000 s).

**The main thread's episodes.** Past the 240 s settle the main thread `kdenlive` wakes 11 times in most 10 s slices (264 of 289) and 15 times in 11 slices spread through the phase (at 30–40 s, 250 s, 460 s, 530 s, 1,030 s, 1,180 s, 1,520–1,530 s, 2,070 s and 2,110 s past the settle); `kdenlive` 10 holds 8 such slices in 279 (at 220–230 s, 490 s, 1,530 s, 1,960 s, 2,490–2,520 s and 2,730 s). The carried 180 s placement catches two of them, 30–50 s into it (wakes +2.9 %; `kdenlive` 10's placement caught none, −0.7 %), and a 120 s placement weighs them enough to read +5.2 %. They recur through both probes, so they are not launch work past the settle.

## Verdict

The carried 180 s idle phase (9.10 D146) holds over the full 2,851 s span `c3-creation` holds `video-editor` idle, on 9.10 D143's standard: at the placement every repeat takes, CPU −0.3 % and wakes +2.9 % of the probe's level over the span (0.0710 ms/s, 1.2199/s), both within 5 %. It also holds on D146's own standard (9.5 D53), the worst placement CPU +4.5 % (at 920 s) and wakes +3.8 % (at 370 s). D146's phase length does not reopen.

Facts for the scope: one long-phase probe, `kdenlive` 13 of the `long-probe` family, run 2026-10-17 (KST; 2026-10-16 22:39–23:33 UTC), 3,100 s past a 30 s settle, read 2,890 s past the 240 s settle (the span 2,851 s, read over 2,860 s); release `meas-ci-probes-2026-10-17`.
