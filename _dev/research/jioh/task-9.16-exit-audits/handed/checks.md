# Task 9.16 — the handed-over items

The items on the 9.16 line of `_dev/TODO.md` that this run covers, read under the 9.16 spec's decision 3: an item that names an intermediate pin is closed by the one dataset-gate run at home and the one CI run on the final build; an item on content that is still current runs as listed. Run 2026-10-17 on branch `jioh/dataset-rebuild` at `928aa8fd`, on the M1 Pro, with the scratchpad venv's Python. The scripts written for this run are in `scripts/`, each taking the repository root as its one argument. Findings, with the fix each one needs, are in `findings.md`.

## Summary

| item | result |
|---|---|
| 9.5 spec decision 13: the venue mix listed per timeline | PASS (the list is below) |
| 9.13: `reads.md` reproduces with its scan scripts | PASS |
| 9.13: every entry's `declared_class` rests on 9.11's class census | FAIL, minor (finding F3) |
| 9.13: the blessed manifest's counts in the changelog's bless entry; the final bless against `dataset/build.manifest.json` | PASS |
| 9.14 decision 1: the mock-media fixture's derivation checks the TIMER skip rule | PASS |
| 9.14 decisions 2 and 6: the input-wake counts per scored task | PASS (the table is below) |
| 9.14 decision 7: the boot-default sweep's step values reproduce from `chain_scan.py` and the entries' tables | FAIL (finding F1) |
| 9.18 decision 6: every timeline's `source` map agrees with `bound-values.md` | PASS |
| 9.19 decision 5: the flap-stress intervals' three sources read at their release tags | FAIL, minor (finding F2); closed by this run's read |
| 9.20 decision 10: `melt-7` and `duplicity` rest on their campaign records; `linux-sched-h` read at v6.17 | PASS |
| 9.21: `scoring_lint.py` over the five generated sets; `gh-hosted-runners` read 2026-10-13 | PASS |
| 9.23 decision 15: the full smoke at home | listed; the lead runs it |
| the items naming 9.17's, 9.18's, 9.22's, 9.19's, 9.20's and 9.21's pins | CLOSED-BY-GATE (the table at the end) |

## 9.5 spec decision 13 — the venue mix per timeline

`scripts/venue.py`. It maps every archetype a timeline binds to that entry's `category_source` in `dataset/archetypes.yaml`, adding the spawned child entries (`compiler-child` under `build-orchestrator`, `module-compiler-child` under `module-build-orchestrator`). The library has two venues (`docs/workload/archetype-plan.md:38`). The first is the runner: 28 entries with `category_source: meas`, every value from one AMD EPYC 7763 core of a GitHub-hosted runner. The second is `lavd-ossna24`: `game-task-chain` alone, taken from the talk's slides and lane-scaled. Script output: `library: Counter({'meas': 28, 'lavd-ossna24': 1})`.

**Core set (51 timelines).** Eight timelines mix the two venues. Each of them binds `game-task-chain`:

| timeline | archetypes bound | venues |
|---|---|---|
| `c1-gaming` | game-client, game-task-chain | lavd-ossna24 + runner |
| `c2-p2a` | game-client, game-download, game-task-chain | lavd-ossna24 + runner |
| `c2-p2a-idle` | game-client, game-download-idle, game-task-chain | lavd-ossna24 + runner |
| `c2-p2b` | game-client, game-task-chain, package-upgrade | lavd-ossna24 + runner |
| `c3-evening` | audio-player, chat-client, game-client, game-task-chain, renderer-hidden, video-player, web-browser | lavd-ossna24 + runner |
| `c4-gaming` | chat-client, game-client, game-task-chain | lavd-ossna24 + runner |
| `c6-dual` | build-orchestrator, code-editor, compiler-child, game-task-chain | lavd-ossna24 + runner |
| `c7-gaming` | game-client, game-task-chain, package-upgrade | lavd-ossna24 + runner |

