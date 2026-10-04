# 9.10 Chrome tab-set campaign — pooled results (meas-ci:desktop:2026-10-04, runs #74–#76)

Machine: EPYC 7763. Repeats pooled per subject; `probe` jobs are never repeats.

## chrome-tabs

Repeats: ['1', '2', '3', '4', '5']  ·  mode ['full']

`renderer-hidden` tasks (D127): ['4']  ·  the spare (D128): ['1']  ·  one count in every repeat

| repeat | build | order | page loads off/on | plain off (steady) | plain on (steady) | pids stable off/on | WebUI off/on | extension launch off/on | extension steady off/on | hidden | spare |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Google Chrome 154.0.8037.57  | off on | 5/5 | 5–5 | 6–6 | 1/1 | 1/1 | 4/4 | 0/0 | 4 | 1 |
| 2 | Google Chrome 154.0.8037.57  | on off | 5/5 | 5–5 | 6–6 | 1/1 | 1/1 | 4/4 | 0/0 | 4 | 1 |
| 3 | Google Chrome 154.0.8037.57  | off on | 5/5 | 5–5 | 6–6 | 1/1 | 1/1 | 4/4 | 0/1 | 4 | 1 |
| 4 | Google Chrome 154.0.8037.57  | on off | 5/5 | 5–5 | 6–6 | 1/1 | 1/1 | 4/4 | 1/0 | 4 | 1 |
| 5 | Google Chrome 154.0.8037.57  | off on | 5/5 | 5–5 | 6–6 | 1/1 | 1/1 | 4/4 | 0/0 | 4 | 1 |

