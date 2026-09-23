# Handoff — task 9.10 Scenarios and timelines (2026-09-23)

The nightly research routine ran stages 1 and 2 of `_dev/research/jioh/research-slice-workflow.md` for issue #15. Stage 3 (decisions) is 인지오's. No file under `dataset/` or `docs/` changed.

## Done

- Stage 1: `_dev/research/jioh/task-9.10-scenarios-timelines/scope-card.md`, which has 70 items in groups A–K, the boundary, the one-observation situation, topics T1–T13 and the compiled numbers the decisions move.
- Stage 2: `search/input.md`; the four class records `search/S1-literature.md` (33 candidates), `S2-project-docs.md` (26), `S3-traces-datasets.md` (13 plus analysis appendices), `S4-ci-observability.md` (16, three of them local checks in the routine's container, not a runner); and `search/candidates.md`, which lists the observations, the candidates per item group and the Not-found list. The source copies stayed in the routine's clone (gitignored), so the records identify every copy by URL or commit and SHA-256.
- The TODO line was already `[WIP]` with `(#15)` when the routine started (commit `1ad17ff`, when the task was delegated), so step 0 needed no commit.
- Records S1, S2 and S4 were each committed as their reader returned, because the session's stop hook rejects untracked files. S3 and `candidates.md` went into the stage-2 commit.

## The one-observation situation

No candidate grounds the whole slice, or any whole situation, on Linux. The observations that exist are:

- **SWELL-KW** (S3-01): raw logs, open access. 25 people in a lab on Windows in 2012. It records focus, switching, page loads, mail sends and background process starts during office work only.
- **BEHACOM** (S3-04): 12 users on their own PCs, Windows and Linux, over 8 weeks in 2019–20. It records the foreground executable and active-app count per minute, not the full running set. This is the only natural-use trace with Linux executable names.
- **Test Pilot v2 dumps** (S3-02): Firefox users in 2010, 159 of them on Linux, giving window and tab counts.
- **Chrome 69 Windows telemetry** (S1-09): renderer and site counts.
- **Windows knowledge-worker logging studies**: switching and focus data (S1-01, S1-03, S1-13, S1-21, S1-24).
- **Configuration and source for stock Linux desktops**: default timers, DKMS hooks and object counts, session processes, Chromium's process model, and the Steam runtime and Proton process chains (S2, S4-08…S4-10). This is documentation, not observation of use.

Nothing observed covers activity order (T3), desktop job sizes (T7), operations per minute (T9), launches per session (T10), Linux call or media composition (T11), or a Linux gaming session beyond one unverified `ps` tree (S3-08).

## Stage 3's first question

Stage 3 must first settle what may count as a situation's observation under decision 3:

- whether a user-behaviour observation from another platform (SWELL-KW, Windows lab; BEHACOM, mostly Windows) can ground focus windows, switching and co-occurrence;
- whether configuration and source documentation (S2, S4) can ground task sets and names where no use is observed (background timers, session processes, the Proton process chain);
- otherwise, which situations become recorded design.

Items 1–2 (arc orders), 5 (focus windows) and 36–37 (the C7 scan and the pre-committed misses) depend on this answer most directly.

## Flags

- **Unreachable:** github.com web and API returned 403 to this session. That blocked the scx issues 9.4 handed on and the byte-verified copy of gamemode issue #457 (S3-08 was read only through WebFetch). ACM DL returned 403 for Chang et al. CHI 2021, Blake et al. ISCA 2010 and Flautner et al. ASPLOS 2000.
- **Restricted:** LANL needs registration and pseudonymises process names. The 8-week Windows data set of arXiv 2105.09900 is available only after vetting.
- **Handled by workaround:** the OpTC Google Drive was over quota, so its corrected copy was read by HTTP range instead. src.fedoraproject.org and gitlab.winehq.org raw files returned a bot-check page, so the readers used `git clone` instead.
- **Not verified:** S2's ZFS object count (≈306) is its own estimate from Kbuild lists; S4-16's DKMS timings come from a 4-vCPU container, not a pinned runner.
- **Hand-offs that may arrive after this card:** 9.5 (Thunderbird `send` re-observation), 9.7 (release) and 9.9 (the session campaign; D19 landed after the card's commit) are still open and may hand more to 9.10.