The other 43 use the runner alone: `c1-backup`, `c1-browsing`, `c1-compile`, `c1-dev`, `c1-idle`, `c1-indexing`, `c1-mail`, `c1-media`, `c1-meeting`, `c1-ml-train`, `c1-office`, `c1-photo`, `c1-render`, `c1-transcode`, `c1-video-edit`, `c2-p1a`, `c2-p1b`, `c2-p3a`, `c2-p3b`, `c3-creation`, `c3-workday`, `c4-compile`, `c4-office`, `c5-t4`, `c5-t5`, `c6-alias`, `c6-fold`, `c6-spoof`, and the C7 counterparts `c7-backup`, `c7-browsing`, `c7-compile`, `c7-dev`, `c7-idle`, `c7-indexing`, `c7-mail`, `c7-media`, `c7-meeting`, `c7-ml-train`, `c7-office`, `c7-photo`, `c7-render`, `c7-transcode`, `c7-video-edit`. The script's full per-timeline rows, with every archetype each timeline binds, are its own output.

**Generated layer (1,562 timelines).** The archetypes were read from each file's `archetype:` tokens, with comments stripped.

| set | lavd-ossna24 + runner | runner only |
|---|---|---|
| transition grid | 60 | 420 |
| return grid | 90 | 630 |
| flap-stress set | 16 | 8 |
| distractor grid | 32 | 240 |
| familiarity ladder | 6 | 60 |

Every generated file that mixes the two venues binds `game-task-chain`. No timeline binds an archetype that is missing from the library.

## 9.13 — the reads, the class census, the bless

**`reads.md` reproduces.** The reads were taken at `27a80abb`. The scan scripts (`_dev/research/jioh/task-9.13-rebuild/scans/`) were run over that commit's `dataset/` tree, extracted with `git archive 27a80abb dataset` into the scratchpad:

- R2, the TIMER-first scan (`timer_scan.py`): "arrive events 270, spawned tasks 79772, wake events 4496190"; "tasks carrying TIMER: 22; literal first op distribution: {'LOOP': 7, 'TIMER': 15}"; by name, `Troy.exe` 7, `mpv` 6, `chrome` 3, and one each of `tracker-miner-f`, `baloo_file`, `audio-stream-he`, `video-playback-`, `xkrr`, `qzvd`; "first-executed-not-TIMER: 0". This equals R2's table (`reads.md:13–20`).
- R4, the set's size (`size_scan.py`): "files 50; total single-lane bytes 665,836,426 (665.8 MB); wakes 4,496,190". The eight largest files match `reads.md:50–57` to the 0.1 MB and the wake: `c6-dual` 189.8 MB / 1,391,059 … `c3-workday` 18.3 MB / 92,827.
- R5, the demand window (`window_scan.py`): "window violations: 9", with `c2-p1a` 14.51, `c2-p2a` 9.38, `c6-dual` 1.00, `c2-p1b` 0.92, `c2-p3b` 0.90, `c3-evening` 0.90, `c3-creation` 0.94, `c3-workday` 0.89, `c2-p3a` 0.44; "demand classes: {'calibration': 40, 'oversubscribed': 10}". This equals `reads.md:67–84`.
- R1, `network-bulk` gone: no occurrence in `dataset/archetypes.yaml` or `dataset/timelines/`, at `27a80abb` and at `928aa8fd` (the latter in `dataset/generated/` too).
- R3 is a reading of code and pooled records, with its locators given; R6 is a test-suite reading. Neither has a scan script.

On the current content, the TIMER-first invariant is the canonical lint (`dataset/tools/wlc/linter.py:363–365`, `_timer_first_violation` at `:464`), which the gate's `lint` step runs.

**`declared_class` against the class census** (`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`). The library's 29 entries:

- 27 entries carry the class the census observed. Two entries carry `idle`, as observed: `file-indexer` (`audit.md:12`, "IDLE, nice 19: all 68 Tracker threads") and `incremental-backup` (`audit.md:13`, "IDLE: `duplicity` ×23, `gpg` ×15 and Déjà Dup's own threads"). The other 25 carry `normal`, which is the census's NORMAL; the census's nice values are not carried, under 9.11 decision 6. The part-one rows are `audit.md:9–19`, the part-two rows `:31–47`, and the class summary is `:58–64`.
- `game-download-idle` is `idle` by design. It is the bounding variant (9.13 changelog D4), and its modelling note says so (`dataset/archetypes.yaml:1457–1463`). PASS.
- `game-task-chain` is `normal`, but the census records "`game-task-chain` (9.4) is no measurement" (`audit.md:23`). The entry's notes (`dataset/archetypes.yaml:1719–1828`) state nothing about its class. FAIL, minor (finding F3).

