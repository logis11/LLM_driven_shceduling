# Reader output R02-lavd

## Copies used

| source id | URL / commit / capture | retrieved | local path | SHA-256 |
|---|---|---|---|---|
| lavd-ossna24 (slides) | https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf (HTTP 200) | 2026-09-13 | sources/lavd-ossna24/scx-lavd-oss-na24.pdf | e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475 |
| lavd-ossna24 (slides, link on the schedule page) | https://hosted-files.sched.co/ossna2024/9b/scx-lavd-oss-na24.pdf (HTTP 200) | 2026-09-13 | sources/lavd-ossna24/alt-hosted-files.pdf | e62d69cd…6402475 (byte-identical to the row above; also identical to the earlier download sources/scx-lavd-oss-na24.pdf) |
| lavd-ossna24 (schedule page) | https://ossna2024.sched.com/event/1aBOT (HTTP 200) | 2026-09-13 | sources/lavd-ossna24/sched-event-1aBOT.html (text: sched-event-1aBOT.txt) | bf0ef926b1bd1774617b4411a1d4822e786977e901d6a05fe5e27f82fac8b51e |
| corbet-lwn24 | https://lwn.net/Articles/991205/ (HTTP 200) | 2026-09-13 | sources/corbet-lwn24/lwn-991205.html (text: lwn-991205.txt) | 0ba6ea8e0eb2f19eccf37ce6dad6bd1a99a74a48d5f9af3f799a1f0e810e5f22 (differs from the earlier sources/lwn-991205.html only in subscription-ad blocks; article text identical) |
| scx | https://github.com/sched-ext/scx.git, branch `main`, commit 8b2479571c0768310510c061960d2c40cb64d160 (committer date 2026-09-11T14:45:50Z, "Merge pull request #3801 …"); full (non-shallow) clone | 2026-09-13 | sources/scx/scx/ | LICENSE: 8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643 |

Derived files: PDF text layer extracted with pypdf 6.18.0 → sources/lavd-ossna24/scx-lavd-oss-na24.pypdf.txt; all 30 slides rendered with Ghostscript at 110 dpi → sources/lavd-ossna24/pages/slide-NN.png (every slide viewed); slides 11, 13, 14, 16, 29 re-rendered at 400 dpi with crops → sources/lavd-ossna24/hires/; embedded JPEGs → sources/lavd-ossna24/img/.

Conventions below: "text layer" = quote copied from the PDF text layer (pypdf), which contains `ﬁ` ligature glyphs where the rendered slide shows "fi"; "[image]" = transcribed by viewing the rendered slide image (content not in the text layer). Slide N = PDF page N; slides 2–30 carry the same printed number in their footer.

The slides never name the game(s) traced, never name the machine/kernel on which the characterization traces (slides 11–16) were taken, and use task IDs that differ between slides (wineserver is `[5789/0]` on slide 11 and `[3845/0]` on slide 15; the slide-16 graph uses group ID 7781), so the figures on different slides appear to come from different traces; the slides do not say how many games or traces underlie the summary numbers on slides 12–14.

---

## lavd-ossna24

### C-lavd-1 — number of tasks observed while a game runs
(a) Text layer, slide 12: "● Around 300 tasks are scheduled while running a game."
Slide 13 figure [image]: x-axis "tasks" running 0 to about 128; caption (text layer) "Distribution of task’s runtime average per schedule in a game".
(b) Slide 12 ("Task scheduling and CPU utilization"), first bullet; slide 13 figure.
(c) Unit: tasks. Statistic: an approximate count ("Around"), a single rounded figure, not a stated mean or range. Scope: "while running a game" — no game, trace length or system is named on slide 12 or anywhere in the characterization section (slides 10–17). The slide-13 chart of one game plots only ~128 tasks, fewer than 300; the slide does not explain the difference (it may plot a subset or a different game — not stated).
(d) PARTIAL — count found; which game(s) and system: not stated anywhere in the deck (searched text layer for game titles, "Steam", "Deck", "kernel", "core", "CPU"; viewed all 30 slides).

### C-lavd-2 — share of long-lived vs short-lived tasks; definition of long-lived
(a) Text layer, slide 12: "○ Around 90% are long-living tasks; only 10% of tasks are terminated."
(b) Slide 12, sub-bullet under "Around 300 tasks".
(c) Unit: share of the ~300 scheduled tasks. Statistic: approximate percentages ("Around 90%", "10%"). The term used is "long-living", not "long-lived". No explicit definition: the only operationalisation is the contrast with "terminated" tasks, i.e. the reading is that a long-living task is one not terminated (during the observation); observation window length not stated. No "short-lived" term appears.
(d) PARTIAL — shares found; "long-living" is not explicitly defined (only implied by "only 10% of tasks are terminated").

