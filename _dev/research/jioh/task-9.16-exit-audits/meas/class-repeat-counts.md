# How each campaign's repeat count was chosen, and where the stopping rule makes the binding value's half-width optimistic

Task 9.16 (the Phase 9 exit audits), the item 9.5's self-review handed to it on its `_dev/TODO.md` line: "the measurement audit reads how each campaign's repeat count was chosen, the stopping rule being what makes the binding value's half-width optimistic". Read 2026-10-17 at `928aa8fd`.

## The rule and why stopping makes an interval optimistic

- **The rule.** `stability.py` (header and lines 1-60) states it: at least five repeats; each carried value's 95 % t half-width is at most 5 % of the mean, or 1 µs where larger. `measurement-overview.md` §6 adds that repeats are added one at a time, or as one batch sized by the pool's projection and then one at a time.
- **Why the stop matters.** A campaign that stops at the first count where the rule holds picks its count from the very estimate it then reports. The value that stopped it — the *binding value* — therefore sits at the boundary, and its stated 95 % interval covers the true mean less often than 95 %. `stopping.py` (lines 2-8 and 38-61) simulates this: one repeat at a time at the value's observed spread.
- **What is stated today.** `measurement-overview.md` §6, row "What the stop guarantees": entries whose widest value sits within half a point of the tolerance (half-width ≥ 4.5 %, `stopping.NEAR`) say so in their scopes. Only the 9.5 entries were simulated (`stopping.entries`, which reads `control_report.ARCH_95`).

**Kinds of stop used below:**

- **first pass** — one repeat at a time, stopped at the first count where the rule holds;
- **projection batch** — one batch up to the pool's own projection (9.7 D26), then the rule read;
- **minimum** — the rule held at five;
- **fixed** — a count set in advance;
- **recording** — the recorded input ran out.

## Per campaign record

Half-widths come from the pooled records (`results/pooled.json` per slice) and from `_dev/research/jioh/measurement-campaign-record.md`.

