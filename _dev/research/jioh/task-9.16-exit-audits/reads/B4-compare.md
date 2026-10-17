# Task 9.16 claim audit — blind reader B4: comparison

Phase 2 of reader B4's blind re-read, for the claims outside the workload dataset. It compares the repository's wording at `928aa8fd` (`git show HEAD:<path>`) with the passages in `reads/B4-reads.md`. That file was finished before this comparison began (sha256 `5bff87f4c46b4df778eed4ef1b27e53a4c7df38dbfd71a387eccea412c6d1417` when Phase 2 started) and has not been edited since. Claim ids are rows of `claims/outside-inventory.md`. Path shorthands: `vol-06` = `docs/guidebook/vol-06-archetypes-and-grounding.md`, `vol-01` = `docs/guidebook/vol-01-systems-and-scheduling.md`, `G/0N` = `docs/guidebook/dataset/0N-*.md`, `proposal` = `docs/research-proposal.md`.

Verdicts: SUPPORTED, meaning the wording stays within the passage. WORDING-FIX, meaning the source supports the core of the claim but the wording goes beyond it in object, unit, statistic, scope or population. CONTRADICTED, meaning the source says otherwise. NOT IN SOURCE, meaning the statement or quotation is not in the source read. UNVERIFIABLE, meaning the source could not be reached.

## Summary

Out of 39 claims: SUPPORTED 22 · WORDING-FIX 12 · CONTRADICTED 1 · NOT IN SOURCE 2 · UNVERIFIABLE 2.

| Claim | Topic | Location | Verdict |
|---|---|---|---|
| A-69 | Chambers, Counter-Strike session times | proposal:309 | WORDING-FIX |
| C-18 | catch-up: Fiedler / mpv / Chromium | vol-01:3059 | SUPPORTED (note) |
| D-13 | Fiedler game loop | vol-06:460 | SUPPORTED |
| B-32 | mpv audio refill | docs/simulator/simulator-guide.md:136 | SUPPORTED (note) |
| B-33 | Chromium fake audio | docs/simulator/simulator-guide.md:136 | SUPPORTED |
| B-34 | Fiedler game loop | docs/simulator/simulator-guide.md:136 | SUPPORTED |
| E-18 | Fiedler game loop | G/02:137 | SUPPORTED |
| F-52 | Fiedler game loop | G/08:1144, :1656 | SUPPORTED |
| D-12 | periodic tools skip by default | vol-06:460 | WORDING-FIX |
| E-17 | periodic tools skip by default | G/01:289; G/02:137 | WORDING-FIX |
| E-16 | rt-app's time unit | G/03:244, :2397 | WORDING-FIX |
| D-14 | GStreamer late frames | vol-06:462 | WORDING-FIX |
| D-21 | LAVD talk: ~300 tasks | vol-06:1108, :1126, :1247 | SUPPORTED |
| E-28 | LAVD talk: 1.4 schedules per wake | G/04:1919 | NOT IN SOURCE |
| D-23 | LAVD slide 16 graph | vol-06:1749, :1863, :1889 | WORDING-FIX |
| F-16 | LAVD slides 12 and 16, wineserver | G/06:539 | CONTRADICTED |
| E-29 | Valve and LAVD | G/02:689 | WORDING-FIX |
| F-19 | LAVD developer | G/08:226 | SUPPORTED |
| D-27 | Steam Deck 60 Hz | vol-06:1424, :1665, :3546, :3661, :3826 | SUPPORTED |
| D-31 | Gregg `perf sched` | vol-06:3826 | SUPPORTED |
| D-36 | Chromium site-per-process | vol-06:1818 | WORDING-FIX |
| D-37 | GLAM: five tabs | vol-06:2647, :2766 | SUPPORTED (note) |
| E-13 | GLAM: five tabs in one window | G/01:598; G/03:419 | WORDING-FIX |
| D-38 | SWELL-KW keystrokes | vol-06:828, :2366, :2464 | SUPPORTED |
| E-20 | SWELL-KW description | G/01:788 (and G/02, G/03) | SUPPORTED |
| D-39 | Proton under the Steam client | vol-06:2366 | WORDING-FIX |
| D-40 | SteamCMD account | vol-06:2366 | SUPPORTED |
| D-42 | CpsMark+ Table 4 | vol-06:2248 | UNVERIFIABLE |
| E-38 | interbench Burn "until done" | G/02:1044 | NOT IN SOURCE |
| E-50 | González & Mark: 3:08 and 11:28 | G/01:1057 | WORDING-FIX |
| E-51 | González & Mark: 11:28 | G/03:603; G/04:1564 | SUPPORTED |
| E-52 | ananicy-cpp key, CachyOS default | G/01:83, :442, :946, :1500; G/04:194 | SUPPORTED |
| E-53 | GitHub runner limits | G/01:874; G/02:610 | SUPPORTED |
| F-13 | Coetzee, short-lived processes | G/06:518 | SUPPORTED |
| B-41 | Game Mode recognition undocumented | docs/background-guide.md:18 | SUPPORTED |
| B-26 | Field & Welsh | harness/experiments/rq0-gate.yaml:476–481 | UNVERIFIABLE |
| B-01 | Brodersen balanced accuracy | docs/harness/metrics.md:258 | SUPPORTED |
| A-62 | Cargo Book | proposal:185 | SUPPORTED |
| A-25 | Ananicy / ananicy-cpp | docs/related-work.md:40; proposal:540 | WORDING-FIX |

