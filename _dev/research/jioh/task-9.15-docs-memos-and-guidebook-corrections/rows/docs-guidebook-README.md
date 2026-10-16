# Work-list rows — `docs/guidebook/README.md`

Chunk K16, Research guidebook, volumes 4-6 (wave 4). 1 open rows. The file has 40 lines at `d5cc7711`.

### W-0683 · applied
- At: `docs/guidebook/README.md` ## 권 목록 table, line 18 (vol 8 row '| 8 | Workload 3: 50개 coreset | 각 파일이 어떤 질문에 답하나 | 예정 |') and line 17 (vol 7 row 'Workload 2: 조립과 compile', 예정)
- Change: Give the planned volume 8's title the core set's current count, 51 files ('51개 coreset'), and mark the planned volumes 7 (timeline assembly and compile) and 8 (the core set) as answered by the dataset guidebook's volume 3 (docs/guidebook/dataset/03-timeline-to-canonical-workload.md) and volume 4 (docs/guidebook/dataset/04-the-coreset.md) in place of '예정' (planned).
- Final word: The 2026-10-14 record-gaps and doc-staleness audit, §2 items 1 and 16: the core set has 51 files, not 50 (the 51st, c2-p2a-idle, added by 9.13 on 2026-10-09); the eight-volume dataset guidebook (docs/guidebook/dataset/, 2026-10-14) now answers what the old guidebook's planned volumes 7 and 8 named, its volume 4 titled '51개의 coreset'.
- Sources: SX-0791 (record-gaps §2 item 1, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:26`); SX-0839 (record-gaps §2 item 16, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:41`)
- Cross-ref: W-0673
- Resolved at merge: The two raw rows offered either edit (the count to 51, or volumes 7–8 pointed at the dataset guidebook); both are applied, since the old guidebook's planned volumes are not being written (the 9.15 task spec, Out of scope: new guidebook volumes) and the title would otherwise keep a stale count.
- Notes: Checked at HEAD: 51 *.timeline.yaml files under dataset/timelines/coreset/; docs/guidebook/dataset/README.md lists volume 3 ('Timeline에서 canonical workload로') and volume 4 ('51개의 coreset'). Item 16's second half ('c5-t3 is now c6-alias') has no text in this file (grep at HEAD); it belongs to the coreset guide's and data-contracts' rows. The vol 6 row's status '완성' describes the pre-rebuild library — see W-0673's head note.
