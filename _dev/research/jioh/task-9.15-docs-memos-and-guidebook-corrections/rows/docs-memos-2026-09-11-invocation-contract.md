# Work-list rows — `docs/memos/2026-09-11-invocation-contract.md`

Chunk K17, Memos (wave 4). 2 open rows. The file has 57 lines at `d5cc7711`.

### W-0694 · applied
- At: `docs/memos/2026-09-11-invocation-contract.md` the header block after the H1 (the `> Status:` line and the `> From …` line)
- Change: Add one header line after the Status line: either closed, naming where the memo's content now lives, or open, naming the ask still outstanding and its owner. Bump the header's `Updated`.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: The memo: to 인경민 and 박이안: the invocation contract, whose normative home is `docs/data-contracts.md` §11 (contract 10). Written in Korean; the header line in the memo's own language. Whether it is open or closed is decided against the code and the records, and logged.

### W-0695 · applied
- At: `docs/memos/2026-09-11-invocation-contract.md` new — an appended `## 정정 (<date>)` section after §5; the corrected statement is in §4 '각자에게', line 51 (박이안's flags: '조건 이름은 daemon guide §4의 표 그대로(`fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`)')
- Change: Append a dated correction section in Korean naming the condition list and stating the current one: `fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle` — `whitelist` became the two name-table conditions (9.12 D6); bump the header's `Updated`; the memo's text stays.
- Final word: 9.12 D6, amended by D91, D105, D109 and D115: the `whitelist` condition becomes two conditions — `shipped_catalogue`, the name-keyed catalogue a shipping distribution enables by default (ananicy-cpp's rules as CachyOS ships them, `ananicy-rules` at `03ef03fb`, matched by `argv[0]`'s basename, untruncated, D105; on that key it keys 19 of the 35 bound names and every name in only 7 of 50 files, D109), answering RQ2 (research question 2, value); and `strongest_name_table`, the strongest name table in the catalogue's design, which carries the paper's claim (D115); 'a faithful reproduction of what shipping systems do today' and 'the whitelist approach real operating systems currently use' restated to the two conditions (D91). The harness already uses the two names.
- Sources: S12-054 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`); SX-0146 (TODO 9.15 line (from 9.12 D6), `_dev/TODO.md:179`)
- Notes: Checked: `harness/tools/harness/evaluator.py:47` CONDITIONS lists exactly the eight names above; `harness/guards/guard-spec.yaml:126`. Other parts of the memo may be stale against the invocation contract since 9.17 (the `--telemetry focus|names` flag, `docs/data-contracts.md:498`, added 2026-10-11 by `fb673690`) — not a raw row here; the heads-up memo's format row (W-0701) names the flag. The memo also gets its one open/closed header line at assembly.
