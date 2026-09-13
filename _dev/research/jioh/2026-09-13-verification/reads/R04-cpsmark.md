# Independent read R04 — cpsmark-tbench23

## Copies used

| # | Copy | Location (relative to _dev/research/jioh/2026-09-13-verification/) | Identity checks | Role |
|---|------|------------------------------|-----------------|------|
| 1 | Publisher PDF (ScienceDirect `main.pdf`, Wayback capture 2023-01-14 13:03:01 UTC) | `sources/cpsmark-tbench23-sd-wayback.pdf` (16 pages, 1,802,501 bytes, SHA-256 `04d9f106862dfaaa8188dedfe06479c9742a578b4dcfb9d4e4dbde687c90f067`) | SHA-1 (base32) `N5BRZQQTCR2E6NVLB5IXGMUREK2OO7QO` equals the Wayback CDX digest in `sources/cdx-mainpdf.json` (byte-identical to the archived capture). PDF metadata `/Subject`: "BenchCouncil Transactions on Benchmarks, Standards and Evaluations, 2 (2022) 100084. doi:10.1016/j.tbench.2023.100084"; `/Creator` Elsevier; PDF/A-1b. Running header on every page: "BenchCouncil Transactions on Benchmarks, Standards and Evaluations 2 (2022) 100084". p.1 footer: DOI, "Received 8 June 2022; Received in revised form 28 December 2022; Accepted 1 January 2023", "Available online 5 January 2023", CC BY-NC-ND. | **Primary text for every topic** |
| 2 | Text extraction of copy 1 | `sources/cpsmark-tbench23.txt`; re-extracted independently with pypdf to `sources/cpsmark-tbench23/reextract-pypdf.txt` | The two extractions are character-identical (97,398 chars). | Search aid only |
| 3 | Page renders of copy 1 (ghostscript) | `sources/cpsmark-tbench23/img/p01.png`–`p16.png` (150 dpi); `img/p12-table5.png`, `img/p13-tables6-7.png` (220 dpi crops) | Rendered from copy 1 | Tables 1–7 and Figs. 1, 3, 4 read from images; text-extraction cell merges corrected (e.g., Table 2 version column) |
| 4 | Crossref record for DOI 10.1016/j.tbench.2023.100084 | `sources/cpsmark-tbench23/crossref.json` | volume 2, issue 4, article-number 100084, published-print 2022-10; authors Yue Zhang, Tong Wu | Bibliographic cross-check (C-cpsmark-13) |
| 5 | Elsevier article API coredata (pre-existing) | `sources/cpsmark-elsapi.xml` | PII S2772-4859(23)00001-7; coverDate 2022-10-31 ("October 2022"); ISSN 2772-4859; open access CC BY-NC-ND | Bibliographic cross-check |
| 6 | GitHub repository named in the paper (`https://github.com/wanghong3116/CpsMarkPLUS`; GitHub canonical name `wanghong3116/CPSmarkPLUS`) | `sources/cpsmark-tbench23/repo/` (git clone) | HEAD = `bf24434261cc2b512a40b3dec1269a31a8e676a0` (branch `final_branch`, committed 2021-05-21 15:50:49 +0800, message "update version message and change some work marks run order."); 7 commits total, first 2020-10-21; GitHub API: `license: null`, repo created 2020-10-21, last push 2021-05-21. GBK-encoded sources; `BenchMark/UI/WorkMark.cpp` decoded to `sources/cpsmark-tbench23/WorkMark.utf8.cpp`. | Supplementary only (C-cpsmark-5/8/12 side notes). Not used to answer what the paper says. |
| 7 | National Metrology Data Center resource page named in the paper (`https://jc.nmdc.ac.cn/view-40-609748.html`) | `sources/cpsmark-tbench23/nmdc-wayback-20221209.html` (Wayback `20221209020916id_`) | Live site returned HTTP 429/timeout from here; Wayback capture 2022-12-09 fetched. Page title "微型计算机办公性能基准测试工具CPSmark+软件资源包". | Supplementary only (C-cpsmark-8) |

Quoting conventions: quotations are copied from copy 1 and checked against the page images. Two mechanical normalisations only: (i) typesetting line-break hyphens are rejoined (e.g., "spec-/ified" → "specified"); where a line-break hyphen is ambiguous it is kept and flagged; (ii) the extraction's spurious space in "CpsMark +" is written "CpsMark+" (the rendered page shows no space). "[sic]" marks typos present in the source. Page numbers are the printed page numbers, which equal PDF page indices 1–16. Email addresses and personal details beyond the byline are not reproduced.

---

## C-cpsmark-1 — usage scenarios: how many, names, grouping into modules, user types / weight classes per module

**(a) Verbatim**

1. §4.3.2, p.4 right column → p.5 left column: "According to the abstracted user profiles of office computers, we cluster the usage models into four groups of common office scenarios based on their overall functions within a specific workflow, i.e., document manipulation, Internet service, graphic design, and multimedia processing, which are described as follows:"
2. §4.3.2, p.5 left: "• The document manipulation scenario contains multiple manipulations towards the documents in common formats, which are involved in most cases of modern business.
   • The Internet service scenario mainly includes web browsing and email creation, which are usually auxiliary means in resource acquisition and information communication.
   • The graphic design scenario refers to visual expression of ideas and information through the combination of symbols, pictures, and text, which is crucial for product presentation tasks like poster production.
   • The multimedia processing scenario relates to utilizing computers for digitizing and integrating graphics, sound, video and other media information in a specific interactive interface, which is widely applied in consulting, marketing and management."
3. §4.3.3, p.5 right: "Hence, we merge the usage scenarios into two separately running and scored modules as follows:
   • Comprehensive Application (CA) module includes the scenarios of document manipulation and Internet service, which reflect light and middleweight use by task or knowledge workers in most business workplaces, where end users might pay more attention to overall performance, response, and smoothness throughout regular use.
   • Comprehensive Calculation (CC) module includes the scenarios of graphic design and multimedia processing, which reflect heavy-weight use by power users skilled in professional fields, where end users possibly focus on the execution efficiency of CPU-intensive or GPU-intensive computing tasks." (flag: "heavy-weight" breaks across lines at the hyphen, so the source spelling "heavyweight" vs "heavy-weight" is not determinable from this line; elsewhere, §4.7.3 p.10, the paper writes "heavyweight".)
4. §4.3.3, p.5 right: "Within each module, in addition to similar performance dependencies, the usage scenarios are highly correlated and tend to appear in a common workflow under daily office scenarios. Further, each usage scenario is given a different weight based on the sum of metrics measured from inclusive workloads."
5. §4.3.1, p.4 right: "In this paper, we mainly focus on most knowledge workers and some part of power users."
6. §4.3, p.4 right: "CpsMark+ has two independent modules for simulating user experience perceived in modern office scenarios, i.e., Comprehensive Application (CA) and Comprehensive Calculation (CC), which can be optionally selected and run independently during the test."
7. Fig. 1 (p.4) shows "User Profile Abstraction" → "Task Workers", "Knowledge Workers", "Power Users" → "Usage Scenario Modeling" boxes "Document Manipulation", "Internet Service" (grouped) and "Graphic Design", "Multimedia Processing" (grouped) → "Master Control Program" with "Comprehensive Application" and "Comprehensive Calculation".

**(b) Locator:** §4.3, §4.3.1, §4.3.2, §4.3.3, pp.4–5; Fig. 1, p.4; Table 2, p.5.

**(c) Reading:** Four usage scenarios, grouped into two modules. CA = document manipulation + Internet service; associated with "task or knowledge workers" and "light and middleweight use". CC = graphic design + multimedia processing; associated with "power users" and heavyweight use. The weight-class wording is the paper's own ("light and middleweight", "heavy-weight"). The paper also says the scope of the paper is "most knowledge workers and some part of power users" — task workers appear in the CA description but not in this focus statement. "Weight" in quote 4 is a different sense (scoring weight per usage scenario, "based on the sum of metrics"), not a user class; the scoring formula in §4.5 (p.8) is a plain ratio of summed workload times with no explicit per-scenario coefficient.

**(d) Verdict: FOUND.**

---

## C-cpsmark-2 — content of Table 1

**(a) Verbatim — Table 1, p.5, caption "The profiles of computer end users." (transcribed from the page image)**

