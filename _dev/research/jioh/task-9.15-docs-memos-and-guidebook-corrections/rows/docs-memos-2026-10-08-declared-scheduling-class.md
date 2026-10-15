# Work-list rows — `docs/memos/2026-10-08-declared-scheduling-class.md`

Chunk K17, Memos (wave 4). 2 open rows. The file has 31 lines at `d5cc7711`.

### W-0707 · open
- At: `docs/memos/2026-10-08-declared-scheduling-class.md` the header block after the H1 (the `> Status:` line and the `> From …` line)
- Change: Add one header line after the Status line: either closed, naming where the memo's content now lives, or open, naming the ask still outstanding and its owner. Bump the header's `Updated`.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: The memo: to 인경민 and 박이안: the declared class; item (e) of the conformance statement — the strict idle class — is owed (`harness/experiments/rq0-gate.yaml:337–340`). Written in English; the header line in the memo's own language. Whether it is open or closed is decided against the code and the records, and logged.

### W-0708 · open
- At: `docs/memos/2026-10-08-declared-scheduling-class.md` new — an appended `## Correction (<date>)` section after §4; the corrected statement is in §1 'The field', the bullet 'The class is the entry's.', line 9 ('`c5-t3` shows two media players as `tracker-miner-f` and `baloo_file`, and they stay `normal`.')
- Change: Append a dated `## Correction (<date>)` section in English naming the statement and stating that the file is now `c6-alias` (9.20 D8, 2026-10-12): `c1-media`'s two players under the two indexers' real names, `spoof: true`, `pre_committed_miss: true`, no familiarity tier — the players still `normal`; bump the header's `Updated`; leave §1's text as written.
- Final word: 9.20 D1, D6, D8 (2026-10-12): `c5-t3` became `c6-alias` (C6, the resolution-limit group) — `c1-media`'s two players under two indexers' real names (`baloo_file`, `tracker-miner-f`), `spoof: true`, `pre_committed_miss: true`, no familiarity tier; the familiarity ladder (C5) is generated over the sixteen modes at tiers 3–5 with the carrier axis (focus holder's name / the others / all), 66 files; the authored C4 (distractor injection) and C5 files are existence cases, the rate claims on the generated distractor grid (272 files) and ladder. A dated memo gets a note, not a rewrite (TODO 9.15 line, from 9.20).
- Sources: SX-0337 (TODO 9.15 line (from 9.20), `_dev/TODO.md:179`); SX-0942 (guidebook dataset vol-03 ch.16 mismatch list (§16.1, declared-class memo), `dataset/03-timeline-to-canonical-workload.md:2239`)
- Notes: Checked: `dataset/timelines/coreset/c6-alias.timeline.yaml` — derived from `c1-media` (c6.variant.yaml), tasks `video` (archetype `video-player`, name `baloo_file`) and `music` (`audio-player`, name `tracker-miner-f`), segment attributes `background_wanted: true`, `pre_committed_miss: true`, `spoof: true`; both entries declare `normal`. The memo also gets its one open/closed header line at assembly.
