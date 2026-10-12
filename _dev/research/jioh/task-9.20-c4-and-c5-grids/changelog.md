# 9.20 — C4 and C5 grids, C5 → C6: changelog

> Status: record · Created 2026-10-12 · Updated 2026-10-12

Spec: `_dev/docs/spec/jioh/task-9.20-c4-and-c5-grids.md`. The grill of 2026-10-12 settled the ten decisions below from the audit record's C4 and C5 directions (`_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`); the implementation followed on `jioh/dataset-rebuild`.

## P — the process-name census behind tier 3

Tier 3 of the familiarity ladder is a program's own real name that carries no meaning (`workload/building-plan.md` C5: `tracker-miner-fs-3`, `cc1`, `baloo_file`). To find which modes can have one, every measurement campaign's record was searched for the real `comm` strings each measured program's tree showed beyond the name the timelines use (search by a sub-agent over `_dev/research/jioh/task-9.4` … `task-9.10`, `dataset/archetypes.yaml`'s `validation_stats`, `dataset/meas/names/`, `_dev/research/jioh/task-9.11-scheduler-constants/sources/census/session/census.edge.json`; 2026-10-12). Threads' comms are not process names and were set aside.

| program (timeline name) | other process names in the tree | recorded at | tier-3 cell? |
|---|---|---|---|
| `code` | none — main, renderer, GPU and utility processes all `code` | 9.5 changelog :75; `archetypes.yaml` :141–167 | no |
| `soffice.bin` | `oosplash` (the launcher), `soffice` (the shell wrapper) | 9.5 `campaign/results-same-machine.md` :37, :42; `dataset/meas/names/names-ubuntu.json` :199 | no — helpers, not the writer |
| `thunderbird-bin` | `WebExtensions`, `RDD Process` (Gecko child processes) | 9.5 changelog :793; `archetypes.yaml` :221, :272 | no — helpers |
| `chrome` | `chrome_crashpad` (the crash handler) | `archetypes.yaml` :477 | no — carries `chrome` |
| `gimp` | `script-fu` (the plug-in process) | 9.5 `results-same-machine.md` :158, :163; `archetypes.yaml` :516 | no — a helper |
| `kdenlive` | `kdenlive_render` (already the export task's name), `melt-7` under it | 9.5 `campaign/method.md` :45; 9.10 `campaign/kdenlive/results/results.md` :81 | the export's cell, below |
| `mpv` | none | 9.5 `results-same-machine.md` :210–229 | no |
| `Troy.exe` (chain) | the member names of the LAVD slides, already tier 3 (`dxvk-cs`, `winepulse_mainl`, `FAudio_AudioCli`, `Task worker thr`) | `archetypes.yaml` :1741–1747 | the C1 file already carries them |
| `steam` | `steamwebhelper` (9 processes); `steamcmd` for the download, a different program | 9.8 changelog :95, :483–485; 9.7 `results-steamcmd.md` :105 | no — carries `steam` |
| `make` + `cc1` | kbuild's `sh`, `gcc`, `as`, `fixdep`, `ld`, `ar`, `objtool`, `modpost` | 9.6 `campaign/results.md` :55–68 | the C1 file already carries `cc1` |
| `dkms` | `dkms_autoinstal`, `x86_64-linux-gn`, kbuild's members, `zstd`, `depmod` | 9.10 changelog :1037, :1041 | C7's job, no ladder cell |
| `python` (MNIST) | none — one process, one thread | 9.10 `campaign/mnist/results/results.md` :31 | no |
| `kdenlive_render` | **`melt-7`** — the child holding 0.9960–0.9963 of the CPU | 9.10 `campaign/kdenlive/results/results.md` :81; `archetypes.yaml` :914 | **yes: render** |
| `HandBrakeCLI` | none — one process, 23 threads | 9.10 changelog :1741 | no |
| `deja-dup` | **`duplicity`** 0.569–0.576 of the CPU, `gpg` 0.134–0.140, `deja-dup-monito` | 9.10 `campaign/dejadup/results/results.md` :87–96; `archetypes.yaml` :1668 | **yes: backup** |
| `tracker-miner-f` | `tracker-extract` (96 % of the CPU), `gst-plugin-scan` | 9.10 changelog :1312; 9.10 `campaign/tracker/results/results.md` :78–81 | the C1 file already carries `tracker-miner-f` |
| `unattended-upgr` | `apt.systemd.dai`, `localedef` (76 %), `dpkg`, `mandb`, … | 9.10 changelog :824; 9.10 `campaign/upgrade/results/results.md` :58, :861 | C7's job, no ladder cell |
| `7z` | none — one process, 34 threads | 9.7 `results-7z.md` :59 | no |
| `element-desktop` | none | 9.10 changelog :514 | no |
| `gnome-shell`, `pipewire`, `systemd`, `dbus-daemon` | `gjs`, `gnome-shell-cal`; `wireplumber`, `pipewire-pulse`; `(sd-pam)`; none | 9.9 changelog :19–21, :77; the 9.11 census | no — other executables of the session, not these programs' own names |

Result: two modes' jobs ran under an opaque name of their own tree — render (`melt-7`) and backup (`duplicity`); three C1 files already carry tier-3 names (compile, indexing, gaming). The rest have no real opaque name to give.

## Decisions

### D1 — the C4 cell is the transition grid's `focus` form with the focus kept on A (spec decision 1)

Grill Q1, option (A) over the TODO line's "B's foreground program arriving at 30 s": two 60 s segments, B's whole set at 60 s by the composition rules, A's focus and input to the file's end, both segments labelled A. The reason recorded in the grill: the transition grid's `focus` form and this cell then have the same open programs and differ in the focus track alone, so every condition run on the pair under the `focus` and `names` telemetry shapes isolates the field's worth. Consequence: the authored C4 files, 30 s injections within one segment, are existence cases, not cells (spec decision 4).

### D2 — the 26 cells whose focus holders share a name are pre-committed misses (spec decision 3)

Found in the grill from telemetry rule 6 (`docs/data-contracts.md` §5: the focus holder is carried by name; a move between two instances of one name changes nothing): where A's and B's focus holders share a name the C4 cell and its `focus`-form twin produce identical telemetry with different labels. `code` over dev, compile, ml-train, indexing (12 ordered pairs); `kdenlive` over video-edit, render, transcode, backup (12); `chrome` over browsing, meeting (2). Q1b, option (i): built and annotated `pre_committed_miss: true` on the second segment, `focus_name_shared: true` in the manifest record; the vocabulary's annotation definition ("a segment whose label no recognizer can reach from names and behaviour") fits.

### D3 — the out-of-vocabulary relation holds the library's two label-invariant programs (spec decision 2)

Q2. The library's 28 measured programs were sorted: the ones in no C1 task set that leave the label unchanged are `element-desktop` (chat client) and `7z` (file archiver); every other non-mode program is a C7 unwanted job that flips `background_wanted` (`unattended-upgr`, `dkms`, the scheduled indexer and backup), and `steam`'s download carries gaming's name. `7z`'s `total_work` is bound to the 60 s span, design, as every generated batch job fills its span; `element-desktop` is segment-bound to the file's end; the scenario tags are the authored C4 files' (S16, S5). The grill considered and set aside bringing the unwanted jobs in as a third program (same shape, the attribute flipped): that is C7's axis and the measurement backlog's.

### D4 — tier 3: two generated cells beside the three C1 files (spec decision 6)

Q3, option (b): render's export renamed `melt-7` and backup's job renamed `duplicity`, the names of the processes that did the work in the campaigns (P above), each tagged `meas-ci:background:2026-10-03c` and `meas-ci:background:2026-10-04`. Helper processes (`oosplash`, `script-fu`, `RDD Process`, the session's `gjs`, `wireplumber`, `(sd-pam)`) do not qualify: they are not the program's own name on the work.

### D5 — the unwanted-jobs measurement stays in the backlog with its timing (spec decision 9)

Q4, option (a). The attribute's `false` side runs on the sixteen C1–C7 pairs (the audit's C2 direction), today one unwanted name on the ten interactive counterparts — a validity limit for RQ1's attribute accuracy, not for RQ0. How many unwanted jobs are needed is the RQ1 experiment spec's decision; the campaigns run after Phase 10's RQ0 run and before the RQ1 run. The backlog line in `_dev/TODO.md` now says so.

### D6 — the ladder's carrier axis in full, coinciding cells collapsed (spec decision 5)

Q5, option (a): the focus holder's name alone, the other names alone, every name; a form renaming nothing has no cell, forms renaming the same set collapse into the `all` cell, whose record lists the carriers it stands for. Count: eight modes with one program (or every name the same, browsing, meeting; or no focus holder, idle) give one cell per tier, eight give three — 32 per tier, 64 over tiers 4 and 5, plus the two tier-3 cells: 66.

### D7 — the names (spec decision 7)

Q6. Tier 4: the hand-written table in `dataset/grids.yaml`, 26 entries (the 20 task names and the chain's six member names of the C1 files), each at most 14 characters, design. Tier 5: four lowercase letters from SHA-256 over `name|familiarity-ladder|<cell id>|<real name>|<attempt>`, redrawn when the draw is a known name — the C1 files' names, the compiler's `wineserver`, the coverage tool's name table (`wlc/grid.py` `NAME_TIERS`), the tier-4 table's names — or a substitute already drawn in the file. One real name maps to one substitute within a file (`chrome × 5` stays × 5; the two `mpv` share one name, unlike the authored `c5-t4`). The orchestrator's `child_name` and the chain's `member_names` are renamed through the same map, their `source` entries `design`. The chain's `wineserver` is the compiler's constant (`wlc/compiler.py:846`) and keeps its name — renaming it would change the compiler, a pinned input of the core set's manifest. The 15-character limit: `docs/references.md` `linux-sched-h` (`TASK_COMM_LEN = 16` with the NUL, `include/linux/sched.h` at v6.17, read 2026-10-12), registered in `dataset/sources.yaml` and the ground of `comm_limit` in `grids.yaml`; the lint checks every name the definition sets against it.

### D8 — `c5-t3` to `c6-alias` (spec decision 8)

Q7. The recipe moved from `c5.variant.yaml` to `c6.variant.yaml`: same tasks, archetypes and seed (104), the segment's `familiarity: 3` dropped, `spoof: true` and `pre_committed_miss: true` added. The core set rebuilt: 51 artifacts, 50 byte-identical, `c5-t3`'s entries replaced by `c6-alias`'s. The scoring spec's entry moved to its C6 section under the new id (terms verbatim), re-frozen; the RQ0 gate spec's reporting list and its pins follow (the hashes in `harness/CHANGELOG.md`). `c5-t4` and `c5-t5` unchanged.

### D9 — implementation notes

- The ladder cell is the mode's C1 task set in one 60 s segment by the composition rules (a batch job scaled to the span, design), then renamed — not the C1 file at its authored length. The spec's "each C1 file with its names substituted" is realised this way because the batch modes' C1 files run to the job's CPU total (compile 1,594 s, transcode 2,971 s) and the grill priced the ladder as 60 s files; it keeps 9.19 decision 1 (every grid segment 60 s) and the layer's one re-timing rule.
- `gen/compose.py`: `_place` takes `track_end` (the input, focus and operations run to it; the distractor grid's A) and `tracks=False` (an arrival the user never turns to); `_compose_distractor`, `_compose_ladder`. `gen/cells.py`: `distractor_cells`, `ladder_cells`, `names_of`, `focus_name`, `known_names`, `tier5_name`; `cells()` takes the C1 timelines. The lint checks the new sets' form, every name against `comm_limit`, every source tag.
- The three 9.19 manifests re-bless: their `inputs` pin `grids.yaml` and the generator's sources by content, all changed here; their artifacts are byte-identical (checked below).
- The core compile leaves stale artifacts in `build/`; `c5-t3`'s two files were removed by hand before `make check` (the gate reports a file pinned by no manifest).

### D10 — the build (2026-10-12, the home machine, M1 Pro, 10 cores)

- The core set: `make dataset` 52 s; 51 artifacts, 50 byte-identical to the 9.22 bless, `c5-t3`'s artifact and report replaced by `c6-alias`'s (the report's hash equal: the report carries no id). Manifest `fad7192d…`. The stale `c5-t3` artifacts removed from `build/` by hand.
- The variants: `make variants` 1 min 53 s; 78 artifacts byte-identical; the manifest's `inputs` entry for the dataset manifest moved. Manifest `03f14b2c…`.
- The generated layer: `make generated` 2 min 17 s for the five sets (2 min 09 s for three in 9.19) — transition grid 480, return grid 720, flap-stress 24, distractor grid 272, familiarity ladder 66; 1,562 artifacts. The 9.19 sets' artifacts, reports, demand and grid records byte-identical to the committed manifests; their `inputs` moved (`grids.yaml`, `gen/cells.py`, `gen/compose.py`, `generate.py`). A first run had changed every generated artifact through `meta.derived_from` because the generated files' header comment had been reworded ("composed or renamed"); the wording was restored and the sets regenerated — the header is part of the timeline bytes the artifact pins.
- Sizes: `build/distractor-grid-single/` 844 MB (the largest artifact 9.5 MB, `dx-transcode-with-gaming`), `build/familiarity-ladder-single/` 96 MB (the largest 2.7 MB, `fl-transcode-t5-all`); `build/` 6.8 GB in all (5.9 GB after 9.19). Manifests 249 KB and 61 KB.
- Pins: dataset `fad7192d2a290c9d0b9f9563a45a0f9834b8c48403c4c88d84ae1869107accd3`, variants `03f14b2c5520edaf304915a2c773f8ac30436a9f88ea9cd2d8b319949c3605d5`, transition-grid `593dc23af28aa6bcb66ca81ff3bdaa29fb44be0338e714728a2e867f7f46e655`, return-grid `183deedb53f83449e392617641d80a01aa493e0cd5f2fb345bf3cfeaf020514d`, flap-stress `d2686e73f704410d352f70167b12cc77b1f5e8bfdd1e9a3080e2b1a3e2f5bf63`, distractor-grid `7236f4b2090d8dbc33e1ce7522626b0bb4cb2e73d8884ca1139432a51f9700dd`, familiarity-ladder `0b8b76ce561ce0b61696d2a0ed34b4561dd09ecd6592c453fe6b30a36fc8a290`; the scoring spec re-frozen at `9cd9a155db7a6f9521a73c89a5159736e7b9ff185a63fbf61b2cc453bc38e360`.
- `make check`: build verified, 3,304 files, 7 manifests, 6 s. Dataset lint clean; the generated-layer tests 17 passed before the build (the manifest test after it, with the suite). Harness lint clean after `c6-alias` joined the RQ0 gate spec's `layer1_exclusions` (the experiment lint derives the list from the `pre_committed_miss` annotations).
