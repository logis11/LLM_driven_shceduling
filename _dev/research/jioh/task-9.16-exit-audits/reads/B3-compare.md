# 9.16 blind reader B3 — Phase 2 comparison

Reader B3, task 9.16 (the Phase 9 exit audits). Compares the repository's wording at `928aa8fd` (and, for the extra topics, the `docs/references.md` entries' quoted passages) with the passages recorded blind in `reads/B3-reads.md` (Phase 1, finished before this file was started and not edited since). Claims are those `claims/dataset-inventory.md` lists for dataset source groups 33 to 47, and those `claims/dataset-findings.md` (finding F-RBS-1, passages held only in the citation index, and the other record-below-standard findings) and `claims/outside-inventory.md` name for the 14 extra sources. Verdicts: SUPPORTED, WORDING-FIX, CONTRADICTED, NOT IN SOURCE, UNVERIFIABLE (the source, or the passage the wording rests on, was not reachable or not read).

"Phase 1 §…" points to the section of `B3-reads.md` (A33–A47 for the dataset groups, B1–B14 for the extra sources). A few checks made only in this phase are marked "(Phase 2 check)" with their copy.

**Locator corrections to Phase 1** (found while comparing; Phase 1 is left as written): the SYSmark 25 User Guide's application list is on PDF page 31 and the Productivity description with "software development (code compilation)" on page 32 (Phase 1 §A40 said 30 and 31); the SYSmark 30 User Guide's application list is on page 34 and its scenario descriptions on page 35 (Phase 1 said 33 and 33–34). Page footers in the extracted text precede the page's content in those two files.

## Summary

### Claims of dataset source groups 33 to 47 and of the extra sources (51)

| claim | subject | verdict |
|---|---|---|
| D-F3-35 | HandBrake 1.7.2's default preset and its settings | SUPPORTED |
| D-F3-36 | HandBrakeCLI as Ubuntu 24.04 packages it, with x264 and FFmpeg | SUPPORTED |
| D-F3-38 | CpsMark+'s HandBrake workload: H.264 to a 1080p "2K" | SUPPORTED |
| D-F3-39 | the CPSmarkPLUS repository has no licence file | SUPPORTED |
| D-F3-40 | the shaped link's 121.0 Mbps, a byte-weighted median of Steam's per-country rates | SUPPORTED |
| D-F3-42 | 7-Zip 23.01 is Ubuntu 24.04's `7z`, run at its default format and level | SUPPORTED |
| D-F3-44 | no distro or media server found starting an ML-training, render or transcode job unasked; the transcoders' process names | SUPPORTED |
| D-F4-34 | what Matt Mahoney's 10 GB set holds and where it came from | SUPPORTED |
| D-F4-01 | CpsMark+'s usage scenarios and the applications each runs | UNVERIFIABLE |
| D-F4-02 | CpsMark+'s archiving workload (WinRAR, mixed files) | UNVERIFIABLE |
| D-F4-04 | the stages of CpsMark+'s CA (light/middleweight module) cooperative workflow | UNVERIFIABLE |
| D-F4-05 | the order of CpsMark+'s CC (heavyweight module) workloads, no handoff | UNVERIFIABLE |
| D-F4-06 | CpsMark+'s graphics-card sensitivity per module (1.77×) | UNVERIFIABLE |
| D-F4-13 | the application PCMark 10's Writing workload runs | SUPPORTED |
| D-F4-14 | PCMark 10's guide times scripted tasks, not processes | SUPPORTED |
| D-F4-15 | where PCMark 10's video-playback test sits | WORDING-FIX |
| D-F4-18 | SYSmark 30's four scenarios and what each models | SUPPORTED |
| D-F4-19 | the applications SYSmark 30 names per scenario | SUPPORTED |
| D-F4-20 | SYSmark 30's archiving workload | SUPPORTED |
| D-F4-21 | SYSmark 30: photo editing beside a background encode; Outlook kept open | WORDING-FIX |
| D-F4-23 | SYSmark 25 includes code compilation, as a scenario description only | SUPPORTED |
| D-F4-24 | which SYSmark versions define Productivity, Creativity and Responsiveness | UNVERIFIABLE |
| D-F4-26 | how many benchmarks UL Procyon lists, and how many run AI inference on the device | WORDING-FIX |
| D-F4-27 | the applications behind Procyon's office, photo and video benchmarks | SUPPORTED |
| D-F4-29 | what Firefox's tab-count probe measures | SUPPORTED |
| D-F4-30 | GLAM's Linux median per-client peak of tabs (4.67) and windows (1), release 152 | SUPPORTED |
| D-F4-31 | whether Firefox's telemetry counts tabs per window | WORDING-FIX |
| D-F4-36 | PyTorch's Basic MNIST example: run command and defaults | SUPPORTED |
| D-F4-37 | Kdenlive 23.08.5's export processes and default render profile | SUPPORTED |
| D-F4-45 | whether Chromium on Linux marks a window covered by another application as occluded | CONTRADICTED |
| D-F4-43 | how long Chromium waits before throttling a background page's timer wake-ups | WORDING-FIX |
| D-F4-46 | how long an idle Matrix client's `/sync` request waits | WORDING-FIX |
| D-F4-40 | GNOME's default idle delay and what the session does then | SUPPORTED |
| D-F4-42 | whether the Ubuntu 24.04 GNOME 46 session at idle runs an X server | SUPPORTED |
| D-F5-21 | Ubuntu 24.04's desktop kernel transparent-hugepage default | SUPPORTED |
| D-F5-01 | Maricq et al.: servers "with supposedly identical parts" differ run to run | SUPPORTED |
| D-F5-02 | Maricq et al. recommend nonparametric median intervals unless normality is shown | SUPPORTED |
| D-F5-03 | Kalibera & Jones: repeat, and take the interval, at the highest level of variation | SUPPORTED |
| D-F5-04 | Kalibera & Jones: on-line count, minimum of five | SUPPORTED |
| D-F5-05 | Georges et al.: interval over independent runs, runs added until a set precision | SUPPORTED |
| D-F5-06 | the stopping rule's "No ceiling" row and its ground column | WORDING-FIX |
| D-F5-07 | a count-weighted mean's half-width is Cochran's ratio estimator | SUPPORTED |
| D-F5-08 | Cochran's ratio variance is a large-sample result | SUPPORTED |
| D-F5-09 | Chow & Robbins: first-crossing coverage, asymptotic, and the .929 bound | WORDING-FIX |
| D-F5-10 | the standard error of a compiled wake count from Feller's recurrent-event theorem | SUPPORTED |
| D-F5-14 | what RFC 8290 grounds for the download's `fq_codel` queue | WORDING-FIX |
| D-F5-15 | GitHub deletes a workflow's artifacts after 90 days | SUPPORTED |
| D-F4-33 | Glean's metrics-ping thread `glean.mps` wakes daily at 04:00 local | SUPPORTED |
| D-F4-39 | a stock Ubuntu 24.04 desktop does not run `systemd-networkd` | SUPPORTED |
| D-F3-11 | the kernel's Makefile passes no `-pipe` | SUPPORTED |
| F-54 (outside) | `sched_waking` fires only for a sleeping thread, before the scheduler takes it off the CPU | WORDING-FIX |