### C-lavd-3 — non-game server processes among scheduled tasks and their share of scheduling
(a) Text layer, slide 12: "● Top 30-40 most frequently scheduled tasks take 95% of scheduling." / "○ Around half of them are system tasks -- especially, wine, " / "graphics, and audio servers , taking 30--40% of scheduling." (rendered slide shows "audio servers, taking 30--40% of scheduling."; `wine`, `graphics`, `audio servers` set in monospace.)
Process names visible in trace figures [image]: slide 16 graph: `swapper[0/0]`, `SteamControlle[4908/4788]` (left edge cut), `winedevice.exe[7284/7273]`, `pipewire-pulse[1707/1703]`, `pipewire-pulse[1703/0]`, `pipewire[1214/1204]`; slide 11 and slide 15: `wineserver[5789/0]`, `wineserver[3845/0]`; slide 15: `CrBrowserMain[4336/4221]`.
(b) Slide 12 bullet 2 and sub-bullet 1; slides 11, 15, 16 figures.
(c) Named categories: "wine, graphics, and audio servers" (called "system tasks"); they are "Around half" of the top 30–40 most-frequently-scheduled tasks and take "30--40% of scheduling" (approximate range). How "share of scheduling" is measured is not defined on any slide; "most frequently scheduled" suggests ranking by number of times scheduled, and slide 11 shows a per-task `num_sched` statistic [image], but the slides do not state that the percentages are shares of scheduling events. The slide also does not say whether 30–40% is a share of all scheduling or of the top set's 95%.
(d) PARTIAL — processes and share found; the measure behind "share of scheduling" is not stated.

### C-lavd-4 — wine/wineserver, graphics, audio linked with game tasks in waker/wakee graphs
(a) Text layer, slide 16 (title "Tasks are tightly linked in a graph"): "● Task graphs of top 50 percentile of waiter-wakers".
Slide 16 graph [image], edges as drawn (arrow tail → head, label):
- `swapper[0/0]` → `SteamControlle[4908/4788]` "sleep (10683)"; `swapper[0/0]` → `winedevice.exe[7284/7273]` "sleep (18441)"
- `Task worker thr[7826/7781]` → `winedevice.exe[7284/7273]` "sleep (9283)"
- `Task worker thr[7826/7781]` → `dxvk-cs[7922/7781]` "futex_wait (10438)"; `Task worker thr[7828/7781]` → `dxvk-cs` "futex_wait (9404)"; `Task worker thr[7827/7781]` → `dxvk-cs` "futex_wait (10354)"; `Task worker thr[7825/7781]` → `dxvk-cs` "futex_wait (10202)"
- `dxvk-cs[7922/7781]` → `dxvk-submit[7920/7781]` "futex_wait (30970)"
- `winepulse_timer[7993/7781]` → `winepulse_mainl[7991/7781]` "poll (20102)"; `winepulse_mainl` → `winepulse_timer` "futex_wait (10145)"
- `winepulse_mainl[7991/7781]` → `pipewire-pulse[1703/0]` "epoll (22574)"; `pipewire-pulse[1703/0]` → `winepulse_mainl` "poll (17091)"
- `pipewire-pulse[1707/1703]` → `pipewire-pulse[1703/0]` "epoll (18959)"; `pipewire-pulse[1707/1703]` → `pipewire[1214/1204]` "epoll (19090)"; `pipewire[1214/1204]` → `pipewire-pulse[1707/1703]` "epoll (19283)"
- `winepulse_timer[7993/7781]` → `FAudio_AudioCli[7992/7781]` "futex_wait (10213)"
Slide 24 [image] repeats the audio sub-graph (winepulse_mainl, winepulse_timer, pipewire-pulse ×2, pipewire, FAudio_AudioCli) with the same labels.
Slide 11 [image], panel headed "- 30.00 percentile of waker-waiter": `redDispatcher3[6347/6340]` → `wineserver[5789/0]` "epoll (109665)"; `redDispatcher7[6351/6340]` → wineserver "epoll (107855)"; `redDispatcher6[6350/6340]` → wineserver "epoll (105654)"; paired edges between wineserver and each of `wine_xinput_hid[6597/6340]` ("pipe_read (183350)", "epoll (121662)"), `redDispatcher5[6349/6340]` ("pipe_read (89991)", "epoll (114748)"), `redDispatcher1[6345/6340]` ("pipe_read (91195)", "epoll (114702)"), `redDispatcher4[6348/6340]` ("pipe_read (86311)", "epoll (110452)"), `redDispatcher2[6346/6340]` ("pipe_read (85900)", "epoll (110359)"); in each pair the pipe_read arrow points from wineserver to the task and the epoll arrow from the task to wineserver.
(b) Slide 16 (full graph), slide 24 (audio sub-graph), slide 11 bottom-right panel (wineserver hub).
(c) The graphs show wine components (`winedevice.exe`, `winepulse_mainl`, `winepulse_timer`, `wine_xinput_hid`, `wineserver`), DXVK graphics threads (`dxvk-cs`, `dxvk-submit`; slide 4 lists DXVK as part of Proton) and audio servers (`pipewire`, `pipewire-pulse`, `FAudio_AudioCli`) connected by edges to `Task worker thr` threads. Several of these share group ID 7781 with the Task worker threads. The slides do not label which nodes are "game tasks", do not explain arrow direction (the bullet says "waiter-wakers", the slide-11 panel says "waker-waiter"), and do not explain the numbers in parentheses (reads as a count per edge, but not stated). "top 50 percentile" / "30.00 percentile" are the only selection criteria given.
(d) FOUND — wine (incl. wineserver on slide 11), graphics (dxvk) and audio components shown linked to other tasks at slides 11, 16, 24; "game task" labelling is not given.

