## Source: focal-arxiv26

Copies used for this source (all retrieved 2026-09-13; local root `_dev/research/jioh/2026-09-13-verification/sources/focal-arxiv26/`):

- arXiv abstract page https://arxiv.org/abs/2604.19541 → `abs.html`; https://arxiv.org/abs/2604.19541v1 → `abs-v1.html`
- v2 PDF https://arxiv.org/pdf/2604.19541v2 (arXiv GenPDF, PDF CreationDate 2026-07-21) → `v2.pdf`, text `v2.txt`
- v1 PDF https://arxiv.org/pdf/2604.19541v1 (PDF CreationDate 2026-04-22) → `v1.pdf`, text `v1.txt`
- v2 author TeX source https://arxiv.org/src/2604.19541v2 → `src-v2/sample-sigconf-authordraft.tex` (+ `src-v2/figures/Data_contruction_2.png`)
- DesktopBench dataset repo https://huggingface.co/datasets/HaoranYin/desktopbench, git clone at commit `49c3683061073ecf8cfadf962ce5d563a2e1dd43` ("Initial public release", 2026-07-19), which is the target of annotated tag `v0.1.0` → `hf-desktopbench/`; HF API JSON → `hf-dataset-api.json`
- Companion code repo metadata https://api.github.com/repos/Haoran2099/focal → `gh-focal-repo.json` (not cloned; metadata only)

**v1 vs v2.** A word-level diff of the extracted text of v1 and v2 shows only three differences: v1 marks "Cao∗" with a "∗Corresponding author." footnote, and the arXiv side-stamp reads `arXiv:2604.19541v1 [cs.MA] 21 Apr 2026` (v1) vs `arXiv:2604.19541v2 [cs.MA] 18 Jul 2026` (v2). Every passage quoted below is therefore present in both versions. Quotes are copied from the v2 TeX source (the PDF text extraction drops inter-word spaces); PDF page locators are given for the v2 PDF.

### C-focal-1 — Interruption split: session count, session structure, primary and interrupting activities

(a) Verbatim.

TeX line 457 (PDF p. 4, §4 intro):
> DesktopBench has two splits: \textbf{DesktopBench-Multitask} for interleaved cross-application workflows and \textbf{DesktopBench-Interruption} for controlled $A\!\rightarrow\!B\!\rightarrow\!A$ timelines that test whether a method can preserve and resume task state after interruption.

TeX lines 507–508 (PDF pp. 4–5, §4.1):
> \textit{DesktopBench-Interruption (100 sessions).}
> To evaluate robustness to context switching, we construct an $A\!\rightarrow\!B\!\rightarrow\!A$ split in which a long-running creative task~$A$ is interrupted by a short YouTube browsing task~$B$ before resuming. This tests whether a model can preserve and recover the latent state of task~$A$ without cross-task drift.

TeX lines 517–518 (PDF p. 5, §4.3):
> It contains 420 sessions in total: 320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption. Multitask sessions contain 2--4 tasks, while Interruption sessions contain exactly two tasks under the $A\!\rightarrow\!B\!\rightarrow\!A$ structure.
> Table~\ref{tab:dataset} summarizes the key statistics. The average session length is 17.3 actions for DesktopBench-Multitask and 16.5 for DesktopBench-Interruption.

Figure 3 caption (TeX line 540, PDF p. 6): `(d)~Interrupted task distribution. (e)~Actions per segment (Interruption).` Panel (e) x-axis labels in the PDF text layer: `A-pre YouTube A-post`.

Released generator `hf-desktopbench/scripts/provenance/generate_videogui_youtube_aba_sessions.py` (commit 49c3683), lines 51–56 and 59–64:
```python
def choose_split_point(action_count: int) -> int:
    if action_count < 4:
        raise ValueError("A-B-A sessions require at least 4 actions in the interrupted task.")
    if action_count == 4:
        return 2
    return action_count // 2
```
```python
    youtube_tasks = [task for task in tasks if task["prefix"] == "YT"]
    interruptable_tasks = [task for task in tasks if task["prefix"] != "YT" and task["action_count"] >= 4]

    if not youtube_tasks:
        raise RuntimeError("No YouTube subtasks found in the source data.")
    if len(interruptable_tasks) < target_sessions:
        raise RuntimeError("Not enough interruptable tasks to build the requested number of A-B-A sessions.")
```
Same file, lines 69–70:
```python
    interruptable_tasks.sort(key=lambda item: (-item["action_count"], item["task_uid"]))
    selected_a_tasks = interruptable_tasks[:target_sessions]
```

