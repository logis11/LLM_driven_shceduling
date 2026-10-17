# 9.16 docs chunk R — the research guidebook, volumes 1–6 and its README

Files changed: `docs/guidebook/vol-01-systems-and-scheduling.md`, `vol-02-related-work.md`, `vol-03-the-research.md`, `vol-05-shared-vocabulary.md`, `vol-06-archetypes-and-grounding.md`. `vol-04` and `README.md` unchanged. The research guidebook carries no status header, so no `Updated` was bumped. Every edit replaces text in place on one line, so the line numbers below are the same before and after. Not committed.

Finding ids: `C-nn` and `D-nn` are the outside-claims trace audit's (`claims/outside-findings.md`, parts C and D); the B4 entries are the fourth blind reader's comparison (`reads/B4-compare.md`). Where the two differ, B4's passage was followed.

## Applied

- **D2, the foreground-window row (outside-claims C-14)**: vol-01:3339. Only the Windows cell is kept ("있음"). The Linux and macOS cells are left empty, so nothing is stated for them.
- **C-10, Windows priority class**: vol-01:2094. "프로그램이 자기를 배경 작업으로 등록할 수 있습니다" is now "priority class와 단계가 있어서 프로그램이 자기 priority를 정할 수 있습니다". The `:3338` cell ("priority class") already fits that wording and stays.
- **C-20, the release that added sched_ext**: vol-01:3234. "2024년 말에 나온 kernel 버전부터" is now "Linux 6.12부터".
- **C-26, the Nielsen book**: vol-02:701 (the finding's :697). "널리 알려진 것은 이 책 덕분입니다" is now "이 책도 같은 값을 적습니다".
- **C-39, unsupported superlatives**: three lines rewritten as the finding proposes.
  - vol-02:2964 now says "카탈로그 하나를".
  - :3232 now says "많은 task로 부하를 주는 도구가 있습니다".
  - :3362 now says "한 제조사의 벤치마크 하나의 기술 문서를".
- **C-42, the commercial benchmarks**:
  - vol-02:3448: Procyon is introduced as "앞에서 본 PCMark 10과 같은 UL의 모음".
  - :3484: the shared programs are now "SYSmark 30과 같은 프로그램".
  - :3486: now says that SYSmark 30's and Procyon's office, photo and video scenarios use the same commercial programs, while PCMark 10 uses open software. "독립적으로" and "업계의 합의" are dropped.
  - :3488–3490 (the 논문으로 box): now "두 제조사의 벤치마크가 같은 상용 프로그램을 쓴다".
  - :3532 (summary): restated the same way.
- **C-44, who loads a sched_ext policy**: vol-03:54 now reads "BPF scheduler 프로그램을 실행 중에 올림".
- **D-02, the interbench manual's word**: "버퍼링" is now "캐싱(caching)" at vol-06:544 (the finding's :538, the manual translation), :1281, :1494 and :3673.
- **D-05, interbench's X emulation**: vol-06:987. The sentence now says each step is 100 ms and one rise from 0 to 100 % takes about 10 s.
- **D-10, interbench as a model**: vol-06:1265. "널리 쓰인다" is now "커뮤니티의 벤치마크로 배포된다".
- **D-12 (B4 WORDING-FIX), the periodic tools**: vol-06:460. interbench, the ROS 2 executor and Lipari and Palopoli's soft real-time thread (their Listing 2) skip late periods. rt-app's default mode re-anchors its timer to the late instant. None of them re-runs missed periods. The trace audit had marked this claim TRACED; B4's passage was followed.
- **D-14 (trace finding and B4 WORDING-FIX; B4's wording followed), GStreamer late frames**: vol-06:462. GStreamer drops a frame whose end is more than 5 ms before now (max-lateness 5 ms) and draws the current frame. If no frame has been drawn for more than 1 s, it draws a late frame anyway.
- **D-17, the Dhakal paper's authors**: vol-06:850. "외 네 명" is now "외 세 명".
- **D-20, the LAVD task count**: vol-06:1237. Now "게임을 하는 동안 시스템 task를 포함해 약 300개의 task가 scheduling되고".
- **D-22, 60 fps in the LAVD slides**: vol-06:1735. Now says no slide states a frame budget or frame period. The only on-screen text is slide 29's uncommented "60FPS", "16.5ms" and "Refresh Rate: 60" in its EEVDF screenshot.
- **D-23 (B4 wording), slide 16's graph**: vol-06:1749. The worker threads converge on DXVK's `dxvk-cs`, which wakes `dxvk-submit`. Lines :1863 and :1889 are traced and stay as they are.
- **D-26, the `corbet-lwn24` row**: vol-06:4109.
  - The description is now "Min의 LPC 2024 발표를 다룬 Corbet의 LWN 기사".
  - The tier is now "그때 deployed-system, 지금 talk·news", matching the format of the `lavd-ossna24` row.
- **D-29, the arXiv report's length**: vol-06:3207. "21쪽" is now "20쪽".
- **D-36 (B4 wording), Chromium's site-per-process model**: vol-06:1818. Now says one renderer holds documents from one site only, and below the process limit separate tabs of the same site get separate renderers.
- **D-39 (B4 wording), Proton and the Steam client**: vol-06:2366. Now "Proton은 Steam 클라이언트와 함께 쓰는 도구로만 문서화되어 있습니다".
- **D-42, CpsMark+ Table 4**: vol-06:2248. In the original paper, Table 4 is a per-workload hardware-sensitivity table, and the module values are in Table 5 and §4.7.2 (the 1.77× included).
  - B4 graded this claim UNVERIFIABLE because the reader had no access to the paper.
  - Per the brief, the earlier record therefore stands: the 2026-09-13 independent read R04 of the CpsMark+ paper. The trace finding rests on R04, so it was applied.

## Applied beyond the findings' listed locations (same fact, same restatement; easy to revert)

- **D1, the boot-default sweep (handed F1)**: vol-05:884 and vol-05:1283 said the call's periodic work is demoted "다섯에 하나꼴로" (about one in five).
  - Both now say about one cycle in twenty: 4.9 % from the measured table, 5.5 % in the compiled files.
  - :1283 also carries D1's second reason. In `c7-meeting`, about 4 of 10 boost intervals have the call demoted and waiting behind the upgrade until the next boost. This is labelled as arithmetic: 1 − 0.95¹⁰, with cycles taken as independent and ten cycles per 100 ms boost.
- **`parallelism_cap` 8's label (dataset claim D-F3-08, decided by 9.6 decision D4, which labels it convention)**: vol-06:2766 said "관례가 아니라 설계" and vol-06:4019 said "설계로 정한 값". Both now say "관례로 정한 값(8 thread 데스크톱에 적용한 `nproc` 규칙)".
- **"Valve sponsors LAVD" (outside-claims A-09 and E-29; B1 D-F1-31, B4 E-29)**: vol-02:3741 said "Valve가 그 개발을 후원하고". It now says Valve holds the code's copyright, and its author Changwoo Min says he develops LAVD at Igalia for SteamOS and the Steam Deck.
- **B4 observation 1, which tick a late job carries**: B4 lists this outside its verdict table. In Chromium's fake audio worker, the late callback runs with the oldest overdue tick, and the worker then moves to the next on-time interval. The trace audit had marked the sentence TRACED (D-15). Per the brief, the blind passage wins.
  - vol-06:462: the audio clause now states Chromium's behaviour. Only games remain "the sources read do not say", and choosing the most recent tick is this research's own choice.
  - vol-01:3077 (the TIMER skip-rule box) carried the same sentence. It is restated the same way, and its GStreamer clause gets D-14's 5 ms wording.

## Not changed

- **Record-only findings**: C-18 and D-13 (Fiedler, mpv and Chromium), D-25 (LAVD slide 10), D-44 (six ananicy rule lines) and D-46 (the `Xorg` and `dbus-daemon` rules). These ask for a read record, not new wording. B4 graded C-18 and D-13 SUPPORTED.
- **C-18's optional note** (B4, SUPPORTED): mpv's queued audio is played late, not dropped. Not added because the verdict is SUPPORTED.
- **D-37** (B4, SUPPORTED, with a note on GLAM versions 155–157): no change.
- **The boundary list's uninventoried general background** (vol-01 scheduler history years, Pathfinder, cgroups): this was left for the lead's call and is not a finding.
- **`README.md`**: no finding touches it.
- **Other findings** (compiled, measurement class reads, the new computations' proposed text, D-F4-45 the Steam window): none has a location or a matching statement in these files. The grep checks run were "Steam 창", occlusion, `renderer-hidden` pooling, the ledger, deciles, `tick_count` and `c2-p3b`.