### C-lavd-5 — per-schedule runtime figures for game-related tasks
(a) Text layer, slide 13 ("Task execution time per schedule"): "● In general, tasks run for very short duration – roughly a few 100s usec " / "on average to a few msec maximum." ; "○ Some coordination tasks run very " / "shortly (e.g., wineserver:260 usec) but " / "some work tasks (e.g., a task worker: " / "1.65 msec) run longer than average." ; figure caption "Distribution of task’s runtime " / "average per schedule in a game", axis labels "tasks", "runtime avg (msec)", overlay "< 1 msec".
Figure [image]: sorted curve of per-task runtime average over ~128 tasks; y-axis 0.0–1.4 msec; shaded band up to 1.0 msec labelled "< 1 msec"; curve stays under ~0.1 msec to about task 100, rises past 0.4 near task 122, and only the last few tasks exceed 1.0 msec, topping out near 1.4 msec (read from the plot, approximate).
(b) Slide 13, bullets 1–2 and figure.
(c) Named tasks: `wineserver` 260 usec; "a task worker" 1.65 msec. The slide does not label the statistic for these two numbers; the surrounding sentence ("predictable using its average", "longer than average") and the chart ("runtime avg") suggest per-task averages, but that is not stated for the two examples. General range: "a few 100s usec on average" (average) to "a few msec maximum" (maximum). Population: tasks while running a game (game unnamed). Caveat: the 1.65 msec example exceeds the plotted maximum (~1.4 msec), so the example and the chart are probably not the same trace (not stated).
(d) PARTIAL — tasks and values found; the statistic for the two named values is not explicitly stated; no percentiles given.

### C-lavd-6 — runtime per schedule consistent over time
(a) Text layer, slide 13: "● Task execution time is very stable and is predictable using its average. "
Text layer, slide 17: "● Majority of game tasks shows periodic behavior" / "○ given the fact that a task has a stable execution time and a stable " / "wait time."
Text layer, slide 15: "property. Each task’s wait time is pretty constant. " (preceded by "● Wait time from one schedule to another schedule is a task’s behavioral "); caption "Wait times over time in a game ".
(b) Slides 13, 15, 17.
(c) Terms used for execution time: "very stable", "predictable using its average", "stable execution time". "Over time" phrasing is used only for wait time (slide 15 plots of `wait_time.ts` against sample index for wineserver[3845/0], three "Umask: 0022" tasks, dxvk-cs[4876/4727], CrBrowserMain[4336/4221] [image]; wait-time units not stated). Slide 11 [image] also shows per-task runtime traces over time for redDispatcher5/1/2 but without commentary. Qualitative only; no variance statistic given.
(d) FOUND.

### C-lavd-7 — what causes scheduling events; shares; named system calls
(a) Text layer, slide 14 ("What makes scheduling happen?"): "● Preemption (e.g., timer interrupt) takes only 25-30% of scheduling." ; "● 70-75% of scheduling is initiated by waiting system calls – such as " / "epoll, pipe_read, futex_wait , etc." ; "● In this case, a task is ﬁrst scheduled out waiting for an event then it is " / "scheduled in when the event is notiﬁed." ; caption "Call stacks which triggered " / "scheduling in a game ".
Pie chart [image] (same chart appears on slide 11 headed "Callstacks tiggered scheduling"): sched_preempt (28.78%), ioctl (13.25%), alloc (7.95%), unlock (7.28%), syscall (6.76%), futex_wait (5.94%), fs_write (4.11%), lock (3.96%), fs_read (3.83%), pipe_write (3.69%), pipe_read (2.96%), futex_wake (2.23%), page_fault (1.57%), recvmsg (1.36%), poll (1.26%), futex (1.05%), blk_mq:bio (0.62%), mmap (0.50%), a label rendered "sehdmsg (0.48%)" (overlapping text, likely sendmsg), mprotect (0.34%), epoll (0.34%, partly obscured), yield (0.2x%, partly obscured); remaining small slices have overlapping, illegible labels.
(b) Slide 14 bullets and pie chart; slide 11 right panel.
(c) Unit: share of scheduling events, classified by the call stack that triggered them. Statistic: approximate ranges in text (25–30% preemption, 70–75% waiting system calls); pie gives exact percentages for one game (unnamed). Named system calls in text: epoll, pipe_read, futex_wait. The pie's single "sched_preempt" slice (28.78%) matches the preemption range; the text does not say which pie categories make up the 70–75%.
(d) FOUND.