Released data `hf-desktopbench/data/interruption_sessions/train.jsonl`, first row, verbatim:
```json
{"scenario": "a_to_youtube_to_a", "segments": [{"action_indices": [18, 19, 20, 21, 22, 23, 24, 25, 26], "subtask_id": 3, "task_id": "PS_03"}, {"action_indices": [0, 1], "subtask_id": 0, "task_id": "YT_10"}, {"action_indices": [27, 28, 29, 30, 31, 32, 33, 34, 35, 36], "subtask_id": 3, "task_id": "PS_03"}], "session_id": "aba_session001"}
```
`hf-desktopbench/README.md`:
> The 100 interruption sessions materialize to 1,691 actions (16.91 per session).
> The paper text reports 16.5 for the latter average; `16.91` is the value computed
> from the released catalog and is recorded as a known discrepancy.

(b) Locators: arXiv:2604.19541v2 §4 intro, §4.1, §4.3, Table 3, Fig. 3(d)(e) (PDF pp. 4–6); TeX source lines as given; DesktopBench v0.1.0 files as given.

(c) Reading. The Interruption split has **100 sessions**. Each is an A→B→A timeline: one task A, interrupted by a short YouTube browsing task B, then A resumes; the paper counts this as exactly two tasks (three segments: A-pre, YouTube, A-post). The paper calls A "a long-running creative task". In the released generator, A is any non-YouTube VideoGUI subtask with ≥4 actions, taking the 100 longest; A is split at ⌊n/2⌋ actions (2 if n = 4); B is one YouTube (`YT`) VideoGUI subtask, chosen to balance reuse. My own count over the released `interruption_sessions` file (python): all 100 rows have 3 segments, segment 2 is always a `YT_*` subtask, segments 1 and 3 are always the same task/subtask; A-pre 4–18 actions (mean 6.15), YouTube 2–10 (mean 4.17), A-post 4–18 (mean 6.59); A prefixes: PPT 23, PS 16, AE 16, RW 12, WEB 10, VLC 7, CC 4, DV 4, PR 3, SD 3, AI 2. Caveats: (1) 17 of the 100 A tasks are `WEB`/`VLC`, which the paper's own Table 2 files under the "Reference" family ("Tutorials, asset browsing"), not a creative/editing family — so "creative task" does not hold for every session in the release. (2) Average length: paper 16.5, released catalog 16.91 (the release itself flags this). (3) The generator's internal record says `"task_count": 3` for each A-B-A session (it counts segments), while the paper says exactly two tasks.

(d) Verdict: **FOUND**.

### C-focal-2 — Multitask split: session count, template count, fields each recorded action carries

(a) Verbatim.

TeX line 501 (PDF p. 4, §4.1):
> Because VideoGUI was built for single-task automation, it lacks the session organization and metadata required for activity logging. We therefore augment each action with the foreground application name (\texttt{app}) and window title (\texttt{title}), while retaining the original task descriptions as semantic reference (Figure~\ref{fig:dataset_construction}).

TeX lines 505–506 (PDF p. 4, §4.1):
> \textit{DesktopBench-Multitask (320 sessions).}
> Sessions are assembled through template-based composition grounded in realistic creative workflows. We use 20 patterns spanning video-centric workflows such as \texttt{video$\to$ref$\to$video} and design-centric workflows such as \texttt{generation$\to$image$\to$slide}. Each session contains at least two distinct application prefixes, and compatible subtasks may be reused to compose richer workflows.

TeX lines 324–332, §3.2 problem formulation (PDF p. 3, eqs. 1–2):
```latex
We model a \textit{session} as an ordered desktop interaction sequence generated within one continuous working context, consisting of $N$ actions:
\begin{equation}
    \mathcal{S} = \{(m_i, v_i)\}_{i=1}^{N}
\end{equation}
where each action contains structured metadata
\begin{equation}
    m_i = (\text{app}_i,\ \text{title}_i)
\end{equation}
and a screenshot $v_i \in \mathbb{R}^{H \times W \times 3}$. A session contains $K$ latent \textit{tasks}; each action is associated with a task id $y_i \in [1, K]$. Define the action-index set of task $k$ as
```

