# S7 — inputs for the setup states and operations (follow-ups spec decision 10)

Read 2026-09-16 for the appdefs item. Question: which of the three benchmark sources already behind the scenario catalog (PCMark 10, SYSmark 30, CpsMark+) state the input the corresponding 9.5 setup or operation needs — a document length, a code project, a photo and filter, a video clip, a web page — and with what words. SYSmark 25 was read for the code project only. Copies are the 2026-09-13 verification's (`_dev/research/jioh/2026-09-13-verification/reads/R05-vendor-benchmarks.md`, "Copies used", with SHA-256 and local paths under that folder's gitignored `sources/`); text extracted with pypdf, quoted as extracted. Two project sources were read for the operation triggers (class 2 of phase decision 4: project documentation and source).

## Copies

| id | document | copy | locator form |
|---|---|---|---|
| pcmark10 | UL, *PCMark 10 Technical Guide*, "Updated February 11, 2021", 141 pp. | s3.amazonaws.com/download-aws.futuremark.com/pcmark10-technical-guide.pdf, retrieved 2026-09-13, SHA-256 d7603a6c…b956067; `sources/pcmark10/pcmark10-technical-guide-2021-02-11.pdf` | PDF page ("Page N of 141") |
| sysmark30 | BAPCo, *SYSmark 30 User Guide* v1.2 (40 pp.) and *An Overview of SYSmark 30* whitepaper v1.2 (40 pp.) | Wayback captures of bapco.com's PDFs, 2026-09-13, SHA-256 03abdae1…4766ed and 4111c36e…5c3d6d; `sources/sysmark30/` | PDF page |
| cpsmark-tbench23 | Zhang & Wu 2023, CpsMark+, BenchCouncil Trans. 100084 | `sources/cpsmark-tbench23.txt` (from the ScienceDirect PDF, 2026-09-13) | section |
| sysmark25 | BAPCo, *SYSmark 25 User Guide* v1.9 and White Paper 1.1 | `sources/sysmark25/` | PDF page |
| kdenlive (project source) | Kdenlive 23.08 `src/timeline2/view/previewmanager.cpp`, `src/mainwindow.cpp`, `src/kdenlivesettings.kcfg` | invent.kde.org/multimedia/kdenlive, branch release/23.08, raw, retrieved 2026-09-16 | function / line |
| kdenlive (manual) | *Kdenlive Manual*, "Timeline Preview Rendering" | docs.kdenlive.org/en/tips_and_tricks/tips_and_tricks/timeline_preview_rendering.html, retrieved 2026-09-16 | section |
| gimp (project source and manual) | GIMP 2.10 `pdb/groups/plug_in_compat.pdb`; *GIMP 2.10 manual*, "Script-Fu Server" | raw.githubusercontent.com/GNOME/gimp/gimp-2-10/pdb/groups/plug_in_compat.pdb; docs.gimp.org/2.10/en/gimp-filters-script-fu.html; retrieved 2026-09-16 | procedure / section |

## Per input

### Photo and filter (GIMP `unsharp-mask`)

- **pcmark10, p. 71** (Photo Editing, Implementation), table: "INTERACTIVE RAW Fujifilm X-E1 24.9 MB 4952 × 3288"; "Following filters are executed on CPU: • color adjusting • unsharp mask 1 • noise adding • thumbnail loading"; p. 72: "Following filters are executed on OCL: • gaussian blur • unsharp mask 2 • local contrast • wavelet denoise • batch transformation". Interactive scenario, p. 72: "Apply brightness, contrast, saturation, unsharp mask, Gaussian noise, Gaussian blur, a further unsharp mask, local contrast and wavelet denoise to the source image via sliders in the user interface". Batch parameters, p. 74: "𝑀5 = 𝑈𝑛𝑠ℎ𝑎𝑟𝑝𝑀𝑎𝑠𝑘𝐼𝑚𝑎𝑔𝑒(𝑟𝑎𝑑𝑖𝑢𝑠 8, 𝑠𝑖𝑔𝑚𝑎 4, 𝑎𝑚𝑜𝑢𝑛𝑡 32, 𝑡ℎ𝑟𝑒𝑠ℎ𝑜𝑙𝑑 3)". The test is implemented on ImageMagick (p. 71), not GIMP.
- **sysmark30** whitepaper p. 11 / user guide p. 34: "editing digital photos (applying filters and creating HDR photos)" — no image size, no filter named.
- **cpsmark-tbench23** §4.3.3: Photoshop "Use the PSD (Photoshop Document) file to make a vertical poster … virtualize the background" — no size.
- **Taken**: image 4952 × 3288 and the unsharp-mask filter from pcmark10; content synthetic (design). Parameter mapping onto GIMP's PDB (design, from `plug_in_compat.pdb`: "&std_pdb_compat('gegl:unsharp-mask') … 'std-dev', radius, 'scale', amount, 'threshold', threshold / 255.0", with radius "0.0 <= float <= 300.0", amount "0.0 <= float <= 300.0", threshold "0 <= int32 <= 255"): std-dev 4.0 (ImageMagick's sigma 4, the blur's standard deviation), amount 0.32 (ImageMagick's amount 32 read on PCMark's percent-scaled sliders "amount 99 − 32", p. 73), threshold 8 (3 % of 255).
- **Trigger**: GIMP manual, Script-Fu Server: "This command will start a server, which reads and executes Script-Fu (Scheme) statements you send him via a specified port"; protocol: request byte 0 "0x47" then "L div 256", "L mod 256"; response "0x47", error "0 on success, 1 on error", then length. Procedure `plug-in-script-fu-server` (run-mode, ip, port, logfile), started with the GUI through `-b`.