| User category | Representative occupations | Performance requirement |
|---|---|---|
| Task workers | • Customer service • Front desk consultation • Bank clerks • Data entry specialist • Human resource | • Basic document operations • A single OS-level application • Simple connectivity needs • Static 2D graphics • Few computing occasions |
| Knowledge workers | • Most students • Teachers and professors • Company administrators • Financial advisors providing multiple advice • Product managers presenting prototypes from multi-angle | • Content creation • Frequent web browsing • Moderately complex application • Moderate scientific computing • Variable multimedia processing like graphics and video • Adequate memory |
| Power users | • Multimedia designers making high-definition video • Professional architects engaged in complex modeling • Physicians examining delicate 3D medical images | • Complex content creation • Intensive video and 3D graphics processing • Heavy CPU computing • Fast system response • Smooth running of applications |

Context, §4.3.1, p.4 right: "For the daily usage of desktop computers in modern office scenarios, we abstract the profiles of end users from the perspective of occupation and profession described in Table 1." and "Since CpsMark+ has been designed for commercial evaluation of desktop computers used in modern office scenarios, the user profiles summarized in Table 1 exclude those working in laboratories, R&D centers, factories, or telecommuting."

**(b) Locator:** Table 1, p.5; §4.3.1, p.4.

**(c) Reading:** Three user categories; each has two columns (representative occupations; performance requirement), qualitative bullet lists only — no numbers, shares, or weights. Scope exclusions: laboratories, R&D centers, factories, telecommuting. The table itself does not map categories to modules; that mapping is in §4.3.3 (see C-cpsmark-1). No source/citation is given for the table's content other than the general reference to Chen et al. [22] in the preceding sentence.

**(d) Verdict: FOUND.**

---

## C-cpsmark-3 — content of Table 2; application selection

**(a) Verbatim — Table 2, p.5, caption "The application selection of workloads." (transcribed from the page image; the text extraction merges the version column with application names, e.g., "Adobe® Premiere Pro CC 2019" — the image shows "Pro" is in the Version column)**

| Module | Usage scenario | Application | Version |
|---|---|---|---|
| Comprehensive application | Document manipulation | Microsoft® PowerPoint | 2016 (16.0.4266.1003) |
| | | Microsoft® Word | 2016 (16.0.4266.1003) |
| | | Microsoft® Excel | 2016 (16.0.4266.1003) |
| | | Adobe® Acrobat | DC (19.010.20091) |
| | | WinRAR | 5.91 (64-bit) |
| | Internet service | Google® Chrome | 73.0.3683.75 |
| | | Microsoft® Outlook | 2016 (16.0.4266.1003) |
| Comprehensive calculation | Graphic design | Autodesk® AutoCAD | 2018 (22.0.49.0) |
| | | Adobe® Photoshop | CC 2019 (20.0.1) |
| | Multimedia processing | Autodesk® 3ds Max | 2018 (20.0.0.966) |
| | | Adobe® Premiere | Pro CC 2019 (13.0) |
| | | Adobe® After Effects | CC 2019 (16.0) |
| | | HandBrake | CLI 1.3.0 |

Selection, §4.3.2, p.5 left: "As for workload applications, we select desktop-level office applications based on the metric of popularity. According to the investigation report of office software markets in China by Chinaiern [23], our software market experts select popular and typical applications for each usage scenario in modern office, which are summarized in Table 2."

"Since sufficient time is required for workloads to be developed and validated, versions of some applications are not the latest when CpsMark+ was released. In addition, the intended applications of CpsMark+ are the most widely used version instead of the latest one. While some application like WinRAR is up to date because it is feasible to be instantly updated by end users."

Reference [23], p.16: "[23] In-depth research of China office software market, 2021, http://www.chinaiern.com/baogao/scbg/2953763.shtml?bd_vid=6645286086633733527."

§4.2, p.4 left: "For the first use of CpsMark+, the trial version of each third-party application is automatically installed on the tested computer system and configured by the execution of an automatic setup program."

**(b) Locator:** Table 2, p.5; §4.3.2, p.5; §4.2, p.4; ref. [23], p.16.

**(c) Reading:** 13 applications (7 CA, 6 CC). Selection criterion stated: "popularity", based on a China office-software market report (Chinaiern, dated 2021 in the reference list) plus judgement of "our software market experts". No popularity figures, shares, or selection thresholds are given. Versions are deliberately the "most widely used version", not latest; WinRAR is the stated exception. Trial versions are installed. Note the reference [23] is dated 2021 while §2.2 says CpsMark+ was "finally developed" in 2019 — the paper does not explain the ordering.

**(d) Verdict: FOUND.**

---

## C-cpsmark-4 — which named application is used in which usage scenario / workload

**(a) Verbatim**

Table 2 (p.5) — see transcription under C-cpsmark-3 (scenario → application).

§4.3.4, p.6 left (CA workloads, one bullet per application; application names in bold in the source):
"• Google Chrome. Simulate users to browse webpages and switch between tabs. Webpages are accessed through locally configured network services. The webpages contain text, pictures, JS (JavaScript) scripts, and flash.
• Microsoft PowerPoint. Set the new template style and create slides. Input texts and adjust character formats, alignment, and font size. Add pictures, captions, and typeset. Insert tables and charts with filled data. Browse slides.
• Microsoft Word. Input characters, modify titles and character formats, split paragraphs, set the directory, insert pictures, create tables and charts, input data.
• Microsoft Excel. Generate and organize data with fixed formula. Classify and enter data under a specific rule. Calculate and sort common statistics. Draw line charts by categories, set titles and styles, adjust size and position. Macro definition and execution.
• Adobe Acrobat. Convert PowerPoint, Word, and Excel documents made in previous workloads to PDF files, browse these PDF files page by page.
• WinRAR. Compress and decompress mixed files in multiple formats, including images, videos, documents, databases, and log files.
• Microsoft Outlook. Simulate users to receive, browse email contents and attachments offline, including Word, Excel, and PowerPoint files. Upload new attachments, edit the body of the email, and reply."

§4.3.4, p.6 left→right (CC workloads):
"• Adobe Photoshop. Use the PSD (Photoshop Document) file to make a vertical poster. Separate target area from the source material and design the layout of layers. In new layers, set titles and captions, add a logo, and adjust its size, coordinates, and transparency. Combine all layers, virtualize the background and merge them into a large picture.
• Autodesk AutoCAD. Use the DWG file to draw distributed structure diagrams of buildings. In the main framework, draw structure and vector identification of each area, add coordinates, and mark the size. Change colors of layers and use different line styles. Design wiring, draw pipeline distribution, and flow direction.
• Autodesk 3ds Max. Design a 3D model of a whale. Develop the 3D framework, color the texture, add lighting effects, make reflections and shadow effects by calculating light source position, incidence angle, and reflection angle. Produce motion trajectories and movements of the whale model, render segmental frames of action sequences.
• Adobe Premiere. Clip and splice source video materials, add lens transition and subtitles, synthesize sound effects, render, and preview the output video.
• Adobe After Effects. Add particle explosion effects, render the firework explosion animation sequence of 1800 frames and 30 FPS.
• HandBrake. Convert the H.264 encoded source video with 4K resolution to the H.256 [sic] encoded target video with 2K resolution, the container format is MP4. Hardware acceleration will be leveraged if enabled."

**(b) Locator:** Table 2, p.5; §4.3.4, p.6.

**(c) Reading:** One workload per application (13 workloads). Mapping:
- Document manipulation (CA): PowerPoint, Word, Excel, Acrobat, WinRAR.
- Internet service (CA): Chrome, Outlook.
- Graphic design (CC): AutoCAD, Photoshop.
- Multimedia processing (CC): 3ds Max, Premiere (Pro), After Effects, HandBrake.
Chrome pages are served locally (no live Internet); Outlook runs "offline". "H.256" is a source typo (context implies H.265). WinRAR is placed under "document manipulation" in Table 2 but is excluded from the Method 1 sampling group in §4.4.1 (p.6: "document manipulation (WinRAR excluded)").

**(d) Verdict: FOUND.**

---

## C-cpsmark-5 — CA workload order: fixed?, stages and order, do outputs feed the next workload (which files)

**(a) Verbatim**