### C-lavd-8 — how game tasks wake one another; structure, shape, stages between input and output
(a) Text layer, slide 16 title/bullet: "Tasks are tightly linked in a graph" / "● Task graphs of top 50 percentile of waiter-wakers".
Text layer, slide 17: "● A sequence of tasks serves for a single job (e.g., from a user input to " / "display update)." ; "● Therefore, the accumulated scheduling delay in a task chain will affect ".
Text layer, slide 24: "● Suppose there are three tasks, Task A, B, and C, coordinated by any waiting " / "calls (e.g., epoll, futex, etc)." / "○  [Task A] --> [Task B] --> [Task C]".
Graph shapes [image]: see C-lavd-4 — slide 16 has a fan-in (four `Task worker thr` → `dxvk-cs`) followed by a chain (`dxvk-cs` → `dxvk-submit`), bidirectional pairs/cycles among winepulse_mainl, winepulse_timer, pipewire-pulse, pipewire, and a chain winepulse_timer → FAudio_AudioCli; slide 11 has a hub-and-spoke around `wineserver`.
(b) Slides 11, 16, 17, 24.
(c) The deck describes the structure as a graph ("tightly linked in a graph"), a "sequence of tasks" / "task chain" serving one job, and the abstract three-task chain A → B → C coordinated by waiting calls. The only endpoints named are "a user input" and "display update"; no intermediate stages between input and output are named. The drawn graphs use thread names, not stage names.
(d) PARTIAL — structure and shapes found; PREMISE NOT IN SOURCE for named stages between input and output (the source names only the two endpoints, as an "e.g.").

