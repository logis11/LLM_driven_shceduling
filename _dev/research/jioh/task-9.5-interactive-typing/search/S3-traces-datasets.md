# S3 — public traces and datasets (T1–T5) — search record

Reader: S3. Date of all fetches and computations: 2026-09-13. Input read: `search/input.md` only.
Copies saved under `sources/S3-<id>/` (gitignored), each folder with `SHA256SUMS.txt`; SHA-256 values below are of the saved copy (for files I gzipped after fetching, the SHA-256 of the raw fetched bytes is given and marked "raw").

Conventions in this record:
- "Verbatim" passages are quoted exactly as fetched, with a locator (`file:line`, README section, issue iid + `description`, comment id + date, JSON key, PDF page).
- Every number under "My computation" is mine, not the source's statement; each states file, rows, and method so it can be re-run.
- Percentiles are linear-interpolated (`k=(n-1)p/100`), as in the scripts run; "share>X" is the fraction of values strictly greater than X.
- Network: outbound HTTPS goes through the session's egress proxy. `github.com` and `api.github.com` returned HTTP 403 for every URL (proxy policy: "GitHub access to this repository is not enabled for this session"); `raw.githubusercontent.com`, `gist.githubusercontent.com` and `git clone` over HTTPS worked. GitLab (`gitlab.freedesktop.org`, `gitlab.gnome.org`) issue notes need login (HTTP 401) but issue descriptions (API) and, on gitlab.gnome.org only, `/uploads/` attachments were reachable; `gitlab.freedesktop.org/…/uploads/…` returned 404 without login.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------------|---------------|--------------------------|
| 1 | 2026-09-13 | curl probe | `https://userinterfaces.aalto.fi/136Mkeystrokes/` | 200 → candidate S3-aalto136m | — |
| 2 | 2026-09-13 | curl probe | `https://www.cs.cmu.edu/~keystroke/` | 200 → S3-cmu-keystroke | — |
| 3 | 2026-09-13 | curl probe | `https://github.com/balabit/Mouse-Dynamics-Challenge` | — | 403 (proxy policy); worked around via `raw.githubusercontent.com` (200) and `git clone --depth 1` (ok) |
| 4 | 2026-09-13 | curl probe | `https://zenodo.org/record/2908966` | 301 → `https://zenodo.org/records/2908966`; API `https://zenodo.org/api/records/2908966` 200 | — |
| 5 | 2026-09-13 | curl probe | `https://osf.io/y3p4d/`; `https://api.osf.io/v2/nodes/y3p4d/` | 200 → S3-osf-y3p4d | first file-list call failed with curl error 3 (unescaped `[` in URL), fixed with `%5B%5D` |
| 6 | 2026-09-13 | curl probe | `https://userinterfaces.aalto.fi/how-we-type/` | 200 → S3-howwetype | — |
| 7 | 2026-09-13 | curl probe | `https://gitlab.freedesktop.org/pipewire/pipewire/-/issues` | — | 404 (HTML listing); API `/api/v4/projects/pipewire%2Fpipewire/issues?search=pw-top…` 200 |
| 8 | 2026-09-13 | curl probe | `https://api.github.com/repos/mpv-player/mpv` | — | 403 (proxy: GitHub API not enabled for this session) |
| 9 | 2026-09-13 | WebSearch | `136M keystrokes dataset Aalto PRESS_TIME RELEASE_TIME readme` | userinterfaces.aalto.fi/136Mkeystrokes (already probed); github.com/aalto-ui/136m-keystrokes (not opened, github.com blocked) | — |
| 10 | 2026-09-13 | WebSearch | `Balabit Mouse Dynamics Challenge dataset github record timestamp client timestamp button state x y` | github.com/balabit/Mouse-Dynamics-Challenge (via raw + clone); ms.sapientia.ro DFL (see #38) | — |
| 11 | 2026-09-13 | WebSearch | `Inputlog copy task dataset zenodo keystroke interval ct.csv osf` | zenodo.org/records/5803401 → S3-inputlog-ct-corpus; zenodo 7886743 KeyRecs → S3-keyrecs | — |
| 12 | 2026-09-13 | curl | `https://userinterfaces.aalto.fi/136Mkeystrokes/data/readme.txt`, `…/readme.txt`, `…/resources/readme.txt` | — | all 404; readme obtained from inside `data/Keystrokes.zip` by HTTP range request instead |
| 13 | 2026-09-13 | curl HEAD + range | `https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip` (Content-Length 1572785433, `Accept-Ranges: bytes`) | ranges 1552185433–1572785432 (20.6 MB, central directory) then per-file ranges for readme, metadata and 6 participant files (206) | — |
| 14 | 2026-09-13 | curl | `https://www.cs.cmu.edu/~keystroke/DSL-StrongPasswordData.csv` | 200, MD5 matches page (`470235f96568f28f9ea0da62234ec857`) | — |
| 15 | 2026-09-13 | curl | `https://zenodo.org/api/records/5803401/files/sub-dataset_EN_21-25year.zip/content` | 200, MD5 matches record (`096cdbd402d4f9ba784a3f335f9fbc1a`) | — |
| 16 | 2026-09-13 | curl | `https://osf.io/download/wp6k4/` (ct.csv, 86,534,920 B) | 200 | — |
| 17 | 2026-09-13 | Zenodo search API | `https://zenodo.org/api/records?q="How we type" Feit` | record 4047775 → S3-howwetype (Readme.txt, `Typing data v2.0.zip` fetched; MD5 `722f56877a6cc03d1ba7cdf8af48e183` matches) | — |
| 18 | 2026-09-13 | GitLab API | pipewire issues `search=pw-top`, then `search=QUANT&in=description`, pages 1–4 (100/page) | 39 issues whose description contains a textual `S ID QUANT RATE WAIT BUSY` table → S3-pipewire-pwtop | issue notes: 401 Unauthorized; uploads `/uploads/45cd…/pw-dump.log` and `…/old_quantumpw.png` (issue 4875): 404 |
| 19 | 2026-09-13 | WebSearch | `share.firefox.dev profile typing keypress latency "profiler.firefox.com" bugzilla text input jank` | bugzilla 1664556, 1408699, 1593115, 1593994 → S3-firefox-profiles | — |
| 20 | 2026-09-13 | WebSearch | `mpv issue "--dump-stats" software decode CPU per frame vo timing stats output` | github mpv issues (blocked, see #8, #31) | — |
| 21 | 2026-09-13 | WebSearch | `video conferencing measurement IMC 2021 dataset Zoom Meet Teams CPU utilization released dataset artifact` | github.com/kyle-macmillan/vca-imc-21 README via raw → S3-imc21-vca | — |
| 22 | 2026-09-13 | WebSearch | `Clarkson II free text keystroke dataset download Buffalo SUNY keystroke dataset free text timestamps` | citer.clarkson.edu page → S3-clarkson2; buffalo.edu page (see #29) | — |
| 23 | 2026-09-13 | Bugzilla REST | `https://bugzilla.mozilla.org/rest/bug/1664556/comment`, `/1408699/comment`, `/1593115/comment`, `/1593994/comment`; `rest/bug?quicksearch=typing lag&op_sys=Linux` | comment 15032066 (2020-09-11) `https://share.firefox.dev/3kanAYe`; comment 14460151 (2019-10-31) profile `2ffa5d5b…`; comments 14473375 (2019-11-07) `https://perfht.ml/2CmlHnK`, 15278588 (2021-02-23) `https://share.firefox.dev/37FMqf3`, `/2MhovuJ`, `/3khBSrt` | 1408699: no profile link in its 9 comments |
| 24 | 2026-09-13 | curl | short links above → `https://profiler.firefox.com/public/<hash>/…` (301) → `https://storage.googleapis.com/profile-store/<hash>` | six profiles downloaded (200) | — |
| 25 | 2026-09-13 | curl | `https://raw.githubusercontent.com/balabit/Mouse-Dynamics-Challenge/master/README.md`; `git clone --depth 1 --filter=blob:none --no-checkout https://github.com/balabit/Mouse-Dynamics-Challenge` | 200; clone ok, HEAD `d00d6f779254a2a917deeab4a5b7a9e8643bd91e` (2018-09-21) | — |
| 26 | 2026-09-13 | WebSearch | `Buffalo keystroke dataset "cubs.buffalo.edu" free text 148 participants download Sun Ceker Upadhyaya` | `http://cubs.buffalo.edu/research/datasets` → 301 → `https://www.buffalo.edu/cubs/research/datasets.html` | curl 403 (both http and https); WebFetch returned a summary (S3-buffalo) |
| 27 | 2026-09-13 | WebSearch | `SWELL-KW dataset knowledge work computer interaction logging keyboard mouse application window 4TU download` | `http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html` (200); DANS `ssh.datastations.nl` doi:10.17026/dans-x55-69zp (Dataverse API 200; two uLog XML files downloaded) → S3-swell-kw | — |
| 28 | 2026-09-13 | WebSearch | `vscode issue typing latency "cpuprofile" keystroke slow typing profile attached` | github.com/microsoft/vscode/issues/62475, 38586, 212031, 150107 | github.com 403 (proxy); `github.com/user-attachments/files/…` 403; MCP `issue_read` denied ("repository not configured for this session"); WebFetch gave only a summary → not cited as a source |
| 29 | 2026-09-13 | WebSearch | `webrtc-internals dump "googAvgEncodeMs" OR "totalEncodeTime" issue attached dump linux CPU encode` | bugs.chromium.org 597087 (Monorail, not opened); gist thg1101/8f11e3c2c7274f114536 via `gist.githubusercontent.com/…/raw/` (200) → S3-webrtc-internals | — |
| 30 | 2026-09-13 | MCP github search_issues | repo mpv-player/mpv: `dump-stats output attached decode time frame timing` | issues 17683, 14245, 6812 listed | bodies unreachable (github.com 403; MCP issue_read denied for non-session repos); WebFetch summary only → not cited |
| 31 | 2026-09-13 | WebSearch | `Clarkson II keystroke dataset download "Clarkson University" free-text 103 users Murphy Huang Hou Schuckers request` | `https://citer.clarkson.edu/clarkson-university-keystroke-dataset-ii/` 200 | — |
| 32 | 2026-09-13 | WebSearch | `ui.perfetto.dev example trace Chrome desktop trace download "example" chrome json trace perfetto sample` | perfetto docs; then MCP `search_code chrome_example_wikipedia repo:google/perfetto` → `ui/src/core_plugins/dev.perfetto.ExampleTraces/index.ts` names `https://storage.googleapis.com/perfetto-misc/chrome_example_wikipedia.perfetto_trace.gz` (21,537,072 B, downloaded 200) → S3-perfetto-chrome | `example_android_trace_15s` (57,202,082 B) not downloaded (mobile) |
| 33 | 2026-09-13 | WebSearch | `sysprof capture attached gnome-shell typing gtk4 text view issue gitlab.gnome.org ".syscap"` | GitLab API `projects/GNOME%2Fgtk/issues?search=syscap` (2 hits: 5762, 3435), `GNOME%2Fgnome-shell` (7454, 6213), `GNOME%2Fgnome-text-editor` (179), `GNOME%2Fmutter` (0) → S3-sysprof-gnome (two .syscap downloaded: gnome-text-editor#179 `g-t-e.syscap`, gtk#3435 `expanding.syscap`) | — |
| 34 | 2026-09-13 | curl probe | `https://www.eecs.harvard.edu/~yaz/` (Endo) | — | 301 → `http://www.wafu.ne.jp/~yaz/` (unrelated host); `http://www.eecs.harvard.edu/~yaz/interactive/` 302 → https, no content followed |
| 35 | 2026-09-13 | curl probe | `https://www.eecs.umich.edu/~tnm/`, `http://www.eecs.umich.edu/~tnm/interactive/` → 301 → `https://web.eecs.umich.edu/~tnm/interactive/` (Flautner) | — | curl exit 60 (TLS: "unable to get local issuer certificate", origin chain incomplete); WebFetch: HTTP 503 |
| 36 | 2026-09-13 | curl | `https://lttng.org/files/` (200), `https://lttng.org/files/samples/` (200) | listing: `sample-ctf-trace-20120412.tar.bz2` (4,872,697 B, 2012-04-15), `trace1.tar.bz2` (870,810 B, 2005-09-22) | not downloaded: no description of workload; kernel traces of unknown sessions (see Not found) |
| 37 | 2026-09-13 | KDE Bugzilla REST | `rest/bug?product=kate&product=kdenlive&product=frameworks-ktexteditor&summary=typing…`; `rest/bug?longdesc=perf.data…`; `rest/bug/{501508,195971,492896}/attachment` | 492896 (konsole, 2024-09) has two `perf.data.perfparser.gz` attachments (670,027 B; 551,246 B) about "Resizing embedded terminal" | 501508 and 195971: no attachments; `rest/bug?quicksearch=…` returned 404 (wrong endpoint form) |
| 38 | 2026-09-13 | WebSearch | `Chao Shen mouse dynamics dataset download Xi'an Jiaotong "mouse behavior" dataset public 28 users; DFL mouse dataset` | figshare 5619313 (API 200; README.pdf downloaded) → S3-shen-mouse; `https://www.ms.sapientia.ro/~manyi/DFL.html` (200; `DFL/User1.zip` 17,124,379 B downloaded) → S3-dfl | `nskeylab.xjtu.edu.cn` original page not probed (README.pdf is a 2015 print of it) |
| 39 | 2026-09-13 | curl | `https://userinterfaces.aalto.fi/typing37k/` | 200 → S3-aalto-typing37k (mobile; off-platform, page only) | — |
| 40 | 2026-09-13 | curl probe | `https://issues.chromium.org/issues/40068567` | 200 (JS app shell, no content without JS) | not usable with curl; no Chromium tracker content cited |
| 41 | 2026-09-13 | pip | `pip install --user perfetto` → `trace_processor_shell` v57.2 downloaded from `commondatastorage.googleapis.com/perfetto-luci-artifacts/v57.2/linux-amd64/` | used for S3-perfetto-chrome | — |

---

## 2. Candidates

### S3-aalto136m — 136M Keystrokes dataset (Dhakal, Feit, Kristensson, Oulasvirta, CHI 2018)

**Citation.** Dhakal, V., Feit, A., Kristensson, P. O., Oulasvirta, A. (2018). Observations on Typing from 136 Million Keystrokes. CHI '18. doi:10.1145/3173574.3174220. Dataset page: `https://userinterfaces.aalto.fi/136Mkeystrokes/`; data file `https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip`.

**Copy read.**
- Page `https://userinterfaces.aalto.fi/136Mkeystrokes/` (HTML, accessed 2026-09-13) → `sources/S3-aalto136m/aalto136.html`, SHA-256 `320fd2561632119e1cc8ad5da9fbecaf8b66730befdbd3f1fb78df6dd3bb010c`.
- `data/Keystrokes.zip`: HTTP `Content-Length: 1572785433`, `Last-Modified: Thu, 29 Mar 2018 10:07:35 GMT`, `ETag: "5dbecd19-5688a4ae747c0"`, `Accept-Ranges: bytes`. Not downloaded whole. I fetched bytes 1552185433–1572785432 (the ZIP64 end records and central directory; `cdoff=1552590881`, `cdsize=20194454`, 168,597 entries), parsed the central directory (saved as `cd_entries.json.gz`), and range-fetched + inflated (`zlib`, raw deflate) the local entries for `Keystrokes/files/readme.txt` (local header offset 1552589247, csize 1577, usize 3468), `Keystrokes/files/metadata_participants.txt` (offset 1545222877, csize 7,366,298, usize 21,255,894) and six participant files chosen by `random.seed(20260913); random.sample(participant_files, 6)` over the 168,593 `*_keystrokes.txt` entries: `16762`, `8502`, `237587`, `267952`, `366835`, `369097`.
- SHA-256 of inflated copies: `readme.txt` `c81fcbee7e98e53a5bc789074207ec338e66edd204bbf9a160c8edfaf098a08c`; `metadata_participants.txt` `3ba22e2c23dbcbb5645197b9dd68c17e9ef68a1be7170e1bc1f0cd869a68ac6d`; `16762_keystrokes.txt` `ce55e1a188162fa92404bbe9ff60c63e6db96ee8381da595d4a464e6380312f7`; `8502_keystrokes.txt` `468c24aecc9fe64bba9ae2b545309c2170ffa1abd9f843e37f5d2a5b478218a4`; `237587_keystrokes.txt` `01079fee01005a6adae571dce1ae2b188fa6dd8b796eadda551c3ade51ac6835`; `267952_keystrokes.txt` `d0fe2ce6f6976db94c74866f99f107c3be9ead164f533f87ac70acd0c3780ab4`; `366835_keystrokes.txt` `970ef6e194d5c4d8b6f425eece2b9424bbda0d310e24f68908263d1c79f91853`; `369097_keystrokes.txt` `f77d09fee2bb70a3085fca98ef40c35b06946bbebdc60e67d8090166bda6238a` (full values in `SHA256SUMS.txt`).

**Verbatim passages.**
- Page, section "The 136M Keystrokes Dataset" → "Data": "Text files of the keystrokes in a .zip file (1.4 GB zipped, 16 GB unzipped). The data contains the keystroke-by-keystroke entries typed by every participant. The package also includes a metadata file. See readme.txt for introduction and license. This data is free to use for research and non-commercial use with attribution to the authors."
- Page, "The 136M Keystrokes Dataset": "The data was collected using an online typing test following scientific standards for testing typing performance. The test was published on a free typing speed assessment website. Users transcribed sentences voluntarily after giving their informed consent that their anonymized data will be collected and used for research purposes."
- `readme.txt:6`: "It contains keystroke data of over 168000 users typing 15 sentences each. The data was collected via an online typing test published at a free typing speed assessment webpage."
- `readme.txt:21`: "You are free to use this data for non-commercial use in your own research or projects with attribution to the authors."
- `readme.txt:59-60`: "PRESS_TIME				Timestamp of the key down event (in ms)" / "RELEASE_TIME			Timestamp of the key release event (in ms)"
- `readme.txt:76`: "KEYBOARD_TYPE			Full (desktop), laptop, small physical (e.g on phone) or touch keyboard"
- `readme.txt:79`: "AVG_IKI					Average inter-key interval"
- `readme.txt:87`: "Note: For some users, Keystrokes are not logged or not displayed correctly. The corresponding javascript keycode is used instead."
- `16762_keystrokes.txt:1-2` (tab-separated): "PARTICIPANT_ID	TEST_SECTION_ID	SENTENCE	USER_INPUT	KEYSTROKE_ID	PRESS_TIME	RELEASE_TIME	LETTER	KEYCODE" / "16762	180565	You can't bench Martin, no matter how bad the matchup may be.	You can't bench Martin, no matter how bad the matchup may be.	8595812	1472127797038	1472127797443	SHIFT	16"
- `metadata_participants.txt:1`: "PARTICIPANT_ID	AGE	GENDER	HAS_TAKEN_TYPING_COURSE	COUNTRY	LAYOUT	NATIVE_LANGUAGE	FINGERS	TIME_SPENT_TYPING	KEYBOARD_TYPE	ERROR_RATE	AVG_WPM_15	AVG_IKI	ECPC	KSPC	ROR"

**My computation (sample of 6 participants).** Files: the six `*_keystrokes.txt` above (706, 679, 675, 664, 753, 786 rows; 15 `TEST_SECTION_ID`s each). Method: per file, group rows by `TEST_SECTION_ID`, sort by `PRESS_TIME`, take successive `PRESS_TIME` differences (ms) = within-sentence press-to-press interval; between-sentence gap = first press of section *k+1* minus last press of section *k* (sections ordered by first press); hold = `RELEASE_TIME − PRESS_TIME`.
- Within-sentence press-to-press: n=4173; min 16; p10 88; p25 124; p50 171; p75 248; p90 396; p95 553; p99 934; max 2025 ms; share>1 s 0.0072; share>2 s 0.00024; share>5 s 0. Per-file medians: 168, 128, 271, 160, 204, 143 ms.
- Between-sentence gap: n=84; min 1480; p10 1862; p50 2780; p90 7297; p99 29002; max 32743 ms; share>1 s 1.0; share>2 s 0.83; share>5 s 0.20 (includes reading the next stimulus; the test presents one sentence at a time).
- Hold: n=4263; p50 103; p90 176; p99 328; max 1360 ms.
- Population (from `metadata_participants.txt`, 168,594 rows): `KEYBOARD_TYPE` counts laptop 91,250; full 73,759; small 1,886; on-screen 1,699. Per-participant `AVG_IKI` (ms): p10 133.8; p50 208.8; p90 381.0; p99 630.0 (n=168,594); restricted to `full`+`laptop`: n=165,009, p50 208.0, p90 378.5.

**Coverage.**
- T1: covers. Object: key-down and key-up timestamps (ms, JavaScript clock in a browser) per keystroke; unit ms; statistic: raw per-event, so any distribution can be derived (I derived the above); scope: transcription of 15 given English sentences in a web typing test, one sentence at a time; population: 168,594 online volunteers (self-reported keyboard type: 98% laptop/full). Pauses: within-sentence intervals only; between-sentence gaps mix reading time with the test's Enter/Next transition. Licence: non-commercial with attribution (readme.txt:21).
- T2, T3, T4, T5: does not cover (no application/CPU data).
- T6: does not cover (one task, one web page).
- T7: does not cover; usable as a replay source (raw timestamps).

**One observation?** One dataset, one task, one web application (the typing test); machine not named (participants' own); subjects anonymised IDs; window: 15 sentences per participant, collection period not stated in the copies read.

---

### S3-howwetype — HOW-WE-TYPE dataset (Feit, Weir, Oulasvirta, CHI 2016), Zenodo 4047775

**Citation.** Feit, A. M., Weir, D., Oulasvirta, A. (2016). How We Type: Movement Strategies and Performance in Everyday Typing. CHI '16, 4262–4273. doi:10.1145/2858036.2858233. Dataset: Zenodo record 4047775, doi:10.5281/zenodo.4047775, publication_date 2016-05-05, licence id `cc-by-nc-4.0` (Zenodo metadata). Project page `https://userinterfaces.aalto.fi/how-we-type/`.

**Copy read.** Zenodo API JSON `https://zenodo.org/api/records/4047775` → `zenodo4047775.json` SHA-256 `b794aa3f0302607c58f3db4ebf932ef36469472746850be54e6dbf3927c2bd70`; `Readme.txt` (6,827 B, Zenodo MD5 `58b5e068625bbfe06af1551d8fa3d85f`) → SHA-256 `4d62ebde494ead2a5ddbef0fafe4a3a49ff579e10c8216eaf5340f471221252c`; `Typing data v2.0.zip` (386,519 B, Zenodo MD5 `722f56877a6cc03d1ba7cdf8af48e183`, verified) → SHA-256 `c35a17c2c6ffaf0c8a044d60e99b25a7e3cedfe16bd24eecbb70304c3b47c85d`; project page → `hwt.html` SHA-256 `6105b15688d70f405ea661cce36b9ef8d24f39394a358d99ba16a3b110c197e7`. Not downloaded: `Motion Capture.zip` (981 MB), `Eye tracking.zip` (15.5 GB), `Reference video.zip` (29.3 GB).

**Verbatim passages.**
- Zenodo description: "Note: updated version of this dataset contains cleaned up typing data where unused (and incorrect) derivative columns were removed. You can derive these from the raw data yourself." … "This dataset contains motion capture, keylog, eye tracking, and video data of 30 participants, transcribing regular sentences." … "The dataset is free for non-commercial use. Please cite the above work." … "Note that participants wrote in either Finnish or English."
- `Readme.txt:6`: "It contains typing data of 30 participants typing regular sentences."
- `Readme.txt:13`: "NOTE: this version of the dataset does not contain data of the conditions "random" and "mix". Please contact feitanna@gmail.com for questions."
- `Readme.txt:19`: "You are free to use this data for non-commercial use in your own research with attribution to the authors."
- `Readme.txt:68-70`: "- Typing data:" / "  recorded keypresses at a sample rate of 40 ms," / "  contains the log data extended with the executing finger."
- `Readme.txt:153-154`: "	input_time: long" / "	the timestamp of the keypress"; `Readme.txt:166-167`: "	iki: int" / "	the inter-key interval, that is the time between the last and the current keypress."
- `Typing data v2.0/106194_log_Sentences_1438250399_matched.txt:1-2`: "input_time	user_id	input_index	iki	key_symbol	finger	transcribed	stimulus" / "1438250401.437	106194	0	0	Shift_R	R_Ring	Do we need the discuss ?	Do we need to discuss?"
- Project page, "The HOW-WE-TYPE Dataset": "Keypress data: symbol, time, and inter-key interval for every keypress, annotated with the finger used to type a key".

**My computation.** All 30 files in `Typing data v2.0.zip` (36,955 rows, 30 `user_id`s). `iki` column for rows with `input_index>0`: n=35,456; min 0; p10 92; p50 155; p90 342; p99 842; max 5180 ms; share>1 s 0.0053; share>2 s 0.0002. Cross-check with `input_time` differences ×1000 within the same `stimulus` and `input_index>0`: n=35,456; p50 156; p90 343; p99 842 (min −8 ms: timestamps are not strictly monotone). Stimulus-boundary gaps (difference across a change of `stimulus`): n=1,469; p10 811; p50 1217; p90 2184; p99 3420; max 87,579 ms; share>1 s 0.70. Most frequent integer `iki` values: 125 (5,127×), 187, 155, 156, 62, 93, 94, 92 — i.e. multiples of ~31 ms, consistent with a coarse clock ("sample rate of 40 ms", Readme.txt:69, is the source's own statement of resolution; my histogram suggests ~31 ms quantisation, not 40).

**Coverage.** T1: covers — keypress timestamps (s, three decimals) and `iki` (ms) per keypress; transcription of sentences; 30 lab participants, one keyboard (Swedish/Finnish layout), motion-capture setting; resolution coarse (see above); licence CC-BY-NC-4.0 / non-commercial with attribution. T2–T7: does not cover.

**One observation?** One lab study, one keyboard, one transcription task; subjects anonymous IDs; window: per-participant session, timestamps in July–September 2015 (from the Unix timestamps in file names, e.g. 1438250399 = 2015-07-30).

---

### S3-cmu-keystroke — CMU keystroke-dynamics benchmark (Killourhy & Maxion, DSN 2009)

**Citation.** Killourhy, K. S., Maxion, R. A. (2009). Comparing Anomaly-Detection Algorithms for Keystroke Dynamics. DSN-2009. Dataset page `https://www.cs.cmu.edu/~keystroke/`.

**Copy read.** Page HTML → `cmu.html` SHA-256 `d824cb2169b158f545a2b7537c4ab00422ccea6b6452fc99e437152d7ad9efd5`; `DSL-StrongPasswordData.csv` (4,669,935 B; page-stated MD5 `470235f96568f28f9ea0da62234ec857`, verified) → SHA-256 `b11d23538b1865fa6ecf4e8b78567caa312e9c1027604bb022fcc6ad7eaa7a33`. Accessed 2026-09-13.

**Verbatim passages** (page text; section "2. The Data" and its Q2-1):
- "The data consist of keystroke-timing information from 51 subjects (typists), each typing a password (.tie5Roanl) 400 times."
- "We built a keystroke data-collection apparatus consisting of: (1) a laptop running Windows XP; (2) a software application for presenting stimuli to the subjects, and for recording their keystrokes; and (3) an external reference timer for timestamping those keystrokes."
- "Whenever the subject presses or releases a key, the software application records the event (i.e., keydown or keyup), the name of the key involved, and a timestamp for the moment at which the keystroke event occurred. An external reference clock was used to generate highly accurate timestamps. The reference clock was demonstrated to be accurate to within ±200 microseconds (by using a function generator to simulate key presses at fixed intervals)."
- "All subjects typed the same password, and each subject typed the password 400 times over 8 sessions (50 repetitions per session). They waited at least one day between sessions, to capture some of the day-to-day variation of each subject's typing."
- "If the subject makes a typographical error, the application prompts the subject to retype the password. In this manner, we record timestamps for 50 correctly typed passwords in each session."
- `DSL-StrongPasswordData.csv:1`: "subject,sessionIndex,rep,H.period,DD.period.t,UD.period.t,H.t,DD.t.i,UD.t.i,H.i,DD.i.e,UD.i.e,H.e,DD.e.five,UD.e.five,H.five,DD.five.Shift.r,UD.five.Shift.r,H.Shift.r,DD.Shift.r.o,UD.Shift.r.o,H.o,DD.o.a,UD.o.a,H.a,DD.a.n,UD.a.n,H.n,DD.n.l,UD.n.l,H.l,DD.l.Return,UD.l.Return,H.Return"
- No licence text appears on the page; it asks for citation of the paper ("we ask authors who find this web resource useful provide a citation to the original paper").

**My computation.** `DSL-StrongPasswordData.csv`, all 20,400 rows (51 subjects × 400), the 10 `DD.*` columns (down-down latency in seconds): n=204,000; min 0.0011; p5 0.0779; p10 0.0945; p25 0.1284; p50 0.1911; p75 0.3007; p90 0.4623; p95 0.6021; p99 1.0402; p99.9 2.0394; max 25.9873 s; mean 0.2492; share>0.5 s 0.0828; share>1 s 0.0114; share>2 s 0.00105; share>5 s 0.000064. The 11 `H.*` hold columns: n=224,400, p50 0.0861 s, p90 0.1286 s. `UD.*` (up-down): min −0.2358 s; share<0 (rollover) 0.108.

**Coverage.** T1: covers — feature table only (no raw timestamps): hold, down-down and up-down latencies (s, 4 decimals) for each of 10 keystrokes of one fixed password; population 51 university-community typists; task: password entry, erroneous repetitions discarded; pauses: only within-password. T2–T7: does not cover.

**One observation?** One apparatus (a Windows XP laptop with external reference timer), one task, 51 subjects, 8 sessions each; window not dated in the copies read.

---

### S3-keyrecs — KeyRecs keystroke dynamics dataset (Zenodo 7886743)

**Citation.** KeyRecs: Keystroke Dynamics Dataset, Zenodo record 7886743, doi:10.5281/zenodo.7886743, publication_date 2023-05-02, licence `cc-by-4.0`; data article doi:10.1016/j.dib.2023.109509 (not opened).

**Copy read.** Zenodo API JSON → `keyrecs.json` SHA-256 `33d83ba06a44eb901075aaa58fb3537b377c5560d5c84ba3e7521fb2f67358b4`; `free-text.csv` (25,402,938 B; Zenodo MD5 `a5ca6fcb0970cfdcd8eb958b3fe9f22a`, verified) → SHA-256 `e38362914461c73a7ae6f25ac59304801f1324363d00ca00e059ac36e922c196`; `demographics.csv` → SHA-256 `2cd458ee6047707776e68223507c38fba231bf75510b11a2264e9e39e6d5fd87`. `fixed-text.csv` (5,676,298 B) not downloaded.

**Verbatim passages.** Zenodo description: "It contains fixed-text and free-text samples of user typing behavior, obtained in a study with 100 participants of 20 different nationalities performing password retype and transcription exercises." / "The samples consist of inter-key latencies computed by measuring the time between each key press and release during an exercise, following a digraph model." `free-text.csv:1`: "participant,session,key1,key2,DU.key1.key1,DD.key1.key2,DU.key1.key2,UD.key1.key2,UU.key1.key2 ,"; `free-text.csv:2-3`: "p001,1,W,Shift,0.15,-0.796,0.166,-0.946,0.016," / "p001,1,Shift,e,0.962,1.148,1.255,0.186,0.293,". `demographics.csv:1-2`: "participant,handedness,age,gender,nationality" / "p001,Right-Handed,51,Male,Portugal".

**My computation.** `free-text.csv`, all 562,583 data rows (99 distinct `participant`, sessions 1: 278,186 rows, 2: 284,397), column `DD.key1.key2` (seconds, 3 decimals): n=562,385 numeric; min −568.083; p10 0.082; p50 0.174; p90 0.528; p99 1.649; max 1712.727 s; share>1 s 0.0276; share>2 s 0.0079; share>5 s 0.0043. Negative and >1000 s values exist (unexplained in the copies read; the data article was not opened).

**Coverage.** T1: covers — digraph latencies (s) for a transcription ("free-text") exercise, 99–100 participants, two sessions; no raw timestamps; task/application/platform not stated in the copies read. T2–T7: does not cover.

**One observation?** One study; machines, application and dates not named in the copies read.

---

### S3-inputlog-ct-corpus — Inputlog Copy Task Corpus (Zenodo 5803401) and Inputlog Copy Task software (Zenodo 2908966)

**Citation.** Van Waes, L. et al., "Inputlog Copy Task Corpus: Exploring and defining typing skills", Zenodo 5803401, doi:10.5281/zenodo.5803401, version 1.05, publication_date 2021-12-24, licence `cc-by-4.0`. Software: "lvanwaes/Inputlog-Copy-Task: Inputlog Copy Task", Zenodo 2908966, doi:10.5281/zenodo.2908966, v1.0.0, 2019-05-18, licence id `other-open`, GitHub release archive `lvanwaes/Inputlog-Copy-Task-v1.0.0.zip` (1,528,688 B; not downloaded). Method paper doi:10.5334/jors.234 (not opened).

**Copy read.** `zenodo5803401.json` SHA-256 `ad65fb81f55fc74e064a496626130724bbce5e323b572fe5ef89f7be3f1d4946`; `zenodo2908966.json` SHA-256 `60d47f1ca33b2edae4a38834a6b179729f6d2f9b780877f2b10c53a63c81078a`; `sub-dataset_EN_21-25year.zip` (336,637 B; MD5 `096cdbd402d4f9ba784a3f335f9fbc1a` verified) SHA-256 `94dddf22e00761843ea2d2c3f26ee59fce71e3932c94fd6f43e39638d894f90d`.

**Verbatim passages.** Zenodo 5803401 description: "Tapping task — press the ‘d’ and ‘k’ key alternatively during 15 s / Sentence — copy a sentence during 30 s / Word combination 1 — copy a combination of three words seven times / … / Consonant groups — copy four blocks of six consonants once" (table rendered as text); "We are happy to make a multilingual corpus available (open access) that currently consists of more than 5000 copy tasks."; "The selection can be downloaded in different formats and levels of aggregation (from raw idfx to synthesized analysis)."; "A subset of the total corpus has been uploaded here. The subset contains a dataset of about 500 tests (English | 21-25-year-olds)." Facts and figures: "Dutch 3130 files / English 1163 files / German 281 files / French 201 files / Other 378 file".
- Zip contents (46 files, 871,362 B): `corpus/data/session.csv` (491 data rows), `corpus/data/components/{tapping,sentence,words1..4,consonants}.csv`, `adjacency/`, `frequency/`, `hands/`, `repetition/`, `trials/`.
- `corpus/data/session.csv:1`: `"id","uuid","language","age","gender","session","keyboard","test_group","experience","handedness","computer","familiarity","browser","disorder","education","repetition","correctness","cpm","score"`
- `corpus/data/components/sentence.csv:1-2`: `"id","targetted","non_targetted","cpm","median","stdev","logmean","mean_iki"` / `216,102,1,367,136,120.5,142.7,163.4`

**Coverage.** T1: covers only in aggregate — the Zenodo subset holds per-test summary statistics of inter-key intervals (`median`, `stdev`, `logmean`, `mean_iki`, in ms per component), not per-event timestamps; population ~491 English-language tests by 21–25-year-olds (web copy task, `computer` = desktop/laptop field present); raw `idfx` event files are advertised only through the interactive dashboard (`https://inputlog-analysis.uantwerpen.be/expert`, not opened). T2–T7: does not cover.

**One observation?** One task battery across many participants; machines not named; browser field per session.

---

### S3-osf-y3p4d — OSF "Modelling typing disfluencies as finite mixture process" (copy-task `ct.csv`)

**Citation.** OSF project y3p4d, title "Modelling typing disfluencies as finite mixture process", created 2020-04-29, modified 2022-05-10, licence CC0 1.0 Universal (OSF licence object 563c1cf88c5e4a3877f9e96c). Data file `data/ct.csv` (86,534,920 B, modified 2020-04-29), download `https://osf.io/download/wp6k4/`. Manuscript files present (`manuscript.pdf`, `markdown/manuscript.Rmd`) but not opened (S1 territory).

**Copy read.** `osf_y3p4d.json` (node) SHA-256 `88bbc507c154f1442beabe5c9175943598b307e0e6d64b28e20b72caeaa8308d`; `osf_y3p4d_files.json` `088c318b85a7b74e5618d78257958ca1dd12f7c9c685b843ed9caa890b3aa4bf`; `osf_data.json` (data folder list) `8ce7d3dd8a3cafb064d64dd297c6b78002142f54426f0e53eebb0ac4af60fe27`; `ct.csv` raw SHA-256 `6cc46981ec789a977943f79842ad4ab54898341aca14e654ec3459089e189dae`, stored as `ct.csv.gz`.

**Verbatim passages.** Node description: "R and Stan code for a statistical analysis of copy-typing data with focus on keyboard typing disfluencies. In particular, typing disfluencies were modelled as the result of a mixture of distributions." `ct.csv:1-3`: "bigram,component,subj,IKI,target,logfile,session,sex,age" / "dk,Tapping,1206,590,1,20170409opvdutch09042017idfx,1,female,56" / "kd,Tapping,1206,390,1,20170409opvdutch09042017idfx,1,female,56". The `logfile` values end in `idfx` (Inputlog's file type), i.e. these are Inputlog copy-task logs.

**My computation.** `ct.csv`, 1,447,310 data rows; 1,662 distinct `subj`; 2,046 (subj, session) pairs; 2,066 distinct `logfile`. `IKI` (integer ms) by `component`: HF n=845,247 p50 128 p90 232 p99 899 max 38,713, share>1 s 0.0080; Tapping n=275,508 p50 101 p90 152 p99 312; Sentence n=221,413 p50 136 p90 226 p99 816 max 41,736, share>1 s 0.0064; LF n=62,123 p50 235 p90 648 p99 1,736, share>1 s 0.037; Consonants n=43,019 p50 389 p90 1,315 p99 3,170, share>1 s 0.172, share>2 s 0.036. All rows: p50 126, p90 261, p99 1,120 ms, share>1 s 0.0126. `target` column: 1,385,813 rows `1`, 61,497 rows `0` (meaning not stated in the copies read).

**Coverage.** T1: covers — per-bigram inter-key interval (ms) for copy-typing components, 1,662 subjects (Dutch-language copy task judging by the logfile names), with subject sex/age; no absolute timestamps, no inter-sentence pauses (components are timed 15–30 s blocks). Licence CC0. T2–T7: does not cover.

**One observation?** One corpus of copy-task logs; machines/applications not named (browser-based Inputlog copy task per S3-inputlog-ct-corpus).

---

### S3-balabit — Balabit Mouse Dynamics Challenge data set (2016)

**Citation.** Fülöp, Á., Kovács, L., Kurics, T., Windhager-Pokol, E. (2016). Balabit Mouse Dynamics Challenge data set. `https://github.com/balabit/Mouse-Dynamics-Challenge` (README "Citation" section, lines 52–54).

**Copy read.** `README.md` (raw.githubusercontent, master) SHA-256 `68736371d2ed76a310cd246dcd8509171ef8f2cf161dccb0d2cdce2be0684f41`; git clone HEAD `d00d6f779254a2a917deeab4a5b7a9e8643bd91e` (commit date Fri Sep 21 14:39:33 2018 +0200), tree listing saved (`git-ls-tree.txt`, 1,678 paths: `README.md`, `public_labels.csv`, `training_files/user{7,9,12,15,16,20,21,23,29,35}/session_*` (65 files), `test_files/…`); one session extracted: `training_files/user12/session_2144641057` (1,349,384 B, 30,288 lines) → SHA-256 `a012c3f96ec71505da6a55afdf14b318658d394663dd8ae4931df2f0a2508297`. No LICENSE file in the tree.

**Verbatim passages.**
- `README.md:16`: "During their work, these users usually log in to remote servers with their remote desktop client. A network monitoring device is set between the client and the remote computer that inspects all traffic as described by the RDP protocol. This includes the mouse interactions of the user that is transmitted from the client to the server during the remote session."
- `README.md:28`: "The 'training_files' folder contains 10 folders, one for every user account in the system. In each of these folders, you are given the data of a few remote sessions that are known to be carried out by the legal owners of the respective user accounts."
- `README.md:33-34`: "- *record timestamp*: elapsed time (in sec) since the start of the session as recorded by the netork monitoring device" / "- *client timestamp*: elapsed time (in sec) since the start of the session as recorded by the RDP client"
- `README.md:48`: "Although this data set is offered as benchmark data for detecting illegal account usages, during its creation no such misuses were carried out. All recorded data reflect work executed during authenticated remote sessions that have not been hijacked. The attacks are imitated. For each user, in order to simulate illegal usage of his/her account, data from other users are artificially mixed into the test data of said user. Since all users engage in the same kind of unspecified administative tasks, the data from the artificial attackers do not reflect malicious activities."
- `training_files/user12/session_2144641057:1-3`: "record timestamp,client timestamp,button,state,x,y" / "0.0,0.0,NoButton,Move,1043,410" / "0.231999874115,0.0939999999828,NoButton,Move,1024,410"

**My computation.** All 7 `training_files/user12/session_*` files (246,824 rows; summed client-clock span 111,668 s). Consecutive `client timestamp` differences: n=246,817; p10 0.047; p50 0.109; p90 0.421; p99 3.713; max 2,214.6 s; share>1 s 0.037; share>10 s 0.004; share==0 0.0945. Move→Move only: n=200,632; p10 0.093; p50 0.109; p90 0.358 s. Fractional parts of the differences cluster on multiples of ≈0.0155 s (0.014, 0.015, 0.016, 0.029, 0.045, 0.046, 0.062, …), i.e. the RDP client clock ticks at ~1/64 s.

**Coverage.** T1 (pointer): covers — per-event mouse timestamps (s) with button/state/x/y for real office work, but as transmitted over RDP (network-side and client-side clocks, ~15.6 ms resolution, coalesced motion), 10 users, sessions of hours; the receiving application is a remote desktop, not a local GUI app. T2–T7: does not cover.

**One observation?** One deployment (Balabit's RDP monitoring), 10 users, machines not named, sessions 2016 or earlier (not dated in the copies read).

---

### S3-dfl — DFL Mouse Dynamics Data Set (Antal & Dénes-Fazakas, 2018)

**Citation.** Antal, M., Dénes-Fazakas, L. (2019). User Verification Based on Mouse Dynamics: a comparison of public data sets. SACI 2019, pp. 143–147 (listed on the page). Page `http://www.ms.sapientia.ro/~manyi/DFL/DFL.html` (fetched as `https://www.ms.sapientia.ro/~manyi/DFL.html`).

**Copy read.** `DFL.html` SHA-256 `51fe180bac261b4f15da01634f216283e5f9dc3fa4f38680ec3afa70dd6ce3df`; `DFL/User1.zip` (17,124,379 B; 31 CSV files, 81,662,997 B unpacked) SHA-256 `fdc7eb0bd53db69c3a69b634a1720f3f913e87ace93bedbb475c6359d1b92d72`.

**Verbatim passages** (page text): "Date: April 7. 2018 - November 15. 2018" / "Number of subjects: 21 (15 male, 6 female)" / "Controlled Acquisition: No" / "Computers: 1 desktop, 20 laptops; touchpad and external mouse, sometimes both" / "Raw data format (similar to Balabit data set available here)" / "Timestamp / Button (Left, Right, NoButton) / State (Move, Pressed, Released, Drag) / x coordinate / y coordinate". No licence statement on the page. `User1/2018_04_23__18_27_46.CSV:1-2`: "client timestamp,button,state,x,y" / "10856,NoButton,Move,369,1049".

**My computation.** All 31 CSVs of User1 (2,682,238 events; `state` counts: Move 2,548,117; Drag 63,107; Scrool 45,649; Pressed 12,685; Released 12,680). Consecutive `client timestamp` differences in the file's raw units (the page does not state the unit; values are consistent with milliseconds): n=2,682,207; min 0; p10 7; p50 8; p90 17; p99 448; max 2,814,538; share>100 units 0.0354; share>1,000 units 0.00506; share>10,000 units 0.00079; no negative differences. Summed per-file span 227,508,156 units (≈63 h if ms).

**Coverage.** T1 (pointer): covers — raw per-event mouse timestamps, uncontrolled everyday use on 21 personal computers (Java logger), 2018; unit of timestamp not documented on the page. T2–T7: does not cover.

**One observation?** 21 subjects, own laptops/desktop, April–November 2018; applications not logged.

---

### S3-shen-mouse — Chao Shen "Mouse-Behavior Data for Static Authentication" (figshare 5619313)

**Citation.** Shen, C., Cai, Z., Guan, X., Maxion, R. — accompaniment to "Performance Evaluation of Anomaly-Detection Algorithms for Mouse Dynamics" (Computers & Security 2014). figshare article 5619313, doi:10.6084/m9.figshare.5619313.v1, published 2017-11-20, licence CC BY 4.0; files `shen-static.zip` (57,648,224 B, MD5 `d6d44baf1dba965e6eddf231dd98ec15`, not downloaded) and `README.pdf` (423,906 B).

**Copy read.** figshare API JSON `figshare5619313.json` SHA-256 `c06750e8f4952034b2257f27345d2c89d9e1847f0fffb5702de055babbd3003d`; `README.pdf` SHA-256 `9af2402d1022987d71592a0d41432ee6f6aa7eeebbd4747edbc055398253013d`.

**Verbatim passages.** figshare description: "The data consist of mouse dynamics information from 56 subjects, each of who accomplish a fixed mouse ­operating pattern 200 times." README.pdf (a 2015-11-04 print of `http://nskeylab.xjtu.edu.cn/people/cshen/data-sets/behavior-data-set/`), page 1: "This webpage is a shared data set for mouse dynamics collected under a tightly-controlled environment."; page 2, "2. The Data": "The data consist of mouse dynamics information from 56 subjects, each of who accomplish a fixed mouse-operating pattern 200 times." and "Q1: How were the data collected? TBA." / "Q2: How are the data structured? What do the column names mean? TBA."

**Coverage.** T1 (pointer): covers only a fixed, controlled mouse-operation pattern (not real desktop use); schema undocumented ("TBA"). T2–T7: does not cover. Data file not opened.

---

### S3-swell-kw — SWELL Knowledge Work dataset (Koldijk et al., ICMI 2014), DANS doi:10.17026/dans-x55-69zp

**Citation.** Koldijk, S., Sappelli, M., Verberne, S., Neerincx, M., Kraaij, W. (2014). The SWELL Knowledge Work Dataset for Stress and User Modeling Research. ICMI 2014. Data: DANS Data Station SSH, doi:10.17026/dans-x55-69zp, version 4 (releaseTime 2025-06-04), dateOfDeposit 2014-08-27, licence CC-BY-NC-SA-4.0. Project page `http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html`.

**Copy read.** `Dataset.html` SHA-256 `9f3df722d7d45e019f1815d700a042262d16096b102f4f3af7775f28b7cc2a75`; Dataverse API JSON `dans.json` (919 files listed) SHA-256 `fa6e6ee01d0246d4864df69744ca65453b72330acc74f2c272ed3538cbec7c3e`; two uLog XML files downloaded via `https://ssh.datastations.nl/api/access/datafile/171735` (`a_pp2_c1_uLog_20120919_125648.xml`, 175,174 B, SHA-256 `b066e4a691915004ffc30c812d914ef952ff7b8a49949f6468a75b608435749d`) and `/171499` (`a_pp16_c2_uLog_20121015_143724.xml`, 2,037,251 B, SHA-256 `83cf6703096808cb69a770df31f9e51653a6746395477cad78adc63f93719489`). No access request was required (`fileAccessRequest: False`).

**Verbatim passages.**
- Project page: "The SWELL-KW dataset contains data from 25 participants (~3 hours each), for working under 3 conditions: neutral, interruptions and time pressure (plus a relax phase)." Table row: "Computer interactions — uLog output & Parsed selection of data — Mouse (3) Keyboard (7) Applications (2)".
- DANS description (dsDescription[0]): "The dataset was collected in an experiment, in which 25 people performed typical knowledge work (writing reports, making presentations, reading e-mail, searching for information). We manipulated their working conditions with the stressors: email interruptions and time pressure. A varied set of data was recorded: computer logging, facial expression from camera recordings, body postures from a Kinect 3D sensor and heart rate (variability) and skin conductance from body sensors."
- `a_pp2_c1_uLog_20120919_125648.xml:1-12`: `<?xml version="1.0" encoding="utf-8"?>` / `<Log>` / `<Event>` / `<EventType>Other</EventType>` / `<EventAction>Window Activated</EventAction>` / `<TimeStamp>2012-09-19T10:56:48.3384245Z</TimeStamp>` / … / `<EventDescription>Window "Noldus IT - uLog 3.2" activated.</EventDescription>`; a keyboard event in `a_pp16_c2…xml` (around line 2153): `<EventType>Keyboard</EventType>` / `<EventAction>special key</EventAction>` / `<TimeStamp>2012-10-15T12:47:37.6634665Z</TimeStamp>` / … / `<KeyboardValue>Return</KeyboardValue>` / … / `<ControlApplication>iexplore</ControlApplication>` / `<ControlWindowText>Google - Windows Internet Explorer</ControlWindowText>`.

**My computation.** `a_pp16_c2_uLog_20121015_143724.xml`: 2,349 `<Event>`; `EventType` counts: Other 1,145, Keyboard 1,124, Mouse 80; (`EventType`,`EventAction`): ("Keyboard","character") 799, ("Keyboard","special key") 307, ("Keyboard","key combination") 18, ("Other","Keyboard focus changed") 893, ("Other","Window Activated") 103, ("Mouse","clicked") 58, ("Mouse","dragged") 11, ("Mouse","wheel turned") 9. Keyboard events by `Control/ControlApplication`: WINWORD 903, OUTLOOK 164, iexplore 57. Inter-keystroke intervals (ms, from `<TimeStamp>`, consecutive keyboard events within the same application): WINWORD n=898 p10 10, p50 191, p90 1,577, p99 28,116, share>1 s 0.153, share>5 s 0.052; OUTLOOK n=162 p50 172, p90 752, p99 3,663, share>1 s 0.068; iexplore n=52 p50 228, p90 2,286, share>1 s 0.25. Timestamps carry 100 ns digits. `a_pp2_c1…xml` (175 KB) contains no Keyboard events (226 events: 184 Other, 42 Mouse). Mouse motion is not logged (only clicks/drags/wheel).

**Coverage.**
- T1: covers — per-keystroke timestamps (`TimeStamp`, 100 ns digits, wall clock) with the focused application and window title, for free composition (report writing in Word, e-mail in Outlook, browsing in IE) on Windows, 25 participants × ~3 h; mouse only as click/drag/wheel events, no motion. Pauses between bursts are present (share>1 s 15 % in Word in the file examined). Licence CC-BY-NC-SA-4.0.
- T6: covers partially — the same log distinguishes application per event (word processor vs mail client vs browser) so per-application inter-arrival can be compared (my numbers above for one participant-condition file); no CPU or wake data.
- T2, T3, T4, T5, T7: does not cover.

**One observation?** One lab experiment (TNO/Radboud, Sept–Nov 2012, Windows PCs running Word 2010/Outlook 2010/Internet Explorer per the `ControlWindowText`/`ControlApplication` fields), 25 participants; machine model not named.

---

### S3-clarkson2 — Clarkson University Keystroke Dataset II (CITeR page)

**Citation.** Murphy, C., Huang, J., Hou, D., Schuckers, S. (2017). Shared dataset on natural human-computer interaction to support continuous authentication research. IJCB 2017: 525–530 (as listed on the page). Page `https://citer.clarkson.edu/clarkson-university-keystroke-dataset-ii/`.

**Copy read.** `citer.html` SHA-256 `c65fc1a425f352cff026c8321516fdc04870b02248104dfef26954dc6b13fc28`.

**Verbatim passage** (page body): "This Clarkson II keystroke dataset was recorded in a user’s natural setting, thus is completely uncontrolled. The user may have used a desktop computer on campus or their own laptop. The dataset has been cleaned up to remove PII information. As a result, there are 101 data files one for each user. Each data file has three columns, from left to right: timestamp when a key is pressed or released, indicator of key press/release (1/0), and a key code. Note that the timestamp is measured in  a unit of  100 nanosecond (10 to the power of -7 second)."

**Coverage.** T1: would cover (raw per-event press/release timestamps at 100 ns units, uncontrolled natural use, 101 users) — but the page carries no download link and no licence; the data were not obtained. T2–T7: does not cover.

---

### S3-buffalo — University at Buffalo (CUBS) keystroke and mouse dataset — access page (curl 403)

**Copy read.** `https://www.buffalo.edu/cubs/research/datasets.html` returned HTTP 403 to curl (twice, http→https redirect). WebFetch returned a model summary that I saved as `webfetch-summary.txt` (SHA-256 in `SHA256SUMS.txt`); it is *not* a raw copy and is quoted here only for the access wording it reports: "To request this dataset, please contact shambhu@buffalo.edu and indicate the specific dataset." — status: request-only; not obtained; no verbatim raw page. T1–T7: nothing citable.

---

### S3-aalto-typing37k — "How do People Type on Mobile Devices?" 37k dataset (MobileHCI 2019) — off-platform

**Copy read.** `https://userinterfaces.aalto.fi/typing37k/` → `typing37k.html` SHA-256 `1ef0edc28da459e5ad1365d0220def3f69fb09e8aafd96084f13ca5484928adc`. Data links on the page: `data/raw_typing_data.zip`, `data/processed_typing_data.zip`, `data/csv_raw_and_processed.zip` (not downloaded).

**Verbatim passages.** "This paper presents a large-scale dataset on mobile text entry collected via a web-based transcription task performed by 37,370 volunteers. The average typing speed was 36.2 WPM with 2.3% uncorrected errors." / "SQL file with raw data as a .zip file (4.7 GB zipped, 43.4 GB unzipped). The data contains five tables: participants, test_sections, log_data, keystrokes, and sentences."

**Coverage.** T1: mobile touch keyboards only — off-platform for desktop; recorded for completeness. T2–T7: does not cover.

---

### S3-firefox-profiles — public Firefox Profiler profiles of typing lag (Bugzilla 1664556, 1593994, 1593115)

**Citation.** Bugzilla.mozilla.org bugs 1664556 ("Kaspersky Security Cloud causes typing lag on Facebook (old) in messenger text box and public/new post box", created 2020-09-11, Windows), 1593994 ("Very slow text input", created 2019-11-05, op_sys Linux), 1593115 ("Occasional laggy text input in latest Firefox Developer edition", created 2019-10-31, op_sys Linux x86_64). Profiles stored at `https://storage.googleapis.com/profile-store/<hash>` and viewable at `https://profiler.firefox.com/public/<hash>/`.

**Copies read** (JSON, gzipped for storage; raw SHA-256):
| hash | from | Firefox | OS (`meta.oscpu`) | CPUs (phys/logical) | raw size | raw SHA-256 |
|---|---|---|---|---|---|---|
| `5sxas21pj91fjpc5j2wp7b53yzm6p1ph1hjgnpg` | 1593994 c.15278588 (2021-02-23), "Firefox 85 – Linux - typing quickly on Twitter's tweet text input box" | rv:85.0 | Linux x86_64 (X11) | 2/4 | 8,078,736 | `afe205c1db87dab8f537648cb0a9a7762f4383969037dd31e24bc993fc54f36c` |
| `5haas106dgm7cvxrd48c9bmmewnceq3f1bcchvr` | same comment, "Firefox 85 – Linux - typing fast on Discord" | rv:85.0 | Linux x86_64 | 2/4 | 21,569,820 | `f81f0b243dac7751cddd031c325ab26f0c61b1766b350121674b12c1edb8a8f9` |
| `4fz2cgv4saezfepvgjn1aczws0e7cjb3xy360n0` | same comment, "Firefox 85 – Linux - typing fast on Slack" | rv:85.0 | Linux x86_64 | 2/4 | 19,207,831 | `49d6dfd1f6073f0ef3e123b6f12d2aa3deef11622dae5d28840d0a9d36f0838a` |
| `07735ce1e8acedac651fea42aca4874491216eb3` | 1593994 c.14473375 (2019-11-07) `https://perfht.ml/2CmlHnK` | rv:70.0 | Linux x86_64 | 4/8 | 27,933,265 | `c50b462087fa86afc61c9d7621fb0429e30d9336131dab505171632ffbb26bca` |
| `2ffa5d5bd8f42db623f1f488de1bea09b5d1b892` | 1593115 c.14460151 (2019-10-31) | rv:71.0 | Linux x86_64 | 6/12 | 7,366,354 | `44a9b9da81014b0dfdb4c56db1ef0d8046df5ab18a468a6090ed8bf2dbe95311` |
| `n7wxtce677dp0yzfk95k06ybceswxq08p79tjer` | 1664556 c.15032066 (2020-09-11) `https://share.firefox.dev/3kanAYe` | rv:80.0 | Windows NT 10.0 x64 | 8/16 | 24,608,905 | `03b3ef4b4b749f034dddb95fb1adc9dc5ac285c607e23322b0ee2ddf1e1e7cf4` |
Bugzilla REST comment JSON copies: `bz1593994_comments.json` `671e0f3148bd47a6d0f803f8eac37b44e5a2b98c6879f2eeda5bc53ef3a28db2`, `bz1593115_comments.json` `c1dd9b9517cd23646f792892a47b08183e5355e8bcd9bd0b2d17e463eb026ab5`, `bz1664556.json` `fee0fbf57713325666b5fed5101e39c956682d0346376c761af555f1b9c72db2`, bug metadata JSONs in folder.

**Verbatim passages.**
- Bug 1593994, comment 15278588 (2021-02-23T15:09:00Z, nekohayo@gmail.com): "Here is the profiling output from typing very fast on:  * Twitter: https://share.firefox.dev/37FMqf3 * Discord: https://share.firefox.dev/2MhovuJ * Slack: https://share.firefox.dev/3khBSrt  For the record: I already have webrender (all) force-enabled and the on-disk cache disabled to improve perform" (truncated at 300 chars in my extraction).
- Bug 1593994, comment 14473373 (2019-11-07T10:55:51Z, github@miggy.org): "Well, that didn't take long (he says typing painfully slowly here as well): https://profiler.firefox.com/from-addon/… The test case is basic" and comment 14473375: "Ah, it helps if I publish and cite that URL: https://perfht.ml/2CmlHnK".
- Bug 1593115, comment 14460151 (2019-10-31T20:39:28Z, jon@thesquareplanet.com): "User Agent: Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0  Steps to reproduce:  Typed into a text area on https://discordapp.com/, though I have observed the issue on other text areas as well (e.g., on GitHub).   Actual results:  Occasionally, Firefox will "freeze" for a few s" (truncated).
- Bug 1664556, comment 15032066 (2020-09-11T20:04:11Z, mstange.moz@gmail.com): "Indeed, lots of keypress latency: https://share.firefox.dev/3kanAYe Most of the time is spent in GC, triggered under GetLoginSelectors from a script from https://ff.kis.v2.scr.kaspersky-labs.com/ ."
- Profile `5haas…` `meta`: `product: Firefox`, `misc: rv:85.0`, `platform: X11`, `oscpu: Linux x86_64`, `version: 22`, `preprocessedProfileVersion: 33`, `interval: 1` (ms), `physicalCPUs: 2`, `logicalCPUs: 4`, `startTime: 1614065018844.1174`. Thread list (name/processName/processType/pid/tid): `GeckoMain Parent Process default 238561/238561`, `Renderer … 238624`, `Compositor … 238633`, four `DOM Worker` threads in the parent, `GeckoMain rdd 239046`, `GeckoMain WebExtensions tab 238706`, `GeckoMain Privileged Content tab 238907`, three `GeckoMain Web Content tab` processes (238752, 238745, 238654) each with DOM Worker threads. No `threadCPUDelta` array in any of the six profiles' `samples` tables (so no per-sample CPU time; only wall-clock markers and 1 ms stack samples).

**My computation** (marker tables; durations = `endTime − startTime` for phase-1 markers, or paired phase-2/phase-3 markers of the same name/eventType; v18 profiles use `data.interval` start/end). "Latency" is the profile's own `data.latency` field of DOMEvent markers (time from event creation to handler start).
- **Discord tab, Linux, Firefox 85** (`5haas…`, thread 17 `GeckoMain Web Content` pid 238654, 21.6 s): keydown handler n=232, p50 4.41, p90 11.48, p99 25.19, max 33.26 ms (share>10 ms 0.147); keypress n=232 p50 24.26, p90 61.37, p99 116.19, max 213.92 ms (share>100 ms 0.030); input n=232 p50 5.32, p90 13.42 ms; keyup p50 1.42 ms; keydown inter-start (typing rate as seen by the content process) n=231 p10 35.8, p50 63.1, p90 146.8, p99 261.4, max 297 ms; RefreshDriverTick n=306 dur p50 23.9, p90 52.8, p99 111 ms, inter-start p50 58.0, p90 119.7 ms; Styles n=2814 p50 0.00, p90 0.64 ms; Reflow n=453 p50 0.31, p90 1.55, max 42.5 ms; DisplayList n=302 p50 8.56, p90 18.6, max 101 ms; setTimeout callback n=35 p50 0.51, p90 15.1 ms; GCMinor n=8 p50 10.2 ms; LongTask n=72 p50 73, p99 186 ms; sum of Styles/Reflow/DisplayList/Rasterize/LayerBuilding marker time in the 100 ms after each keydown: p50 16.5, p90 31.6, max 82 ms. keydown latency (event queued before handling) p50 5,904 ms, p90 9,825 ms — the profile was taken while the tab was already several seconds behind. Parent-process main thread (thread 0): keydown handler p50 0.25 ms, p90 0.87 ms (n=232). Parent `Compositor` thread: `CompositeToTarget` n=914 inter-start p10 16.11, p50 16.37, p90 47.4 ms (≈60 Hz when busy), duration p50 0.03 ms.
- **Slack tab** (`4fz2…`, thread 18, pid 238745, 18.2 s): keydown p50 1.54 ms; keypress p50 54.9, p90 127.9, p99 220.9, max 255 ms (share>100 ms 0.217); input p50 0.59 ms; keydown inter-start p50 72.6, p90 176.8 ms (n=142); RefreshDriverTick dur p50 18.3, p90 41.8, max 460 ms; Reflow p50 9.16, p90 19.1 ms (n=108); setTimeout callback n=342, inter-start p50 1.84 ms; LongTask n=99, p50 78.7 ms.
- **Twitter tab** (`5sxas…`, thread 17, pid 238654, 4.2 s of typing): keydown p50 1.88 ms; keypress p50 29.8, p90 47.6, max 95.5 ms; input p50 24.7 ms; keydown inter-start p10 28.0, p50 48.3, p90 79.0, max 160 ms (n=81; a very fast burst); RefreshDriverTick dur p50 16.8 ms, inter-start p50 54.5 ms; DisplayList p50 4.94 ms; paint-marker sum within 100 ms after keydown p50 8.2, p90 14.0 ms.
- **Bug 1593994 first profile** (`07735…`, Firefox 70, Linux, thread 7 pid 4251, 19.8 s, unnamed text field): keydown p50 0.32 ms; keypress p50 3.94, p99 6.88 ms; input p50 2.56 ms; keydown inter-start p10 103, p50 200, p90 304, max 399 ms (n=81 — "typing painfully slowly", per the comment); RefreshDriverTick n=568, inter-start p10 16.05, p50 17.06, p90 56.6 ms (≈60 Hz), dur p50 3.38, p90 4.39 ms; Styles n=2652 p90 0.09 ms; Reflow n=501 p50 0.02 ms; DisplayList n=379 p50 0.53 ms; LayerBuilding n=374 p50 1.93 ms; setTimeout callback n=826 p50 0.07 ms. Parent `Compositor` thread: `Composite` n=402 dur p50 0.24 ms, inter-start p10 16.07, p50 17.07, p90 150.6 ms.
- **Bug 1593115** (`2ffa…`, Firefox 71, Linux, 0.5 ms interval, 1.3 s window, Discord text area): keydown p50 0.43 ms; keypress p50 8.12 ms; input p50 5.39 ms; LongTask n=6, p50 200.6 ms; keydown inter-start p50 213 ms (n=6).
- **Bug 1664556 (Windows, Firefox 80, Facebook tab, thread 19 pid 9388, 23.3 s)**: keydown n=81, p50 0.98 ms but p90 276.7, max 326 ms (share>100 ms 0.346 — the GC stalls the comment describes); keypress p50 4.00, p90 18.4 ms; keydown inter-start p50 104, p90 314 ms; RefreshDriverTick n=554 inter-start p10 12.6, p50 16.7, p90 79 ms, dur p50 0.60, p90 6.96 ms; setTimeout callback n=2804 (p50 0.05 ms; inter-start p50 0.08 ms — a 100 ms timer per the marker text "setTimeout handler with interval 100ms"); GCSlice n=556 p50 10.0 ms; GCMinor n=409 p50 1.53 ms; LongTask n=33 p50 255 ms. GPU-process `Compositor` thread: `Composite` n=341 dur p50 5.73, p90 9.56 ms, inter-start p10 16.58, p50 16.72 ms. `samples.eventDelay` on the content thread: p50 20.9, p90 225.6, max 519 ms.

**Coverage.**
- T1: covers, narrowly — keydown inter-arrival as received by a browser content process during short bursts of fast typing (Linux profiles: p50 48–73 ms while bursting; the 2019 profile p50 200 ms); one user per profile, no pauses beyond the ~20 s window.
- T2: covers, as wall-clock (not CPU) durations per keyboard event on the content thread and the parent thread, with paint-phase durations per refresh tick; Linux x86_64, Firefox 70/71/85, web apps (Discord, Slack, Twitter, unnamed). Handler durations exceed 1 ms in 78–100 % of keypress events, 10 ms in 100 % of keypress events on Discord/Slack/Twitter (Firefox 85) and 0 % in the 2019 profile; 100 ms in 3 % (Discord) and 22 % (Slack). CPU time per event is not in the profile (no CPU deltas); the 1 ms sampling only shows the thread is running.
- T3: covers — thread population of a Firefox instance (GeckoMain per process, Renderer, Compositor, DOM Workers, rdd, GPU process on Windows), timer-driven work (setTimeout callbacks: 100 ms timer on Facebook, 342 callbacks in 18 s on Slack), refresh-driver ticks at ≈16.7 ms when animating/painting and irregular (p90 47–210 ms) otherwise, compositor composites at 16.1–16.7 ms spacing when busy, GC slices as non-input wakeups. Scheduler-level wake gaps and per-schedule runtimes: not present (no sched data).
- T4, T5: does not cover.
- T6: partial — browser only; three different web applications differ in per-keypress handler time (Twitter p50 30 ms, Discord 24 ms, Slack 55 ms; 2019 unnamed page 4 ms).
- T7: does not cover.

**One observation?** Yes, per profile: one machine (not named beyond CPU count and OS string), one browser, one web application, one user, 1–23 s windows on the dates given.

---

### S3-perfetto-chrome — Perfetto example Chrome trace `chrome_example_wikipedia.perfetto_trace.gz` — off-platform (Android)

**Citation.** Perfetto UI example trace, URL constant `EXAMPLE_CHROME_TRACE_URL = 'https://storage.googleapis.com/perfetto-misc/chrome_example_wikipedia.perfetto_trace.gz'` in `google/perfetto` `ui/src/core_plugins/dev.perfetto.ExampleTraces/index.ts` (GitHub code search hit; file itself not opened). Object `Last-Modified: Mon, 14 Nov 2022 15:59:08 GMT`, `ETag: "d03b3b444dbcc31c9055e3fe79c6043d"`, 21,537,072 B.

**Copy read.** SHA-256 `7401f67e30cb025b113cef1db53d7e154705e688e33142f65fd7875df26f2cf0` (the served bytes are a raw Perfetto proto, not gzip, despite the name). Parsed with `trace_processor_shell` v57.2 via the `perfetto` Python package.

**Verbatim passages** (trace `metadata` table rows): `system_name = Linux`, `system_release = 5.10.107-android13-4-00004-gf0fe4f768061-ab8935229`, `android_build_fingerprint = google/oriole/oriole:13/TP1A.221005.002/9012097:userdebug/dev-keys`, `cr-os-name = Android`, `cr-os-version = 13`, `cr-num-cpus = 8`, `cr-cpu-brand = ARMv8 Processor rev 0 (v8l)`, `cr-gpu-gl-renderer = Mali-G78`, `tracing_service_version = Perfetto v25.0 (N/A)`, trace_config data sources `org.chromium.trace_event`, `track_event` (with `enable_thread_time_sampling: true`), `org.chromium.trace_metadata`, `linux.ftrace` (empty `ftrace_config {}`), `duration_ms: 30000`. `sched` table: 0 rows; `thread_state`: 0 rows; `slice`: 297,603 rows; `counter`: 454,993 rows; trace bounds 29,181.67 ms. Processes: 17145 `Browser`, 17241 `Renderer`, 17255 `GPU Process`, 18412 `Service: data_decoder.mojom.DataDecoderService`. Threads (name per process): Browser: `CrBrowserMain`, `Chrome_IOThread`, `NetworkService`, `ThreadPoolServiceThread`, 6× `ThreadPoolForegroundWorker`, `ThreadPoolSingleThreadSharedForeground1`, `ThreadPoolSingleThreadSharedForegroundBlocking0`, `MemoryInfra`, `HangWatcher`; Renderer: `CrRendererMain`, `Compositor`, `CompositorTileWorker1`, `CompositorTileWorkerBackground`, `Chrome_ChildIOThread`, `ThreadPoolServiceThread`, 4× `ThreadPoolForegroundWorker`, `HangWatcher`; GPU Process: `CrGpuMain`, `VizCompositorThread`, `Chrome_ChildIOThread`, `GpuWatchdog`, `ThreadPoolServiceThread`, 2× `ThreadPoolForegroundWorker`.

**My computation** (top-level `ThreadControllerImpl::RunTask` slices per thread; `thread_dur` is Chrome's sampled thread CPU time per task, wall `dur` the slice length; ms):
- `CrRendererMain`: n=1,490; wall p50 0.020, p90 2.50, p99 9.56, max 89.1 (share>1 ms 0.232, >10 ms 0.009); CPU p50 0.021, p90 2.37, p99 6.73, max 54.6; sum CPU 1.16 s over 29.2 s; task start inter-arrival p50 0.79, p90 10.2, p99 38.3 ms.
- `CrBrowserMain`: n=3,327; wall p50 0.019, p90 0.26, p99 1.22, max 51.4; CPU sum 0.42 s; inter-arrival p50 0.045, p90 4.97 ms.
- Renderer `Compositor`: n=4,009; CPU p50 0.049, p90 0.92, p99 1.69, max 3.12; sum 0.93 s; inter-arrival p50 0.165, p90 4.08 ms.
- `VizCompositorThread`: n=1,555; CPU p50 0.134, p90 0.99 ms; sum 0.51 s; inter-arrival p50 2.39, p90 6.62 ms.
- `CrGpuMain`: n=1,220; wall p50 0.39, CPU p50 0.30, p90 1.04 ms; sum 0.66 s.
- Input-related slice names present: `LatencyInfo.Flow` 2,768; `EventLatency` 393; `RendererCompositorQueueingDelay` 393; `InputRouterImpl::FilterAndSendWebInputEvent` 383; `RenderWidgetHostImpl::ForwardGestureEvent` 323 (touch/scroll gestures, no keyboard).

**Coverage.** T2/T3: covers the *thread organisation* and per-task CPU-time distribution of a Chromium browser, but on Android 13 (Pixel 6, touch scrolling of Wikipedia) — off-platform for a Linux desktop; no kernel scheduler data in the trace. T1, T4, T5, T6, T7: does not cover.

---

### S3-sysprof-gnome — sysprof captures attached to GNOME GitLab issues (gnome-text-editor#179, gtk#3435)

**Citation.**
- GNOME/gnome-text-editor issue 179, "Worse scrolling performance compared to GtkSourceView test app", opened 2021-10-09T19:10:39Z by `YaLTeR`, `https://gitlab.gnome.org/GNOME/gnome-text-editor/-/issues/179`; attachment `g-t-e.syscap` (`/uploads/b997169dd5ff0dc9674305890c0f5710/g-t-e.syscap`, 14,582,112 B).
- GNOME/gtk issue 3435, "Builder constraints demo window slow to shrink", opened 2020-12-04T08:26:10Z by `YaLTeR`, `https://gitlab.gnome.org/GNOME/gtk/-/issues/3435`; attachment `expanding.syscap` (`/uploads/f1f8aaf6492e275419ce0514a90dec9e/expanding.syscap`, 9,851,008 B). (`shrinking.syscap` not downloaded.)
- Format reference: `sysprof-capture-types.h` from `GNOME/sysprof` master via raw.githubusercontent (frame types `SYSPROF_CAPTURE_FRAME_SAMPLE = 2`, `PROCESS = 4`, `CTRDEF = 8`, `CTRSET = 9`, `MARK = 10`, `METADATA = 11`; header struct at lines 156–173, frame header lines 176–187, sample lines 231–239, mark lines 336–344).

**Copies read.** `g-t-e.syscap` SHA-256 `3b618b7a2e264064417c804849019ce4a51c27193218eb97c08128bdeac1ec63`; `expanding.syscap` `e6fd467243148b0e73e2520b3c08631922f1778e013ac259136d838bdbfc3179`; issue JSONs `gte_issue179.json` `f52a13abb40f319d14cbee7bff1a29791d858f2342ead7769e25bcc5857c56b6`, `gtk_issue3435.json` `18bce7484565b7c5a9c73197cd6d466af6871a80d0dd1e47c1ceba20024c4daf`; search JSONs; `sysprof-capture-types.h` (SHA in folder).

**Verbatim passages.**
- Issue 179 description: "For some reason, g-t-e achieves only about 70 FPS with quick scrolling which feels laggy, while the GtkSourceView test app achieves 100+ FPS and feels much smoother." / "- Fedora 35 Silverblue, GNOME Wayland." / "- AMD RX 580 GPU, AMD Ryzen 9 5900X CPU." / "- g-t-e https://gitlab.gnome.org/GNOME/gnome-text-editor/-/commit/2b345db18a8ff5cf32451fbfe6378e6f5f402191 from gnome-nightly Flatpak." / "Even with the default monospace font which is easier on the performance sometimes g-t-e scrolls at smooth 144 FPS and sometimes if I close and open it it inexplicably scrolls at 100 FPS."
- Issue 3435 description: "## Steps to reproduce / 1. Open Builder constraints `gtk4-demo` / 2. Make it wider, it's smooth / 3. Make it narrower, it's laggy" / "## Version information / Fedora 33, Wayland, d278afc85b3355ab8e5e4fd14705e0685f05a9c6".
- Capture headers (parsed): `g-t-e.syscap` version 1, little-endian, `capture_time` "2021-10-09T18:35:21Z", span 17.02 s; `expanding.syscap` `capture_time` "2020-12-04T08:17:08Z", span 11.14 s. Metadata frame `local-profiler` in `g-t-e.syscap`: "[profiler]\nwhole-system=true\nspawn=false\n…\n[source-0]\ngtype=SysprofProcSource\n\n[source-1]\ngtype=SysprofGovernorSource\ndisable-governor=false\n\n[source-2]\ngtype=SysprofSymbolsSource\n\n[source-3]\ngtype=SysprofPerfSource\n\n[source-4]\ngtype=SysprofHostinfoS" (truncated at 300 chars in my print). Counter definitions include "CPU Percent / Total CPU 0 / Total CPU usage 0" and "CPU Frequency / CPU 0 / Frequency of CPU 0" for each CPU. Process frame cmdlines include `/app/bin/gnome-text-editor --gapplicatio…` (pid 86039), `/usr/bin/gnome-shell` (pid 2006), `gtksourceview5-widget` (pid 85476), `install/bin/gtk4-demo` (pid 29894), `pool-gnome-shel` (pid 2397), `/app/extra/zoom/zoom` (pid 17089), `/usr/bin/pulseaudio --daemonize=no --log…` (pid 2402), `/usr/bin/Xwayland :0 -rootless -noreset …` (pid 2630), `'/app/discord/Discord --type=renderer --…` (pid 4313).
- Neither capture contains MARK frames (0 of type 10), so no GTK frame-clock marks; frame counts: `g-t-e.syscap` {SAMPLE 13,723; MAP 51,934; PROCESS 1,075; FILE_CHUNK 738; CTRSET 223; FORK 145; EXIT 66; OVERLAY 4}; `expanding.syscap` {SAMPLE 24,558; MAP 62,132; PROCESS 409; CTRSET 108; FILE_CHUNK 29}.

**My computation** (SAMPLE frames grouped by (pid, tid); a sample exists only when the thread is on-CPU under perf sampling, so consecutive-sample gaps ≤2 ms are treated as one on-CPU "episode" — an approximation, not a scheduler record):
- `g-t-e.syscap`, gnome-text-editor main thread (86039/86039), 7,223 samples in 17.0 s: sample gap p50 0.547 ms (sampling ≈1.83 kHz), p99 20.1 ms; 660 episodes; samples per episode p50 10, p90 22, p99 30, max 56 (≈5.5–30 ms on-CPU per episode at the observed sampling gap); gap between episodes p10 4.8, p50 8.8, p90 20.3, p99 33.4 ms. gnome-shell main thread (2006/2006): 1,759 samples; 1,676 episodes of p50 1 sample; inter-episode gap p50 6.9, p90 11.0 ms. Other sampled threads in the same 17 s: `gnome-shell` tid 2089 (152 samples), `polkitd` (315), `kgx` (96), `sysprofd` (83), `gtksourceview5-widget` (60), `Element` renderer (57).
- `expanding.syscap`, `gtk4-demo` main thread (29894/29894), 5,891 samples in 11.1 s: sample gap p50 0.374 ms; 464 episodes; samples per episode p50 7, p90 24, max 50; inter-episode gap p10 3.9, p50 5.98, p90 8.18, p99 45.2 ms. gnome-shell (2397 `pool-gnome-shel`, 5,250 samples): episodes 854, samples/episode p50 5, inter-episode gap p50 2.71, p90 4.2 ms. Zoom (pid 17089) threads 17486, 17225, 17089, 17223 with 1,177/748/492/352 samples; pulseaudio 517; Xwayland 504; Discord renderer 912 — all during a window resize on a GNOME Wayland desktop.

**Coverage.**
- T3: covers, approximately — a GTK4 text editor during fast scrolling and a GTK4 demo during window resize on Linux (Fedora 33/35, Wayland): the main thread wakes in bursts spaced ~6–9 ms (median) with ~5–30 ms on-CPU per burst (sample-count based), i.e. paint-cadence-driven, not input-driven; the compositor (gnome-shell) wakes ~every 3–7 ms with sub-ms work; audio server (pulseaudio) and a conferencing client (Zoom) appear as concurrent sampled threads. No thread names inside the app (sysprof PROCESS frames give the cmdline only), no scheduler wake gaps (perf samples, not sched events).
- T2: does not cover (no keyboard input in either capture; scrolling and resizing only).
- T4: partial — pulseaudio's main thread was sampled 517 times in 11.1 s in `expanding.syscap` (a CPU-time proxy of ≈0.19 s at ~0.37 ms/sample, my estimate), no period information.
- T5: partial — Zoom threads sampled (see above), no frame cadence information.
- T1, T6, T7: does not cover.

**One observation?** Yes: one machine each (issue 179: Ryzen 9 5900X + RX 580, Fedora 35 Silverblue, GNOME Wayland; issue 3435: Fedora 33, Wayland, hardware not named), one application (gnome-text-editor nightly commit `2b345db1…`; gtk4-demo at GTK commit `d278afc8…`), one user (`YaLTeR`), windows 17.0 s (2021-10-09 18:35:21Z) and 11.1 s (2020-12-04 08:17:08Z).

---

### S3-pipewire-pwtop — `pw-top` tables quoted in PipeWire GitLab issue descriptions

**Citation.** `https://gitlab.freedesktop.org/pipewire/pipewire/-/issues/<iid>` (the API `web_url` field renders as `/-/work_items/<iid>`); descriptions fetched via `https://gitlab.freedesktop.org/api/v4/projects/pipewire%2Fpipewire/issues?search=QUANT&in=description&scope=all&state=all&per_page=100&page=1..4` (accessed 2026-09-13; 39 issues contain a `S ID QUANT RATE WAIT BUSY` header). Copies: `search_pwtop_{1..4}.json` (SHA-256 `e77b2724387715ceb87e0f21686016614d50755206b49cef671da1ed2dda4fb4`, `f50add6c5e0a6ef8d91dae263edd940f068ffdd7c2ec6095946d558d4abfc033`, `7da90c2b43f47b6ecc0a39023c9c2d845f7d8a0666a3d6ec80819f3ff0c2d65b`, `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`), `issue_4875.json` `c66c49ed8bbedf8c5d9be33e4f80d5ad376c13dc6b346cf99a8c46b4992fe251`, `gl_pw_issues.json`. Issue notes/comments were not readable (401), and freedesktop `/uploads/` attachments returned 404 — only description text is cited.

**Verbatim passages** (issue `description` fields; the `WAIT`/`BUSY` columns are pw-top's per-node wait and busy times per cycle, `W/Q` and `B/Q` their ratio to the quantum — pw-top's own column meanings are S2's business; here only the numbers are recorded):
- Issue 3900, "USB Interface, audio latency drifts over time", created 2024-03-07T17:25:52Z:
  ```
  S   ID  QUANT   RATE    WAIT    BUSY   W/Q   B/Q  ERR FORMAT           NAME
  I   28     64  48000  45,9us   0,1us  0,03  0,00    0                  Dummy-Driver
  S   29      0      0    ---     ---   ---   ---     0                  Freewheel-Driver
  S   39      0      0    ---     ---   ---   ---     0                  Midi-Bridge
  R   88     64  48000 129,3us   0,0us  0,10  0,00    0    S24LE 4 48000 alsa_input.usb-Avid_Mbox-00.pro-input-0
  R   62    900  48000 113,9us   3,4us  0,09  0,00    1    F32LE 2 48000  + Firefox
  R  144      0      0   2,5us   1,9us  0,00  0,00    5    S24LE 4 48000  + alsa_output.usb-Avid_Mbox-00.pro-output-0
  R  128     64      0 114,2us  10,1us  0,09  0,01    0                   + jack_delay
  I   71      0      0   0,0us   0,0us  0,00  0,00    0    F32LE 2 48000 Firefox
  ```
- Issue 4662, "Choppy Bluetooth audio in Kodi after upgrade from 1.2.7 to 1.4", created 2024-04-21T21:15:58Z; description header lines: "- PipeWire version (`pipewire --version`): 1.4.2" / "- Distribution and distribution version (`PRETTY_NAME` from `/etc/os-release`): Arch Linux" / "- Desktop Environment: i3" / "- Kernel version (`uname -r`): 6.14.2-arch1-1" (year 2025 per `created_at` 2025-04-21T21:15:58Z):
  ```
  S   ID  QUANT   RATE    WAIT    BUSY   W/Q   B/Q  ERR FORMAT           NAME
  R   90    512  48000  44.0us  25.3us  0.00  0.00    0    S16LE 2 48000 bluez_output.XX_XX_XX_XX_XX_XX.1
  R   73    800  48000  22.1us   8.8us  0.00  0.00  222    F32LE 2 48000  + Kodi
  ```
- Issue 2845, "Different client buffer sizes (and required wake time)", created 2022-11-20T21:17:52Z:
  ```
  S   ID  QUANT   RATE    WAIT    BUSY   W/Q   B/Q  ERR FORMAT           NAME
  S   29      0      0    ---     ---   ---   ---     0                  Dummy-Driver
  S   30      0      0    ---     ---   ---   ---     0                  Freewheel-Driver
  R   31    512  48000  64.7us  10.2us  0.01  0.00    0     F32P 2 48000 null-audio-sink
  R   39    512  48000  13.8us  46.4us  0.00  0.00   82    S16BE 2 48000  + rtp-sink
  R   65   2048  48000  22.8us  18.9us  0.00  0.00  118    F32LE 2 48000  + Game
  R   69    512  48000 660.9us  30.1us  0.06  0.00    2    F32LE 2 48000  + Chromium
  ```
- Issue 4479, "ALSA lib pcm.c:8772:(snd_pcm_recover) underrun occurred", created 2024-12-30T11:04:29Z ("pw-dump with master version (1.3.0)"):
  ```
  R   53    512  44100 158.7us   4.5us  0.01  0.00    0    S32LE 2 44100 alsa_output.usb-SABAJ_SABAJ_USB_AUDIO-00.analog-stereo
  R   89    441  44100   6.2us   3.1us  0.00  0.00    0    S16LE 2 44100  + alsa_playback.wine64-preloader
  R   68    441  44100  95.1us  23.7us  0.01  0.00    0    S32LE 2 44100  + alsa_playback.wine64-preloader
  ```
- Issue 4796, "pipewire graph not activated when disabling tsched", created 2025-07-11T17:35:38Z: `R 58 1024 48000 296,0us 9,5us 0,01 0,00 0 S32LE 2 48000 alsa_output.pci-0000_0a_00.4.analog-stereo` / `R 60 0 0 20,3us 262,9us 0,00 0,01 0 + jack_mixer`.
- Issue 4374, "GStreamer pipewiresink plays back audio with delay and error count in pwtop increasing", created 2024-10-28T13:02:02Z ("PipeWire version (`pipewire --version`): 1.2.4", "Raspbian GNU/Linux 12 (bookworm)", "6.1.21-v8+ (Raspberry Pi 4B)"): `R 35 512 48000 37.6us 62.6us 0.00 0.01 0 S16LE 2 48000 alsa_output.platform-fd500000_pcie-pci-0000_01_00_0-usb-0_1_4_1_1_0.analog-stereo` / `R 89 0 48000 39.7us 23.2us 0.00 0.00 3531249 S16LE 1 48000 + gst-launch-1.0`.
- Issue 4875, "pipewire-pulse default quantum might be too low", created 2025-09-01T04:54:40Z, description: "- PipeWire version (`pipewire --version`): 1.4.7" / "- Distribution and distribution version (`PRETTY_NAME` from `/etc/os-release`): Fedora Linux 42" / "- Desktop Environment: KDE Plasma 6.4.4" / "- Kernel version (`uname -r`): 6.16.3-200.fc42.x86_64" / "- Processor: 4 × Intel® Core™ i3-1005G1 CPU @ 1.20GHz" / "After some investigation, it seems setting the env var `PULSE_LATENCY_MSEC=30` on my machine completely fixes the issue" / "On my system, anything under 30 produces crackling." (its pw-top outputs are PNG screenshots at `/uploads/…png`, HTTP 404 without login — not read).

**Coverage.**
- T4: covers, as isolated observations — per-node quantum (`QUANT` 64/441/512/800/900/1024/2048 frames at `RATE` 44100/48000, i.e. cycle periods 1.33 ms (64@48k), 10 ms (441@44.1k), 10.7 ms (512@48k), 16.7 ms (800@48k), 18.75 ms (900@48k), 21.3 ms (1024@48k), 42.7 ms (2048@48k) — my arithmetic) and per-cycle `BUSY` time of a client node (Firefox 3.4 µs at quantum 900; Kodi 8.8 µs at 800; Chromium 30.1 µs at 512; Wine 3.1–23.7 µs at 441; gst-launch 23.2 µs) and of the ALSA sink node (4.5–62.6 µs). These are single pw-top snapshots on the reporters' machines during faults; `BUSY` is the graph-thread time in the node's process callback, not the player's whole per-period CPU (decoding etc. is not in it).
- T3/T5: does not cover (except that Chromium/Firefox/Kodi appear as audio clients with quanta larger than the driver's).
- T1, T2, T6, T7: does not cover.

**One observation?** Each is one snapshot on one reporter's machine (named in some descriptions, e.g. issue 4875's i3-1005G1/Fedora 42/Plasma; issue 4662's Arch/i3/6.14.2; 4374's Raspberry Pi 4B), application named in the `NAME` column, window: a single refresh of pw-top.

---

### S3-webrtc-internals — a public `webrtc_internals_dump.txt` (gist thg1101/8f11e3c2c7274f114536)

**Copy read.** `https://gist.githubusercontent.com/thg1101/8f11e3c2c7274f114536/raw/` (278,248 B) → `gist_thg1101.txt` SHA-256 `faa7dffd6ea49a54645e5d44fb5045e85e7d887ee23005612f8c8e5b89bb2c56`. Author/date of the gist not retrievable (gist.github.com page blocked, 403); the dump's own timestamps are 2015-10-06T07:25:36Z–07:26:30Z. No platform/OS field in the dump.

**Verbatim passages.** `getUserMedia[1]`: `"origin": "https://simplewebrtc.com"`, `"video": "mandatory: {maxWidth:1680, chromeMediaSourceId:ZujvhCqlZZ2eSRFM4GcwAg==, maxHeight:1050, maxFrameRate:3, chromeMediaSource:desktop}, optional: {googLeakyBucket:true, googTemporalLayeredScreencast:true}"`. `PeerConnections["7108-1"].stats["ssrc_4020138328_send-googAvgEncodeMs"]`: `startTime 2015-10-06T07:25:36.578Z`, `endTime 2015-10-06T07:26:30.580Z`, values `[4,7,6,8,7,6,7,6,6,6,7,7,7,8,8,8,9,9,9,9,9,8,10,10,11,10,9,12,11,1,1,10,11,10,1,9,9,11,11,10,9,9,1,10,9,10,10,11,9,11,9,11,9,14,9]`; `…-googEncodeUsagePercent`: `[70,70,…,70,21,21,20,20,…,24,23]`; `…-googFrameRateInput`: `[0,8,8,8,8,7,8,7,…]`; `…-googFrameRateSent`: `[0,8,8,8,8,8,…,6,6,8,…]`. `PeerConnections["7108-2"]` (the desktop capture at `maxFrameRate:3`): `googAvgEncodeMs` `[5,5,3,1,0,0,0,0,0,1,1,0,0,1,1,1,1,2,2,1,2,1,2,1]`, `googFrameRateSent` `[0,0,3,3,3,0,0,0,1,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3]`.

**Coverage.** T5: covers thinly — one Chrome WebRTC session (2015, simplewebrtc.com), camera stream at 7–8 fps with average encode time 4–14 ms per frame, screen share at 3 fps with 0–5 ms; OS/CPU unknown; no decode or capture-thread data. Other topics: does not cover.

---

### S3-imc21-vca — "Measuring the Performance and Network Utilization of Popular Video Conferencing Applications" (IMC 2021) — automation code; data on request

**Copy read.** `https://raw.githubusercontent.com/kyle-macmillan/vca-imc-21/main/README.md` → SHA-256 `dfe5e63003c0b68e0c7a1a115d4858f3559e13e87b80f5d9af0e6d5271896466` (accessed 2026-09-13).

**Verbatim passages.** `README.md:1-4`: "# Automating videoconferencing applications (VCA)" / "This is a repo containing the code used to automate video conferencing calls in [Measuring the Performance and Network Utilization of Popular Video Conferencing Applications](https://arxiv.org/pdf/2105.13478.pdf)." `README.md:80-81`: "## Requesting data" / "We are happy to share the data we collected from our experiments upon request." Section "## Data Collected": "Executing the sample command will automate the calls, save network traffic and grab WebRTC (for meet and teams). Network traffic is saved in a directory called `captures` … WebRTC stats are saved as jsons in a directory called `webrtc` in the working directory."

**Coverage.** T5: not covered by any obtainable data — the artifact is pcap + webrtc-internals JSON (network-side; no CPU columns are mentioned), and the data are request-only. Other topics: does not cover.

---

## 3. Not found

- **T1 — desktop free-composition or code-editing datasets with raw timestamps and licence.** The only free-composition per-keystroke logs with application context found are SWELL-KW (Windows, 2012, 25 participants; CC-BY-NC-SA) and Clarkson II (request-only, no download page). Buffalo (CUBS) is request-only (curl 403; WebFetch summary only). Searches #11, #22, #26, #27, #31. No code-editing keystroke dataset with timestamps was found (search terms "keystroke dataset" with "code editing"/"IDE" were not separately run; the keystroke-dynamics sources found are password, transcription or uncontrolled free text).
- **T1 — pointer/mouse traces of a local GUI session with application names.** Balabit (RDP-side), DFL (raw local, no app names), Shen (fixed pattern) found; no dataset logging pointer events per local application. SWELL-KW logs clicks/wheel/drag but not motion.
- **T2 — CPU time per input event for a desktop editor/office/mail/image/video application on Linux.** Nothing with CPU time per event: Firefox profiles give wall-clock handler durations only (no CPU deltas); the Perfetto Chrome trace has per-task thread CPU but is Android. VS Code typing-latency issues with `.cpuprofile` attachments (#62475, #38586) could not be opened (github.com and `user-attachments` 403; MCP denied; WebFetch summary not citable). mpv issue bodies likewise unreachable (#30). KDE Bugzilla: no typing bug with a perf attachment (search #37; only konsole 492896 "Resizing embedded terminal" has `perf.data.perfparser.gz`, not downloaded because it is not an input-driven workload). Chromium tracker (issues.chromium.org) is a JS app not readable with curl (#40). GNOME sysprof captures found are scrolling/resizing, not typing (#33).
- **T3 — Linux scheduler traces (sched_switch/wakeup) of a desktop session with a focused GUI app.** None found: LTTng sample traces (`lttng.org/files/samples/`, 2005 and 2012 tarballs) have no workload description and were not opened; the Perfetto Chrome example has an empty `ftrace_config` (0 sched rows) and is Android; sysprof captures carry perf samples and counters only, no scheduler events. Endo/Seltzer (Harvard `~yaz`) redirects to an unrelated host (#34); Flautner (Michigan `~tnm/interactive/`) unreachable: TLS chain failure via proxy and HTTP 503 via WebFetch (#35).
- **T4 — per-wake CPU of an audio playback path with a stated period.** Only single pw-top snapshots from PipeWire issues (S3-pipewire-pwtop), each with an unnamed workload or a game/Wine; no measurement dataset; PulseAudio `pactl` outputs with latency fields were not searched separately after the PipeWire results (no query run); jack_iodelay / LAC datasets: no query run (time-boxed).
- **T5 — per-frame CPU of software video decode (mpv/VLC/GStreamer) or of a conferencing client on Linux.** Not found: mpv issue bodies unreachable (#8, #30); IMC21 data request-only; the only WebRTC dump found is a 2015 Chrome screen-share/camera session of unknown platform (S3-webrtc-internals). MangoHud CSV logs of video players: no query run.
- **T6 — one dataset distinguishing editor/office/mail/browser/image/video-editor behaviour.** Only SWELL-KW distinguishes applications (Word/Outlook/IE) in inter-keystroke data; nothing distinguishes CPU-per-input or wake structure across application classes.
- **T7.** Out of class; nothing recorded.