1. §4.3, p.4 right: "Each of them has a series of workloads executed in a specific order."
2. §4.2, p.4 right: "The MCP is devised as a serial layout and contains two separate test modules. Users can initialize the number of iterations to run for eliminating fluctuation of benchmark results. Composed of a sequence of orderly executed workloads, each module independently generates a synthetic score that reflects the performance of inclusive workloads. There is an automatic reboot of the tested computer system between the two modules for eliminating the impacts of varying system status (e.g., cache) on module independence."
3. §4.3.4, p.6 left: "The workload operations of the CA module are briefly described in execution order as follows:" (followed by Chrome, PowerPoint, Word, Excel, Acrobat, WinRAR, Outlook — bullets quoted under C-cpsmark-4).
4. §4.3.4, p.6 right: "Within each module, the workloads are executed in the order specified above. The format or even the content of the generated output for some specific applications is identical to that of the input data set for subsequent applications. Such design enables test modules to describe cooperation across tasks throughout a common workflow. For example, the workloads of the CA module simulate the following coherent user behaviors: resource preparation via the Internet, content creation, document processing, and email delivery."
5. §4.3.4, p.6 left (Acrobat bullet): "Convert PowerPoint, Word, and Excel documents made in previous workloads to PDF files, browse these PDF files page by page."
6. §4.3.4, p.6 left (Outlook bullet): "Simulate users to receive, browse email contents and attachments offline, including Word, Excel, and PowerPoint files."
7. §4.3.4, p.6 left: "the workload of CpsMark+ is more than a concept of application automation, but a logical integration of three elements: the input data set extracted from the resource package, the workload operations performed on the input data set through the applications executed by the MCP, and the generated output." and "We guarantee the completeness of workloads via designing diversified operations that independently generate finished files as output for each application. Moreover, there is no random process in the MCP so that the generated output is uniquely determined by the input data set and the workload operations."
8. §4.4.3, p.7 right: "More concretely, for the Nth workload, the MCP first decompresses the resource package and extracts the exclusive input files to a specified location, then an MD5 [29] check is performed towards them to ensure the data integrity. If the MD5 check fails, the test will abort and return to the initialization phase, otherwise, the MCP will move forward to the application execution phase depicted as the dashed rectangle in Fig. 3, where the designed metric T_N is tested. When all the workload operations are finished, an MD5 check is performed towards the generated output. Finally, after a five-second countdown, if there is no user input to interrupt the test, i.e., mouse clicks on the pause button, the MCP will proceed for the next workload until the entire benchmark is completed."
9. §4.4.3, p.7 right: "It is worth noting that for the workloads in the usage scenario of document manipulation and Google Chrome, the applications are launched through direct open of the input files, while for the workloads in the usage scenarios of graphic design, multimedia processing, and Microsoft Outlook, the input files are loaded after separate launch of the applications."
10. Fig. 3 (p.8), caption "Intra-workload and inter-workload pipelines of metric testing in CpsMark+.", boxes in flow order (read from image): "Workload N−1" → "Resource Decompression" → "MD5 Checksum" → [dashed box T_N: "Application Launching" → "Input Files Loading", or "Direct Open of Input Files"; then "Workload Operations"] → "MD5 Checksum" → "Countdown" → "Workload N+1"; failure branches ("F") go to "Initialization Interface"; "User Input" → "Pause".

**(b) Locator:** §4.2 p.4; §4.3 p.4; §4.3.4 p.6; §4.4.3 p.7; Fig. 3 p.8.

**(c) Reading:**
- Fixed order: yes — both modules run their workloads in a fixed, stated order. CA order: Chrome → PowerPoint → Word → Excel → Acrobat → WinRAR → Outlook. The number of iterations is user-set; modules can be run independently; reboot between modules.
- "Stages": the paper names two different things that could be called stages. (i) User-behaviour stages of the CA workflow, in order: "resource preparation via the Internet, content creation, document processing, and email delivery" — the paper does not explicitly assign each application to one of these four behaviours. (ii) Per-workload pipeline stages (Fig. 3 / §4.4.3): resource decompression → MD5 check of input → application launch + input loading (or direct open) → workload operations (timed as T_N) → MD5 check of output → five-second countdown → next workload.
- Output → input chaining: the general claim is hedged to "some specific applications" and "format or even the content". The only explicit file-level chain in the paper is Acrobat: it converts the "PowerPoint, Word, and Excel documents made in previous workloads" to PDF. Outlook's attachments are "Word, Excel, and PowerPoint files", but the paper does not say these are the outputs of the earlier workloads. No chain is stated for Chrome, WinRAR (its inputs are "mixed files in multiple formats"), or into Outlook. Tension inside the paper: §4.4.3 says each workload's "exclusive input files" are extracted from the resource package and MD5-checked, which describes per-workload inputs from the package rather than from a prior workload's output; the paper does not reconcile this with the Acrobat description. Also, the Acrobat workload directly follows Excel but uses outputs of three earlier workloads, so "feeds the next" in a strict adjacent sense is only partly what is described.

Supplementary, repository (copy 6, HEAD `bf24434…`, not the paper): `BenchMark/UI/WorkMark.cpp` lines 342–361 add CA workloads in the order Chrome (`CFG_MARK_NET`), PowerPoint, Word, Excel, PDF (Acrobat), WinRAR, Outlook, then Photoshop and AutoCAD; the last commit's message is "change some work marks run order" and its diff moves Outlook from 2nd to 7th and Excel after Word. `BenchMark/mark/PDFMark.cpp` `run()` calls only `convertPPTToPdf()` and its input path is `Resources\pdf\ppt.pptx` from `Resources\pdf.zip` (lines 20, 67, 97–110), i.e., in this code version the PDF workload converts a PowerPoint file shipped in its own resource archive, not Word/Excel outputs of earlier workloads. `OutlookMark.cpp` attaches files from `Resources\MsOffice\` (lines 280–282). The paper says the repository "is still under further improvement and subject to change", so code/paper differences are recorded, not resolved.

**(d) Verdict: FOUND** (fixed order and stages stated explicitly; for "which files", only the Acrobat chain is stated — PowerPoint, Word, Excel documents → PDF; any other chain is NOT in the source).

---

## C-cpsmark-6 — content of Table 4: hardware factors varied, sensitivity values per workload/module, which workloads are sensitive to CPU frequency or storage

**(a) Verbatim**

Setup, §4.7.1, p.8 right: "We alter five different hardware characteristics of a predefined datum point to build the tested computer systems, including the number of CPU cores, CPU frequency, graphics card, storage device, and system memory, which are crucial factors in determining user experience. For each hardware characteristic, we select four configurations with significant pairwise performance differences. They are denoted as Config 1 to Config 4 in ascending order of performance."

"For the configurations of the CPU characteristic, instead of using different processor models, we stick to the CPU model of the datum point and enable different CPU frequencies or numbers of CPU cores by changing BIOS settings. For the configurations of the graphics card, we use the same brand of discrete graphics cards to ensure consistency of graphics drivers and available physical memory. For the configurations of system memory, we all adopt the single-channel mode and only change the memory size of the datum point."

Datum point, p.8 right: "• CPU Model: Intel® Core™ i7-9700K (8 cores, 3.60 GHz, 12 MB L3 cache) • Graphics: Nvidia® GeForce® GTX 750 • RAM: Kingston® ValueRAM™ 4 GB DDR4 2666 MHz • Storage: Seagate® Barracuda® 1TB SATA III HDD (6 GB/s, 5400 RPM) • Chipset: Intel® Z390 • Display Resolution: 1920 × 1080 • OS: Microsoft® Windows® 10"

"Notably, for all the experiments in this section, we disable common auxiliary optimization technologies, e.g., Turbo Boost, Hyper-Threading, and Hardware Acceleration, to better highlight the influence of different configurations under various hardware characteristics on benchmark performance from a static perspective."

Table 3, p.9, caption "The hardware characteristics and related configurations." (from image):

| Hardware characteristic | Configuration 1 | Configuration 2 | Configuration 3 | Configuration 4 |
|---|---|---|---|---|
| CPU cores | 2-Core | 4-Core | 6-Core | 8-Core |
| CPU frequency | 2.0 GHz | 2.5 GHz | 3.0 GHz | 3.5 GHz |
| Graphics card | Nvidia GeForce GTX 750 | Nvidia GeForce GTX 980 | Nvidia GeForce GTX 1080 | Nvidia GeForce RTX 2080Ti |
| Storage device | Seagate Barracuda 1TB SATA III 5400RPM HDD | Western Digital Blue 1TB SATA III 7200 RPM HDD | Samsung 860 EVO 250GB SATA III SSD | Samsung 970 PRO 512GB NVMe M.2 SSD |
| System memory | 4 GB | 8 GB | 16 GB | 32 GB |