**The bless.** The 9.13 changelog's bless entry (D7, `changelog.md:41–56`) records 51 files. The final bless is 9.15's second data rebuild (`_dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/logs/B4-data-rebuild.md:25–35`, the "after" column). `shasum -a 256` of the seven committed manifests today:

| manifest | sha256 today | B4's "after" |
|---|---|---|
| `build.manifest.json` | `0f0af422…3417f` | equal |
| `build.variants.manifest.json` | `cdc14319…b579f6` | equal |
| `build.transition-grid.manifest.json` | `d84fb68a…53083d` | equal |
| `build.return-grid.manifest.json` | `a6980482…312512` | equal |
| `build.flap-stress.manifest.json` | `92676677…bbdf` | equal |
| `build.distractor-grid.manifest.json` | `1d129a51…84fe5` | equal |
| `build.familiarity-ladder.manifest.json` | `8c38e7a8…d6ca` | equal |

The manifests' entries: the core set has 51 artifacts and 51 reports, and 33 inputs. The variants manifest has 78 artifacts. The generated sets have 480, 720, 24, 272 and 66 artifacts, each with as many reports. Together that is 3,304, the figure in B4's "build verified (3304 files, 7 manifests)" (`B4-data-rebuild.md:3`). The RQ0 gate spec pins `dataset` at `0f0af422…` and `variants.all` at `cdc14319…` (`harness/experiments/rq0-gate.yaml:509–511`). PASS.

## 9.14 decision 1 — the mock-media derivation as the check of the TIMER skip rule

The skip rule (`docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md` §1): a task that reaches its TIMER after one or more ticks have passed consumes the latest passed tick at once, and each earlier unconsumed tick is a missed job with no work.

- `scripts/skip_replay.py` is an independent replay of the fixture's `run.json`: one lane, FIFO, run to block, TIMER under the skip rule, t₀ at arrival. Every `deadline` line and every `timer_tick` time it writes equals the fixture's `trace.jsonl`. The key moment is t = 76667, when `video` finishes job 2 with ticks 3 (50001) and 4 (66668) passed. The replay writes job 2 (due 50001, slack −26666, missed), then the skipped tick 3 (due 66668, `met: false`, slack −9999), then `ready(timer_tick)` at 76667 for tick 4. Job 4 then meets its deadline at 83334 (due 83335, slack 1).
- The derivation in `harness/tools/tests/fixtures/mock-media/worked.md` agrees with the rule line by line, and its row tables agree with `expected.csv`: six `job` rows for `video` with `skipped` 1 on tick 50001, five `timer_tick` `ready_wait` rows, and `busy` 85001.
- `pytest tests/test_records.py tests/test_reader.py -k "media or expected"` (from `harness/tools`): "8 passed".

PASS.

## 9.14 decisions 2 and 6 — the input-wake counts per scored task

`scripts/input_wakes.py`. Each scored `ready_wait` term's compiled file is first checked against the core manifest's sha256; all 39 matched. For each term the script counts the file's wake events on the term's entity and channel kind inside the term's window. These are offered wakes, read on `dataset/build/coreset-single`. The evaluator's `input_wake_count` line reads the same quantity off the fixed run's `ready_wait` count (`harness/tools/harness/evaluator.py:585–608`).