Table 3 (PDF p. 5), text layer:
> Number of sessions 320 100
> Average session length (actions) 17.3 16.5
> Task count per session 2–4 2

Figure 2 (`src-v2/figures/Data_contruction_2.png`, image text, transcribed from the image — not a text layer): middle panel "Metadata Annotation": "1. Collect one screenshot at a time from the raw screen recording dataset", "2. Identify the active application and its window title from the screenshot", "3. Output structured Result"; example table with columns "Task | app | title" and rows "PPT_12_0 | PowerPoint | project - Saved to this PC", "SD_7_2 | Chrome | Stable Diffusion"; right panel "Human Verification & Session Assembly".

Released generator `hf-desktopbench/scripts/provenance/generate_videogui_multitask_sessions.py` lines 20–44 define `VIDEO_PATTERNS` with 9 entries (`video_ref`, `ref_video`, `video_ref_video`, `ref_video_video`, `generation_video`, `video_generation`, `ref_video_generation`, `generation_ref_video`, `ref_video_video_generation`) and `DESIGN_PATTERNS` with 11 entries (`image_slide`, `slide_image`, `reference_image`, `reference_slide`, `reference_image_slide`, `image_reference_slide`, `slide_reference_image`, `generation_image`, `generation_image_slide`, `reference_generation_slide`, `reference_image_slide_generation`); e.g. line 21:
```python
    ("video_ref", ["editing_video", "reference"], 0.7),
```
Same file lines 360–361:
```python
    parser.add_argument("--target-sessions", type=int, default=320)
    parser.add_argument("--seed", type=int, default=20260324)
```

Released annotation file `hf-desktopbench/data/active_window_annotations/train.jsonl`, first row verbatim:
```json
{"app": "Adobe After Effects 2023", "image_id": "AE_0_action000", "label_source": "ollama_vlm", "title": "project (converted).aep"}
```
`hf-desktopbench/scripts/provenance/annotate_active_window_with_ollama.py` lines 2–9:
```
"""Annotate active window app/title for screenshots using an Ollama VLM.

Output fields per image:
- image_id: e.g. PPT_14_action004
- app: normalized app name from allowed list
- title: active window title (browser tab title or project/file name)
- screenshot_path
- file_name
```
`hf-desktopbench/README.md` table row and limitation:
> | `active_window_annotations` | 2,572 | Stable image IDs and project-generated app/title labels |

> - App/title and summary labels are model-generated and can contain errors.

`hf-desktopbench/scripts/prepare_videogui_raw_from_hf.py` (runtime reconstruction) lines 11–20:
```
Each output record corresponds to one atomic action with fields required by
FOCAL experiments:
- timestamp (ISO 8601)
- app
- title
- duration
- kpm
- cpm
- screenshot_path
- gt_task_id / gt_subtask_id / gt_subtask_query
```
and `scripts/rebuild_desktopbench.py` line 13:
```python
DROP_FIELDS = {"timestamp", "duration", "kpm", "cpm", "screenshot_paths"}
```

(b) Locators: arXiv:2604.19541v2 §3.2 eq. (1)–(2) (p. 3), §4.1 (p. 4), Table 3 (p. 5), Figure 2 (p. 5); TeX lines as given; DesktopBench v0.1.0 files at commit 49c3683.

(c) Reading. **320 sessions**; each has 2–4 tasks and at least two distinct application prefixes; mean 17.3 actions (the release computes 5,540 actions / 320 = 17.3125). The paper says "template-based composition" and **20 patterns**; the released generator indeed holds 20 (9 video-band + 11 design-band), each a weighted sequence of application families, and it also forbids repeating a prefix within a session. Per action, the paper's model input is **(app, title) metadata plus one screenshot**, with the original VideoGUI task description retained as a semantic reference; the ground-truth task id is the label. Caveats on the word "recorded": (1) `app`/`title` were not captured from the OS — the release says they are VLM-generated from each screenshot (`label_source: "ollama_vlm"`, script default model `qwen3-vl:8b`), and Figure 2 says "Identify the active application and its window title from the screenshot"; the paper's wording "augment each action with the foreground application name … and window title" does not say this. (2) In the full runtime reconstruction each record also carries the upstream VideoGUI action payload (`action_id`, `action_type`, `start_position`, `action_narration`), `subtask_query`, `action_sequence`, and ground-truth task ids, while `timestamp`, `duration`, `kpm`, `cpm` are dropped (see C-focal-4). (3) No per-action process/PID/CPU field exists anywhere in the paper or release.