Method, §4.7.2, p.9 left: "Specifically, we run CpsMark+ on each configuration for 20 independent iterations with a system reboot and a 15-min interval between each run. In each iteration, we sum the tested metrics of the included workloads for each module, then the average of the sums is adopted as the module performance on a certain configuration. Finally, for each hardware characteristic, we calculate the inverse ratio of the module performance tested on the other three configurations to the module performance tested on the first configuration, i.e., base configuration, respectively. The sensitivity of the module performance and the workload performance of CpsMark+ to various hardware characteristics are shown in Fig. 4 and Table 4, respectively."

Table 4, p.10, caption "The sensitivity of the workload performance to various hardware characteristics." (full transcription; checked against page image):

| CPU cores | Chrome | PowerPoint | Word | Excel | Acrobat | WinRAR | Outlook | Photoshop | AutoCAD | 3ds Max | Premiere | After effects | HandBrake |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Config 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Config 2 | 1.18 | 1.21 | 1.19 | 1.27 | 1.23 | 1.25 | 1.19 | 1.48 | 1.51 | 1.55 | 1.49 | 1.52 | 1.56 |
| Config 3 | 1.35 | 1.37 | 1.35 | 1.41 | 1.36 | 1.39 | 1.34 | 1.73 | 1.72 | 1.74 | 1.69 | 1.75 | 1.71 |
| Config 4 | 1.41 | 1.43 | 1.42 | 1.47 | 1.44 | 1.45 | 1.42 | 1.89 | 1.87 | 1.92 | 1.91 | 1.93 | 1.93 |

| CPU frequency | Chrome | PowerPoint | Word | Excel | Acrobat | WinRAR | Outlook | Photoshop | AutoCAD | 3ds Max | Premiere | After effects | HandBrake |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Config 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Config 2 | 1.20 | 1.22 | 1.21 | 1.25 | 1.23 | 1.26 | 1.19 | 1.18 | 1.19 | 1.22 | 1.24 | 1.23 | 1.22 |
| Config 3 | 1.37 | 1.38 | 1.39 | 1.44 | 1.40 | 1.43 | 1.38 | 1.33 | 1.35 | 1.37 | 1.36 | 1.34 | 1.34 |
| Config 4 | 1.63 | 1.65 | 1.64 | 1.68 | 1.64 | 1.67 | 1.62 | 1.59 | 1.57 | 1.63 | 1.61 | 1.58 | 1.61 |

| Graphics card | Chrome | PowerPoint | Word | Excel | Acrobat | WinRAR | Outlook | Photoshop | AutoCAD | 3ds Max | Premiere | After effects | HandBrake |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Config 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Config 2 | 1.01 | 0.99 | 1.00 | 1.02 | 1.01 | 1.01 | 0.98 | 1.36 | 1.34 | 1.37 | 1.35 | 1.34 | 1.36 |
| Config 3 | 1.03 | 1.00 | 1.01 | 1.01 | 0.99 | 1.02 | 1.02 | 1.66 | 1.65 | 1.68 | 1.66 | 1.63 | 1.65 |
| Config 4 | 1.05 | 1.04 | 1.04 | 1.03 | 1.02 | 1.03 | 1.01 | 1.77 | 1.79 | 1.77 | 1.75 | 1.78 | 1.76 |

| Storage device | Chrome | PowerPoint | Word | Excel | Acrobat | WinRAR | Outlook | Photoshop | AutoCAD | 3ds Max | Premiere | After effects | HandBrake |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Config 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Config 2 | 1.26 | 1.25 | 1.27 | 1.23 | 1.24 | 1.27 | 1.25 | 1.25 | 1.22 | 1.24 | 1.25 | 1.23 | 1.21 |
| Config 3 | 1.48 | 1.47 | 1.49 | 1.51 | 1.50 | 1.51 | 1.47 | 1.46 | 1.45 | 1.48 | 1.49 | 1.47 | 1.48 |
| Config 4 | 1.54 | 1.55 | 1.53 | 1.53 | 1.55 | 1.54 | 1.56 | 1.51 | 1.52 | 1.49 | 1.50 | 1.48 | 1.47 |

| System memory | Chrome | PowerPoint | Word | Excel | Acrobat | WinRAR | Outlook | Photoshop | AutoCAD | 3ds Max | Premiere | After effects | HandBrake |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Config 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Config 2 | 1.17 | 1.16 | 1.17 | 1.15 | 1.18 | 1.14 | 1.15 | 1.22 | 1.19 | 1.21 | 1.18 | 1.22 | 1.20 |
| Config 3 | 1.23 | 1.22 | 1.25 | 1.24 | 1.23 | 1.22 | 1.22 | 1.28 | 1.27 | 1.29 | 1.26 | 1.25 | 1.30 |
| Config 4 | 1.24 | 1.21 | 1.26 | 1.23 | 1.26 | 1.23 | 1.24 | 1.31 | 1.29 | 1.33 | 1.32 | 1.28 | 1.33 |

Module-level values — Table 5, p.12, CpsMark+ columns only (cell format "sensitivity/repeatability", repeatability = CV in percent; from image):

| Characteristic | Config | CA | CC |
|---|---|---|---|
| CPU cores | 1 / 2 / 3 / 4 | 1.00/2.43; 1.24/2.15; 1.35/1.46; 1.41/0.84 | 1.00/2.81; 1.51/2.66; 1.72/1.72; 1.89/1.35 |
| CPU frequency | 1 / 2 / 3 / 4 | 1.00/2.54; 1.23/2.76; 1.41/1.95; 1.63/1.12 | 1.00/2.87; 1.21/2.95; 1.38/2.38; 1.59/1.74 |
| Graphics card | 1 / 2 / 3 / 4 | 1.00/0.96; 1.01/0.64; 1.03/0.43; 1.04/0.14 | 1.00/1.62; 1.35/1.07; 1.64/0.45; 1.77/0.29 |
| Storage device | 1 / 2 / 3 / 4 | 1.00/1.05; 1.24/0.88; 1.50/0.84; 1.55/0.71 | 1.00/1.27; 1.23/0.84; 1.48/1.06; 1.51/0.53 |
| System memory | 1 / 2 / 3 / 4 | 1.00/0.84; 1.12/0.51; 1.20/0.44; 1.23/0.25 | 1.00/1.37; 1.19/0.65; 1.28/0.76; 1.32/0.42 |

Text on which workloads are sensitive, §4.7.2, p.10 left: "Generally, the performance of all the workloads is highly sensitive to the number of CPU cores, CPU frequency, and the storage devices. The performance of the workloads that require massive GPU-intensive computing, e.g., AutoCAD and Premiere, is more sensitive to graphics cards, compared to the relatively lightweight workloads, e.g., Microsoft Office. However, the performance of some workloads in the CA module, e.g., Excel and WinRAR, is more sensitive to CPU frequency and storage devices, which might be resulted from frequent float point calculations in the RAM and massive document I/O operations in disks triggered by these workloads. We also find out that the performance improvement of most workloads is not significant once the size of system memory reaches 8 GB, which is likely to be the requirement threshold for the workload software to run smoothly."

Module-level text, §4.7.2, p.9 right: "The CC module has a significantly higher sensitivity to the graphics card, the best configuration performs 1.77 times better than the base configuration, while there is no significant difference in the performance of the CA module" and "Rotation speed and storage media of hard disks also have a great influence on the performance of both modules, since the workloads involve application launching and many I/O operations, while drive interface and protocol contribute less to the module performance."

**(b) Locator:** §4.7.1 p.8; Table 3 p.9; Fig. 4 p.9; §4.7.2 pp.9–10; Table 4 p.10; Table 5 p.12.