| file | set | entity | channel | window (µs) | wakes |
|---|---|---|---|---|---|
| `c1-compile` | judging | `editor` | input | whole | 2,544 |
| `c1-ml-train` | judging | `editor` | input | whole | 1,984 |
| `c1-render` | judging | `editor` | timer | whole | 16,296 |
| `c1-transcode` | judging | `video-editor` | timer | whole | 1,015,553 |
| `c2-p1a` | judging | `editor` | input | 60000000–99435000 | 188 |
| `c2-p3a` | judging | `editor` | timer | 60000000–326000000 | 56,496 |
| `c7-browsing` | judging | `browser` | input | whole | 84 |
| `c7-compile` | judging | `editor` | input | whole | 398 |
| `c7-dev` | judging | `editor` | input | whole | 49 |
| `c7-ml-train` | judging | `editor` | input | whole | 1,753 |
| `c7-office` | judging | `writer` | input | whole | 101 |
| `c7-photo` | judging | `photo-editor` | timer | whole | 214 |
| `c7-render` | judging | `editor` | timer | whole | 6,619 |
| `c7-transcode` | judging | `video-editor` | timer | whole | 632,587 |
| `c7-video-edit` | judging | `editor` | timer | whole | 9,836 |
| `c1-backup` | reporting | `editor` | timer | whole | 62,851 |
| `c1-browsing` | reporting | `browser` | input | whole | 123 |
| `c1-dev` | reporting | `editor` | input | whole | 186 |
| `c1-indexing` | reporting | `editor` | input | whole | 47 |
| `c1-mail` | reporting | `mailer` | input | whole | 35 |
| `c1-office` | reporting | `writer` | input | whole | 270 |
| `c1-photo` | reporting | `photo-editor` | timer | whole | 511 |
| `c1-video-edit` | reporting | `editor` | timer | whole | 17,232 |
| `c2-p1b` | reporting | `editor` | input | 60000000–99435000 | 188 |
| `c2-p3b` | reporting | `editor` | timer | 60000000–326000000 | 56,496 |
| `c3-creation` | reporting | `photo-editor` | timer | whole | 981 |
| `c3-creation` | reporting | `video-editor` | timer | whole | 34,672 |
| `c3-evening` | reporting | `browser` | input | whole | 77 |
| `c3-workday` | reporting | `browser` | input | whole | 7 |
| `c3-workday` | reporting | `writer` | input | whole | 139 |
| `c3-workday` | reporting | `mailer` | input | whole | 60 |
| `c4-compile` | reporting | `editor` | input | whole | 2,544 |
| `c4-office` | reporting | `writer` | input | whole | 270 |
| `c6-dual` | reporting | `editor` | input | whole | 13,751 |
| `c6-fold` | reporting | `browser` | input | whole | 123 |
| `c6-spoof` | reporting | `browser` | input | whole | 123 |
| `c7-backup` | reporting | `editor` | timer | whole | 39,672 |
| `c7-indexing` | reporting | `editor` | input | whole | 27 |
| `c7-mail` | reporting | `mailer` | timer | whole | 5,308 |

- There are 39 interaction-latency terms: 24 on the `input` channel and 15 on `timer`. The 15 are 9.14 decision 2's fourteen (the video editor's and the image editor's terms) plus `c7-mail`, which moved to `timer` under 9.14 decision 6. No term reads an empty filter.
- The thinnest judging term is `c7-dev`, with 49 keystrokes. The thinnest scored term is `c3-workday`'s browser, with 7 keystrokes (reporting).
- 9.14 decision 2 recorded `c7-browsing` 29 and `c7-indexing` 30 (`_dev/research/jioh/task-9.14-consumer-rework/changelog.md:19`). They now read 84 and 27, after the later rebuilds. That record is point-in-time. No current doc states the old figures (searched across `docs/`, `harness/`, `dataset/` and `_dev/docs/`).

PASS.

## 9.14 decision 7 — the boot-default sweep's step values

`chain_scan.py` (`_dev/research/jioh/task-9.14-consumer-rework/scans/`) was run on `c1-gaming`, `c2-p2a`, `c2-p2a-idle`, `c2-p2b`, `c4-gaming` and `c7-gaming`, which took 63 s.