(d) Verdict: **FOUND** (template count is stated as "20 patterns").

### C-focal-3 — How sessions were produced (recorded natural use vs constructed) and from which dataset

(a) Verbatim.

TeX line 265 (PDF p. 2, §1):
> To validate FOCAL, we conduct experiments on DesktopBench, reconstructed from VideoGUI, with both multi-task sessions and interruption scenarios.

TeX line 456 (PDF p. 4, §4):
> We reconstruct \textbf{VideoGUI}~\citep{lin2024videogui} into \textbf{DesktopBench}, a benchmark for multi-task desktop activity logging. Following Table~\ref{tab:task_family}, we regroup its source tasks into five application families spanning editing, generation, slides, and reference activities.

TeX line 518 (PDF p. 5, §4.3):
> Because compatible source subtasks may be reused when composing workflows, these counts measure instantiated actions with multiplicity rather than unique screenshots.

Figure 2 `\Description` (TeX line 495):
> Diagram showing the dataset construction pipeline from original VideoGUI subtasks to Multi-task and Interruption session splits.

`hf-desktopbench/README.md`:
> Reconstruction is pinned to:
>
> - `VideoGUI/VideoGUI-Mid-Plan@6852d8c9f2b9c586d7ff7cce2611080140f1a30c`
> - `VideoGUI/VideoGUI-Action@0a8110739acf4c766d4d55c9672cb38d1d9bfcbd`

`hf-desktopbench/scripts/prepare_videogui_raw_from_hf.py` lines 210–212 and 258:
```python
            for action_row in ordered_actions:
                app = str(mid_info.get("app") or action_row.get("app") or "Unknown")
                duration = 6.0
```
```python
                current_ts = current_ts + timedelta(seconds=duration)
```

(b) Locators: arXiv:2604.19541v2 §1 (p. 2), §4 and §4.1 (p. 4), §4.3 (p. 5); Fig. 2; DesktopBench v0.1.0 README and scripts at commit 49c3683.

(c) Reading. Sessions are **constructed, not recorded natural use**. The authors took single-task VideoGUI subtasks (screenshots of human re-enactments of YouTube tutorials — see C-videogui-1) and concatenated them: Multitask by sampling one of 20 family patterns, Interruption by splitting one subtask around a YouTube subtask. Source subtasks are reused across sessions (the paper says counts are "with multiplicity"). The source dataset is **VideoGUI** (Lin et al., NeurIPS 2024 D&B), specifically the Hugging Face `VideoGUI-Action` (2,572 rows at the pinned revision) and `VideoGUI-Mid-Plan` (462 rows) datasets. No inter-session or cross-subtask timing comes from real use; the runtime timeline is synthetic (fixed 6.0 s per action from a base timestamp), and even that is dropped.

(d) Verdict: **FOUND**.

### C-focal-4 — Release location, version, data licence, script licence; per-action timestamps

(a) Verbatim.

Paper: searched `v1.txt`, `v2.txt` and the v2 TeX source for `github`, `hugging`, `licen`, `release`, `zenodo`, `http`, `available`; and listed every link annotation in both PDFs. The only URLs are reference-list DOIs/URLs (NeurIPS, OpenAI docs, PMLR). The acknowledgments block in the TeX source (line 1220) reads `Omitted for anonymous review.` inside a disabled `\iffalse` (line 864) … `\fi` (line 1224) region, so it does not print. The arXiv licence field for the paper itself is `http://arxiv.org/licenses/nonexclusive-distrib/1.0/` (PDF metadata `/License`).