**(c) Reading:**
- Factors varied (one at a time from the datum point): CPU cores (2/4/6/8, via BIOS on an i7-9700K), CPU frequency (2.0/2.5/3.0/3.5 "GHz" [sic, = GHz], via BIOS), graphics card (GTX 750/980/1080, RTX 2080Ti), storage (5400 RPM HDD / 7200 RPM HDD / SATA SSD / NVMe SSD), system memory (4/8/16/32 GB single-channel). Turbo Boost, Hyper-Threading, Hardware Acceleration disabled.
- Statistic: dimensionless ratio, Config k vs Config 1 of the same characteristic, computed as the inverse ratio of mean (over 20 iterations) summed time, so >1.00 = faster than Config 1. The computation is described for module performance; Table 4 applies it per workload (the paper does not restate the formula per workload). Fig. 4's y-axis is labelled "Percentage difference of performance relative to the baseline configuration" but plots ratios on a 0–2.0 scale. No dispersion (CI/SD) is given for the ratios; CVs are given separately (Fig. 5, Table 5).
- CPU frequency, Config 4: all 13 workloads between 1.57 (AutoCAD) and 1.68 (Excel); CA workloads 1.62–1.68, CC workloads 1.57–1.63. Excel (1.68) and WinRAR (1.67) are the two highest.
- Storage, Config 4: all 13 between 1.47 (HandBrake) and 1.56 (Outlook); CA workloads 1.53–1.56, CC 1.47–1.52. At Config 3, Excel and WinRAR (1.51) tie for highest; at Config 4 they are 1.53 and 1.54, below Outlook (1.56), PowerPoint (1.55) and Acrobat (1.55). So the paper's named examples (Excel, WinRAR) are the top two for CPU frequency but not uniquely the most storage-sensitive at Config 4 in Table 4.
- Paper's own classification: "all the workloads" are "highly sensitive" to CPU cores, CPU frequency and storage; Excel and WinRAR singled out as "more sensitive to CPU frequency and storage devices"; GPU-heavy workloads (AutoCAD, Premiere named) more sensitive to graphics cards; memory gains flatten after 8 GB.

**(d) Verdict: FOUND.**

---

## C-cpsmark-7 — target operating system; any gaming scenario; per-process timing

**(a) Verbatim**

OS:
- §4.2, p.4 left: "Note that CpsMark+ only supports Microsoft Windows 10."
- §4.6 baseline platform, p.8 left, and §4.7.1 datum point, p.8 right: "• OS: Microsoft® Windows® 10"
- §2.2, p.2 right (predecessor): "the third-party software used as workloads and the operating system (Windows 7) supported by the benchmark is obsoleted in burgeoning computer-related markets."

Gaming — the only occurrences of "gam" in the text:
- §2.1, p.2 right: "3DMark [8] mainly describes real-time gaming performance of graphic cards, its dependence of frame rate as the only metric limits further uses in other fields [2]."
- §3.2, p.3 left: "A game enthusiast who is keen on 3D games, for instance, might also pay attention to computational performance required by a software engineer."
- The scenario list (§4.3.2, p.4–5) is exactly four: "document manipulation, Internet service, graphic design, and multimedia processing".

Timing granularity:
- §4.4, p.6 right: "As a result, in the context of CpsMark+, we define work efficiency as the time consumption for systems under test to complete all operations related to user experience within a specific workload, i.e., application launching, input files loading, and basic operating units, which are outlined in Section 4.3.4. Then we take the defined work efficiency as the metric of CpsMark+"
- §4.4.1, p.6 right: "we predefine runtime as the time spent by each basic operating unit that actively uses system resources, while response time is the time interval between task activation and task completion."
- §4.4.1, p.7 left (Method 1, document-manipulation workloads except WinRAR, and Internet service): "Hence, we sample the start timestamps and the end timestamps of the entire task and calculate its response time, i.e., t7 − t0 in Method 1, then we sample the time intervals of irrelevant events and subtract them from the response time as the metric of these workloads."
- §4.4.1, p.7 left (Method 2, other workloads): "Finally, we sum the sampled runtime of each basic operating unit as the metric of these workloads."
- §4.2, p.4 left: "Such design reduces the influence of the MCP on system performance and enables a clear view of workload conditions provided by logs."

**(b) Locator:** §4.2 p.4; §4.6 p.8; §4.7.1 p.8; §2.1–2.2 p.2; §3.2 p.3; §4.3.2 pp.4–5; §4.4–4.4.1 pp.6–7.

**(c) Reading:**
- OS: Windows 10 only (explicit).
- Gaming: CpsMark+ contains no gaming scenario or game workload; "game" appears only when describing 3DMark and as an example of hard-to-capture user needs. Searched: full-text grep for "gam" (2 hits, both above); scenario list and Table 2 read.
- Per-process timing: not reported. The timed unit is the workload (one application task), measured either as whole-task response time minus irrelevant-event intervals (Method 1) or as the sum of per-operating-unit runtimes (Method 2); module scores sum workload times. The paper reports no per-process (OS process) timing, no CPU-time, and does not publish absolute per-workload times; its per-workload results are ratios (Table 4) and CVs (Fig. 5). Searched: grep for "process" (all hits are "process" in the procedural sense, "processor", "multimedia processing", or "program process" in §4.4.1 about sampling interference); read §4.4 fully.

**(d) Verdict: PARTIAL** — OS: FOUND. Gaming scenario: NOT FOUND (source enumerates four non-gaming scenarios; grep "gam"). Per-process timing: NOT FOUND (source times per workload / per operating unit instead; grep "process", read §4.4).

---

## C-cpsmark-8 — open source?; where the control program and resource packages are hosted

**(a) Verbatim**

- §4.1, p.3 right (design criterion): "• The benchmark should be open-source and vendor-neutral. Development of closed-source benchmarks is likely to be manipulated by certain vendors through biased workload design, leading to suspicion [21] and loss of credibility. An open-source benchmark enables public supervision and guarantees the fairness of benchmark results, which is significantly crucial in centralized procurement."
- §4.2, p.3 right → p.4 left: "CpsMark+ benchmark tool contains three components: • The automatic setup program, which installs third-party applications and the Master Control Program (MCP) in batches. MCP is responsible for benchmark execution, including test initialization, resource extraction, data integrity check, workload execution, log recording, metric measuring and calculation, and report generation. • The resource package, including the input files of workload operations. • The third-party application package, which contains the setups of all third-party applications."
- §4.2, p.4 left: "The source code of MCP is maintained online at https://github.com/wanghong3116/CpsMarkPLUS, which is still under further improvement and subject to change. The resource and third-party application packages have been uploaded on the website of National Metrology Data Center of China, which can be accessed online through https://jc.nmdc.ac.cn/view-40-609748.html."
- §4.2, p.4 left: "We have not integrated input files, workload applications and the MCP into a unitary package as most commercial benchmarks, which makes our work transparent and easy to be maintained."
- §1, p.1 right (predecessor): "To address the limitations of SYSmark and PCMark, CpsMark 1.0 [3], an open-source benchmark for microcomputers was developed."
- Article licence, p.1 footer: "This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by-nc-nd/4.0/)." (applies to the article, not the software)

**(b) Locator:** §4.1 p.3; §4.2 pp.3–4; §1 p.1.

**(c) Reading:** Hosting is explicit: MCP source code on GitHub (wanghong3116/CpsMarkPLUS); resource package and third-party application package on the National Metrology Data Center of China site. "Open source": the paper states open-source as a design criterion that CpsMark+ is designed to meet and calls CpsMark 1.0 "open-source", and it publishes MCP source; it does not contain a sentence literally declaring "CpsMark+ is released as open source" nor name a software licence. Searched: grep "open-source|open source" (6 hits: SYSmark/PCMark not open-source ×2, CpsMark 1.0, Phoronix, the §4.1 criterion ×2) and "licen" (only the article CC licence).

Supplementary (not the paper):
- GitHub (copy 6): repository exists at HEAD `bf24434261cc2b512a40b3dec1269a31a8e676a0` (2021-05-21); no LICENSE file in the tree; GitHub API reports `license: null`. README: "Adaption and development environment: windows10, vs2017-x86." A publicly visible repository without a licence file is not open source in the OSI sense; the paper does not address this.
- NMDC page (copy 7, Wayback 2022-12-09): "项目组现将其使用资源包公开，欢迎广大社会公众进行使用并给予反馈。" (my translation, outside quotes: the project team makes the resource package public and welcomes use and feedback). Install steps include "本工具仅支持Windows 10操作系统，安装及使用前需断开网络连接；" and "访问https://github.com/wanghong3116/CPSmarkPLUS，下载工具源代码并使用Visual Studio 2017 x86平台编译为可执行程序；" and "从本站下载工具配套的第三方软件包和资源包压缩文件；". The page also says "于2020年自主研发了新一代微型计算机办公性能基准测试工具CPSmark+" (developed in 2020), whereas the paper §2.2 says "finally developed CpsMark+ in 2019"; and "使用日常办公场景中有代表性的13种第三方应用软件的正式试用版作为测试负载" (13 third-party applications, official trial versions), consistent with Table 2. Live NMDC site not reachable from here (HTTP 429 then timeout).

**(d) Verdict: PARTIAL** — hosting: FOUND; "released as open source": the paper states open-source as a design criterion and publishes MCP source, but contains no explicit release/licence statement for CpsMark+.