- **The C2 gaming pair** (`c2-p2a`, `c2-p2b`): "chain members 17: per-frame RUN sum 15833 us; longest game.chain.14 2131 us; second 2099". The slack is 16,667 − 15,833 = 834 µs. The stages above 1,200 µs are 1,220, 1,733, 2,099 and 2,131: four stages, from 1,220 to 2,131. The Steam client runs 1,309,617 µs over 86,385,000 µs, which is 252.7 µs per 16,667 µs frame (`dataset/build/coreset-single/c2-p2a.report.json`, `per_task`), so "about 250 µs" holds.
- **The gaming base** (`c1-gaming`, `c4-gaming`, `c7-gaming`): "per-frame RUN sum 14999 us; longest game.chain.5 1436 us; second 1191". The slack is 1,668 µs. Nine stages lie from 992 to 1,436 µs (992, 1,052, 1,095, 1,113, 1,124, 1,159, 1,171, 1,191, 1,436); the cluster runs from 992 to 1,191, and the longest is 1,436.
- **The chain values** in `harness/experiments/rq0-gate.yaml:123–127` and `:413–415` reproduce.
- **The periodic tables do not read as stated.** The tables are the `cycle_run` params of `video-player` (`dataset/archetypes.yaml:623`) and `video-call` (`:673`). Each table's ten values are the percentiles p1, p5, p10, p25, p50, p75, p90, p95, p99 and p99.9 (`dataset/tools/wlc/sampling.py:75`, `QUANTILE_PROBS`; the library header, `archetypes.yaml:44–47`). The sweep's reasons read them as deciles. They were checked with the compiler's own sampler (`_quantile_sample`, 200,000 uniform draws) and against the compiled files: `c1-meeting` has 6,000 voice cycles, `c7-meeting` 2,639, and `c1-media` 1,800 video cycles.

| statement | where | stated | the table and the compiled files |
|---|---|---|---|
| the call's cycles that run past 10 ms | `rq0-gate.yaml:31`, `:121`, `:242`, `:416–417`; `harness/scoring/scoring-spec.yaml:67` | "about a fifth" | about one in twenty: the sampler gives 4.94 %, `c1-meeting` 5.50 %, `c7-meeting` 5.53 %. The table's p95 is 9,992 µs and its p99 12,221 µs |
| the call's 12.2 ms | `rq0-gate.yaml:129`, `:417` | "ninth decile" | the 99th percentile (12,221 µs). The ninth decile is 7.4 ms (sampler 7,388 µs; `c1-meeting` 7,484 µs) |
| the cycles above 14 ms | `rq0-gate.yaml:129` | "under a tenth of its cycles" | 0.04 % (sampler); `c1-meeting` 0.03 %. True, but a thousandth, not a tenth |
| the video player's cycle range | `rq0-gate.yaml:127`, `:415` | "decile cuts 2.3 to 7.5 ms" | 2.3 ms is the 1st percentile and 7.5 ms the 99.9th. The deciles are 2.8 ms (p10) to 5.4 ms (p90) |
| the cycles a 3 ms slice demotes | `rq0-gate.yaml:127` | "about seven in ten" | about eight in ten: sampler 81.6 %, `c1-media` 82.4 % |
| the video player's upper decile | `rq0-gate.yaml:128` | "7.5 ms" | 5.4 ms (5,376 µs). 5 ms still lies between the median (3,982 µs) and p90 |

Every point still sits on the side of the step its reason names. The fractions and the quantile labels are misread, though, and the first row is also the premise of `c7-meeting`'s place in the judging set (9.14 spec decision 2, `_dev/docs/spec/jioh/task-9.14-consumer-rework.md:28`). FAIL (finding F1).

## 9.18 decision 6 — the timelines' `source` maps against `bound-values.md`

`scripts/bound_values.py` transcribes the table of `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md:7–30` as (file, archetype, key) → (value, tags). It compares that, in both directions, with every core-set timeline's per-task `source` map and bound value. Under the table's rule that derived files carry the value their variant op binds (`bound-values.md:3`), `c2-p2a-idle` inherits `c2-p2a`'s bindings (`dataset/timelines/coreset/c2-pairs.variant.yaml`).