`hf-desktopbench/README.md` (commit 49c3683):
> DesktopBench is the benchmark used by
> [FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal
> Desktop Summarization](https://arxiv.org/abs/2604.19541). This public `v0.1.0`
> release contains only project-generated annotations, session constructions,
> ground-truth summaries, provenance, and deterministic reconstruction tools.
>
> It does **not** redistribute VideoGUI screenshots, image bytes, screenshot
> paths, or copied `raw_records` containing upstream action text. Complete runtime
> inputs are reconstructed locally from pinned upstream revisions.

> As of this release, the upstream Hugging Face dataset cards do not declare a
> data license. Access to this public repository does not grant any right to
> VideoGUI artifacts. Users must review and comply with upstream terms before
> downloading or using them.

> The companion [`Haoran2099/focal`](https://github.com/Haoran2099/focal)
> repository provides the supported wrapper:

> Scripts are MIT licensed under [LICENSE_CODE](LICENSE_CODE). The dataset itself
> is marked `license: other`; repository visibility does not grant a redistribution
> license for the annotations or GT. Cite the paper using
> [CITATION.cff](CITATION.cff).

`hf-desktopbench/DATA_TERMS.md`:
> The project-generated annotations, session mappings, and ground-truth summaries
> in this public `v0.1.0` release are available for research inspection. Public
> repository visibility is not a license grant: the dataset remains marked
> `license: other`, and no redistribution, sublicensing, or republication license
> is granted for annotations or ground-truth summaries unless separately
> authorized by the applicable rights holder.

`hf-desktopbench/LICENSE_CODE` lines 1–3:
> MIT License
>
> Copyright (c) 2026 HAORAN YIN

`hf-desktopbench/CITATION.cff`:
> version: 0.1.0
> date-released: 2026-07-19
> repository: "https://huggingface.co/datasets/HaoranYin/desktopbench"

`hf-desktopbench/manifests/upstream.json` (excerpt):
```json
      "license_declared_in_dataset_card": null,
      "repo_id": "VideoGUI/VideoGUI-Action",
      "revision": "0a8110739acf4c766d4d55c9672cb38d1d9bfcbd"
```

Timestamps: `scripts/prepare_videogui_raw_from_hf.py` line 212 `duration = 6.0`, line 237 `"timestamp": current_ts.isoformat(),`, line 258 `current_ts = current_ts + timedelta(seconds=duration)`, lines 283–286:
```python
        "--base-timestamp",
        type=str,
        default="2026-01-01T08:00:00+00:00",
        help="ISO 8601 base timestamp for sequential assignment",
```
`scripts/rebuild_desktopbench.py` line 13 and line 76:
```python
DROP_FIELDS = {"timestamp", "duration", "kpm", "cpm", "screenshot_paths"}
```
```python
        updated = {key: value for key, value in row.items() if key not in DROP_FIELDS}
```
Upstream `VideoGUI/VideoGUI-Action` dataset card at revision 0a81107 (`sources/videogui-arxiv24/hf-VideoGUI-Action-README.md`) lists features `split, app, screenshot_start, action_type, action_narration, start_position, end_position, scroll_value, task_id, subtask_id, action_id` — no time field.

GitHub API for `Haoran2099/focal` (`gh-focal-repo.json`): `created_at` 2026-07-19T11:33:21Z, `license.spdx_id` `MIT`.

(b) Locators: as given; DesktopBench HF repo commit `49c3683061073ecf8cfadf962ce5d563a2e1dd43`, tag `v0.1.0` (annotated tag object pointing at that commit).

(c) Reading. The **paper does not state any release location, version or licence** for DesktopBench. The release exists separately: **Hugging Face dataset `HaoranYin/desktopbench`, v0.1.0, released 2026-07-19** (one day after arXiv v2), with a companion GitHub repo `Haoran2099/focal` (MIT). **Data terms:** the data is marked `license: other`; it is available "for research inspection" but no redistribution/sublicensing/republication licence is granted for annotations or GT; no VideoGUI screenshots are redistributed; upstream VideoGUI HF cards declare no licence, and users must check upstream terms themselves. **Scripts:** MIT. **Per-action timestamps: not included.** The released files carry no time field; the reconstruction script assigns synthetic timestamps (base 2026-01-01T08:00Z, +6.0 s per action, ordered by task id) and then drops `timestamp`, `duration`, `kpm`, `cpm` when building the runtime records; the upstream VideoGUI-Action rows have no time field either. Caveat: the VideoGUI card points to a Google Drive "full metadata, recording" archive that I did not download; whether it holds real timings is unchecked.

(d) Verdict: **PARTIAL** — release location, version, data terms, script licence and timestamp absence are FOUND in the release artifacts, but **NOT in the paper itself** (searched as described).

### C-focal-5 — Authors, title, arXiv number, version and date, venue status

(a) Verbatim.

`abs.html` meta tags: `citation_title` = `FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization`; `citation_author` in order `Yin, Haoran`, `Wen, Zhiyuan`, `Cao, Jiannong`, `Yuan, Bo`, `Yang, Ruosong`; `citation_arxiv_id` `2604.19541`.

`abs.html` submission history (tags stripped):
> [v1] Tue, 21 Apr 2026 15:00:41 UTC (4,239 KB)
> [v2] Sat, 18 Jul 2026 13:19:51 UTC (3,848 KB)

Subjects: `Multiagent Systems (cs.MA); Human-Computer Interaction (cs.HC)`. No Comments and no Journal-ref field on the abstract page.

v2 PDF p. 1 author block order (text layer): `Haoran Yin … Zhiyuan Wen … Jiannong Cao … Ruosong Yang … Bo Yuan` (affiliations: The Hong Kong Polytechnic University ×4; China Mobile Communications Company Limited Research Institute for Bo Yuan). Side stamp: `arXiv:2604.19541v2  [cs.MA]  18 Jul 2026`. Running header pp. 2–9: `Preprint. Under review.`

(b) Locators: https://arxiv.org/abs/2604.19541 (retrieved 2026-09-13); v2 PDF p. 1–2.

(c) Reading. Yin, H., Wen, Z., Cao, J., Yuan, B., Yang, R. (arXiv metadata order); title as above; arXiv:2604.19541; latest version v2 submitted 2026-07-18 (v1 2026-04-21). **Preprint, no venue**: arXiv has no journal reference, and the PDF says "Preprint. Under review." (ACM `acmart` template, acknowledgments "Omitted for anonymous review"). Caveat: the author order **differs** between the arXiv metadata / PDF metadata (`…Cao; Bo Yuan; Ruosong Yang`) and the printed author block in both PDFs (`…Cao, Ruosong Yang, Bo Yuan`). The DesktopBench `CITATION.cff` follows the arXiv metadata order.

(d) Verdict: **FOUND** (with the author-order discrepancy noted).

## Source: videogui-arxiv24

Copies used (retrieved 2026-09-13; local root `_dev/research/jioh/2026-09-13-verification/sources/videogui-arxiv24/`):

- arXiv abstract page https://arxiv.org/abs/2406.10227 → `abs.html` (only v1 exists: `[v1] Fri, 14 Jun 2024 17:59:08 UTC (46,368 KB)`)
- v1 PDF https://arxiv.org/pdf/2406.10227v1 → `v1.pdf` (24 pp.), text `v1.txt`
- NeurIPS proceedings page https://proceedings.neurips.cc/paper_files/paper/2024/hash/804e757b7d7043c26701c3a313032101-Abstract-Datasets_and_Benchmarks_Track.html → `neurips-abstract-804e.html` (found via web search; the page itself is the evidence)
- The URL printed in FOCAL's reference [14], https://proceedings.neurips.cc/paper_files/paper/2024/hash/0fa4e4715c2d876d5ba7bb04f6f7f75f-Abstract-Datasets_and_Benchmarks_Track.html → HTTP 404 (`neurips-abstract.html`); same hash on papers.nips.cc → 404
- HF API + dataset cards at pinned revisions: `VideoGUI/VideoGUI-Action@0a8110739acf4c766d4d55c9672cb38d1d9bfcbd` → `hf-VideoGUI-Action.json`, `hf-VideoGUI-Action-README.md`; `VideoGUI/VideoGUI-Mid-Plan@6852d8c9f2b9c586d7ff7cce2611080140f1a30c` → `hf-VideoGUI-Mid-Plan.json`, `hf-VideoGUI-Mid-Plan-README.md`

### C-videogui-1 — Identity of the VideoGUI paper; whether DesktopBench derives from it

(a) Verbatim.

arXiv `abs.html` meta: title `VideoGUI: A Benchmark for GUI Automation from Instructional Videos`; authors `Lin, Kevin Qinghong`, `Li, Linjie`, `Gao, Difei`, `WU, Qinchen`, `Yan, Mingyi`, `Yang, Zhengyuan`, `Wang, Lijuan`, `Shou, Mike Zheng`; date `2024/06/14`; Comments `24 pages, 16 tables, 17 figures`.

NeurIPS proceedings page text:
> VideoGUI: A Benchmark for GUI Automation from Instructional Videos
> Kevin Qinghong Lin, Linjie Li, Difei Gao, Qinchen Wu, Mingyi Yan, Zhengyuan Yang, Lijuan Wang, Mike Zheng Shou
> Advances in Neural Information Processing Systems 37  (NeurIPS 2024)
> Datasets and Benchmarks Track

VideoGUI v1 PDF p. 3 §3.1 (text layer):
> Pipeline. The VideoGUI creation pipeline is illustrated in Fig.2. For each software, (i) we manually
> select instructional videos paired with high-quality transcripts from YouTube, focusing on those
> teaching practical and novel usages. To collect the human manipulation trajectory , we build a
> simulated environment to monitor user behaviors including Click, Drag, Type/Press, and Scroll.
> (ii) We invite five participants who first watch the selected video and then try to reproduce the effects
> shown using our simulator, which records all cursor and keyboard activities (e.g., [x, y] coordinates of

p. 4:
> Data statistic. Overall, VideoGUI includes 178 tasks across 11 software applications (Fig. 3a) on
> Windows and Web browsers (Chrome, Edge, Firefox). It comprises 86 complex tasks (i.e., full task)
> and 92 simple tasks (i.e., subtask) that do not require high-level planning, where those 86 full tasks
> can be further divided into 371 subtasks, resulting in a total of 463 subtasks. Fig. 3b shows the
> distribution of number of actions per task. In total, we collect 2,712 atomic manual actions.

VideoGUI-Action card YAML at revision 0a81107: `num_examples: 2572`. VideoGUI-Mid-Plan card at 6852d8c: `num_examples: 462`.

FOCAL side (from focal-arxiv26): TeX line 456 `We reconstruct \textbf{VideoGUI}~\citep{lin2024videogui} into \textbf{DesktopBench}`; FOCAL reference [14] (v2 PDF p. 9): `Kevin Qinghong Lin, Linjie Li, Difei Gao, Qinchen Wu, Mingyi Yan, Zhengyuan Yang, Lijuan Wang, and Mike Zheng Shou. 2024. VideoGUI: A Benchmark for GUI Automation from Instructional Videos. InAdvances in Neural Information Processing Systems, Vol. 37.` (followed by the 0fa4e47… URL). DesktopBench `manifests/upstream.json` pins `VideoGUI/VideoGUI-Action` (expected_rows 2572) and `VideoGUI/VideoGUI-Mid-Plan` (expected_rows 462).

(b) Locators: arXiv:2406.10227v1 abstract page, PDF pp. 3–4 §3.1; NeurIPS 2024 proceedings page (hash 804e757b…); HF cards at the named revisions; FOCAL v2 §4 and ref. [14]; DesktopBench v0.1.0 manifest.

(c) Reading. VideoGUI = Lin, Li, Gao, Wu, Yan, Yang, Wang, Shou, "VideoGUI: A Benchmark for GUI Automation from Instructional Videos", arXiv:2406.10227 (v1 only, 2024-06-14), published in NeurIPS 2024 Datasets and Benchmarks Track (Advances in NeurIPS 37). Its data are five participants re-enacting YouTube tutorials in 11 applications on Windows/web inside the authors' recording simulator — scripted reproductions, not natural desktop use; 178 tasks, 463 subtasks, 2,712 atomic actions (the public HF Action split has 2,572 rows). **Yes, DesktopBench derives from it**: FOCAL states it, and the DesktopBench release rebuilds from the two pinned VideoGUI HF datasets. The VideoGUI paper itself of course says nothing about DesktopBench. Caveat: the NeurIPS URL printed in FOCAL's reference [14] returns HTTP 404; the working proceedings URL has hash `804e757b7d7043c26701c3a313032101`.

(d) Verdict: **FOUND**.