---

## C-cpsmark-9 — what CpsMark+ says about SYSmark and PCMark methodology, and about openness / vendor neutrality

**(a) Verbatim**

1. §1, p.1 left→right: "While some newer benchmarks, e.g., Business Applications Performance Corporation's SYSmark and Futuremark's PCMark, mainly consist of common business application workloads and are more representative of commercial use, while they fail to offer an overall and scenario-oriented evaluation for general end-user experience [2]. Furthermore, they are not open-source benchmarks, thus the opacity of scoring methodology and workload operations impairs their fairness and transparency, which are essential for centralized procurement."
2. §2.1, p.2 left: "SYSmark 2018 [4] adopts real-world third-party software as workloads to evaluate overall computer performance and is widely applied in commercial markets. Usage scenarios are modeled in the form of subjectively grouped job nature like productivity and creativity, which cannot describe cooperation across tasks in a common workflow. In terms of the workloads, most of them are designed to be CPU-intensive and place little pressure on GPU and storage system, making the evaluation insensitive to graphics and I/O performance that might be cared by end users in daily use. Further, system responsiveness and program start-up are isolated and measured by specific applications, thus weakening the realistic reference value of benchmarking results."
3. §2.1, p.2 left: "PCMark 10 [5] reports an overall score calculated by the geometric mean of tested metrics for the inclusive workloads within each test group. The geometric mean returns a normalized score that treats the performance of each workload equally. This scoring methodology outputs a balanced result of performance evaluation, which neglects the diversity of importance of different workloads and is unable to describe real user experience in a specific scenario."
4. §4.4.2, p.7 left (not naming SYSmark/PCMark here): "Some benchmarks leverage automated scripts like AutoIt to initiate and navigate applications by simulating mouse clicks or keystrokes [25]. The duration of each task is measured when the completion of the task is detected by application-specific methods. Such an approach mimics practical human interaction at UI level, nevertheless, it instead impedes the accurate reflection of user experience for performance evaluation."
5. §4.8.1, p.10 right → p.11 left: "We do not select other metrics, e.g., test duration and power consumption, since SYSmark 2018 and PCMark 10 are not open-source benchmarks and do not have built-in functions to precisely measure these metrics, which as well makes it impossible to compare the sensitivity and the repeatability of them at a finer granularity, e.g., the level of workload performance."
6. §4.8.1, p.11 left: "the Productivity module of SYSmark 2018 has the highest sensitivity to all the configurations under each hardware characteristic, since it includes some workloads that have relatively high consumption of system resources, e.g., AutoIT and Shotcut, while the CA module of CpsMark+ has the second highest sensitivity"
7. §4.8.1, p.11 right: "the Productivity module of SYSmark 2018 has the lowest repeatability, i.e., the highest CV. This result is attributed to the UI-level automation of SYSmark 2018, which introduces massive unstable and delayed interactions, e.g., clicking dialog windows."
8. §4.8.2, p.11 right: "To be more specific, the Responsiveness module of SYSmark 2018 solely measures the response time of program initialization, its workloads consist of a series of sequential application starts and shutdowns, which however, cannot reflect the practical use case in daily office routines and will over amplify the influence of storage devices on the overall performance evaluation based on user experience." … "Moreover, the Essentials module of PCMark 10 contains the playback of a video with fixed duration, thus massive time consumption is included in the calculation of test metrics, which nevertheless, will dilute the contribution of better hardware characteristics to the performance improvement of this module and further reduce the benchmark sensitivity."
9. §4.8.2, p.12 left: "Secondly, for each module of PCMark 10, the scoring methodology takes the geometric mean over the test metrics of inclusive workloads, which returns a normalized score that treats the performance of each workload equally and neglects different importance of various workload operations in daily office scenarios. By contrast, as described in Section 4.5, for each module of CpsMark+, the scoring methodology takes the weighted sum over the test metrics of inclusive workloads, which emphasizes the influence of heavy or durable workload performance on simulated user experience and ignores the importance of trivial workload operations that are less involved in the routines of end users."
10. Openness / vendor neutrality, §4.1, p.3 right: see C-cpsmark-8 quote ("The benchmark should be open-source and vendor-neutral. Development of closed-source benchmarks is likely to be manipulated by certain vendors through biased workload design, leading to suspicion [21] and loss of credibility. …"). Ref. [21], p.16: "[21] U. Gordon, PCWorld, in: AMD Accuses BAPCo and Intel of Cheating with Sysmark Benchmarks, 2016, https://www.pcworld.com/article/419213/amd-accuses-bapco-and-intel-of-cheating-with-sysmark-benchmarks.html."
11. §5, p.12 right: "Specifically, in a vendor-neutral tendering of desktop computers for a Chinese company, the tendering was divided into two separate batches with different bid evaluation methods." and §5.1, p.12 right: "which were based on the standard and high-performance configurations in Bitkom's guideline for IT procurement [14], i.e., Vendor-neutral Tendering of Desktop Computers."
12. §2.2, p.2 right: "To address the mentioned limitations of SYSmark and PCMark, we released the microcomputer benchmark CpsMark 1.0 in 2014".

**(b) Locator:** §1 p.1; §2.1–2.2 p.2; §4.1 p.3; §4.4.2 p.7; §4.8.1–4.8.2 pp.10–12; §5, §5.1 p.12; ref. [21] p.16.

**(c) Reading:** Claims about SYSmark (2018): real third-party apps; scenarios grouped by job nature (productivity, creativity) without cross-task workflow; mostly CPU-intensive, little GPU/storage load; responsiveness/start-up measured in isolation; UI-level automation blamed for its lower repeatability; Responsiveness module = sequential app starts/shutdowns that over-weight storage. Claims about PCMark (10): geometric-mean scoring treats workloads equally; Essentials includes fixed-duration video playback that dilutes sensitivity. Both: "not open-source", opacity of scoring and workloads "impairs their fairness and transparency"; no built-in way to measure duration/power or per-workload results. Openness/vendor neutrality: stated as a CpsMark+ design criterion, justified by a vendor-manipulation risk citing a PCWorld news item on AMD's accusation against BAPCo and Intel (a news report of an accusation, not an adjudicated finding). "Vendor-neutral" also names the tendering format in the case study, following Bitkom's guideline. Note an internal inconsistency: §4.8.2 says PCMark 10 uses geometric mean while CpsMark+ uses a "weighted sum", but the §4.5 formula is an unweighted sum ratio (no per-workload weights); "weighted" there is the paper's term.

**(d) Verdict: FOUND.**

---

## C-cpsmark-10 — which prior benchmarks (and versions) CpsMark+ compares itself against

**(a) Verbatim**

1. §4.8, p.10 right: "In this section, we mainly focus on quantitative and qualitative comparison between CpsMark+ and two commonly used computer benchmarks in commercial field, i.e., SYSmark 2018 and PCMark 10."
2. §4.8.1, p.11 left: "The modules of SYSmark 2018 include Productivity, Creativity, and Responsiveness, while the modules of PCMark 10 include Essentials, Creativity, and Digital Content Creation." … "Note that in this section, among the three benchmarks, we only compare the sensitivity and the repeatability of the modules that evaluate system performance in similar usage scenarios."
3. §4.8.1, p.11 left: "among the three modules that evaluate system performance related to document editing and Internet surfing, i.e., the CA module of CpsMark+, the Productivity module of SYSmark 2018, and the Productivity module of PCMark 10" and "among the three modules that evaluate system performance related to multimedia processing and graphics design, i.e., the CC module of CpsMark+, the Creativity module of SYSmark 2018, and the Digital Content Creation module of PCMark 10"
4. §4.8.2, p.11 right: "Firstly, the Responsiveness module of SYSmark 2018 and the Essentials module of PCMark 10 contain a large amount of irrelevant workload operations that cannot precisely simulate user experience perceived in practical usage scenarios of tested computer systems, which is not consistent with the primary attribute of CpsMark+ and accounts for the reason why we exclude them from the above quantitative comparison."
5. Table 5 (p.12) column headers (image): "CpsMark+ (sensitivity/repeatability)" → "CA", "CC"; "SYSmark 2018 (sensitivity/repeatability)" → "Productivity", "Creativity", "Responsiveness"; "PCMark 10 (sensitivity/repeatability)" → "Essentials", "Productivity", "Digital content creation".
6. §4.8.1, p.11 right: "Generally, in terms of the modules that evaluate system performance in similar usage scenarios, CpsMark+ exhibits the highest repeatability against state-of-the-art commercial benchmarks, i.e., SYSmark 2018 and PCMark 10, while it also possesses the second highest sensitivity to the hardware characteristics tested in this experiment, which is close to the sensitivity of SYSmark 2018."
7. §6, p.15: "Extensive experiments on multiple real-world tested computer systems demonstrate high sensitivity and repeatability of benchmark scores from CpsMark+, compared to SYSmark 2018 and PCMark 10."
8. Reviewed but not experimentally compared, §2.1 p.2: "Phoronix Test System [6]", "3DMark [8]", "SPEC CPU 2017 [9]", "The Stanford SPLASH benchmark system [10]" (ref. [10] is "The SPLASH-2 programs"), "Micro benchmarks such as STREAM [11] and Imbench [sic] [12]" (ref. [12] is "Lmbench"). Predecessor: "CpsMark 1.0" (released 2014, §2.2 p.2).