| campaign record | entries | count | how chosen | binding value at the stop | widest value carried on the rule now | optimistic? stated? |
|---|---|---|---|---|---|---|
| `interactive:2026-09-18` | `office-writer` | 14 | first pass | `input_run` mean under the 136M Keystrokes stream ±4.96 % | the same | **Yes.** Simulated coverage 91–93 %; stated in scope `archetypes.yaml:111`. |
| `interactive:2026-09-18` | `image-editor` | 5 | minimum (held at five) | op `script-fu` run mean ±4.40 % | the same | Barely: count at stop 5.4, coverage 94.8 %, below the 4.5 % line; not stated, and not required. |
| `interactive:2026-09-18` | `video-editor` (driven and operation phases) | 20 | first pass | driven `kdenlive` run mean ±4.997 % | the same | **Yes.** Coverage about 91 %; stated in scope `archetypes.yaml:607`. |
| `playback:2026-09-18` | `video-player` | 24 | first pass on `vo` wakes/s ±4.98 %, a value no longer carried since 9.5 D75 | `vo` wakes/s | play CPU share ±2.86 % | No for the carried values: the stop was not conditioned on them. The simulated row (93 %) is conservative. |
| `playback:2026-09-18` | `audio-player` | 31 | first pass on `ao` run mean ±4.93 %, no longer carried since D75 | `ao` run mean | play CPU share ±4.68 % | Stated (scope `archetypes.yaml:657`, coverage about 92 %). This is conservative: the carried value was not the one that stopped the campaign. |
| `interactive:2026-09-19` | `mail-client` idle phase | 77 | 43 by first pass, then after 9.5 D94 one projection batch of 34, the rule read once at 77 | `WebExtensions/StreamTrans` run mean ±4.75 % | the same | **Yes.** Coverage 93–94 %; stated in scope `archetypes.yaml:355`. |
| `interactive:2026-09-20` | `web-browser` | 38 | recording (the Internet Explorer stream's last window) | none: not stopped by the rule | idle `renderer/chrome` run mean ±4.37 % | No stopping optimism. `input_run` ±5.90 % is carried under the recording-runs-out exception. |
| `playback:2026-09-20` | `video-call` | 45 | first pass on `gpu/Chrome_ChildIOT` gap mean ±4.95 %, no longer carried since D75 | that gap mean | play CPU share ±1.52 % | No for the carried values. |
| `interactive:2026-09-25` | `code-editor` | 44 | stopped at window 44, short of the Word recording's 57 (9.5 D99) | none: neither the rule nor the recording's end chose it | `input_run` mean ±4.84 % | No first-crossing optimism: the rule did not choose the count. The scope states the stop. |
| `interactive:2026-09-27` | `mail-client` input and send | 8 | recording (the Outlook stream's last window) | none | none on the rule: the 39 values are reported with their half-widths (`input_run` ±10.41 %) | Not applicable. |
| `interactive:2026-10-05` | `video-editor` idle phase | 16 | first batch of 5, then projection batches to 6, 8 and 16; the rule held at 16 | `kdenlive` run mean ±4.45 % | the same | **Yes, mildly.** Coverage 91.3–92.3 % (`stopping.py` re-run 2026-10-17). It sits just under the 4.5 % line, so no caveat is required, but the committed stopping record still shows the driven phase's row (finding F2). |
| `build:2026-09-18` | `compiler-child`, `build-orchestrator` | 14 | the rule, the count set by `cpu-batch` programs since retired (`clamscan`, `python3`) | a retired program's value | step tables ±0.6–2.0 %; dispatch ±0.94 % | No for the carried values. |
| `background:2026-09-19` | `file-archiver` | 6 | the first batch of six held | run ±2.18 % | the same; block per run within the 1 µs floor | Negligible. |
| `background:2026-09-19` | `game-download` | 30 | batches (repeats 6–12, 14–22), then one at a time | not named in the record. The likeliest is the reported, uncarried network wait ±4.18 %. | run ±2.21 %; block ±0.90 µs (passes on the floor) | No for the carried values. |
| `desktop:2026-09-20` | `chat-client` | 18 | the rule (the record names no batch, so presumably first pass) | not named in the record | residual run mean ±4.35 % | Mild, under the line; not stated, not required. |
| `desktop:2026-09-20` | `game-client` | 12 | first pass on the values left on the rule after 9.8 D18 removed four run means (committed before windows 6–12 were launched) | not named in the record | `CJobMgr::m_Work` run mean ±5.69 %, which passes only on the 1 µs floor | Mild. The four excepted run means are carried with their own half-widths (±5.3–10.1 %); none is conditioned on the stop. |
| `session:2026-09-24` | the four session entries | 24 | a projection batch (24 jobs, 15 landed), then closed at 24 on the values as analysed that day ("widest 3.7 %"). Re-analyses by cause (9.9 D27, D47) moved values afterwards, with no repeat added. | a pre-D27 value | `wireplumber/gmain` wake rate ±4.48 % | No first-crossing optimism on the current values: the stop was taken on earlier ones. The record rounds 4.48 to "±4.5 %", which reads as at the line. `pid1/systemd` run mean and the system bus are carried between sessions (±7.8 %, ±10.7–11.1 %). |
| `background:2026-10-01` | `package-upgrade` | 9 | first batch of 5, then a projection batch to 9 | run ±6.31 % and CPU total ±7.72 % at five | CPU total ±3.78 %; run ±3.10 % | Mild, under the line. |
| `background:2026-10-02` | `module-build-orchestrator`, `module-compiler-child` | 26 landings of 23 repeats | first batch of 5, then a projection batch to 23 | 37 of 60 values failing at five | `kprobe gcc step 2/3` ±4.13 % | Mild, under the line. The tail's block per run is carried ±8.35 %. |
| `background:2026-10-02b` | `file-indexer` | 18 | first batch of 5, then a projection batch to 18 | block per run ±12.08 % at five | block per run ±3.58 % | Mild, under the line. |
| `background:2026-10-03` | `cpu-batch` (`python3`) | 6 | first batch of 5, then one repeat to the projection | CPU total ±5.32 % at five | CPU total ±4.04 % | Mild, under the line. The run and block tables are carried under the machine exception (±27.3 %, ±10.8 %). |
| `background:2026-10-03b` | `video-transcoder` | 5 | minimum | none | CPU total ±2.6 % | No. |
| `background:2026-10-03c` | `cpu-batch` (`kdenlive_render`) | 30 | first batch of 5, then a projection batch to 30 (9.10 D109) | block per run ±98 % at five | block per run ±13.1 %, passing on the 1 µs floor | Not material: the value passes on an absolute floor. |
| `background:2026-10-04` | `incremental-backup` | 28 of 30 | fixed: one batch to 30, decided in advance (9.10 D122), with the exception as fallback | none | run ±4.38 % | No first-crossing optimism. |
| `desktop:2026-10-04b` | launches of eight entries | 5 each | fixed (the workflow's five) | none: a launch is replayed per repeat, not on the rule | — | Not applicable. |
| `desktop:2026-10-05` | `video-editor` launch | 5 | fixed | none | — | Not applicable. |
| `desktop:2026-10-05b` | `renderer-hidden` steady phase and launch | 5 | minimum | none: 4 of 18 values pass at five; the other 14 are carried under 9.8's per-value treatments (9.10 D155) | `chrome` wake rate ±1.59 % | No stopping optimism. The 14 values are stated with their half-widths (±5.1–61.3 %). |

## Read

- **Where the stop makes a binding value optimistic.** This happens in five pools, the four 9.5 pools within half a point of the line — `office-writer` 14, `video-editor` driven 20, `mail-client` idle 77, and `audio-player` 31 (conservatively, its stop was on a value no longer carried) — plus, mildly and under the line, `video-editor`'s idle 16.
- **The four within half a point are stated.** All four state it in their scopes, as `measurement-overview.md` §6 says.
- **No other campaign's carried value reaches 4.5 %.** The non-9.5 campaigns' carried values on the rule are all below it (the highest is the session's ±4.48 %). Their first-pass and projection-batch stops make the stated interval mildly optimistic (coverage in the low 90s % at ±4–4.5 %, on the 9.5 simulations' evidence). This is consistent with §6's half-point line. `stopping.py` was never run on them; running it on the session, `chat-client`, `incremental-backup` and the DKMS pools would close that read.
- **Four counts were not chosen by first crossing.** `web-browser` and the keys-only `mail-client` stopped at the end of their recordings; `code-editor` stopped short of its recording (9.5 D99); `incremental-backup`'s count was fixed in advance. None of their half-widths is made optimistic by the stop.
- **One stopping record is stale.** The committed record (`task-9.5-interactive-typing/campaign/results-stopping.md`) no longer matches what `stopping.py` computes for `video-editor` — finding F2.