### Video clip and render (Kdenlive `preview-render`)

- **pcmark10, p. 76** (Video Editing, Implementation): "Part 2: Sharpening • Sharpens the 1080p H.264 video • Uses publicly available executable FFmpeg.exe • Command line: FFmpeg.exe -y -v 40 -i <input file> -vf scale=w=1920:h=1080:flags=bicubic,unsharp=opencl=%OCL%:lx=7:ly=7:la=0.56:cx=7:cy=7:ca=0.28 -strict -2 <output file>". The test measures frames per second (p. 77).
- **sysmark30** whitepaper p. 11: "A video encode is started in Adobe Premiere and sent to the background while Adobe Photoshop is launched" — no clip stated.
- **cpsmark-tbench23** §4.3.3: Premiere "Clip and splice source video materials, add lens transition and subtitles, synthesize sound effects, render, and preview the output video"; HandBrake "Convert the H.264 encoded source video with 4K resolution to the H.256 encoded target video with 2K resolution" — no length.
- **Taken**: a 1920 × 1080 H.264 clip sharpened with ffmpeg's unsharp at lx=7:ly=7:la=0.56:cx=7:cy=7:ca=0.28 from pcmark10 (as MLT's `avfilter.unsharp`); 20 s at 30 fps, synthetic content, video-only (design). The operation is the *timeline preview* render, not the export (spec decision 7).
- **Trigger**: Kdenlive manual: "Set the timeline zone in (I) and out (O) points for the zone you want to render for preview. Next, select Add Preview Zone"; "Select Start Preview Render (Menu ‣ Sequence ‣ Timeline Preview ‣ Start Preview Render). Or press Shift + Return". Source (`mainwindow.cpp`, 23.08): `set_render_timeline_zone` "Add Preview Zone" and `clear_render_timeline_zone` "Remove All Preview Zones" carry no default shortcut; `prerender_timeline_zone` "Start Preview Render" is `QKeySequence(Qt::SHIFT | Qt::Key_Return)`. `previewmanager.cpp`: chunks of `KdenliveSettings::timelinechunks()` frames (kcfg default 25); the render is an external process — `m_previewProcess.start(KdenliveSettings::kdenliverendererpath(), args)` with args `"preview-chunks", scene, cacheDir, dirtyChunks, chunkSize − 1, profile, extension, params`; chunk files `"%1.%2".arg(chunk).arg(m_extension)` in the preview cache dir; Ubuntu noble's kdenlive 4:23.08.5-0ubuntu4 ships `/usr/bin/kdenlive_render`. Completion is that process exiting.

### Web page (Chrome `page-load`)

- **pcmark10, pp. 52–53** (Web Browsing): "The content is served with a local lightweight web server that is embedded into the benchmark. The content is custom made for the benchmark and represents common web sites."; social media: "Navigates to and load a social media site. • The page updates the news feed with new content. • The page updates the feed again."; online shopping: "View and zoom in on high resolution images of shopping items. • View 3D models of items."; typical "Social media page load s 0.10-0.18" (p. 55).
- **cpsmark-tbench23** §4.3.3: "Google Chrome. Simulate users to browse webpages and switch between tabs. Webpages are accessed through locally configured network services. The webpages contain text, pictures, JS (JavaScript) scripts, and flash."
- **sysmark30**: "web browsing" only.
- **Taken**: a locally served page whose script builds a feed with text and high-resolution pictures (pcmark10, cpsmark-tbench23); 300 posts, thirty 1600 × 1200 pictures, a 200 000-record sort-and-aggregate pass (design). Completion: the page sets its title after the first paint of the built feed (design).

### Large document (Writer setup state)

- **pcmark10, p. 63** (Writing): "1. Load Document 1, display in a window 2. Load Document 2, display in a window 3. Copy a large part of Document 1 and paste into Document 2 … 10. Insert some pictures from a local drive in Document 2" — no length, no picture count. Implemented on LibreOffice Writer (p. 63).
- **sysmark30**: "word processing (mail merge, document comparison, and PDF conversion)"; **cpsmark-tbench23** §4.3.3, Word: "Input characters, modify titles and character formats, split paragraphs, set the directory, insert pictures, create tables and charts, input data" — no length.
- **Taken**: not found in any of the three. Design: 100 sections of five 100-word paragraphs (≈ 50 000 words, about 100 pages) with ten 1024 × 768 pictures; the stream types at the end of the document.

### Code project (VS Code setup state)

- **sysmark25** white paper 1.1 p. 14 / user guide v1.9 p. 32: "software development (code compilation)" among the Productivity scenario's activities; the application lists (user guide pp. 31–32) name Office, Acrobat, Adobe applications and Chrome only — no development tool or project.
- **pcmark10**, **sysmark30**, **cpsmark-tbench23**: no software-development workload.
- **Taken**: not found. Design: sindresorhus/got at commit 64f21e2a4797b8c56493143e416508893983063f (tag v16.0.0), dependencies installed, `source/index.ts` open, so VS Code's built-in TypeScript language server runs and re-checks the file the stream types into.

## Coverage

Stated by a source and taken: the photo size and filter (pcmark10); the clip format and the sharpening filter (pcmark10); the page kind and its local serving (pcmark10, cpsmark-tbench23). Not stated by any of the three: document length and picture count; code project. Filter parameters are stated for ImageMagick and ffmpeg; their mapping onto GIMP's and MLT's parameters is design and is written on the archetype's scope at fold-in.