Table 5 SYSmark 2018 and PCMark 10 columns (transcribed from image; cell = sensitivity/CV%):

| Characteristic | Config | SYSmark Productivity | SYSmark Creativity | SYSmark Responsiveness | PCMark Essentials | PCMark Productivity | PCMark Digital content creation |
|---|---|---|---|---|---|---|---|
| CPU cores | 1 | 1.00/3.76 | 1.00/4.97 | 1.00/4.28 | 1.00/3.15 | 1.00/2.78 | 1.00/4.15 |
| | 2 | 1.28/3.52 | 1.43/4.35 | 1.35/3.83 | 1.19/2.86 | 1.20/2.62 | 1.44/3.72 |
| | 3 | 1.41/3.04 | 1.68/4.06 | 1.38/3.51 | 1.30/2.34 | 1.34/2.17 | 1.68/3.08 |
| | 4 | 1.47/2.17 | 1.81/3.87 | 1.40/3.04 | 1.33/1.77 | 1.37/1.56 | 1.81/2.54 |
| CPU frequency | 1 | 1.00/3.88 | 1.00/5.12 | 1.00/4.35 | 1.00/3.25 | 1.00/2.91 | 1.00/3.97 |
| | 2 | 1.26/4.02 | 1.16/5.11 | 1.13/4.21 | 1.15/3.11 | 1.15/2.63 | 1.13/4.16 |
| | 3 | 1.48/3.34 | 1.32/4.53 | 1.19/3.96 | 1.32/2.48 | 1.33/2.24 | 1.32/3.52 |
| | 4 | 1.71/2.73 | 1.57/4.17 | 1.22/3.48 | 1.47/1.93 | 1.49/1.75 | 1.49/3.23 |
| Graphics card | 1 | 1.00/2.35 | 1.00/4.16 | 1.00/3.26 | 1.00/1.79 | 1.00/1.48 | 1.00/3.35 |
| | 2 | 1.04/2.14 | 1.35/3.25 | 1.12/2.74 | 1.02/1.28 | 1.01/0.81 | 1.32/2.41 |
| | 3 | 1.05/1.85 | 1.60/2.64 | 1.14/2.21 | 1.03/0.82 | 1.02/0.59 | 1.58/1.77 |
| | 4 | 1.05/1.56 | 1.75/1.83 | 1.15/1.77 | 1.03/0.56 | 1.04/0.37 | 1.71/1.46 |
| Storage device | 1 | 1.00/2.47 | 1.00/3.47 | 1.00/2.95 | 1.00/1.87 | 1.00/1.52 | 1.00/2.58 |
| | 2 | 1.29/2.15 | 1.18/3.12 | 1.47/2.72 | 1.24/1.39 | 1.21/1.07 | 1.18/2.21 |
| | 3 | 1.53/2.02 | 1.39/2.85 | 1.83/2.49 | 1.39/1.28 | 1.36/0.89 | 1.37/1.84 |
| | 4 | 1.65/1.97 | 1.47/2.34 | 2.25/2.11 | 1.47/1.35 | 1.42/0.81 | 1.43/1.57 |
| System memory | 1 | 1.00/2.20 | 1.00/3.84 | 1.00/3.09 | 1.00/1.85 | 1.00/1.67 | 1.00/2.94 |
| | 2 | 1.17/1.75 | 1.19/2.98 | 1.23/2.45 | 1.08/1.26 | 1.11/1.25 | 1.14/2.06 |
| | 3 | 1.26/1.58 | 1.29/3.25 | 1.25/2.06 | 1.15/0.99 | 1.17/0.95 | 1.25/1.71 |
| | 4 | 1.33/1.33 | 1.34/2.77 | 1.26/2.23 | 1.19/0.63 | 1.22/0.71 | 1.30/1.45 |

**(b) Locator:** §4.8, §4.8.1, §4.8.2, pp.10–12; Table 5 p.12; §2.1–2.2 p.2; §6 p.15.

**(c) Reading:** Experimental comparison: only SYSmark 2018 and PCMark 10, at module level, on sensitivity (ratio vs Config 1) and repeatability (CV %), same setup as §4.7 (20 iterations per configuration, datum point, optimisations disabled). Pairings: CA ↔ SYSmark Productivity ↔ PCMark Productivity; CC ↔ SYSmark Creativity ↔ PCMark Digital Content Creation. SYSmark Responsiveness and PCMark Essentials are shown in Table 5 but excluded from the comparison argument. Internal inconsistency: the §4.8.1 text lists PCMark 10 modules as "Essentials, Creativity, and Digital Content Creation", while Table 5 and the rest of §4.8.1 use "Productivity" as the second PCMark 10 module. Reviewed-only (no measurements): Phoronix Test System (2022 URL), 3DMark, SPEC CPU 2017, SPLASH(-2), STREAM, lmbench (spelled "Imbench"), and the predecessor CpsMark 1.0 (2014). Versions tested are stated only as product generations ("SYSmark 2018", "PCMark 10"); no build numbers.

**(d) Verdict: FOUND.**

---

## C-cpsmark-11 — real procurement deployment; any user validation period

**(a) Verbatim**

1. §5, p.12 right: "Specifically, in a vendor-neutral tendering of desktop computers for a Chinese company, the tendering was divided into two separate batches with different bid evaluation methods. For the second batch, we combined the original bid evaluation method prepared for the first batch with benchmark scores from CpsMark+ to formulate a new bid evaluation method. The original and the new bid evaluation methods were then independently adopted in the above two tendering batches, respectively. After one-year use of the wining [sic] desktops selected by the two bid evaluation methods, we independently investigated the user experience of end users from each tendering batch and collected their ratings."
2. §5.1, p.12 right: "At the beginning of 2020, a large digital marketing agency in China initialized a centralized procurement to purchase desktop computers for the employees from a functional department and a business department, which are denoted as A and B, respectively. For innovating the traditional tendering policy and validating the effectiveness of CpsMark+, within each department, the procurement was arranged as two separate batches of vendor-neutral tendering with different bid evaluation methods, which are denoted as 1 and 2. The basic information of the four tendering batches are listed in Table 6. Then during the next year, the employees of each department were divided into two groups to use the desktop computers purchased in the two tendering batches, respectively."
3. Table 6, p.13, caption "Basic information of the four tendering batches." (from image):

| Tendering batches | Purchase quantity | End users | Primary responsibilities |
|---|---|---|---|
| 1A | 39 | Department A (Functional) | Supportive market research & analysis |
| 2A | 39 | Department A (Functional) | Supportive market research & analysis |
| 1B | 46 | Department B (Business) | Marketing related service of FMCG |
| 2B | 46 | Department B (Business) | Marketing related service of FMCG |

4. §5.2.2, p.13 right: "To maintain a total score of 100 points, the benchmark score weights for the tendering batches of 2A and 2B are 63 and 70, respectively." and "The weights of the CA/CC module for the tendering batches of 2A and 2B turn out to be 0.71/0.29 and 0.12/0.88, respectively." and "𝑠𝑖 is the median score of the 𝑖th module over 5 independent tests on a certain bidding product."
5. §5.3, p.13 right: "for the winning bids purchased in the tendering batches of 1A/1B and 2A/2B, we performed a comparative analysis towards the one-year user experience rated by the respective end users."
6. §5.3.1, p.14 left: "For each tendering batch, i.e., 1A, 2A, 1B, and 2B, we randomly invited 20 end users from the corresponding group of their department to independently rate the user experience of the desktop computers purchased in this tendering batch. The questionnaires adopted for rating the user experience are similar as CSAT [34]."
7. Table 9, p.15, caption "Descriptive statistics of the user experience ratings and the average quotation for the winning bids." (from text, layout checked on image):