The result: 77 entries in the timelines and 77 expected (76 transcribed, plus `c2-p2a-idle`'s `member_names`, which the first transcription missed and the derived-file rule covers). Every tag and value agrees. No bound value lacks a `source` entry. PASS.

## 9.19 decision 5 — the flap-stress intervals' three sources at their release tags

The intervals are in `dataset/grids.yaml:66–70`: 2 s `design`, 5 s `feral-gamemode`, 10 s `tuned` and 30 s `systemd-oomd`. The standard is phase spec decision 1: the verbatim passage, its locator, and the copy read.

- `feral-gamemode` (`docs/references.md:580–583`). Read at tag `1.8.2`, verbatim with the copy named. Re-read today: `example/gamemode.ini` at tag 1.8.2 (commit `c54d6d42`, release published 2024-08-19, sha256 `678cd894…`), lines 2–3: "; The reaper thread will check every 5 seconds for exited clients, for config file changes, and for the CPU/iGPU power balance" / "reaper_freq=5". PASS.
- `tuned` (`docs/references.md:585–588`). Read at tag `v2.28.0`. Re-read today: `tuned-main.conf` at v2.28.0 (commit `a4907c9a`, sha256 `6a41544b…`), lines 9–18: "if disabled only static tuning will be used." / "dynamic_tuning = 0"; "How long to sleep before checking for events (in seconds)" / "higher number means lower overhead but longer response time." / "sleep_interval = 1"; "Update interval for dynamic tunings (in seconds)." / "It must be multiply of the sleep_interval." / "update_interval = 10". PASS.
- `systemd-oomd` (`docs/references.md:590–593`). The record reads `man/oomd.conf.xml` "at `main` (version 263~devel)". That is a branch, with no commit and no release tag, so the record does not meet the item. FAIL, minor (finding F2). Read today at two release tags:
  - **v262.1**, systemd's latest release, published 2026-10-16 (commit `73612ea5`, sha256 `36ae3e47…`). Lines 198–202: "Sets the amount of time a unit's control group needs to have exceeded memory pressure limits before <command>systemd-oomd</command> will take action. … Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0." Lines 183 and 190: "the fraction of time in a 10 second window in which all tasks in the control group were delayed" … "Defaults to 60%."
  - **v255**, the major version Ubuntu 24.04 ships, 255.4 (`docs/references.md:516`) (commit `db11bab3`, sha256 `9cbf877f…`). The same sentences are at lines 85–88, 70 and 77.

  The value and wording the repository uses hold at both tags.

## 9.20 decision 10 — the tier-3 names and `linux-sched-h`

- The tags come from `dataset/grids.yaml:111–112`: `render: {kdenlive_render: {name: melt-7, source: "meas-ci:background:2026-10-03c"}}` and `backup: {deja-dup: {name: duplicity, source: "meas-ci:background:2026-10-04"}}`. The generated cells `fl-render-t3` and `fl-backup-t3` carry the names at line 42. Both tags are in `dataset/meas-releases.yaml` (`:221`, `:259`).
- `melt-7`. The Kdenlive campaign's results list `` `melt-7` [32582] /usr/bin/melt-7 threads 9 `` in each repeat (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/kdenlive/results/results.md:81` onward). The 9.10 changelog says "`melt-7` holds 0.9960–0.9963 of the CPU" (`changelog.md:1997`), and the library entry says the same (`dataset/archetypes.yaml:917`).
- `duplicity`. The Déjà Dup campaign's results list `` `duplicity` [33213] /usr/bin/duplicity `` and further processes (`campaign/dejadup/results/results.md:90`, `:94`). The 9.10 changelog says "`duplicity` holds 0.569–0.576 of the CPU over its eight runs" (`changelog.md:2269`), and so does the library (`archetypes.yaml:1674`).
- The 9.20 census table points into `archetypes.yaml` at `:914` and `:1668` (`_dev/research/jioh/task-9.20-c4-and-c5-grids/changelog.md:25–27`). The passages now sit at `:917` and `:1674`, after later library edits. That is line drift in a dated record, and the passages are unchanged. PASS.
- `linux-sched-h` (`docs/references.md:384–387`). It was read at tag v6.17. Re-read today (`include/linux/sched.h` at v6.17, sha256 `d7a2b1e7…`): lines 315–316, "Define the task command name length as enum, then it can be visible to BPF programs."; line 320, `TASK_COMM_LEN = 16,`; lines 1156–1161, "executable name, excluding path." … "set it with set_task_comm()" … "strscpy_pad() to ensure it is always NUL-terminated and zero-padded"; line 1165, `char comm[TASK_COMM_LEN];`. Every quoted passage is present. PASS.

## 9.21 — `scoring_lint.py` and `gh-hosted-runners`

- `harness/tools/scoring_lint.py` (2 min 53 s, exit 0) reported: "scoring spec: 49 files, 75 terms"; "generated transition-grid: 480 files with terms, 1320 terms by the rule"; "return-grid: 716 …, 2865"; "flap-stress: 24 …, 248"; "distractor-grid: 255 …, 374"; "familiarity-ladder: 64 …, 104"; "lint clean". The file counts equal the TODO line's 480/716/24/255/64, and the term counts equal those in `B4-data-rebuild.md:57`.
- `gh-hosted-runners` (`docs/references.md:369–372`) has the cite (GitHub Docs, "GitHub-hosted runners reference", section "Standard GitHub-hosted runners for public repositories", Linux x64 row: 4 processors, 16 GB, 14 GB), the URL, "accessed 2026-10-13" and status "verified (2026-10-13; the page read on that date)". It is not in `dataset/sources.yaml`, which is right: the dataset derives no value from it (`CLAUDE.md`, the citations rule). PASS.

## 9.23 decision 15 — the full smoke

`make -C harness smoke` on the final build, with its time recorded, is run by the lead. Listed only.

## Items closed by the gate and the CI run (9.16 spec decision 3)

| TODO-line item | the pin it names | closed by |
|---|---|---|
| the 2026-10-11 review: the generated layer reproduces from its generator; 9.18's counterpart test and source-field lint; the five gate pins and the generated layer's pins equal the committed bytes | — | gate `generated` + `check` (the generator's `--check` and `check_build.py`), `test` (`test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds`), `lint` (the source-field lint); the RQ0 gate spec's pins checked here too (below) |
| 9.17 decision 6: the 51 artifacts and 78 variants reproduce (`compile.py --check`, `variants.py --check`) | dataset `625e431f…`, variants `328560cf…` | gate `dataset`, `variants`, `check`; CI run |
| 9.18 decision 6: artifacts, reports and variants reproduce, `build/` equals the manifests | dataset `976a943c…`, variants `6c244f17…`, scoring spec `1f7e9e30…` | gate `dataset`, `variants`, `check`; the scoring-spec pin by `experiment_lint.py` (below); CI run |
| 9.22 decisions 5 and 6: the manifests' `inputs` on the 9.22 tooling; CI run 38131040159 | dataset `d10bcd42…`, variants `831a854e…` | gate `dataset`, `variants`, `check`; CI run |
| 9.19 decision 5: the three generated manifests reproduce (`generate.py --check`) | `899efa53…`, `7a758f6e…`, `8c4c6fce…` | gate `generated`, `check`; CI run |
| 9.20 decision 10: the five generated manifests reproduce, 3,304 files, 7 manifests; CI run 38243554308 | `593dc23a…`, `183deedb…`, `d2686e73…`, `7236f4b2…`, `0b8b76ce…`; core `fad7192d…`, variants `03f14b2c…` | gate `generated`, `dataset`, `variants`, `check`; CI run |
| 9.21: the five manifests with `grid` placements; the scoring spec re-frozen; `coverage-grid.json` reproduces (`derive.py --check`) | `e26aa8e6…`, `21826be3…`, `a8c271dd…`, `6d9192db…`, `2cb56e69…`; scoring spec `0ff71b1f…` | gate `generated`, `check` (`derive.py --check --require-coverage` is in `check`, `B4-data-rebuild.md:56`); the scoring-spec pin by `experiment_lint.py`; CI run |

Each named pin is superseded by the final state's. The final pins were checked here: the seven manifests' sha256 match the table above. `shasum -a 256` gives `harness/scoring/scoring-spec.yaml` `2ad757b6…`, `harness/guards/guard-spec.yaml` `24ccb875…` and `daemon/driver-table/prior.yaml` `0fba4b3c…`, equal to `harness/experiments/rq0-gate.yaml:506–511`. `harness/tools/experiment_lint.py` reported "rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap" and "lint clean", exit 0.
