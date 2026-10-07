# Handoff — task 9.12 Related-work and proposal prose (2026-10-07)

The nightly research routine produced this from issue #18. Stages 1 and 2 of `_dev/research/jioh/research-slice-workflow.md` are done. Stage 3 (decisions) is 인지오's. Everything is committed and pushed on branch `jioh/dataset-rebuild`.

## Files

- `_dev/research/jioh/task-9.12-related-work-prose/scope-card.md` — the boundary and 70 items in five groups:
  - A, `related-work.md`: 20 items.
  - B, `research-proposal.md` plain-text claims, with the boundary docs' sentences merged in: 27 items.
  - C, the registry entries that only prose cites: 12 items.
  - D, the guidebook vol-02 map: 1 item.
  - E, the hand-offs, most of them pass-through to 9.15: 10 items.
  - Topics T1–T15 are stated neutrally.
- `search/input.md` — the reader input.
- The four class records:
  - `search/S1-literature.md`: 29 candidates.
  - `S2-project-docs.md`: 44 candidates.
  - `S3-traces-datasets.md`: 17 candidates.
  - `S4-ci-observability.md`: 10 candidates. These are documentation and method only. Nothing was run on a runner; there is a labelled sandbox illustration.
- `search/candidates.md` — the observations table, the candidates for each item, and what no class found.

Deviations from the routine:
- Step 0 needed no edit, because the TODO line was already `[WIP] … (#18)` at `60149db`.
- The records landed one commit per reader as each finished, instead of one commit for all four.

## The one-observation situation

No observation can ground the whole slice, and none is needed: the items are claims about what documents say. Every cited source in `related-work.md` now has a hashed copy and verbatim passages (S1-01–S1-18, S2-01–S2-20, S2-30–S2-32). The proposal's plain-text quantities are the only items an observation could settle:
- scheduler decision cost
- context-switch cost
- switch rate
- local LLM latency

For those, the readers found the following:
- Context-switch costs from 599 ns to 3.8 µs direct, on old or named machines (S1-01, S1-21, S1-23).
- One Android trace, at 1 826–4 089 switches per CPU per second (S3-07).
- No measured Linux pick-next cost.
- No end-to-end latency for a short structured output from a 3–8B model on consumer x86.

Findings stage 3 should see first:
- **Items 16 and 21 (Game Mode).** No vendor documents a list of executables:
  - Windows says Game Mode "works by default for most Windows games" (S2-16).
  - macOS turns it on in full screen and lets apps opt in with `LSSupportsGameMode` (S2-18, S2-20).
  - Feral's GameMode is requested by the game or entered through `gamemoderun` (S2-19).
- **Item 2.** `sched-ext.rst` makes no verifier-safety claim (S2-01, S2-02).
- **Item 7.** SteamOS 3.8 gives "Initial support" for LAVD, opt-in by command (S2-15). Meta calls LAVD a "candidate" default (S2-11, S2-13).
- **Items 11 and 19.** ASA is an XGBoost classifier that reports 96.83 % recognition accuracy (S1-11). AKTS (arXiv 2609.12276, September 2026) measures small LLMs classifying telemetry and finds them at chance (S1-19).
- **Item 26.** `updatedb` (plocate, findutils, mlocate), LocalSearch, Baloo and Déjà Dup all declare an idle or low class. ClamAV, borg and restic do not. Debian counts are in S3-01.
- **Item 27.** OSTEP names BSD, Solaris and Windows NT as MLFQ forms and never Linux (S1-02).
- **Item 70.** The 2011 BAPCo departures concerned SYSmark 2012 and the "weighting of scores" (S2-40–S2-42).

## Stage 3's first question

Item 21, the paper's baseline framing: the proposal, related-work, research-claims and background-guide all say that shipping game modes work from lists of known executables, and that `whitelist` reproduces them. Every vendor document read says otherwise (S2-16, S2-18–S2-20). Stage 3 has to decide what the `whitelist` condition claims to reproduce, and which source grounds that claim. `ananicy-rules`, a name-keyed catalogue, is the candidate the registry already points to.

After that:
- items 2 and 3 (sched_ext and scx wording against the existence-only tier)
- item 19 (the "first at the recognition layer" priority claim, against ASA and AKTS)
- item 26 (the declared-class sentence)

## Flags from the readers

- **Returned HTTP 403:**
  - ACM DL (Kgent; David et al. 2007)
  - the OpenReview PDF (LumOS, so only its abstract was read)
  - ossna2024.sched.com
  - openbenchmarking.org and phoronix.com (Cloudflare)
  - github.com discussions and api.github.com
  - the Debian Code Search API (its no-JS HTML page worked)
- **Proxy 502:** git.sesse.net and the Xbox content API host. The Xbox Support Game Mode article is script-only and could not be obtained, so the Windows Update question stays unread first-hand.
- **Other dead ends:**
  - the WoWAH home page answered 500; the WPI mirror worked
  - eprints.soton answered 401
  - archive.org's availability API answered 429
  - salsa needed a login
  - semiaccurate.com had a TLS name mismatch, which was not bypassed
- **Paywalled:** Statista.
- **Not downloaded because of size:** wowah.rar (578 MB) and 0_SWELL.zip (7.5 GB).
- **Partial reads:** Nvidia's own reason for leaving BAPCo and Dessau's original blog post were not found; the record carries reports of them only.
- S3's T12 rates are foreground-application switches, not changes in the set of running applications.