| | | 1A | 2A | 1B | 2B |
|---|---|---|---|---|---|
| Efficiency | Mean (%) | 3.51 (70%) | 3.90 (78%) | 3.40 (68%) | 3.93 (79%) |
| | 95% confidence interval | [3.32–3.71] | [3.69–4.10] | [3.18–3.61] | [3.70–4.15] |
| Smoothness | Mean (%) | 3.23 (65%) | 3.69 (74%) | 3.53 (71%) | 3.96 (79%) |
| | 95% confidence interval | [3.02–3.45] | [3.47–3.91] | [3.28–3.78] | [3.71–4.22] |
| Average quotation per computer, CNY | | 5316 | 5562 | 6465 | 6948 |

8. Table 10, p.15 (Student's t-test p-values, 1A vs 2A / 1B vs 2B): Efficiency "0.0070" / "0.0001"; Smoothness "0.0035" / "0.0165".
9. §4.2, p.4 left (development-time user feedback, not a deployment): "Within each phase, requirements are elicited from various end users through market research or consultation, then representatives are selected to give feedback on the outcomes of decision-making and implementation."

**(b) Locator:** §5, §5.1–5.3.3, pp.12–15; Tables 6, 9, 10 pp.13, 15; §4.2 p.4.

**(c) Reading:** Yes, the paper reports one real centralized procurement: an unnamed "large digital marketing agency in China" (the §5 opening says "a Chinese company"), beginning of 2020, two departments (A functional, B business), four batches (39+39 and 46+46 desktops = 170). CpsMark+ scores replaced performance-related technical items in batches 2A/2B. Validation period: one year of use, then a rating survey of 20 randomly invited users per batch on 5-point efficiency and smoothness scales (weighted by the applications each department used, Table 8). Reported gains: efficiency +11.11% (A) and +15.59% (B), smoothness +14.24% (A) and +12.18% (B); all four t-test p-values < 0.05. The agency is anonymous; no independent/third-party audit is described; the paper's authors ran the evaluation.

**(d) Verdict: FOUND.**

---

## C-cpsmark-12 — CC module contents; are its workloads sequenced, in what order

**(a) Verbatim**

1. §4.3.3, p.5 right: "• Comprehensive Calculation (CC) module includes the scenarios of graphic design and multimedia processing, which reflect heavy-weight use by power users skilled in professional fields, where end users possibly focus on the execution efficiency of CPU-intensive or GPU-intensive computing tasks."
2. Table 2, p.5 (CC rows): Graphic design — "Autodesk® AutoCAD" "2018 (22.0.49.0)", "Adobe® Photoshop" "CC 2019 (20.0.1)"; Multimedia processing — "Autodesk® 3ds Max" "2018 (20.0.0.966)", "Adobe® Premiere" "Pro CC 2019 (13.0)", "Adobe® After Effects" "CC 2019 (16.0)", "HandBrake" "CLI 1.3.0".
3. §4.3.4, p.6 left: "The workload operations of the CC module are briefly described in execution order as follows:" — bullets in order: "Adobe Photoshop.", "Autodesk AutoCAD.", "Autodesk 3ds Max.", "Adobe Premiere.", "Adobe After Effects.", "HandBrake." (full bullet text under C-cpsmark-4).
4. §4.3.4, p.6 right: "Within each module, the workloads are executed in the order specified above."
5. §4.4.3, p.7 right: "while for the workloads in the usage scenarios of graphic design, multimedia processing, and Microsoft Outlook, the input files are loaded after separate launch of the applications."
6. §4.4.1, p.7 left (applies to CC workloads, which are all outside the Method 1 group): "For the other workloads of CpsMark+, their basic operating units are relatively sparse and have a high concentration of resource consumption. … To accurately measure the runtime, we artificially add extra short waits, e.g., t2 − t1 in Method 2, between the heavyweight operating units to reset the resource consumption. Finally, we sum the sampled runtime of each basic operating unit as the metric of these workloads."
7. §4.2, p.4 right: "There is an automatic reboot of the tested computer system between the two modules for eliminating the impacts of varying system status (e.g., cache) on module independence."

**(b) Locator:** §4.3.3 p.5; Table 2 p.5; §4.3.4 p.6; §4.4.1 p.7; §4.4.3 p.7; §4.2 p.4.

**(c) Reading:** CC = 6 workloads across 2 scenarios. Sequenced: yes, fixed order Photoshop → AutoCAD → 3ds Max → Premiere → After Effects → HandBrake. (Table 2 lists AutoCAD before Photoshop, but Table 2 is not described as an execution order; §4.3.4 is.) No output→input chain is stated for any CC workload; the only concrete chaining example given is for CA. CC workloads use Method 2 timing (summed per-operation runtime with inserted waits); applications launched first, then input loaded. 3ds Max workload is a whale model; After Effects renders 1800 frames at 30 FPS; HandBrake transcodes 4K H.264 → 2K "H.256" [sic] MP4.

Supplementary, repository (copy 6, HEAD `bf24434…`, not the paper): CC branch of `MarkWorkInit` (`WorkMark.cpp` lines 362–375) runs 3ds Max (whale) → Premiere → After Effects → HandBrake — four workloads; Photoshop and AutoCAD are instead added in the CA branch (lines 356, 358), their classes set `m_eMarkClassify = E_MARK_CLASSIFY_Comprehensive_Application` (`Photoshop.cpp` line 15, `AutoCADMark.cpp` line 11), and `ResultDetailUI.cpp` lines 53–54 hold counts "4" (CC) and "9" (CA). So the May-2021 code places the graphic-design workloads in CA, unlike the paper's Table 2 / §4.3.3. The relative order Photoshop → AutoCAD → 3ds Max → Premiere → After Effects → HandBrake is the same as the paper's; the last commit swapped After Effects to follow Premiere. The code was not built or run.

**(d) Verdict: FOUND.**

---

## C-cpsmark-13 — authors, title, journal, article number, DOI

**(a) Verbatim (p.1)**

- Journal line: "BenchCouncil Transactions on Benchmarks, Standards and Evaluations 2 (2022) 100084"
- "Research article"
- Title: "CpsMark+: A scenario-oriented benchmark system for office desktop performance evaluation in centralized procurement via simulating user experience"
- Byline: "Yue Zhang, Tong Wu ∗" / "National Institute of Metrology, China" / "∗ Corresponding author."
- "https://doi.org/10.1016/j.tbench.2023.100084"
- "Received 8 June 2022; Received in revised form 28 December 2022; Accepted 1 January 2023"
- "Available online 5 January 2023"
- "2772-4859/© 2023 The Authors. Publishing services by Elsevier B.V. on behalf of KeAi Communications Co. Ltd. This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by-nc-nd/4.0/)."

Crossref (copy 4): title as above; container-title "BenchCouncil Transactions on Benchmarks, Standards and Evaluations"; volume "2"; issue "4"; article-number "100084"; published-print 2022-10; authors Yue Zhang (first), Tong Wu. Elsevier API (copy 5): PII "S2772-4859(23)00001-7"; coverDisplayDate "October 2022".

**(b) Locator:** p.1 header, title block, footer; Crossref record; Elsevier API coredata.

**(c) Reading:** Authors Yue Zhang and Tong Wu (corresponding), National Institute of Metrology, China. Journal: BenchCouncil Transactions on Benchmarks, Standards and Evaluations, vol. 2, issue 4 (October 2022 issue), article 100084, DOI 10.1016/j.tbench.2023.100084. The input bibliographic entry's author names, title, journal, article number and DOI all match. Year nuance: the DOI and copyright carry 2023 and the article went online 5 January 2023, but it is assigned to the volume 2 (2022) October issue; a citation "(2023)" matches online publication, while the page header and Crossref issue date give 2022. The input entry gives no volume/issue; the source has vol. 2, no. 4.

**(d) Verdict: FOUND.**

---

## Verdict counts (one headline verdict per topic)

- FOUND: 11 (C-cpsmark-1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13)
- PARTIAL: 2 (C-cpsmark-7, 8)
- NOT FOUND: 0 as headline (sub-parts: C-cpsmark-7 gaming scenario and per-process timing)
- PREMISE NOT IN SOURCE: 0
- COPY UNREACHABLE: 0