**A correction to my Phase 1 read, disclosed here because `B4-reads.md` cannot be edited.** In Phase 1 I read the LAVD talk's slide 16 (the topic on the LAVD talk slides, T-05) from a render of the visible page. Here, after the repository's record (Troy.exe, wineserver on slide 16) prompted me, I extracted the embedded image itself (`pdfimages`, page 16, object 158, 2048×211 px). It is wider than the slide, and its left part, which the visible slide crops off, holds `Troy.exe[7781/0]` ⇄ `wineserver[7256/0]` (`epoll (134200)`, `pipe_read (58134)`) and `wineserver[7256/0]` ⇄ `explorer.exe[7301/0]` (`pipe_read (20549)`, `epoll (20489)`). Copy: `<scratch>/t05/img16/i-008.png`, sha256 `552f461643267098c03fc3df119b02fb228483511e6490f072dea7f674b64300` (`<scratch>` is the scratch folder named in `B4-reads.md`). The rest of the image matches my Phase 1 node list. D-23 and F-16 below use the full image. This finding is not blind: the repository's wording prompted it.

---

## Per claim

### A-69 — proposal:309
- Repository: "on one Counter-Strike server most sessions lasted minutes — a Weibull fit with a median of about 9.6 min — and more than 99 % under 2 h (`chambers-imc05`)".
- Passage (Chambers et al., p. 4, §3.2): "a Weibull distribution with β = 0.5, η = 20, and γ = 0 closely fits the PDF of measured session times"; "more than 99% of all sessions last less than 2 hours." The word "median" does not occur in the paper.
- Verdict: **WORDING-FIX**. The 9.6 min is our arithmetic: the median of a Weibull with shape 0.5 and scale 20 min, 20·(ln 2)². The sentence reads as if the source reported it.
- Fix: "a Weibull fit (shape 0.5, scale 20 min), whose median works out to about 9.6 min (our arithmetic), and more than 99 % under 2 h".

### C-18 — vol-01:3059
- Repository: rt-app's "absolute" mode piles up and catches up late iterations; the fixed-timestep game loop "화면은 한 번만 그리면서 simulation step은 이렇게 따라잡고, 따라잡는 횟수에 상한을 둡니다" (renders once while catching up simulation steps, with a cap on the catch-up); "mpv는 비어 버린 audio buffer를 한 번에 다시 채우고" (mpv refills an emptied audio buffer in one go); Chromium's fake output, used when there is no sound device, "늦은 callback을 한 번 돌린 뒤 다음 제때 간격으로" (runs a late callback once, then moves to the next on-time interval); "둘 다 늦은 일을 다시 돌리지 않습니다" (neither re-runs late work).
- Passages:
  - rt-app, `rt-app.c:589–596`: absolute mode keeps the old reference, so late timer events return without sleeping.
  - Fiedler: `while ( accumulator >= dt )` … `render( state );` and `if ( frameTime > 0.25 ) frameTime = 0.25;`.
  - mpv, `buffer.c:620–653`: each wake-up writes the whole free space.
  - Chromium, `fake_audio_worker.cc:177–193`: "Even if we're late, this callback must be called" and "find the next nearest ontime interval".
  - Chromium, `audio_output_resampler.cc:383–388`: the fake output is the fallback when the audio device cannot be opened.
- Verdict: **SUPPORTED**.
- Note: in mpv the audio that was due during an underrun is not dropped. Playback stops, and `ao_start` later "plays all data in the queue", so that audio plays late. "다시 돌리지 않습니다" (does not re-run) holds for wake-ups but not for data.
- Optional addition: "(mpv: the queued audio is played late, not dropped)".

### D-13 — vol-06:460 (last sentence)
- Repository: "고정된 시간 간격으로 도는 게임 루프가 화면은 한 번만 그리면서 시뮬레이션 단계를 따라잡는 경우" (a fixed-timestep game loop rendering once while catching up simulation steps).
- Passage: Fiedler, "Free the physics": the inner `while ( accumulator >= dt )` loop, then one `render( state );`.
- Verdict: **SUPPORTED**.

