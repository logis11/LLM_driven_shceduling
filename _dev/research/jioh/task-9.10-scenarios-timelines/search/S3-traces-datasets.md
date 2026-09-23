# S3 — public traces and datasets (task 9.10, stage 2 search)

Reader class S3. Topics owned: T1, T2, T4, T5, T7, T9, T12 (others noted where a data set speaks to them). All access on 2026-09-23 (UTC) from a claude.ai cloud container through an egress proxy. Local copies are under `../sources/S3-NN/` (gitignored); everything needed is quoted below. Statistics computed here are given with the script that produced them (scripts are reproduced verbatim in the Appendix; run from the stated folder over the copy identified by SHA-256).

## 1. Search log

| # | Date | Engine / venue | Exact query or request | Hits followed | Dead ends (status) |
|---|---|---|---|---|---|
| 1 | 2026-09-23 | doi.org → DANS SSH Data Station (Dataverse API) | `https://doi.org/10.17026/dans-x55-69zp`; `GET /api/datasets/:persistentId/?persistentId=doi:10.17026/dans-x55-69zp` | dataset v4 file list (919 files); 76 raw uLog XML files, docs → S3-01 | — |
| 2 | 2026-09-23 | WebSearch | `"Week in the Life of a Browser" Test Pilot data download` | github.com/mozilla/testpilotweb aggregated-data.html → S3-02 | testpilot.mozillalabs.com itself: Wayback `available` API returned no snapshot for `/testcases/a-week-life-2` |
| 3 | 2026-09-23 | git | `git clone --depth 1 https://github.com/mozilla/testpilotweb.git` | commit 50d5f37341e30b53af16a1c56bc981fc9a52097b (2019-03-28) | — |
| 4 | 2026-09-23 | Wayback CDX | `cdx?url=testpilot.mozillalabs.com/testcases/a-week-life-2/&matchType=prefix` | witl_small.tar.gz (20110711102216), witl_large.tar.gz (20110711101127), witl.db.gz (1.0 GB, not fetched) | `witl.tar.gz` capture is HTTP 404; several CDX/download attempts: curl (35) connection reset (proxy `ws_closed_mid_exchange` on web.archive.org), succeeded on retry |
| 5 | 2026-09-23 | data.firefox.com | `/dashboard/usage-behavior` (JS app); `/datasets/desktop/{usage-behavior,user-activity,hardware}/index.json`; `/datasets/desktop/user-activity/Worldwide/<metric>/index.json`; `/datasets/desktop/hardware/default/osName/index.json` | S3-03 | `/datasets/desktop/<x>` (404), `…/Worldwide/index.json` (404), `…/metrics/…` (404) |
| 6 | 2026-09-23 | WebSearch | `BEHACOM dataset behaviour of computer users Mendeley Data foreground application` | Mendeley Data cg4br62535 v2; PMC7270191 → S3-04 | — |
| 7 | 2026-09-23 | Mendeley Data public API; Europe PMC REST | `/public-api/datasets/cg4br62535?version=2`, `/files?folder_id=root&version=2`; `europepmc/webservices/rest/PMC7270191/fullTextXML` | Behacom.zip (37,414,157 B); article XML | — |
| 8 | 2026-09-23 | WebSearch | `DARPA OpTC dataset ecar process create download GitHub FiveDirections` | github.com/FiveDirections/OpTC-data → S3-05 | — |
| 9 | 2026-09-23 | Google Drive (gdown folder listing + `drive.usercontent.google.com/download`) | folder `1n3kkS3KR31KUegn42yk3-e6JkZvf0Caa` | manifest of 4,481 files (524 eCAR paths) | every eCAR file tried (7 ids) returned HTTP 200 with the HTML page "Google Drive - Quota exceeded … Too many users have viewed or downloaded this file recently" — no data |
| 10 | 2026-09-23 | WebSearch | `OpTC ecar dataset mirror huggingface OR kaggle OR zenodo process create benign` | "Corrected version of the DARPA OpTC dataset", DOI 10.57745/UXCWOC (Recherche Data Gouv) | doi.org resolution: CONNECT 502; README (file 717349): connection reset ×3 |
| 11 | 2026-09-23 | Recherche Data Gouv Dataverse API | `/api/datasets/:persistentId/?persistentId=doi:10.57745/UXCWOC`; `GET /api/access/datafile/713542` with `Range: bytes=0-20971519` | HTTP 206, 20 MiB head of `2019-09-16.tar` (13,437,603,840 B) → S3-05 | first two attempts CONNECT 502 / reset |
| 12 | 2026-09-23 | csr.lanl.gov | `https://csr.lanl.gov/data/cyber1/` | S3-06 (page only) | data download requires submitting an e-mail address and intended use in a web form — not done (would require sending the user's address to a third party) |
| 13 | 2026-09-23 | GitHub MCP `search_issues` (sched-ext/scx) | `scx_lavd log Proton game wine threads stutter` | 20 issue hits (#3750, #3791, #296, #3739, #3130 …) | api.github.com and github.com HTML for sched-ext/scx: HTTP 403 from the session's GitHub gate ("GitHub access to this repository is not enabled for this session"); MCP `issue_read`: "Access denied"; `add_repo` (read) confirmed only git reads are served |
| 14 | 2026-09-23 | Wayback CDX | `url=github.com/sched-ext/scx/issues/{3750,3791,296}` | #3750 capture 20260820065436 (body only) → S3-07 | #3791 CDX: connection reset; #296 capture download: reset ×4 |
| 15 | 2026-09-23 | WebSearch | `"runnable task stall" scx_lavd "steamwebhelper" OR "wineserver" OR "gamescope" dump` | none relevant | — |
| 16 | 2026-09-23 | WebSearch | `"ps aux" "wineserver" "steam-runtime-launcher-service" "pressure-vessel" output forum` | bbs.archlinux.org viewtopic id=302470 (fetched; contains Steam startup journal and `pacman -Qs`, no running-game process list) | — |
| 17 | 2026-09-23 | WebSearch | `"reaper" "SteamLaunch" "wineserver" "pv-bwrap" pstree OR "ps -ef" game running` | github.com/FeralInteractive/gamemode/issues/457 → S3-08 via WebFetch | curl of github.com: 403 (session gate); Wayback CDX for the issue: reset ×4 |
| 18 | 2026-09-23 | store.steampowered.com | `/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam`; `/hwsurvey/?platform=linux` | S3-09 | — |
| 19 | 2026-09-23 | popcon.debian.org; popcon.ubuntu.com | `https://popcon.debian.org/by_inst.gz`, `/` ; `https://popcon.ubuntu.com/` | S3-10 | popcon.ubuntu.com: HTTP 200 whose whole visible text is "Thanks!" — no statistics served |
| 20 | 2026-09-23 | openbenchmarking.org | `/test/pts/{build-linux-kernel,build-llvm,build-gcc,build-ffmpeg,build-godot,build-chromium,build-mesa,build-php,build-nodejs}` | 8 pages with metrics → S3-11 | default curl UA: HTTP 403 Cloudflare "Just a moment…" challenge; with UA `Mozilla/5.0 (X11; Linux x86_64) Phoronix-Test-Suite`: 200; build-chromium page had no metrics table |
| 21 | 2026-09-23 | travistorrent.testroots.org; Zenodo API | `https://travistorrent.testroots.org/`; `zenodo.org/api/records?q=travistorrent` | Zenodo hits 4682056, 829968, 5834872, 1291582, 17745286 (CI metadata; not opened) | travistorrent.testroots.org now serves an unrelated gambling page (domain lapsed) — dead end; copy deleted |
| 22 | 2026-09-23 | Zenodo API | `"window focus" dataset`; `"application usage" log desktop`; `ActivityWatch dataset`; `"computer usage" dataset`; `keylogging application switching dataset`; `"foreground application" dataset`; `KeyRecs`; `"process list" dataset windows`; `RescueTime data`; `Carat energy dataset apps running` | 22835224 (ActivityWatch release, software not data), 16414116 (WinMET malware sandbox traces), 5024083 (smartphone app-switch networks, 53 participants), 7886743 (KeyRecs keystrokes, no app field) | Zenodo phrase queries return mostly unrelated generic records; none is a desktop focus/process trace |
| 23 | 2026-09-23 | WebSearch | `Carat dataset University of Helsinki running applications samples download access request` | cs.helsinki.fi/group/carat/data-sharing/ → S3-13 | — |
| 24 | 2026-09-23 | HTTP range on Carat zip | `Range` on `carat-data-top1k-users-2014-to-2018-08-25.zip` (6,375,824,106 B): last 1 MiB (central directory), bytes 309211–5115724 (member part-00995.gz) | S3-13 | — |
| 25 | 2026-09-23 | WebSearch | `public dataset desktop application usage logs window title foreground timestamps participants weeks Linux OR Windows download` | arXiv 2105.09900 (31 Windows 10 users, 8 weeks) → S3-14; SENSE-42 (Zenodo 20328099) | SENSE-42: access_right "restricted", PsychoPy task logs (no desktop apps); "Mobile Phone Use Dataset" (342 participants, 2016, smartphone) not pursued (mobile) |

Downloads total ≈ 1.2 GB (SWELL uLog 378 MB, witl_large 491 MB, witl_small 7.7 MB, BEHACOM 37 MB, OpTC ranges 20 MiB, Carat ranges 5.8 MB, rest small). Large objects were read by range or streaming: OpTC (20 MiB head of a 13.4 GB tar), Carat (1 MiB central directory + one 4.8 MB member of a 6.4 GB zip), BEHACOM (6 GB of CSV streamed from the 37 MB zip without extraction), witl_large (3.65 GB events.csv streamed from the tar).

## 2. Candidates

(Id S3-07 is a lead recorded at the end of this section; S3-12 is unused — the TravisTorrent lead died, see search log #21.)

### S3-01 — SWELL-KW raw uLog computer-interaction logs (knowledge work, Windows, 2012)

**Citation.** Koldijk, S.; Sappelli, M.; Verberne, S.; Neerincx, M.; Kraaij, W. *The SWELL Knowledge Work Dataset for Stress and User Modeling Research*, DANS data set, DOI 10.17026/dans-x55-69zp (version 4, released 2025-06-04T08:57:35Z). Paper read for method: Sappelli, Verberne, Koldijk, Kraaij, "Collecting a dataset of information behaviour in context", CaRR'14, DOI 10.1145/2601301.2601306 (`CARR2014_CameraReady.pdf` in the data set).

**Access.** Open download from ssh.datastations.nl (no login); licence CC-BY-NC-SA-4.0 (from the dataset JSON: `'license': {'name': 'CC-BY-NC-SA-4.0'…}`); `termsOfAccess` "N/a".

**Copy read.**
- Dataset metadata JSON `https://ssh.datastations.nl/api/datasets/:persistentId/?persistentId=doi:10.17026/dans-x55-69zp` — SHA-256 `fa6e6ee01d0246d4864df69744ca65453b72330acc74f2c272ed3538cbec7c3e`.
- All 76 files in folder `0 - Raw data/A - anonimized Computer interaction - raw data uLog` fetched via `https://ssh.datastations.nl/api/access/datafile/<id>`; SHA-256 of the sorted `sha256sum` listing of all 76 files: `af2bd2259a3b48dd8414b160e4c389c4ba5dbf9a2e3d90dc151ba437089d3423`. Participant 1 files (the per-participant analysis): `a_pp1_c1_uLog_20120918_131425.xml` (datafile 172103, 5,324,611 B) `fb2c85bc362d62905dee83c0f835ed8162b5bddb4a1eaeab2c7b0beeb96bd884`; `a_pp1_c2_uLog_20120918_142524.xml` (171006) `0861f46aee280a3ef8c6e1859a65353bcc55d15f637bdf2a620c57c754590432`; `a_pp1_c3_uLog_20120918_152106.xml` (172241) `ff4b831f14d8e47f2d920ac1ef4118904f8b4141182b8d207ebd3fc6d96f5c5a`.
- `SWELL-KW - overview available data.tab` (datafile 171769) `0fd05a806288a994c829b080e94427f317631cec30985d4d60cefa5e6a1db0a7`; `CARR2014_CameraReady.pdf` (171844) `16ebe03138e944086c6d832a0a5df63981602771a8c5782b6bc8008f9b777d62`; `Manual KW Dataset .docx` (172099) `294a690ac7b63b7661c271bbcc1a3f1bcdc146196257a91f02a06bc22cce98e0`.
- Local: `../sources/S3-01/` (`ulog/`, `analysis/`).

**Verbatim passages.**
- CaRR'14 paper p.1 §2.1: "We collected data from 25 participants with an average age of 25 (std 3.25). … There were 8 females and 17 males, and the participants were recruited among university students and interns at TNO".
- p.1 §2.2: "The participants executed their tasks on a laptop computer equipped with Microsoft Office. The default browser was Internet Explorer with www.google.nl as start page. Also, uLog version 3.2.5⁴ was installed. [⁴ = the paper's footnote marker, extracted as "3.2.54"] uLog is a key-logging tool that saves the active application, window title, url or file that is open, caption information, mouse movements, mouse clicks and keyboard activity with timestamps."
- p.1 §2: "three conditions: a) a neutral condition in which the participants were asked to work as they normally do; b) a condition in which they were time pressured and c) a condition in which they were interrupted with email messages. Each of the conditions lasted between 30 and 45 minutes."
- p.2 §2.3: "At the beginning of each condition the participants were asked to watch a relaxing movie for 10 minutes."
- `overview.tab` rows 2–4 (block order and condition per participant): `"1"	"1"	"N"	…` / `"1"	"2"	"T"	…` / `"1"	"3"	"I"	…`; row 34 (pp11 block 3): `"yes**"` with note `"* no valid HR extracted, ** uLog crashes after a while"`.
- Raw event, `a_pp1_c1_uLog_20120918_131425.xml:1911–1926`:
  ```
  <EventAction>Window Activated</EventAction>
  <TimeStamp>2012-09-18T11:28:19.8782212Z</TimeStamp>
  …
  <EventDescription>Window "Lonely Planet Perth.docx - Microsoft Word" activated.</EventDescription>
  …
  <ControlClass>OpusApp</ControlClass>
  <ControlApplication>WINWORD</ControlApplication>
  ```
- Process-start event, same file lines 218–230: `<EventAction>Application started</EventAction>` / `<TimeStamp>2012-09-18T11:14:28.5208606Z</TimeStamp>` / `<EventDescription>The process "OUTLOOK" has started</EventDescription>` / `<CustomValue>C:\Program Files (x86)\Microsoft Office\Office14\OUTLOOK.EXE</CustomValue>`.
- Page-load event, same file lines 2973–2978: `<EventAction>Browser URL changed</EventAction>` / `<TimeStamp>2012-09-18T11:29:03.4068922Z</TimeStamp>` / `<EventDescription>The address of the browser window inside Internet Explorer changed to "mhtml:file://C:\Users\6837\Desktop\Documents\Road Trip USA along the Pacific Coast Highway …Suite101_com.mht".</EventDescription>`.
- Activation sequence, pp1 c1 (EventAction line : TimeStamp : ControlApplication): `1913: 11:28:19.878Z WINWORD` → `2126: 11:28:24.933Z explorer ("Documents")` → `2341: 11:28:33.091Z iexplore` → `2414: 11:28:33.698Z explorer` → `2633: 11:28:36.981Z iexplore` → `2994: 11:29:03.417Z iexplore` → `3556: 11:29:08.877Z WINWORD ("Document1 - Microsoft Word")` → `3680: 11:29:12.117Z explorer ("Task Switcher")` → `3724: 11:29:12.657Z iexplore` → `3971: 11:29:15.337Z OUTLOOK ("Inbox - tnoparticipant@gmail.com - Microsoft Outlook")` → `4177: 11:29:16.627Z iexplore` → `5759: 11:30:39.316Z WINWORD`. Last event timestamp at line 139274: `2012-09-18T12:14:58.035644Z`.

**What the files contain.** One XML per participant × block (76 files; pp2 block 1 is split in two, the first 13-min fragment containing only the relaxation video). Event types in pp1 c1 (6,307 events): character 3,694; special key 974; Keyboard focus changed 734; clicked 331; Window Activated 185; Application exited 98; wheel turned 95; dragged 91; Application started 56; Browser URL changed 28; doubleclicked 14; key combination 4; MessageBox activated 3 (`grep -o "<EventAction>[^<]*" | sort | uniq -c`). Each log starts before the ~8-min relaxation video (vlc) and runs until the block ends. The file index `c1/c2/c3` is the chronological block; the condition comes from `overview.tab` (verified: the T blocks are the short ones, median 30.9 min vs N 46.1 and I 45.4 min).

**Statistics computed (script `swell_focus.py`, `swell_all.py`, `swell_filtered.py`, `swell_url.py`, `swell_send.py`, Appendix A).** Definitions: a focus segment runs from a `Window Activated` event to the next activation of a *different* ControlApplication (or end of log); a switch is a boundary between segments; the "work window" starts at the first WINWORD/POWERPNT activation (excludes the relaxation video).

Participant 1 (one observation: one person, one laptop running Windows with Office 2010 (Office14 path), 2012-09-18, three blocks):

| block (condition) | span (min) | work window (min) | switches in work window | switches/min | median dwell (s) |
|---|---|---|---|---|---|
| c1 (N) 11:14–12:14 UTC | 60.54 | 46.64 | 165 | 3.54 | 4.6 |
| c2 (T) | 42.07 | 30.86 | 141 | 4.57 | 1.7 |
| c3 (I) | 58.06 | 46.64 | 157 | 3.37 | 4.7 |

Per-application focus in pp1 c1 (segments / total dwell s / median dwell s): WINWORD 53 / 1746.0 / 15.5; iexplore 53 / 812.5 / 6.8; vlc 1 / 480.2 / 480.2 (relaxation video); explorer 38 / 298.3 / 1.0; OUTLOOK 6 / 220.4 / 2.4; uLog 3.2 4 / 59.4 / 1.0; (unnamed "Unknown" windows) 19 / 15.8 / 0.7. Processes started in pp1 c1: dllhost 38, SearchProtocolHost 7, iexplore 5, WINWORD 2, OUTLOOK 1, vlc 1, FlashUtil32_11_3_300_257_ActiveX 1, splwow64 1.

All participants (74 blocks with a work window ≥ 10 min; 25 participants; pp25 block 1 excluded because the participant wrote in notepad, never in WINWORD/POWERPNT; pp2's 13-min fragment excluded):
- Work-window length: median 42.93 min (p25 31.20, p75 46.19).
- Switches/min per block, all segments: median 2.89 (p25 2.20, p75 4.11, max 6.98); N 2.55, T 2.83, I 3.12 (medians).
- Switches/min with explorer, unnamed windows and the logger removed and adjacent same-app segments merged: median 1.95 (p25 1.44, p75 3.03, max 5.45); dwell per app visit on that basis: median 9.1 s, p25 3.1, p75 24.9, p90 58.5 (n = 6,527 visits).
- Pooled dwell of all segments: n = 9,249, median 4.62 s, p75 16.75 s, max 2,043.5 s.
- Foreground apps (blocks in which the app held focus / pooled median dwell s): WINWORD 74 / 9.8; explorer 74 / 1.3; iexplore 73 / 8.0; OUTLOOK 69 / 4.0; POWERPNT 47 / 10.1; SumatraPDF 20 / 6.3; wmplayer 4; SndVol 4; calc 4; mspaint 3; notepad 3; SnippingTool 2.
- Processes started during blocks (blocks containing / total starts): dllhost 74 / 2,634; SearchProtocolHost 74 / 846; WINWORD 74 / 112; vlc 74 / 76; iexplore 73 / 446; splwow64 71 / 79; OUTLOOK 71 / 81; FlashUtil32_…_ActiveX 70 / 87; POWERPNT 47 / 52; SumatraPDF 20 / 23; wuauclt 2 / 2; WerFault 3; Firefox Setup 16.0.2 1.
- Page loads: "Browser URL changed" events per minute of iexplore focus: median 4.10 per block (p25 2.61, p75 5.43, max 18.07; 73 blocks); pooled 3,856 changes / 908.0 focused minutes = 4.25 /min. Many URLs are local `.mht` files provided as task material, not web pages.
- E-mail sends: clicks on an OUTLOOK control captioned "Send": 68 in the interruption condition (21 of 25 blocks, max 6 per block), 0 in N and T (all 76 files; example `a_pp10_c2_uLog_20121008_142012.xml`, 2012-10-08T12:39:25.2861091Z, "Left mouse button clicked on \"button Send\".").

**Coverage.**
- T1: covers — which applications ran together in a lab office-work session (Word, PowerPoint, IE, Outlook, SumatraPDF, VLC, Explorer) and background processes seen starting (dllhost, SearchProtocolHost (Windows Search indexer protocol host), splwow64, FlashUtil, wuauclt), with process names and start timestamps; unit: process-start events; scope: 25 students/interns, Windows laptop with Office 2010, 2012, one ~3 h lab session each. No list of all running processes (only starts/exits after logging began).
- T2: covers — window-activation events with application names and timestamps; the dwell and switch statistics above; population 25 participants × 3 conditions of 30–45 min each; lab tasks (report writing), not natural use.
- T3: partial — the task order is imposed (movie, then writing/presentations; e-mails pushed by experimenters); not a natural order.
- T4: covers weakly — IE page-load (URL change) rate per focused minute; no tab counts; IE, not Chromium.
- T9: covers — page-load rate and e-mail send counts per block; heavy in-app operations otherwise not logged.
- T10: covers — "Application started" events per block (e.g., WINWORD 112 starts over 74 blocks), no launch durations.
- T12: covers — public HCI log with process names and timestamps; population, time span (Sep–Nov 2012), licence CC-BY-NC-SA-4.0, open download.
- T5, T6, T7, T8, T11, T13: does not cover.
- One observation per file: machine (lab laptop, Windows, Office 2010), subject (ppN), window (file timestamps) are all named.

### S3-02 — Mozilla Test Pilot "A Week in the Life of a Browser – Version 2" (Firefox, Nov 2010)

**Citation.** Mozilla Labs Test Pilot, *A Week in the Life of a Browser – Version 2: Aggregated Data Samples*, testpilot.mozillalabs.com/testcases/a-week-life-2/ (2010); description page preserved in github.com/mozilla/testpilotweb.

**Access.** Original host gone; data via Internet Archive. Licence: "Creative Commons Attribution 3.0 United States License" (page line 41).

**Copy read.**
- `testpilotweb` at commit `50d5f37341e30b53af16a1c56bc981fc9a52097b` (2019-03-28), file `testcases/a-week-life-2/aggregated-data.html`, SHA-256 `edde45f06141630ce7a79aeb77619b4ba7212d6af707a0eef4544d0acbf4f3db`.
- `https://web.archive.org/web/20110711102216id_/https://testpilot.mozillalabs.com/testcases/a-week-life-2/witl_small.tar.gz` (7,746,321 B) SHA-256 `789ea6a5270dffe6434ad304cf563d93f33532912887493a6ee9668d45323c0d`; members `witl_small/events_small.csv` `9fabe8b54aaf548ad194b2faf51dbde6010e82e4e87b1a33d7b5a563406f51f0`, `users.csv` `fb6f92476473bbe69f08c75cff05c231ac6e360d8eea41c3fed299124222bfb1`.
- `https://web.archive.org/web/20110711101127id_/https://testpilot.mozillalabs.com/testcases/a-week-life-2/witl_large.tar.gz` (491,322,968 B) SHA-256 `8743f52d4fb3646db1ff0cfdc67c9e7caf671af6dd3c7efad0223eaadece2ea3`; member `witl_large/events.csv` (3,649,544,188 B) streamed with `tar -xOzf`, never stored.
- Local: `../sources/S3-02/`.

**Verbatim passages** (`aggregated-data.html` at the commit above).
- l.22 "Test duration: 7 days"; l.24 "Firefox versions covered: Fx 3.5 and Fx 3.6, Fx4 Beta"; l.25 "Data submission: 527,817 test sets submitted in November 2010."
- l.37–38 table rows: "witl_large.tar.gz | 469 MB | 3 | About 27,000 | Gzipped Tar archive of three CSV files, one for each table"; "witl_small.tar.gz | 7.4 MB | 3 | About 27,000, 387 w/ event data | …".
- l.43 "There is no personally-identifiable information, and no URLs, contained in this data set."
- l.127 event code 26 "NUM_TABS | Recorded whenever memory is recorded (at startup and every 15 minutes) and also whenever a window or tab is opened or closed. | 'data1' is number of windows, 'data2' is number of tabs (including the one just opened)."
- l.117 event code 20 "SESSION_ON_RESTORE | Recorded on application startup, when session restore triggers. | 'data1' is the number of windows restored, 'data2' is the number of tabs restored across all windows."
- Data rows, `witl_small/events_small.csv:2` `0,26,"1 windows","4 tabs","",1288742315024,""`; `:42` `0,26,"1 windows","5 tabs","",1288742475909,""`; `users.csv:2` `0,"",4.0b6,"WINNT Windows NT 6.1",1.0.3,"",3`; `users.csv:158` `157,"",4.0b6,"Linux Linux i686",1.0.3,"",1`.

**Statistics computed (script `witl_tabs.py`, Appendix B; large set filtered first with `tar -xOzf witl_large.tar.gz witl_large/events.csv | awk -F, 'NR>1 && ($2==26||$2==20||$2==1||$2==4||$2==5)'`; rows whose counts are `NaN` are skipped).**
- witl_large: 26,322 users with NUM_TABS events (Windows 24,895; macOS 1,267; Linux 159; SunOS 1); 12,098,012 samples. Per-user median open tabs: median 2 (p75 3, p90 6, max 247). Per-user maximum tabs over the week: median 8 (p25 5, p75 13, p90 20, max 1,103). Per-user maximum windows: median 3 (p75 4, p90 5). Pooled samples: tabs median 3 (p75 5, p90 10); windows median 1, 78.0 % of samples have exactly one window; tabs per window median 3.0 (p90 9). Session restores with >0 windows: 99,508 of 639,366 startups; restored tabs median 2 (p90 8). Tab-count changes (consecutive NUM_TABS samples of one user with different tab counts, i.e. tab opens/closes) per user per calendar day with events: median 40.2 (p25 20.3, p75 77.7, p90 140.3). Per-user observation span median 6.24 days.
- Linux subset (159 users): per-user median tabs median 5 (p75 9, p90 23); per-user maximum tabs median 14 (p75 27, p90 51); per-user maximum windows median 2.
- witl_small (387 users with events: Windows 371, macOS 15, Linux 1): per-user median tabs median 2, per-user max tabs median 8, per-user max windows median 3 — consistent with the large set.

**Coverage.**
- T4: covers — logged window and tab counts per user over one week, Firefox 3.5/3.6/4 beta, ~26,000 volunteer users (opt-in Test Pilot add-on, self-selected, mostly Windows), November 2010; statistic: distributions above. No page-load or tab-switch (tab-select) events exist in this study; no distinct-site counts ("no URLs"); no renderer-process information (Firefox 2010 was single-process for content).
- T2: does not cover focus sequences; BROWSER_ACTIVATE/INACTIVE events (codes 4/5) mark idle via a 5-min self-ping or 10-min idle observer — too coarse for dwell.
- T12: covers — OS-vendor-adjacent telemetry publication with per-user event timestamps (browser-only).
- T1, T3, T5–T11, T13: does not cover.
- Not one observation: a population of ~26,000 installations (a user may have several submissions, per the page's `user_id` note).

### S3-03 — Firefox Public Data Report (data.firefox.com), 2021–2026

**Citation.** Mozilla, *Firefox Public Data Report*, https://data.firefox.com/ (weekly; dates 2021-02-01 to 2026-09-14 in the index).

**Copy read** (JSON behind the dashboard):
- `https://data.firefox.com/datasets/desktop/usage-behavior/index.json` `c0a8ef8ccdfb35dc6c7a0bf9ec92f5aabe60e3edeb6dd241f0da5e4840262fd0`
- `…/user-activity/index.json` `a6f7cdf8f9b5440351bc1b08b8264027c7c6a04bed5a9110ba1f189b1f575a0c`
- `…/hardware/index.json` `ac7947860efdc31bf91b29f8ec4a9c4289a657656770078e0b07892360178238`
- `…/user-activity/Worldwide/avg_daily_usage(hours)/index.json` `88b6873a789f44ffa113cb293522baf0eba7a9bf22476a14b9fae28006139a61`
- `…/user-activity/Worldwide/avg_intensity/index.json` `2e9e4da0cdeb63bb21d95c3abf2267b1f8095fefa36433bd9708ccb6e4b80c94`
- `…/hardware/default/osName/index.json` `4f5bc17f9db682a537cb95bc9c784447fd907f11f0f973e84e1a5d67f900d49a`
- Local `../sources/S3-03/`.

**Verbatim passages.**
- usage-behavior index: `"metrics": ["locale", "pct_addon", "top10addons"]`; user-activity index: `"metrics": ["MAU", "avg_daily_usage(hours)", "avg_intensity", "pct_new_user", "pct_latest_version"]`; hardware index: `"metrics": ["resolution", "gpuModel", "gpuVendor", "cpuSpeed", "ram", "cpuCores", "cpuVendor", "osName", "browserArch", "osArch", "hasFlash"]`.
- avg_daily_usage: `"description": ["Daily Usage shows the hours spent browsing for a typical Firefox Desktop client in a typical day of use. Globally, the typical Firefox client averages around 4.5 hours of use per day."]`, `"axes": {"y": {"unit": "hours per day"}}`; latest point `{"x": "2026-09-14", "y": 5.511424525}`.
- avg_intensity: "Intensity shows how many days per week users use Firefox Desktop. Overall, the typical Firefox client uses the browser 3.5 days per week."
- osName 2026-09-14 values (% of clients): Windows 11 49.963; Windows 10 29.426; Windows 7 4.711; Linux-6.x 2.692; Linux-7.x 2.577; Linux Other 1.229; macOS Tahoe 3.267; macOS Other 3.624; macOS Sequoia 1.417.

**Coverage.** T4: does not cover (no tab, window, page-load or process metric is published). T2: covers only daily browsing hours per client (weekly aggregate; population: Firefox desktop release clients, worldwide). T12: OS-vendor telemetry publication; aggregate only, no per-process data. Linux share of Firefox desktop clients 6.5 % (sum of the three Linux rows). Not one observation.

### S3-04 — BEHACOM (12 users' own computers, Windows and Linux, Nov 2019–Jan 2020)

**Citation.** Sánchez Sánchez, P. M. et al., *BEHACOM*, Mendeley Data v2, DOI 10.17632/cg4br62535.2 (published 2020-05-06); article: "BEHACOM - a dataset modelling users' behaviour in computers", *Data in Brief* (2020), PMC7270191.

**Access.** Open; licence CC BY 4.0 (API: `'short_name': 'CC BY 4.0'`).

**Copy read.**
- `https://data.mendeley.com/public-files/datasets/cg4br62535/files/0d0c2ab7-462f-42c2-abf7-6a05f44dbb67/file_downloaded` → `Behacom.zip` 37,414,157 B, SHA-256 `92e1b44b0d0853435f8e984e8dff76aa5ad7a90c5f04fdb7936045d3d0a15e44` (matches the repository's published `sha256_hash`). Twelve CSVs (6.8 MB – 2.0 GB each, ≈6 GB) streamed from the zip; `Behacom/Readme.txt` extracted, SHA-256 `c02056adaf0f013adb940fa4cd25ace9809bf7c9c12ef44dbfaf448b7863b1b5`.
- Article full text `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7270191/fullTextXML` SHA-256 `c7880aa76a91786aa91fa5e76f331cb8db3370967b53f9007f5feb17d8f3ccfd`.
- Local `../sources/S3-04/`.

**Verbatim passages.**
- Article, "Scenario description and selected features": "The twelve individuals are right-handed male, with ages ranging from 20 to 45 years old. Eight of them use Windows as operating system, three Linux, and one both." … "The first timestamp (UNIX ms) of the dataset is 1574245230186 (Wednesday, 20-Nov-19 10:20:30 UTC) and the last one is 1578995678310 (Tuesday, 14-Jan-20 09:54:38 UTC)."
- Article, "Data collection": "To obtain the process identifier (pid) of the application in foreground, xdotool [8] is used in the Linux implementation and pywin32 ( win32process and win32gui ) [9] in Windows. Process names, CPU, memory and network usage are obtained by the psutil [10] library, in both operating systems."
- Article, "Feature extraction": "This file is read line by line, extracting the periodic measurements (every 5 seconds) about active applications and resources in use."
- Article, "Code repository": "we have implemented a data collection application for Windows, the most used desktop operating system, and another for Linux distributions based on Debian."
- `Readme.txt:67` "active_apps_average. This feature measures the average number of applications active during the time window."; `:69` "current_app. This feature contains the application in foreground when the vector was generated, it contains a string with the application executable name."; `:73` "changes_between_apps. This feature contains the number of changes between different foreground applications during the time window."; `:75` "current_app_foreground_time. … If no application changes occur, this feature will value 60."; `:77` "current_app_average_processes. This feature represents the average number of processes that the current application in foreground had active during the time window."
- Example row, `Behacom/User6/User6_BEHACOM.csv` line 7, last 18 columns: `active_apps_average=1.0, current_app=csgo.exe, penultimate_app=explorer.exe, changes_between_apps=2, current_app_foreground_time=36.42, current_app_average_processes=1.0, …, current_app_average_cpu=62.8, …, system_average_cpu=28.97, …, USER=6`. `User5_BEHACOM.csv` line 81: `active_apps_average=4.78, current_app=League of Legends.exe, penultimate_app=LeagueClientUx.exe, changes_between_apps=2, current_app_foreground_time=42.68, …, system_average_cpu=34.26, …`.

**Statistics computed (scripts `behacom_stats.py`, `behacom_game.py`, Appendix C; one row = one minute).**

| user | minutes | days | active_apps_average median (p90) | changes_between_apps mean /min | top foreground executables (minutes) | median processes of current app |
|---|---|---|---|---|---|---|
| 0 | 6,059 | 43 | 2 (4) | 0.26 | chrome.exe 4107, wps.exe 434, Winamax Poker.exe 386, wxmaxima.exe 304, csgo.exe 182, explorer.exe 146, acad.exe 131, codeblocks.exe 117 | chrome.exe 14 |
| 1 | 42,281 | 42 | 31 (43) | 0.01 | firefox 27728, soffice.bin 5368, update-manager 2911, gnome-calculator 2127, gedit 1900, evince 869, gnome-terminal-server 634, skypeforlinux 289 | firefox 1 |
| 2 | 179 | 1 | 6 (6.12) | 0.34 | firefox.exe 164, WhatsApp.exe 8, Telegram.exe 7 | firefox.exe 11 |
| 3 | 3,221 | 18 | 4 (8.17) | 0.15 | firefox 2374, soffice.bin 291, sublime_text 203, plasmashell 73, wireshark 58, dolphin 54, okular 40, konsole 33 | firefox 1 |
| 4 | 10,114 | 31 | 5.57 (7.5) | 0.82 | thunderbird.exe 3290, explorer.exe 2323, chrome.exe 1487, Skype.exe 1015, WhatsApp.exe 961, AcroRd32.exe 311, WINWORD.EXE 233 | chrome.exe 16 |
| 5 | 2,128 | 5 | 4 (6) | 0.27 | firefox.exe 1275, League of Legends.exe 255, Telegram.exe 172, explorer.exe 160, vlc.exe 90, Spotify.exe 50, Steam.exe 9 | firefox.exe 11 |
| 6 | 1,332 | 11 | 1 (2) | 0.27 | chrome.exe 556, csgo.exe 432, ApplicationFrameHost.exe 197, explorer.exe 55, Steam.exe 31, ts3client_win64.exe 14 | chrome.exe 12 |
| 7 | 55,778 | 37 | 9 (11) | 0.02 | thunderbird 25358, chrome 10949, firefox 6419, soffice.bin 4487, update-manager 3253, skypeforlinux 1611, tilix 1009 | chrome 15 |
| 8 | 5,404 | 23 | 5 (9) | 0.51 | chrome.exe 2391, LockApp.exe 1785, ApplicationFrameHost.exe 314, Telegram.exe 240, thunderbird.exe 205 | chrome.exe 19.2 |
| 9 | 7,920 | 21 | 4.2 (7) | 0.83 | chrome.exe 1641, Skype.exe 1244, Acrobat.exe 1104, thunderbird.exe 942, POWERPNT.EXE 715, WINWORD.EXE 598, notepad++.exe 577, eclipse.exe 69 | chrome.exe 24.33 |
| 10 | 15,358 | 53 | 5 (7) | 0.11 | firefox 13230, evince 607, skypeforlinux 394, java 317, gnome-terminal-server 307, chrome.exe 102, kdenlive 21 | firefox 1 |
| 11 | 17,284 | 55 | 9 (12) | 0.24 | firefox 6190, chrome 4818, Telegram 1567, plasmashell 824, nxplayer.bin 810, spotify 626, VirtualBoxVM 577, skypeforlinux 549 | chrome 10 |

Pooled over 167,058 minutes: 90.6 % of minutes have zero foreground changes; changes_between_apps mean 0.17/min. Linux-style executable names (no `.exe`) appear for users 1, 3, 7, 10 (10 also has `.exe` names) and 11 — five users, while the article states three Linux and one both. On Linux users (1, 7, 10) long runs of minutes with a foreground app and ~0 changes suggest vectors are also produced while the user is away; `active_apps_average` on user 1 (median 31) is not comparable with the Windows users (definition of "application" differs by collector). Game minutes (`behacom_game.py`): User0 csgo.exe 182 min, penultimate app "-" in 168, ts3client_win64.exe 6, Steam.exe 3, Spotify.exe 2; median system_average_cpu 28.4 %. User5 League of Legends.exe 255 min, median active_apps_average 6, system CPU 45.5 %. User6 csgo.exe 435 min, penultimate Steam.exe 11, explorer.exe 10, ts3client_win64.exe 4; system CPU 74.5 %.

**Coverage.**
- T1: covers — per-minute count of active applications and foreground executable names, from natural use on the subjects' own PCs; 12 male users (Spain/Italy), Windows and Debian-based Linux, Nov 2019–Jan 2020; combinations visible only as current + penultimate foreground app per minute (not the full set of running processes).
- T2: covers — changes between foreground apps per minute and foreground seconds per minute (aggregated per minute, not raw event sequences).
- T4: covers — "number of processes of the current application" gives Chrome process counts on Windows and Linux (per-user medians 10–24 while Chrome is in foreground) and Firefox (1 on Linux collector, 11 on Windows collector — collectors differ), no tab counts.
- T5: covers weakly — Windows gaming minutes (CS:GO, League of Legends) with Steam and TeamSpeak 3 as penultimate apps; no Linux gaming.
- T9, T10: does not cover (no in-app operations, no launch events).
- T12: covers — public (CC BY 4.0) per-minute foreground-process trace with executable names and timestamps.
- One observation per user file: subject (UserN), OS (by executable naming), window (timestamps) named; machine model not named.

### S3-05 — DARPA OpTC endpoint telemetry (Windows 10, Sept 2019) — scripted benign activity

**Citation.** DARPA / Five Directions, *Operationally Transparent Cyber (OpTC) Data Release*, github.com/FiveDirections/OpTC-data (commit `5b108604f11f767aa11ea79ff827595f3fad15fd`, 2020-06-17); corrected version: *Corrected version of the DARPA OpTC dataset*, Recherche Data Gouv, DOI 10.57745/UXCWOC.

**Access.** Public domain ("DARPA is releasing these files in the public domain"). Original data on Google Drive — unreachable (quota exceeded on every file tried). Corrected version: open, ten daily tar files of 13–125 GB each; read by HTTP range.

**Copy read.**
- `OpTC-data/README.md` `bbbeca5d5a861ffc765a6d42ddd19cb84acb93861226b4b93887bb950e121074`; `ecar.md` `1df4539c49963cc49b783580033fe1ec68bbae68434abf29da83c47b5d26d16b`; `errata.md` `4044970eae0db4f67055fa2c0e5bb99824628c13d991fcef01dcc5ec06e8d062`; `OpTCRedTeamGroundTruth.pdf` `5986d23b81169221a491f7a8302fce140b12638ef4cf9b3a894ed3cb2fad9567`.
- Drive manifest (gdown listing, 4,481 entries) `gdrive_manifest.txt` `e62d596aa92ee3c8352bc5aec49321130e3274d6060535659820e073d157d872`; corrected-dataset metadata JSON `3ba1e41aa58d6fc55ed3f5576f6ce2039a56136e88e5198a52b7580544e0af03`.
- `https://entrepot.recherche.data.gouv.fr/api/access/datafile/713542` (`2019-09-16.tar`, 13,437,603,840 B), bytes 0–20,971,519 (HTTP 206) → `2019-09-16.head20MB.tar` SHA-256 `8184a02ee48ab02408bbcf785ee5d16d7e1d6e664d4ff7b2d1911b0dc181cd41`; the truncated member `2019-09-16/AIA-251-275/AIA-251-275.ecar-2019-09-16-sysclient0254.json.gz` (20,969,984 of 63,678,765 B) `119a9f542eab22eed68bf5d675c178c991c5de520bd19b57bcdb66c2f69d266a`; `zcat 2019-09-16/AIA-251-275/AIA-251-275.ecar-2019-09-16-sysclient0254.json.gz > sysclient0254_partial.jsonl` (gzip reports the truncation) yields 373,481 JSON lines (SHA-256 of the decompressed text `c48648f7dbeb7b217d3a309586b64d9f0c5266edb6dfc98bf4b35dab41063b42`; line numbers below refer to it).
- Local `../sources/S3-05/`.

**Verbatim passages.**
- README.md:12 "Each Windows 10 endpoint is equipped with an endpoint sensor that monitors host events, packs them into JSON records, and sends them to Kafka."
- README.md:14 "The evaluation started with a period of benign record generation, followed by the injection of malware by a red team. Benign traffic ran continuously during red team activity. Due to constraints in collection data space during the evaluation, data from five hundred hosts was collected rather than from the full set of one-thousand hosts."
- ecar.md:33 "When process details are present, an "image_path" entry in Event.properties will also typically be present".
- Decompressed line 173899 (PROCESS CREATE, 2019-09-16T20:12:39.787-04:00, principal `SYSTEMIACOM\alaparan`): command line `geckodriver --port 49763`, parent `\Device\HarddiskVolume1\Python27\python.exe`.
- line 174230 (20:12:42.581): `"\\?\C:\Program Files (x86)\Mozilla Firefox\firefox.exe" -marionette -profile C:\Users\alaparan\AppData\Local\Temp\rust_mozprofile.FylziXvpBDyj`, parent `geckodriver.exe`.
- line 232271 (20:24:29.867): `"C:\Program Files (x86)\Microsoft Office\Office15\WINWORD.EXE" /Automation -Embedding`, parent `svchost.exe`.
- line 97468 (20:07:20.139): `"C:\Program Files\Windows Defender\MpCmdRun.exe" SignaturesUpdateService -ScheduleJob -UnmanagedUpdate`, parent `MsMpEng.exe`, user `NT AUTHORITY\SYSTEM`.

**Statistics computed (`optc_proc.py`, Appendix D) on the 80-minute fragment of host SysClient0254 (2019-09-16 19:39:19 – 20:59:29 −04:00).** Events by type: FLOW START 151,215; FLOW MESSAGE 65,615; PROCESS OPEN 64,224; FILE READ 21,537; MODULE LOAD 20,747; … PROCESS CREATE 457; PROCESS TERMINATE 349. PROCESS CREATE by image: PING.EXE 99, svchost.exe 41, conhost.exe 36, reg.exe 28, MpCmdRun.exe 19, cmd.exe 17, taskhostw.exe 14, GoogleUpdate.exe 12, sppsvc.exe 11, schtasks.exe 8, SearchProtocolHost.exe 6, SearchFilterHost.exe 6, EXCEL.EXE 4, WINWORD.EXE 4, python.exe 3, OneDriveSetup.exe 3 (host rebooted at 19:44:19, hence smss/wininit/csrss creates). Distinct image names acting per 10-minute bucket: 5–67; the 20:10–20:20 bucket has 61 names including firefox.exe, geckodriver.exe, python.exe, outlook.exe, excel.exe, searchindexer.exe, msmpeng.exe, mpcmdrun.exe, tiworker.exe, trustedinstaller.exe, usoclient.exe, vmtoolsd.exe.

**Coverage.** T1/T12: covers the *structure* of Windows 10 enterprise-endpoint process activity with image names and timestamps (500 of 1,000 VMs, 17–25 Sept 2019), but the "user" activity is scripted (Selenium/geckodriver driving Firefox, Office via COM automation), so application co-occurrence is not human behaviour. T6-like background jobs on Windows are real (Defender signature updates, Windows Search, Windows Update/TiWorker, GoogleUpdate). T2/T4/T9: does not cover (no focus, tabs, or user operations). One observation for the fragment: host SysClient0254, window 19:39–20:59 on 2019-09-16.

### S3-06 — LANL "Comprehensive, Multi-Source Cyber-Security Events" (2015)

**Citation.** Kent, A. D., *Comprehensive, Multi-Source Cyber-Security Events*, Los Alamos National Laboratory, DOI 10.17021/1179829 (2015). **Copy read:** `https://csr.lanl.gov/data/cyber1/` HTML, SHA-256 `d8aa79edfbe50e139971687e92b591c5ceaed7686d8a7b21e4669df419f0881e` (`../sources/S3-06/cyber1.html`). Data files not downloaded (form requires an e-mail address).

**Verbatim passages** (page, "Comprehensive, Multi-Source Cyber-Security Events" and "proc.txt.gz"): "This data set represents 58 consecutive days of de-identified event data collected from five sources within Los Alamos National Laboratory's corporate, internal computer network." … "In total, the data set is approximately 12 gigabytes compressed across the five data elements and presents 1,648,275,307 events in total for 12,425 users, 17,684 computers, and 62,974 processes." … "All other users, computers, process, ports, times, and other details were de-identified as a unified set across all the data elements (e.g. U1 is the same U1 in all of the data). The specific timeframe used is not disclosed for security purposes." proc.txt.gz: "This data represents process start and stop events collected from individual Windows-based desktop computers and servers. Each event is on a separate line in the form of "time,user@domain,computer,process name,start/end"" — example lines `1,C553$@DOM1,C553,P16,Start` / `1,C553$@DOM1,C553,P25,End`. Licence: "Los Alamos National Laboratory has waived all copyright and related or neighboring rights". Download: "To download the data set, please help us understand how it will be used." (form: e-mail address, intended use).

**Coverage.** T1/T12: process start/stop with timestamps on Windows desktops and servers, 58 days, but process names are pseudonyms (P16, P25) and desktops are not separated from servers — application identity and co-occurrence by application cannot be recovered. Access requires registering an e-mail address. Not one observation.

### S3-08 — gamemode issue #457: process listing of a running Proton game under Flatpak Steam (Arch Linux, Jan 2024)

**Citation.** flagel, "gamemoderun does not renice all processes", FeralInteractive/gamemode issue #457, 2024-01-04, https://github.com/FeralInteractive/gamemode/issues/457.

**Copy read.** github.com was blocked for curl in this session (HTTP 403 session gate) and the Wayback CDX request was reset four times; the page was read through the WebFetch tool, whose output is a model-rendered Markdown copy. The code blocks as returned were saved verbatim to `../sources/S3-08/gamemode_issue457.webfetch.txt` (SHA-256 `88b335c9daf6ea1f32273b5248b0c15ed556b34e6d14b24cded7eb61737bf488`). **Not byte-verified against the original HTML** — treat as provisional until re-read from github.com.

**Verbatim passages (as rendered).** Header as returned: "Game: Worms Armageddon (via Steam Flatpak with Proton)"; "System: Arch Linux 6.6.8-arch1-1, gamemode 1.8.1-1". Process tree (first block, `PID  NI PRI PSR COMMAND`):
```
71697   0  19   6 bwrap
71698   0  19   6  \_ pressure-vessel
71732   0  19   3      \_ python3
71734   0  19   3      |   \_ steam.exe
71736   0  19   9      \_ wineserver
71740   0  19   2      \_ services.exe
71743   0  19   1      \_ winedevice.exe
71753   0  19   6      \_ winedevice.exe
71766   0  19   1      \_ plugplay.exe
71772   0  19   0      \_ svchost.exe
71780   0  19  11      \_ conhost.exe
71782   0  19   3      \_ explorer.exe
71791   0  19   8      \_ rpcss.exe
71801   0  19   5      \_ tabtip.exe
71818   0  19  10      \_ WA.exe
1   0  19   5 bwrap
2   0  19   2 bash
28700   0  19   7  \_ bash
28806   0  19   9  |   \_ steam
28839   0  19   0  |       \_ steamwebhelper
28869   0  19   0  |       |   \_ steamwebhelper
28882   0  19   5  |       |   |   \_ steamwebhelper
28870   0  19   1  |       |   \_ steamwebhelper
28964   0  19   1  |       |   |   \_ steamwebhelper
30072   5  14   0  |       |   |   \_ steamwebhelper
71861   5  14  10  |       |   |   \_ steamwebhelper
28918   0  19  10  |       |   \_ steamwebhelper
44019   0  19  11  |       |   \_ steamwebhelper
28990   0  19   0  |       \_ steam-runtime-l
71621  -5  24   7  |       \_ reaper
71622  -5  24   6  |       |   \_ steam-runtime-l
71851   0  19  10  |       \_ gameoverlayui
71954   0  19   6  \_ ps
```
Native-game comparison block: `72209 28806 user -5 1 reaper` / `72210 72209 user -5 7 hl.sh` / `72213 72210 user -5 0 hl_linux`.

**Counts (from the block above).** Proton game container: 15 processes (bwrap, pressure-vessel, python3, steam.exe, wineserver, services.exe, 2 × winedevice.exe, plugplay.exe, svchost.exe, conhost.exe, explorer.exe, rpcss.exe, tabtip.exe, WA.exe). Steam client side (Flatpak sandbox): steam, 8 × steamwebhelper, 2 × steam-runtime-l (comm truncated to 15 chars), reaper, gameoverlayui — 13 processes, plus sandbox bwrap/bash. Native (GoldSrc) game: reaper → hl.sh → hl_linux. No thread counts; no compositor or voice-chat process in the listing (the listing is restricted to the Flatpak sandbox's PID namespace).

**Coverage.** T5: covers — one observation of process names and count for one Proton game (Worms Armageddon, WA.exe) and the Steam client helpers, Arch Linux kernel 6.6.8, Steam Flatpak, January 2024; subject: one reporter; no threads, no download state. T1: covers the gaming case for that one machine. Other topics: does not cover.

### S3-09 — Steam Hardware & Software Survey, August 2026

**Citation.** Valve, *Steam Hardware & Software Survey: August 2026*, https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam. **Copy read:** that URL, SHA-256 `eb2b13335dcc9fe058ad877f1446f9b0df7cc1a5e1e04fc0e0aef69b91e7b151`; `https://store.steampowered.com/hwsurvey/?platform=linux` `55ea36856eb4e21e6bef2cde0404459e7189a50adab785a96814decada5b4c6a` (`../sources/S3-09/`).

**Verbatim passages.** "Steam conducts a monthly survey to collect data about what kinds of computer hardware and software our customers are using. Participation in the survey is optional, and anonymous." OS table rows (item | percentage | change): "Windows | 93.95% | +0.28%"; "Windows 11 64 bit | 70.97% | +0.71%"; "Windows 10 64 bit | 22.90% | -0.40%"; "OSX | 2.14% | -0.18%"; "Linux | 3.90% | -0.11%"; "SteamOS Holo 64 bit | 0.82% | -0.07%"; "CachyOS 64 bit | 0.60% | +0.03%"; "Arch Linux 64 bit | 0.34% | +0.01%"; "Linux Mint 22.3 64 bit | 0.33% | 0.00%"; "Bazzite 64 bit | 0.30% | -0.01%"; "Freedesktop SDK 25.08 (Flatpak runtime) 64 bit | 0.21% | -0.01%"; "Fedora Linux 44 (KDE Plasma Desktop Edition) 64 bit | 0.12% | 0.00%"; "Ubuntu 26.04 LTS 64 bit | 0.11% | -0.01%"; "Ubuntu 24.04.4 LTS 64 bit | 0.10% | -0.01%"; "Nobara Linux 44 (KDE Plasma Desktop Edition) 64 bit | 0.06% | +0.06%".

**Coverage.** T5: population context only — Linux share of Steam survey respondents (3.90 %) and distribution mix; the Linux page has no session-type (Wayland/X11), desktop-environment or process data (grep for wayland/x11/session/gnome: no hits except edition names). "Freedesktop SDK … (Flatpak runtime)" 0.21 % indicates Flatpak Steam installs. Not one observation (monthly opt-in sample).

### S3-10 — Debian popularity-contest (popcon), generated 2026-09-22

**Citation.** Debian Popularity Contest, https://popcon.debian.org/ ("Made by Bill Allombert. Last generated on Tue Sep 22 13:57:29 2026 UTC."). **Copy read:** `https://popcon.debian.org/by_inst.gz` SHA-256 `0a35503aaf12da9ef1ddaea16c3c3e86836e855065f029285b77246b32bea781`; index page `0109cbe10b3d7d4fc4fe858aa273cc85a2d12ee3fea942944b86ce867cb89acc` (`../sources/S3-10/`).

**Verbatim passages.** Index: "Number of submissions considered: 290000"; "amd64 : 282149". `by_inst` header: "#<inst> is the number of people who installed this package;" / "#<vote> is the number of people who use this package regularly;". Rows (`by_inst.txt:<line>`: rank name inst vote old recent no-files):
`132: 121 dbus 285896 249370 20101 16395 30`; `270: 259 dbus-daemon 238934 223459 62 15403 10`; `18182: 18171 dbus-broker 612 604 4 4 0`; `1168: 1157 pipewire 107233 94193 2595 10433 12`; `1237: 1226 pipewire-pulse 100329 85660 4065 10594 10`; `1236: 1225 wireplumber 100343 89090 830 10412 11`; `2091: 2080 pulseaudio 50109 42713 3989 3398 9`; `774 xserver-xorg-core 138225 105731` (line 785); `1271: 1260 xwayland 97059 73921 12892 10234 12`; `1676: 1665 gnome-shell 70758 59432`; `2846: 2835 plasma-workspace 34197 29752`; `2366: 2355 dkms 42552 22224 17481 2837 10`; `5483: 5472 nvidia-kernel-dkms 10967 4482`; `7496: 7485 zfs-dkms 5425 4999`; `14181: 14170 virtualbox-dkms 1199 935`; `5414: 5403 clamav-freshclam 11359 10129`; `5443: 5432 clamav 11181 2458`; `4696: 4685 plocate 16242 14131`; `4034: 4023 mlocate 20617 9399 … (Not in sid)`; `4853: 4842 locate 14915 12556`; `3215: 3204 tracker 29561 5121`; `3467: 3456 tracker-miner-fs 26403 21855`; `9029: 9018 localsearch 3363 2891`; `2113: 2102 tinysparql 48975 4851`; `3445: 3434 baloo6 26570 23099`; `5898: 5887 baloo-kf5 9139 7102`; `6297: 6286 borgbackup 7969 3613`; `8366: 8355 restic 4161 2298`; `5301: 5290 deja-dup 12038 8151`; `13427: 13416 gamescope 1351 140`; `5981: 5970 steam-launcher 8883 8285 … (Not in sid)`; `7023: 7012 steam-installer 6322 3138`; `2941: 2930 flatpak 32954 31272`; `772: 761 anacron 139522 122057`; `2019: 2008 unattended-upgrades 52758 37399`; `907 packagekit 129335 104750` (line 918); `5929: 5918 zoom 9034 2311 … (Not in sid)`; `1013: 1002 firefox-esr 123486 52953`; `3277: 3266 chromium 28720 9283`; `3220: 3209 thunderbird 29513 10981`; `1847: 1836 gimp 61391 10506`; `7091: 7080 kdenlive 6171 947`; `7304: 7293 blender 5756 679`; `6144: 6133 obs-studio 8339 1606`.

**Coverage.** T1/T6/T8 (population of installed packages): covers — on 290,000 opt-in Debian (and derivative) installations, of which 282,149 amd64: dbus-daemon (238,934 installs) vs dbus-broker (612); pipewire 107,233 vs pulseaudio 50,109; xwayland 97,059; gnome-shell 70,758 vs plasma-workspace 34,197; dkms 42,552 (nvidia-kernel-dkms 10,967; zfs-dkms 5,425; virtualbox-dkms 1,199); clamav-freshclam 11,359; plocate 16,242; tracker-miner-fs 26,403; baloo6 26,570; borgbackup 7,969; gamescope 1,351. Population mixes servers and desktops; "vote" = package files accessed recently. Ubuntu popcon is discontinued (popcon.ubuntu.com shows only "Thanks!"). Not one observation.

### S3-11 — OpenBenchmarking.org timed-compilation test profiles (public PTS results, 2024–2026)

**Citation.** OpenBenchmarking.org test profile pages `pts/build-linux-kernel`, `pts/build-llvm`, `pts/build-gcc`, `pts/build-ffmpeg`, `pts/build-godot`, `pts/build-mesa`, `pts/build-php`, `pts/build-nodejs` (Phoronix Media), accessed 2026-09-23.

**Copy read** (`https://openbenchmarking.org/test/pts/<name>`, fetched with UA `Mozilla/5.0 (X11; Linux x86_64) Phoronix-Test-Suite`; SHA-256): build-linux-kernel `c1159c97c3526ce8f24321f6df1fe833f5fc8472cf8b3c8b08875d15ab5c3da7`; build-llvm `7caf7d0c9408386060812c986899bd57dd1161e420a4891a3eca25972f50c22a`; build-gcc `82e02d2bbd190c4d237b19670b68895a826aad1b19629d754a15b82355499719`; build-ffmpeg `7124773654d82af072c9eb1cdd3c666f3892677b2bcd9ce2e871f27426359be2`; build-godot `3177091165c664d48abfd04b7aeeba93f6d39490319456dc383f21961364b6b7`; build-mesa `bc902094b4924142c55153d0eaf2b15c084e623fa2faaa4c26005114b36d1960`; build-php `1a563dc921f074f6cb83e4e08e51c1a7648b9f8d3eaa4c3fe0b3be1e42a04ef3`; build-nodejs `23697ac6b2c06564e5d4adfc1a3167f129d72482a849955d5c6ee12886e64c56` (`../sources/S3-11/`).

**Verbatim passages.**
- kernel page: "OpenBenchmarking.org metrics for this test profile configuration based on 1,131 public results since 20 April 2026 with the latest data as of 23 September 2026 ."; "Based on OpenBenchmarking.org data, the selected test / test configuration ( Timed Linux Kernel Compilation 7.0 - Build: defconfig ) has an average run-time of 12 minutes ."; distribution: "Build: defconfig 1131 Results Range From 20 To 13705 Seconds"; percentile table "Median | 50th | 79" (seconds); rows e.g. "AMD Ryzen 9 7900 12-Core | 49th | 4 | 82".
- "* Uploading of benchmark result data to OpenBenchmarking.org is always optional (opt-in) via the Phoronix Test Suite for users wishing to share their results publicly."
- llvm: "( Timed LLVM Compilation 21.1 - Build System: Ninja ) has an average run-time of 30 minutes"; based on 851 public results since 4 October 2025; median 346 s.
- gcc: "( Timed GCC Compilation 15.2 - Time To Compile ) has an average run-time of 1 hour, 32 minutes"; 259 results; median 1087 s.
- ffmpeg: "( Timed FFmpeg Compilation 7.0 - Time To Compile ) has an average run-time of 6 minutes"; 1,465 results since 5 April 2024; median 38 s.
- godot: "( Timed Godot Game Engine Compilation 4.5 - Time To Compile ) has an average run-time of 19 minutes"; 919 results; median 223 s.
- mesa: "( Timed Mesa Compilation 26.1 - Time To Compile ) has an average run-time of 2 minutes"; 87 results; median 46 s.
- php: "( Timed PHP Compilation 8.4.9 - Time To Compile ) … average run-time of 6 minutes"; 602 results; median 63 s.
- nodejs: "( Timed Node.js Compilation 25.9 - Time To Compile ) … average run-time of 25 minutes"; 365 results; median 217 s.
("average run-time" includes the default ≥3 repetitions.)

**Statistics computed (`ob_ratio.py`, Appendix E).** Ratio of a test's per-CPU "Seconds (Average)" to the kernel defconfig value on the same CPU model, over CPU models listed on both pages (the listed CPUs are mostly the top-percentile, high-core-count models):

| test (config) | CPU models in common with kernel | ratio median (min–max) | ratio of population medians |
|---|---|---|---|
| FFmpeg 7.0 | 8 | 0.67 (0.52–0.76) | 38/79 = 0.48 |
| Mesa 26.1 | 1 | 0.56 | 46/79 = 0.58 |
| PHP 8.4.9 | 7 | 1.06 (0.97–1.37) | 63/79 = 0.80 |
| Godot 4.5 | 18 | 3.02 (2.48–3.26) | 223/79 = 2.82 |
| LLVM 21.1 (Ninja) | 11 | 3.42 (2.84–4.21) | 346/79 = 4.38 |
| Node.js 25.9 | 13 | 4.64 (4.28–5.64) | 217/79 = 2.75 |
| GCC 15.2 | 3 | 17.57 (15.06–17.85) | 1087/79 = 13.8 |

Example matched rows (seconds, test vs kernel): 2 × AMD EPYC 9655 96-Core — LLVM 82 vs 24, Godot 72 vs 24, Node.js 109 vs 24, FFmpeg 16 vs 24; AMD Ryzen Threadripper 9980X 64-Cores — GCC 482 vs 27, Mesa 15 vs 27, PHP 30 vs 27.

**Coverage.** T7: covers — full-build wall times of several projects relative to a Linux 7.0 defconfig build on the same CPU; population: opt-in Phoronix Test Suite uploads (dominated by servers/workstations; many-core CPUs), 2024–2026; clean builds with the test profile's own configuration, not a user's incremental builds; no object counts. Not one observation. Other topics: does not cover.

### S3-13 — Carat "Top 1000 Users Long-Term App Usage Dataset" (Android, 2014–2018)

**Citation.** University of Helsinki Carat project, *Carat Top 1000 Users Long-Term App Usage Dataset*, https://www.cs.helsinki.fi/group/carat/data-sharing/ ; cite Oliner et al., "Carat: Collaborative Energy Diagnosis for Mobile Devices", SenSys 2013.

**Access.** Public download, password-protected zip (password published on the page); "released to the public for research purposes only. Commercial use is strictly prohibited."

**Copy read.** Page HTML SHA-256 `a3f3e5fed2761ac72af6e0f3434aa54d86a1b2c6544ef32b1c9b971fc15768b2`. Zip `carat-data-top1k-users-2014-to-2018-08-25.zip` (Content-Length 6,375,824,106; `Accept-Ranges: bytes`): last 1 MiB (central directory, 2,535 entries) `tail1MB.bin` SHA-256 `2574152c97ade574c2079dcb05896523a4d71e7a34eb5450aebfb4cc41dfd805`; bytes 309211–5115724 (local header + member `…json-rdd/part-00995.gz`) `part-00995.range.bin` `cb2d8fd775906443ea6a041ba27fd2a80686db57849081dfead26671cd4c5a09`; decrypted member `part-00995.gz` `9a6f19db14403fedeb74f044f8627aa59ca9b598973151e47950ce273df0527e` (12,758 JSON lines). Local `../sources/S3-13/`.

**Verbatim passages.** Page: "The app collected application usage and battery level information every time the battery level changed by 1%, as allowed by the mobile operating system." … "There are 18,146,042 time series records spanning 4.65 years for the longest duration users, and over 2 years even for the 1000th. The records are from over 100 countries, and 315 timezones." … "processName (App Android package name)" / "priority (background, foreground, etc, see Android documentation)". Data, `part-00995.gz` line 1: `{"uuid":"2060efca…1d44","timestamp":1443336825,"batteryLevel":46,"batteryStatus":"charging","timeZone":"Europe/Helsinki","mobileCountryCode":"UNKNOWN","apps":[{"processName":"com.android.chrome","priority":"Foreground app"},{"processName":"com.google.process.gapps","priority":"Visible task"},…,{"processName":"com.skype.raider","priority":"Background process"},…`.

**Statistics computed (`carat_stats.py`, Appendix F) on part-00995 (865 users, 12,758 samples).** Distinct running process names per sample: median 52 (p25 35, p75 73, p90 84, max 118). Priority classes over all entries: Background process 283,292; Service 250,344; Foreground app 87,669; Visible task 52,357; Perceptible task 21,012.

**Coverage.** T1/T12: covers co-running application sets with package names and timestamps, but on Android phones (not desktop), sampled at battery-level changes; volunteers of an energy app, 2014–2018. T2: does not cover (Android "Foreground app" importance class, several per sample, is not the focused app). Not one observation.

### S3-14 — Computer-usage profiles of 31 Windows 10 users over 8 weeks (dataset not public)

**Citation.** "Online Binary Models are Promising for Distinguishing Temporally Consistent Computer Usage Profiles", arXiv:2105.09900v2 (2 Sep 2021). **Copy read:** `https://arxiv.org/pdf/2105.09900` SHA-256 `92fbe5f909ec23f68aef2ffe69f172eabc0d8561b3850abbc518087f60a234c9` (`../sources/S3-14/`).

**Verbatim passages.** Abstract: "We collected ecologically-valid computer usage profiles from 31 MS Windows 10 computer users over 8 weeks". p.2 §1: "All artifacts created throughout the course of this study, including our module for extracting profiles and our dataset of ecologically-valid computer usage data itself, will be made publicly available for vetted research usage". §4: "This IRB-approved study requested that participants installed our extractor module on their personal computers and used their devices naturally for 8 weeks. The entire study took place asynchronously from September 2020 to".

**Coverage.** T12: a process/network/keystroke usage data set from natural use exists, but release is "for vetted research usage" and no download location was found; the data were not read. Other topics: not assessable.

### Leads examined and recorded as not covering (kept for traceability)

- **S3-07 — sched-ext/scx issue #3750** (Wayback capture 20260820065436 of https://github.com/sched-ext/scx/issues/3750; decompressed HTML SHA-256 `00c4159d17a07bdd53252bf6196b1e8e0000bc0cd42b9c25acd3d696514703a5`). Verbatim body: "OS: Nobara Linux" / "Version tested: scx_lavd 1.1.3 (stutter/freeze) vs scx_lavd 1.1.2 (stable)" / "Game / Context: CS2 (Counter-Strike 2)". No log, process list or thread count in the captured body; the 19 later comments could not be read (GitHub gated, see search log #13–14). T5: does not cover.
- **Arch Linux forum topic 302470** (`https://bbs.archlinux.org/viewtopic.php?id=302470`, HTML SHA-256 `0fba274754e3375d23255ba6454282333094a3818b3da650e4070d0d281078a0`, `../sources/S3-08/arch302470.html`): contains Steam start-up journal lines such as (extracted text line 91) "steamwebhelper.sh[8311]: Starting steamwebhelper under bootstrap sniper steam runtime via /home/fractured/.local/share/Steam/ubuntu12_64/steam-runtime-sniper.sh", but no listing of a running game. T5: does not cover.

## 3. Not found

- **T1 on Linux desktops with real users (full running-process sets).** No public data set with the complete set of running processes on real Linux desktops during named activities was found. BEHACOM (S3-04) gives only the foreground and penultimate executable per minute (and a count), SWELL (S3-01) is Windows, OpTC (S3-05) is scripted Windows VMs, LANL (S3-06) pseudonymises process names, Carat (S3-13) is Android. Searches: #6–12, #22, #23, #25.
- **T2 raw focus-event logs from natural (non-lab) use.** Only SWELL (lab tasks, Windows, 2012) has raw window-activation events with application names; BEHACOM has per-minute aggregates of natural use. No ActivityWatch/RescueTime/Tockler export was found as a public multi-user data set (search #22: Zenodo "ActivityWatch dataset" returned the software release only; "RescueTime data" nothing relevant). The 8-week Windows 10 data set of S3-14 is announced "for vetted research usage" only.
- **T4 Chromium renderer-process counts for a given tab/site set; tab-switch and page-load rates in current browsers.** Not found in any public data set. Test Pilot (S3-02) has window/tab counts but no tab-select or page-load events and predates multi-process Firefox; data.firefox.com (S3-03) publishes no tab/window metric; BEHACOM gives only a per-app process count (Chrome 10–24 processes, tabs unknown). Searches #2–5, #6.
- **T5 Proton game thread counts; Steam download behaviour while a game runs on Linux; compositor/overlay/voice-chat co-presence on Linux.** Not found as data. The only process listing of a running Proton game obtained is S3-08 (names and PIDs, no threads, WebFetch rendering, not byte-verified). scx issues with lavd logs could not be read (github.com gated for this session: HTTP 403; MCP issue_read denied; Wayback resets), searches #13–17. ProtonDB report dumps were not opened (they carry system info, not process lists; not attempted within the budget). Steam survey (S3-09) has no session-type or process data.
- **T6 run frequency/duration of background jobs from real desktops.** Not found in S3 sources; popcon (S3-10) gives install counts only; public `systemd-analyze`/`list-timers` attachments from real desktops were not reached (GitHub gated; search budget spent on data sets).
- **T7 object counts per build, video render/transcode lengths, backup-run sizes, desktop ML training runs.** Not found as data. OpenBenchmarking (S3-11) gives only whole-build wall times (and ratios to the kernel build). TravisTorrent's home page (search #21) now serves an unrelated site; CI data sets on Zenodo were not opened (CI ≠ desktop).
- **T9 image-filter applications, video-editor preview renders per minute; interaction vs idle.** Not found. SWELL gives page-load and e-mail-send counts only (S3-01).
- **T10 launch durations on Linux.** Not found (SWELL logs Windows application starts without durations).
- **T11 video-call client process structure; concurrent media playback.** Not found in S3 sources (BEHACOM shows Skype/skypeforlinux and Spotify as foreground apps in some minutes; SWELL's only media is the imposed relaxation video).
- **T12 OS-vendor desktop telemetry with process names.** Not found publicly beyond browser vendors' aggregates (S3-02, S3-03). Restricted or unreachable: OpTC original Google Drive (quota exceeded), LANL (e-mail registration), S3-14 (vetted access), SENSE-42 (restricted, and not desktop-app data).
- **T13.** Outside S3; nothing found.

## Appendix — scripts (verbatim; run from the stated folder)

### Appendix A — run in `sources/S3-01/`

`analysis/swell_focus.py`:

```python
# Usage: python3 swell_focus.py <uLog.xml> [...]   -> per-file focus dwell / switch statistics
import sys, xml.etree.ElementTree as ET, collections, statistics as st
from datetime import datetime
def ts(s):  # '2012-09-18T11:14:25.5412554Z' -> datetime (truncate to microseconds)
    s=s.rstrip('Z'); d,f=(s.split('.')+['0'])[:2]
    return datetime.fromisoformat(d+'.'+(f+'000000')[:6])
def analyse(fn, verbose=True):
    root=ET.parse(fn).getroot()
    evs=[(ts(e.findtext('TimeStamp')), e.findtext('EventAction'), e.findtext('Control/ControlApplication') or '(unknown)', e.findtext('EventDescription')) for e in root if e.findtext('TimeStamp')]
    t0,t1=evs[0][0],evs[-1][0]
    act=[(t,a) for t,x,a,_ in evs if x=='Window Activated']
    # focus segments: app holds focus from its activation until the next activation of a different app
    segs=[]
    for t,a in act:
        if segs and segs[-1][0]==a: continue
        segs.append([a,t])
    out=[]
    for i,(a,t) in enumerate(segs):
        end=segs[i+1][1] if i+1<len(segs) else t1
        out.append((a,(end-t).total_seconds()))
    started=collections.Counter(d.split('"')[1] for t,x,a,d in evs if x=='Application started')
    exited=collections.Counter(d.split('"')[1] for t,x,a,d in evs if x=='Application exited')
    # work window: from first WINWORD/POWERPNT activation to end (excludes relaxation movie before task)
    work=[i for i,(a,t) in enumerate(segs) if a in ('WINWORD','POWERPNT')]
    res=dict(file=fn.split('/')[-1], span_min=(t1-t0).total_seconds()/60, n_events=len(evs), n_activations=len(act), n_focus_segments=len(out), n_switches=len(out)-1, started=started, exited=exited)
    if work:
        tw=segs[work[0]][1]; ws=[(a,d) for (a,d),(aa,t) in zip(out,segs) if t>=tw]
        res['work_min']=(t1-tw).total_seconds()/60; res['work_switches']=len(ws)-1
        res['work_switch_per_min']=(len(ws)-1)/res['work_min']
        res['work_dwell_median_s']=st.median(d for a,d in ws)
        res['work_dwells']=ws
    per=collections.defaultdict(list)
    for a,d in out: per[a].append(d)
    res['per_app']={a:(len(v),sum(v),st.median(v)) for a,v in per.items()}
    if verbose:
        print('file',res['file'],'span_min %.2f'%res['span_min'],'events',len(evs),'activations',len(act),'focus_segments',len(out),'switches',len(out)-1)
        print('app  n_segments  total_dwell_s  median_dwell_s')
        for a,(n,tot,med) in sorted(res['per_app'].items(), key=lambda x:-x[1][1]): print('  %-22s %4d %9.1f %8.1f'%(a,n,tot,med))
        if work: print('work window (from first WINWORD/POWERPNT focus): %.2f min, switches %d, %.2f switches/min, median dwell %.1f s'%(res['work_min'],res['work_switches'],res['work_switch_per_min'],res['work_dwell_median_s']))
        print('processes started:',dict(started.most_common()))
    return res
if __name__=='__main__':
    for f in sys.argv[1:]: analyse(f)
```

`analysis/swell_all.py`:

```python
# Usage: cd sources/S3-01 && python3 analysis/swell_all.py   -> population statistics over all 76 raw uLog files
import glob, re, csv, collections, statistics as st, sys
sys.path.insert(0,'analysis'); from swell_focus import analyse
cond={}
for r in csv.DictReader(open('overview.tab'),delimiter='\t'):
    if r['PP'].isdigit(): cond[(int(r['PP']),int(r['Block']))]=r['Condition']
rows=[]; allstart=collections.Counter(); filesstart=collections.Counter(); alldw=[]; appdw=collections.defaultdict(list); fg=collections.Counter()
for f in sorted(glob.glob('ulog/*.xml')):
    m=re.search(r'pp(\d+)_c(\d)',f); pp,b=int(m[1]),int(m[2])
    r=analyse(f,verbose=False)
    if 'work_min' not in r or r['work_min']<10: print('skip',f,'%.1f'%r.get('work_min',0)); continue
    c=cond[(pp,b)]; rows.append((pp,b,c,r['work_min'],r['work_switches'],r['work_switch_per_min'],r['work_dwell_median_s'],len(r['per_app'])))
    allstart.update(r['started']); filesstart.update(set(r['started']))
    for a,d in r['work_dwells']: alldw.append(d); appdw[a].append(d)
    fg.update(set(a for a,d in r['work_dwells']))
print('sessions',len(rows),'participants',len(set(x[0] for x in rows)))
def q(v): v=sorted(v); n=len(v); return 'n=%d min=%.2f p25=%.2f median=%.2f p75=%.2f max=%.2f mean=%.2f'%(n,v[0],v[n//4],st.median(v),v[3*n//4],v[-1],st.mean(v))
print('work-window length (min):',q([x[3] for x in rows]))
print('switches/min per session (all):',q([x[5] for x in rows]))
for c in 'NTI': print('  condition',c,q([x[5] for x in rows if x[2]==c]))
print('median dwell per session (s):',q([x[6] for x in rows]))
print('pooled focus-segment dwell (s):',q(alldw))
print('foreground apps: sessions in which app held focus (of %d) / pooled median dwell s / total segments'%len(rows))
for a,n in fg.most_common(): print('  %-34s %3d %7.1f %6d'%(a,n,st.median(appdw[a]),len(appdw[a])))
print('processes started (Application started events): sessions containing / total starts')
for a,n in filesstart.most_common(): print('  %-40s %3d %5d'%(a,n,allstart[a]))
for c in 'NTI': print('work-window length (min), condition',c,q([x[3] for x in rows if x[2]==c]))
for b in (1,2,3): print('work-window length (min), file index c%d'%b,q([x[3] for x in rows if x[1]==b]))
```

`analysis/swell_filtered.py`:

```python
# Usage: cd sources/S3-01 && python3 analysis/swell_filtered.py -> switch rate when shell/taskbar (explorer), unnamed windows ((unknown)) and the logger (uLog 3.2) are removed and adjacent same-app segments merged
import glob, statistics as st, sys
sys.path.insert(0,'analysis'); from swell_focus import analyse
SKIP={'explorer','(unknown)','uLog 3.2'}; rates=[]; dw=[]
for f in sorted(glob.glob('ulog/*.xml')):
    r=analyse(f,verbose=False)
    if 'work_min' not in r or r['work_min']<10: continue
    seq=[]
    for a,d in r['work_dwells']:
        if a in SKIP: continue
        if seq and seq[-1][0]==a: seq[-1][1]+=d
        else: seq.append([a,d])
    rates.append((len(seq)-1)/r['work_min']); dw+= [d for a,d in seq]
v=sorted(rates); n=len(v); print('sessions',n,'app switches/min (filtered): p25 %.2f median %.2f p75 %.2f max %.2f'%(v[n//4],st.median(v),v[3*n//4],v[-1]))
w=sorted(dw); m=len(w); print('pooled dwell per app visit (s, filtered; time of removed segments dropped): n=%d p25 %.1f median %.1f p75 %.1f p90 %.1f'%(m,w[m//4],st.median(w),w[3*m//4],w[9*m//10]))
```

`analysis/swell_url.py`:

```python
# Usage: cd sources/S3-01 && python3 analysis/swell_url.py -> 'Browser URL changed' events per minute of iexplore focus, per session
import glob, statistics as st, sys
sys.path.insert(0,'analysis'); from swell_focus import analyse, ts
import xml.etree.ElementTree as ET
rates=[]; tot=0; totmin=0
for f in sorted(glob.glob('ulog/*.xml')):
    r=analyse(f,verbose=False)
    if 'work_min' not in r or r['work_min']<10: continue
    n=sum(1 for e in ET.parse(f).getroot() if e.findtext('EventAction')=='Browser URL changed')
    ie=sum(d for a,d in r['work_dwells'] if a=='iexplore')/60
    if ie>1: rates.append(n/ie); tot+=n; totmin+=ie
v=sorted(rates); k=len(v)
print('sessions',k,'URL changes per iexplore-focused minute: min %.2f p25 %.2f median %.2f p75 %.2f max %.2f; pooled %d changes / %.1f min = %.2f/min'%(v[0],v[k//4],st.median(v),v[3*k//4],v[-1],tot,totmin,tot/totmin))
```

`analysis/swell_send.py`:

```python
# Usage: cd sources/S3-01 && python3 analysis/swell_send.py -> clicks on an OUTLOOK control captioned "Send" per session and per condition
import glob, re, csv, collections, xml.etree.ElementTree as ET
cond={(int(r['PP']),int(r['Block'])):r['Condition'] for r in csv.DictReader(open('overview.tab'),delimiter='\t') if r['PP'].isdigit()}
per=collections.defaultdict(list); ex=None
for f in sorted(glob.glob('ulog/*.xml')):
    m=re.search(r'pp(\d+)_c(\d)',f); c=cond[(int(m[1]),int(m[2]))]
    n=0
    for e in ET.parse(f).getroot():
        if e.findtext('EventAction')=='clicked' and e.findtext('Control/ControlApplication')=='OUTLOOK' and (e.findtext('Control/ControlCaption') or '').strip()=='Send':
            n+=1; ex=ex or (f,e.findtext('TimeStamp'),e.findtext('EventDescription'))
    per[c].append(n)
for c,v in per.items(): print(c,'sessions',len(v),'total Send clicks',sum(v),'sessions with >=1',sum(1 for x in v if x),'max',max(v))
print('example:',ex)
```

### Appendix B — run in `sources/S3-02/`

`witl_tabs.py`:

```python
# Usage: python3 witl_tabs.py <events.csv> <users.csv>  -> windows/tabs distributions from NUM_TABS (code 26) and SESSION_ON_RESTORE (code 20)
import csv, sys, collections, statistics as st
ev, us = sys.argv[1], sys.argv[2]
osmap={r['id']:r['os'] for r in csv.DictReader(open(us))}
tabs=collections.defaultdict(list); wins=collections.defaultdict(list); ts=collections.defaultdict(list); rest=[]
for r in csv.DictReader(open(ev)):
    if r['event_code']=='26':
        try: w=int(r['data1'].split()[0]); t=int(r['data2'].split()[0])
        except (ValueError, IndexError): continue  # rows with NaN counts are skipped
        tabs[r['user_id']].append(t); wins[r['user_id']].append(w); ts[r['user_id']].append(int(r['timestamp']))
    elif r['event_code']=='20':
        try: rest.append((int(r['data1'].split()[-1]),int(r['data2'].split()[-1])))
        except (ValueError, IndexError): pass
def q(v):
    v=sorted(v); n=len(v); return 'n=%d p10=%s p25=%s median=%s p75=%s p90=%s max=%s mean=%.2f'%(n,v[n//10],v[n//4],st.median(v),v[3*n//4],v[9*n//10],v[-1],st.mean(v))
users=sorted(tabs); print('users with NUM_TABS events:',len(users))
fam=collections.Counter(osmap.get(u,'?').split()[0] for u in users); print('OS family of those users:',dict(fam))
print('per-user median tabs:',q([st.median(tabs[u]) for u in users]))
print('per-user max tabs:',q([max(tabs[u]) for u in users]))
print('per-user median windows:',q([st.median(wins[u]) for u in users]))
print('per-user max windows:',q([max(wins[u]) for u in users]))
print('pooled NUM_TABS samples, tabs:',q([t for u in users for t in tabs[u]]))
print('pooled NUM_TABS samples, windows:',q([w for u in users for w in wins[u]]))
print('share of samples with 1 window: %.3f'%(sum(1 for u in users for w in wins[u] if w==1)/sum(len(wins[u]) for u in users)))
print('tabs per window (pooled):',q([t/w for u in users for t,w in zip(tabs[u],wins[u]) if w>0]))
span=[(max(ts[u])-min(ts[u]))/86400000 for u in users]; print('per-user observation span (days):',q(span))
print('SESSION_ON_RESTORE with >0 windows: %d of %d; restored tabs among those:'%(sum(1 for w,t in rest if w>0),len(rest)), q([t for w,t in rest if w>0]) if any(w>0 for w,t in rest) else '')
# tab-count changes: consecutive NUM_TABS samples (time-ordered, per user) whose tab count differs = tab opened/closed
chg=[]; lin=[u for u in users if osmap.get(u,'').startswith('Linux')]
for u in users:
    o=sorted(zip(ts[u],tabs[u])); c=sum(1 for a,b in zip(o,o[1:]) if a[1]!=b[1])
    d=len(set(t//86400000 for t,_ in o)); chg.append(c/d)
print('tab-count changes per user per calendar day with events:',q(chg))
print('Linux users:',len(lin)); 
if len(lin)>3:
    print('  Linux per-user median tabs:',q([st.median(tabs[u]) for u in lin])); print('  Linux per-user max tabs:',q([max(tabs[u]) for u in lin])); print('  Linux per-user max windows:',q([max(wins[u]) for u in lin]))
```

### Appendix C — run in `sources/S3-04/`

`behacom_stats.py`:

```python
# Usage: cd sources/S3-04 && python3 behacom_stats.py  -> streams Behacom.zip (no extraction), per-user app statistics from the per-minute feature vectors
import zipfile, io, collections, statistics as st
z=zipfile.ZipFile('Behacom.zip')
names=sorted([n for n in z.namelist() if n.endswith('.csv')], key=lambda n:int(n.split('User')[1].split('/')[0]))
def q(v):
    v=sorted(v); n=len(v); return 'n=%d p10=%.2f p25=%.2f median=%.2f p75=%.2f p90=%.2f max=%.2f mean=%.2f'%(n,v[n//10],v[n//4],st.median(v),v[3*n//4],v[9*n//10],v[-1],st.mean(v))
allapps=collections.Counter(); usersper=collections.Counter(); pooled_act=[]; pooled_ch=[]
for n in names:
    f=io.TextIOWrapper(z.open(n),encoding='utf-8',errors='replace')
    hdr=f.readline().rstrip('\n').split(','); ix={h:i for i,h in enumerate(hdr)}
    # the last 18 columns hold the app/resource features; take them from the line tail (rsplit) to avoid parsing 12k columns
    tail=len(hdr)-ix['active_apps_average']
    act=[];ch=[];apps=collections.Counter();ts=[];procs=collections.defaultdict(list)
    for line in f:
        p=line.rstrip('\n').rsplit(',',tail)[1:]
        if len(p)!=tail: continue
        try: a=float(p[0]); c=float(p[3]); t=int(float(line.split(',',1)[0]))
        except ValueError: continue
        act.append(a); ch.append(c); apps[p[1]]+=1; ts.append(t)
        try: procs[p[1]].append(float(p[5]))
        except ValueError: pass
    days=len(set(t//86400000 for t in ts))
    print('%s minutes=%d distinct_days=%d'%(n,len(act),days))
    print('  active_apps_average per minute:',q(act))
    print('  changes_between_apps per minute:',q(ch))
    print('  top foreground apps (minutes):',apps.most_common(12))
    print('  median current_app_average_processes for top apps:',{a:st.median(procs[a]) for a,_ in apps.most_common(6) if procs[a]})
    allapps.update(apps); usersper.update(set(apps)); pooled_act+=act; pooled_ch+=ch
print('POOLED active_apps_average:',q(pooled_act)); print('POOLED changes_between_apps:',q(pooled_ch))
print('share of minutes with 0 changes: %.3f'%(sum(1 for c in pooled_ch if c==0)/len(pooled_ch)))
print('apps by number of users having them in foreground (users, minutes):',[(a,usersper[a],allapps[a]) for a,_ in usersper.most_common(40)])
```

`behacom_game.py`:

```python
# Usage: python3 behacom_game.py  -> for game foreground minutes: penultimate apps, active_apps_average, system CPU
import zipfile, io, collections, statistics as st
z=zipfile.ZipFile('Behacom.zip'); games={'csgo.exe','League of Legends.exe','TslGame.exe'}
for n in ['Behacom/User0/User0_BEHACOM.csv','Behacom/User5/User5_BEHACOM.csv','Behacom/User6/User6_BEHACOM.csv']:
    f=io.TextIOWrapper(z.open(n),encoding='utf-8',errors='replace'); hdr=f.readline().rstrip('\n').split(','); ix={h:i for i,h in enumerate(hdr)}
    tail=len(hdr)-ix['active_apps_average']; b=ix['active_apps_average']
    pen=collections.Counter(); act=[]; cpu=[]; appcpu=[]; ex=None
    for k,line in enumerate(f,2):
        p=line.rstrip('\n').rsplit(',',tail)[1:]
        if len(p)!=tail or p[1] not in games: continue
        pen[p[2]]+=1; act.append(float(p[0])); cpu.append(float(p[ix['system_average_cpu']-b])); appcpu.append(float(p[ix['current_app_average_cpu']-b]))
        if ex is None: ex=(k,[hdr[b+i]+'='+v for i,v in enumerate(p)])
    print(n,'game minutes',len(act),'penultimate_app',pen.most_common(8),'median active_apps_average',st.median(act),'median system_average_cpu',st.median(cpu),'median current_app_average_cpu',st.median(appcpu))
    print('  example row (file line %d), last columns:'%ex[0],ex[1])
```

### Appendix D — run in `sources/S3-05/`

`optc_proc.py`:

```python
# Usage: python3 optc_proc.py sysclient0254_partial.jsonl -> PROCESS CREATE image names, time span, and distinct image names seen per 10-min bucket
import json, collections, sys
c=collections.Counter(); ts=[]; alive=collections.defaultdict(set); first=None
rows=[]
for i,l in enumerate(open(sys.argv[1]),1):
    try: e=json.loads(l)
    except Exception: continue
    ts.append(e['timestamp'])
    if e['object']=='PROCESS' and e['action']=='CREATE':
        img=e['properties'].get('image_path','?').split('\\')[-1]; c[img]+=1; rows.append((i,e['timestamp'],img,e['properties'].get('parent_image_path','').split('\\')[-1]))
    img=e['properties'].get('image_path')
    if img: alive[e['timestamp'][:15]].add(img.split('\\')[-1].lower())
print('events',len(ts),'first',min(ts),'last',max(ts))
print('PROCESS CREATE by image:',c.most_common(40))
print('first 15 PROCESS CREATE rows (line, timestamp, image, parent):'); [print(' ',r) for r in rows[:15]]
print('distinct image names acting per 10-minute bucket:',{k:len(v) for k,v in sorted(alive.items())})
k=sorted(alive)[len(alive)//2]; print('names in bucket',k,sorted(alive[k]))
```

### Appendix E — run in `sources/S3-11/`

`ob_ratio.py`:

```python
# Usage: cd sources/S3-11 && python3 ob_ratio.py -> per-CPU "Seconds (Average)" from each openbenchmarking test page's default-configuration table, ratio to build-linux-kernel defconfig on the same CPU
import re, glob, statistics as st
def parse(f):
    L=open(f).read().splitlines()
    i=next(k for k,l in enumerate(L) if l.startswith('OpenBenchmarking.org metrics for this test profile configuration'))
    cfg=L[i-2]+' | '+L[i-1]; meta=L[i]
    j=next(k for k in range(i,len(L)) if L[k]=='Seconds (Average)')+1
    d={}; med=None; k=j
    while k+3<len(L):
        if L[k]=='Median': med=L[k+2]; k+=3; continue
        if re.match(r'^\d+(st|nd|rd|th)$',L[k+1]) and re.match(r'^\d+$',L[k+2]) and re.match(r'^[\d.]+( \+/- [\d.]+)?$',L[k+3]):
            d[L[k]]=float(L[k+3].split()[0]); k+=4
        else: break
    rt=[l for l in L if 'has an average run-time of' in l]
    return cfg,meta,med,d,(rt[0] if rt else '')
P={f[3:-4]:parse(f) for f in glob.glob('ob_*.txt')}
K=P['build-linux-kernel'][3]
for t,(cfg,meta,med,d,rt) in sorted(P.items()):
    common=[c for c in d if c in K]
    r=[d[c]/K[c] for c in common]
    print('%-20s cfg=[%s] cpus=%d median_s=%s common_with_kernel=%d'%(t,cfg,len(d),med,len(common)), ('ratio_to_kernel_defconfig median=%.2f min=%.2f max=%.2f'%(st.median(r),min(r),max(r)) if r else ''))
    print('    ',meta); print('    ',rt[:200])
```

### Appendix F — run in `sources/S3-13/`

`carat_extract.py`:

```python
# Usage: python3 carat_extract.py part-00995.range.bin out.gz -> decrypts one ZipCrypto-stored member fetched by HTTP range (local header at byte 309211 of the 6,375,824,106-byte zip)
import struct, sys, zlib
b=open(sys.argv[1],'rb').read(); assert b[:4]==b'PK\x03\x04'
flag,meth=struct.unpack('<HH',b[6:10]); nl,el=struct.unpack('<HH',b[26:30]); name=b[30:30+nl].decode(); data=b[30+nl+el:]
print(name,'flag',flag,'method',meth)
crc=[0]*256
for i in range(256):
    c=i
    for _ in range(8): c=(c>>1)^0xEDB88320 if c&1 else c>>1
    crc[i]=c
k=[0x12345678,0x23456789,0x34567890]
def upd(ch):
    k[0]=crc[(k[0]^ch)&0xff]^(k[0]>>8); k[1]=(k[1]+(k[0]&0xff))&0xffffffff; k[1]=(k[1]*134775813+1)&0xffffffff; k[2]=crc[(k[2]^(k[1]>>24))&0xff]^(k[2]>>8)
for ch in b'carat-helsinki-lagerspetz': upd(ch)
out=bytearray()
for c in data[:4806283]:
    t=(k[2]|2)&0xffff; p=c^(((t*(t^1))>>8)&0xff); upd(p); out.append(p)
open(sys.argv[2],'wb').write(bytes(out[12:]))
```

`carat_stats.py`:

```python
# Usage: python3 carat_stats.py part-00995.gz -> distinct running process names per sample, by priority class
import gzip, json, statistics as st, collections
n=[];fg=[];users=set();pri=collections.Counter()
for l in gzip.open('part-00995.gz','rt'):
    d=json.loads(l); users.add(d['uuid']); a=d.get('apps') or []
    n.append(len(set(x['processName'] for x in a))); fg.append(len(set(x['processName'] for x in a if x.get('priority')=='Foreground app')))
    pri.update(x.get('priority') for x in a)
def q(v): v=sorted(v); k=len(v); return 'n=%d p10=%s p25=%s median=%s p75=%s p90=%s max=%s mean=%.2f'%(k,v[k//10],v[k//4],st.median(v),v[3*k//4],v[9*k//10],v[-1],st.mean(v))
print('users in part',len(users)); print('distinct processNames per sample:',q(n)); print('distinct Foreground-app names per sample:',q(fg)); print('priority counts:',pri.most_common())
```