### C-lavd-9 — frame time budget and targeted latency; corresponding frame rate
(a) Text layer, slide 27 ("Task’s time slice"): "● The LAVD scheduler tries to schedule all runnable tasks at least once " / "within a predeﬁned time window, which is called a targeted latency (e.g., " / "15 msec)." ; "● The scheduler proportionally divides the targeted latency as per task’s nice " / "priority (i.e., weight)."
Slide 29 [image], EEVDF screenshot, overlay at top-left: "100%", "60FPS", "16.5ms", "min: 5.5ms, max: 43.4ms" (overlay's own labels cut off at the left edge); both screenshots list "Refresh Rate: 60".
(b) Slide 27; slide 29 lower screenshot.
(c) "Targeted latency" is a scheduler time window used to size time slices, given only as an example value ("e.g., 15 msec"); the slide does not tie it to games, frames or a frame rate. No "frame time budget" is stated anywhere in the text, and no slide relates 15 msec (or any value) to 60 FPS or another frame rate. The 16.5 ms / 60 FPS figures are uncommented readouts inside a screenshot.
Context from scx at 8b24795 (not the talk): the main.bpf.c header comment still uses the 15 msec example (scheds/rust/scx_lavd/src/bpf/main.bpf.c:69–72: "The LAVD scheduler tries to schedule all the runnable tasks at / least once within a predefined time window, which is called a targeted / latency. For example, if a targeted latency is 15 msec and 10 tasks are / runnable, the scheduler equally divides 15 msec of CPU time into 10 tasks."), but the code constant is `LAVD_TARGETED_LATENCY_NS	= (10ULL * NSEC_PER_MSEC),` (scheds/rust/scx_lavd/src/bpf/lavd.bpf.h:73), used in `calc_sys_time_slice` as `slice_wall = (LAVD_TARGETED_LATENCY_NS * sys_stat.nr_active) / nr_q;` then clamped to [slice_min_ns, slice_max_ns] (src/bpf/sys_stat.bpf.c:767–768). At the commit that added scx_lavd (6ab3928, 2024-03-16) the constant was `LAVD_TARGETED_LATENCY_NS	= (15 * NSEC_PER_MSEC),` (src/bpf/intf.h:55 at that commit).
(d) PREMISE NOT IN SOURCE — no frame time budget or frame-rate correspondence is stated; the source has instead a scheduler "targeted latency (e.g., 15 msec)" and an uncommented 60 FPS / 16.5 ms HUD readout in one screenshot.

### C-lavd-10 — concentration of scheduling across tasks; how share is measured
(a) Text layer, slide 12: "● Top 30-40 most frequently scheduled tasks take 95% of scheduling."
(b) Slide 12, bullet 2.
(c) Of ~300 tasks, the top 30–40 (ranked by how frequently they are scheduled) take 95% of "scheduling". Statistic: range for the task count, single figure for the share. Measurement of "share of scheduling" is not defined (plausibly share of scheduling events, but not stated). Game/system unnamed.
(d) PARTIAL — concentration found; the measure is not stated.

### C-lavd-11 — game (vs non-game) tasks dominating scheduling; combined share; frame-critical/pipeline
(a) Text layer, slide 12: "○ There are 15-20 game-speciﬁc tasks, which takes 60-70% " / "scheduling."
Text layer, slide 17: "● A sequence of tasks serves for a single job (e.g., from a user input to " / "display update)."
(b) Slide 12, second sub-bullet under "Top 30-40"; slide 17.
(c) 15–20 "game-specific" tasks within the top 30–40 take 60–70% of scheduling (ranges). The slide does not say whether 60–70% (and the system tasks' 30–40%) is a share of all scheduling or of the top set's 95%. Slide 12 does not call these tasks "frame-critical" or a "pipeline"; neither word occurs anywhere in the deck (text-layer search for "frame-critical", "critical", "pipeline"). The nearest description is slide 17's generic "sequence of tasks" / "task chain" for game tasks, not tied to the 15–20 set; slides 22–26 use "latency-critical"/"latency criticality" for the scheduler's per-task metric.
(d) PARTIAL — count and share found; not described as frame-critical or as a pipeline.

### C-lavd-12 — activity of tasks outside the dominant set
(a) No passage. Closest text (slide 12): "● Top 30-40 most frequently scheduled tasks take 95% of scheduling."
(b) —
(c) Arithmetic implication only (not stated): the remaining ~260–270 tasks account for the other ~5%. No slide describes them as idle, waiting, sleeping, periodic or otherwise. The words "idle" appear only inside slide 11 images ("System-wide task and idle statistics", "sw_idle_stat" [image]) about system-wide idle statistics, not about non-dominant tasks.
(d) NOT FOUND — searched text layer for "idle", "wait", "sleep", "rest", "remaining", "other", "background", "inactive"; viewed all 30 slides.

### C-lavd-13 — CPU utilization during gaming
(a) Text layer, slide 12: "● CPU utilization is moderately high -- around 65-95%, but not " / "overloaded (i.e., no 100%)."
(b) Slide 12, last bullet.
(c) Unit: CPU utilization percent. Statistic: approximate range ("around 65-95%"), with the note that it never reaches 100%. Scope: while running a game; whether system-wide or per-core, the averaging window, game and hardware are not stated. (Slide 29 EEVDF overlay shows an unlabeled "100%" [image]; its label is cut off, so it cannot be identified as CPU utilization.)
(d) FOUND.

### C-lavd-14 — relation of frame-rate metrics to scheduler performance metrics
(a) Text layer, slide 7: "○ Throughput: how much job can be done in a given time" / "○ Latency: time to process a task" / "○ Tail latency (99p, 99.9p): latency of the worst 1% or 0.1%".
Text layer, slide 8: "● In games, FPS (frame per second) or frame time are the widely used " / "metric" / "○ Average FPS   ≈ throughput of FPS" / "○ Low 1% FPS    ≈ 99p latency of FPS" / "○ Low 0.1% FPS ≈ 99.9p latency of FPS" / "● Not only average FPS but also low 1% FPS are critical in user " / "experience. A sudden FPS dip is also known as a stuttering problem. "
Text layer, slide 17: "● Therefore, the accumulated scheduling delay in a task chain will affect " / "end-user’s experience; it would eventually result in a sudden spike of " / "frame time (low 1% FPS)."
Slide 6 [image + text layer]: "Scheduler A" "Avg FPS: 41.3" "Low 1% FPS: 29.5"; "Scheduler B" "Avg FPS: 34.2" "Low 1% FPS: 4.6"; FPS-vs-frames plots (schedulers, game unnamed).
Slide 29 text layer: "● In many cases, LAVD provides better or similar performance than EEVDF in " / "terms of average FPS and Low 1% FPS"; screenshots [image]: LAVD "Minimum FPS: 32", "Average FPS: 40", "Maximum FPS: 52", "Frames rendered: 2635"; EEVDF "Minimum FPS: 25", "Average FPS: 33", "Maximum FPS: 47", "Frames rendered: 2176"; both "Resolution: 1280 x 800", "V-Sync: OFF", "Framerate Lock: OFF", "Refresh Rate: 60", "Graphics Quality: High"; caption "6.9-rc1 upstream kernel".
(b) Slides 6, 7, 8, 17, 29.
(c) Mapping stated as approximations (≈): average FPS ↔ throughput; low 1% FPS ↔ 99th-percentile latency; low 0.1% FPS ↔ 99.9th-percentile latency. Causal link stated on slide 17: accumulated scheduling delay in a task chain → frame-time spike (low 1% FPS). Caveat: slide 29's claim mentions Low 1% FPS but the screenshots show min/avg/max FPS, not a low-1% value; the benchmark/game is not named.
(d) FOUND.

### C-lavd-15 — hardware (core count) and system for the gaming observations
(a) No passage stating the measurement hardware for the characterization. Adjacent text layer, slide 4: "SteamDeck runs x86 Windows games!" / "● AMD APU" / "○ AMD Van Gogh: x86 8-core CPU + AMD GPU" / "● SteamOS" / "○ Arch-Linux based Linux distribution" / "● Proton" / "○ Compatibility layer for Windows games on Linux" / "○ Includes patched version of Wine". Slide 29 text layer: "6.9-rc1 " / "upstream kernel". Schedule-page abstract (sched-event-1aBOT.txt line 41, 1-based): "Suboptimal task scheduling can cause stuttering while playing games on the Steam Deck game console."
(b) Slide 4 (background on Steam Deck), slide 29 (kernel for the LAVD-vs-EEVDF screenshots), schedule page abstract.
(c) Slide 4 describes Steam Deck hardware as motivation ("8-core"), but no slide states that the traces on slides 11–16 or the numbers on slides 12–14 were collected on a Steam Deck or on any particular machine, core count, OS or kernel. "6.9-rc1 upstream kernel" labels only the slide-29 benchmark comparison.
(d) NOT FOUND — searched text layer for "core", "CPU", "Steam", "Deck", "kernel", "machine", "hardware", "system"; viewed all slides including trace images.

### C-lavd-16 — non-game applications (chat/voice/overlay) running during gaming
(a) No text passage. Images only: slide 15 plot headed "CrBrowserMain[4336/4221]" among "Wait times over time in a game" [image]; slide 16 node "SteamControlle[4908/4788]" [image]; slide 29 EEVDF screenshot shows an on-screen performance overlay with "60FPS", "16.5ms", "min: 5.5ms, max: 43.4ms" [image].
(b) Slides 15, 16, 29 (images).
(c) The deck never mentions chat, voice, Discord, browsers, overlays or other applications running alongside the game. Trace images include thread names that are not game threads by name (CrBrowserMain, SteamControlle…), but the slides do not say what application they belong to. A frame-time HUD is visible in one benchmark screenshot but is not named or discussed.
(d) PARTIAL — no mention of chat/voice/overlay apps; only unexplained non-game thread names and an unnamed HUD appear in images. (Text-layer search terms: "chat", "voice", "Discord", "overlay", "browser", "background", "Steam".)

### C-lavd-17 — characterization of task durations; latency outliers vs user-perceived frame problems
(a) Text layer, slide 13: "● In general, tasks run for very short duration – roughly a few 100s usec " / "on average to a few msec maximum."
Text layer, slide 7: "○ Tail latency (99p, 99.9p): latency of the worst 1% or 0.1%".
Text layer, slide 8: "● Not only average FPS but also low 1% FPS are critical in user " / "experience. A sudden FPS dip is also known as a stuttering problem. "
Text layer, slide 17: "● Therefore, the accumulated scheduling delay in a task chain will affect " / "end-user’s experience; it would eventually result in a sudden spike of " / "frame time (low 1% FPS)."
(b) Slides 7, 8, 13, 17.
(c) Durations: "very short", a few hundred µs average up to a few ms maximum per schedule (see C-lavd-5 for the chart). Outliers: tail latency is defined as the worst 1%/0.1%; low 1% FPS ≈ 99p latency of FPS; a sudden FPS dip = "stuttering"; accumulated scheduling delay along a task chain is said to eventually cause frame-time spikes (low 1% FPS). The link is stated qualitatively; no measured delay-to-frame-time data is shown.
(d) FOUND.

### C-lavd-18 — organizations stated to ship or deploy LAVD, and setting
(a) Talk: no passage. Slides show only the speaker's affiliation (slide 1 "changwoo@igalia.com" and Igalia logo; slide 30 "Join us!" with Igalia logo [image]). Schedule page (sched-event-1aBOT.txt lines 36, 44, 41; 1-based): "Optimizing Scheduler for Linux Gaming - Changwoo Min, Igalia"; "Kernel engineer, Igalia"; the abstract says "Lastly, we will share our progress on the optimized scheduler for reducing the stuttering problems in Linux gaming, especially Steam Deck."
Cross-source (for the verifier, other entries in this input):
- corbet-lwn24, lwn-991205.html lines 121–125: "One of those appears to be scx_lavd (about which more was heard later), which is headed for shipment in Steam Deck gaming systems." (markup removed: `<tt>`, link to store.steampowered.com/steamdeck). Also lines 131–133: "Support for sched_ext is now shipping in a number of distributions, including CachyOS, Arch Linux, Ubuntu, Fedora, Nix, and openSUSE." (about sched_ext support, not scx_lavd specifically).
- scx @ 8b24795: scx_lavd source files carry copyright notices, e.g. scheds/rust/scx_lavd/src/bpf/main.bpf.c:180 " * Copyright (c) 2023, 2024 Valve Corporation." and src/main.rs:3 "// Copyright (c) 2024 Valve Corporation."; Cargo.toml:4 `authors = ["Changwoo Min <changwoo@igalia.com>", "Igalia"]`. These are copyright/authorship lines, not shipping or deployment statements. Repo-wide search found no "Steam Deck"/"SteamOS" deployment statement for scx_lavd.
(b) As listed.
(c) The talk states no organization that ships or deploys LAVD; it presents LAVD as work in progress ("Early result is promising", slide 29). The LWN article (Sept 2024) says scx_lavd is "headed for shipment in Steam Deck gaming systems" without naming the shipping organization.
(d) NOT FOUND (in the talk slides and schedule page; searched for "ship", "deploy", "Valve", "Steam", "production"). See cross-source notes above.

### C-lavd-19 — workload description format provided by the talk or the scheduler
(a) No passage in the talk. scx_lavd README (scheds/rust/scx_lavd/README.md:20–23): "`scx_lavd` is initially motivated by gaming workloads. It aims to improve / interactivity and reduce stuttering while playing games on Linux. Hence, this / scheduler's typical use case involves highly interactive applications, such as / gaming, which requires high throughput and low tail latencies."
(b) Slides 1–30; schedule page; scx @ 8b24795: scheds/rust/scx_lavd/README.md, Cargo.toml, src/main.rs (clap options at lines 81–301).
(c) The talk shows analysis outputs (plots, graphs) but no format for describing a workload. The scheduler's inputs are command-line options (e.g. `--autopilot`, `--performance`, `--powersave`, `--balanced`, `--slice-max-us` default "5000", `--slice-min-us` default "500", `--cpu-pref-order`, `--no-futex-boost`, `--stats`, `--monitor`, `--monitor-sched-samples`; src/main.rs:90–270) and it emits statistics/sampled scheduling decisions; it reads no workload description file. It observes live tasks (e.g. attaches futex ftrace/tracepoints, src/main.rs:487–492).
(d) NOT FOUND — searched slide text for "format", "trace", "workload", "json", "yaml"; searched scheds/rust/scx_lavd for "workload", "trace", "json", "yaml" (only matches: README/comment mentions of "gaming workloads", "spiky workloads", and tracing attachments).

### C-lavd-20 — speaker, title, event, date, slide URL
(a) Text layer, slide 1: "Optimizing Scheduler for Linux Gaming" / "Changwoo Min" / "changwoo@igalia.com" / "April 17, 2024". Footer on slides 2–29: "Optimizing Scheduler for Linux Gaming" / "Changwoo Min, April 17, 2024". PDF metadata: `/Title: scx-lavd-oss-na24`, `/Creator: Google`.
Schedule page (sched-event-1aBOT.txt, 1-based lines): line 1 "Open Source Summit North America 2024: Optimizing Scheduler for Linux Gaming -..."; lines 7–8 "April 16-18, 2024" / "Seattle, Washington"; lines 36–39 "Optimizing Scheduler for Linux Gaming - Changwoo Min, Igalia" / "Wednesday April 17, 2024  2:55pm -  3:35pm" / "PDT" / "345-346 (Level 3)"; lines 52–56 "LinuxCon" / "Content Experience Level" / "Intermediate" / "Session Slides Attached" / "Yes"; attachment link in HTML `href="https://hosted-files.sched.co/ossna2024/9b/scx-lavd-oss-na24.pdf"` labelled "scx lavd oss na24" "pdf".
(b) Slide 1; schedule page.
(c) Speaker Changwoo Min (Igalia); title "Optimizing Scheduler for Linux Gaming"; event Open Source Summit North America 2024, Seattle, Washington (the event name appears only on the schedule page, not on the slides); date Wednesday 17 April 2024, 2:55–3:35 pm PDT, room 345-346 (Level 3), track "LinuxCon". Slide URL: the schedule page links hosted-files.sched.co/ossna2024/9b/scx-lavd-oss-na24.pdf; the cited static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf serves a byte-identical file.
(d) FOUND.

---

## corbet-lwn24

### C-corbet-1 — date, conference year, scx_lavd section and its gaming characterization
(a) lwn-991205.html line 56: "Sched_ext at LPC 2024"; line 60: "By Jonathan Corbet" / "September 26, 2024"; lines 68–70: "At the 2024 Linux Plumbers Conference, the growing sched_ext community held one of its first public gatherings".
Section heading line 186: "Higher frame rates". Lines 188–191: "Changwoo Min took over via a remote link to talk about scx_lavd, which is a "latency criticality aware virtual deadline" scheduler aimed at gaming applications."
Lines 194–199: "The goal behind this scheduler was to provide the best gaming experience on Linux in general — not just on the Steam Deck. That requires getting high performance (and high video frame rates) without stuttering (short-term performance loss due to load in the system). The scheduler should deliver reasonable performance across a wide range of CPU configurations, but it is not intended to be the best server or general-purpose scheduler."
Lines 201–209: "A key aspect of gaming workloads is that tasks tend to run quickly, typically no more than 100µs at a time. There are a lot of tightly linked tasks, though, and performance depends on the most critical of those tasks running in the necessary sequence; that is the critical path. Every task has a latency criticality that is determined by its place in this path; tasks that wait on others, and are waited on in turn, have a large impact on overall performance and are thus "latency critical". Detecting these tasks requires observing which tasks wait for which others, and ensuring that the tasks being waited for are run with low latency."
Lines 233–235: "Min concluded by saying that, for gaming applications, scx_lavd consistently enables higher frame rates than the EEVDF scheduler while using (slightly) less power and with fewer stutters."
Also lines 97–99 (overview section): "The scx_lavd scheduler, for example, is focused on interactivity and, specifically, consistently getting higher frame rates out of games."
(Markup such as `<tt>` and line breaks removed; words unchanged.)
(b) lwn-991205.html lines as given; section "Higher frame rates".
(c) Dated 2024-09-26; covers the sched_ext microconference at the 2024 Linux Plumbers Conference (a different talk from OSS NA, April 2024, given remotely). It has a dedicated scx_lavd section ("Higher frame rates"). Gaming characterization: tasks run quickly, "typically no more than 100µs at a time" (reporter's paraphrase of the talk; note this differs in wording from the OSS NA slide 13 "a few 100s usec on average to a few msec maximum"); many tightly linked tasks; a critical path; latency criticality from waiting/being-waited-on. No task counts, shares or CPU utilization figures are given.
(d) FOUND.

### C-corbet-2 — article exists, date, author
(a) lwn-991205.html line 3: "<title>Sched_ext at LPC 2024 [LWN.net]</title>"; line 60: "By <b>Jonathan Corbet</b><br>September 26, 2024</br>".
(b) lwn-991205.html lines 3, 56, 60.
(c) Exists at lwn.net/Articles/991205/ (HTTP 200, 2026-09-13); author Jonathan Corbet; date September 26, 2024. Footer line 380: "Copyright &copy; 2024, Eklektix, Inc."
(d) FOUND.

---

## scx

### C-scx-1 — scx_lavd in sched-ext/scx; repository license
(a) Directory `scheds/rust/scx_lavd/` exists at commit 8b2479571c0768310510c061960d2c40cb64d160; scheds/rust/README.md:22 "- [scx_lavd](scx_lavd/README.md)".
LICENSE:1–2: "                    GNU GENERAL PUBLIC LICENSE" / "                       Version 2, June 1991".
scheds/rust/scx_lavd/Cargo.toml:8: `license = "GPL-2.0-only"`; scheds/rust/scx_lavd/LICENSE is a symlink to `../../../LICENSE`.
scheds/rust/scx_lavd/src/bpf/main.bpf.c:1: "/* SPDX-License-Identifier: GPL-2.0 */"; line 197: `char _license[] SEC("license") = "GPL";`.
scheds/rust/scx_lavd/src/bpf/main.bpf.c:3–9: " * scx_lavd: Latency-criticality Aware Virtual Deadline (LAVD) scheduler" … " * LAVD is a new scheduling algorithm which is still under development. It is" / " * motivated by gaming workloads, which are latency-critical and" / " * communication-heavy."
Added by commit 6ab3928a0d5b7ffc52c69ddf4665d8753f2350ec (2024-03-16T10:31:07+09:00) "scx_lavd: add scx_lavd (Latency-criticality Aware Virtual Deadline) scheduler"; Cargo.toml at that commit line 7: `license = "GPL-2.0-only"`.
GitHub API (api.github.com/repos/sched-ext/scx, 2026-09-13): `license: {'key': 'gpl-2.0', 'name': 'GNU General Public License v2.0', 'spdx_id': 'GPL-2.0'}`, default branch `main`, not archived.
(b) As listed, at commit 8b24795 unless noted.
(c) scx_lavd lives in sched-ext/scx under scheds/rust/scx_lavd (Rust userspace part + BPF part). Repository license file is GPL version 2; scx_lavd declares GPL-2.0-only. Caveat: per-file SPDX tags across the repo are mostly GPL-2.0 / GPL-2.0-only, but a few files are dual-licensed — `git grep` counts: GPL-2.0 (153), GPL-2.0-only (17), "(GPL-2.0-only OR BSD-2-Clause)" (4), "(LGPL-2.1 OR BSD-2-Clause)" (2).
(d) FOUND.

---

## Verdict counts

- FOUND: 10 (C-lavd-4, 6, 7, 13, 14, 17, 20; C-corbet-1, C-corbet-2; C-scx-1)
- PARTIAL: 8 (C-lavd-1, 2, 3, 5, 8, 10, 11, 16) — C-lavd-8 includes a premise-not-in-source component (no named intermediate stages)
- NOT FOUND: 4 (C-lavd-12, 15, 18, 19)
- PREMISE NOT IN SOURCE: 1 (C-lavd-9)
- COPY UNREACHABLE: 0