### B-32 — docs/simulator/simulator-guide.md:136
- Repository: "mpv drops late video frames by default and its audio output refills a drained buffer in one write (`mpv`)".
- Passages: `options.rst:1143–1144` "<vo> Drop late frames on video output (default)"; `buffer.c:620–653`: the whole free space is written in one `driver->write` call.
- Verdict: **SUPPORTED**. The note under C-18 applies: after an underrun the queued audio is played late, not dropped.

### B-33 — docs/simulator/simulator-guide.md:136
- Repository: "Chromium's fake audio output runs a late callback once and moves to the next on-time interval (`chromium`)".
- Passage: `fake_audio_worker.cc:177–193`, as quoted under C-18.
- Verdict: **SUPPORTED**.

### B-34 — docs/simulator/simulator-guide.md:136
- Repository: "a fixed-timestep game loop catches up its simulation steps, capped, and renders once per loop (`fiedler-gaffer04`)".
- Passages: Fiedler, "The final touch": `if ( frameTime > 0.25 ) frameTime = 0.25;`, the `while` loop, then one `render`. The text also says: "Alternatively you can clamp at a maximum # of steps per-frame".
- Verdict: **SUPPORTED**.

### E-18 — G/02:137
- Repository: "fixed-timestep game loop의 simulation 단계는 밀린 주기를 따라잡고" (a fixed-timestep loop's simulation steps catch up on the missed periods).
- Passage: as D-13.
- Verdict: **SUPPORTED**.

### F-52 — G/08:1144, :1656
- Repository: "fixed-timestep 게임 loop의 simulation step은 따라잡습니다" (the fixed-timestep game loop's simulation steps catch up).
- Passage: as D-13.
- Verdict: **SUPPORTED**.

### D-12 — vol-06:460
- Repository: "그때 읽은 주기 작업 도구들은 기본 동작에서 놓친 주기를 다시 돌리지 않고 건너뜁니다. interbench, ROS 2의 executor, Lipari와 Palopoli가 Linux용으로 제시한 주기 thread, 그리고 rt-app의 기본 모드가 그렇습니다." (the periodic tools read then skip missed periods by default: interbench, ROS 2's executor, the Linux periodic thread Lipari and Palopoli present, and rt-app's default mode).
- Passages:
  - interbench, `interbench.c:398–411`: skips whole intervals.
  - Teper et al., p. 3: "the executor may skip timer jobs".
  - Lipari & Palopoli, §2.1 Listing 1, "Structure of a periodic thread in Linux": `timespec_add_us(&next, ps->period_us); clock_nanosleep(…TIMER_ABSTIME, &next…)`, and on a deadline miss "we abort the thread". Skipping appears only in §3.1 Listing 2, for soft real-time, where it is offered "As an alternative … skip future instances".
  - rt-app, `rt-app.c:594–596`: relative mode sets `t_next` to now, which re-anchors the timer.
- Verdict: **WORDING-FIX**.
  - Lipari & Palopoli's periodic thread does not skip by default. Their reference listing advances by one period from the previous activation, so a late thread runs back-to-back, and it aborts on a miss. Only their soft real-time variant skips.
  - rt-app's default does not skip onto the original grid; it re-anchors to the late instant.
- Fix: "… interbench, ROS 2's executor and the soft real-time periodic thread of Lipari and Palopoli (their Listing 2) skip late periods, and rt-app's default mode re-anchors its timer to the late instant; none of them re-runs the missed periods".

### E-17 — G/01:289; G/02:137
- Repository: G/02:137 lists "interbench, ROS 2 executor, Lipari와 Palopoli의 주기 thread, rt-app의 기본 모드" (interbench, the ROS 2 executor, Lipari and Palopoli's periodic thread, rt-app's default mode) as skipping by default, and says rt-app's "absolute" mode and the fixed-timestep loop catch up. G/01:289 lists interbench, the ROS 2 executor, rt-app's default mode and mpv dropping late video frames.
- Passages: as D-12. mpv: `options.rst:1143`. rt-app absolute mode: `tutorial.txt:548–567`.
- Verdict: **WORDING-FIX**: the same two points as D-12, Lipari & Palopoli at G/02:137 and the rt-app default at both locations. The mpv and absolute-mode parts are SUPPORTED.
- Fix: as D-12.

### E-16 — G/03:244, :2397
- Repository: "`rt-app` — Linux scheduler 연구에서 널리 쓰는 workload 생성 도구로, 시간을 µs 정수로 다룹니다" (a workload generator widely used in Linux scheduler research; handles time as integer µs).
- Passages:
  - `tutorial.txt:350–367`: run, runtime and sleep are "Integer … in usec".
  - `tutorial.txt:156`: delay is in usec.
  - `tutorial.txt:221–235`: dl-runtime, dl-period and dl-deadline are in usec.
  - `tutorial.txt:36`: "duration : Integer. Duration of the use case in seconds".
  - The timer `period` is an int passed through `usec_to_timespec`; the timer paragraph states no unit.
  - Nothing in the files read says rt-app is widely used.
- Verdict: **WORDING-FIX**. Event and deadline times are integer µs, but the global duration is in integer seconds. "Widely used" is not in the source read.
- Fix: "a workload generator whose task-event times (run, sleep, timer period, deadline parameters) are integer microseconds (the use case's duration is in seconds)", with "widely used" dropped or cited.

### D-14 — vol-06:462
- Repository: "영상 재생에서는 GStreamer의 영상 출력이 그렇게 합니다. 지금 시각이 들어 있는 frame은 바로 그리고, 그보다 앞의 frame은 버립니다." (GStreamer's video output does that: it draws the frame containing now at once and drops the frames before it).
- Passages:
  - `gstvideosink.c:177`: `gst_base_sink_set_max_lateness (…, 5 * GST_MSECOND)`.
  - `gstbasesink.c:118–129`: a buffer is too late when "presentation time … plus the duration is before the current time"; "If the frame is later than max-lateness, the sink will drop the buffer".
  - `gstbasesink.c:3209–3216`: "if we did not receive anything valid for more than a second, render it anyway".
- Verdict: **WORDING-FIX**. A frame whose end passed less than 5 ms ago is still rendered, and after more than 1 s without a render a late frame is rendered anyway. The base-sink default (−1) never drops. G/02:137 already says it correctly ("5 ms 넘게 늦은 frame을 버리고", drops frames more than 5 ms late).
- Fix: "the video sink drops a frame that ends more than 5 ms before now (max-lateness 5 ms) and draws the current one, rendering anyway after a second without a frame".

### D-21 — vol-06:1108, :1126, :1247
- Repository: "Min은 2024-04-17 발표에서 게임을 하는 동안 시스템 task를 포함해 약 300개의 task가 scheduling된다고 보고했다" (Min reported in his 2024-04-17 talk that about 300 tasks, system tasks included, are scheduled while a game runs). Line 1108 adds that the number counts the whole system, system tasks included, while gaming.
- Passages:
  - Slide 1: "Changwoo Min … April 17, 2024".
  - Slide 12: "Around 300 tasks are scheduled while running a game." and, of the top 30-40, "Around half of them are system tasks".
  - Slide 10: "We collect and analyze all scheduling activities while playing games."
- Verdict: **SUPPORTED**. The slides never say "system-wide" in so many words, but slide 10 and the system tasks among the most scheduled tasks support it.

### E-28 — G/04:1919
- Repository: "(9.4 D9; lavd-ossna24 s14, about 1.4 on average)", that is, a wake is split into about 1.4 schedules on average.
- Passage: slide 14 gives only "Preemption … takes only 25-30% of scheduling", "70-75% … initiated by waiting system calls" and the pie slice "sched_preempt (28.78%)". No slide states schedules per wake.
- Verdict: **NOT IN SOURCE**. The 1.4 is the 9.4 slice's decision D9 arithmetic, 1/(1−0.2878) ≈ 1.40. That arithmetic assumes every wake ends in a waiting call, but the sentence attributes the number to slide 14.
- Fix: "(9.4 D9's arithmetic from s14's 28.78 % preemption share: about 1.4 schedules per wake, our derivation)".

### D-23 — vol-06:1749, :1863, :1889
- Repository: slide 16 shows "게임 본체와 `wineserver`가 서로 주고받는 작은 고리, 여러 작업 thread가 그래픽 제출 thread 하나로 모이는 모양, 소리 서버끼리의 고리" (a small loop between the game body and wineserver; several worker threads converging on one graphics-submit thread; a loop among the sound servers). Line 1863: wineserver "슬라이드 16의 그림에서 게임 본체와 계속 주고받는 고리에 있습니다" (sits in the loop exchanging with the game body in slide 16's figure); slide 13 calls it a short coordination task of 260 µs.
- Passages:
  - Slide 16's embedded image (the correction above): `Troy.exe[7781/0]` ⇄ `wineserver[7256/0]`; four `Task worker thr` → `dxvk-cs[7922/7781]` by `futex_wait`; `dxvk-cs` → `dxvk-submit[7920/7781]` by `futex_wait (30970)`; a loop among winepulse, pipewire-pulse and pipewire.
  - Slide 13: "Some coordination tasks run very shortly (e.g., wineserver:260 usec)".
- Verdict: **WORDING-FIX**. The wineserver loop and the sound-server loop are there; the wineserver loop is drawn in the part of the image the visible slide crops off. The workers converge on `dxvk-cs`, the DXVK command-stream thread, which then wakes `dxvk-submit`; they do not converge on a submit thread.
- Fix: "several worker threads converging on one DXVK thread (`dxvk-cs`), which wakes the submit thread (`dxvk-submit`)", and optionally note that the wineserver loop lies outside the slide's visible area.

### F-16 — G/06:539
- Repository: "슬라이드 12장은 wine을 시스템 task로 분류하고, 16장의 그래프는 wineserver를 중심으로 한 구조를 보입니다" (slide 12 classes wine as a system task, and slide 16's graph shows a structure centred on wineserver).
- Passages:
  - Slide 12: "Around half of them are system tasks -- especially, wine, graphics, and audio servers".
  - Slide 11, "30.00 percentile of waker-waiter": `wineserver[5789/0]` is the hub linked to `redDispatcher1…7` and `wine_xinput_hid` (all of process 6340).
  - Slide 16 (full embedded image): wineserver sits only in a side loop with `Troy.exe` and `explorer.exe`; the centre of the graph is `dxvk-cs`.
- Verdict: **CONTRADICTED** for slide 16. The wineserver-centred structure is on slide 11. The slide 12 part is SUPPORTED.
- Fix: "slide 12 counts wine among the system tasks; the graph centred on wineserver is slide 11's (with one game process's dispatcher threads); on slide 16 wineserver is a side loop with the game's main thread and explorer.exe".

### E-29 — G/02:689
- Repository: "`docs/workload/grounding-sources.md`는 gaming scheduling이 실제 문제라는 근거로 "Valve ships it"를 적음" (`docs/workload/grounding-sources.md` writes "Valve ships it" as grounds that gaming scheduling is a real problem).
- Passages:
  - SteamOS 3.8 (3.8.10, 2026-06-18): "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`".
  - scx_lavd sources: "Copyright (c) 2024 Valve Corporation. Author: Changwoo Min <changwoo@igalia.com>".
  - LWN (2026-01-07): no mention of Valve.
- Verdict: **WORDING-FIX**. "Valve ships it" no longer appears in `docs/workload/grounding-sources.md`, whose line 30 now reads "Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default". The release notes support "ships it in SteamOS 3.8 as user-selected". No source I read uses "sponsors"; what the sources show is that Valve holds the copyright on the scx_lavd sources.
- Fix: quote the current line, or "Valve ships LAVD in SteamOS 3.8 as a scheduler the user selects (`steamos-lavd`)". Drop "sponsors" unless a source states it.

### F-19 — G/08:226
- Repository: "LAVD(Igalia의 Changwoo Min이 SteamOS·Steam Deck을 위해 만든 Linux scheduler)" (LAVD, a Linux scheduler made by Igalia's Changwoo Min for SteamOS and the Steam Deck).
- Passage: LWN: "Min said that he has been developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck."
- Verdict: **SUPPORTED**. LWN reports this as Min's own statement.

### D-27 — vol-06:1424, :1665, :3546, :3661, :3826
- Repository: the frame period is grounded on "Steam Deck LCD의 기본 화면 갱신 60 Hz" (the Steam Deck LCD's default 60 Hz refresh), and the value is labelled design.
- Passages: SteamOS 3.2 post: "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps)" and "60hz = 16.66ms/frame". Tech specs: "Refresh rate 60Hz".
- Verdict: **SUPPORTED**.

### D-31 — vol-06:3826
- Repository: "Gregg가 빌드 하나를 1초 동안 `perf sched`로 잡은 기록에 붙고" (the note attaches to Gregg's one-second `perf sched` capture of a build); the numbers are not carried over.
- Passage: §6.7: "# perf sched record -- sleep 1"; "this example is an 8 CPU server running a software build".
- Verdict: **SUPPORTED**.

### D-36 — vol-06:1818
- Repository: "`renderer-hidden`(사이트마다 렌더러 하나, Chromium의 site-per-process 모델)" (one renderer per site, Chromium's site-per-process model).
- Passages:
  - Process model doc: "In (one-)site-per-process mode, each process is locked to documents from a single site."
  - Same doc: separate instances of a principal "can safely run in separate processes".
  - Same doc, soft process limit: same-site processes are reused only over the limit, as in the 50 `example.com` tabs example.
- Verdict: **WORDING-FIX**. Site-per-process means one site per renderer, not one renderer per site; a site can occupy many renderers. The repository's own count of one renderer per tab, at line 2647, agrees with the source.
- Fix: "(each renderer holds one site — Chromium's site-per-process model; separate tabs of a site get separate renderers below the process limit)".

### D-37 — vol-06:2647, :2766
- Repository: "탭 다섯 개는 Firefox의 Linux 사용 통계(`glam`)에서" (the five tabs come from Firefox's Linux telemetry, `glam`).
- Passage: GLAM, Linux release, metrics ping, read 2026-10-17. The p50 of the per-client maximum tab count is bucket 4.49 for versions 155 and 156 and bucket 3.80 for 157. With exponential bucket keys as lower bounds, bucket 4.49 holds the integer 5 and bucket 3.80 holds 4. The repository's record cites version 152 (4.67), which the API no longer serves.
- Verdict: **SUPPORTED** for 155 and 156 (5 tabs).
- Note: the newest, partial version 157 gives 4, and the version-152 value cannot be re-read at the live API.

### E-13 — G/01:598; G/03:419
- Repository: "창 하나에 tab 다섯" (five tabs in one window) and "한 브라우저 창에 탭이 다섯 개라는 것은 Firefox의 Linux telemetry(`glam`)에서" (five tabs in one browser window comes from Firefox's Linux telemetry).
- Passages:
  - `metrics.yaml:254`: "maximum number of tabs open during a subsession, across all windows".
  - GLAM: the window-count p50 (per-client maximum) is 1.
- Verdict: **WORDING-FIX**. The tab count is across all windows, not per window. The median window count of 1 makes the reading plausible, but the source does not state tabs per window.
- Fix: "a median of five tabs open at most across all windows, with a median of one window (`glam`)".

### D-38 — vol-06:828, :2366, :2464
- Repository: the keystroke streams are SWELL-KW's (Koldijk et al., 2014) real input, replayed by the measurement campaign.
- Passages:
  - §3.5: "Computer interactions were logged with the key-logging application uLog".
  - The uLog XML records per-key `<TimeStamp>` and `<KeyboardValue>` with `<ControlApplication>`.
- Verdict: **SUPPORTED**. The replay itself is ours.

### E-20 — G/01:788 (also G/02:310, G/03:537, :2320, the G/02 glossary)
- Repository: "2012년 Windows 실험실에서 학생과 인턴 25명이 지식 노동 과제를 약 3시간씩 한 기록" (a record of 25 students and interns doing knowledge-work tasks for about 3 hours each in a Windows lab, in 2012), with per-key timestamps and the foreground application.
- Passages:
  - §3.7: "25 students participated … They were interns from TNO and students from Delft University of Technology".
  - §3.3: "the total experiment took about 3 hours".
  - §3.4: "Windows 7 Professional", "controlled lab setting".
  - DANS file names are dated September to November 2012; the paper states no year.
  - uLog events carry the application.
- Verdict: **SUPPORTED**. The year rests on the DANS data files, not on the paper.

### D-39 — vol-06:2366
- Repository: "Proton은 Steam 클라이언트 아래에서만 돕니다" (Proton runs only under the Steam client).
- Passages: README: "**Proton** is a tool for use with the Steam client"; "**Most users should use Proton provided by the Steam Client itself.**" No client-less use is documented.
- Verdict: **WORDING-FIX**. The source does not say "only". It describes a tool for use with the Steam client and documents no other way to run it.
- Fix: "Proton is documented only as a tool for use with the Steam client".

### D-40 — vol-06:2366
- Repository: "`steam`의 다운로드는 계정이 있어야 해서, 익명으로 로그인한 SteamCMD의 숫자를 … 근사로 씁니다" (the Steam download needs an account, so SteamCMD's numbers under an anonymous login are used as an approximation).
- Passage: SteamCMD wiki: "To download most game servers, you can login anonymously"; under "No subscription": "the game/server … either requires a login or that you have purchased the game".
- Verdict: **SUPPORTED**. I read the 2026-10-16 Internet Archive copy, because the live page is behind a bot challenge.

### D-42 — vol-06:2248
- Repository: "인용 문서는 Table 4를 작업과 모듈마다의 하드웨어 민감도 표로 적고(1.77배는 CC 모듈에서 가장 좋은 그래픽 카드 구성을 기본 구성과 비교한 수)" (the citing document describes Table 4 as a per-workload and per-module hardware-sensitivity table; 1.77× compares the CC module's best graphics-card configuration with the base one). The full text is said to have been read from a Wayback copy of the publisher PDF.
- Passage: none. ScienceDirect returns 403, the Elsevier API without a key returns metadata only, and the 2023-01-14 Wayback captures of the article and its `pdfft` link are HTML without the body.
- Verdict: **UNVERIFIABLE**.
- Fix: none proposed. The table structure and the 1.77 need a reader with access. Note also that the Wayback `pdfft` captures I found are HTML, not the PDF; the copy the 2026-09-13 independent read R04 used should be identified by its capture timestamp.

### E-38 — G/02:1044
- Repository: "`cpu-batch`는 원래 "a process that simply computes until it is done"이라는 interbench Burn의 한 줄이었습니다" (`cpu-batch` was originally interbench Burn's line "a process that simply computes until it is done").
- Passages:
  - `interbench.8:120–121`: "Burn: A configurable number of threads fully cpu bound (4 by default)."
  - `interbench.c:595–632`: the threads loop `burn_loops` until the benchmark posts the stop semaphore.
- Verdict: **NOT IN SOURCE**. The quoted line is not in interbench. Burn's threads also do not finish on their own: they run until the benchmark stops them.
- Fix: "`cpu-batch` started from interbench's Burn load (N fully CPU-bound threads that run until the benchmark stops them); the phrase "a process that simply computes until it is done" is the repository's own (`docs/data-contracts.md`)".

### E-50 — G/01:1057
- Repository: "`gonzalez-chi04`의 사건 하나에 약 3분(3분 08초)과 working sphere 안에서 전환 전까지의 평균 연속 구간 11분 28초" (`gonzalez-chi04`'s about 3 minutes (3 min 08 s) per event, and 11 min 28 s as the mean continuous segment in a working sphere before switching).
- Passages:
  - Table 2: 0:03:08 is the row "All events except “Formal meetings” and “Other”"; the text adds "(leaving out formal meetings, unknown, and personal events)".
  - Table 4: 0:11:28 is the row "Central and Peripheral WS only".
- Verdict: **WORDING-FIX**. Both averages exclude part of the population: events other than formal meetings, unknown and personal; spheres other than metawork, personal and unknown. Over all events the figure is 8:55, and over all spheres 13:49.
- Fix: "about 3 minutes per event (3 min 08 s, leaving out formal meetings, unknown and personal events) and 11 min 28 s per working-sphere segment (central and peripheral spheres)".

### E-51 — G/03:603; G/04:1564
- Repository: "the mean continuous segment in a working sphere before switching, 11 min 28 s".
- Passages: p. 117: "the actual average duration of a working sphere segment is quite short (11 min, 28 sec.)"; Conclusion: "eleven and a half minutes in continuous work on a project or theme before they switch to another".
- Verdict: **SUPPORTED**. This is the paper's own phrasing.
- Note: Table 4 scopes the figure to central and peripheral spheres.

### E-52 — G/01:83, :442, :946, :1500; G/04:194
- Repository: the catalogue CachyOS installs with ananicy-cpp and enables (`ananicy-rules` at `03ef03fb`), matched on each process's `argv[0]` basename, untruncated; on that key, 19 of 35 bound names and all names in 7 of 50 files.
- Passages:
  - ananicy-cpp `process.cpp:193–257`: argv[0] basename first, then the exe basename, then `comm`.
  - `cachyos-settings` depends on `ananicy-cpp` and `cachyos-ananicy-rules`, and its `post_install` enables `ananicy-cpp`.
  - The installer's `pacstrap.conf` lists `cachyos-settings` among the base packages.
- Verdict: **SUPPORTED**.
- Notes:
  - The 19-of-35 and 7-of-50 counts are our own computation, not a source statement.
  - Pinning the catalogue to commit `03ef03fb` is ours; the installer installs whatever version the `cachyos-ananicy-rules` package is.
  - I read the installer and package sources, not the ISO image.

### E-53 — G/01:874; G/02:610
- Repository: runner storage 14 GB; "Each job in a workflow can run for up to 6 hours of execution time"; 4 vCPU, 16 GB RAM, 14 GB SSD; `ubuntu-24.04` with 4 vCPU.
- Passages: Limits: "All GitHub-hosted runners | Job execution time | 6 hours | Each job in a workflow can run for up to 6 hours of execution time." Runners, for public repositories: "Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04 …".
- Verdict: **SUPPORTED**. This holds for a public repository; private repositories get 2 CPUs and 8 GB.

### F-13 — G/06:518
- Repository: Coetzee "리눅스 커널 빌드의 짧게 사는 많은 프로세스를 `cp`와 `mkdir`을 예로 수 없이 말한다" (speaks of the Linux kernel build's many short-lived processes, with `cp` and `mkdir` as examples, without a count).
- Passage: p. 9: "the Linux kernel build’s enormous number of short-lived processes like cp and mkdir".
- Verdict: **SUPPORTED**.

### B-41 — docs/background-guide.md:18
- Repository: "(Windows' and macOS's Game Mode … on Windows by default for most games, on macOS when a game goes full screen — and neither documents how it recognises a game.)"
- Passages:
  - Microsoft: "Game Mode works by default for most Windows games …". The only mechanism documented is a declaration: "By using the expandedResources capability, you can explicitly declare that the game will work with Game Mode".
  - Apple Support: "When your game enters full screen, Game Mode automatically turns on for that game."
  - Apple Developer, `LSSupportsGameMode`: "If you don’t include this key in your Info.plist, Game Mode might not turn on for your game."
  - None of these states a list, heuristic or category.
- Verdict: **SUPPORTED**.
- Notes:
  - The Xbox Support page could not be read (rendered by JavaScript).
  - Both vendors document a developer declaration bearing on Game Mode, `expandedResources` and `LSSupportsGameMode`; the sentence could mention them.

### B-26 — harness/experiments/rq0-gate.yaml:476–481 (lines 484–489 in the uncommitted working tree, same text)
- Repository: "Field and Welsh's consistency result holds for balanced one-way arrays and their simulations ran 5 and 15 clusters of equal size, where the cluster bootstrap underestimated the variance".
- Passage: abstract only, via Crossref: "bootstrapping clustered data from one-way arrays … the cluster bootstrap gives consistent estimates under both the transformation and the random-effect model". The full text is closed (OUP 403, ANU copy restricted).
- Verdict: **UNVERIFIABLE**. "One-way arrays" is in the abstract. "Balanced", the asymptotic regime, the simulations' 5 and 15 equal clusters and the underestimation are not in the abstract and could not be read.

### B-01 — docs/harness/metrics.md:258 (same line in the working tree)
- Repository: "Balanced accuracy is defined for two classes (`brodersen-icpr10`, which defines it off a two-by-two matrix and gives no K-class form)".
- Passages:
  - §III: "the balanced accuracy, which can be defined as the average accuracy obtained on either class. Based on a confusion matrix [2×2] … ½ (TP/P + TN/N)".
  - §V: "The notions of the posterior distribution of both the accuracy and the balanced accuracy can be generalized in a natural way to a multiclass setting … replacing the Beta distribution by the Dirichlet distribution."
- Verdict: **SUPPORTED**. The paper gives no K-class formula.
- Optional precision: "(… and only remarks that its posterior generalises to K classes via a Dirichlet)".

### A-62 — proposal:185
- Repository: "`cargo build` compiles a Rust package and its dependencies, Cargo invoking `rustc` (`cargo-book`)".
- Passages: cargo-build(1): "Compile local packages and all of their dependencies." Why Cargo Exists: "Invokes rustc or another build tool with the correct parameters to build your package."
- Verdict: **SUPPORTED**.

### A-25 — docs/related-work.md:40; proposal:540
- Repository:
  - related-work.md: "ananicy-cpp (its upstream, Ananicy, archived since 2023-03-21) … a rule's `name` is matched against the basename of the process's `argv[0]`, untruncated, and the rule's type sets the process's nice value — on every thread — its I/O class and its scheduling policy".
  - proposal:540: the catalogue "as CachyOS installs and enables it with ananicy-cpp", matched on the untruncated `argv[0]` basename.
- Passages:
  - GitHub repository metadata: `archived: true`, `pushed_at 2023-03-21T15:03:42Z`; last commit `1e2cc9a6`, committed 2023-03-21 and authored 2021-10-07. Neither the API nor the README gives the date of archiving.
  - ananicy-cpp `process.cpp:193–257`: the matching order.
  - `priority.cpp:41–51`: nice set per thread via `/proc/<pid>/task`.
  - `set_io_priority` and `set_sched`: applied to the pid.
  - README "Types": "All options defined in the type will be used as if written explicitly in the rule".
- Verdict: **WORDING-FIX**. 2023-03-21 is the date of the last commit and push. The archiving date is not shown by any source read. The matching, per-thread nice, I/O class, policy, and CachyOS default parts are SUPPORTED.
- Fix: "its upstream, Ananicy, archived (last commit 2023-03-21)".

---

## Observations outside the claim list

1. **The Chromium fake audio worker says which tick a late job belongs to** (vol-06:462 "오디오와 게임에서는 읽은 출처가 어느 눈금을 늦게 처리하는지 말하지 않아서", for audio and games the sources read do not say which tick is processed late; G/02:137 "그쪽 출처(Chromium의 fake audio worker, Vulkan의 FIFO 모드)는 늦은 일이 어느 격자의 것인지 말하지 않기 때문입니다", those sources, Chromium's fake audio worker and Vulkan's FIFO mode, do not say which grid point the late work belongs to).
   - In `fake_audio_worker.cc:163–193` the late callback runs with the `read_time` it was scheduled for, which is the earliest overdue tick. The worker then jumps to the first interval after now.
   - So for Chromium the source does say it: one late job, carrying the oldest missed tick. That is not the most recent missed tick, which the TIMER skip rule chooses.
   - Fiedler's loop catches up on all of them. I did not read the Vulkan source.
2. **The Burn default differs between interbench's man page and its code.** The man page says "4 by default"; the 0.31 code defaults to the number of online processors (`interbench.c:1520`), and its usage text agrees with the code. Any repository statement of Burn's thread count should say which of the two it follows.
3. **The working tree is not clean.** It has uncommitted changes to `docs/harness/metrics.md` and `harness/experiments/rq0-gate.yaml`, which hold claims B-01 and B-26. The text of both claims is unchanged; only B-26's line numbers moved (476 → 484).
4. **GLAM's live API serves only the three current release versions** (155–157 on 2026-10-17). Any record that cites an older version's value, such as version 152's 4.67 in the 9.10 slice's search log S3, cannot be re-read at the API. The records should keep the response file they read.