Counts: SUPPORTED 34, WORDING-FIX 10, CONTRADICTED 1, NOT IN SOURCE 0, UNVERIFIABLE 6.

### Outside-inventory rows on the same extra sources (14), short form at the end

E-42, E-43, E-44, E-45, E-46, E-47, E-54, F-11, F-56, F-58, F-59, F-60: SUPPORTED. F-55: WORDING-FIX at `docs/guidebook/dataset/06-grounding-measurement-verification.md:882` only (same issue as D-F5-06). F-57: UNVERIFIABLE for its "many VMs, many times" clause (§7.5 not read); its §2 clause SUPPORTED.

### The `docs/references.md` entries of the extra sources, quoted passages

`kalibera-ismm13`, `chow-aoms65`, `glean`, `systemd-ubuntu`, `gh-artifact-retention`, `fqcodel-rfc18`: every quoted passage matches the copy read. `georges-oopsla07`: WORDING-FIX ("a cap of about thirty runs"). `maricq-osdi18`: abstract and §2 match; §5 and §7.2/§7.5 quotes not read (UNVERIFIABLE). `cochran-st77`: §6.3, §6.5, §9A.1 (p. 250) and Theorem 6.1 (6.4) match; the §6.4 (p. 155) quotes were seen only in the scan's OCR layer. `feller-ipta50`: (4.5) on p. 248 matches; §12.2 (p. 242), the theorem and (4.8)–(4.9) on p. 249 not read (UNVERIFIABLE). `netplan`: the `generate.c` quotes match (`parse.c` not read); its copy can be pinned to commit 5cb27ab (= tag `import/1.1.2-8ubuntu1_24.04.3`). `livecd-rootfs`: the quoted passage matches; "nothing in the build applies systemd presets" not checked.

---

## Per claim — dataset source groups 33 to 47

### D-F3-35 — HandBrake 1.7.2's default preset and its settings
- Location: `dataset/archetypes.yaml:1625-1627`; `docs/workload/measurement-overview.md:52`; `docs/references.md:446`.
- Repo: "running its default preset unchanged, "Fast 1080p30" (x264 at fast, RF 22, profile main, level 4.0, AAC stereo at 160 kb/s, MP4)"; references: "Fast 1080p30", the preset HandBrake 1.7.2 marks as its default — x264 at fast, RF 22, 1920×1080 at most, MP4.
- Passage (Phase 1 §A33): `preset_builtin.json` at tag 1.7.2, l. 908 `"Default": true`, l. 956 `"PresetName": "Fast 1080p30"`, l. 971 `"VideoEncoder": "x264"`, l. 976 `"VideoPreset": "fast"`, l. 982 `"VideoQualitySlider": 22.0`, l. 978–979 `"main"` / `"4.0"`, l. 890–894 AAC 160 stereo, l. 909 `"mp4"`, l. 951–952 1920×1080. Same SHA-256 as the 9.10 record's copy (5fb29a61…).
- Verdict: SUPPORTED.
- Fix: none (the record's missing passage is the audit's finding; these lines can be copied into the 9.10 record S2-55).

### D-F3-36 — HandBrakeCLI as Ubuntu 24.04 packages it
- Location: `dataset/archetypes.yaml:1625-1626`; `docs/workload/scenario-catalog.md:19`.
- Repo: "HandBrakeCLI 1.7.2 as Ubuntu 24.04 packages it (`handbrake-cli` 1.7.2+ds1-1build2, x264 0.164.3108, FFmpeg 6.1.1)".
- Passage (Phase 1 §A33): `Package: handbrake-cli` / `Version: 1.7.2+ds1-1build2` / `Depends: … libavcodec60 (>= 7:6.1), … libx264-164 (>= 2:0.164.3108+git31e19f9)`; `libx264-164` `2:0.164.3108+git31e19f9-1`. (Phase 2 check, same `Packages-noble-universe`: `libavcodec60` `7:6.1.1-3ubuntu5`.)
- Verdict: SUPPORTED.
- Fix: none.

### D-F3-38 — CpsMark+'s HandBrake workload: H.264 to a 1080p "2K"
- Location: `dataset/archetypes.yaml:1629-1630`; `docs/workload/scenario-catalog.md:19`; `docs/workload/measurement-overview.md:52`; `docs/references.md:451, :456`.
- Repo: "CpsMark+'s HandBrake workload, its H.264 codec and its 1080p "2K" from the benchmark's own code, its clip and its preset's settings not"; catalog: "read from the benchmark's own code as H.264 to 1080p".
- Passage (Phase 1 §A33): `HandBrake.cpp` l. 6–9 preset names `fast_1080p_h264_sw`, `fast_1080p_h264_nvenc`, `fast_1080p_h264_vce`, `fast_1080p_qsv`; l. 39 input `tos_c2_4k_24fps_40mbps_8bit_h264_aac_10sec.mp4`; l. 114 `"Handbrake:4K->2K视频转码进行中..."`; DCI §4.3.1 (p. 31) "A 2K distribution – the resolution of the DCDM*[3] container is 2048x1080."
- Verdict: SUPPORTED (the codec and 1080p come from the preset names, the "2K" from the log line; DCI's 2K is 2048×1080, which the quotation marks and the `dci-dcss` entry make explicit).
- Fix: none.

### D-F3-39 — CPSmarkPLUS has no licence
- Location: `docs/workload/source-vetting.md:137`.
- Repo: "the GitHub repository has no licence file … The source is pinned at `bf24434`".
- Passage (Phase 1 §A33): at bf24434 no tracked licence or copying file; GitHub API `"license": null`; README holds only the title and the build environment.
- Verdict: SUPPORTED (the paper's open-source wording is outside this reader's reach; see D-F4-01).
- Fix: none.

### D-F3-40 — the shaped link's rate, 121.0 Mbps
- Location: `docs/workload/measurement-overview.md:52`; `dataset/archetypes.yaml:1411`; `docs/references.md:510-511`.
- Repo: "a link shaped to 121.0 Mbps, the byte-weighted median of Valve's per-country download rates (`steam-download-stats`)"; references: version `09-19-2026-04`, "most recent 7 days", 238 countries, the statistic the project's.
- Passage (Phase 1 §A34): page "Steam Global Traffic Map (most recent 7 days)", "Average Download Rate", per-country and per-network tables, data version in the URL (`v=10-17-2026-08` on the day read). (Phase 2 check, same country table: the byte-weighted median over 237 countries, sub-national rows excluded, is 118.0 Mbps on 2026-10-17.)
- Verdict: SUPPORTED (statistic, window and data version match the page's structure; the value is the 2026-09-19 week's, and the live page has moved on, as the entry says).
- Fix: none.

### D-F3-42 — 7-Zip 23.01 is Ubuntu 24.04's `7z`
- Location: `dataset/archetypes.yaml:1354-1355`.
- Repo: "7-Zip 23.01 (Ubuntu 24.04's `7zip`) at its default format and level with eight threads".
- Passage (Phase 1 §A36): `7zip` 23.01+dfsg-11 ships `/usr/bin/7z` → `/usr/lib/7zip/7z`; `p7zip-full` 16.02+transitional.1 only depends on `7zip`; `kDefaultArcType = "7z"`; `GetLevel()` returns 5 when unset.
- Verdict: SUPPORTED.
- Fix: none (optionally name the defaults: "7z format, level 5").

### D-F3-44 — no distro or vendor starts an ML-training, render or transcode job unasked; transcoder names
- Location: `dataset/timelines/coreset/c7.variant.yaml:67-70`.
- Repo: "No distro or vendor was found starting an ml-train, render or transcode job unasked (… Jellyfin runs its transcoder as plain `ffmpeg` and Plex as `Plex Transcoder`, neither found converting media on a schedule)".
- Passage (Phase 1 §A35): Jellyfin 12.0 "Generate Trickplay Images" daily at 03:00 and "Extract Chapter Images" daily at 02:00, both acting only on libraries where extraction is enabled (`EnableTrickplayImageExtraction`, `EnableChapterImageExtraction`, model default false); Plex video preview thumbnails "either only during your Scheduled Tasks maintenance or both during maintenance and when new content is added" once the user enables them (default not stated in the article); `/usr/lib/jellyfin-ffmpeg/ffmpeg`, `ffmpeg`; `./usr/lib/plexmediaserver/Plex Transcoder`.
- Verdict: SUPPORTED (no unasked conversion found; process names match). The scheduled frame-extraction jobs both servers can run once enabled are not "converting media", but they are scheduled video-decoding work.
- Fix: optional precision — "neither found converting media on a schedule (both extract preview frames on a schedule once the user enables it)".

### D-F4-34 — Matt Mahoney's 10 GB set
- Location: `docs/workload/measurement-overview.md:52`; `docs/references.md:426`.
- Repo: "Matt Mahoney's 10 GB benchmark set, 79,431 files from one laptop"; references: "exactly 10 GB (10^10) bytes in 79,431 files in 4006 directories from my Windows laptop collected from 2009 to 2013".
- Passage (Phase 1 §A37): identical sentence in "Test Data Description"; same page SHA-256 as 9.7's copy (72df2093…).
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-01, D-F4-02, D-F4-04, D-F4-05, D-F4-06 — CpsMark+ (the paper)
- Locations: D-F4-01 `docs/workload/scenario-catalog.md:12, :13, :15, :17, :33`, `dataset/sources.yaml:104-106`, `docs/workload/grounding-sources.md:17`, `docs/references.md:34`; D-F4-02 `docs/references.md:34`; D-F4-04 `dataset/sources.yaml:109-111`, `docs/workload/building-plan.md:133`, `dataset/timelines/coreset/c3-workday.timeline.yaml:2-3`; D-F4-05 `docs/workload/building-plan.md:135`; D-F4-06 `dataset/sources.yaml:112-115`, `docs/references.md:34`.
- Repo: scenarios document manipulation / Internet service / graphic design (with the Windows → Linux mappings); WinRAR "compresses and decompresses "mixed files in multiple formats" (Table 2, §4.3.4)"; CA workflow "Internet -> creation -> document processing -> email delivery"; CC "photo → video → transcode only as a subsequence, no handoff stated"; "the CC module's best graphics-card configuration performing 1.77 times its base configuration and the CA module showing no significant difference (sec-4.7.2)".
- Passage (Phase 1 §A38): full text unreachable (ScienceDirect 403; Elsevier API metadata only; the archived PDF link is a JavaScript challenge). The abstract alone was read: "scenario-oriented workloads portraying representative user behaviors modeled from the cooperative workflow in modern office routines"; "high sensitivity of CpsMark+ to various hardware components, e.g., CPU". The issue's cover date, October 2022, matches the entry's "(the October 2022 issue …)".
- Verdict: UNVERIFIABLE (all five).
- Fix: none from this reader; another reader with access to the publisher PDF (the entry's Wayback capture of `main.pdf`, SHA-256 04d9f106…) should re-read Tables 2 and 4, §4.3.4 and §4.7.2.

### D-F4-13 — the application PCMark 10's Writing workload runs
- Location: `docs/workload/scenario-catalog.md:12, :33`.
- Repo: "PCMark 10 Productivity runs LibreOffice Writer (`pcmark10`)".
- Passage (Phase 1 §A39, the April 2018 edition, p. 40): "The test uses LibreOffice Writer application and is implemented using AutoIt3 scripts."; p. 7: "PCMark 10 improves the Writing workload by using LibreOffice Writer instead of the simpler Workpad-like app used in PCMark 8."
- Verdict: SUPPORTED (read in the 2018 edition; the cited 2021-02-11 edition was not obtained).
- Fix: none.

### D-F4-14 — whether PCMark 10's guide documents per-task or per-process timing
- Location: `dataset/sources.yaml:125-126`; `docs/references.md:224`.
- Repo: "The guide times each workload's scripted tasks; it documents no per-process timing."
- Passage (Phase 1 §A39, 2018 edition): "implemented using AutoIt3 scripts"; "The workloads measure the time it takes to load the documents, save the file, add pictures, and edit the document."; "Measure the time taken until the application is responsive."; no per-process timing found.
- Verdict: SUPPORTED (2018 edition).
- Fix: none.

### D-F4-15 — where PCMark 10's video-playback test sits
- Location: `docs/workload/scenario-catalog.md:24` (row S13), `:33` (note 1); `docs/references.md:224`.
- Repo: ":24 "PCMark 10's Video playback battery-life profile (`pcmark10`)"; :33 "PCMark 10's groups define … S13 (Video playback)"; references.md:224 "its Productivity, Web Browsing, Video Conferencing, Photo Editing, Video Editing and Video-playback battery groups".
- Passage (Phase 1 §A39): online guide: "PCMark 10 Battery Life Profile" › "Video battery life" (one of five battery-life scenarios); 2018 guide p. 31: the "Video" workload inside the Web Browsing test of the Essentials test group. Neither makes a "Video playback" test group.
- Verdict: WORDING-FIX (:33 and references.md:224 call it a group; :24's "profile" names the Battery Life Profile, whose Video entry is a scenario).
- Fix: :24 "PCMark 10's Battery Life Profile, its Video scenario"; :33 "… S7 (Video Editing), and its Battery Life Profile's Video scenario S13"; references.md:224 "… and the Battery Life Profile's Video scenario".

### D-F4-18 — SYSmark 30's four scenarios
- Location: `docs/references.md:229`; `dataset/sources.yaml:131-135`; `docs/workload/grounding-sources.md:15`.
- Repo: the four scenario descriptions quoted from the guide; sources.yaml "Office Applications, General Productivity (incl. archiving and unpacking a mixed file set, OCR, browsing), Photo Editing, Advanced Content Creation (incl. a multitasking workload switching photo<->video editing)".
- Passage (Phase 1 §A40): User Guide v1.2 pp. 34–35 and whitepaper §2.6, word for word the entry's quotations ("models OCR of documents, web browsing, application installation, and archiving and unpacking a mixed file data set", "A multitasking workload switches between photo editing and video editing workloads.").
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-19 — the applications SYSmark 30 names
- Location: `docs/references.md:229`; `docs/workload/scenario-catalog.md:12, :18, :27`.
- Repo: "Microsoft Excel / Outlook / PowerPoint / Word 2021 Professional Plus VL; … Corel WinZip 26.0, Google Chrome 106.0.5249.103; … Photoshop CC 23 and Premiere CC 22"; mappings Word → LibreOffice Writer, Premiere → Kdenlive, WinZip → 7-Zip.
- Passage (Phase 1 §A40): the identical lists in the User Guide (p. 34) and the whitepaper §2.3.
- Verdict: SUPPORTED (the Linux mappings are the project's, labelled in `dataset/sources.yaml:116`).
- Fix: none.

### D-F4-20 — SYSmark 30's archiving workload
- Location: `docs/workload/scenario-catalog.md:27, :33`.
- Repo: "SYSmark 30 General Productivity's archive workload, WinZip → 7-Zip (`sysmark30`)".
- Passage (Phase 1 §A40): "archiving and unpacking a mixed file data set"; "Corel WinZip 26.0".
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-21 — photo editing beside a background encode; Outlook kept open
- Location: `docs/workload/building-plan.md:135`; `dataset/timelines/coreset/c3-creation.timeline.yaml:2-3`; `docs/workload/scenario-catalog.md:15, :33`; `docs/references.md:229`.
- Repo: "SYSmark 30 Advanced Content Creation (`sysmark30`) defines photo editing beside a background encode"; "SYSmark 30 keeps Outlook open (`sysmark30`)"; references.md:229 "its multitasking workload is an overlap, not a sequence".
- Passage (Phase 1 §A40): whitepaper v1.2 §2.2 (pp. 10–11): "A video encode is started in Adobe Premiere and sent to the background while Adobe Photoshop is launched and used to manipulate photos in the foreground." and "MS Outlook is launched and remains open throughout the scenario for ambient load." The User Guide v1.2 — the copy `sysmark30` cites — says only "A multitasking workload switches between photo editing and video editing workloads" and lists Outlook without saying it stays open.
- Verdict: WORDING-FIX (the facts hold in the whitepaper, not in the cited guide; "overlap, not a sequence" contradicts the guide's own "switches between" unless the whitepaper is cited).
- Fix: add the whitepaper v1.2 (bapco-sysmark30-whitepaper-v1.2.pdf, Wayback 20250423012959, SHA-256 4111c36e…, §2.2 pp. 10–11) to the `sysmark30` cite and point these four locations and references.md:229's "overlap" sentence to it.

### D-F4-23 — SYSmark 25 includes code compilation
- Location: `docs/references.md:234`; `docs/workload/scenario-catalog.md:22, :33`; `docs/workload/grounding-sources.md:15`.
- Repo: "The Productivity scenario's description names "software development (code compilation)" (p. 32); no compiler or IDE appears in any application list (p. 31)".
- Passage (Phase 1 §A40, pages corrected above): p. 32 "… software development (code compilation), application installation, and archiving files."; p. 31 Productivity list (Acrobat, Audacity installer, AutoIT, WinZip 24, Chrome, Office 2019, Shotcut) — no compiler or IDE.
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-24 — which SYSmark versions define Productivity, Creativity and Responsiveness
- Location: `docs/references.md:234`; `docs/workload/grounding-sources.md:15`.
- Repo: "SYSmark 2018 already defines the same three scenarios, Productivity, Creativity and Responsiveness, its Productivity naming software development; SYSmark 30 carries neither".
- Passage (Phase 1 §A40): SYSmark 25 defines the three (pp. 31–32); SYSmark 30's four scenarios are others (its user guide's disclosure section still says "Office Productivity, General Productivity", p. 38, and "the Productivity scenario rating", p. 39). The SYSmark 2018 guide was not read.
- Verdict: UNVERIFIABLE (the SYSmark 2018 clause, the claim's point, was not read; the SYSmark 25 and 30 parts are supported).
- Fix: none from this reader; optionally note the SYSmark 30 guide's leftover "Productivity" wording in its disclosure section.

### D-F4-26 — how many Procyon benchmarks, and how many run AI inference on the device
- Location: `docs/workload/grounding-sources.md:16`; `docs/references.md:239`.
- Repo: "UL's suite of ten benchmarks, three of them local-AI inference (text generation, image generation, computer vision)"; references: "The other seven: … and "AI Inference Benchmark for Android"".
- Passage (Phase 1 §A41): ten benchmarks in the page body (nine in its menu); AI Inference Benchmark for Android: "Benchmark and compare the AI inference performance of the latest Android smartphones. … The models run on the device". Same page SHA-256 as the entry's (b65d770e…).
- Verdict: WORDING-FIX (four run on-device AI inference).
- Fix: "ten benchmarks, four of them on-device AI inference (text generation, image generation, computer vision, and inference on Android)", or "three desktop AI inference benchmarks, beside one for Android".

### D-F4-27 — Procyon's office, photo and video applications
- Location: `docs/references.md:239`; `docs/workload/grounding-sources.md:16`.
- Repo: "Office Productivity (Word, Excel, PowerPoint, Outlook), Photo Editing (Adobe Lightroom, Adobe Photoshop), Video Editing (Adobe Premiere Pro)".
- Passage (Phase 1 §A41): "using Microsoft Word, Excel, PowerPoint and Outlook"; "uses Adobe® Lightroom® … in Adobe® Photoshop®"; "uses Adobe® Premiere® Pro".
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-29 — what Firefox's tab-count probe measures
- Location: `dataset/sources.yaml:195-198`; `docs/references.md:541-542`.
- Repo: "the per-subsession maximum of open tabs across all windows"; references quotes `metrics.yaml:254–256` at commit cf519493 "The count of maximum number of tabs open during a subsession, across all windows, including tabs in private windows and restored at startup".
- Passage (Phase 1 §A42): at commit 751f5671 (2026-10-15, the Glean Dictionary's source): "The count of maximum number of tabs open, across all windows, including tabs in private windows and restored at startup." (Phase 2 check: `metrics.yaml` at cf519493 reads "… tabs open during a subsession, across all windows, …", lines 254–256 — the entry's quotation holds at its pinned commit; the words "during a subsession" were removed upstream between 2026-09-26 and 2026-10-15.)
- Verdict: SUPPORTED (at the pinned commit).
- Fix: none required; optionally note that the current definition no longer says "during a subsession" (the metric's lifetime is `ping`).

### D-F4-30 — GLAM's Linux medians for release 152
- Location: `docs/references.md:542`; `docs/workload/building-plan.md:116`; `dataset/timelines/coreset/c1-browsing.timeline.yaml:4`, `c1-office.timeline.yaml:3`, `c3-workday.timeline.yaml:5`, `c3-evening.timeline.yaml:4`, `c4.variant.yaml:47`; `docs/workload/grounding-sources.md:51`; `docs/workload/measurement-overview.md:198`.
- Repo: "Linux, release 152, 7,535,303 clients: the median per-client peak of concurrent tabs 4.67, so five tabs; windows, the median per-client peak 1. The Linux median of the tab peak holds at 3.4–5.0 across releases 137–156".
- Passage (Phase 1 §A42, `ping_type` `*`): `max` median 4.67 tabs, 1 window, version 152 Linux. (Phase 2 check with the entry's `ping_type: metrics`, local `…/glam/tab-metrics.json`: `total_users` 7,535,303, median 4.67 — exact; over versions 137–156 the `max` median runs 3.37 (v149) to 4.98, i.e. 3.4–5.0.)
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-31 — whether Firefox's telemetry counts tabs per window
- Location: `docs/workload/coreset-guide.md:197`.
- Repo: "Firefox Linux telemetry의 창당 탭 다섯(`glam`)" ("five tabs per window").
- Passage (Phase 1 §A42): "The count of maximum number of tabs open, across all windows, …"; the window count is a separate probe (median 1).
- Verdict: WORDING-FIX.
- Fix: "Firefox Linux telemetry의 탭 다섯과 창 하나(`glam`)" (five tabs and one window).

### D-F4-36 — PyTorch's Basic MNIST example
- Location: `dataset/sources.yaml:175-180`; `docs/references.md:436`; `dataset/archetypes.yaml:923-925`; `docs/workload/scenario-catalog.md:23`; `dataset/timelines/coreset/c1-ml-train.timeline.yaml:2-3`.
- Repo: "run as the README's `python main.py` with `--save-model` at the defaults"; "14 epochs of batch 64 … a test pass of batch 1,000 … the checkpoint written (`main.py:75–137`)".
- Passage (Phase 1 §A43): README "python main.py"; `main.py` l. 75 batch 64, l. 77 test batch 1000, l. 79 epochs 14, l. 93 `--save-model` `store_true`, l. 136–137 `torch.save(…, "mnist_cnn.pt")`.
- Verdict: SUPPORTED.
- Fix: none.

### D-F4-37 — Kdenlive 23.08.5's export
- Location: `dataset/sources.yaml:185-188`; `docs/references.md:461`; `dataset/archetypes.yaml:929-935`; `docs/workload/scenario-catalog.md:18`; `dataset/timelines/coreset/c1-render.timeline.yaml:3-6`.
- Repo: "the render dialog starts `kdenlive_render`, which runs `melt-7` on the project's playlist with the shipped default MP4-H264/AAC profile"; "x264 `veryfast`, CRF 23, a GOP of 15, AAC at 160 kb/s".
- Passage (Phase 1 §A43): `renderwidget.cpp:789–790` `QProcess::startDetached(KdenliveSettings::kdenliverendererpath(), rendererArgs)`; `kdenlive_render.cpp:153, 179–180` (the melt renderer path argument); `renderjob.cpp:276` `m_renderProcess->start(m_prog, m_args)`; `kdenlivesettings.kcfg:966–969` `<default>MP4-H264/AAC</default>`; `profiles.xml:7–11` (libx264, `defaultquality="23"`, `g=15`, `defaultaudiobitrate="160"`, `defaultspeedindex="6"` = `preset=veryfast` in its list).
- Verdict: SUPPORTED (the binary name `melt-7` comes from `mltconnection.cpp`, not read here; the chain kdenlive_render → melt matches).
- Fix: none.

### D-F4-45 — whether Chromium on Linux marks a window covered by another application as occluded
- Location: `docs/workload/measurement-overview.md:51`.
- Repo: "the Steam client is measured with its window shown, which a game covering it would not change, since Linux Chromium tracks no cross-application occlusion".
- Passage (Phase 1 §A44, tag 155.0.8059.84): the computed native occlusion tracker is `#if BUILDFLAG(IS_WIN)` only — but `x11_window.cc:2405–2407` `is_occluded_ = visibility->state == x11::Visibility::FullyObscured;` → `kOccluded` → `OnOcclusionStateChanged`, mapped to `Window::OcclusionState::OCCLUDED` (`window_tree_host_platform.cc:354–371`). (Phase 2 checks: `ui/aura/window_occlusion_tracker.cc` at the same tag, l. 1188–1201, stores the host's reported state for the root window and recomputes occlusion, so the X11 report reaches the windows the tracker follows; the same `FullyObscured` lines are present at 30010bf0, the commit the 9.8 record read, `x11_window.cc:2405`.)
- Verdict: CONTRADICTED (at source level: on X11 Chromium marks its window occluded when the X server reports it fully obscured, which is cross-application occlusion; the record looked only at the Windows-only computed tracker). Whether the X server (or Xwayland under GNOME's compositor) ever sends `FullyObscured` for the Steam window is not settled by the source; the Wayland backend sets no occlusion.
- Fix: "since Linux Chromium computes no occlusion of its own (Windows only) and on X11 marks a window occluded only when the X server reports it fully obscured, [which the measurement setting does / does not deliver — state with its evidence]"; or remove the "since" clause and rest the choice on the measurement.

### D-F4-43 — how long Chromium waits before throttling a background page's timers
- Location: `docs/workload/measurement-overview.md:51`; `dataset/archetypes.yaml:738`.
- Repo: overview "Background tabs are measured past Chromium's documented intensive-throttling grace"; archetypes "observed past Chromium's intensive-wake-up-throttling grace (… 330 s of the documented five-minute default …)".
- Passage (Phase 1 §A44): `features.h` "wake ups from timers with a high nesting level are limited to 1 per minute on a page that has been backgrounded for GetIntensiveWakeUpThrottlingGracePeriod()" … "- 1 wake up per second in a background page or hidden cross-origin frame - 1% CPU time in a page that has been backgrounded for 10 seconds"; `kIntensiveWakeUpThrottling_GracePeriodSeconds_Default = 5 * 60;` `kIntensiveWakeUpThrottling_GracePeriodSecondsLoaded_Default = 60;`; `features.cc` l. 75–83: `if (loading) { seconds = …GracePeriodSeconds.Get(); } else { seconds = …GracePeriodSecondsLoaded_Default; }`. (Phase 2 check: the same branch at 999361f1, the commit the 9.8 record read, `features.cc:75–83`.)
- Verdict: WORDING-FIX (the five-minute default is the grace for a page still loading; a loaded page — the measured setInterval page — gets 60 s by default. The measurement, 330 s past, is past both, so overview :51 holds).
- Fix: archetypes.yaml:738 "… 330 s of the documented grace (five minutes while loading, 60 s once loaded) …".

### D-F4-46 — how long an idle Matrix client's `/sync` request waits
- Location: `docs/workload/measurement-overview.md:51`.
- Repo: "the chat client idles on the Matrix 30 s `/sync` long poll".
- Passage (Phase 1 §A45): spec `sync.yaml:109–117` "The maximum time to wait, in milliseconds … By default, this is `0` …", `example: 30000`; matrix-js-sdk `sync.ts:189` `pollTimeout: 30 * 1000`, used once caught up (l. 948–964).
- Verdict: WORDING-FIX (30 s is the client library's default, not the protocol's, whose default is 0).
- Fix: "the chat client idles on matrix-js-sdk's 30 s `/sync` long poll".

### D-F4-40 — GNOME's default idle delay and what follows
- Location: `docs/workload/measurement-overview.md:51`.
- Repo: "the session is left untouched until its 300 s idle delay locks the screen and blanks the monitor".
- Passage (Phase 1 §A46): `idle-delay` `<default>300</default>` "Time before session is considered idle"; gnome-session binds it to presence idle (`gsm-manager.c:3480–3487`, `gsm-presence.c:143–151`); screensaver `lock-enabled` true, `lock-delay` 0; gnome-settings-daemon blanks once the screensaver is on (`gsd-power-manager.c:1926–1939`).
- Verdict: SUPPORTED (the presence-idle → screen-shield step is gnome-shell's, which the 9.9 record read and this reader did not).
- Fix: none.

### D-F4-42 — whether the GNOME 46 session at idle runs an X server
- Location: `docs/workload/scenario-catalog.md:29`; `dataset/timelines/coreset/c1-idle.timeline.yaml:1-3`.
- Repo: "Ubuntu 24.04's GNOME 46 Wayland session at idle, blanked, which runs no X server".
- Passage (Phase 1 §A46): Mutter 46.2 `meta-context-main.c:332–353`: in a Wayland session run as a systemd user unit, `META_X11_DISPLAY_POLICY_ON_DEMAND`.
- Verdict: SUPPORTED (on demand, so none at idle unless an X client asks; the absence itself is the campaign's observation).
- Fix: none.

### D-F5-21 — Ubuntu 24.04's desktop kernel transparent-hugepage default
- Location: `docs/workload/measurement-overview.md:209`; `dataset/archetypes.yaml:929, :942, :1638`.
- Repo: "Ubuntu 24.04's desktop kernel defaults to `madvise`".
- Passage (Phase 1 §A47): `debian.master/config/annotations` at Ubuntu-6.8.0-31.31 and Ubuntu-6.8.0-147.147: `CONFIG_TRANSPARENT_HUGEPAGE_MADVISE` `'amd64': 'y'`, `…_ALWAYS` `'amd64': 'n'`. (The 9.10 record read the HWE 7.0.0-31 config, also `MADVISE=y`.)
- Verdict: SUPPORTED (for the GA kernel, release and current, as well as the HWE one the record read).
- Fix: none.

---

## Per claim — the extra sources

### D-F5-01 — servers of one nominal type differ run to run (`maricq-osdi18`)
- Location: `docs/workload/measurement-overview.md:73` (also :172).
- Repo: "`maricq-osdi18`: servers "with supposedly identical parts" differ run to run."
- Passage (Phase 1 §B3): abstract, p. 409: "software run repeatedly on the same server (or a different server with supposedly identical parts) can produce performance results that differ with each execution."
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-02 — nonparametric median intervals unless normality is shown (`maricq-osdi18`)
- Location: `docs/workload/measurement-overview.md:79`.
- Repo: "`maricq-osdi18` recommends nonparametric intervals of the median unless normality is shown; the rule's is a t interval."
- Passage (Phase 1 §B3): §2, p. 410: "we adopt nonparametric statistics for the remainder of this paper, and recommend that, for performance experiments, these methods be used unless normality can be demonstrated." … "In nonparametric analysis, one uses the median, rather than the mean".
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-03 — repeat and take the interval at the highest level (`kalibera-ismm13`)
- Location: `docs/workload/measurement-overview.md:74` (also :173).
- Repo: "The interval is taken over independent repeats, never over samples within a run. | `kalibera-ismm13` §3, §9.3"; references.md:119 quotes §3 and §9.3.
- Passage (Phase 1 §B1): §3, p. 66 "At the very least, repetition must be done at the highest level that has random variation to avoid bias"; §9.3, p. 72, eq. (4) with "ν = rn − 1 degrees of freedom"; §11 "the confidence interval uses only the variance estimate at the highest level".
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-04 — on-line count, minimum of five (`kalibera-ismm13`)
- Location: `docs/workload/measurement-overview.md:76` (also :173).
- Repo: "At least five repeats. Repeats are added one at a time … until every value holds. … | `kalibera-ismm13` §11".
- Passage (Phase 1 §B1): §11, p. 73 "We do not show counts of fewer than 5 executions as they could hardly be used to get the variance estimate right"; "The number of executions (highest-level repetitions) can be established on-line, by adding repetitions until the confidence interval is sufficiently narrow."
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-05 — Georges et al.'s construction (`georges-oopsla07`)
- Location: `docs/workload/measurement-overview.md:174`.
- Repo: "the same construction: an interval over independent runs, runs added until a set precision".
- Passage (Phase 1 §B2): §4.3, p. 66 "If the confidence interval achieves a desired level of precision, i.e., the confidence interval is within 1% or 2% of the sample mean, the script stops the experiment"; §4.1 the interval over VM invocations, z above 30 measurements, t otherwise.
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-06 — the "No ceiling" row's ground column
- Location: `docs/workload/measurement-overview.md:76`; also `docs/guidebook/dataset/06-grounding-measurement-verification.md:882`.
- Repo: "Minimum and stopping | At least five repeats. … until every value holds. No ceiling. | `kalibera-ismm13` §11; `georges-oopsla07` §4".
- Passage (Phase 1 §B2, §B1): Georges §4.3 "Or, if the desired level of precision is not reached after a preset number of runs, e.g., 30 runs, the obtained confidence interval is simply reported along with the sample mean."; Kalibera §11 sets the top-level count on-line and states no cap.
- Verdict: WORDING-FIX (Georges has a preset cap; "no ceiling" is the project's, 9.5 decision D33).
- Fix: "No ceiling (9.5 D33)", and cite `georges-oopsla07` §4.3 only for "runs added until a set precision".

### D-F5-07 — the half-width of a count-weighted mean (`cochran-st77`)
- Location: `docs/workload/measurement-overview.md:75` (also :175).
- Repo: "The table's half-width is the ratio estimator's (`cochran-st77`)."; references.md:134 quotes §9A.1 p. 250.
- Passage (Phase 1 §B5): p. 250 "If the Mi and hence M0 are all known, an alternative is a ratio estimate in which Mi is taken as the auxiliary variate xi" … "By theorem 6.1, assuming that the number of clusters in the sample is large, V(Ŷ_R) = … (9A.4). As (9A.4) shows, the variance of Ŷ_R depends on the variability among the means per element". The scan lacks p. 249 (the start of §9A.1).
- Verdict: SUPPORTED.
- Fix: none.

### D-F5-08 — Cochran's ratio variance is a large-sample result
- Location: `docs/workload/measurement-overview.md:79`.
- Repo: "`cochran-st77`'s ratio variance is a large-sample result, and the campaigns' counts are 5 to 77."
- Passage (Phase 1 §B5): §6.3, p. 153 "As working rule, the large-sample results may be used if the sample size exceeds 30 and is also large enough so that the coefficients of variation of x̄ and ȳ are both less than 10%."; §6.5, p. 156 "When these conditions do not apply, the formula for v(R̂) tends to give values that are too low".
- Verdict: SUPPORTED (the counts are the project's; references.md:134 says "5 to 45", this line "5 to 77", which the guidebook's volume 6 line 959 already explains).
- Fix: none.

### D-F5-09 — first-crossing coverage and the .929 bound (`chow-aoms65`)
- Location: `docs/workload/measurement-overview.md:77` (also :176).
- Repo: "`chow-aoms65`: first-crossing coverage reaches the nominal level only asymptotically, with a lower bound near .929".
- Passage (Phase 1 §B4): (5) p. 458 "lim d→0 P(µ ε IN) = α"; p. 461 "Extensive numerical computations in the N(µ, σ²) case have been made by Starr … for α = .95 the lower bound for all d > 0 of P(…), where N is the smallest odd integer k ≥ 3 such that …, is about .929 if the values ak are taken from the t-distribution with (k − 1) degrees of freedom."
- Verdict: WORDING-FIX (the .929 is Starr's, for normal data, the t constants and odd k ≥ 3; stated unqualified).
- Fix: "… with a lower bound near .929 in the normal case with a t rule (Starr's computations, reported p. 461)".

### D-F5-10 — the standard error of a compiled wake count (`feller-ipta50`)
- Location: `docs/workload/measurement-overview.md:106` (also :177).
- Repo: "within 5 % or four standard errors of the count (`feller-ipta50`)"; "the standard error of a compiled wake count".
- Passage (Phase 1 §B6): §12.4, p. 248 "This leads to defining the variable Nr as the number of occurrences of E in r trials." … "Now let us suppose that E is certain and that the distribution {fn} has finite mean µ and finite variance σ². Then by the central limit theorem …" with the reduced variable "(4.5) Nr* = (Nr − r/µ)/(σ r^½ µ^−3/2)".
- Verdict: SUPPORTED (the count's scale σ r^½ µ^−3/2 is on p. 248; the theorem's statement on p. 249 and §12.2 were not read here). The topic's binomial-to-Poisson limit (§6.4) is not what the repository uses.
- Fix: none (the tolerances' label is the separate finding on D-F5-11).

### D-F5-14 — what RFC 8290 grounds for the queue
- Location: `docs/workload/measurement-overview.md:52`, `:197`.
- Repo: :52 "with an `fq_codel` queue (`fqcodel-rfc18`)"; :197 "the download's link rate and why its queue is `fq_codel`".
- Passage (Phase 1 §B12): abstract "a powerful tool for fighting bufferbloat and reducing latency … provides isolation for low-rate traffic …"; "Category: Experimental"; "This document is not an Internet Standards Track specification".
- Verdict: WORDING-FIX at :197 (the RFC states what the discipline is for, not why this project adopted it); :52 SUPPORTED.
- Fix: :197 "why `fq_codel` was the queue tried (its adoption: 9.7 D25)".

### D-F5-15 — GitHub deletes artifacts after 90 days (`gh-artifact-retention`)
- Location: `docs/workload/measurement-overview.md:42, :179`; `docs/workload/building-plan.md:250`; `dataset/README.md:219`.
- Repo: "before GitHub deletes a workflow's artifacts after 90 days".
- Passage (Phase 1 §B11): "By default, checks, workflow runs, commit statuses, and the artifacts and log files generated by workflows are retained for 90 days before they are automatically deleted." Same SHA-256 as the entry.
- Verdict: SUPPORTED (it is the default; a public repository can set 1–90 days).
- Fix: none.

### D-F4-33 — Glean's `glean.mps` thread at 04:00 (`glean`)
- Location: `docs/workload/measurement-overview.md:200`; `docs/references.md:421`.
- Repo: "Thunderbird's daily 04:00 metrics thread, stated as a clock event"; references: `const SCHEDULED_HOUR: u32 = 4;`, "Today's 04:00 in local time", spawned as `"glean.mps"`, reschedules daily, "overdue" at startup.
- Passage (Phase 1 §B7): `scheduler.rs:21` `const SCHEDULED_HOUR: u32 = 4;`; l. 138 `// Today's 04:00 in local time`; l. 154 `Some("overdue")`; l. 212 `crate::thread::spawn("glean.mps", …)`.
- Verdict: SUPPORTED (Glean SDK at 25b0fb2; which Glean Thunderbird 156 vendors was not read here either, as the entry states).
- Fix: none.

### D-F4-39 — a stock Ubuntu 24.04 desktop does not run `systemd-networkd`
- Location: `docs/workload/measurement-overview.md:100, :199`; `docs/references.md:401, :406, :416`.
- Repo: "software a stock Ubuntu 24.04 desktop does not run (`ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan`)"; references: postinst enables getty@tty1, remote-fs.target, systemd-pstore "by default on new installs" and no other unit; presets applied only on a first boot; netplan enables networkd only if it wrote networkd configuration; the desktop image writes `renderer: NetworkManager`.
- Passage (Phase 1 §B8–§B10): `systemd.postinst:35–40`; `debian/rules:251–259`; `90-systemd.preset:21–22` `enable systemd-networkd.service`; `manager.c:1865–1883` presets only on first boot; `main.c:2145–2158`; netplan `generate.c:314–317` `if (any_networkd) enable_networkd(…)`; livecd-rootfs `functions:1045–1058` `renderer: NetworkManager`.
- Verdict: SUPPORTED (that an installed desktop is not a first boot rests on `ubuntu-desktop-bootstrap`, not read here).
- Fix: none; pin `netplan`'s copy to 5cb27ab (= `import/1.1.2-8ubuntu1_24.04.3`).

### D-F3-11 — the kernel's Makefile passes no `-pipe`
- Location: `dataset/archetypes.yaml:1017-1018`.
- Repo: "no `-pipe` in the kernel's Makefile so `cc1` and `as` run in sequence".
- Passage (Phase 1 §B14): no `-pipe` in `Makefile`, `arch/x86/Makefile*` or `scripts/Makefile*` at v6.17; none in `Makefile` or `arch/x86/Makefile` at v6.6 (the tag 9.6 built) or any tag from v5.4 on; `arch/x86/Makefile` had `KBUILD_CFLAGS += -pipe` at v4.19 (l. 218).
- Verdict: SUPPORTED (GCC's piping rule, the second half, was not read here).
- Fix: none; the record can take this grep with the tags.

### F-54 (outside inventory) — when `sched_waking` fires
- Location: `docs/guidebook/dataset/08-decision-chronicle.md:1027, :1722`.
- Repo: ":1027 "`sched_waking`은 잠든 thread에만 발생하고 scheduler가 그 thread를 내려놓기 전에 찍히므로" (fires only for a sleeping thread and is recorded before the scheduler takes that thread off the CPU); :1722 "`sched_waking`은 짧은 대기에서 switch-out 기록보다 먼저 찍혀" (on a short wait it is recorded before the switch-out)".
- Passage (Phase 1 §B13): `sched.h:167–169` "Tracepoint called when waking a task; this tracepoint is guaranteed to be called from the waking context."; `core.c:4216–4221` `trace_sched_waking(p)` right after `ttwu_state_match`, before `if (READ_ONCE(p->on_rq) && ttwu_runnable(…))` and before `smp_cond_load_acquire(&p->on_cpu, !VAL)` ("If the owning (remote) CPU is still in the middle of schedule() with this task as prev, wait until it's done referencing the task.").
- Verdict: WORDING-FIX (:1027 makes it always precede the switch-out; the source orders it before the waker checks the runqueue and waits for the task to leave its CPU, so it *can* precede the switch-out on a short wait — :1722's wording — but follows it when the task has long been switched out; it also fires for a task that set a sleep state and has not yet switched out at all, which `ttwu_runnable` handles).
- Fix: :1027 "`sched_waking`은 잠든 상태로 표시된 thread에만, waker 쪽에서 그 thread가 CPU를 떠났는지 확인하기 전에 찍히므로, 짧은 대기에서는 그 thread의 switch-out 기록보다 먼저 올 수 있습니다" (fires only for a thread in a sleep state, in the waker, before it checks that the thread has left its CPU — so on a short wait it can precede the thread's own switch-out).

---

## Outside-inventory rows on the extra sources (short form)

| row | location | repo wording (short) | passage (Phase 1) | verdict | fix |
|---|---|---|---|---|---|
| E-42 | `docs/guidebook/dataset/02-the-archetype-library.md:843` | Thunderbird's Glean metrics-ping scheduler wakes once a day at local 04:00 | §B7 `SCHEDULED_HOUR = 4`, "Today's 04:00 in local time" | SUPPORTED | none |
| E-43 | `…/02-the-archetype-library.md:633` | "servers with supposedly identical parts" differ run to run | §B3 abstract | SUPPORTED | none |
| E-44 | `…/02-the-archetype-library.md:641` | §11 "We do not show counts of fewer than 5 executions …" | §B1 §11 p. 73, verbatim | SUPPORTED | none |
| E-45 | `…/02-the-archetype-library.md:646` | a sequential interval stopped at its first pass reaches nominal coverage only asymptotically | §B4 rule (3), (5) "lim d→0 P(µ ε IN) = α" | SUPPORTED | none |
| E-46 | `…/02-the-archetype-library.md:640` | the table's half-width is the ratio estimator's | §B5 p. 250 | SUPPORTED | none |
| E-47 | `…/02-the-archetype-library.md:669` | `feller-ipta50` the ground of the count standard error | §B6 p. 248 (4.5) | SUPPORTED | none |
| E-54 | `…/01-the-big-picture.md:1127`; `…/02-the-archetype-library.md:629` | GitHub deletes a workflow's artifacts after 90 days | §B11 l. 234 | SUPPORTED | none |
| F-11 | `…/06-grounding-measurement-verification.md:1065`; `…/07-*.md:1290` | "… retained for 90 days before they are automatically deleted" | §B11 l. 234, verbatim | SUPPORTED | none |
| F-55 | `…/06-*.md:869, :878, :881, :882, :891, :897, :916`; `…/08-decision-chronicle.md:983, :1719` | §3 highest level; §9.3 single-level equivalence; §11 minimum five; §11 figures are Table 6's columns; §12 "do not use our dimensioning results at face value" | §B1 §3, §9.3, §11, §12, verbatim | WORDING-FIX at `06-*.md:882` only ("상한 없음", no ceiling, grounded on `kalibera-ismm13` §11 and `georges-oopsla07` §4); the rest SUPPORTED | at :882 attribute "no ceiling" to 9.5 D33 and cite Georges only for adding runs to a precision |
| F-56 | `…/06-*.md:882, :916, :961` | §4.3's "30 runs" an example; §6.2.1 variation across hardware platforms | §B2 §4.3 "e.g., 30 runs"; §6.2.1 "The various graphs show different hardware platforms" (with §5.3's three platforms) | SUPPORTED | none |
| F-57 | `…/06-*.md:877, :958, :1686` | §2 nonparametric median intervals "unless normality can be demonstrated"; many VMs, many times | §B3 §2 p. 410; §7.5 not read | SUPPORTED for the §2 clause; UNVERIFIABLE for "many VMs, many times" | none from this reader |
| F-58 | `…/06-*.md:883, :944, :1688` | rule (3); asymptotic only; Starr "about .929" (normal population, t rule, at :944) | §B4 p. 457, p. 458, p. 461 | SUPPORTED (:944 carries the qualification) | none |
| F-59 | `…/06-*.md:873, :899, :959` | §9A.1 ratio estimate; §6.3 "exceeds 30 … less than 10%"; §6.5 "tends to give values that are too low" | §B5 pp. 250, 153, 156, verbatim | SUPPORTED | none |
| F-60 | `…/06-*.md:1037` | the wake-count standard error from Feller's recurrent-event theorem | §B6 p. 248 | SUPPORTED | none |

## The `docs/references.md` entries of the extra sources — quoted passages against the copies read

- `kalibera-ismm13` (`docs/references.md:117-120`): §3, §9.3 (eq. 4 and the single-level equivalence), §11 (on-line count, the 1/1.5/2.5/5 % sentence, the minimum of five, counts depending on platform, VM and benchmark), §12 — all match Phase 1 §B1. SUPPORTED.
- `georges-oopsla07` (`:112-115`): §4.1, §4.2, §4.3 quotations match Phase 1 §B2 (§4.2's sentence is in the same copy, p. 65). "its stopping rule has a cap of about thirty runs" — WORDING-FIX: the source gives "a preset number of runs, e.g., 30 runs". Fix: "its stopping rule caps at a preset number of runs (its example: 30)".
- `maricq-osdi18` (`:122-125`): the abstract and §2 ("an estimate of what is required to get the desired confidence: empirical CIs must still be computed from the data gathered"; "unless normality can be demonstrated") match Phase 1 §B3. The §5 ("2.1–5.9×", "ten repetitions") and §7.2/§7.5 quotations were not read: UNVERIFIABLE here.
- `chow-aoms65` (`:127-130`): rule (3) p. 457, (5) and (6) p. 458, the Starr passage p. 461, "under the sole assumption that 0 < σ² < ∞" — all match Phase 1 §B4. SUPPORTED. (Phase 1 read the Wayback capture of Project Euclid's PDF; Project Euclid itself was not reachable.)
- `cochran-st77` (`:132-135`): §9A.1 p. 250, Theorem 6.1's (6.4) p. 153, §6.3 p. 153, §6.5 p. 156 and (6.15) match Phase 1 §B5. The §6.4 p. 155 quotations ("… as a sample estimate of the population variance. This estimate has a bias of order 1/n", (6.13)) were seen only in the scan's OCR layer, which garbles the formula: not verified against the page image.
- `feller-ipta50` (`:137-140`): the reduced variable (4.5) on p. 248 matches Phase 1 §B6. §12.2 (p. 242), the theorem's statement, (4.8), (4.9) and note 3 on p. 249 were not read: UNVERIFIABLE here.
- `fqcodel-rfc18` (`:142-145`): the four abstract quotations and "Experimental, not Standards Track" match Phase 1 §B12. SUPPORTED.
- `gh-artifact-retention` (`:379-382`): both quotations match Phase 1 §B11 (same SHA-256). SUPPORTED.
- `systemd-ubuntu` (`:399-402`): postinst, `override_dh_installsystemd`, links, `systemd.install` line 225, preset lines 21–22, `manager.c` 1865–1871, `main.c` 2152–2160, `machine-id.xml` 141–142 — all match Phase 1 §B8. SUPPORTED.
- `netplan` (`:404-407`): the `generate.c` passages match Phase 1 §B9; the `parse.c` (`finish_iterator`) claim was not read. Its copy has no commit: the branch head read here is 5cb27ab = tag `import/1.1.2-8ubuntu1_24.04.3`.
- `livecd-rootfs` (`:414-417`): the quoted comment and `renderer: NetworkManager`, the NetworkManager condition and the `desktop-preinstalled` exception match Phase 1 §B10 (same commit f492363). "nothing in the build applies systemd presets" was not checked.
- `glean` (`:419-422`): every quotation matches Phase 1 §B7 (same commit). SUPPORTED.
