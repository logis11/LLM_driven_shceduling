# Task 9.12 — Related-work and proposal prose: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — `whitelist` reproduces the name-keyed catalogue, `ananicy-rules`; Game Mode is cited for its category only (2026-10-08)
> Amended by D3 (CachyOS installs ananicy-cpp with the catalogue and enables it by default: the design point ships in a distribution; `:536` and the `whitelist` lines restated to it).
> Amended by D6 (the `whitelist` condition becomes two conditions: the shipped catalogue, and the strongest name table in its design).
> Amended by D45 (the §2.1 Windows row gains the Windows Update deferral; the Xbox Support article read rendered, S2-58).
> Amended by D94 (the macOS row's versions: Game Mode on macOS Sonoma 14 or later; the LSSupportsGameMode declaration listed for macOS 26.0 and later).

By 인지오's decision, scope-card item 21: the `whitelist` condition reproduces the name-keyed catalogue design point — a hand-maintained table from executable name to priority class, matched by name — grounded in `ananicy-rules`, with `ananicy` for the matching rule. No shipped game mode is cited as working from a list of executables, and no sentence says an operating system ships the design point.

- **The design point.** `ananicy-rules` (verified 2026-09-12 at commit `03ef03f`): a table of 15 813 entries from process name to type, 13 528 of them typed `Game`, maintained "by the CachyOS team and the community". `ananicy` (the ananicy-cpp README): `name`, the only required field, is "used for match processes by exec bin name". No source read states that a distribution enables the daemon or the catalogue by default.
- **What the game modes document** (search records S2-16 to S2-20):
  - Windows (S2-16, the four Microsoft Learn pages): "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer"; a developer may declare the `expandedResources` capability; "The app must be in the foreground and have focus before exclusive resources are granted." How a game is recognised is not stated. The Xbox Support article (S2-17) renders by script and was not read.
  - macOS (S2-18, Apple Support 105118; S2-20, the `LSSupportsGameMode` Info.plist key): "When your game enters full screen, Game Mode automatically turns on for that game"; an app declares support with a Boolean key — "If you don't include this key in your Info.plist, Game Mode might not turn on for your game." How macOS decides an app is a game is not stated in any copy read.
  - Feral GameMode (S2-19, commit `a74b810`): games "request a set of optimisations", or are launched through `gamemoderun`; its `whitelist`/`blacklist` filter is user-set and commented out in the example config. No built-in list.
- **Kept.** "Game Mode is on or off" (`docs/research-proposal.md:160`): `HasExpandedResources` reports whether the app runs "in Game Mode or shared mode" (S2-16), and Apple's is a per-game on/off (S2-18).

Hands to 9.15:

- `docs/research-proposal.md` — `:34`, `:195`, `:802` (Game Mode's "lists of known game executables", "executable list") restated without a list; the §2.1 table's rows `:148–149` restated to each vendor's documented trigger — macOS: full screen, with the app's `LSSupportsGameMode` declaration; Windows: on by default for most games, the mechanism undocumented, an optional `expandedResources` declaration, foreground and focus required; `:159`'s enumeration limit ("Game Mode works from a whitelist") attributed to the name-keyed catalogue; `:530`'s `whitelist` row "Reproduces" the name-keyed catalogue (`ananicy-rules`); `:536`'s "what shipping operating systems actually do today" restated to what a deployed, community-maintained daemon does.
- `docs/background-guide.md:18`, `:60`; `docs/research-claims.md:83`, `:132`; `docs/terminology.md:189–190`; `docs/daemon/daemon-guide.md:92`.
- The guidebook: vol-01 `:1360`, `:3376`, `:3438`, `:3719`; vol-03 `:57`, `:115`, `:1631`; vol-04 `:448`, `:492`, `:1414`, `:1797`.
- `dataset/sources.yaml`'s `gamemode-docs` note ("Existence of the category and of the whitelist design point only") restated to the category; no dataset file cites the entry, so it stays only if a dataset value derives from it (the contributor recipe, `docs/references.md:16`).

Compiled effect: none.

## D2 — related-work states Game Mode as a shipped category, Windows and macOS each from its own documentation; the name-table instance is ananicy alone (2026-10-08)
> Amended by D45 (the `:40` sentence gains the Windows Update deferral) and D99 (`gamemode-docs` has five Learn pages, D53).

By 인지오's decision, scope-card item 16: `docs/related-work.md:40`'s sentence "Windows Game Mode reprioritizes resources when a foreground executable matches a curated list [gamemode]" leaves the name-table paragraph. Game Mode is stated in a sentence of its own as a shipped foreground-game category, Windows citing `gamemode-docs` and macOS citing Apple's documentation. The paragraph's premise sentence ("These systems validate our premise — process identity carries actionable scheduling information") rests on ananicy alone.

- **Windows** (`gamemode-docs`; S2-16, the four Microsoft Learn pages; 2026-09-13 read R07, C-gamemode-1): Game Mode grants "a game exclusive or priority access to hardware resources" — exclusive CPU sets ("Gets the expected number of exclusive CPU sets that are available to the app when in Game Mode") and "increased GPU prioritization"; "The app must be in the foreground and have focus before exclusive resources are granted." It "works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer"; a developer may declare the `expandedResources` capability. How a game is recognised is not stated. The deprecation note is carried with the APIs: "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."
- **macOS** (S2-18, Apple Support "Use Game Mode", support.apple.com/en-us/105118, "Published Date: September 14, 2026", SHA-256 `10857702…`; S2-20, the `LSSupportsGameMode` Info.plist key, SHA-256 `a712464b…`): on a Mac with Apple silicon and macOS Sonoma 14 or later, "When your game enters full screen, Game Mode automatically turns on for that game", "giving your game the highest priority access to your CPU and GPU, lowering usage for background tasks". The `LSSupportsGameMode` key is a Boolean by which an app declares support, listed for macOS 26.0 and later — "If you don't include this key in your Info.plist, Game Mode might not turn on for your game." How macOS decides an app is a game is not stated.
- **"reprioritizes resources"** (C-gamemode-1, WORDING-FIX) restated to the two resources Microsoft names; other work is kept off the reserved cores, not throttled (`gamemode-docs`, "What the documentation does state").

Hands to 9.15:

- `docs/related-work.md:40` restated as above; `:44`'s note ("Game Mode is closed — cite Microsoft documentation but reconstruct from ananicy's design") brought in line with D1.
- `docs/references.md` — Apple's two pages entered as deployed-system entries under the id-minting rule (one entry per citable artifact), each with its URL, accessed 2026-10-07, and the copy's SHA-256 from S2-18 and S2-20; the `LSSupportsGameMode` entry's cite names the human-readable page (developer.apple.com/documentation/bundleresources/information-property-list/lssupportsgamemode), the JSON being the copy read. `gamemode-docs`' cite line: its "[Exact URLs to pin.]" replaced by the four Learn URLs of S2-16.
- `docs/guidebook/vol-02-related-work.md` ch. 7.2, the same restatement.

Compiled effect: none.

## D3 — related-work's ananicy sentence: ananicy-cpp and the CachyOS catalogue, which CachyOS installs and enables by default (2026-10-08)
> Amended by D6 (the `whitelist` lines of D3's hand-off restated to the two conditions).

By 인지오's decision, scope-card item 17, after a stage-3 read (search records S2-45, S2-46, S3-19): `docs/related-work.md:40`'s sentence "On Linux, ananicy adjusts process priorities from a community-maintained catalog mapping process names to priority classes; the catalog is maintained by hand, and every entry is a human decision made in advance [ananicy]" is restated to the sources.

- **The daemon** (`ananicy`): ananicy-cpp, the maintained daemon — upstream Ananicy is archived since 2023-03-21 (S2-30). A rule's `name` is "used for match processes by exec bin name", optionally narrowed by `cmdlines`; its type sets nice, I/O class and scheduling policy — `Game` nice −5, `BG_CPUIO` nice 16 with the idle I/O class and `SCHED_IDLE` (S2-30 `README.md:71–79`; S2-31; S2-32 `00-types.types:4`, `:22`).
- **The catalogue** (`ananicy-rules`): "maintained by the CachyOS team and the community"; entries are contributed by pull request or issue, checked by a lint for syntax and duplicates (S2-32 `README.md:3`, `:63–65`, `:73`). 15 813 entries at `03ef03fb`, which is tag `1.1.49`, the version CachyOS packages (S2-45, S3-19).
- **Shipped by default** (new): CachyOS's installer installs `cachyos-settings` on both its paths — a pacstrap base package online, the live image offline; the package depends on `ananicy-cpp` and `cachyos-ananicy-rules`, and its install hook runs `systemctl enable` on `ananicy-cpp` (S2-45, CachyOS-PKGBUILDS `03924f78`, cachyos-calamares `5f098957`). Observed on the published desktop ISO of 2026-08-09 (SHA-256 equal to the published one): `ananicy-cpp` 1.2.0 and `cachyos-ananicy-rules` 1.1.47 installed as dependencies of `cachyos-settings`, the catalogue 15 794 entries, and `ananicy-cpp.service` linked into `multi-user.target.wants` (S2-46).
- **"every entry is a human decision made in advance"** restated to what the history shows: every entry entered by a contributor's commit — the current entries last changed by 112 authors — and a rule acts only on a name the catalogue already carries (S3-19). Whether a contributor wrote an entry by hand or generated it outside the repository is not observable.
- **The catalogue's growth** (S3-19, counted by the registry entry's method): 880 entries at the end of 2022, 1 066 (2023), 1 367 (2024), 1 645 (2025), 6 329 at 2026-03-30, 14 731 at 2026-06-29, 15 813 at `03ef03fb`; `Game` 965 at the end of 2025, 13 528 at `03ef03fb`. Two contributors last changed 85.3 % of the current entries.

Hands to 9.15:

- `docs/related-work.md:40` restated as above, naming ananicy-cpp and the CachyOS catalogue, citing `ananicy` for the daemon and its matching rule, `ananicy-rules` for the catalogue, and the new CachyOS entry for its default installation. The section heading "Semantic recognition shipped today: static name tables" holds for the catalogue.
- D1's lines restated to the shipped design point: `docs/research-proposal.md:530`'s `whitelist` row reproduces the name-keyed catalogue CachyOS ships enabled (`ananicy-rules`); `:536`'s "what shipping operating systems actually do today" restated to what a shipping Linux distribution, CachyOS, does by default; `docs/terminology.md:189–190`, `docs/background-guide.md:60` and the guidebook's `whitelist` rows (vol-04 `:448`, `:1797`) the same.
- `docs/references.md`: a deployed-system entry for CachyOS's default installation of ananicy-cpp — the `cachyos-settings` package (PKGBUILD and install hook at CachyOS-PKGBUILDS `03924f78`, version 1.4.1), the installer's base package list (cachyos-calamares `5f098957`), and the 2026-08-09 ISO observation (S2-46) in its status line; `ananicy-rules` — the catalogue packaged as `cachyos-ananicy-rules` 1.1.49 = `03ef03fb`, and the growth counts with their commits; `ananicy` — the version pinned (ananicy-cpp 1.2.0 as shipped, S2-46; upstream commit `3554447c` read, S2-31) and upstream Ananicy's archived state.

Compiled effect: none.

## D4 — the proposal's Feral GameMode row: the game requests the mode, or the user launches it under `gamemoderun`; the whitelist is a filter (2026-10-08)

By 인지오's decision, scope-card item 25: `docs/research-proposal.md:150`'s row "Linux | Feral GameMode daemon | Explicit opt-in list, or game calls the API itself" is restated to Feral's repository (S2-19, FeralInteractive/gamemode `a74b8106a2236d1f2696aa44c93bc4c8ef13b42e`, 2026-06-15, version 1.8.2), and Feral GameMode is cited from a new registry entry.

- **How a game enters** (`README.md:2`, `:23–28`; `data/gamemoded.8.in:49–56`): GameMode "allows games to request a set of optimisations be temporarily applied to the host OS and/or a game process"; "For games/launchers which integrate GameMode support, simply running the game will automatically activate GameMode. For others, you must manually request GameMode when running the game. This can be done by launching the game through `gamemoderun`"; the library call is `gamemode_request_start()`.
- **The whitelist** (`example/gamemode.ini:49–55`): "If "whitelist" entry has a value(s) gamemode will reject anything not in the whitelist" — a user-set filter on requesters, commented out in the example config. It opts no program in; "Explicit opt-in list" leaves.
- Item 18 (`docs/related-work.md:44`'s note) needs no decision of its own: D1–D3 answer it, and D2 hands `:44` to 9.15.

Hands to 9.15:

- `docs/research-proposal.md:150` restated: the game requests the mode through the library or an integrating launcher, or the user launches it under `gamemoderun`; an optional user-set whitelist restricts which requesters are accepted. The guidebook's copy of the row, vol-03 `:58` ("명시적 참여 목록, 또는 게임이 직접 API를 호출"), the same.
- `docs/references.md`: a deployed-system entry for Feral GameMode, pinned to commit `a74b8106` (version 1.8.2), with S2-19's copies of `README.md`, `data/gamemoded.8.in` and `example/gamemode.ini` and their SHA-256.

Compiled effect: none.

## D5 — the audio-workstation case: no game mode's documentation addresses it; the shipped catalogue registers the major DAWs, in the music players' class (2026-10-08)
> Amended by D6 (the catalogue is the shipped-catalogue condition's rule list, not `whitelist`'s).

By 인지오's decision, scope-card item 37: `docs/research-proposal.md:640`'s "no shipping Game Mode covers it. It is simultaneously our hardest deadline test and a clean whitelist-failure case" is restated to the sources; "a clean whitelist-failure case" is withdrawn.

- **The game modes.** Microsoft's and Apple's Game Mode documentation speaks of games only and names no audio workstation (S2-16, S2-18, S2-20). Feral's GameMode acts on any process that requests it or is launched under `gamemoderun` (S2-19, D4), so a user can apply it to an audio workstation; its documentation speaks of games only.
- **The shipped catalogue** (`ananicy-rules` at `03ef03fb`, which `whitelist` reproduces, D1, D3; S3-19, "Passages: audio entries"): `reaper`, `bitwig-studio` and `BitwigStudioEngine`, `ArdourGUI`, `lmms` and `audacity` are entries of type `Player-Audio` (nice −4); the audio servers `pipewire`, `pipewire-pulse`, `wireplumber` and `pulseaudio`, and `mixxx`, are `LowLatency_RT` (nice −12, best-effort I/O). `Player-Audio` is also the type of nineteen music players (`spotify`, `rhythmbox`, `mpd`, …). No entry names `qtractor`, `rosegarden`, `zrythm`, `renoise`, `hydrogen`, `carla` or `jackd`.
- **What the catalogue's limit is for this case.** It registers the major audio workstations by name and gives them the music players' class: a recording session and playback receive the same nice value. A registration failure holds only for an audio workstation the catalogue does not carry.
- Whether the proposal's Family 3 keeps an audio-workstation row — an audio workstation shown absent from the catalogue at the pinned commit — is that family's design, not decided here. The deadline figures in the same sentence ("1–3 ms rather than gaming's 16 ms") are item 36.

Hands to 9.15:

- `docs/research-proposal.md:640` restated: no game mode's documentation addresses audio workstations, Feral's can be applied by the user; the catalogue registers the major audio workstations, in the music players' class; "a clean whitelist-failure case" removed. `:635`'s row ("Audio DAW + plugin chain") no longer stated as unregistered software under Family 3's heading ("Where the whitelist fails structurally") while it names no program absent from the catalogue.
- The guidebook: vol-04 `:1410`, `:1414` the same.

Compiled effect: none.

## D6 — the `whitelist` condition becomes two: the shipped catalogue, and the strongest name table in its design (2026-10-08)
> Amended by D91 (research-proposal.md:60 and :216's clause restated to the two conditions).
> Amended by D105 (ananicy-cpp matches a rule by `argv[0]`'s basename; the open points homed).
> Amended by D109 (on ananicy-cpp's key the catalogue keys 19 of the 35 bound names, every name in 7 of 50 files — a different seven; "after truncation" leaves).
> Amended by D115 (`:536` per condition: the shipped catalogue answers RQ2, the strongest name table carries the claim; by 인지오's decision).

By 인지오's decision, raised by D1–D5: the experiment carries two name-table conditions in place of `whitelist`, each answering the claim that names it.

- **The shipped-catalogue condition** reproduces what CachyOS ships enabled (D3): its rule list is `ananicy-rules`' entries at the pinned commit, matched by name as ananicy-cpp matches them, with a stated mapping from the catalogue's types to the recognition vocabulary (design). It answers research question 2 as worded — "Does that reading beat what shipping systems do?" (`docs/research-claims.md:128–132`).
- **The strongest-name-table condition** is a rule list in the catalogue's design — name to situation, matched by name — written to cover the software the dataset presents as known; the unregistered software of the proposal's Family 3 and the invented names of familiarity tiers 4–5 carry no rule. It tests world knowledge against enumeration at its best: "the strongest non-LLM implementation of semantic recognition" (`docs/related-work.md:34`), the condition `docs/workload/building-plan.md:86` expects to score perfectly on the single-situation calibration files, and the condition that fails structurally on mechanism 2, world knowledge (`docs/research-claims.md:62–76`).
- **Why one list cannot be both** (S3-19, "the core set's process names in the catalogue"): of the 35 process names the 50 compiled core-set files bind, the catalogue at `03ef03fb` carries 14 exactly and none more after truncation to 15 characters; every name of a file is carried in 7 of 50 files. Unmatched include `kdenlive`, `make`, `python`, `HandBrakeCLI`, `deja-dup`, `tracker-miner-f`, `thunderbird-bin` and most of the game chain's threads.
- **Open, for the build of the two conditions:** their identifiers; the type-to-vocabulary mapping; which names the strongest table carries at the familiarity tiers' boundary; and how ananicy-cpp compares a rule's `name` — the 15-character `comm` or the executable's basename (not read; S3-19) — read from ananicy-cpp's source at the pinned version before the shipped-catalogue list is built.

Hands to:

- **9.14** — the condition list amended where the harness freezes it: `harness/tools/harness/evaluator.py` (`CONDITIONS`), the schemas that enumerate conditions (`harness/{records,grades,scores,aggregates,experiments,guards}/schema/*.json`), `harness/guards/guard-spec.yaml`'s `applies_to` lists, in its one harness changelog entry; the two identifiers chosen there. The RQ0 gate's conditions (`fixed`, `random`, `oracle`) are unchanged.
- **The build of the two conditions** (no phase yet in `_dev/TODO.md`) — the two rule lists and the open points above. Phase 6's spec froze the condition names (`_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md:87`); the amendment is this entry.
- **9.15** — every doc naming `whitelist` restated to the two conditions: `docs/research-proposal.md:530`, `:536` (D1, D3), `docs/research-claims.md:83`, `:128–137`, `docs/related-work.md:34`, `:36`, `:42`, `:48`, `docs/terminology.md:133`, `:181`, `:189–192`, `docs/background-guide.md:60`, `docs/daemon/daemon-guide.md:25`, `:44`, `:92`, `:121`, `:136`, `:152`, `docs/data-contracts.md:49`, `:344`, `:376`, `:382`, `:467`, `:516`, `docs/harness/metrics.md:74`, `docs/harness/harness-and-records-guide.md:1139`, `:1243`, `:1390`, `docs/workload/building-plan.md:86`, `:113`, `docs/workload/scenario-catalog.md:6`, the guidebook (vol-04 `:448`, `:492`, `:1797`, and every other `whitelist` line), and the docs the sweep `grep -rn -i whitelist docs` finds beyond these.

Compiled effect: none on any compiled file.

## D7 — related-work's sched_ext sentence: first released in 6.12, loadable at runtime, integrity and fallback as the kernel states them; "verifier-enforced safety" leaves (2026-10-08)

By 인지오's decision, scope-card item 2: `docs/related-work.md:8`'s "sched_ext, merged in Linux 6.12 … custom schedulers load at runtime with verifier-enforced safety and automatic fallback to the default scheduler [schedext]" is restated to the kernel's own statements, citing `schedext-docs`.

- **First release** (S2-47): `kernel/sched/ext.c` and `Documentation/scheduler/sched-ext.rst` are absent at v6.11 and present from v6.12-rc1; Linux 6.12 is the first release carrying sched_ext. The scx README's "starting from version 6.12" (S2-09) agrees.
- **Loadable at runtime** (S2-01, `sched-ext.rst:14` at v6.12): "The BPF scheduler can be turned on and off dynamically anytime." `kernel/Kconfig.preempt:150–151` at v6.12 (S2-47): "Rapid scheduler deployments: Non-disruptive swap outs of scheduling policies in production environments."
- **Integrity and fallback** (S2-01 `:16–19`; S2-02 `:18–21` at mainline `7b63ef2d`): "The system integrity is maintained no matter what the BPF scheduler does. The default scheduling behavior is restored anytime an error is detected, a runnable task stalls, or on invoking the SysRq key sequence `SysRq-S`." The fallback target is CFS at v6.12 and "the fair-class scheduler" at mainline.
- **"verifier-enforced safety" leaves.** The kernel document names the BPF verifier only in a comment of its example code (S2-01 `:145`, S2-02 `:195`), the Kconfig help not at all (S2-47); `schedext-docs`' constraint (1) stands: no verifier-safety claim is sourced here.

Hands to 9.15:

- `docs/related-work.md:8` restated as above; `:59`'s placeholder row (`schedext` "Linux 6.12") is item 20's.
- `docs/references.md` `schedext-docs`: the v6.11 / v6.12-rc1 / v6.12 tree check (S2-47) in its status line as the ground of "first released in 6.12".

Compiled effect: none.

## D8 — related-work's production-scheduler sentence: per scheduler, as each operator reports it; `scx_rusty` leaves (2026-10-08)
> Amended by D113 (the LPC slides, the LPC abstract and LWN 1051430 minted under the new talk, abstract or news-report type; by 인지오's decision).

By 인지오's decision, scope-card item 3, after a stage-3 read (S2-48): `docs/related-work.md:8`'s "Production schedulers built on it — scx_rusty, scx_layered, scx_lavd — demonstrate that non-default policies are deployable at scale [scx]" is restated per scheduler, each statement attributed to its operator. `scx` stays an existence-only source: it grounds that the repository ships the schedulers (fifteen at `v1.1.3`, S2-09), not their deployment.

- **`scx_layered`** — Meta reports it deployed on "1M+ machines with significant perf gains" (S2-48: the LPC 2024 sched_ext microconference talk "The current status and future potential of sched_ext", 2024-09-18, presenter David Vernet, Meta, per the conference timetable; its slides "sched_ext status and plans", which also call the schedulers "Still very early days"; no operator or method named on the slide) and across its Reality Labs GPU fleet — "we deployed it to the entire Reality Labs GPU fleet with tens of thousands of GPUs" (S2-11, LPC 2025 contribution 2039, Meta speakers). LWN's "over one million machines" (S2-12) is the report of the 2024 slide, not a second source.
- **`scx_lavd`** — Valve's SteamOS 3.8 (stable 2026-06-18) offers it as an opt-in scheduler: "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`" (S2-15); Meta presented it as a candidate default fleet scheduler — "SCX_LAVD is one such candidate" (S2-11, LPC 2025 contribution 2099).
- **`scx_rusty`** — no deployment statement in any copy read (S2-09, S2-48); it leaves the sentence.
- The sentence's conclusion is restated to what the statements carry: a non-default policy deployed at fleet scale, as its operator reports — not "demonstrate that non-default policies are deployable at scale".

Hands to 9.15:

- `docs/related-work.md:8` restated as above.
- `docs/references.md`: deployed-system or footnote-tier entries for the LPC 2024 slides "sched_ext status and plans" (URL, accessed 2026-10-08, SHA-256 from S2-48; footnote tier, as `lavd-ossna24`), the LPC 2025 abstract "Accelerating AI training fleets with sched_ext" (contribution 2039, S2-11), and Valve's SteamOS 3.8 release note (S2-15); `scx`'s role line keeps existence only.
- The guidebook: vol-02 ch. 3.3–3.4 ("얼마나 실제로 쓰이나", `:1226–1240`) given the operators' statements above beside the repository's. Also found in this sweep, with no source behind it: vol-02 `:2699` ("지금 수백만 대의 컴퓨터에서 실제로 돌고 있는 소프트웨어입니다", of Game Mode and the priority daemons) — restated to what D2 and D3 ground, with no count.

Compiled effect: none.

## D9 — "Valve shipping it": Valve sponsors LAVD and ships it in SteamOS as a selectable scheduler, installed and configured but not enabled (2026-10-08)

By 인지오's decision, scope-card item 7, after two stage-3 reads (S2-49, S2-50): `docs/related-work.md:20`'s note "Valve shipping it legitimizes 'desktop scheduling matters'" is restated to what Valve ships.

- **Sponsorship** (S2-09, `scheds/rust/scx_lavd/src/bpf/lat_cri.bpf.c:3–4` at scx `v1.1.3`): "Copyright (c) 2023-2025 Valve Corporation. Author: Changwoo Min"; the author develops it "as part of his work at Igalia on SteamOS and the Steam Deck" (S2-13).
- **Selectable in SteamOS 3.8** (S2-15, S2-49): Valve's release notes, the only ones through 2026-10-08 that name LAVD, say "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`"; Valve's settings daemon `steamos-manager` offers `None` and `LAVD` through an "Optional interface for adjusting CPU scheduler", and selecting `LAVD` starts `scx.service`.
- **Not enabled out of the box** (S2-50, the SteamOS 3.8.14 recovery image, `BUILD_ID=20260707.10`): `scx-scheds` 1.1.1 is installed, `/etc/default/scx` sets `SCX_SCHEDULER=scx_lavd`, and `scx.service` is not enabled — no `wants` link in the root or the `/etc` overlay, presets `disable *` with no line naming `scx`. The kernel's default scheduler runs until the user selects LAVD.
- **Meta** — a "candidate" default fleet scheduler (S2-11), not adopted; that half of `grounding-sources.md:30` is item 58's.

Hands to 9.15:

- `docs/related-work.md:20`'s note restated: Valve sponsors LAVD's development and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default.
- `docs/references.md`: a deployed-system entry for SteamOS's LAVD support — the SteamOS 3.8 release note (S2-15), `steamos-manager` at `302d37b9` (S2-49), and the 3.8.14 image observation (S2-50) in its status line.

Compiled effect: none.

## D10 — related-work's scx_lavd sentence: the mechanism from its code and README, the origin in its README's words; "most developed" leaves (2026-10-08)

By 인지오's decision, scope-card item 5: `docs/related-work.md:16`'s "The most developed recent instance is scx_lavd, which estimates each task's latency criticality from its wake/wait patterns and task-chain structure, and feeds that estimate into deadline assignment; it originated in gaming workloads, where mis-scheduling within a task chain surfaces as stutter [lavd]" is restated to scx_lavd's source and README at scx `v1.1.3` (S2-09), with the OSS NA 2024 slides (`lavd-ossna24`, S2-10) beside them.

- **Inputs** (`scheds/rust/scx_lavd/src/bpf/lat_cri.bpf.c:179–186`): "A task is more latency-critical as its wait or wake frequencies (i.e., wait_freq and wake_freq) are higher, and its runtime is shorter"; a weight factor (`:192`) that boosts wakeups and kernel tasks and respects nice (`:25–27`, `:68–71`, `:110–113`).
- **Task chains** (`:194–201`): "If both are high, the task is in the middle of a task chain"; criticality propagates between waker and wakee, "Forward propagation is to keep the waker's momentum forward to the wakee, and backward propagation is to boost the low-priority waker" (`:209–217`). Slide 25 defines the chain A → B → C on runtime, wake frequency and wait frequency.
- **Use** (`scx_lavd/README.md:7–12`): "leveraging the task's latency-criticality information in making various scheduling decisions (e.g., task's deadline, time slice, etc.)"; slide 22: "(Virtual) deadline based algorithm".
- **Origin** (`README.md:20–23`): "`scx_lavd` is initially motivated by gaming workloads. It aims to improve interactivity and reduce stuttering while playing games on Linux."
- **Leave:** "The most developed recent instance" (no source compares behavioural schedulers); "where mis-scheduling within a task chain surfaces as stutter" as one causal claim (no copy states it; the README states the aim, the slides and LWN 991205 the chain's latency-critical tasks, each stated as its source states it).

Hands to 9.15:

- `docs/related-work.md:16` restated: scx_lavd estimates each task's latency criticality from its wait and wake frequencies, runtime and weight, propagating it between wakers and wakees along task chains, and uses it to set the task's virtual deadline and time slice; it was motivated by gaming workloads, to reduce stuttering. Cited to the scx_lavd README and `lat_cri.bpf.c` at `v1.1.3` and to `lavd-ossna24` slides 22 and 25.
- `docs/references.md` `scx`: its role extended to scx_lavd's documented design (the README and `lat_cri.bpf.c` at the release, with SHA-256 from S2-09).
- The guidebook: vol-02 `:3572` ("이 칸의 가장 발전한 형태", the same superlative) restated without it; `:1331` and `:3863` checked against the inputs above.

Compiled effect: none.

## D11 — every LAVD source is footnote tier; the source naming and the production clause of `grounding-sources.md:30` restated (2026-10-08)
> Amended by D100 (`lavd-ossna24`'s pairing clause leaves with `corbet-lwn24`'s "prose-citable").
> Amended by D113 (`lavd-ossna24` and `corbet-lwn24` are the new talk, abstract or news-report type; by 인지오's decision).

By 인지오's decision, scope-card item 58 (with item 61's read lines): LAVD has no scholarly citation — no peer-reviewed paper or archived preprint describes it (S1 "Not found", T2: arXiv 0 results, OpenAlex none; stage 3) — so every LAVD source sits in the deployed-system / footnote tier, and the paper keeps its two tiers.

- **The sources and what each carries:** `lavd-ossna24` — Changwoo Min's OSS NA 2024 talk slides (Seattle, 2024-04-17; S2-10), the numbers and the task-chain characterization; scx_lavd's source and README at scx `v1.1.3` (`scx`, D10), the mechanism and origin; `corbet-lwn24` — LWN 991205 (Jonathan Corbet, 2024-09-26), its report of the LPC 2024 talks, qualitative only (its "typically no more than 100µs at a time" differs from slide 13); LWN 1051430 (Jake Edge, 2026-01-07; S2-13), its report of the LPC 2025 talks; the SteamOS sources of D9; the LPC slides and abstracts of D8. LWN articles carry only what they report, attributed as reports.
- **`grounding-sources.md:74`** (C-lavd-20 / C-corbet-1, CONTRADICTED): "LAVD/LWN-covered work" leaves the scholarly list.
- **`grounding-sources.md:30`, the source column** (C-lavd-20, MISATTRIBUTED): "LAVD design notes (LKML, LPC talks)" restated to the OSS NA 2024 slides, scx_lavd's source and README at `v1.1.3`, and LWN's reports of the LPC 2024 and 2025 talks.
- **`grounding-sources.md:30`, the production clause** (C-lavd-18 (a), (b), MISATTRIBUTED): "Valve ships it; Meta adopted the scheduler server-side" restated per D9 (Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default) and D8 (Meta presented it as a candidate default fleet scheduler).

Hands to 9.15:

- `docs/workload/grounding-sources.md:30`, `:74` restated as above.
- `docs/references.md`: an entry for LWN 1051430 (Jake Edge, "Lessons from creating a gaming-oriented scheduler", 2026-01-07; copy and SHA-256 from S2-13), footnote tier; `corbet-lwn24` names 991205 only, its role "prose-citable secondary" restated to an attributed report, qualitative only, and its "Later option to evaluate" line replaced by the new entry; `lavd-ossna24` unchanged (footnote tier).
- The 2026-09-13 verdicts on the same sources already handed through item 61 — `docs/workload/coreset-guide.md:64`, `:184` ("LAVD 논문", WORDING-FIX: talk slides, not a paper) — applied with these.

Compiled effect: none.

## D12 — the priority claim scoped and dated: no prior work measures an LLM recognizing a desktop situation from process identity against labels, to the literature searched through 2026-10-08 (2026-10-08)

By 인지오's decision, scope-card item 19 (and the substance of item 15's third clause): `docs/related-work.md:48`'s "evaluated, for the first time in this line, at the recognition layer itself" is replaced by a scoped, dated statement, with the three nearest measurements named and their figures given.

- **The statement:** to our knowledge — the literature searched through 2026-10-08 (S1 search log, stage 2 and the stage-3 refresh, eight arXiv queries; S1 "Not found", T5) — no prior work measures an LLM's accuracy at recognizing a desktop situation from process identity against ground-truth labels.
- **The nearest measurements:**
  - ASA (arXiv 2511.11628v1, 2025-11-07; S1-11, p. 9): "the base workload classifier achieves a notable accuracy of 96.83%", 99.19 % after online fine-tuning; an XGBoost-led ensemble, not an LLM, over behavioural OS metrics (Table 1) — no process identity among its features.
  - SchedCP (arXiv 2509.01245v4, NeurIPS 2025 Workshop on ML for Systems; S1-12, v4 p. 5): "Claude Opus successfully classified all 8 workloads at $0.15 per analysis, while Claude Sonnet failed" — an outcome reported beside its four research questions, none of which is on recognition; its agent starts "from process name and commands" and then profiles.
  - AKTS (arXiv 2609.12276v2, 2026-10-07; S1-19, S1-32, §4.2): Qwen2.5 at 0.5B, 1.5B and 3B route high- and low-load telemetry to a policy index at "20/40 correct, i.e. chance; n=40 per model"; 16 of 48 of the 0.5B model's decisions were not a valid index.
- **`:34`'s "prior LLM-scheduling work measures end-to-end performance only"** is restated to the same three: SchedCP reports a classification outcome, AKTS measures recognition on telemetry. Item 15's other two clauses are its own.

Hands to 9.15:

- `docs/related-work.md:48`, `:34` restated as above; `:36`'s note ("which SchedCP's evaluation has no analogue of") brought in line.
- `docs/references.md`: an entry for AKTS, arXiv 2609.12276v2 (2026-10-07), scholarly tier as an archived preprint, with S1-32's copy and SHA-256; `asa-arxiv25`'s role line — its "'measuring recognition itself has no analogue in prior work' … false of this one" — kept, with the scoped statement beside it; `schedcp-mlsys25` — the 8-of-8 outcome at v4 p. 5.
- The search log dates the statement: any re-run before submission extends it.
- The guidebook: vol-02 `:2088` ("인식 자체를 따로 재는 평가는 그쪽에 대응물이 없다", said of the LLM line) restated — AKTS measures LLM recognition on telemetry and SchedCP reports an 8-of-8 outcome; `:2092`, `:2180`, `:2465` already agree with D12 and stay.

Compiled effect: none.

## D13 — the "Cooperation" limit restated: who declares, how many do, in which direction, and which background tools (2026-10-08)
> Amended by D49 (a vendor-documented case of priority inflation: Apple's XNU scheduler document, on the traditional Mach model).
> Amended by D64 (on the depicted Ubuntu 24.04 desktop updatedb is not installed and the installable plocate declares only the idle I/O class; the count shows direction, mostly daemons raising).

By 인지오's decision, scope-card item 26 (with 9.6 D17's and 9.11 D33's hand-offs), after a stage-3 recount (S3-20): `docs/research-proposal.md:158`'s "Linux scheduling classes and macOS QoS require the application to declare its own nature. Most applications never do. Those that do tend to claim they are the most important thing on the system. `updatedb` does not volunteer that it is background work." is restated to the sources.

- **Who declares.** On Linux a program's policy, nice value and I/O class are set by the program itself (LocalSearch's `tracker-main.c`, Baloo's `priority.cpp`; S3-02), by its installed unit (plocate's, findutils'; S3-02), or by a wrapper (Déjà Dup's `chrt --idle 0 ionice -c3`; 9.11 S2-27); on macOS the developer declares a QoS class in code (S2-21).
- **How many, in units** (S3-20, Debian unstable `main`, 2026-10-08): of 1 438 source packages that install a systemd service unit, 56 (3.9 %) carry `Nice=`, `IOSchedulingClass=` or `CPUSchedulingPolicy=` in an installed unit — a floor, since a class set in code or by a wrapper is not counted.
- **In which direction.** 40 of the 56 only lower their priority, 16 only raise it, none both; of the 49 `Nice=` values in installed units, 33 lower priority (25 at nice 19) and 16 raise it (S3-20). "Those that do tend to claim they are the most important thing on the system" leaves: contradicted by the count, and no documented case of over-claiming was found (S2-29).
- **Which background tools.** `updatedb` declares itself background work: plocate's unit sets `Nice=19` and `IOSchedulingClass=idle`, findutils' `locate.service` the same with `IOSchedulingPriority=7` (S3-02). LocalSearch (Tracker) and Baloo set background classes on themselves; Déjà Dup wraps its scheduled backup in `chrt --idle 0`; ClamAV's units, borg and restic declare nothing; borgmatic's sample unit runs `SCHED_BATCH` at nice 19 (9.11 D4, D33; S2-22 to S2-27 of 9.11). On Ubuntu 24.04 Tracker's own unit also places it in `background.slice`, weighted 30 against `app.slice`'s 100, while Déjà Dup's backup runs in `app.slice` beside the editor (9.11 D16).
- **The limit the bullet can claim** rests on these facts: declaration is partial — present for some background tools and absent for others — and fixed per program by its author or packager.
- **S3-01's denominator** (1 593) counted the grouped search view's headers, not packages (S3-20); its percentages are not used.

Hands to 9.15:

- `docs/research-proposal.md:158` and `docs/background-guide.md:18` ("they rarely do, and when they do declare something, everyone claims to be important") restated as above.
- `docs/references.md`: the Debian count's sources — Debian unstable's `Contents` and `Packages` indexes of 2026-10-08 and Debian Code Search — entered under the id-minting rule, with S3-20's hashes; plocate's and findutils' units (S3-02) where the prose names them.
- The guidebook lines saying the same: vol-01 `:2097` ("대부분의 프로그램이 선언하지 않습니다"), `:2099` ("성능에 민감한 프로그램들이 필요 이상으로 높은 priority를 요구하는 경향", no source), `:2143`, `:3338`, `:3364`; vol-03 `:107`, `:109` ("파일 색인을 만드는 프로그램이 자진해서 … 말하는 일은 잘 없습니다", contradicted by S3-02 and 9.11 S2-22), `:314`.

Compiled effect: none.

## D14 — the load-bearing pair restated: two real jobs beside an editor, with opposite correct policies, differing in behaviour and in declared class (2026-10-08)
> Amended by D88 (the premise's other lines: research-proposal.md:129, :617, research-claims.md:23, :214–216, background-guide.md:115; the past-10 ms shares read from the pair the dataset carries).

By 인지오's decision, scope-card items 6 and 47 (with 9.6 D17, D21, D32 and 9.10 D6, D12's hand-offs): `docs/related-work.md:18`'s "an ML training run versus a file indexer, both manifesting as one CPU-saturating process beside an editor — is constructed so that the two situations are behaviorally indistinguishable in principle, yet demand opposite policies. No refinement of this quadrant can separate them; the distinguishing information exists only in what the processes *are*, not in what they *do*", and `docs/research-proposal.md:627`'s "no behavioural heuristic can separate them even in principle", are restated to 9.10 D6: two real jobs beside an editor with opposite correct policies.

- **The two jobs, as the dataset carries them:**
  - The training side (`c2-p1a`): PyTorch's basic MNIST example on the CPU, an actual training run that does not claim desktop users train MNIST (9.6 D32, 9.10 D12, D82–D90; `dataset/archetypes.yaml` `cpu-batch` scope). One thread, saturation 0.99988–0.99991; the run between voluntary blocks 69.49 s ±27.3 %; CPU total 1 389.885 s ±4.04 % (9.10 D90). Default policy, nice 0 (9.6 D17).
  - The indexer side (`c2-p1b`): GNOME's Tracker indexing a home folder (9.10 D81). Five processes, saturation 0.655–0.676 over the job; the run between voluntary blocks 1.876 ms ±1.12 %, the block per run 227.0 µs ±3.58 %; CPU total 39.435 s ±0.28 % (9.10 D81). `SCHED_IDLE`, nice 19, idle I/O class, set by the program on itself (9.6 D17; 9.11 S2-22).
  - The share of each program's CPU past a 10 ms slice without a voluntary block: Tracker 0.530–0.536, `python3` 0.917–0.920 (9.6 D21).
- **What the pair tests** (9.10 D6; 9.11 D4): whether recognition improves on a baseline that already honours the indexer's declared class — "a baseline may deprioritize the indexer without recognition; the RQ0 gate then measures that headroom as it is."
- **Leave:** "behaviorally indistinguishable in principle", "No refinement of this quadrant can separate them", "the distinguishing information exists only in what the processes *are*, not in what they *do*" (`related-work.md:18`); "no behavioural heuristic can separate them even in principle" (`research-proposal.md:627`); `related-work.md:20`'s "which the F2 pair defeats by construction".

Hands to 9.15:

- `docs/related-work.md:18`, `:20`; `docs/research-proposal.md:624`, `:627` restated as above; "ML training run" worded per 9.6 D32 and 9.10 D12.
- The same premise for P1 elsewhere: the guidebook vol-03 `:1565`, `:1635`, `:3701`; vol-04 `:1084`, `:1100`, `:1275`; vol-05 `:90`, `:112`, `:2171`, `:2364`; vol-06 `:115`, `:200`, `:1495–1499`; vol-02 `:1453`, `:2177`, `:3574` (the behaviour channel's limit stated through the pair); `docs/workload/coreset-guide.md:182`, `:436`. 9.10 D6 already handed `building-plan.md` §3 C2 (`:91`) and `archetype-plan.md:77`'s rationale.
- The general "same behaviour, opposite treatment" passages that illustrate with a download against a scan or a training run against a scan — vol-01 `:448`, `:1314`, `:1350`, `:1396`, `:2561`, `:3751`, and `docs/research-proposal.md:131`, `:175` — are read with item 33 (the download and the virus scan, against 9.6's and 9.7's measured values).

Compiled effect: none.

## D15 — the download-against-scan premise restated to the dataset's pair: the game download against the stock unattended upgrade, two real jobs differing in run shape, structure, size and declared priority (2026-10-08)
> Amended by D89 (research-proposal.md:133).
> Amended by D101 (locator: `:179`, not `:178`).

By 인지오's decision, scope-card item 33 (with 9.10 D3's replacement of the scan, and the general passages D14 routed here): `docs/research-proposal.md:131`'s "a game download the user is impatiently waiting for, and a virus scan the user did not ask for, are behaviourally identical. Both are sustained background bulk work hammering the disk. … No CPU utilization graph will ever separate them", the §2.3 table's row and sentence (`:175`, `:178`: "same process count, same behavioural signature, opposite correct policy") and `docs/background-guide.md:12–16` ("these two machines look **identical** … Every measurement the OS can take … comes out the same") are restated to the pair the dataset carries, `c2-p2a` against `c2-p2b`.

- **The unwanted job** is Ubuntu 24.04's stock unattended upgrade, not a virus scan (9.10 D3): ClamAV's documentation states "ClamAV is not a traditional anti-virus or endpoint security suite" and no ClamAV package examined ships a scheduled scan; a scheduled desktop `clamscan` runs only through ClamTk, which "is no longer maintained", in regular use on 0.11 % of Debian popcon submissions; `unattended-upgrades` is in the stock desktop's default layer, enabled by default, run daily (9.10 S2-01, S2-03, S2-30, S3-30).
- **The two jobs, as measured:**
  - `game-download` (`dataset/archetypes.yaml`, `meas-ci:background:2026-09-19`, 9.7 D28–D29): CPU over the job 0.907–0.958, 697–761 s in 760–822 s; one process of 83–84 threads; the run between voluntary blocks 162.7 µs ±2.21 %; network wait 220.6 µs ±4.18 %. Nice 10 does 75.33 % of its CPU over the 30 pooled repeats (9.11, the `game-download` pool; D6).
  - `package-upgrade` (`meas-ci:background:2026-10-01`, 9.10 D17, D39): CPU over the stage 0.990–0.994; 916 short-lived processes, locale-gen's 18 `localedef` runs 72.8–76.5 % of the CPU; the run between voluntary blocks 1.798 ms ±3.10 %; CPU total 26.385 s ±3.78 %. Nice 19 does 2.67 % of its CPU (9.11).
- **What holds:** both keep a CPU 91–99 % busy beside the game. **What leaves:** "behaviourally identical", "same behavioural signature", "No CPU utilization graph will ever separate them", "Every measurement the OS can take … comes out the same" — the jobs differ in how their work is cut (163 µs against 1.8 ms between blocks), in structure (one 84-thread process against 916 processes), in size (about 700 s of CPU against 26 s) and in declared priority (the wanted download at nice 10 for three quarters of its CPU).
- **The pair's claim**, as D14 states P1's: two real jobs beside a game with opposite correct policies — the wanted download throttled and never starved, the unwanted upgrade deferred — testing what recognition adds over a behavioural and declared-priority baseline.

Hands to 9.15:

- `docs/research-proposal.md:131`, `:175`, `:178`, `:622` ("Game + antivirus full scan"), `:185`'s "that a scheduled antivirus scan is not" (its Steam clause is item 34's); `docs/background-guide.md:12–16`; `docs/research-claims.md:222` ("download versus antivirus scan"); `docs/data-contracts.md:92` ("a virus scan in full swing") — restated as above.
- The guidebook: the general passages D14 routed here, vol-01 `:448`, `:1314`, `:1348–1352`, `:1396`, `:2561`, `:3422`, `:3751`; vol-03 `:74`, `:142`, `:150`, `:168`, `:180–183`, `:266`, `:1484`; vol-04 `:1398`; vol-05 `:941`, `:1011–1014`, `:1056`, `:1075–1077`, `:1194–1198`, `:1259`, `:1300`, `:1386`, `:1402`, `:1449`, `:1636–1643`, `:2638`.
- 9.10 D3 already handed the workload docs (the scenario catalog's S17 row, `docs/recognition-vocabulary.md`'s examples, `building-plan.md` §3 C2 and C7, and with them `docs/workload/coreset-guide.md:650–663`, `:915–929`, `:957–959`).

Compiled effect: none.

## D16 — "a Steam download is something the user initiated" narrowed to the depicted install; Steam's own updates queue themselves and pause at game launch (2026-10-08)

By 인지오's decision, scope-card item 34 (with 9.10 D7 and D170): the proposal's general claim that a Steam download is user-initiated is narrowed to the download the dataset depicts — an install of another game the user starts during play, which Steam runs at once.

- **What Valve states** (`steam-downloads`; 2026-09-13 read R07, C-steam-2, C-steam-3): "Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself. You can turn this feature off by navigating to your download settings: Steam > Settings > Downloads. From here, check the Allow Downloads During Gameplay box." (FAQ 4F9E-6328-E9B8-47F9); "Games are automatically put into your download queue when a game releases an update", and "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing." (FAQ 71AB-698D-57EB-178C). A Steam download is in general not user-initiated: updates queue themselves, and by default queued downloads pause while a game runs.
- **What the dataset depicts** (9.10 D7): the user starts installing another game while playing; "if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately" (steam-for-linux #8821, one user's repeated observation on SteamOS 3.4), with Valve's issue triager: "this is not specific to SteamOS or the Steam Deck" (9.10 S3-27). That download is user-initiated (`initiated: user`).
- **What recognition faces:** the name `steam` downloading is an install the user started or an update nobody started; the name alone does not settle which.

Hands to 9.15:

- `docs/research-proposal.md:185` ("that a Steam download is something the user initiated and is waiting on") restated to the install the user just started, beside an update nobody started; `:174`, `:621` ("Steam download", "transfer the user wants") named as that install; `:311–313`'s sample model output ("The Steam process is downloading, which the user started deliberately") restated to the same install.
- `docs/references.md`: `steam-downloads`' role line without "the wanted/unwanted toggle" (9.10 D170) and with the automatic update queue (FAQ 71AB); an entry for steam-for-linux #8821 (9.10 D7's hand-off).
- The guidebook: vol-01 `:1397`, `:2527`; vol-02 `:3116`; vol-03 `:141`, `:154`, `:171`, `:193`, `:265`, `:316`, `:500`, `:640`, `:1164`; vol-04 `:376`.

Compiled effect: none.

## D17 — related-work's ghOSt sentence: "without kernel rebuilds" becomes "without deploying a new kernel or rebooting" (2026-10-08)

By 인지오's decision, scope-card item 1: `docs/related-work.md:8`'s "ghOSt delegates kernel scheduling decisions to userspace agents, motivated by the need to iterate on policy across a fleet without kernel rebuilds [ghost-sosp21]" keeps its mechanism and motivation; "without kernel rebuilds" becomes "without deploying a new kernel or rebooting".

- **Grounds** (`ghost-sosp21`; S1-01, the SOSP '21 PDF, SHA-256 `c37d6360…`): Abstract — "kernel schedulers are difficult to implement, test, and deploy efficiently across a large fleet"; policies "are modified without a host reboot". §2, p. 3 — "Deploying changes to scheduling policy requires deploying a new kernel across a large fleet … kernel rollouts are not well-tolerated below an O(month) granularity"; "ghOSt enables scheduler update, testing, and tuning without having to update the kernel and/or reboot machines and applications." The mechanism: a kernel scheduling class with user-space agents, falling back to CFS when agents crash (§3, p. 5; §3.4, p. 8).

Hands to 9.15: `docs/related-work.md:8` as above; the guidebook vol-02 ch. 3.2 checked against the same passages (item 60).

Compiled effect: none.

## D18 — the classic heuristics: MLFQ classifies by CPU use; CFS and EEVDF account against a fair share, their sleeper handling shaping a waking task's place (2026-10-08)
> Amended by D101 (locator: `related-work.md:16`'s second sentence).

By 인지오's decision, scope-card item 4 (and the `mlfq` and `eevdf` keys of item 20): `docs/related-work.md:16`'s "Classic interactivity heuristics — MLFQ's demotion by CPU consumption, and the sleep/wake accounting behind CFS and EEVDF — classify tasks by how they use the CPU [mlfq, eevdf]" keeps MLFQ as a classifier and restates CFS and EEVDF as accounting.

- **MLFQ** (`ostep`, ch. 8, Version 1.10; S1-02): "If, for example, a job repeatedly relinquishes the CPU while waiting for input from the keyboard, MLFQ will keep its priority high … If, instead, a job uses the CPU intensively for long periods of time, MLFQ will reduce its priority" (p. 2); Rules 4a/4b (p. 3), revised to Rule 4: "Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced" (p. 8). The original (`corbato-sjcc62`; S1-04, printed p. 341–342): a program not done within 2^ℓ quanta moves to level ℓ+1, and "the level classification procedure for programs is entirely automatic, depending on performance and program size rather than on the declarations (or hopes) of each user".
- **CFS** (`Documentation/scheduler/sched-design-CFS.rst` at mainline `7b63ef2d`; S2-04): "CFS basically models an "ideal, precise multi-tasking CPU" on real hardware" (`:18–19`); "has no heuristics whatsoever" (`:96–105`), beside "various algorithm variants to recognize sleepers" (`:51–53`) in the same document.
- **EEVDF** (`sched-eevdf.rst` at `7b63ef2d`, S2-03; `eevdf-tr95`, S1-05): a virtual run time and a lag per task, the eligible task with the earliest virtual deadline run next, "latency-sensitive tasks with shorter time slices" favoured (`:13–22`); a sleeping task's lag decays (`:24–32`). The report bounds the lag by a quantum (Corollary 2, p. 20) and leaves the compensation of a rejoining client a policy choice (§5, p. 11–12).
- **The key map:** `mlfq` → `ostep` with `corbato-sjcc62`; `eevdf` → `eevdf-tr95` with the kernel's `sched-eevdf.rst` and `sched-design-CFS.rst`.

Hands to 9.15: `docs/related-work.md:16`'s first sentence restated as above, its keys resolved; the guidebook vol-02 ch. 2.2 and 2.5 checked against the same passages (item 60).

Compiled effect: none.

## D19 — the learned-scheduler sentence: Decima and FIRM kept; Park restated as an open platform of twelve environments (2026-10-08)
> Amended by D101 (locator: `related-work.md:24`'s second sentence).

By 인지오's decision, scope-card item 8 (and the `decima`, `firm`, `park` keys of item 20): `docs/related-work.md:24`'s "Decima learns cluster scheduling policies via RL over job DAGs [decima]; Firm learns SLO-driven resource management for microservices [firm]; Park generalizes the setting [park]" keeps its first two clauses; "Park generalizes the setting" becomes "Park offers an open platform of twelve system-optimization environments for learning-augmented systems".

- **Decima** (`decima-sigcomm19`; S1-06): "Decima encodes its scheduling policy in a neural network trained via a large number of simulated experiments" (p. 1); its graph embedding "takes as input the job DAGs whose nodes carry a set of stage attributes" (§5.1, p. 4).
- **FIRM** (`firm-osdi20`; S1-07): an RL agent (DDPG, p. 9) sets per-microservice resource limits for CPU, memory, LLC, I/O and network (Table 3, p. 10), beside an SVM that localizes SLO violations (p. 3); the title names "SLO-Oriented Microservices".
- **Park** (`park-neurips19`; S1-08): "Park: An Open Platform for Learning-Augmented Computer Systems"; "Currently, Park consists of 12 real world system-centric optimization problems with one common easy to use interface" (Abstract), 7 backed by real systems and 5 by simulators (p. 2).

Hands to 9.15: `docs/related-work.md:24`'s first sentence as above, its keys resolved; the guidebook vol-02 ch. 5.2–5.4 checked against the same passages (item 60).

Compiled effect: none.

## D20 — the learned line's limits grounded in the learned papers' own statements, SchedCP as the LLM line's summary of them (2026-10-08)

By 인지오's decision, scope-card item 9: `docs/related-work.md:24`'s "limits are by now well documented — including by later work in the LLM lineage: they require extensive per-workload retraining, and they operate inside a problem space a human has already formalized (features, knobs, objectives) [schedcp]" keeps both limits; "by now well documented" becomes "stated by the learned papers themselves and summarized by later LLM work", and each limit cites its primary.

- **Per-workload training:**
  - Decima (`decima-sigcomm19`; S1-06, §7.4, p. 11): "As Decima learns workload-specific policies, we expect its effectiveness to depend on whether broad test workload characteristics, such as interarrival time and job size distributions, match the training workload"; trained with an "anti-skewed" workload, "it generalizes poorly and underperforms the optimized weighted fair policy".
  - FIRM (`firm-osdi20`; S1-07, p. 3, p. 10, p. 13): "To enable rapid (re)training of the proposed system as the underlying systems and workloads change in datacenter environments, FIRM uses transfer learning"; about 2 000 iterations with it against about 15 000 for the one-for-all agent.
  - Park (`park-neurips19`; S1-08, §3.3, p. 5): "discrepancies between simulation and reality prevent direct generalization"; training from simulation's method "would take a single-threaded agent more than 10 years to complete training in reality".
- **A human-formalized problem space:** each paper's own state and action design — Decima's stage attributes and scheduling actions (§4, §5.1), FIRM's state and action space (Table 3, p. 10).
- **The summary** (`schedcp-mlsys25`, v4 §2, p. 2; S1-12): "Prior RL-based schedulers [10, 17, 19, 11] require extensive training per workload type, lack semantic understanding to transfer across workloads, and only tweak configurations after engineers have already defined the entire problem space: selecting features, specifying knobs, and writing objective functions" — [10] Decima, [17] FIRM, [19] Zhang et al. TPDS 2024, [11] Park.

Hands to 9.15: `docs/related-work.md:24` restated as above; the guidebook vol-02 ch. 5 checked against the same passages (item 60).

Compiled effect: none.

## D21 — the ASA sentences: a recognizer trained once over behavioural metrics, a per-machine measurement pass for the mapping table; "training per deployment context" leaves (2026-10-08)

By 인지오's decision, scope-card items 10 and 11: `docs/related-work.md:24`'s "ASA recognizes workload patterns online — via time-weighted voting over behavioral signals — and routes to expert scheduling policies atop sched_ext [asa]" and `:26`'s "ASA's recognizer, like the RL line, reads behavioral features and requires offline training per deployment context; ours reads process identity against world knowledge that requires no training on the target machine" are restated to the paper (`asa-arxiv25`; S1-11, arXiv 2511.11628v1).

- **What ASA does** (Abstract, p. 1): "an offline process trains a universal, hardware-agnostic machine learning model to recognize abstract workload patterns from system behaviors. Second, at runtime, ASA continually processes the model's predictions using a time-weighted probability voting algorithm to identify the workload, then makes a scheduling decision by consulting a pre-configured, machine-specific mapping table to switch to the optimal scheduler via Linux's sched_ext framework." The classifier is an XGBoost-led ensemble (§3.3, p. 4).
- **What it reads** (Table 1, p. 4): CPU, memory, disk, process, scheduling and network metrics, among them the window-focused process's CPU and memory and input events; no process identity.
- **What each new machine needs** (§4.4, p. 7): "By exclusively running the "Generalization Model Training" (Stage 3) on the target machine, ASA can interact directly with the new environment and its available schedulers, resulting in the creation of a precise, hardware-specific scheduler mapping table ready for immediate use. The entire process can then be followed by an optional, low-overhead fine-tuning process" — a measurement pass, not a retraining of the recognizer.
- **Restated:** item 10 — ASA classifies the workload from OS metrics with a model trained once offline, smooths its predictions by time-weighted voting, and switches among expert sched_ext schedulers through a per-machine mapping table. Item 11 — its recognizer reads behavioural metrics with no process identity; each new machine needs a measurement pass that builds the mapping table, with optional fine-tuning; "requires offline training per deployment context" leaves. "Ours … requires no training on the target machine" stays, scoped to the recognizer.

Hands to 9.15: `docs/related-work.md:24`'s last sentence and `:26` restated as above; the guidebook vol-02 ch. 5.6 (`:2110`, `:2148`, `:2177–2180` already agree) checked against the same passages (item 60).

Compiled effect: none.

## D22 — Kgent's sentence kept; `kgent-ebpf24` read in full from its open-access copy (2026-10-08)

By 인지오's decision, scope-card items 12 and 54: `docs/related-work.md:32`'s "Kgent synthesizes kernel extensions from natural language [kgent]" stands; the registry's open point closes.

- **Grounds** (S1-33; the eBPF '24 paper, DOI 10.1145/3672197.3673434, read from UC Santa Cruz's eScholarship copy, https://escholarship.org/content/qt3jg1f0jr/qt3jg1f0jr.pdf, CC BY 4.0, SHA-256 `1292f750…`): "This paper presents Kgent, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language. Kgent uses recent advances in large language models (LLMs) to synthesize an eBPF program given a user's English language prompt." (Abstract, p. 1).

Hands to 9.15: `docs/references.md` `kgent-ebpf24` — status: the paper read 2026-10-08 from the open-access eScholarship copy, with its URL and SHA-256; "DOI record not re-checked (ACM DL unreachable)" leaves. The guidebook vol-02 ch. 6.3 checked against the same passages (item 60).

Compiled effect: none.

## D23 — SchedCP's description kept to v4; "a given server or batch workload" names its evaluation and its personal-device motivation (2026-10-08)

By 인지오's decision, scope-card items 13 and 15 (its first two clauses; the third is D12's): `docs/related-work.md:32`'s description of SchedCP stands, cited to v4's locators; `:34`'s "SchedCP optimizes a given server or batch workload" becomes "SchedCP optimizes a given workload (its evaluation runs kernel compilation, schbench and batch workloads), though it names edge and personal devices among its motivations"; "through an agentic session with sandboxed profiling (reading source, running perf)" stands.

- **Item 13** (`schedcp-mlsys25`, v4; S1-12, S1-34): "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs" (Abstract); "1. Workload Analysis Engine Provides tiered access to system performance data … (2) secure sandbox access to file reading, application building, Linux profiling tools (perf, top) and dynamically attachable eBPF probes" (§3, p. 3); the Observation, Planning, Execution and Learning Agents, the Planning Agent "configuring existing schedulers, generating patches, or composing new schedulers from primitives" (§4, p. 4); "reaching 1.79× total improvement over EEVDF" for kernel compilation (§5, p. 4).
- **Item 15** (v4; S1-34): §2, p. 2 — "edge/personal device users lack both kernel optimization expertise and understanding of application-specific targets"; §5, p. 4 — "Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13"; its workloads kernel compilation, schbench and batch workloads (S1-12).

Hands to 9.15: `docs/related-work.md:32` cited to v4 as above, `:34` restated; the guidebook vol-02 ch. 6.2 checked against the same passages (item 60).

Compiled effect: none.

## D24 — the adjacent LLM efforts: TuneAgent tunes the kernel's build configuration, cited as KDD '26 by its DOI; Jadhav et al. kept as a preprint (2026-10-08)

By 인지오's decision, scope-card items 14, 50 and 51 (and the `tuneagent`, `hpc-llm` keys of item 20): `docs/related-work.md:32`'s "Adjacent efforts tune kernel parameters [tuneagent] and schedule HPC jobs [hpc-llm] with LLMs in the loop" becomes "Adjacent efforts tune the kernel's build configuration [tuneagent] and schedule HPC jobs [hpc-llm] with LLMs in the loop".

- **TuneAgent** (S1-14, S1-35): v1, "OS-R1", abstracts "the kernel configuration space as an RL environment"; v2, "TuneAgent formulates the kernel space as a constrained RL environment, enabling large language models (LLMs) to autonomously explore the kernel while enforcing valid and precise configuration modifications"; Qwen2.5 3B and 7B, evaluated on UnixBench. Venue: Crossref resolves DOI 10.1145/3770855.3817987 to *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2*, published 2026-08-08 (KDD '26), authors Lin, Li, Luo, Lin, Zhang, Xing, Wu.
- **Jadhav et al.** (`jadhav-arxiv25`; S1-15, S1-35): a ReAct-style LLM scheduler for HPC job queues, o4-mini and Claude 3.7 on "seven real-world HPC workload scenarios"; arXiv 2506.02025 v2 (2025-09-03), "work under review", no later version.
- **The alternate candidate leaves** `jadhav-arxiv25`'s role line: arXiv 2511.11612 (Sharma & Kunkel; S1-16) is a one-shot task-to-node mapping over 21 models, journal-ref *Robot Autom Eng J.*

Hands to 9.15:

- `docs/related-work.md:32` as above, its keys resolved.
- `docs/references.md`: `tuneagent-arxiv25` re-minted under the id-minting rule as a scholarly entry for the KDD '26 paper — `tuneagent-kdd26` — cited by its DOI, the arXiv versions named (v1 "OS-R1", v2 "TuneAgent"), status verified (S1-35's Crossref record), "to-pin" retired; `jadhav-arxiv25` — status re-checked 2026-10-08 (still v2, under review), the "(Alternate candidate …)" sentence removed.
- The guidebook vol-02 ch. 6.4 checked against the same passages (item 60).

Compiled effect: none.

## D25 — the reference-placeholder table becomes the final key-to-registry map (2026-10-08)
> Amended by D99 (the `gamemode` row: five Learn pages and the Xbox Support entry).

By 인지오's decision, scope-card item 20 (with entries 52 and 53): `docs/related-work.md:56–73`'s table maps each citation key to its registry entries and their settled form; the "verify" column leaves, every open point being closed by D1–D24 and the checks below.

| Key | Registry entries and form | Decision |
|---|---|---|
| `ghost` | `ghost-sosp21`, SOSP '21 | D17 |
| `schedext` | `schedext-docs`; first released in Linux 6.12 (the kernel tree, S2-47) | D7 |
| `scx` | `scx` at release `v1.1.3`, commit `c8728c6b` | D8, D10 |
| `lavd` | `lavd-ossna24` (OSS NA 2024 slides), scx_lavd's README and `lat_cri.bpf.c` at `v1.1.3` (`scx`), `corbet-lwn24` (LWN 991205) and the LWN 1051430 entry — all footnote tier; "LKML + LPC talks" leaves (C-lavd-20, MISATTRIBUTED) | D10, D11 |
| `mlfq` | `ostep` ch. 8, Version 1.10, with `corbato-sjcc62` | D18 |
| `eevdf` | `eevdf-tr95` (1995; "Revised January 26, 1996" is the revision, not the year) with the kernel's `sched-eevdf.rst` and `sched-design-CFS.rst` | D18 |
| `decima`, `firm`, `park` | `decima-sigcomm19`, `firm-osdi20`, `park-neurips19` | D19, D20 |
| `asa` | `asa-arxiv25`: arXiv 2511.11628v1 (2025-11-07), no venue — re-checked 2026-10-08, still v1, no journal reference | D21 |
| `schedcp` | `schedcp-mlsys25`: arXiv 2509.01245v4; venue as the NeurIPS virtual site lists it, NeurIPS 2025 Workshop on ML for Systems (S1-12; C-schedcp-4 WORDING-FIX of "MLforSystems '25"); no successor by its authors in the searches through 2026-10-08 (S1 search log) | D12, D23 |
| `kgent` | `kgent-ebpf24`, eBPF '24, DOI 10.1145/3672197.3673434, the open-access eScholarship copy | D22 |
| `tuneagent` | `tuneagent-kdd26`, KDD '26, DOI 10.1145/3770855.3817987 | D24 |
| `hpc-llm` | `jadhav-arxiv25`, arXiv 2506.02025v2, under review | D24 |
| `gamemode` | `gamemode-docs` (Microsoft Learn, four pages) and Apple's two Game Mode entries | D1, D2 |
| `ananicy` | `ananicy` (ananicy-cpp, 1.2.0 as CachyOS ships it), `ananicy-rules` at `03ef03fb` = tag 1.1.49, and the CachyOS default-install entry | D3 |

New keys from D1–D24, added to the table: AKTS (D12), SteamOS's LAVD support (D9), the LPC 2024 slides "sched_ext status and plans" and the LPC 2025 abstract on the Reality Labs fleet (D8), Feral GameMode (D4), LWN 1051430 (D11).

Hands to 9.15: `docs/related-work.md:54–73` rewritten as the map above; the registry entries it names minted or restated as the listed decisions hand them.

Compiled effect: none.

## D26 — the proposal's Linux scheduling-class statements: who declares and through which call; EEVDF a proportional-share algorithm (2026-10-08)

By 인지오's decision, scope-card items 22 and 39: `docs/research-proposal.md:145`'s row "Scheduling classes (`SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`, `SCHED_BATCH`, `SCHED_IDLE`) — Application or admin declares it via `sched_setscheduler`" and `:424`'s "`SCHED_DEADLINE` is EDF, `SCHED_FIFO` is fixed-priority real-time, `SCHED_OTHER` is EEVDF, a deterministic relative of proportional-share scheduling" are restated to the kernel's documents and man-pages 6.19.

- **The policies** (sched(7), sched_setattr(2); S2-07, S2-51): `SCHED_OTHER` (the default), `SCHED_BATCH`, `SCHED_IDLE`, `SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`; and `SCHED_EXT` since Linux 6.12 (S2-47).
- **Who declares and how**: the program itself, its systemd unit (`CPUSchedulingPolicy=`, `Nice=`) or a wrapper (`chrt`) (D13; S3-02, S3-20); through `sched_setscheduler(2)`, or for `SCHED_DEADLINE` "one must use the Linux-specific sched_setattr(2) and sched_getattr(2) system calls" (sched(7)). Unprivileged threads may lower priority or switch to a non-real-time policy; real-time priority is capped by `RLIMIT_RTPRIO`; "A thread must be privileged (CAP_SYS_NICE) in order to set or modify a SCHED_DEADLINE policy" (sched(7)).
- **`SCHED_DEADLINE`**: "basically an implementation of the Earliest Deadline First (EDF) scheduling algorithm, augmented with a mechanism (called Constant Bandwidth Server, CBS)" (`sched-deadline.rst:41–44`, S2-05); "implemented using GEDF (Global Earliest Deadline First) in conjunction with CBS" (sched(7)).
- **`SCHED_FIFO`**: static priorities above 0; it "will always immediately preempt any currently running SCHED_OTHER, SCHED_BATCH, or SCHED_IDLE thread"; "a simple scheduling algorithm without time slicing" (sched(7)).
- **`SCHED_OTHER`**: EEVDF since Linux 6.6 (`sched-eevdf.rst:5–11`, S2-03), a deterministic proportional-share algorithm — the report's title, "…A Flexible and Accurate Mechanism for Proportional Share Resource Allocation" (`eevdf-tr95`). Man-pages 6.19's sched(7) still names CFS as the default; the kernel's own document is cited for the default class.

Hands to 9.15: `docs/research-proposal.md:145` and `:424` restated as above; `docs/references.md` entries for sched(7) and sched_setattr(2) (man-pages 6.19) and the kernel's `sched-deadline.rst` and `sched-eevdf.rst` where the prose cites them, under the id-minting rule.

Compiled effect: none.

## D27 — sched_ext as the deployment path: the mechanism kept; the path stated as what could run on a kernel the depicted desktop already carries; "prototype of something shippable" stated as intent (2026-10-08)

By 인지오's decision, scope-card items 23 and 46: `docs/research-proposal.md:146` and `:844` (sched_ext as "Pluggable schedulers loaded from userspace as BPF programs") stand; `:152`'s "it is the concrete deployment path for anything this project produces, and it means our simulator work is a prototype of something shippable rather than a purely academic exercise" is restated to what holds, `:804`'s future-work sentence kept.

- **The mechanism** (`schedext-docs`; S2-01, S2-47): "sched_ext is a scheduler class whose behavior can be defined by a set of BPF programs - the BPF scheduler" (`sched-ext.rst:5–6` at v6.12); "The BPF scheduler can be turned on and off dynamically anytime" (`:14`); `SCHED_CLASS_EXT` "allows scheduling policies to be implemented as BPF programs" (`kernel/Kconfig.preempt` at v6.12).
- **The path on the depicted machine** (S2-52): Ubuntu 24.04's HWE kernel 7.0.0-34 (the depicted desktop's, 9.10 D48) sets `CONFIG_SCHED_CLASS_EXT` `y` for amd64 (`debian.master/config/annotations`); the runner's 6.17.0-1022-azure exposes `/sys/kernel/sched_ext` (state `disabled`, 9.11 D2). Operators run sched_ext schedulers in production (D8), and SteamOS ships LAVD as a selectable scheduler (D9).
- **What is intent, not fact:** the simulator models one CPU lane and nothing else (`docs/simulator/simulator-guide.md:44`); no algorithm or executor of this project has a sched_ext implementation. `:152` states sched_ext as the path by which the CPU driver could run on a real kernel, the port future work as `:804` says; "a prototype of something shippable" is stated as the intent.

Hands to 9.15: `docs/research-proposal.md:152` restated as above; `:844`'s "The realistic deployment path for this work" kept with the same scope; `docs/references.md` — the Ubuntu kernel's configuration (S2-52) entered under the id-minting rule where the prose cites it.

Compiled effect: none.

## D28 — macOS QoS row kept, cited to Apple's current API page and its archived guide; undeclared work runs as `default` (2026-10-08)

By 인지오's decision, scope-card item 24: `docs/research-proposal.md:147`'s row "macOS | Quality-of-Service classes (`user-interactive`, `user-initiated`, `utility`, `background`) | Developer declares it in code" stands, with one addition: work the developer leaves undeclared is treated as `default`.

- **The classes** (S2-53, Apple Developer documentation, Foundation `QualityOfService`, accessed 2026-10-08): "Constants that indicate the nature and importance of work to the system"; cases `userInteractive`, `userInitiated`, `utility`, `background`, `default`; macOS 10.10 and later; "Work with higher quality of service classes receive more resources than work with lower quality of service classes whenever there's resource contention."
- **The declaration and its effect** (S2-21, Apple's Energy Efficiency Guide for Mac Apps, archived, updated 2016-09-13): "By assigning a QoS to work, you indicate its importance, and the system prioritizes it and schedules it accordingly"; "The system uses QoS information to adjust priorities such as scheduling, CPU and I/O throughput, and timer latency"; "Work that has no QoS information assigned is treated as default"; `background` is for work "such as indexing, synchronizing, and backups".

Hands to 9.15: `docs/research-proposal.md:147` with the addition; `docs/references.md` — Apple's `QualityOfService` page and the archived guide entered under the id-minting rule where the prose cites them; the guidebook vol-01 `:3277`, `:3342`, `:3718` and vol-03 `:55` checked against the same passages.

Compiled effect: none.

## D29 — MLFQ as the baseline: restated to what each OS ships; "the family Linux, macOS and Windows all ship" leaves (2026-10-09)

By 인지오's decision, scope-card item 27: `docs/research-proposal.md:117`'s "MLFQ … is the algorithm family that Linux, macOS, and Windows all ship variants of", `:830`'s "The basis of most production schedulers" and `docs/background-guide.md:203`'s "the default scheduler family real OSes use" are restated to each vendor's own documentation (S2-54).

- **Windows** (Microsoft Learn, "Scheduling Priorities", "Priority Boosts", 2025-07-14): 32 priority levels, round-robin within the highest ready level; a thread is boosted "when a wait operation associated with disk or keyboard I/O finishes", on foreground and on input, and "the scheduler reduces that priority by one level each time the thread completes a time slice, until the thread drops back to its base priority" — an MLFQ form, as OSTEP names "Windows NT and subsequent Windows operating systems" (S1-02, p. 10).
- **macOS** (Apple's XNU, `doc/scheduler/sched_clutch_edge.md` at `xnu-12377.121.6`): "The scheduling bucket level uses an Earliest Deadline First (EDF) algorithm" across buckets that "roughly map to the QoS classes"; "a variation of the FreeBSD ULE scheduler" across thread groups; at the thread level the Mach timesharing algorithm, "thread priority = base priority - (thread CPU usage >> priority shift)" — usage-decayed priority inside an EDF-over-QoS hierarchy.
- **Linux**: EEVDF since 6.6, a proportional-share algorithm (D18, D26); OSTEP's MLFQ chapter never names Linux (S1-02).
- **Why MLFQ is the baseline**, restated: it is the textbook form of classification by behaviour (OSTEP ch. 8; Corbató 1962, D18), not a family every OS ships. "The basis of most production schedulers" and "the default scheduler family real OSes use" leave.

Hands to 9.15: `docs/research-proposal.md:117`, `:830`, `docs/background-guide.md:203` restated as above; `docs/references.md` entries for Apple's XNU scheduler document and Microsoft's two Learn pages under the id-minting rule; the guidebook vol-01's MLFQ-everywhere passages (`:3320` table, `:3338`, `:3344`) checked against S2-54.

Compiled effect: none.

## D30 — "It cannot remove starvation protection" leaves the model's bounds: the executor has no starvation window, the cap is a field the model sets, and the harness's 30 s guard judges the run (2026-10-09)
> Amended by D79 (the cap is the driver table's under every condition but llm_full and is to be enforced, not yet; four more lines and the trace example restated).
> Amended by D114 (§4.7 as D30 and D79 state it; `:756`, 인경민's team area, leaves the hand-off; by 인지오's decision).

Taken under 인지오's delegation (2026-10-09), scope-card item 71 (added from 9.11 D19's hand-off): `docs/research-proposal.md:473`'s bullet "It cannot remove starvation protection. Per-class bandwidth caps are enforced by the executor regardless of what any configuration says", in §4.7's list of what the model is never allowed to do, and `:756`'s "Bandwidth caps and starvation protection" among 인경민's areas, are restated to the project's own design and executor.

- **The executor has no starvation window** (`simulator/memo/memo_261001.md` §5.5, "Not implemented": "The executor's starvation safety net. EDF's deadline class and FIFO have no horizon."; §6, question 3: "No safety net exists, so there is no number."). 9.11 D7 took no executor net; one is reconsidered with 인경민 only if 9.14's dry runs show waits near 30 s (9.11 D19's hand-off to 9.14).
- **The cap is configuration, not a bound on it** (`docs/recognition-vocabulary.md` §2, the frozen envelope): `"batch_bandwidth_cap": null | 0.05–0.95`, "`null` means no ceiling"; validation rule 4, "`batch_bandwidth_cap` is `null` or clamped into 0.05–0.95". The model sets the one batch-class cap and may leave it unset; "regardless of what any configuration says" contradicts the schema, and "per-class caps" names more caps than it holds. The executor is to enforce the cap a configuration sets (`docs/simulator/simulator-guide.md` §5); the simulator does not yet read it (memo §5.5: "`batch_bandwidth_cap` — not even read from the config"; `simulator/src/notes.md`, gap 1).
- **What the schema bounds.** MLFQ's boost, the one anti-starvation rule the schema holds, can be lengthened to 10 s and not removed (`boost_interval_us` 10 000–10 000 000, §2's MLFQ table). FIFO and EDF's deadline class have no horizon (memo §5.5), so the model can choose a configuration under which a task waits without bound.
- **What judges such a run** (`harness/guards/guard-spec.yaml:137–148`): `starvation_floor`, 30 000 000 µs, `applies_to: all`, read per task as the largest `ready_wait` over any cause on the whole file; design, sched_ext's watchdog maximum borrowed for the deployment path (9.11 D19). A failed non-exempt guard on a run the RQ0 criterion reads makes the verdict `invalid` (`harness/tools/harness/evaluator.py:312–335`, `k_of_n_gap`). The guard judges the run after the fact; it bounds no configuration the model emits.
- **Restated:** `:473`'s bullet leaves §4.7's list. In its place §4.7 states what holds: the executor has no starvation window; under FIFO, EDF's deadline class or an unset cap a configuration can leave a task waiting without bound, and MLFQ's boost the model can lengthen to 10 s but not remove; a run in which any task waits more than 30 s fails the harness's `starvation_floor` guard, and on a run the criterion reads that failure makes the verdict invalid. The batch class's bandwidth cap is stated as a configuration field — unset, or 0.05–0.95 — which the executor enforces. `:756`'s duty becomes "the batch class's bandwidth cap"; "starvation protection" leaves.

Hands to 9.15:

- `docs/research-proposal.md:473`, `:756` restated as above; `:287`'s diagram line "per-class bandwidth caps" → the batch class's bandwidth cap.
- Found in the sweep (`grep -rn -i "starvation\|bandwidth cap" docs`), beyond 9.11 D19's lines (`docs/terminology.md:122`; guidebook vol-03 `:1089–1091`, `:1327–1329`; vol-04 `:1196`, `:1227`, `:1251–1257`, `:1317`): `docs/simulator/simulator-guide.md:210` ("per-class bandwidth caps, enforced by the executor regardless of what any config says"), restated to the one cap the configuration sets; guidebook vol-03 `:1093` ("이 상한은 실행부가 지킵니다. 설정이 무엇을 요구하든 상관없습니다"), the same; vol-03 `:451` and `:3749` ("class별 대역폭 상한") → the batch class's cap. The memos that told 인경민 a net exists (2026-09-08 `:16`, 2026-09-09 `:45`, `:82`) are point-in-time records, answered by the declared-class memo's paragraph (9.11 D19).

Compiled effect: none.

## D31 — a runner campaign for items 28 and 29: the kernel's switch and pick costs and a structured answer's latency, measured on the dataset's machine (2026-10-09)

Taken under 인지오's delegation (2026-10-09); the push it needs approved by 인지오 the same day ("approve to push"). Scope-card items 28 (the proposal's kernel quantities) and 29 (local inference latency).

- **Why a measurement.** The literature found gives context-switch costs on three machines of 2007–2021 (S1-01: 599 ns, Linux 4.15; S1-21: 3.8 µs direct, Linux 2.6.17; S1-23: at least 3 400 cycles, Linux 3.16) and nothing for the scheduler's pick (S1 search log; candidates "Not found", T10); no published latency of a short structured answer from a 3–8B model on a named x86 machine (T11). The proposal's §4.1 table states both. The dataset's values are this machine's (`measurement-campaign-workflow.md`), and the S4 record gives the method (S4-03–S4-10).
- **The method** (`campaign/method.md`, fixed before the gated launch): job `kernel` — the pipe ping-pong of Li, Ding & Shen with its single-process subtraction, `perf bench sched pipe` and lmbench `lat_ctx`; `pick_next_task_fair`, `pick_task_fair` and `sched_balance_newidle` timed per call by ftrace's function-graph tracer under three loads, a getpid-path calibration and the tracer's whole cost per call; per-CPU switch rates at idle. Job `llm` — llama.cpp at the commit S4-08 read, Qwen2.5-3B and Llama 3.1 8B at Q4_K_M (LocalScore's two models, S3-05), a stand-in recognizer request built from the frozen vocabulary and telemetry shapes, the `system`-only and the full-proposal schema, and llama-bench. EPYC 7763 under the machine gate; the workflow's stability rule on every value of the list.
- **The dry run** (run 37859640740, no gate): both jobs ran end to end. On the EPYC 7763, ping-pong 6.41–6.52 µs per round trip, self pipe 0.81–0.82 µs per pair, `perf bench sched pipe` 5.59–5.71 µs per round trip, `lat_ctx` 2.36–2.47 µs per switch; `pick_next_task_fair` median 791–802 ns under the ping-pong, the tracer's share not yet calibrated — `__x64_sys_getpid` is not traceable on 6.17.0-1022-azure, so the calibration moves to `__task_pid_nr_ns` and the untraced loads are added. On an EPYC 9V45 (not a repeat), the 3B answered the `system` block in 5.4 s and the full proposal in 9.0 s, the 8B in 13.4 s and 19.5 s, prompt processing most of each.
- **A consumer machine beside it.** The proposal's latency claim names "consumer hardware"; the runner is a server CPU's 4 vCPUs. The same request runs on 인지오's development Mac (Apple M1 Pro) as a separate observation, recorded in the S3 record.

Applied: `.github/workflows/meas-costs.yml`, `.github/campaign-costs.json`, `dataset/tools/meas/costs/`, `dataset/tools/meas/llm/`, `campaign/method.md`.

Hands to: items 28 and 29's decisions, on the pooled values.

Compiled effect: none.

## D32 — the proposal's scheduling background (§1.1–§1.2) restated to OSTEP, Miller and Deber, Li et al., and the dataset's measured CPU per keystroke (2026-10-09)
> Amended by D57 (Li, Ding & Shen's regions: in cache, beyond it, and the stride experiment) and D62 (the per-key venue and VS Code's stimulus).
> Amended by D63 (Miller's echo 0.1–0.2 s; Deber's indirect touch surface; EEVDF's requested slice; SJF's full conditions; Solaris's table as OSTEP describes it).
> Amended by D93 (research-proposal.md:416's FIFO clause and background-guide.md:119).

Taken under 인지오's delegation (2026-10-09), scope-card item 31: `docs/research-proposal.md:87`, `:95`, `:111` and `:113` are restated to their sources. OSTEP's chapters 7 and 8 re-read from copies byte-identical to S1-03 and S1-02 (SHA-256 `0912b1a3…`, `96241b4e…`; re-downloaded 2026-10-09).

- **SJF's optimality** (`:87`: "The theoretically optimal policy — Shortest Job First — requires knowing job lengths in advance, which nobody ever does"). OSTEP §7.4, p. 5: "given our assumptions about jobs all arriving at the same time, we could prove that SJF is indeed an optimal scheduling algorithm" (for turnaround, under §7.1's five assumptions, p. 2); §7.5, p. 6: "STCF is provably optimal". §7.9 "No More Oracle", p. 10: "in a general-purpose OS (like the ones we care about), the OS usually knows very little about the length of each job"; ch. 8, p. 1: "the OS doesn't generally know how long a job will run for, exactly the knowledge that algorithms like SJF (or STCF) require". Restated: SJF minimises average turnaround when every job arrives at once and its length is known, STCF without the simultaneous arrival; a general-purpose OS usually knows little of a job's length. "which nobody ever does" leaves.
- **What interactive work does per key** (`:95`: "works for a millisecond or two, and goes back to sleep"). The dataset's measured CPU per keystroke — the window rule: the process tree's run time until the next key, less the idle rate (9.5 D13) — on the EPYC 7763 runner under Xvfb with no GPU, so rendering runs on the CPU (each entry's venue bound), SWELL-KW keystrokes replayed (`dataset/archetypes.yaml` `input_run`): median 3.23 ms for LibreOffice Writer (p10–p90 2.53–9.55 ms), 4.07 ms for a Chrome text field (2.93–5.53 ms), 4.65 ms for Thunderbird's compose window (3.21–6.74 ms), 79.7 ms for VS Code, its TypeScript language server re-checking the file (15.3–179 ms). While typing, the three use 0.2–1.4 % of their CPU (`driven cpu-share`), VS Code 14–45 %. Restated: a few milliseconds of CPU per key for an office editor, a browser field and a mail composer, most of the time asleep; an IDE's language server can make it tens of milliseconds and a sizeable share of the CPU — named as the dataset's measurements, this software on this machine (9.5 D10).
- **The 100 ms** (`:111`: "a 100 ms delay before the screen responds is perceived as lag"). 9.11 D1: Miller's guideline, key-to-echo "no more than 0.1 to 0.2 seconds" and control feedback "No more than 0.1 second", his "best calculated guesses" (`miller-fjcc68`, p. 271); Deber et al. measured a latency detection threshold of 96 ms for indirect tapping, among which they place key typing behind "the textbook threshold of 100 ms" (`deber-chi15`, p. 1831). Restated: about 100 ms is the guideline's limit for a keystroke's echo, near a measured detection threshold for indirect input; "is perceived as lag" attributed to them.
- **The cost of interruption** (`:111`: "being interrupted frequently wastes cycles on context switches and destroys cache locality"). OSTEP §7.7, p. 8: programs "build up a great deal of state in CPU caches, TLBs, branch predictors, and other on-chip hardware. Switching to another job causes this state to be flushed and new state relevant to the currently-running job to be brought in, which may exact a noticeable performance cost"; Li, Ding & Shen measured the total cost per switch at 4.2–8.7 µs for working sets of 1–200 KB and 38.6–203.2 µs at 256–512 KB, past 1 000 µs at the largest (S1-21, p. 2; Linux 2.6.17, dual 2.0 GHz Pentium Xeon). Restated: each switch costs the switch itself and the cache state the program built, by an amount that grows with its working set; "destroys" leaves. Item 28 gives the switch's own cost on the dataset's machine.
- **Short turns at high priority** (`:113`: "The standard resolution is: give interactive work high priority but a very short turn on the CPU; give batch work low priority but a long turn"). OSTEP §8.5, pp. 8–9: "most MLFQ variants allow for varying time-slice length across different queues. The high-priority queues are usually given short time slices … (e.g., 10 or fewer milliseconds). The low-priority queues … longer time slices work well (e.g., 100s of ms)"; Solaris's TS table, 20 ms at the top to a few hundred at the bottom (p. 9); CTSS, 2^ℓ quanta at level ℓ (`corbato-sjcc62`, D18). Linux's EEVDF gives a latency-sensitive task a shorter slice without a priority level (`sched-eevdf.rst`, D18). Restated as MLFQ's resolution, as OSTEP describes most of its variants, not "the standard" of every scheduler.

Hands to 9.15: `docs/research-proposal.md:87`, `:95`, `:111`, `:113` restated as above; `:818`'s glossary "discards cache locality" with `:111` (its "1–5 μs" is item 28's). The guidebook vol-01 ch. 7.3 (`:1522–1524`) already states SJF's conditions and stays.

Compiled effect: none.

## D33 — the MLFQ illustration stated with the dataset's measured pair: an editor's runs between blocks against `cc1`'s object compile (2026-10-09)
> Amended by D62 (cc1's 367.6 ms runs from start to exit, unblocked in 99.4 % of object jobs).

Taken under 인지오's delegation (2026-10-09), scope-card item 32: `docs/research-proposal.md:123`'s "`bash` given a 10 ms slice uses 0.5 ms of it, while `cc1plus` burns all 10 ms" and `docs/background-guide.md:115`'s "The editor wakes for a keystroke, computes 0.5 ms of a 10 ms slice … The compiler chews through its full 10 ms slice" carry no source; the dataset measured both kinds of program on its machine, so the illustration is stated with them.

- **The editor** (9.5's `office-writer`, `meas-ci:interactive:2026-09-18`, 14 repeats, `task-9.5-interactive-typing/campaign/results-same-machine.md`, the driven phase): LibreOffice Writer's `soffice.bin` threads, while SWELL-KW keystrokes are typed, run 0.046 ms between blocks at the median, 1.13 ms at p90 and 2.98 ms at p99 (238 329 runs); the first run after a key 0.062 ms at the median; all of a key's CPU 3.23 ms at the median (D32).
- **The compiler** (9.6's `compiler-child`, `meas-ci:build:2026-09-18`, 14 repeats, `dataset/archetypes.yaml` `cc1_step_1`): `cc1` compiling one object of a warm `-j8` linux-6.6 build wakes once in 99.3 % of jobs and runs 367.6 ms of CPU at the median (p10 165.9 ms, p90 778.3 ms) before it next blocks.
- **Restated:** on the dataset's machine an editor's threads run a few hundredths of a millisecond between blocks, a few milliseconds at the 99th percentile, while `cc1` runs hundreds of milliseconds without blocking — the first gives up a 10 ms slice almost at once, the second uses every slice it is given. `bash` (not measured) and `cc1plus` (the C++ compiler; the dataset's build is C) leave the sentence. The measurements are this software on this machine (9.5 D10).

Hands to 9.15: `docs/research-proposal.md:123` and `docs/background-guide.md:115` restated as above, the diagram `:101–108` labelled with the same two programs; found in the sweep (`grep -n cc1plus docs`): `:177`'s §2.3 row "cc1plus ×8, bash" named for the build the dataset depicts (`cc1`, `-j8`).

Compiled effect: none.

## D34 — the world-knowledge examples restated: OBS encodes live and skips frames when it falls behind; `cargo build` compiles a Rust package; `updatedb` leaves the list, its unit declaring its class (2026-10-09)
> Amended by D65 (updatedb per D64; the OBS KB banner is commented out; Cargo's own words).
> Amended by D92 (research-proposal.md:160's encoder clause).

Taken under 인지오's delegation (2026-10-09), scope-card item 35, after a stage-3 read (S2-55, S2-56): `docs/research-proposal.md:185`'s "knowing things about software that an operating system has no way to learn on its own: that OBS is a real-time encoder, … that `cargo build` is a compiler and `updatedb` is maintenance", and `:176`'s row "LoL, Discord, OBS | Gaming while streaming | Encoder is now latency-critical too — it cannot drop frames", are restated to the sources. The Steam and antivirus clauses of `:185` are D16's and D15's.

- **OBS** (S2-55): "free and open source software for video recording and live streaming" (obsproject.com); when its encoder falls behind it warns "Encoding overloaded! Consider turning down video settings or using a faster encoding preset." and counts "Skipped frames due to encoding lag" (obs-studio `7d98bebe`, `frontend/data/locale/en-US.ini:58`, `:271`). Restated: OBS records and streams, encoding as it goes, so its encoder has a deadline per frame; "it cannot drop frames" leaves — an encoder that falls behind skips frames, which OBS counts and reports.
- **`cargo build`** (S2-56): "cargo-build — Compile the current package"; "Compile local packages and all of their dependencies"; Cargo is "the Rust package manager". Restated: `cargo build` compiles a Rust package and its dependencies, Cargo driving the compiler.
- **`updatedb`** leaves the list of what "an operating system has no way to learn on its own": its installed unit declares its class — plocate's `Nice=19`, `IOSchedulingClass=idle`; findutils' the same with `IOSchedulingPriority=7` (S3-02; D13). What the declaration leaves unsaid stays the point of `:185` — whether the user is waiting on the work, which D13's count shows is declared for some background tools and not others.
- **"None of that is observable from process behaviour"** (`:187`) restated as D14 and D15 state the pairs: what a process is for, and whether the user is waiting on it, is not stated by its behaviour; its run shape and declared class are, and the experiment tests what recognition adds over them.

Hands to 9.15: `docs/research-proposal.md:176`, `:185`, `:187` restated as above; `docs/references.md` — entries for OBS Studio (the locale file at `7d98bebe`; the home page) and the Cargo Book's `cargo build` page where the prose cites them, under the id-minting rule; the KB page quoted, not linked, at its own request. The sweep (`grep -rn -w -i obs docs`) finds no guidebook line on OBS; `docs/background-guide.md:20` ("what OBS does") and `docs/terminology.md:151` ("the model knows what OBS is") stay.

Compiled effect: none.

## D35 — the media deadlines stated as arithmetic on named rates: 16.7 ms at 60 Hz, 2.67 ms for 128 frames at 48 kHz; the audio workstation's "1–3 ms" restated to its buffer and Ardour's 5 ms target (2026-10-09)
> Amended by D66 (no source ties 64–128 frames to Ardour's 5 ms; the target's arithmetic is about 32 frames; JACK's defaults are its ALSA backend's).
> Amended by D90 (the consequence of a missed deadline, per kind: research-proposal.md:414, :820, background-guide.md:207).

Taken under 인지오's delegation (2026-10-09), scope-card item 36: `docs/research-proposal.md:414` ("this must complete within 3 ms or a frame drops"), `:640` ("Its deadlines are 1–3 ms rather than gaming's 16 ms, buffer underruns are audible rather than a dropped frame") and `:820` ("A game rendering at 60 fps has a 16 ms deadline every frame … An audio buffer at 128 samples has a deadline nearer 3 ms; missing it is audible") are restated to arithmetic on rates their sources name.

- **The frame** (arithmetic): 1 / 60 Hz = 16.67 ms. Steam Deck's LCD runs "up to 60Hz", adjustable 40–60 Hz; its OLED "up to 90Hz" (S2-39), 11.1 ms. The dataset's game chain ticks every 16 667 µs (`steamos-refresh`, design, 9.4). Restated: "16.7 ms at 60 Hz".
- **The audio buffer** (arithmetic): 128 / 48 000 Hz = 2.67 ms. 48 kHz is PipeWire's and JACK's default rate; their default buffer is 1 024 frames, 21.3 ms (`default.clock.quantum = 1024`, S2-36; `jackd -p` "(default: 1024)", S2-37); a smaller buffer is the user's low-latency choice — "If you need low latency, set -p as low as you can go without seeing xruns" (S2-37). Restated: a 128-frame buffer at 48 kHz, a low-latency setting below the 1 024-frame default, comes due every 2.67 ms.
- **The audio workstation** (`:640`): no source states "1–3 ms". Ardour's manual: the A/D/A conversion alone is "about 1.5–2 ms", and "Latency below 5 ms should be suitable for a professional recording setup", which needs "extremely low buffer sizes" (S2-38). Restated: recording through a 64–128-frame buffer at 48 kHz gives a period of 1.33–2.67 ms (arithmetic), the buffer Ardour's 5 ms target calls for; "gaming's 16 ms" as the 60 Hz frame above.
- **"audible"** kept, cited: a missed audio deadline is an xrun, "leaving its merry trail of clicks, pops and crackles" (S2-57, Ardour's manual).
- **`:414`'s EDF row** restated without mixing the two: a periodic job's deadline is its next period — a frame every 16.7 ms at 60 Hz, a 128-frame audio buffer every 2.67 ms at 48 kHz.

Hands to 9.15: `docs/research-proposal.md:414`, `:640`, `:820` restated as above (`:640`'s Game Mode and whitelist clauses are D5's); `docs/references.md` — PipeWire's and JACK's defaults (S2-36, S2-37), the Ardour manual's two pages (S2-38, S2-57) and the Steam Deck page (S2-39) where the prose cites them, under the id-minting rule.

Compiled effect: none.

## D36 — lottery scheduling as the paper states it: shares proportional in expectation, starvation absent for any client holding tickets, O(n) selection with a list and O(lg n) with a tree; "Stride" leaves the menu row (2026-10-09)
> Amended by D67 (a ticket holder eventually wins, after 1/p lotteries on average, with no bound).

Taken under 인지오's delegation (2026-10-09), scope-card item 38: `docs/research-proposal.md:415` ("Lottery / Stride … MLFQ cannot guarantee proportions. "Roughly less" is easy; "exactly 15% to background" is not"), `:422` ("its advantage is proportional guarantees and starvation-freedom, not speed. Selection is O(n) in the number of processes (O(log n) with a tree)") and `:828` ("Gives proportional CPU shares and freedom from starvation, at O(n) selection cost") are restated to `waldspurger-osdi94` (S1-09; the copy re-downloaded 2026-10-09, SHA-256 `e704678e…`, equal to the record's).

- **Proportional, in expectation** (§2.2, p. 2): "Scheduling by lottery is probabilistically fair. The expected allocation of resources to clients is proportional to the number of tickets that they hold. … the actual allocated proportions are not guaranteed to match the expected proportions exactly. However, the disparity between them decreases as the number of allocations increases"; throughput proportional to tickets "with accuracy that improves with √n". "proportional guarantees" and "exactly 15% to background" restated: lottery gives the background an expected 15 %, its error shrinking as lotteries accumulate.
- **Starvation** (p. 2): "Since any client with a non-zero number of tickets will eventually win a lottery, the conventional problem of starvation does not exist." Kept, scoped to a client holding tickets.
- **Selection cost** (§4.2, p. 3): "O(n) operations to traverse a client list of length n"; with "a tree of partial ticket sums … only O(lg n) operations". Kept. "slower per decision than popping an MLFQ queue head" kept as the complexity comparison it is: MLFQ runs the jobs of the highest non-empty queue in round-robin (OSTEP ch. 8, Rules 1–2).
- **"Stride"** leaves `:415`'s row: no registry entry and no read carries stride scheduling, and the frozen menu's algorithm is `LOTTERY` (`docs/recognition-vocabulary.md` §2). "It earns its place because ticket allocation is the natural way to express something like `batch_bandwidth_cap`" (`:422`) is a design statement and stays.

Hands to 9.15: `docs/research-proposal.md:415`, `:422`, `:828` restated as above; `docs/references.md` `waldspurger-osdi94`'s role line with the selection cost (§4.2) beside the quantum it quotes.

Compiled effect: none.

## D37 — EDF's optimality stated with its conditions: one processor, Liu and Layland's (A1)–(A5), utilisation at most 1 (2026-10-09)
> Amended by D68 (the optimality sentence is on p. 58; above utilisation 1 no feasible schedule exists, p. 56).

Taken under 인지오's delegation (2026-10-09), scope-card item 40: `docs/research-proposal.md:824`'s "Optimal for meeting deadlines on a single core, but requires deadlines to be declared" is restated to `liu-jacm73` (S1-10; the scan re-downloaded 2026-10-09, SHA-256 `de9fb725…`, equal to the record's).

- **The conditions** (printed p. 48): (A1) periodic requests at constant intervals; (A2) "each task must be completed before the next request for it occurs"; (A3) independent tasks; (A4) constant run-time; (A5) no critical non-periodic tasks — on "a single processor" (Abstract).
- **The result** (printed p. 55–56): "if a set of tasks can be scheduled by any algorithm, it can be scheduled by the deadline driven scheduling algorithm"; "THEOREM 7. For a given set of m tasks, the deadline driven scheduling algorithm is feasible if and only if (C1/T1) + (C2/T2) + ··· + (Cm/Tm) ≤ 1." The paper says nothing of behaviour above a utilisation of 1 (`liu-jacm73`'s registry line).
- **"requires deadlines to be declared"**: under (A2) a task's deadline is its next request, so the algorithm needs each task's period; Linux's `SCHED_DEADLINE` takes a declared runtime, deadline and period through `sched_setattr(2)` (D26).
- **Restated:** on one processor, for independent periodic tasks whose deadline is the next request, EDF schedules every task set any algorithm can — exactly those whose utilisation is at most 1 — and it needs each task's period or deadline.

Hands to 9.15: `docs/research-proposal.md:824` restated as above; `:414`'s EDF row read with it (D35).

Compiled effect: none.

## D38 — the "70 % fallbacks" example stated through the guard that judges it (2026-10-09)
> Amended by D69 (held time runs the configuration in force; data contracts §7; "70%" leaves).

Taken under 인지오's delegation (2026-10-09), scope-card item 41: `docs/research-proposal.md:718`'s "A condition that scores well while 70% of its configurations were fallbacks did not demonstrate anything about recognition; it demonstrated that MLFQ is fine" is an example with no source, and the project has since fixed the line it illustrates.

- **The line, as designed** (`harness/guards/guard-spec.yaml:115–124`; 9.11 D10): `provenance_share`, the time-weighted share of `fallback` and `held` configuration intervals, below 0.5 under every condition but `fixed`; design, reading appendix B.3's "most of its configurations were fallbacks" (`:916`) as a majority of the run's time. A failing guard on a run the RQ0 criterion reads makes the verdict invalid (D30).
- **What a fallback is** (`docs/data-contracts.md` §6): "the default, from boot or after repeated failures" — the boot default configuration, plain MLFQ (`docs/recognition-vocabulary.md` §2), so "it demonstrated that MLFQ is fine" holds of a fallback-heavy run.
- **Restated:** a condition whose run spent half or more of its time under fallback or held configurations fails the `provenance_share` guard — it demonstrated nothing about recognition, only that the boot default is fine. "70%" leaves, or stays marked as an example above the guard's line.

Hands to 9.15: `docs/research-proposal.md:718`, and `:916` (B.3) with it, stated as above.

Compiled effect: none.

## D39 — "a gaming session lasts an hour" restated to the two measured games; "stable for the whole thing" stated as the premise it is (2026-10-09)
> Amended by D70 (Chambers is the counter-case; WoWAH's 1.8 h is a median of per-avatar averages, one realm's Horde faction; six coreset files test transitions).

Taken under 인지오's delegation (2026-10-09), scope-card item 42, after a stage-3 read (S3-23): `docs/research-proposal.md:303` ("A gaming session may last an hour; polling every 30 seconds would produce 120 identical answers") and `:732` ("A gaming session lasts an hour; the situation is stable for the whole thing") are restated to what the sources measure.

- **The measured sessions:** on one World of Warcraft realm over three years, per-avatar mean session time 2.8 h, median 1.8 h, 5th–95th percentile 0.4–5.5 h, with a "knee" at about one hour — "a high probability that players will stay for at least one hour, but usually no longer than 5 hours" (S3-11, WoWAH, MMSys 2011, Table 4 and p. 126; 10-minute sampling); on one Counter-Strike server over 13 months, "more than 99% of all sessions last less than 2 hours" (S3-23, Chambers et al., IMC 2005). Both are server-side connection time to one game, not a PC's process activity. No measurement of PC gaming sessions in general was found (S3, "Not found", T12; the 2026-10-09 search).
- **Restated `:303`:** a gaming session can run an hour or more — a median 1.8 h on one MMO realm, under 2 h for more than 99 % on one shooter's server — so polling every 30 s would ask the same question about 120 times an hour (arithmetic).
- **Restated `:732`:** "the situation is stable for the whole thing" leaves as a statement of fact. It is the premise of the risk: if the process set stays unchanged through a session, the moments where recognition matters are its transitions — which is why the workloads are built around transitions. How often a desktop's process set changes is not measured by any source found (only foreground-window switching, S3-12, S3-16).

Hands to 9.15: `docs/research-proposal.md:303`, `:732` restated as above; `docs/references.md` entries for WoWAH (S3-11) and Chambers et al. (S3-23) where the prose cites them, under the id-minting rule.

Compiled effect: none.

## D40 — "stating its reading first tends to produce better decisions" restated to what the literature finds and turned into a question the project measures (2026-10-09)
> Amended by D71 (the scale leg restated to current 7–9B models; the format leg to what Tam et al.'s published version tests).

Taken under 인지오's delegation (2026-10-09), scope-card item 43: `docs/research-proposal.md:340`'s "*Quality.* Requiring the model to state its reading before committing to a decision tends to produce better decisions than asking for the decision alone" has no source, and the sources found bound it. The copies re-downloaded 2026-10-09 are byte-identical to S1-25–S1-28's, each passage below re-read in them.

- **Scale** (S1-26, Wei et al., NeurIPS 2022, p. 4): chain-of-thought prompting "does not positively impact performance for small models, and only yields performance gains when used with models of ∼100B parameters. We qualitatively found that models of smaller scale produced fluent but illogical chains of thought, leading to lower performance than standard prompting."
- **Task kind** (S1-28, Sprague et al., ICLR 2025, Abstract): "CoT gives strong performance benefits primarily on tasks involving math or logic, with much smaller gains on other types of tasks. On MMLU, directly generating the answer without CoT leads to almost identical accuracy as CoT unless the question or model's response contains an equals sign".
- **Format** (S1-27, Tam et al., arXiv 2408.02442v3, p. 7): "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy."
- **Restated:** the recognizer's answer is a classification from a closed menu, from a 3–8B local model under a JSON schema — a task kind, a scale and a format for which the literature reports little or no gain from reasoning first. The *Quality* bullet leaves as a claim; whether stating the reading first improves the answer is stated as a question Layer 1 can answer, the recognizer run with and without the `reasoning` field. The *Diagnosis* and *Auditability* bullets (`:339`, `:341`) stand: they argue for the field's use, not its effect on accuracy. The latency cost of the field is item 29's measurement (D31: the full-proposal schema against the `system` block alone).

Hands to 9.15: `docs/research-proposal.md:340` restated as above; `docs/references.md` entries for Wei et al., Sprague et al. and Tam et al. where the prose cites them, under the id-minting rule. **9.14:** whether Layer 1 pre-registers the with-and-without-`reasoning` comparison is the RQ0 gate spec's and the recognizer's design, not decided here.

Compiled effect: none.

## D41 — "batch processes consume every cycle you give them" restated to the measured batch jobs: most keep a CPU busy, the indexer does not (2026-10-09)
> Amended by D61 (every measured batch job keeps a CPU busy while it works; the indexer 88–91 % from Initializing; the rescan figure leaves).

Taken under 인지오's delegation (2026-10-09), scope-card item 45: `docs/research-proposal.md:97`'s "**Batch** processes have nobody waiting — a compile, a backup, a file indexer, a video encode. Their defining trait is that they consume every cycle you give them. An eight-second compile computes for eight solid seconds" is read against the dataset's measurements of the same four kinds, each alone on one CPU of the EPYC 7763 runner.

- **The compile:** the warm `-j8` linux-6.6 build keeps the CPU 99.74–99.77 % busy over 14 repeats, `-j1` 99.70–99.71 % (S3-21, the busy share; 9.6's `meas-ci:build:2026-09-18`); `cc1` runs a median 368 ms of CPU between blocks (D33).
- **The backup:** Déjà Dup's incremental backup, saturation 0.9935–0.9952 over the job (`incremental-backup`, 9.10 D119), and it runs in the idle class: Déjà Dup wraps it in `chrt --idle 0` (9.10 D112; 9.11 S2-27).
- **The video encode:** HandBrakeCLI 1.7.2 at its default preset, saturation 0.99938–0.99947 (`video-transcoder`, 9.10 D97).
- **The indexer:** Tracker's first index of a home, saturation 0.655–0.676 over the job, its run between voluntary blocks 1.876 ms (`file-indexer`, 9.10 D81; D14); 9.6's rescan phase kept the CPU 20.4–25.4 % busy (S3-21).
- **Restated:** batch work has nobody waiting on each step and runs long; most of it keeps a CPU busy for as long as it runs — a kernel build, a video encode and a backup at 99.4–99.9 % on the dataset's machine — but not all: a file indexer blocks every couple of milliseconds and leaves a third of the CPU idle. "consume every cycle you give them" leaves as a trait of all batch work; "An eight-second compile computes for eight solid seconds" stands as an illustration, the build measured at 99.7 %.

Hands to 9.15: `docs/research-proposal.md:97` restated as above; the bash/cc1plus diagram (`:101–108`) is D33's.

Compiled effect: none.

## D42 — TuxBot and Vulcan read in full and cited in related-work as adjacent LLM work: TuxBot beside the tuning efforts, Vulcan beside the synthesis line (2026-10-09)
> Amended by D72 (Vulcan's v3 Table 1; "the nearest architecture" leaves; DOI out of the cite line; LumOS read in full).
> Amended by D111 (related-work cites TuxBot, LumOS and Vulcan, each by what it does, without superlatives; by 인지오's decision).

Taken under 인지오's delegation (2026-10-09), scope-card items 48 and 49: both entries were `provisional` (abstract pages only); stage 2 read both bodies (S1-17, TuxBot v2; S1-18, Vulcan v3 and v1), and the 2026-10-09 re-check finds no newer version (S1 search log #56).

- **TuxBot** (S1-17): "a host-side framework for steady-state OS tuning with bounded language-model guidance"; "every proposed change passes through typed validation before reaching kernel or sysctl interfaces"; it adjusts "the parameters of such OS controllers, e.g., the CPU scheduler time slice or the network stack's polling budget, over seconds-to-minutes timescales", out of band, not "kernel fast-path controllers such as the CPU scheduler"; "13 live workloads from five benchmark suites while tuning up to 41 Linux parameters". It reports no measurement of recognition, so D12's scoped statement holds.
- **Vulcan** (S1-18): LLM-driven search synthesizing "simple stateless decision functions" in a restricted language, Anvil, "that guarantees important properties by construction"; evaluated on spot-VM scheduling, cache eviction and tiered memory; CPU scheduling appears only as an interface example in v1's Table 3. "Accepted for publication at EuroSys 2027" (the authors' arXiv comment); its DOI 10.1145/3842654.3848582 is not registered at Crossref on 2026-10-09.
- **Where related-work cites them** (`docs/related-work.md:32`): TuxBot beside the adjacent tuning efforts, as the nearest architecture to this work's — an LLM setting a live host's controller parameters out of the fast path, behind a typed validator; Vulcan beside Kgent, as LLM synthesis of verifiable policy code, its domains named (not CPU scheduling).
- **Status:** `tuxbot-arxiv26` — verified, v2's full text read 2026-10-07 (S1-17, SHA-256 `543bd4fc…`), no venue; "Read the paper before citing, and decide which related-work subsection it belongs to" answered. `vulcan-arxiv25` — verified, v3's full text read (S1-18, `ed85ead6…`), the EuroSys 2027 acceptance stated as the authors'; the id stays arXiv's under the id-minting rule until the DOI resolves, then re-minted for the proceedings.

Hands to 9.15: `docs/related-work.md:32` with the two sentences above; `docs/references.md` `tuxbot-arxiv26` and `vulcan-arxiv25` status and role lines as above (Vulcan's "Comments field: "19 pages"" and "(v2, submitted 2026-06-16)" brought to v3, "21 pages, 12 figures. Accepted for publication at EuroSys 2027"); the D25 key map gains `tuxbot` and `vulcan`; `schedcp-mlsys25`'s status line ("both `provisional` — identified from their abstract pages, bodies unread") updated.

Compiled effect: none.

## D43 — the six scholarly entries' status lines gain the independent read and its copies (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 55: `ghost-sosp21`, `decima-sigcomm19`, `firm-osdi20`, `park-neurips19`, `eevdf-tr95` and `corbato-sjcc62` carry "verified 2026-09-12" from the author's own reads, with no independent read and no copy in the clone. Stage 2 read each in full (S1-01, S1-06, S1-07, S1-08, S1-05, S1-04), D17–D20 rest on those reads, and the copies were re-downloaded on 2026-10-09 from the same URLs, byte-identical, a passage of each re-read:

| Entry | Record | SHA-256 | Passage re-read 2026-10-09 |
|---|---|---|---|
| `ghost-sosp21` | S1-01 | `c37d6360…` | "not well-tolerated below an O(month) granularity" (§2, p. 3) |
| `decima-sigcomm19` | S1-06 | `b6b50a58…` | "generalizes poorly and underperforms the optimized weighted fair policy" (§7.4, p. 11) |
| `firm-osdi20` | S1-07 | `a0adcf98…` | "rapid (re)training of the proposed system" (p. 3) |
| `park-neurips19` | S1-08 | `c686bc44…` | "consists of 12 real world system-centric optimization problems" (Abstract) |
| `eevdf-tr95` | S1-05 | `b44b71a7…` | the title, "…Proportional Share Resource Allocation" |
| `corbato-sjcc62` | S1-04 | `3e5f2a3b…` | "entirely automatic, depending on performance and program size" (printed p. 342) |

Each status line keeps its 2026-09-12 read and adds: "independently read in full 2026-10-07 (9.12 S1-xx), the copy's SHA-256, re-verified 2026-10-09". The tier of each is unchanged (scholarly).

Hands to 9.15: `docs/references.md` — the six status lines as above.

Compiled effect: none.

## D44 — `scx` and `schedext-docs` confirmed against D7, D8 and D10: tier and role as those decisions leave them (2026-10-09)
> Amended by D73 (scx's README states Meta's deployment in progress; the deployment-path claim and :215 restated).
> Amended by D112 (the tier rule admits a deployed system's documented design or behaviour, attributed at its pinned version, and its published figures as its report; by 인지오's decision).

Taken under 인지오's delegation (2026-10-09), scope-card items 56 and 57: no further read; the two entries' role and status lines are brought to what D7, D8, D10 and D27 decided.

- **`scx`** (deployed-system): role — the repository ships the schedulers (fifteen at `v1.1.3`, S2-09) and documents scx_lavd's design (its README and `lat_cri.bpf.c`, D10), and holds the three schedulers' watchdog timeouts (9.11 D19); "existence of production sched_ext schedulers" restated to existence of the schedulers, production deployment being stated by the operators' own entries (D8: Meta's LPC 2024 slides and LPC 2025 abstract; D9: Valve's SteamOS sources), never by `scx`. Status — adds the D10 read of scx_lavd's README and `lat_cri.bpf.c` at `v1.1.3`.
- **`schedext-docs`** (deployed-system): role kept — mechanism, runtime loading and the integrity and fallback statement, with no verifier claim (D7); the deployment path as D27 states it (what could run on a kernel the depicted desktop already carries). Status — adds the v6.11 / v6.12-rc1 / v6.12 tree check (S2-47) as the ground of "first released in 6.12" (D7's hand-off).

Hands to 9.15: `docs/references.md` `scx` (`:214`, `:216`) and `schedext-docs` (`:291`, `:293`) as above.

Compiled effect: none.

## D45 — `gamemode-docs`' open question resolved: Microsoft's Xbox Support article states Game Mode holds back Windows Update's driver installs and restart notifications while a game runs (2026-10-09)
> Amended by D74 (dated: Xbox Wire 2018-10-02 and the 2018-12-30 capture; ananicy-rules' role line handed).

Taken under 인지오's delegation (2026-10-09), scope-card item 59, after a stage-3 read (S2-58): the registry's "one open question, deliberately unresolved" — "whether Microsoft documents that Game Mode defers Windows Update driver installs or restart/notification prompts during play" — is answered by the Microsoft-published page the entry named, read rendered.

- **What Microsoft states** (S2-58, Xbox Support, "Use Game Mode while gaming on your Windows device", rendered 2026-10-09): "When you use Game Mode, Windows prioritizes your gaming experience by turning things off in the background. When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications; Helps achieve a more stable frame rate depending on the specific game and system"; "Game Mode is turned on by default." K5's C-gamemode-5 (CONTRADICTED against the status line) is confirmed first-hand.
- **What it adds to D2's Game Mode sentence:** besides exclusive CPU sets and GPU priority (Microsoft Learn, S2-16), Windows Game Mode defers part of the system's own background work while a game runs — Windows Update's driver installations and restart notifications. With Steam pausing its downloads at game launch (D16), it is a shipped instance of background work held back during play, the half of `docs/workload/grounding-sources.md:18`'s Role A line ("the wanted/unwanted-background distinction") that K3's C-ananicy-rules-4 found NOT IN SOURCE for ananicy: the instance holds back named system work, by the vendor's rule, not by a judgement of what the user wants.
- **How a game is recognised** stays undocumented (S2-58 does not say); D1 stands.

Hands to 9.15:

- `docs/references.md` — a deployed-system entry for the Xbox Support article under the id-minting rule (URL, rendered 2026-10-09, SHA-256 from S2-58, "no date on the page"); `gamemode-docs`' status line: the open question closed, pointing to the new entry; its "[Exact URLs to pin.]" replaced per D2.
- `docs/related-work.md:40` (D2's restated Game Mode sentence) and `docs/research-proposal.md:148–149` (the §2.1 rows, D1) gain the Windows Update deferral, cited to the new entry; `docs/workload/grounding-sources.md:18`'s Role A line restated to what the instances ground: the gaming category (Windows, macOS, Feral), background work held back during play by vendor rule (Windows Update in Game Mode; Steam's downloads, D16), and a per-name priority catalogue (`ananicy-rules`, D3) — not a wanted/unwanted judgement by any of them.

Compiled effect: none.

## D46 — the SYSmark 2011 note: the departures concerned SYSmark 2012, and the reasons given include its workloads, not its scoring alone (2026-10-09)
> Amended by D75 (Dessau's own post read; the weighting complaint is AMD's; the registry's :250 note handed).

Taken under 인지오's delegation (2026-10-09), scope-card item 70: the paper's prose (`docs/related-work.md`, `docs/research-proposal.md`, `docs/research-claims.md`, `docs/background-guide.md`) carries no sentence on the 2011 departures (`grep -n -i "sysmark\|bapco"`, 2026-10-09). The claim stands only in `docs/workload/source-vetting.md:40` — "2011 AMD/Nvidia/VIA departure concerned scoring weights, not scenario lists — state this explicitly in the paper" — and its premise, "Scenario/application lists documented separately from scoring methodology, so taxonomy can be cited without touching contested scoring" (C-sysmark30-5, prose only). The registry and `dataset/sources.yaml` lines the 2026-09-13 verification named no longer carry it.

- **What the departures concerned** (S2-40–S2-44): SYSmark 2012, not SYSmark 30. AMD (its press release, 2011-06-21): "AMD does not believe SM2012 achieves this objective" — "clear and reliable measurements" — and it "will only endorse benchmarks based on real-world computing models and software applications"; Dessau's blog as Tom's Hardware quotes it: "the SYSmark benchmark is not only comprised of unrepresentative workloads … but it actually generates misleading results". VIA (as AnandTech and X-bit Labs reproduce it): the tests "developed for SYSmark 2012 and EEcoMark 2.0 do not accurately reflect real world PC usage scenarios and workloads". Nvidia: "We have resigned" — "No reason was given" (AnandTech). AnandTech's own summary of AMD's: "a long standing dispute over the weighting of scores within the SYSmark suite".
- **"concerned scoring weights, not scenario lists"** is contradicted: two of the three vendors objected to the workloads' representativeness, and AMD's dispute over weighting is a report of it beside that.
- **The paper's need:** it cites SYSmark 30 for its scenario categories, existence only (`sysmark30`'s role). The 2011 dispute concerned an earlier version's workloads and scoring; no sentence of the paper needs it, and the instruction "state this explicitly in the paper" leaves. If the paper ever discusses benchmark validity, the dispute is stated as the vendors stated it, cited to AMD's release (S2-40) and the reproduced VIA statement (S2-41, S2-43), with AnandTech's report attributed.

Hands to 9.15: `docs/workload/source-vetting.md:40`'s sentence restated as above or removed; `docs/references.md` — entries for AMD's release and AnandTech's report only if prose cites them.

Compiled effect: none.

## D47 — part E: the kernel build's grounding line restated to SchedCP's own use and the dataset's measured build; items 62 and 66–69 pass through (2026-10-09)
> Amended by D76 (SchedCP's evaluation, singular; ocallahan-atc17 kept; cc1_step_1).
> Amended by D103 (item 63's pass-through lines handed).

Taken under 인지오's delegation (2026-10-09), scope-card items 62, 63 and 66–69.

- **Item 63 — `docs/workload/grounding-sources.md:32`**: "kernel build (make -jN) | The de facto standard compile workload in every scheduler evaluation, including SchedCP's | The compile Family's fork-heavy, short-lived-children structure". "in every scheduler evaluation" is a universal no source states (NOT IN SOURCE, K1). What SchedCP states (v4, S1-34, SHA-256 `cce49d3c…`, §5): "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF"; and "short-lived processes" is its Observation Agent's generated profile, "it produces profiles like "CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization."" (§4; C-kernelbuild-2). The structure the dataset carries is its own measurement: a warm `-j8` linux-6.6 defconfig build, 5 957 forks under 719 make processes and 2 857 six-member object jobs per build, `cc1` a median 368 ms of CPU (9.6's `build-orchestrator` and `compiler-child`, D33). Restated: a compile workload scheduler evaluations use, SchedCP's among them (kernel compilation, its 1.79×); the compile family's structure grounded in the dataset's measured build; SchedCP's "short-lived processes" attributed as its agent's profile text, not a measurement.
- **Item 62 — `source-vetting.md:14`'s precedent sentence** ("interbench/hackbench/rt-app/stress-ng have LWN-documented or peer-reviewed usage precedents"): the paper's prose names none of these tools (`grep -n -i "interbench\|schbench\|hackbench\|rt-app\|stress-ng\|precedent"` over `docs/related-work.md`, `docs/research-proposal.md`, `docs/research-claims.md`, 2026-10-09: no line), so no read is owed; the K1 verdicts (C-interbench-13 and the lines of item 62) pass through to 9.15 as recorded, with 9.11 D12's precedent wording.
- **Items 66–69** (9.7, 9.7 D17, 9.8, 9.9): pass through as the scope card lists them; no sentence of the paper relies on them. Item 67's `interbench` entry stays while the Role B prose and vol-02 ch. 8.3 cite it (the scope card's answer).

Hands to 9.15: `docs/workload/grounding-sources.md:32` restated as above; items 62 and 66–69's lines applied from their recorded verdicts.

Compiled effect: none.

## D48 — constrained decoding stated as the servers document it: a completed answer is well-formed; a schema feature the converter lacks is skipped silently and an answer cut at the token limit is not, so the parse branch stays (2026-10-09)
> Amended by D77 (the converter's behaviour as its code shows; the schema carries the menu, not the number ranges).

Taken under 인지오's delegation (2026-10-09), scope-card item 30: `docs/research-proposal.md:489`'s "a local server (Ollama or vLLM)" and "constrained decoding (GBNF grammars, guided decoding) can make malformed output structurally impossible, removing an entire class of validator branches" are restated to the servers' documentation (S2-33, S2-34, S2-35, S2-59) and the project's own requests.

- **What is guaranteed.** llama.cpp: "the `root` rule always defines the starting point of the grammar. In other words, it specifies what the entire output must match" (S2-33, `grammars/README.md:106`); vLLM: with `json`, "the output will follow the JSON schema" (S2-34); Ollama: "The model will generate a response that matches the schema", and in JSON mode "the output will always be a well-formed JSON object" (S2-35).
- **What is not.** llama.cpp converts "a subset" of JSON Schema and "Unsupported features are skipped silently" (S2-33, `:143`, `:207`), so an answer can satisfy the grammar and miss a constraint of the schema; and a generation can end at the token limit before the grammar completes — `stop_type` "`limit`: Stopped because `n_predict` tokens were generated before stop words or EOS was encountered" (S2-59). The schema is not shown to the model: "describe it explicitly in your prompt" (S2-33, `:151`).
- **What the project observed** (D31's runner repeats landed by 2026-10-09, the dry run, and S3-22): 164 of 164 requests under a JSON schema parsed, every one stopping at `eos`, at an `n_predict` of 384 against answers of 25–96 tokens.
- **Restated:** constrained decoding restricts every generated token to the grammar compiled from the schema, so an answer that completes is well-formed; the validator still needs its parse-failure branch for an answer cut off at the token limit — the data contracts' `proposal: null` with the verbatim `raw` (`docs/data-contracts.md` §7) — and its own checks for what the schema cannot carry or the converter skips (the menu, ranges and cross-field rules of `docs/recognition-vocabulary.md` §2). "structurally impossible" and "removing an entire class of validator branches" leave. "a local server (Ollama or vLLM)" names llama.cpp's server beside them, the server the project's measurements ran.

Hands to 9.15: `docs/research-proposal.md:489`'s two clauses restated as above (its latency clause is item 29's); `docs/references.md` — llama.cpp's grammar and server documentation at `bd4eeaa0`, vLLM's at `v0.31.0` and Ollama's at `f9f4af6c` under the id-minting rule where the prose cites them.

Compiled effect: none.

## D49 — D13 amended: Apple documents priority inflation on its own platform under the traditional Mach scheduler; Linux's units still lower more than they raise (2026-10-09)
> Amended by D78 (Apple's words: priority inflation as the Mach scheduler's artifact; no "macOS's own", no "instance").

Taken under 인지오's delegation (2026-10-09), amending D13 (scope-card item 26) on a passage found while reading S2-54 for item 28: D13 said of `docs/research-proposal.md:158`'s "Those that do tend to claim they are the most important thing on the system" that "no documented case of over-claiming was found (S2-29)". One is documented by a vendor.

- **The passage** (Apple's XNU, `doc/scheduler/sched_clutch_edge.md:7` at `xnu-12377.121.6`, S2-54, SHA-256 `5f4201d2…`, "Background"): "One artifact of this thread based timesharing approach is that threads at the same priority level are treated similarly irrespective of which user workload they are servicing, which often leads to non-optimal decisions. It ultimately leads to priority inflation across the platform with individual subsystems raising their priority to avoid starvation and timesharing with other unrelated threads." Apple states it as a motivation for the Clutch scheduler, of macOS's own subsystems under the traditional Mach model.
- **What it does and does not ground.** A documented instance: on macOS, under thread-level timesharing, subsystems raised their priority to avoid starvation — by Apple's account, not measured here. Not a tendency of declaring programs in general: on Debian's installed units, 40 of the 56 that declare only lower their priority and 16 only raise it (S3-20, D13), and macOS's QoS classes are declared per unit of work by the developer (D28).
- **D13's restatement amended:** "Those that do tend to claim they are the most important thing on the system" still leaves as a general claim; the limit may add that over-declaration is documented on one platform — Apple's subsystems under the traditional Mach scheduler (S2-54) — while the Linux count runs the other way.

Hands to 9.15: with D13's lines (`docs/research-proposal.md:158`, `docs/background-guide.md:18`, the guidebook vol-01 `:2099` — "성능에 민감한 프로그램들이 필요 이상으로 높은 priority를 요구하는 경향" — restated to this instance with its source, not left unsourced); `docs/references.md`'s entry for Apple's XNU scheduler document (D29's hand-off) with this passage in its role.

Compiled effect: none.

## D50 — the kernel quantities restated to the dataset's machine and the published measurements: a pick of about half a microsecond, a 2.4 µs switch, hundreds of switches a second per CPU, seconds per answer (2026-10-09)
> Amended by D55 (the four values outside the 5 % rule leave the campaign's list, by 인지오's decision; kept in `results.md` as observed ranges).
> Amended by D56 (the pick: the fair-class pick, about 0.45–0.54 and 0.54–0.63 µs less the tracer's share read in the scheduler; traced values upper bounds).
> Amended by D57 (others' switch costs: Li, Ding & Shen's regions as measured, Becker & Chakraborty's frequent ~30 000 cycles, ghOSt's patched kernel).
> Amended by D58 (the switch rates over the pooled repeats: 13 to 12 497 a second, median phase 422, 13 of 67 at 1 000 or more; switches as a lower bound on picks).
> Amended by D59 (the ratio with one denominator: four to eight orders, six to seven on the laptop; the 8B on one input; :241; hand-off extended).
> Amended by D110 (the laptop figures cited as `meas-local:m1pro-llm:2026-10-08`; by 인지오's decision).

Taken under 인지오's delegation (2026-10-09), scope-card item 28, on the campaign `meas-ci:costs:2026-10-08` (D31; `campaign/results.md`; S4-11, S4-12), S3-21 and S3-22: `docs/research-proposal.md:85` ("Thousands to tens of thousands of times per second, per core. Its decision logic has a budget measured in microseconds"), the §4.1 table (`:233–241`: decision "~1-10 microseconds", context switch "~1-5 microseconds", time slice "~1-10 milliseconds", one LLM inference "~200-3000 milliseconds", "5-6 orders of magnitude slower"), `:243` ("In the time it takes to answer once, the scheduler has made hundreds of thousands of decisions"), `:204` ("scheduling decisions happen tens of thousands of times per second and inference cannot"), `:818` ("Costs 1–5 μs and discards cache locality") and `:848` ("Typically 1–10 ms") are restated to what was measured.

- **The pick** (job `kernel`, 19 repeats on the EPYC 7763, kernel 6.17.0-1022-azure): `pick_next_task_fair` — the fair class's selection with its put-previous and set-next bookkeeping (`kernel/sched/fair.c:8771` at v6.17) — traced per call, median 795.6 ns ±0.64 % under the ping-pong and 892.0 ns ±2.14 % under 80 messaging processes on one CPU; the selection alone (`pick_task_fair`) 493.3 ns and 547.8 ns. Inside its two timestamps the tracer adds what the calibration reads: `__task_pid_nr_ns`, getpid's whole work, 260.9 ns traced. Less that, the pick is about 535 and 631 ns and the selection about 232 and 287 ns — the subtraction also removes the calibration function's own few tens of nanoseconds, so these lean low, and the traced values are upper bounds. Its whole cost per call (traced minus untraced) is 929 ns, so the tracer hides no larger cost.
- **The switch:** lmbench `lat_ctx` 2.38 µs ±1.17 % (0 KB per process), 2.42 µs (16 KB), 2.44 µs (64 KB); the pipe ping-pong 6.454 µs a round trip, the self pipe 0.814 µs a write+read pair, so 2.41 µs ±0.98 % a switch with its wakeup, Li, Ding & Shen's subtraction; `perf bench sched pipe` 5.63 µs a round trip. Others measured 599 ns (ghOSt, Table 3: a Xeon Platinum 8173M, Linux 4.15; S1-01), 3.8 µs direct (Li et al.: a 2.0 GHz Pentium Xeon, Linux 2.6.17; S1-21) and at least 3 400 cycles (Becker & Chakraborty, Sandy Bridge, Linux 3.16; S1-23); Li et al. measured the total with cache refill at 4.2–8.7 µs for 1–200 KB working sets and up to over 1 000 µs at the largest.
- **How often:** on one CPU running one of the dataset's programs, 12 to 12 447 context switches a second, the median program 437; 13 of 71 program phases at 1 000 or more, 2 at 10 000 or more, both SteamCMD's download (S3-21). The runner at idle switches 320 times a second over its four CPUs (±3.5 %).
- **The slice:** Linux's base slice 0.70 ms × (1 + log₂ of the CPUs, up to 8) since v6.15, 2.1 ms on the runner's four CPUs; `SCHED_RR` 100 ms on the runner (9.11 D2, D23); scx_lavd 0.5–5 ms with a boost to 500 ms, scx_rusty 20 ms or 1 ms (9.11 D31); MLFQ variants "10 or fewer milliseconds" at the top and "100s of ms" at the bottom (OSTEP §8.5), Solaris's TS table 20 ms to a few hundred (OSTEP p. 9).
- **One answer** (D51): a recognizer-shaped request of 437–454 prompt tokens, answered in 1.19 s (Qwen2.5-3B, the `system` block) to 5.34 s (Llama 3.1 8B, reasoning first) on an Apple M1 Pro with Metal (S3-22); 14.1–43.4 s on the runner's four vCPUs, CPU only (S4-12); AKTS reports a median of 13.5 ms for a single-digit answer from Qwen2.5-0.5B on an A100 (S1-32, §4.2: "median decision latency is 13.5 ms (n=30, temperature 0)").
- **The ratio** (arithmetic): an answer over a pick — 1.19 s / 0.8 µs ≈ 1.5 × 10⁶ on the laptop; 13.5 ms / 0.8 µs ≈ 1.7 × 10⁴ for AKTS's 0.5B model on a datacenter GPU; 43.4 s / 0.53 µs ≈ 8 × 10⁷ on four server vCPUs. Four to eight orders of magnitude across the settings measured, about six on a consumer laptop.
- **Decisions during one answer** (arithmetic): during the laptop's 1.19 s answer, one CPU running the median program switches about 520 times, running SteamCMD's download about 14 800 times; a machine has several CPUs.
- **Restated:** `:85` — the scheduler runs hundreds to thousands of times a second on each CPU, more under some loads (the measured range above), and each pick takes about half a microsecond on the dataset's machine; the §4.1 table's rows replaced by the measured values with their machines, the LLM row by the measured answers; "5-6 orders" → four to eight orders across the settings measured, about six on a consumer laptop; `:243` → the arithmetic above; `:204` → "hundreds to thousands of times a second per CPU"; `:818` → about 2.4 µs on the dataset's machine, 0.6–3.8 µs on others' measured, more with the cache state it refills (D32); `:848` → the per-system slices above. The conclusion the table supports — the LLM cannot sit in the decision path — stands, on four to eight orders of magnitude instead of five to six.
- **Outside the rule** (the workflow's exception for a value whose spread follows the machine, not the program; no stated quantity rests on them): the measured CPU's idle switch rate, 61–108 a second, and its schedule() calls, 117–567 a second (the runner's agent and timers share the CPU); the idle-path pick median, 481–902 ns, and newidle balancing's mean, 471–842 ns (the other CPUs' runqueues) — carried with their ranges over the 19 repeats.

Hands to 9.15: `docs/research-proposal.md:85`, `:204`, `:233–243`, `:818`, `:848` restated as above; `docs/references.md` — the campaign `meas-ci:costs:2026-10-08` as a measurement entry (its tag, runs and pooled record), and Li, Ding & Shen (ExpCS 2007), Becker & Chakraborty (arXiv 1811.01412v2) and ghOSt's Table 3 where the prose cites them, under the id-minting rule.

Compiled effect: none.

## D51 — local inference latency restated to the measured answers: about 1–3 s for the `system` block on a consumer laptop, 14–36 s on four server vCPUs; "well under the hosted-API figures" and "substantially faster" leave; "a handful of times per hour" stated as an assumption (2026-10-09)
> Amended by D59 (the 8B's runner answer on one input: 43.18 s, reasoning 6.81 s) and D60 (one M1 Pro, one stand-in request, the answer stops at system).
> Amended by D107 (the published figures as their pages compute them: Artificial Analysis's per-provider 72-hour medians, LocalScore's 12 GB RTX 3060 mean over submitted runs).
> Amended by D110 (the laptop figures cited as `meas-local:m1pro-llm:2026-10-08`, their records released with the hostname removed; by 인지오's decision).

Taken under 인지오's delegation (2026-10-09), scope-card item 29: `docs/research-proposal.md:263`'s "A quantized 3–8B model running locally emits a short structured output in roughly 200–800 ms on consumer hardware, well under the hosted-API figures usually quoted. Since the model fires only when the process set changes materially — a handful of times per hour in real use — local inference is the realistic deployment shape", and `:489`'s "local inference is substantially faster on short structured outputs", are restated to the project's measurements.

- **On a consumer machine** (S3-22: an Apple M1 Pro, 16 GB, Metal, llama.cpp at `bd4eeaa0`; five repeats of five requests): the stand-in recognizer request (437–454 prompt tokens, `dataset/tools/meas/llm/prompt.json`) answered with the `system` block in 1.19 s (Qwen2.5-3B Q4_K_M; prompt 0.73 s, 25 tokens 0.46 s) and 2.95 s (Llama 3.1 8B Q4_K_M; 1.91 s, 26 tokens 1.04 s); with `reasoning` and `situation` first, 2.25 s and 5.34 s.
- **On the dataset's machine, CPU only** (S4-12: four vCPUs of the EPYC 7763, AVX2; 11 repeats): `system` 14.10 s ±0.40 % (3B) and 36.39 s ±0.31 % (8B); reasoning first 17.48 s and 43.43 s. Reading the prompt is most of each: 12.5 s and 32.7 s.
- **Elsewhere:** on an A100, AKTS's Qwen2.5-0.5B answers a single digit in a median 13.5 ms (S1-32); LocalScore's crowd-submitted runs of Llama 3.1 8B Q4_K_M give an RTX 3060's average time to first token as 0.88 s, averaged over nine tests of 16–4 096 prompt tokens (S3-05). No hosted API was measured; the one hosted figure found is a ~10 000-token prompt's 0.84 s to first token on Groq (S3-18).
- **What leaves:** "roughly 200–800 ms on consumer hardware" — neither measured machine reaches it at this prompt length, the laptop's fastest answer 1.19 s; "well under the hosted-API figures usually quoted" and "substantially faster" — no measurement compares them.
- **What stands:** the deployment reason that needs no latency — the process list never leaves the machine (`:489`); and the latency's place in the experiment: the daemon stamps each configuration late by the recognition latency it measured (`docs/data-contracts.md` §6), so these seconds enter the results as measured.
- **"a handful of times per hour in real use"** has no source: how often a desktop's process set changes is not measured by any source found (only foreground-window switching, S3-12, S3-16), and the dataset's timelines are built around their transitions — 2–5 set changes in files of 17 s to 3.4 h, three in each of the longest (`c1-transcode`, 79 min; `c6-dual`, 3.4 h). It is stated as an assumption of the deployment shape.
- **Restated `:263`:** a quantized 3–8B model running locally answers a recognizer-shaped request in about 1–3 s for the `system` block on a consumer laptop (2–5 s with reasoning first) and in 14–36 s on four server vCPUs without a GPU; since the model is consulted only when the process set changes — assumed to be rare in real use — a latency of seconds delays a configuration, not a scheduling decision.

Hands to 9.15: `docs/research-proposal.md:263`, `:489`'s latency clause, restated as above; `docs/references.md` — the campaign entry (D50) and LocalScore (S3-05) where the prose cites them. **9.14:** the RQ4 latency figures and the daemon's latency stamping read these measurements; the reasoning field's cost — 1.06 s on the 3B and 2.39 s on the 8B on the laptop, 3.4 s and 7.0 s on the runner — is RQ4's "latencies measured with reasoning included" (`:742`).

Compiled effect: none.

## D52 — determinism at temperature 0 restated to what was observed: byte-identical answers to the same input on the same hardware; longer answers differ across hardware; Llama 3.1's template puts the day into the input (2026-10-09)
> Amended by D60 (comparisons per prompt; the 8B's system answer unchanged across days; the EPYC 9V45 as the dry run's observation).

Taken under 인지오's delegation (2026-10-09), scope-card item 44: `docs/research-proposal.md:740`'s "Local inference with a fixed seed and temperature 0 reduces it substantially" (non-determinism) is restated to the project's requests and the literature.

- **On one hardware type** (S3-22, S4-12; temperature 0, seed 1, `cache_prompt` false, one request at a time): every model, schema and prompt gave one byte-identical answer — across the five requests of a server, across the five restarts on the M1 Pro, and across the 11 separate runner VMs of the EPYC 7763 (9 on one prompt and 2 on the other, below).
- **Across hardware types** (the same prompt bytes): the short `system` answers were identical on the M1 Pro's Metal GPU, an EPYC 9V45 and the EPYC 7763, for both models; the longer answers with reasoning first were not — the 3B gave three texts on the three, each deciding `gaming`, `false`; the 8B's text was identical on the EPYC 9V45 and the EPYC 7763 for one prompt, and on the other differed between the M1 Pro and the EPYC 7763 in its decision: `background_wanted` `false` on the M1 Pro, `true` on the EPYC 7763.
- **The day in the input:** Llama 3.1's chat template, as llama.cpp applies it, writes "Today Date: 08 Oct 2026" or "09 Oct 2026" into the system header; the repeats on either side of midnight UTC read different prompts of the same length and answered with different texts (79 and 71 tokens). The server takes `chat_template_kwargs` per request (S2-59, `:216`, `:1346`); whether the template's date can be pinned through it is not checked.
- **The literature:** "Run-to-run determinism on a single device is typically guaranteed, but nothing constrains two different architectures to select the same kernel" (S1-36, Cooper et al., §2); serving non-determinism from batch composition (He and Thinking Machines Lab 2025, as S1-36 reports it); llama.cpp's own warning that the prompt cache can make results non-deterministic (S2-59); served models at temperature 0 with a fixed seed varied in accuracy by up to 15 % across runs (S1-25, Atil et al.).
- **Restated:** at temperature 0 with a fixed seed, local inference one request at a time returned the same answer to the same input on the same hardware, so Layer 1's consistency measure on one machine reads what changes in the input, not sampling noise; answers can differ across hardware and under batched serving, and an input that carries the day changes from one day to the next. The record/replay cache (§4.8) holds the answers fixed for the experiment.

Hands to 9.15: `docs/research-proposal.md:740` restated as above; `docs/references.md` entries for Cooper et al. (S1-36) and Atil et al. (S1-25) where the prose cites them. **9.14 and 박이안:** the recognizer's prompt fixes or records what its chat template inserts — Llama 3.1's "Today Date" — so the same snapshot is the same input on every day, and the recognition log keeps the formatted prompt; Layer 1's consistency measure states its hardware.

Compiled effect: none.

## D53 — vol-02's quotations read against their sources: 239 of 278 exact, none missing; the corrections listed for 9.15 (2026-10-09)
> Amended by D97 (277 passages by its own rule: 238 exact, 39 differ; `:1032`, `:949`, `:582`, `:1967`) and D98 (the copies: two record copies replaced by fixed captures; the ghOSt repository entry).

Taken under 인지오's delegation (2026-10-09), scope-card item 60: every block-quoted source passage in `docs/guidebook/vol-02-related-work.md` (278 lines: 92 in chapters 2–3, 134 in 4–6, 52 in 7–8; the guidebook's own callouts excluded) was compared word for word with a copy of its source (`search/V60-vol02-quotations.md`, three readers' reports verbatim). Every copy equals its record's SHA-256 except two live pages whose quoted text is unchanged — Nielsen's NN/g excerpt and Microsoft's Game Mode concept page. Spot-checked here: the Kgent table row, the Park and Kgent omissions, the ghOSt order and Miller's count, each confirmed in the copy.

- **Counts:** exact 239 (84, 103, 52); differs 38 (8, 30, 0) — 27 of them only drop citation or cross-reference markers without an elision mark; locator wrong 1 (line 1967); not found 0. Seven code-block passages in chapter 7 are exact, the ananicy-rules type file at `:2944–2990` identical to the source by `diff`.
- **Substantive corrections:**
  - `:1080` (ghOSt §4.4, p. 599) — two sentences joined in reverse source order behind an elision that also hides "(i.e., within 10%)".
  - `:582` (EEVDF TR, p. 3) — "virtual dead line" for "virtual deadline".
  - `:1867` (Park) — drops "(affecting job runtime in the rewards)" without a mark.
  - `:2579` (Kgent) — "the comprehension and symbolic execution component" for "the comprehension engine and symbolic execution component".
  - `:2568` (Kgent, Table 1) — the human-expertise row's columns swapped: the source reads accuracy 72.5 %, false positive 2.5 %, false negative 25 %; the guidebook shows 72.5 % as failed-to-produce and 25 % as accuracy (the paper's prose agrees with its table: Kgent's 80 % beats the human baseline).
  - `:1967` — introduced as ASA's first sentence, it runs into the second.
- **Claims around the quotes:**
  - `:558` — "lag" is not in the EEVDF introduction: it is defined in §2 (p. 4), virtual time formally in §3 (p. 6).
  - `:674` — Miller has seventeen topics, not eighteen ("The seventeen types of response category and response time", p. 269).
  - `:2209`, `:2674` — SchedCP's journal-reference field reads "MLforSystem 2025", not "ML for Systems 2025" (D25).
  - `:2211` — "went back" to a short form is unsupported: v1 and v2 are the same 8-page manuscript, v3 and v4 6 pages, with no earlier short version.
  - `:2791–2797`, `:3174` — the Windows Update question stated as unconfirmed; D45 settled it (S2-58).
  - `:3421` — "nine" Procyon benchmarks; the page lists ten, one of them "AI Inference Benchmark for Android".
  - Nuances: `:865` (the abstract's first two sentences), `:1116` (five bullets in `sched-ext.rst`, not four), `:1208` (each scx README's Overview line, after a shared first line), `:696` (the Nielsen chapter title not in the copy, the registry already marking it); `:875` duplicates `:873`.
- **Small corrections:** `:1048` prints "RocksDB" where ghOSt has "RockDB" (a [sic] or the source's spelling); `:1339`, `:1571`, `:1757`, `:1851`, `:2395`, `:2551` — a joined heading, cut clauses and figure references, a capitalised "We" (the report's rows give the source text); the marker drops at `:887`, `:925`, `:931`, `:949`, `:993` and the 22 listed for chapters 4–6 — an elision mark where the guidebook elides, as it does at `:600`.
- **Registry points from the read:** `gamemode-docs` gains the `ReleaseExclusiveCpuSets` page, the source of `:2777` ("After this function is called, the app will still have access to other Game Mode resources, such as increased GPU prioritization.") — S2-16 copied the concept and header pages and two function pages, not it; `hackbench` — vol-02 cites HEAD `fd45df83`, the registry pins tag v2.11 (`62da2bef`), the quoted files byte-identical at both; `rt-app` — `:3299` comes from `README.in`, a file the entry's cite does not list. SchedCP's version marking holds throughout (every unmarked quote in v4; every long-version quote in v2 only).

Hands to 9.15: `docs/guidebook/vol-02-related-work.md` — each line above corrected to its source as the report's row gives it; `docs/references.md` `gamemode-docs` (the fifth page), `hackbench` (the version vol-02 names), `rt-app` (`README.in`).

Compiled effect: none.

## D54 — batch: hand-off pointers (2026-10-09)

Taken under 인지오's delegation (2026-10-09), stage 4: every decision's hand-off reaches its task through `_dev/TODO.md`, as 9.11 D33 did.

- **9.14** — D6's condition split where the harness freezes the condition list (the two identifiers chosen there; the build of the two rule lists has no phase yet); D40's question whether Layer 1 pre-registers the recognizer with and without `reasoning`; D51 and D52's measured latencies for RQ4 and the daemon's stamp, the consistency measure's hardware, and the chat template's inserted date, with 박이안.
- **9.15** — every decision's "Hands to 9.15": the restatements of `docs/related-work.md` and `docs/research-proposal.md` by section, `whitelist` across the docs (D6), the workload docs' lines (D11, D45–D47), `docs/simulator/simulator-guide.md:210` (D30), the registry entries minted and restated, the guidebook lines each decision names, and vol-02's quotation corrections (D53).
- **The inputs on 9.12's own line**, answered: 9.6 D32's training-run wording (D14), 9.6 D17's `updatedb` sentence (D13), 9.11 D19's starvation lines (D30), 9.11 D33's declared-class survey (D13, D49).
- **The campaign** `meas-ci:costs:2026-10-08` is in `measurement-campaign-record.md`; its raw records released on 인지오's go-ahead (2026-10-09) as the GitHub release `meas-ci-costs-2026-10-08` at `ab379f2e`: the 30 pooled repeats, the three dry-run jobs and the 66 gated jobs' reports, 34 archives.

Applied: `_dev/TODO.md` — the 9.14 and 9.15 lines.

Hands to: as listed.

Compiled effect: none.

## D55 — the four values D50 carried outside the 5 % rule leave the campaign's list: the measured CPU's idle switch and schedule() rates, the idle-path pick median and newidle balancing's mean, kept in `results.md` as observed ranges (2026-10-09)

By 인지오's decision (2026-10-09), amending D50 (scope-card item 28) and D31's campaign method, on the 9.12 audit's re-pool of `meas-ci:costs:2026-10-08` (A1-01, A1-02). D50 carried four values "with their ranges over the 19 repeats" under the workflow's exception for "a value whose spread follows the machine, not the program", which is taken "by 인지오's decision per value, recorded in the slice's changelog, and only for a value that carries none of the effects the slice reports", with "Its 95 % half-width, observed range and repeat count, the part of the machine its spread follows, and the share of the job's time the quantity holds" stated and "when it was taken and the pool's projection" recorded (`measurement-campaign-workflow.md:29–30`).

- **The four** (`campaign/results.md`, 19 repeats; half-width, observed range, the pool's projection): `idle.cs_per_s.measured_cpu` ±7.96 %, 61.0–108.3 a second, 45 repeats; `idle.schedule_per_s.measured_cpu` ±18.39 %, 117.1–567.2 a second, 227; `pick_next_task_fair.sleep.median_ns` ±7.81 %, 481–902 ns, 43; `sched_balance_newidle.sleep.mean_ns` ±6.49 %, 470.8–842.5 ns, 31.
- **What rests on them:** no quantity D50–D52 state. The pick is read under the ping-pong and messaging loads; the idle switch rate stated is the four CPUs' sum, 319.8 a second ±3.54 %, within the rule (A1-02).
- **Decided:** the four leave the campaign's list by a dated amendment to its method; `results.md` keeps them as observed ranges, not carried values. The exception is not taken. D50's "Outside the rule" bullet leaves.

Applied: `campaign/method.md` — an Amendments section, the list without the four; `campaign/results.md` — a note naming the four as observed only; `measurement-campaign-record.md` — the 9.12 `kernel` row.

Hands to: none.

Compiled effect: none.

## D56 — D50's pick restated: the fair-class pick `pick_next_task_fair`, about 0.45–0.54 µs under the ping-pong and 0.54–0.63 µs under 80 messaging processes once the tracer's share is taken out; the traced values are upper bounds (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D50 (scope-card item 28) on the 9.12 audit's re-pool of `meas-ci:costs:2026-10-08` from its release and its reading of the traced calls (A1-01–A1-03, A1-06). D50 said: "Less that, the pick is about 535 and 631 ns and the selection about 232 and 287 ns — the subtraction also removes the calibration function's own few tens of nanoseconds, so these lean low, and the traced values are upper bounds. Its whole cost per call (traced minus untraced) is 929 ns, so the tracer hides no larger cost."

- **The re-pool:** the release's 34 archives match GitHub's digests; its 30 pooled job folders are byte-identical to the loop's copies; `pool.py --cpu-model "EPYC 7763"` over the release gives `pool.txt` lines 1–68 and `pooled.json`'s `jobs` unchanged (A1-01, A1-02). Every value D50 states from the campaign stands as pooled.
- **What the two timestamps hold** (A1-06): the function-graph tracer takes `calltime` on entry (`kernel/trace/trace_functions_graph.c:255` at v6.17) and `rettime` as the first statement of the return handler (`:356`), so the duration of every traced call holds the same in-bracket tracer work plus the function's body. The subtraction assumes that in-bracket share is the same for the calibration call and for the pick.
- **The in-bracket share read inside the scheduler** (A1-03): in the sleeper pass, a `pick_task_fair` call followed by a switch to `<idle>` returned at its first test — "`if (!cfs_rq->nr_queued) return NULL;`" (`kernel/sched/fair.c:8747–8748` at v6.17) — and its traced median is 340–351 ns across the 19 repeats (mean of the repeat medians 349.3 ns), against the getpid-path calibration's 260.9 ns. A near-empty call inside the scheduler reads about 90 ns more than the calibration; the subtraction of 260.9 ns does not lean low.
- **The whole cost per call** (`pick_next_task_fair.pingpong.tracer_ns_per_call` 929.1 ns, `__task_pid_nr_ns.getpid.tracer_ns_per_call` 576.1 ns; `campaign/results.md`) exceeds the traced duration it would bound (795.6 ns) and differs between the two contexts by 353 ns; it bounds nothing about the pick.
- **The pick, both subtractions** (arithmetic): under the ping-pong 795.6 − 349.3 = 446 ns to 795.6 − 260.9 = 535 ns; under 80 messaging processes 543 to 631 ns. The selection alone (`pick_task_fair`): 144–232 ns and 199–287 ns. The put-previous and set-next bookkeeping, both traced under the same load: 795.6 − 493.3 = 302 ns and 892.0 − 547.8 = 344 ns. The traced medians, 795.6 and 892.0 ns, are upper bounds.
- **What the pick is** (A1-06): `pick_next_task_fair` (`fair.c:8771`) is the fair class's pick — `pick_task_fair`'s EEVDF selection, the put-previous and set-next walk under group scheduling, and `sched_balance_newidle` when nothing is runnable — called directly from `__pick_next_task` (`kernel/sched/core.c:6001`) when every runnable task is in the fair class. It is not the whole of `__schedule` (the runqueue lock, the clock update, dequeuing the blocking task, `context_switch`) and not the scheduler's other choices, made outside `__schedule`: the wakeup's CPU (`select_task_rq_fair`), the wakeup preemption check (`check_preempt_wakeup_fair`), the tick (`task_tick_fair`).
- **Restated** (D50's "The pick" bullet and the §4.1 table's decision row, `docs/research-proposal.md:233`): the fair class's pick of the next task (`pick_next_task_fair`), traced per call on the dataset's machine, 0.80 µs under the ping-pong and 0.89 µs under 80 messaging processes, upper bounds; less the tracer's share — 0.26 µs read from the calibration call in a getpid loop, 0.35 µs from a near-empty call on the scheduler's idle path — about 0.45–0.54 µs and 0.54–0.63 µs — about half a microsecond. The EEVDF selection inside it is 0.14–0.29 µs. The row is labelled as the fair-class pick; the rest of a context switch is the switch row's.
- **Noted:** `dataset/tools/meas/costs/graph_durations.py:10` names the calibration `__x64_sys_getpid`, the function D31's dry run found untraceable; `run.sh:114` traces `__task_pid_nr_ns`, as `campaign/method.md` and the results state.

Hands to 9.15: `docs/research-proposal.md:85`'s "Its decision logic has a budget measured in microseconds" and the §4.1 table's decision row (`:233`) restated as above.

Compiled effect: none.

## D57 — the context switch's cost as others measured it: Li, Ding & Shen's three regions attributed as measured, Becker & Chakraborty's frequent value beside their minimum, ghOSt's 599 ns on its patched kernel (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D50 and D32 (scope-card items 28 and 31) on the 9.12 audit's re-read of S1-21, S1-23 and S1-01 from copies byte-identical to their records (A1-12). D50 said: "Others measured 599 ns (ghOSt, Table 3: a Xeon Platinum 8173M, Linux 4.15; S1-01), 3.8 µs direct (Li et al. …) and at least 3 400 cycles (Becker & Chakraborty …); Li et al. measured the total with cache refill at 4.2–8.7 µs for 1–200 KB working sets and up to over 1 000 µs at the largest"; D32: "4.2–8.7 µs for working sets of 1–200 KB and 38.6–203.2 µs at 256–512 KB, past 1 000 µs at the largest … by an amount that grows with its working set"; D31 and D50 quote S1-23 as "at least 3 400 cycles" only.

- **Li, Ding & Shen** (S1-21, `expcs2007.pdf`, §3.1–§3.2, pp. 2–3): sequential access, three regions — from 1 KB to about 200 KB, "context switch times ranging from 4.2µs to 8.7µs. This is because the entire dataset … can fit into the L2 cache, and the context switch does not cause any visible cache interference"; from 256 KB, where each process's data fits the 512 KB L2 cache but the combined dataset does not, "from 38.6µs to 203.2µs"; from 512 KB, "the curves do not increase monotonously with the array size". The figure past 1 000 µs is the stride experiment's (§3.2, arrays of 32 KB–2 MB): "When the access stride is 128B, the cost ranges between 133.8µs and 1496.1µs with the mean 825.3µs" — "the data access pattern can affect the cost of context switch significantly". Direct cost "3.8 microsecond" (p. 2; dual 2.0 GHz Pentium Xeon, Linux 2.6.17).
- **Becker & Chakraborty** (S1-23, `becker-1811.01412v2.pdf`, §2.2.2, p. 7): "Using lmbench, we found that context switches on our system take at least 3,400 cycles, with a frequent value around 30,000 cycles" (Table 1, p. 2: i7-2640M at 2.8 GHz, Sandy Bridge, Linux 3.16.51-3) — at the nominal 2.8 GHz about 1.2 µs and 10.7 µs (arithmetic).
- **ghOSt** (S1-01, Table 3, printed p. 596, "CFS Context Switch Overhead 599 ns"; printed p. 595: "experiments run on Linux 4.15 with our ghOSt patches applied", Xeon Platinum 8173M at 2 GHz).
- **Restated D50** (the switch bullet's "Others measured"): others measured 599 ns (ghOSt's CFS on its patched Linux 4.15) and 3.8 µs (Li et al., direct, Linux 2.6.17) for the switch itself, and Becker & Chakraborty's lmbench runs at least 3 400 cycles with a frequent value around 30 000 (Linux 3.16); with its cache effects, Li et al. measured 4.2–8.7 µs while the data fit the L2 cache, 38.6–203.2 µs once the two processes' data no longer did, and up to 1 496 µs with a 128-byte stride. **`:818`** → about 2.4 µs on the dataset's machine, 0.6–3.8 µs for the switch itself and a frequent value near 10 µs on others' machines, more with the cache state it disturbs.
- **Restated D32** (the cost of interruption): each switch costs the switch itself and the cache state the program built, by an amount that depends on whether its data still fit the cache and on its access pattern (Li et al.: 4.2–8.7 µs in cache, 38.6–203.2 µs beyond it, up to 1 496 µs with a 128-byte stride).

Hands to 9.15: `docs/research-proposal.md:111` and `:818` restated as above; `docs/references.md` — Li, Ding & Shen and Becker & Chakraborty cited with both figures where the prose cites them.

Compiled effect: none.

## D58 — the switch rate per CPU over the repeats each slice pooled: 13 to 12 497 a second, the median program phase 422; the switches during one answer as switches, a lower bound on picks (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D50 (scope-card item 28) and the search record S3-21 on the 9.12 audit's re-run of S3-21 restricted to the pooled repeats (A1-07). D50 said: "on one CPU running one of the dataset's programs, 12 to 12 447 context switches a second, the median program 437; 13 of 71 program phases at 1 000 or more, 2 at 10 000 or more, both SteamCMD's download (S3-21)"; and "during the laptop's 1.19 s answer, one CPU running the median program switches about 520 times, running SteamCMD's download about 14 800 times". S3-21 (Method) kept every gate-open, full-mode EPYC 7763 phase file on disk, 1 806 over 509 runs.

- **The selection:** 594 of the 1 806 full-mode files are outside the repeat lists the owning slices pooled — 541 from superseded campaigns or replaced phases (9.5 D55, D65, D72, D79–D80; 9.7 D3; 9.10 D146, D152), 31 left out by a slice's validity check or as a duplicate landing (borg's repeat 3 and Déjà Dup's repeats 12 and 25, their sets fetched as a 12 KB page, 9.10 D125 for Déjà Dup; SteamCMD repeats 21, 32, 33, 9.7 D27, D32, D33; 9.5 D66's twice-landed windows), 22 landed but not pooled (9.10 D75's Tracker batches; 9.6 D27's `clamscan` repeats 4–8; 9.6 D28's `train` repeats 4–10); 16 idle-mode files come in (Kdenlive's re-measured idle phase, 9.10 D146). Every pooled (run, repeat) pair is on disk.
- **The madvise check** leaves the count: 9.10's MNIST check under the desktop kernel's `madvise` mode is "never a repeat" (`measurement-campaign-record.md:545`), pooled apart (9.10 D87, D88).
- **Restricted** (A1-07): 67 program phases over 1 223 phase files; group medians from 12.9 (single-threaded MNIST training) to 12 497.2 a second, the median phase 422.0 (`mpv-audio/play`); 53 phases at 100 or more, 13 at 1 000 or more — the same 13 as recorded — and 2 at 10 000 or more, SteamCMD's shaped fresh install traced (11 094.5) and untraced (12 497.2).
- **The counting rule** holds (A1-07): `perf sched timehist` prints one row per `sched:sched_switch` event (`tools/perf/builtin-sched.c` at v6.17), the event fires only when the outgoing and incoming task differ, where `rq->nr_switches` counts (`kernel/sched/core.c`), so a CPU's rows are its context switches, those to and from `<idle>` included; over all 2 195 files every matched line is a switch row and no "lost events" line appears. A schedule() call that keeps the same task is not a row, so a switch is a lower bound on picks.
- **Switches during one answer** (arithmetic): in the M1 Pro's 1.19 s answer (S3-22), one runner CPU running the median program phase switches about 500 times, running SteamCMD's download about 14 900 times — each switch at least one pick; the answer is the laptop's and the rates the runner's.
- **Restated D50 "How often":** on one CPU running one of the dataset's programs, 13 to 12 497 context switches a second over the repeats each slice pooled, the median program phase 422; 13 of 67 program phases at 1 000 or more, 2 at 10 000 or more, both SteamCMD's download, traced and untraced (S3-21, restricted). The runner at idle switches 320 times a second over its four CPUs (±3.5 %).
- **S3-21's busy shares** are over whole phase files, harness time included; restricted to the pooled repeats, `clamscan` 0.9334–0.9435 over 10 repeats and `train` 0.8475–0.8575 over 8; the other seven lines unchanged (A1-08).

Applied: `search/S3-traces-datasets.md` — S3-21 gains a "Restricted (9.12 audit, 2026-10-09)" note: the selection above, the restricted output (A1-07) and busy shares (A1-08), the phase-file denominator. The record's own lines stay as read.

Hands to 9.15: `docs/research-proposal.md:85` and `:204` ("hundreds to thousands of times a second per CPU") and `:241` as above.

Compiled effect: none.

## D59 — the answer over the pick with one denominator and one input: four to eight orders of magnitude, six to seven on the laptop; Llama 3.1 8B's runner answer on the comparable prompt, 43.2 s; D50's hand-off extended (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D50 and D51 (scope-card items 28 and 29) on the 9.12 audit's re-pool and its split of the 8B's runner repeats by prompt (A1-04). D50 said: "an answer over a pick — 1.19 s / 0.8 µs ≈ 1.5 × 10⁶ on the laptop; 13.5 ms / 0.8 µs ≈ 1.7 × 10⁴ for AKTS's 0.5B model on a datacenter GPU; 43.4 s / 0.53 µs ≈ 8 × 10⁷ on four server vCPUs. Four to eight orders of magnitude across the settings measured, about six on a consumer laptop"; D51: "reasoning first 17.48 s and 43.43 s", and the reasoning field's cost "3.4 s and 7.0 s on the runner".

- **The 8B's two inputs** (A1-04): `pool.py` pools the `llama3.1-8b` values per model; repeats 6 and 8 read "Today Date: 08 Oct 2026" and the other nine "09 Oct 2026" (`campaign/results.md`). The nine on the 9 Oct prompt — byte-identical to the M1 Pro's (prompt SHA-256 prefix `b765936ca9` on both, A1-05) — give reasoning first 43.18 s ±0.43 % (71 tokens, generation 10.50 s ±1.67 %) and `system` 36.37 s ±0.35 %, each within the stability rule over nine; repeats 6 and 8, 44.34 s and 44.75 s (79 tokens). The workflow's "identical work" leaves repeats 6 and 8 out of the 8B's figures: the runner's 8B answers are 36.37 s (`system`) and 43.18 s (reasoning first); the reasoning field's cost 6.81 s; the 3B's unchanged (14.10 s, 17.48 s; 3.39 s).
- **One denominator:** the pick under the ping-pong, 0.45 µs (less the scheduler-side tracer share) to 0.80 µs (traced), D56. Each ratio is an answer on its machine over a pick on the runner (arithmetic): the M1 Pro's 1.19 s (3B, `system`) 1.5–2.7 × 10⁶ and 5.34 s (8B, reasoning first) 6.7 × 10⁶–1.2 × 10⁷; AKTS's 13.5 ms on an A100 1.7–3.0 × 10⁴; the runner's 14.10 s 1.8–3.2 × 10⁷ and 43.18 s 5.4–9.7 × 10⁷. 4.2 to 8.0 orders of magnitude across the settings measured; 6.2–7.1 on the laptop.
- **Locator:** "In the time it takes to answer once, the scheduler has made hundreds of thousands of decisions" is `docs/research-proposal.md:241`, not `:243`.
- **The slices** (D50's slice bullet): Solaris's TS table, 20 ms at the top to a few hundred at the bottom, is OSTEP's description (p. 9) of the table at a 100 Hz clock; the illumos table at the default 1 000 Hz clock gives 2–20 ms (`docs/references.md:327`). It is stated as OSTEP describes it.
- **Restated D50 "The ratio":** an answer on each machine over a pick on the dataset's machine — four to eight orders of magnitude across the settings measured, six to seven on a consumer laptop; the conclusion the table supports — the LLM cannot sit in the decision path — stands. **D51:** "reasoning first 17.48 s and 43.18 s"; the reasoning field's cost on the runner 3.4 s and 6.8 s.
- **D50's hand-off extended** to the same quantities elsewhere: `docs/research-proposal.md:204`'s "five to six orders of magnitude" (with its rate, already handed), `:220` (RQ4: "LLM inference takes hundreds of milliseconds to seconds. Scheduling decisions take microseconds"), `:293` (the diagram's "scheduling loop (1000s/sec)"), `docs/background-guide.md:24` ("hundreds of thousands of times per second, in microseconds … five to six orders of magnitude, and it will never close"), `docs/research-claims.md:232–233` ("five to six orders of magnitude slower").

Hands to 9.15: the lines above restated as D50 and this entry state them. **9.14:** `dataset/tools/meas/costs/pool.py` keys the LLM values by the formatted prompt's hash if the campaign is re-pooled; the RQ4 figures read 43.18 s and 6.81 s for the 8B on the runner.

Compiled effect: none.

## D60 — the latency and determinism statements bound to what was measured: one Apple M1 Pro, one stand-in request, an answer that stops at `system`; the 8B's comparisons per prompt; the EPYC 9V45 as the dry run's observation (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D51 and D52 (scope-card items 29 and 44) on the 9.12 audit's recount of every request record (A1-05). D51's restatement of `:263` says "on a consumer laptop" and "a recognizer-shaped request"; D52's restatement says "local inference one request at a time returned the same answer to the same input on the same hardware", with "(the same prompt bytes)" across hardware.

- **What was measured:** one Apple M1 Pro with Metal (S3-22), the machine's own work beside it; one stand-in request, `dataset/tools/meas/llm/prompt.json` — its own note: "Not the project's recognizer prompt" — of 437 (3B) and 454 (8B) prompt tokens, one snapshot (`c2-p2a` at 60 s, nine process names); no recognizer prompt exists in the repository to measure instead. The "full" schema (`schema.full.json`) carries `reasoning`, `situation` and `system`; the proposal's `subsystems` block (`docs/data-contracts.md` §6) is not in it, so the answers measured stop at `system`.
- **Warm-up:** each repeat's warm-up request is labelled and left out (`pool.py`, `summarize_llm.py`); no stated latency includes a model load (S3-22: loads after repeat 1 warm).
- **Answer identity** (A1-05; temperature 0, seed 1): every (model, schema, prompt, hardware) group returned one answer — EPYC 7763: 3B `system` 66 requests, reasoning first 55; 8B `system` 12 (8 Oct prompt) and 54 (9 Oct), reasoning first 10 and 45; M1 Pro: 30, 25, 30, 25.
- **Across hardware, per prompt:** the 3B's prompt is the same bytes on the three machines: its `system` answer identical on all three, its reasoning-first answer three different texts, each `gaming`, `false`. The 8B's prompt depends on the day: the EPYC 9V45 (D31's dry run, one server start) and the EPYC 7763's repeats 6 and 8 read the 8 Oct prompt, the M1 Pro and the other nine the 9 Oct prompt; the reasoning-first answer was identical on the EPYC 9V45 and the EPYC 7763 on the first, and differed between the M1 Pro (`background_wanted` `false`) and the EPYC 7763 (`true`) on the second; the `system` answer is the same 26-token text on both prompts and all three machines.
- **The day in the input:** across the two prompts only the 8B's reasoning-first answer changed (79 and 71 tokens); its `system` answer did not.
- **The EPYC 9V45** is the dry run's observation, not a repeat ("A job on any other model measures nothing", `measurement-campaign-workflow.md`); it is stated as observed in the dry run.
- **Locators:** the daemon's latency stamp is `docs/data-contracts.md` §7 (the config schedule, `:334`), not §6; the telemetry shape `prompt.json`'s note and `campaign/method.md:19` cite as §4 is §5 (`:271`).
- **Restated D51 `:263`:** a quantized 3–8B model answered one stand-in recognizer request of about 440–450 tokens in 1.2–3.0 s for the `system` block on one consumer laptop (an Apple M1 Pro with Metal; 2.3–5.3 s with reasoning first) and in 14–36 s on four server vCPUs without a GPU; the `subsystems` block was not measured. **D52:** for the two models and the one request measured, the same input on the same hardware returned the same answer at temperature 0 with a fixed seed; the longer answers differed across hardware, and an input that carries the day changes from one day to the next.

Hands to 9.15: `docs/research-proposal.md:263`, `:740` restated as above; `:345` and `:742` ("the duty cycle is low") stated with D51's assumption; `:559` ("LLMs are non-deterministic; a single good output means nothing") restated to D52's observation. **9.14:** the latency figures carry the one-machine, one-request scope; Layer 1 measures the real recognizer prompt with its `subsystems` block.

Compiled effect: none.

## D61 — batch work restated: every measured batch job keeps a CPU busy while it works; the indexer differs by a 15 s start and its declared idle class, not by idling (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D41 (scope-card item 45) on the 9.12 audit's recount from the raw records of the repeats each slice pooled (A1-08–A1-10). D41 said: "Tracker's first index of a home, saturation 0.655–0.676 over the job, its run between voluntary blocks 1.876 ms (`file-indexer`, 9.10 D81; D14); 9.6's rescan phase kept the CPU 20.4–25.4 % busy (S3-21)", and restated "but not all: a file indexer blocks every couple of milliseconds and leaves a third of the CPU idle".

- **The indexer's job** (A1-09; 18 repeats, the pool of 9.10 D81): saturation 0.655–0.676 over the job, which opens with Tracker's shipped 15 s initial sleep — `Initializing` arrives 15.37–16.24 s into a 58.3–60.3 s job — and the dataset carries that sleep as the task's arrival (9.10 D71; `dataset/archetypes.yaml` `file-indexer`: "the initial sleep 14.40-15.23 s, carried as the task's arrival"). From `Initializing` on, the program's saturation is 0.884–0.911 (the campaign record's 0.891–0.919 divides the whole job's CPU, 0.33–0.36 s of it before `Initializing`, by the span after it). Its runs between voluntary blocks: mean 1.86 ms (the record's 1.876 ms is a mean), median 0.058 ms; 0.843–0.848 of its CPU runs past 10 ms without a voluntary block. Every thread runs SCHED_IDLE at nice 19 (9.6 D17; `file-indexer` notes).
- **9.6's rescan** (A1-08, A1-09; 14 repeats): the 20.4–25.4 % is the busy share over the whole phase file, 20.8–25.9 s, which runs to the harness's stop rule; over the job 9.6 D16 defines (the miner's first schedule-in to its own `Idle`, about 5 s) the program's saturation is 0.926–0.964, `cpu-batch`'s stated 0.925–0.964 (9.6 D37). 9.6 D16 withdrew the phase-lifetime reading.
- **The others** (A1-10): the HandBrakeCLI transcode, saturation 0.99938–0.99947 over 5 repeats (9.10 D100); Déjà Dup's incremental backup 0.99352–0.99517 over 28 (9.10 D125, repeats 12 and 25 left out); the warm `-j8` build's load CPU busy 0.9974–0.9977 over 14 (S3-21's busy share, 9.6's pool). The build's figure is the CPU's busy share over the phase, the encode's and the backup's the program's saturation over its job.
- **Restated:** batch work has nobody waiting on each step and runs long, and every batch job measured keeps a CPU busy while it works — a kernel build at 99.7 % (busy share), a video encode at 99.9 % and a backup at 99.4–99.5 % (saturation over the job), a first index of a home at 88–91 % once it starts indexing; the indexer runs short by count (median 0.06 ms between blocks) yet 84–85 % of its CPU past a 10 ms slice. What sets the indexer and the backup apart is that they declare themselves background — the indexer SCHED_IDLE at nice 19, the backup in the idle class — and the indexer waits out a 15 s start first. "consume every cycle you give them" is restated to "nearly every cycle while they work".

Hands to 9.15: `docs/research-proposal.md:97` restated as above; the glossary's "Batch process — … Consumes all available CPU" (`:814`) restated with it.

Compiled effect: none.

## D62 — the editor and the compiler stated as measured: `cc1`'s 367.6 ms runs from its start to its exit, unblocked in 99.4 % of object jobs; the per-key figures name their stimulus and their venue (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D33 and D32 (scope-card items 32 and 31) on the 9.12 audit's recount of 9.5's and 9.6's pools (A1-11). D33 said `cc1` "wakes once in 99.3 % of jobs and runs 367.6 ms of CPU at the median … before it next blocks"; D32 said "under Xvfb with no GPU, so rendering runs on the CPU (each entry's venue bound)" and "79.7 ms for VS Code, its TypeScript language server re-checking the file".

- **`cc1_step_1`** (`dataset/archetypes.yaml`, p50 367 630 µs, n 39 998 over 14 repeats; 9.6 D20): `cc1` has no child, so its one structural step runs from its start to its exit; it ends at exit, not at a block. It wakes once in 39 749 of the 39 998 object jobs (99.4 %; per repeat 99.2–99.6 %); 99.3 % is repeat 4's (9.6 D20).
- **The per-key venue** (9.5 `campaign/method.md` §4, "Single core"): the application's process tree pinned to one CPU, "Xvfb, perf, the replay driver and the snapshots run on the other vCPUs … with the display server idealised" — the per-key CPU is the application's tree; the X server's drawing is not in it.
- **VS Code's stimulus** (`code-editor` scope): "the keys are a fixed letter cycle (D4: timing only), so the per-key cost is the language server re-checking a file being filled with letter runs".
- **Restated D33:** on the dataset's machine an editor's threads run a few hundredths of a millisecond between blocks, a few milliseconds at the 99th percentile, while `cc1` runs a median 368 ms of CPU from its start to its exit, unblocked in 99.4 % of object jobs. **D32:** the per-key figures are the application's process tree on one CPU, the X server's drawing left out; VS Code's 79.7 ms is its language server re-checking a file being filled with letter runs.

Hands to 9.15: `docs/research-proposal.md:123`, `docs/background-guide.md:115` (D33) and `:95` (D32) as restated; the glossary's "Interactive process — … Short CPU bursts, long sleeps" (`:826`) stated with D32's measurements (VS Code 14–45 % of its CPU while typing).

Compiled effect: none.

## D63 — D32 amended: Miller's echo limit is 0.1–0.2 s; Deber's indirect input is a touch surface; EEVDF's shorter slice is a requested one; SJF's optimality carries "only the CPU"; Solaris's table is OSTEP's 100 Hz figures (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D32 (scope-card item 31) on the 9.12 audit's re-read of its sources (A2-01–A2-04).

- **The 100 ms** (`:111`). D32's restatement "about 100 ms is the guideline's limit for a keystroke's echo" narrows Miller. Miller, p. 271: for a key's visual feedback, "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds", with "(Note that this delay in feedback may be far too slow for skilled keyboard users …)"; for a control's own response, "Time delay: No more than 0.1 second"; the estimates are "the best calculated guesses by the author" (A2-01). Deber et al.'s indirect input is finger tapping on a touch surface whose image appears on a separate screen, "an indirect setup akin to a laptop touchpad and screen" (p. 1829); its mean detection threshold 96 ms and "the textbook threshold of 100 ms (a value based on Miller's work …)" (p. 1831) (A2-02). No keyboard was measured.
- **Short turns** (`:113`). D32's "Linux's EEVDF gives a latency-sensitive task a shorter slice without a priority level" restated to the kernel document: EEVDF "calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next. It's important to note that this allows latency-sensitive tasks with shorter time slices to be prioritized"; "tasks can request specific time slices using the new sched_setattr() system call" (`sched-eevdf.rst:18–22`, `:30–32`; A2-03). Solaris's table "from 20 milliseconds (highest priority) to a few hundred milliseconds (lowest)" is OSTEP's description (ch. 8, p. 9); at illumos's default `hz` of 1 000 the same table's quanta are 2–20 ms (`illumos-ts`'s role line), so it is cited as OSTEP describes it, not as a current value.
- **SJF's optimality** (`:87`). OSTEP's conditions are carried in full: by §7.4 the first of §7.1's five assumptions is already relaxed (§7.3, p. 3: "let's relax assumption 1"), so "given our assumptions about jobs all arriving at the same time, we could prove that SJF is indeed an optimal scheduling algorithm" (p. 5) holds under assumptions 2–5; §7.6, p. 6: "if we knew job lengths, and that jobs only used the CPU, and our only metric was turnaround time, STCF would be a great policy" (A2-04).
- **Restated:**
  - `:111` — Miller's guideline puts a keystroke's echo at 0.1–0.2 s and a control's own response at 0.1 s, his "best calculated guesses"; Deber et al. measured a mean detection threshold of 96 ms for tapping on an indirect touch surface, near "the textbook threshold of 100 ms"; "is perceived as lag" attributed to them.
  - `:113` — EEVDF selects the task with the earliest virtual deadline, which lets a task with a shorter slice run sooner; a task requests its slice through `sched_setattr()`. Solaris's table as OSTEP describes it.
  - `:87` — SJF minimises average turnaround when every job arrives at once, runs to completion, uses only the CPU and has a known length; STCF without the simultaneous arrival.
  - D32's cache-cost clause and Li, Ding & Shen's figures are D57's.

Hands to 9.15: `docs/research-proposal.md:87`, `:111`, `:113` restated as above, replacing D32's wording of the same lines.

Compiled effect: none.

## D64 — D13 amended: on the depicted Ubuntu 24.04 desktop `updatedb` is not installed, and the plocate a user installs declares only the idle I/O class; the Linux count shows direction, mostly daemons raising (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D13 (scope-card item 26, with 9.6 D17's hand-off) on the 9.12 audit's read of `updatedb` on the distribution the dataset depicts — a stock Ubuntu 24.04 desktop session (`docs/workload/measurement-overview.md:21`, `:93`) — and its re-run of S3-20 (A2-05, A2-24).

- **D13's statement** "`updatedb` declares itself background work: plocate's unit sets `Nice=19` and `IOSchedulingClass=idle`, findutils' `locate.service` the same with `IOSchedulingPriority=7` (S3-02)" holds for Debian unstable (plocate 1.1.25-1, findutils 4.11.0-3; byte-identical to S3-02's copies).
- **On Ubuntu 24.04** (A2-05): the desktop image's manifest (`ubuntu-24.04.5.1-desktop-amd64.manifest`) carries no `plocate`, `mlocate` or `locate` package, and `ubuntu-desktop`, `ubuntu-desktop-minimal` and `ubuntu-standard` 1.539 neither depend on nor recommend one. The plocate a user can install is 1.1.19-2ubuntu2 (universe; the only version published to noble's Release pocket, no update — Launchpad, read 2026-10-09); its `plocate-updatedb.service` sets `IOSchedulingClass=idle` and no `Nice=` or `CPUSchedulingPolicy=`, so its CPU priority is the default. `Nice=19` enters with plocate 1.1.23 (NEWS: "plocate 1.1.23, November 24th, 2024 — Various improvements, in particular to the systemd unit file"; absent from 1.1.18-1 and 1.1.19). findutils' `locate` 4.9.0-5build1 on noble ships no unit, only `/etc/cron.daily/locate`, running `nice -n ${NICE:-10}` with `NICE=10`, `IONICE_CLASS=3` (`:31`, `:35`, `:68`).
- **"declares its class"** is an I/O class, plus a nice value from plocate 1.1.23 on; no `updatedb` unit read declares a CPU scheduling policy.
- **The direction count** (S3-20 re-run, output byte-identical, A2-24): 40 packages only lower, 16 only raise. The 16 that raise are brltty, espeakup, svxlink, osmo-bts, osmo-mgw, osmo-pcu, frr, gdnsd, earlyoom, low-memory-monitor, readsb, railcontrol, hdapsd, hipercontracer, deepin-boot-maker and deepin-log-viewer — mostly latency-bound daemons; a raise is not by itself an over-claim. The count is of Debian packages' service units, mostly daemons, not of applications; it shows the direction of declarations, not whether any declaration exceeds what its work warrants.
- **D13's restatement amended:** "Which background tools" — on the depicted Ubuntu 24.04 desktop `updatedb` is not in the stock image; where a user installs plocate (1.1.19), its unit declares the idle I/O class and leaves its CPU priority at the default; plocate's units from 1.1.23 (Debian unstable's) declare both. "In which direction" — stated as the direction of Debian's unit declarations, with who raises.

Hands to 9.15: `docs/research-proposal.md:158` ("`updatedb` does not volunteer that it is background work") restated to the depicted distribution as above — on it the sentence holds for the CPU and not for I/O; `docs/background-guide.md:18` with it; guidebook vol-03 `:109` restated to the same (D13's hand-off said "contradicted by S3-02"; on Ubuntu 24.04 the contradiction is the I/O class only). `docs/references.md` — plocate's unit cited at the version the prose names (1.1.19-2ubuntu2 for the depicted desktop, 1.1.23+ where Debian's is meant), with A2-05's hashes.

Compiled effect: none.

## D65 — D34 amended: `updatedb` per D64; the OBS knowledge-base page carries no live request against linking; Cargo's own words for "driving the compiler" (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D34 (scope-card item 35) on the 9.12 audit's re-read of S2-55, S2-56 and S3-02 (A2-05–A2-07).

- **`updatedb`** — D34's "its installed unit declares its class — plocate's `Nice=19`, `IOSchedulingClass=idle`; findutils' the same with `IOSchedulingPriority=7`" restated per D64: on the depicted Ubuntu 24.04 desktop it is not installed; the installable plocate 1.1.19 unit declares the idle I/O class only; plocate from 1.1.23 also `Nice=19`. It still leaves `:185`'s list of what "an operating system has no way to learn on its own": where it is installed, its unit declares it background work for I/O.
- **The OBS knowledge-base page** (A2-06): the banner "we ask that you avoid linking users to any knowledge base pages at this time" sits inside an HTML comment (`<!--<div id="noticeBar" …>…</div>-->`, line 150 of both S2-55's copy and the 2026-10-09 copy) and is not displayed. "the KB page quoted, not linked, at its own request" leaves; the page is cited like any other copy where the prose quotes it.
- **"Cargo driving the compiler"** (A2-07): the Cargo Book, "Why Cargo Exists": Cargo "Invokes `rustc` or another build tool with the correct parameters to build your package."

Hands to 9.15: `docs/research-proposal.md:185`'s `updatedb` clause as above; `docs/references.md` — the Cargo Book's "Why Cargo Exists" page beside its `cargo build` page; the OBS KB page entered without the "at its own request" note.

Compiled effect: none.

## D66 — D35 amended: no source ties a 64–128-frame buffer to Ardour's 5 ms; the target's arithmetic under jackd's default periods is about 32 frames; JACK's defaults are its ALSA backend's (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D35 (scope-card item 36) on the 9.12 audit's re-read of S2-36–S2-39 and S2-57 (A2-08).

- **Ardour's target** (`latency-considerations.html:12–23`): "The latency of any conversion from analog to digital and back to analog is about 1.5–2 ms … Latency below 5 ms should be suitable for a professional recording setup. Because 2 ms are already used in the A/D/A process, extremely low buffer sizes must be used in the workstation I/O setup to keep the overall latency below 5ms. Not all computer audio systems are able to work reliably at such low buffer sizes." It names no frame count. It continues (`:26–28`): "For this reason it is sometimes best to route the monitor signal through an external mixing console while recording, an approach taken by most if not all professional recording studios."
- **What the target takes** (arithmetic on the sources' formulas): the latency that matters is round trip, capture "usually one audio period" plus playback (`latency-and-latency-compensation.html`); jackd: capture latency is "--period divided by --rate", playback "--nperiods times --period divided by --rate. The default is 2" (jackd(1) `:244–246`, `:285–286`, ALSA backend). At 48 kHz with two playback periods, a 128-frame period gives 2.67 + 5.33 = 8.0 ms before conversion, 9.5–10 ms with it; 64 frames 4.0 ms, 5.5–6 ms; 32 frames (0.67 ms; PipeWire's `default.clock.min-quantum = 32`) 2.0 ms, 3.5–4 ms — the largest power-of-two period under 5 ms.
- **Defaults:** jackd's `-r` 48000 and `-p` 1024 are its ALSA backend's (`:287`, `:292`); its CoreAudio backend's are 44100 and 128 (`:359`, `:364`). PipeWire's `default.clock.quantum = 1024` is the "Default quantum used when no client specifies one" (`pipewire.conf.5.md:233–234`). Steam Deck's 40–60 Hz range is an embedded update post on its page ("The in-game screen refresh rate can now be adjusted on the fly anywhere between 40-60Hz"), beside the specification lists' "up to 60Hz" (LCD) and "up to 90Hz" (OLED).
- **Restated `:640`:** no source states "1–3 ms". Ardour's manual sets a recording target below 5 ms round trip, which under jackd's default two periods at 48 kHz takes a 32-frame period (0.67 ms, arithmetic), and notes that studios usually monitor through an external console instead; a 128-frame buffer at 48 kHz comes due every 2.67 ms (arithmetic). "the buffer Ardour's 5 ms target calls for" leaves. `:414` and `:820` as D35 restated them.

Hands to 9.15: `docs/research-proposal.md:640` restated as above, replacing D35's wording; `:414`, `:820` as D35 states them, with JACK's defaults named as its ALSA backend's.

Compiled effect: none.

## D67 — D36 amended: a ticket holder "will eventually win", its expected wait 1/p lotteries, with no bound (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D36 (scope-card item 38) on the 9.12 audit's re-read of `waldspurger-osdi94` (A2-09).

- **The paper** (§2.2, p. 2): "The number of lotteries required for a client's first win has a geometric distribution. The expected number of lotteries n that a client must wait before its first win is E[n] = 1/p, with variance σ²ₙ = (1 − p)/p². Thus, a client's average response time is inversely proportional to its ticket allocation"; "Since any client with a non-zero number of tickets will eventually win a lottery, the conventional problem of starvation does not exist." The guarantee is eventual; the paper states no worst-case wait.
- **Against the harness's 30 s guard** (arithmetic): a client holding 1/1 000 of the tickets, at 10 ms a lottery, waits past 30 s (3 000 lotteries) with probability 0.999³⁰⁰⁰ ≈ 5 %.
- **Restated:** D36's "Starvation … Kept, scoped to a client holding tickets" becomes: a client holding tickets eventually wins, after 1/p lotteries on average (p its share of the tickets), with no bound on the wait. "freedom from starvation" (`:828`) and "starvation-freedom" (`:422`) restated so.

Hands to 9.15: `docs/research-proposal.md:422`, `:828` as above, with D36's other restatements.

Compiled effect: none.

## D68 — D37 amended: the optimality sentence is on printed p. 58; above a utilisation of 1 no feasible schedule exists (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D37 (scope-card item 40) on the 9.12 audit's re-read of `liu-jacm73` (A2-10).

- **Locators:** "if a set of tasks can be scheduled by any algorithm, it can be scheduled by the deadline driven scheduling algorithm" is on printed p. 58 (end of §7), not pp. 55–56; p. 55 states it as "if a set of tasks can be scheduled by some priority assignment, it can also be scheduled by this method", and there EDF is defined: "priorities are assigned to tasks according to the deadlines of their current requests".
- **Above 1** (Theorem 7's proof, printed p. 56): "(C1/T1) + … + (Cm/Tm) > 1, there is clearly no feasible scheduling algorithm." D37's "The paper says nothing of behaviour above a utilisation of 1" leaves: above 1 no algorithm meets every deadline; how EDF misses deadlines there the paper does not say.
- **Restated:** on one processor, for independent periodic tasks whose deadline is the next request, EDF — priority by the deadline of the current request (p. 55) — schedules every task set any algorithm can (p. 58), exactly those whose utilisation is at most 1 (Theorem 7, p. 56); above 1 none can (p. 56). It needs each task's period or deadline.

Hands to 9.15: `docs/research-proposal.md:824` as above; `docs/references.md` `liu-jacm73`'s role clause "it says nothing about behaviour above utilisation 1" → "above utilisation 1 no feasible schedule exists (p. 56); how EDF behaves there it does not say".

Compiled effect: none.

## D69 — D38 amended: held time runs the configuration in force, not the boot default; the definition is the data contracts' §7; "70%" leaves (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D38 (scope-card item 41) on the 9.12 audit's read of the contracts, the guard and the aggregates code (A2-11).

- **The definitions** are in `docs/data-contracts.md` §7 (`:344`), not §6: "`held` (proposal rejected; previous config carried forward), or `fallback` (the default, from boot or after repeated failures)"; "`config` is the post-validation configuration actually in force after the entry — … the carried-forward config for `held`".
- **The guard sums both** (`harness/tools/harness/aggregates.py:185–187`: `fb = ci[ci["provenance"].isin(["fallback", "held"])]`, emitted as `fallback_share`; `guard-spec.yaml:114–123`). Held time runs whatever configuration was last in force — a recognized one (MLFQ, EDF, LOTTERY or FIFO) or the boot default; fallback time runs the boot default, MLFQ in all ten committed boot-default files (`harness/boot-defaults/`).
- **Restated:** a condition whose run spent half or more of its time under fallback or held configurations fails the `provenance_share` guard, and its score is not read as evidence about recognition; the part of that time under fallback measured the boot default, MLFQ. "70%" leaves (an example with no source; the guard's line is one half).

Hands to 9.15: `docs/research-proposal.md:718`, and `:916` (B.3) with it, stated as above, replacing D38's wording.

Compiled effect: none.

## D70 — D39 amended: one shooter's sessions are mostly minutes; WoWAH's 1.8 h is the median of each avatar's average session on one realm's Horde faction; the transitions are six coreset files (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D39 (scope-card item 42) on the 9.12 audit's re-reads of S3-11 and S3-23 (A2-12, A2-13).

- **Counter-Strike** (Chambers et al., IMC '05, §3.2 "Gamers have short attention spans", p. 4): "a significant number of players play only for a short time before disconnecting and … the number of players that play for longer periods of time drops sharply as time increases"; "more than 99% of all sessions last less than 2 hours"; "a Weibull distribution with β = 0.5, η = 20, and γ = 0 closely fits the PDF of measured session times" (minutes; Figure 2). Its median is η(ln 2)^(1/β) ≈ 9.6 minutes (arithmetic). The source is the counter-case to "an hour", not support for it. One server, cs.mshmro.com; the trace table (p. 2) runs Tue Apr 1 2003 to Mon May 31 2004, the abstract says "13-month".
- **World of Warcraft** (WoWAH, MMSys '11, A2-13): Table 4 (p. 126), "Session time (hr)", (mean, SD) (2.8, 1.8), quantiles (5 %, 25 %, 50 %, 75 %, 95 %) (0.4, 1.0, 1.8, 3.0, 5.5) — "the quantiles and averages of the average daily play time, average session play time, and average daily session count": a distribution over 91 065 avatars of each avatar's average session, not over the 667 032 sessions (p. 125); one realm, TW-Light's Hope, one faction, Horde (Table 1, p. 125); the "knee" sentence is likewise of "the average session play time" (p. 126).
- **The coreset's transitions** (`dataset/README.md:83–91`): three transition arcs (C3) and three distractor injections (C4), 6 of the 50 files.
- **Restated `:303`:** polling every 30 s asks the same question 120 times in an hour of play (arithmetic); how long a session lasts depends on the game — on one World of Warcraft realm the median avatar's average session was 1.8 h (5th–95th percentile 0.4–5.5 h), while on one Counter-Strike server most sessions lasted minutes and more than 99 % under 2 h.
- **Restated `:732`:** "the situation is stable for the whole thing" stays a premise, as D39 states it; "which is why the workloads are built around transitions" → the coreset's three transition arcs and three distractor injections test the transitions.

Hands to 9.15: `docs/research-proposal.md:303`, `:732` restated as above, replacing D39's wording; `docs/references.md` WoWAH (S3-11) and Chambers et al. (S3-23) with these locators.

Compiled effect: none.

## D71 — D40 amended: the scale leg restated to current 7–9B models; the format leg to what Tam et al. test, on the published version (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D40 (scope-card item 43) on the 9.12 audit's re-read of S1-26–S1-28 and the published version of Tam et al. (A2-14).

- **Scale.** Wei et al.'s threshold (p. 4: gains "only … with models of ∼100B parameters") is measured on 2022 models on arithmetic reasoning (§3.1, p. 4: GPT-3 "350M, 1.3B, 6.7B, and 175B", LaMDA "422M, 2B, 8B, 68B, and 137B", PaLM "8B, 62B, and 540B", UL2 20B, Codex). Sprague et al.'s Table 6 (p. 25; direct answer % → CoT %) shows current 7–9B instruction-tuned models gaining on math: Meta-Llama 3.1 8b 16.0 → 47.8, Gemma 2 9b 18.5 → 50.5, Qwen 2 7b 15.9 → 53.5. The ∼100B threshold does not bound them.
- **Task kind** (Sprague et al.): on commonsense, language-understanding and reading-comprehension datasets "there is little to no separation between the performance of zero-shot CoT and zero-shot direct answer" (§4.2, p. 6); "For non-math questions, we find no features to indicate when CoT will help" (p. 2); Meta-Llama 3.1 8b commonsense 72.9 → 73.4, knowledge 70.1 → 74.1, soft reasoning 55.0 → 56.2; Qwen 2 7b soft reasoning 54.4 → 49.4 (Table 6).
- **Format** (Tam et al., EMNLP 2024 Industry Track, pp. 1218–1236; the published version): every format carries both fields — "we limit the number of key-value pairs for each dataset to 2: reasoning and answer fields" (§3.2, p. 1220); "In Table 11 we found in classification task JSON-mode performs much better than text due to the restriction on answer space. However in reasoning related task, JSON-mode failed to adhere to the order of reasoning first followed by answer" (p. 1222); "100% of GPT 3.5 Turbo JSON-mode responses placed the "answer" key before the "reason" key, resulting in zero-shot direct answering instead of zero-shot chain-of-thought reasoning", and "The order of keys in structured outputs and the decoupling of reasoning from format adherence emerge as important factors" (p. 1221); "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy" (Conclusion, p. 1224). Open-weight models tested: LLaMA3-8B-Instruct and Gemma-2-9B-Instruct (§3.3, p. 1220). They do not compare an answer with and without a reasoning field. The passages are worded the same in arXiv v3.
- **Restated:** the recognizer's answer is a classification from a closed menu, by a 3–8B local model under a JSON schema. For classification-like, non-math questions the literature finds little or no gain from reasoning first (Sprague et al.); models of this size do gain on math, so scale alone does not rule a gain out; under a JSON schema, constrained decoding helped classification by restricting the answer space and hurt reasoning, and an answer generated before its reasoning turned chain-of-thought into direct answering (Tam et al.). No source compares a classification with and without a reasoning field. The *Quality* bullet leaves as a claim and stands as the question Layer 1 can answer, as D40 decided; Wei et al. leaves the grounds.

Hands to 9.15: `docs/research-proposal.md:340` as above; `docs/references.md` — Tam et al. under its published version (EMNLP 2024 Industry Track, its ACL Anthology copy), Sprague et al. (ICLR 2025); Wei et al. only if the prose cites it. **9.14:** with D40's question, Tam et al.'s key-order finding: the comparison holds only if `reasoning` is generated before `system` (the contract and the stand-in schema list it first: `docs/data-contracts.md` §6; `dataset/tools/meas/llm/schema.full.json`).

Compiled effect: none.

## D72 — D42 amended: Vulcan lists CPU scheduling as an example task in its v3 Table 1; "the nearest architecture" leaves; Vulcan's DOI stays out of the cite line; LumOS read in full (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D42 (scope-card items 48, 49) on the 9.12 audit's re-reads of S1-17 and S1-18 and its full read of S1-20 (A2-15–A2-17).

- **Vulcan's tables** (A2-15): v3's Table 1 (p. 6), "Examples of systems resource management tasks", lists "CPU scheduling [70] | Select which thread to schedule next. | Rank: all runnable threads."; v1 lists it in Table 1 (p. 4) and in Table 3, "Examples of RANK tasks" (p. 6). D42's "CPU scheduling appears only as an interface example in v1's Table 3" → an example task in its interface tables (v3 Table 1; v1 Tables 1 and 3), not an evaluated domain. Its evaluation: spot-VM scheduling, cache eviction (libCacheSim) and tiered memory, searched with OpenEvolve and ShinkaEvolve (§3.2).
- **"as the nearest architecture to this work's"** leaves: no source compares TuxBot's architecture with this work's or with ASA's and SchedCP's, which `docs/related-work.md:24` ("Closest to our architecture in shape, ASA") and `:32` ("SchedCP, the closest prior work") already rank — as D10 removed "the most developed". TuxBot is stated as what it does (A2-16): an online tuner whose fast loop proposes updates out of band, "not kernel fast-path controllers such as the CPU scheduler" (p. 1), on hosted Gemini 2.5 Flash and Flash-Lite (p. 9), every change through "typed validation"; the registry's "Nearest point of contact … is the gating" stays as its role line words it.
- **Vulcan's DOI** 10.1145/3842654.3848582, printed on v3 (p. 1), resolves nowhere on 2026-10-09: doi.org handle API `{"responseCode":100}`, Crossref "Resource not found.", DataCite 404; the ACM Digital Library returned a challenge page (A2-15). The cite line carries the arXiv id only, as D42 states, until the DOI resolves.
- **LumOS** (S1-20, read in full from the author's PDF linked from the project page, A2-17): Liargkovas, Jabrayilov, Franke and Kaffes, "An Expert in Residence: LLM Agents for Always-On Operating System Tuning", NeurIPS 2025 Workshop: Machine Learning for Systems — TuxBot's first two authors' earlier work. An LLM loop (Gemini 2.5 Flash) tunes CFS's `latency_ns` and `min_granularity_ns` online against a TPC-C/PostgreSQL workload's p99 latency, one proposal per "10-second workload run" (p. 2), on Linux 5.15; against Bayesian optimisation "reduces p99 by 5.0% in 1-parameter tuning … and by 7.1% in 2-parameter tuning" (p. 3); the proposed agent's actions are JSON-Schema tools "validated server-side (types/ranges)" (p. 3). It reports no measurement of recognition, so D12's scoped statement holds. Whether related-work cites it is decided with D42's citations (pending 인지오).

Hands to 9.15: `docs/related-work.md:32`'s TuxBot sentence without the superlative; Vulcan's sentence naming its evaluated domains; `docs/references.md` `vulcan-arxiv25` — "CPU scheduling … an example task in its interface tables (v3 Table 1), not evaluated"; S1-20's entry status updated to the full read.

Compiled effect: none.

## D73 — D44 amended: `scx`'s README states Meta's deployment in progress; the role's "deployment-path claim" and the "Bound on the deployment claim" paragraph are restated with it (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D44 (scope-card items 56, 57) on the 9.12 audit's re-read of `scx` at `v1.1.3` (A2-18).

- **What the repository states** (`README.md:33–35` at `c8728c6b`): "`sched_ext` is supported by the upstream kernel starting from version 6.12. Both Meta and Google are fully committed to `sched_ext` and Meta is in the process of mass production deployment"; `OVERVIEW.md:283–284`: "Distros are able to package and release these schedulers". D44's "production deployment being stated by the operators' own entries … never by `scx`" restated: `scx`'s README states Meta's deployment as in progress; the paper's production statements cite the operators' own entries (D8: Meta's LPC 2024 slides and LPC 2025 abstract; D9: Valve's SteamOS sources), and `scx` for the schedulers' existence and design.
- **The role's "the deployment-path claim"** (`docs/references.md:214`) is D27's path, grounded in `schedext-docs` and the Ubuntu kernel configuration (D27); it leaves `scx`'s role.
- **The "Bound on the deployment claim" paragraph** (`:215`) stays with its quotations, restated to the line above.

Hands to 9.15: `docs/references.md` `scx` — `:214` (role without "the deployment-path claim"; "existence of production sched_ext schedulers" → existence of the schedulers, D44) and `:215` as above, beside D44's `:216`.

Compiled effect: none.

## D74 — D45 amended: Microsoft's statement is dated: Xbox Wire, 2018-10-02, and the support article's wording captured on 2018-12-30; `ananicy-rules`' role line handed (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D45 (scope-card item 59) on the 9.12 audit's dating of S2-58 (A2-19).

- **The article today** (rendered 2026-10-09; body text identical to S2-58's rendering): "When you use Game Mode, Windows prioritizes your gaming experience by turning things off in the background. When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications"; the page carries no date.
- **Its dated copies:** the Internet Archive's capture of `https://support.xbox.com/en-US/games/game-setup/use-game-mode-gaming-on-pc` of 2018-12-30 (20181230054712) reads "When you use Game Mode, Windows prioritizes your gaming experience. When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications."; the capture of 2018-07-06 (20180706084246) has no Windows Update sentence.
- **Microsoft's dated statement:** Xbox Wire, "Latest October 2018 Windows Update Gaming Features", `datePublished` 2018-10-02T21:44:22Z (capture 20220808125358): "Now auto-enabled for all games with a master On/Off toggle in Windows Settings, Game Mode suppresses Windows Update driver installs and blocks Windows Update interruptions such as restart notifications while you're gaming." It does not say how Windows recognises a game; D1 stands.
- **`ananicy-rules`' role line** (`docs/references.md:236`: "grounds the wanted/unwanted-background distinction as deployed practice") says what D45 restated `grounding-sources.md:18` away from; it is restated the same.

Hands to 9.15: `docs/references.md` — the Xbox Support entry carries the 2018-12-30 capture as the earliest dated copy of the wording and the Xbox Wire post (2018-10-02) as Microsoft's dated statement, in place of "no date on the page" alone; `ananicy-rules`' role line `:236` restated to a per-name priority catalogue, not a wanted/unwanted judgement (D3, D45).

Compiled effect: none.

## D75 — D46 amended: Dessau's own post is read: AMD's CMO gave weighting, GPU acceleration and unrepresentative workloads; the registry still carries the old note (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D46 (scope-card item 70) on the 9.12 audit's read of Dessau's blog post and X-bit Labs' report through the Internet Archive (A2-20).

- **Dessau's post** (Nigel Dessau, "Voting for Openness", blogs.amd.com, June 21, 2011; capture 20110623165026; AMD's release links it as "Executive Blog"; "Nigel Dessau is Senior Vice President & Chief Marketing Officer for AMD. His postings are his own opinions and may not represent AMD's positions"): "We got workloads included that represent the things you and I actually do in a day … But the question remained: what weighting would BAPCo ultimately give to the real-world workloads − since it is this weighting that defines the actual benchmark scores"; "only 7 applications and less than 10 percent of the total measurements dominate the overall score"; "a relatively large proportion of the SM2012 score is based on system performance rated during optical character recognition (OCR) and file compression activities"; "SM2012 scores do not take into account GPU-accelerated applications"; "The heart of our complaint is this: the SYSmark benchmark is not only comprised of unrepresentative workloads (workloads that ignore the importance of heterogeneous computing and, frankly, favor our competitor's designs), but it actually generates misleading results".
- **X-bit Labs** (capture 20110625114727 of its 2011-06-23 report): "disagreements over the scoring system of SYSmark2012 which does not take graphics card's role into account" is the reporter's wording; Nvidia's spokesperson: "We have resigned [from BAPCo]".
- **Restated:** AMD's CMO gave the weighting of SYSmark 2012's scores and its neglect of GPU-accelerated work, calling its workloads unrepresentative; VIA said its tests "do not accurately reflect real world PC usage scenarios and workloads"; Nvidia gave no reason, its departure tied to SYSmark 2012 by reporters. D46's "AMD's dispute over weighting is a report of it beside that" leaves: the weighting complaint is AMD's own. The conclusion stands — the reasons were not the scoring alone — and no sentence of the paper needs it.
- **The registry** (`docs/references.md:250`, `sysmark30`'s role): "Note in paper: the 2011 vendor departures concerned scoring, not scenario lists." — D46's "The registry … no longer carry it" is wrong for this line.

Hands to 9.15: `docs/references.md:250`'s note removed or restated as above (with `docs/workload/source-vetting.md:40`, D46's hand-off); if prose ever cites the dispute, Dessau's post through its 2011-06-23 capture, not through Tom's Hardware.

Compiled effect: none.

## D76 — D47 amended: SchedCP's evaluation, singular; the compile family's short-lived structure keeps `ocallahan-atc17`; the 368 ms is `cc1_step_1` (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D47 (scope-card item 63) on the 9.12 audit's re-read of its grounds.

- **"a compile workload scheduler evaluations use, SchedCP's among them"** — the plural rests on SchedCP alone in this slice's reads (v4 §5, p. 4: "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source) … 1.79× total improvement over EEVDF"). Restated: a compile workload SchedCP's evaluation uses (1.79×).
- **The short-lived structure** keeps the registry's ground: `ocallahan-atc17`, "make forks and execs 2430 processes, mostly short-lived" (§4.3; `docs/references.md:107`), which `dataset/archetypes.yaml`'s compile notes already cite for "the class's existence and short-lived character only" (9.6's read: a `make -j8` build, "not a kernel build"); the measured structure is the dataset's build (D47), SchedCP's "short-lived processes" its agent's profile text.
- **"`cc1` a median 368 ms of CPU"** is `compiler-child`'s `cc1_step_1` p50, 367 630 µs (`dataset/archetypes.yaml:971–972`), the `cc1` process's CPU from start to exit (D62).

Hands to 9.15: `docs/workload/grounding-sources.md:32` as above, replacing D47's wording.

Compiled effect: none.

## D77 — D48 amended: what llama.cpp's converter does with what it does not support, as its code at `bd4eeaa0` shows; the schema carries the menu, not the number ranges (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D48 (scope-card item 30) on the 9.12 audit's read of llama.cpp's code at the commit the project's runner pins (A2-22).

- **Silent:** the schema reader (`common/json-schema.cpp`) reads 22 keywords — `$ref`, `oneOf`, `anyOf`, `allOf`, `type`, `const`, `enum`, `properties`, `additionalProperties`, `required`, `items`, `prefixItems`, `minItems`, `maxItems`, `pattern`, `format`, `minLength`, `maxLength`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`; any other is ignored without a message. A `number` is built with no bounds (`json-schema-to-grammar.cpp:963–964`; an `integer`'s bounds are built, `:952–961`).
- **Warned on the server only:** a pattern it cannot express is accepted as any string — "pattern … is not supported (…), accepting any string" (`:394–397`) — and the server prints "WARNING: JSON schema conversion was incomplete" to its stderr (`:979–980`); the client is not told.
- **An error:** a `$ref` outside the document fails the request ("unsupported $ref …, only references into the same document are supported", `json-schema.cpp:104–105`), as does any conversion error (`json-schema-to-grammar.cpp:976–977`; `tools/server/server-schema.cpp:268–269`).
- **A completed answer is well-formed:** the end-of-generation token's logit is set to −∞ unless a grammar stack is empty (`src/llama-grammar.cpp:1366–1387`), so an `eos` stop implies the grammar completed. Besides `limit`, a generation ends at a stop word (`word`, `tools/server/README.md:669`; the project sends none) or past the context (`truncated`, `:674`).
- **The runner's build** pins `LLAMA_SHA=bd4eeaa0…` (`dataset/tools/meas/llm/run.sh:14`) with default CMake, and `LLAMA_LLGUIDANCE` defaults `OFF` (`CMakeLists.txt:146`), so requests go through this converter; `request.py` sends `json_schema` to `/completion` with `n_predict` 384. The two measured schemas use only keywords it reads.
- **What the schema carries:** the algorithm menu is an `enum` the converter supports; the number ranges (`timeslice_growth` 1–8, `batch_share` 0.01–0.90, `batch_bandwidth_cap` 0.05–0.95), the clamping rule and the cross-field rule (`docs/recognition-vocabulary.md` §2, validation rules 3–5) are not enforced by the grammar.
- **Restated:** D48's "a schema feature the converter lacks is skipped silently" → llama.cpp converts a subset of JSON Schema: keywords it does not read are ignored without notice, a pattern it cannot express is accepted as any string with only a server-log warning, and some unsupported constructs fail the request. D48's "(the menu, ranges and cross-field rules …)" → the number ranges, the clamping rule and the cross-field rule. The parse-failure branch stays for answers ended by the token limit or the context.

Hands to 9.15: `docs/research-proposal.md:489` as above, replacing D48's wording of the two clauses.

Compiled effect: none.

## D78 — D49 amended: Apple's document, in its own words: "priority inflation across the platform", subsystems raising priority to avoid starvation, as an artifact of the Mach scheduler (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D49 (scope-card item 26) on the 9.12 audit's re-read of S2-54 (A2-23).

- **The passage in context** (`doc/scheduler/sched_clutch_edge.md:7` at `xnu-12377.121.6`; the same text in `osfmk/kern/sched_clutch.md:5` at `xnu-6153.11.26`): "The XNU kernel runs on a variety of platforms … The traditional Mach scheduler attempts to achieve these goals by expecting all threads in the system to be tagged with a priority number … It then uses a timesharing model based on priority decay … One artifact of this thread based timesharing approach is that threads at the same priority level are treated similarly irrespective of which user workload they are servicing, which often leads to non-optimal decisions. It ultimately leads to priority inflation across the platform with individual subsystems raising their priority to avoid starvation and timesharing with other unrelated threads."
- **Not in the source:** "macOS" (the document says "the platform"; the word macOS does not occur), "macOS's own subsystems" (no subsystem is named or attributed), "a documented instance" (a design rationale, with no named case, date or data), "over-declaration" (the motive stated is defensive: to avoid starvation and timesharing with unrelated threads).
- **D49's restatement amended:** Apple's XNU scheduler documentation gives priority inflation across the platform — individual subsystems raising their priority to avoid starvation and timesharing with unrelated threads — as an artifact of the traditional Mach scheduler's thread-level timesharing and a motivation for the Clutch scheduler (S2-54). The limit at `:158` may cite it so; on Linux, Debian's unit declarations mostly lower priority, and those that raise are mostly latency-bound daemons (D64).

Hands to 9.15: with D13's and D49's lines (`docs/research-proposal.md:158`, `docs/background-guide.md:18`, guidebook vol-01 `:2099`), worded as above; `docs/references.md`'s XNU entry role with this passage, without "macOS's own" or "instance".

Compiled effect: none.

## D79 — D30 amended: the cap is the driver table's under every condition but `llm_full`, and the executor is to enforce it, not yet; four more lines rest on the removed premise (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D30 (scope-card item 71) on the 9.12 audit's read of the code, the contracts and the proposal (A2-25).

- **Who sets the cap.** Only `llm_full` fills the `cpu_scheduler` block (`docs/research-proposal.md:441`); under `llm_algo` "the cap and the constants remain the table's" (`:439`); `random`, `whitelist`, `llm_vocab` and `oracle` "receive the row's **default** entry" (`docs/data-contracts.md` §10, `:467`). The driver table's cap "is never null" (`daemon/driver-table/prior.yaml:17`): 16 rows at 0.05, 11 at 0.5, 4 at 0.333, 1 at 0.2. An unset cap comes from the boot default (`batch_bandwidth_cap: null`, `docs/recognition-vocabulary.md` §2) and from `llm_full`. D30's "the cap is a field the model sets" restated so.
- **Who enforces it.** The simulator's loader reads no cap (`simulator/src/sim.cpp:892–925`; no occurrence of "bandwidth" in the file); the simulator guide lists "per-class bandwidth caps, enforced by the executor regardless of what any config says" among what is "Needed eventually" (`docs/simulator/simulator-guide.md:210`, §5). D30's restated "which the executor enforces" → which the executor is to enforce, not yet implemented.
- **When a wait is unbounded.** FIFO's and EDF's deadline tasks return no horizon (`sim.cpp:165`, `:291–293`); the cap is a ceiling on the batch class's share while non-batch work is runnable (`recognition-vocabulary.md:70`), not a floor, so an unset cap leaves a wait unbounded only beside an algorithm without a horizon. An idle-class task "runs only when no task of another class is runnable" and "waits behind every run of its editor by design" (9.11 D5, D7) under every configuration; the simulator has no idle class yet (`sim.cpp`).
- **Lines the sweep missed** (`grep "starvation\|bandwidth cap"` does not match them): `docs/research-proposal.md:517`, the identical-executor diagram's "same algorithms / same parameters / same caps" — the caps differ by condition and row; `:131` "throttled but never starved", `:174` "throttled, not starved", `:621` "Throttle, never starve" — no executor rule gives the download a floor; `:908`, the appendix trace's `"reason": "bandwidth_cap"`, not a value of the trace contract ("reason ∈ block | preempt | exit | depart", `docs/data-contracts.md:415`).
- **Restated (the parts not pending):** §4.7's statement of what holds reads: the executor has no starvation window; FIFO and EDF's deadline class have no horizon, so beside them an unset cap can leave a task waiting without bound, and an idle-class task waits behind other classes by design; MLFQ's boost can be lengthened to 10 s but not removed; a run in which any task waits more than 30 s fails `starvation_floor`, and on a run the criterion reads that makes the verdict invalid. The batch class's cap is a configuration field — the driver table row's under every condition but `llm_full`, unset or 0.05–0.95 there — which the executor is to enforce.

Hands to 9.15: `docs/research-proposal.md:473`'s replacement as above (replacing D30's wording); `:517` → the same executor, with the algorithm, parameters and cap each configuration sets; `:131`, `:174`, `:621` → throttled by the batch class's cap, its waits judged by the 30 s guard, not guaranteed; `:908` → a trace reason the contract defines; `docs/simulator/simulator-guide.md:210` (D30's hand-off) to the one cap, "to be enforced". `:756` is pending 인지오.

Compiled effect: none.

## D80 — related-work's opening of the behavioural section: inside the scheduler what is inferred is inferred from behaviour; deployed systems also act on declarations, the window system and a name table (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (no scope-card item): `docs/related-work.md:16`'s "Where situational awareness exists in deployed schedulers today, it is inferred from runtime behavior." is read against the slice's reads of what deployed systems act on (A4-09 to A4-12; D2, D10, D13, D18, D26, D28, D29).

- **Inferred from behaviour, inside the scheduler:** MLFQ's demotion by CPU use, CFS's and EEVDF's sleeper handling (D18), scx_lavd's latency criticality from wake/wait patterns (D10); Windows boosts a thread "when a wait operation associated with disk or keyboard I/O finishes" (A4-09).
- **Declared by the program, its packager or a wrapper:** on Linux the policy, nice value and I/O class — "The nice value can be modified using nice(2), setpriority(2), or sched_setattr(2)" (sched(7), A4-12) — set by the program, its unit or a wrapper (D13, D26); on macOS a QoS class the developer assigns, "Constants that indicate the nature and importance of work to the system" (Apple's `QualityOfService`, A4-12), which XNU's scheduler follows: "These scheduling buckets roughly map to the QoS classes used by the OS runtime to define performance expectations for various pieces of work" (`sched_clutch_edge.md:24`, A4-12; D28, D29).
- **From the window system:** Windows — "When a process that uses NORMAL_PRIORITY_CLASS is brought to the foreground, the scheduler boosts the priority class of the process associated with the foreground window" and "When a window receives input, such as timer messages, mouse messages, or keyboard input, the scheduler boosts the priority of the thread that owns the window" (Microsoft Learn, "Priority Boosts", A4-09); Game Mode — "The app must be in the foreground and have focus before exclusive resources are granted" (A4-10), and on macOS "When your game enters full screen, Game Mode automatically turns on for that game" (A4-11; D2).
- **From a name table:** ananicy-cpp's catalogue, matched by executable name (D3).
- **"it is inferred from runtime behavior"** holds for what a scheduler infers about a task itself; as a statement of where deployed situational awareness comes from it is contradicted by the declared classes, the foreground and input boosts and the game modes above.
- **Restated:** inside the scheduler, what a deployed scheduler infers about a task it infers from runtime behaviour; the other signals deployed systems act on are declared — a Linux class, nice value or unit setting, a macOS QoS class — or come from the window system (Windows' foreground and input boosts; Game Mode's foreground or full-screen game) or from a name table (ananicy-cpp's catalogue). D18's restatement is of `:16`'s second sentence and D10's of its third; this decision is the first's.

Hands to 9.15: `docs/related-work.md:16`'s first sentence restated as above; the section heading ("Behavioral inference inside the scheduler") stands; Microsoft's "Priority Boosts" page is D29's registry entry.

Compiled effect: none.

## D81 — the learned line's mapping: Decima and FIRM learn a policy from observed state to actions — Decima's scheduling decisions, FIRM's resource limits; Park defines such state and action spaces (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (no scope-card item): `docs/related-work.md:24`'s "These systems learn a mapping from observed system state to scheduling actions" is read against the three papers (A4-08), after D19 (`:24`'s first sentence, Park restated as a platform) and D20 (the limits clause that follows).

- **Decima** (`decima-sigcomm19`): "a scheduling agent observes the cluster state to decide a scheduling action on the cluster environment … The agent uses a graph neural network to turn job DAGs into vectors for the policy network, which outputs actions" (Fig. 4 caption, PDF p. 4); "Mapping the cluster state to a scheduling decision takes less than 15ms" (§6.1, PDF p. 8).
- **FIRM** (`firm-osdi20`): the RL agent "performs an action at ∈ A based on its policy πθ (s) … which maps state space S to action space A" (RL primer, PDF p. 8); its state is SLO maintenance ratio, workload changes, request composition and resource utilization, its action "Resource Limits RLTi (t), i ∈ {CPU, Mem, LLC, IO, Net}" (Table 3, PDF p. 10) — resource-management actions, not scheduling actions.
- **Park** (`park-neurips19`): "an open, extensible platform that presents a common RL interface to connect to a suite of 12 computer system environments"; "For each environment, Park defines the MDP formulation, e.g., events that triggers an MDP step, the state and action spaces and the reward function" (§1, PDF p. 2) — it learns nothing itself; agents are learned in its environments.
- **Restated:** Decima and FIRM learn a policy mapping observed system state to actions — Decima's scheduling decisions over job DAGs, FIRM's per-microservice resource limits — and Park defines such state and action spaces for the twelve environments in which agents are learned. D20's limits clause follows unchanged.

Hands to 9.15: `docs/related-work.md:24`'s second sentence, its opening clause restated as above.

Compiled effect: none.

## D82 — the two shared commitments scoped to the works that state them: the semantic gap SchedCP's, the LLM out of the per-decision path SchedCP's, TuxBot's, Vulcan's and AKTS's; Jadhav et al.'s LLM makes the decisions (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (no scope-card item): `docs/related-work.md:34`'s "We share two commitments with this line: the semantic gap as the problem, and LLM reasoning kept strictly out of the scheduling hot path." is read against the LLM works related-work cites or will cite (D12, D22–D24, D42): SchedCP, Kgent, TuneAgent, Jadhav et al., TuxBot, Vulcan, AKTS (A4-01 to A4-07).

- **The semantic gap as the problem:**
  - SchedCP frames it: "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs" (v4 Abstract, A4-01).
  - TuxBot frames prior tuners' failure as "Lack of semantic understanding" (v2 §1, p. 1, A4-02).
  - Kgent's problem is writing eBPF ("alleviates the difficulty of writing an eBPF program", Abstract, A4-07); TuneAgent's the kernel configuration space (A4-06); Jadhav et al.'s multiobjective HPC job scheduling (A4-05); Vulcan's LLM-friendly interfaces for systems heuristics (A4-03); AKTS's switching kernel scheduling to a serving node's load regime (A4-04). None frames a semantic gap.
- **The LLM out of the scheduling hot path:**
  - SchedCP: "operating in the control plane to generate optimized code that runs natively with negligible runtime overhead, unlike traditional ML models that would cause unacceptable inference latency in the scheduler hot path" (v4 §2, PDF p. 2; v2 §3.1: "producing native eBPF code that executes without any ML inference overhead during actual scheduling decisions", A4-01).
  - TuxBot: "We study tuners that operate out of band: they are not inline on each request, and they are not kernel fast-path controllers such as the CPU scheduler, a packet scheduler, or a TCP congestion controller" (v2 §1, p. 1, A4-02).
  - Vulcan: "Vulcan takes a different stance: it avoids neural inference in the hot path entirely, confining learning to an offline search over small, interpretable LLM-generated code snippets" (v3 §9, PDF p. 14, A4-03).
  - AKTS: "Schedulers place tasks every few microseconds while even small models need milliseconds per decision, so inference on the scheduling path is ruled out by construction" (v2 §1, p. 1, A4-04).
  - Kgent and TuneAgent state no such commitment; their LLM's output is an eBPF program (Kgent) or a kernel configuration that is rebuilt and deployed before it runs — "kernel tuning requires rebuilding, deploying, and benchmarking the system" (TuneAgent v2 §1, PDF p. 2, A4-06).
  - Jadhav et al.: the LLM is the scheduler — "a novel Large Language Model (LLM)-based scheduler using a ReAct-style framework (Reason + Act), enabling iterative, interpretable decision-making" (Abstract, p. 1); "The wall-clock times required (up to an hour for 100 jobs) indicate that, at the moment, LLM-based scheduling is not suitable for real-time job submission scenarios" (§3.7.3, PDF p. 9, A4-05).
- **Restated:** we share with SchedCP the semantic gap as the problem, and with SchedCP, TuxBot, Vulcan and AKTS the LLM kept out of the scheduler's per-decision path, each stating it; Jadhav et al.'s LLM makes the HPC job-scheduling decisions itself. "this line" and "strictly" leave.

Hands to 9.15: `docs/related-work.md:34`'s first sentence restated as above, cited per work (`schedcp-mlsys25` v4 §2 and Abstract; `tuxbot-arxiv26`; `vulcan-arxiv25`; the AKTS entry D12 mints; `jadhav-arxiv25`). The sentences after it are D12's and D23's.

Compiled effect: none.

## D83 — the positioning paragraph: the LLM line's outputs and settings stated per work; the identity-reading, signal-producing cell's one documented recognizer is a name table, beside declarations and window-state triggers; the mechanisms clause scoped (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (no scope-card item): `docs/related-work.md:48`'s "Mechanisms (ghOSt, sched_ext) underlie all quadrants", "The LLM-agent line reads meaning but spends it on per-workload policy synthesis for servers" and "The meaning-reading, signal-producing quadrant — where desktop situation awareness must live — is today occupied only by static name tables" are read against D2, D3, D4, D12, D13, D21, D23, D24, D28, D42 and A4-01 to A4-07. D12 takes the paragraph's "for the first time in this line"; D6 its `whitelist` wording.

- **What the LLM line produces:**
  - Policy code: SchedCP's agents configure existing schedulers, generate patches or compose new ones (D23); Kgent synthesizes eBPF programs (D22); Vulcan synthesizes stateless decision functions in a restricted language (D42).
  - Configuration and parameters: TuneAgent the kernel's build configuration (D24); TuxBot up to 41 Linux parameters, online and out of band (D42).
  - Decisions: Jadhav et al.'s LLM schedules HPC jobs (D24; A4-05).
  - A selection among fixed policies: AKTS routes high- and low-load telemetry to a policy index — "recognize the regime at a coarse timescale and switch kernel scheduling behavior to match" — and its actuator lets "a slow agent switch among verified kernel policies" (A4-04; D12).
- **What it reads:** SchedCP's Observation Agent starts "from process name and commands" and then profiles (D12); TuxBot reads "knob schemas, telemetry, current configuration, recent action–response history, and retrieved prior runs" (A4-02); AKTS reads load telemetry (D12).
- **Where it is evaluated:** SchedCP on an 86-core Xeon server and an 8-core Core Ultra 7 258V laptop, naming edge and personal devices among its motivations (D23); AKTS on a GPU-backed LLM serving node (A4-04); Jadhav et al. on HPC job traces (A4-05); TuneAgent on UnixBench and server applications (A4-06). "per-workload policy synthesis for servers" holds for part of SchedCP only.
- **The identity-reading, signal-producing cell:**
  - The one deployed system documented as recognizing a situation from process identity is ananicy-cpp's name catalogue, which CachyOS installs and enables (D3).
  - Beside it, deployed systems act on what a program declares — a Linux class, nice value or unit setting (D13, D26), a macOS QoS class (D28), a game's request to Feral GameMode (D4), the `LSSupportsGameMode` key (D2) — and on window state: Windows' and macOS's Game Mode act on the foreground or full-screen game, how Windows recognises a game being undocumented (D2; D80). Nothing in these is recognized; the program or the window system states it.
  - Behaviour-reading recognizers that produce a selection among fixed policies exist: ASA (D21) and AKTS, the latter with an LLM (D12).
- **"Mechanisms (ghOSt, sched_ext) underlie all quadrants":** SchedCP and ASA deploy through sched_ext (D21, D23); ananicy-cpp's types set nice, I/O class and scheduling policy through the kernel's existing interfaces (D3); Windows Game Mode grants CPU sets (D2). The mechanisms underlie the policy-replacing systems, not the name table or the game modes.
- **"Behavioral heuristics and learned schedulers occupy the behavior-reading column and cannot see intent"** is the paper's argument; D14 restated the pair that grounded it in `:18`, and the clause follows D14.
- **Restated:** the LLM line turns what it reads — process names and profiles, telemetry, knob schemas — into policy code (SchedCP, Kgent, Vulcan), configuration and parameters (TuneAgent, TuxBot), job decisions (Jadhav et al.) or a selection among verified policies from telemetry (AKTS), evaluated on servers, HPC queues and, for SchedCP, a laptop; in the cell that reads process identity and produces a signal, the one documented recognizer deployed today is a static name table (ananicy-cpp's catalogue), beside the declarations and window-state triggers deployed systems act on; mechanisms such as ghOSt and sched_ext let a policy-replacing system take effect.

Hands to 9.15: `docs/related-work.md:48` restated as above, its quadrant figure (if made) drawn from the same placements; the guidebook's positioning passages checked against it.

Compiled effect: none.

## D84 — the `:12` note: "the mechanism layer is already proven" stated as D7 and D8 ground it; "forfeits less than it appears to" is the authors' argument, the simulator one lane with no sched_ext port (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (no scope-card item): `docs/related-work.md:12`'s note — "this paragraph doubles as the honest framing for why our evaluation is simulator-based with sched_ext as future work — the mechanism layer is already proven, so simulating the executor forfeits less than it appears to" — is read against D7, D8 and D27. The note is a writing note: "Each subsection ends with an italicized note … Delete the notes before submission" (`docs/related-work.md:3`).

- **"the mechanism layer is already proven"** — what the sources ground: the kernel states sched_ext's integrity and fallback ("The system integrity is maintained no matter what the BPF scheduler does", D7); operators report sched_ext schedulers deployed at fleet scale, Meta's `scx_layered` on "1M+ machines" and Valve's SteamOS offering `scx_lavd` (D8, D9). Restated to these.
- **"so simulating the executor forfeits less than it appears to"** is the authors' argument, with no source. What the simulation is: "**One lane.** Exactly one simulated CPU. The scheduler answers one question: *who holds the lane until the next event*" (`docs/simulator/simulator-guide.md:44`, A4-13); no algorithm or executor of this project has a sched_ext implementation (D27).
- **Restated:** the note, if kept in any form, states the mechanism layer as D7 and D8 ground it and the simulator as one lane with sched_ext as future work (D27); "forfeits less than it appears to" leaves or is stated as the authors' expectation.

Hands to 9.15: `docs/related-work.md:12`'s note brought in line with D7, D8 and D27, or removed with the notes before submission.

Compiled effect: none.

## D85 — the proposal's Family 3 rows read against the shipped catalogue: Discord, the Godot editor, Blender, Resolve and `node` are entries; the cluster's and the databases' programs are not (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding (sentences no scope-card item carries): `docs/research-proposal.md:631`'s "Where the whitelist fails structurally, and where the world-knowledge claim in §2.4 is decided", its rows `:636–638` ("Godot-built indie game + Discord", "Blender background render + Resolve timeline playback", "Local Kubernetes + database + dev server") and `docs/research-claims.md:75` ("A Godot-built indie game is a game that nobody registered.") are read against `ananicy-rules` at `03ef03fb` as D5 read `:635`'s row (A5-01).

- **The catalogue's entries for the rows' programs** (A5-01; a rule's `name` is "used for match processes by exec bin name", D1):
  - `:636` — `Discord` and `discord` are entries of type `Chat` (`Chats/chats.rules:17–18`; nice −3, best-effort I/O 7, `00-types.types:36`). Godot: the editor's builds `godot.x11.opt.tools.64` and `.32` are `Game` (`Games/linux-native/linux-native_g.rules:90–91`; nice −5), and `GodotWorkshopUtility.x86_64` is `BG_CPUIO` (`Games/linux-native/common.rules:524`). A game made with Godot is matched only if its own process name is an entry.
  - `:637` — `blender` (`Creative/blender.rules:2`) and `resolve` (`Creative/davinci.rules:2`) are both `Heavy_CPU` (nice 9, best-effort I/O 7, `00-types.types:33`).
  - `:638` — no entry for `kubelet`, `kube-apiserver`, `k3s`, `k3d`, `kind`, `minikube`, `containerd`, `dockerd`, `docker`, `etcd`, `postgres`, `mysqld`, `mariadbd`, `redis-server` or `mongod`; `node` is `BG_CPUIO` (`Development & Programming/node.rules:2`; nice 16, idle I/O, `SCHED_IDLE`, `00-types.types:22`), `podman` is `Service` (`Tools/podman.rules:2`).
- **What holds of the heading, row by row:**
  - `:636` — a registration failure for a game whose process name the catalogue does not carry; Discord, beside it, is registered. `docs/research-claims.md:75` holds as written for such a game; "A finite list cannot cover software it never enumerated" (`:76`) stands.
  - `:637` — not a registration failure: both programs are entries. The row's split — Resolve's playback in the foreground, Blender's render wanted in the background (`media`, `background_wanted: true`) — is one the catalogue's single type for both does not make, which is mechanism 1, combination (`docs/research-claims.md:69–72`), not mechanism 2.
  - `:638` — a registration failure for the cluster's and the databases' programs; a Node.js dev server is an entry, in the idle class.
- **D6's conditions:** the shipped-catalogue condition matches `:636`'s Discord, `:637`'s two programs and `:638`'s `node` as above; the strongest-name-table condition gives Family 3's software no rule by its definition (D6). Which of these programs Family 3 keeps, and which names the strongest table carries at the familiarity tiers' boundary, is that family's design and the build of the two conditions (D6's open points), not decided here.

Hands to 9.15:

- `docs/research-proposal.md:631` — "Where the whitelist fails structurally" stated of the programs the catalogue does not carry; `:636` and `:638` named as such, Discord and a Node.js dev server noted as entries; `:637` no longer stated as unregistered software under Family 3's heading while it names programs the catalogue carries (as D5 did for `:635`).
- `docs/research-claims.md:75–77` stand.

Hands to the build of the two conditions (D6): Family 3's rows as one input to the strongest table's boundary.

Compiled effect: none.

## D86 — "every real scheduler is a guessing machine" restated: schedulers act on CPU used against a share, on what programs declare, and on recent behaviour (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding: `docs/research-proposal.md:89`'s "So every real scheduler is a guessing machine: a pile of heuristics that watch past behaviour to estimate the future" is read against the kernel's own documents and the reads D18, D26, D28 and D29 took.

- **CFS** (A5-02; `sched-design-CFS.rst` at `7b63ef2d`, byte-identical to S2-04): "CFS basically models an "ideal, precise multi-tasking CPU" on real hardware" (`:18–19`); "it always tries to run the task with the smallest p->se.vruntime value (i.e., the task which executed least so far)" (`:45–47`); "the CFS scheduler has no notion of "timeslices" in the way the previous scheduler had, and has no heuristics whatsoever" (`:96–98`), beside "a few add-on embellishments like nice levels, multiprocessing and various algorithm variants to recognize sleepers" (`:51–53`). It replaced "the previous vanilla scheduler's SCHED_OTHER interactivity code" (`:13–14`).
- **EEVDF** (A5-03; `sched-eevdf.rst` at `7b63ef2d`, byte-identical to S2-03): "EEVDF aims to distribute CPU time equally among all runnable tasks with the same priority" (`:13–14`); it "picks tasks with lag greater or equal to zero and calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next" (`:18–20`); "tasks can request specific time slices using the new sched_setattr() system call" (`:30–32`).
- **Declarations:** Linux's scheduling classes, set by the program, its unit or a wrapper (D26); macOS's QoS classes, "Work that has no QoS information assigned is treated as default" (D28); a requested slice (EEVDF above).
- **Behaviour:** MLFQ's demotion by CPU used (OSTEP ch. 8; D18); Windows' boosts on I/O completion, foreground and input, decaying one level per slice (D29); XNU's usage-decayed thread priority inside its EDF-over-QoS hierarchy (D29).
- **What stands:** no scheduler knows a job's future length (OSTEP §7.9, p. 10; D32). **What leaves:** "every real scheduler is a guessing machine", "a pile of heuristics" — CFS's document says it has none, and part of what the schedulers act on is declared, not watched.
- **Restated:** no scheduler knows how long a job will run; each acts on what it has — the CPU a task has used against its fair share (CFS, EEVDF), what a program or its unit declares (a scheduling class, a QoS class, a requested slice), and recent behaviour (MLFQ's demotion, Windows' boosts, XNU's usage decay).

Hands to 9.15: `docs/research-proposal.md:89` restated as above.

Compiled effect: none.

## D87 — the MLFQ rules stated as OSTEP's revised Rule 4 and Rule 5, which the simulator implements; "slept before the slice ran out → stay high" stated with its accounting (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding: `docs/research-proposal.md:119–121` ("Used up your entire time slice? → probably batch → demote to a lower queue / Went to sleep for I/O before your slice ran out? → probably interactive → stay high / Periodically, boost everything back up so nothing starves forever"), `docs/background-guide.md:111–113` (the same three rules) and the rule text of `docs/background-guide.md:203`'s glossary row ("burn your whole slice → demoted (probably batch), sleep before it ends → stay high (probably interactive); periodic boost so nothing starves") are read against OSTEP and the project's simulator.

- **OSTEP ch. 8** (A5-04; Version 1.10, byte-identical to S1-02): the first attempt, p. 3 — "Rule 4a: If a job uses up its allotment while running, its priority is reduced (i.e., it moves down one queue)"; "Rule 4b: If a job gives up the CPU (for example, by performing an I/O operation) before the allotment is up, it stays at the same priority level (i.e., its allotment is reset)". Rule 4b can be gamed, p. 8: "Without any protection from gaming, a process can issue an I/O before its allotment ends, thus staying at the same priority level, and dominating CPU time." Revised, p. 8: "We thus rewrite Rules 4a and 4b to the following single rule: Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (i.e., it moves down one queue)." The boost, p. 6: "Rule 5: After some time period S, move all the jobs in the system to the topmost queue", by which "processes are guaranteed not to starve".
- **The simulator** (A5-05; `simulator/src/sim.cpp` at `a7ad2f29`, "The five textbook rules", `:173`): a full slice at a level demotes (`:214`); blocking "keeps both level and allotment" (`:221`); the CPU a task runs is charged to its allotment (`:231`) and its turn ends when the slice less the allotment is used (`:230`); every `boost_interval_us` all tasks return to the top queue with their allotments cleared (`:199–206`), 100 ms by default (`docs/recognition-vocabulary.md:113`). This is Rule 4 with the allotment equal to one slice, and Rule 5.
- **Restated:** used up your allotment at this level — a slice's worth of CPU, counted across every sleep along the way? → demoted (Rule 4); gave up the CPU before using it up? → stay at your level, the CPU you used still counted (Rule 4b's reset leaves, OSTEP's reason given); every boost interval, everything returns to the top queue, so no job starves (Rule 5).

Hands to 9.15: `docs/research-proposal.md:119–121`, `docs/background-guide.md:111–113` and `:203`'s rule text restated as above (`:203`'s "the default scheduler family real OSes use" is D29's). The guidebook vol-01 §10.7–10.9 states Rule 4b as the first attempt and its revision (`:2225`, `:2336–2348`) and stays.

Compiled effect: none.

## D88 — D14 amended: the premise's other lines — the proposal's §1.4 and Family 2 sentences, the claims page's thesis and pair, the background guide's MLFQ story; the past-10 ms shares of the pair the dataset carries (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D14 (scope-card items 6 and 47) on the 9.12 audit's coverage finding: lines that carry the premise D14 restated, and that D14 did not hand, are restated with it.

- **`docs/research-proposal.md:129`** — "A C++ compiler and a cryptocurrency miner both look like "CPU-bound." A file indexer and a chat client both look like "sleeps often, low CPU."" Measured (A5-10): the dataset's file indexer, Tracker's first index of a home, keeps its CPU about nine-tenths busy from the miner's `Initializing` (0.884–0.911 on one basis, D61; the 0.891–0.919 of `dataset/archetypes.yaml:1502` divides the whole job's CPU by the span after `Initializing`; 9.10 D81) and runs 0.844–0.849 of its CPU past a 10 ms slice without a voluntary block (`:1503`); the chat client, Element idle in one room, uses 0.088–0.114 % of its CPU at 12.0–12.6 wakes a second (`:771`; `meas-ci:desktop:2026-09-20`, 18 repeats). No cryptocurrency miner is read or measured; the compiler (`cc1`, D33) and the ML training run (D14) are, both keeping a CPU busy. Restated: a compiler and a training run both look CPU-bound; a chat client sleeps often at low CPU, the indexer does not once it is indexing — the training run and the indexer both keep a CPU busy, and differ in how their work is cut and in declared class (D14).
- **D14's "The share of each program's CPU past a 10 ms slice without a voluntary block: Tracker 0.530–0.536, `python3` 0.917–0.920 (9.6 D21)"** is of 9.6's measured phases — its Tracker rescan and its training-loop stand-in — not of the pair the dataset carries: the dataset's indexer (`file-indexer`, 9.10 D81) runs 0.844–0.849 of its CPU past the 10 ms slice (`dataset/archetypes.yaml:1503`), and its training run, PyTorch's basic MNIST example (9.10 D12, D87–D90), runs 69.49 s ±27.3 % between voluntary blocks (`:891`), nearly all of its CPU past any slice. D14's bullet restated to these.
- **`docs/research-proposal.md:617`** — "Pairs whose process sets and behavioural signatures are nearly identical and whose correct policies differ." Restated as D14 and D15 state the pairs: pairs of real jobs whose correct policies differ, which also differ in behaviour and declared class as measured; the pair tests what recognition adds over them.
- **`docs/research-claims.md:23`** — "On workloads where behaviour is identical and the correct policy differs, a language model reading process names recovers the difference, and a name whitelist cannot." "behaviour is identical" restated: workloads where the correct policy differs and neither behaviour nor declared class settles it (D14, D15); "a name whitelist" is D6's sweep.
- **`docs/research-claims.md:214–216`** — "Both are one sustained CPU-bound process beside an editor. No behavioural heuristic separates them, even in principle. The difference exists only in the names." Restated as D14 restates `docs/related-work.md:18` and `docs/research-proposal.md:627`.
- **`docs/background-guide.md:115`**, last sentence — "a wanted training run and an unwanted indexer behave identically, so MLFQ necessarily treats them identically" restated the same way (the sentence's 0.5 ms illustration is D33's).

Hands to 9.15: the five lines above restated as stated.

Compiled effect: none.

## D89 — D15 amended: "That difference appears only in the name" (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D15 (scope-card item 33) on the 9.12 audit's coverage finding: `docs/research-proposal.md:133`'s "That difference appears only in the *name*. That gap is the entire project.", which closes the download-against-scan paragraph D15 restated (`:131`), was not handed.

- D15: the pair's jobs differ in how their work is cut, in structure, in size and in declared priority; what they share is a busy CPU beside the game, and whether the user wants the work is stated by neither's behaviour.
- **Restated:** whether the user wants the work is not in its behaviour, and its declared class does not settle it; the name, read with what is known of the software, carries it — what recognition adds over behaviour and declared class is what the experiment measures (D14, D15). "appears only in the name" leaves.

Hands to 9.15: `docs/research-proposal.md:133` restated as above.

Compiled effect: none.

## D90 — D35 amended: what a missed deadline does, per kind — a late game frame waits for the next vertical blank, a late video frame is dropped, a late audio buffer is an xrun (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D35 (scope-card item 36) on the 9.12 audit's coverage finding: D35 restated the deadlines' lengths; the consequence clauses of the same lines — `docs/research-proposal.md:414` ("or a frame drops"), `:820` ("A game rendering at 60 fps has a 16 ms deadline every frame; missing it drops the frame") — and `docs/background-guide.md:207` ("each job must finish within its period or the frame drops / audio pops") are read against 9.11 D17's grounds (A5-07).

- **A game frame** (`vulkan`; Vulkan-Docs `e4e53e4b`, `chapters/VK_KHR_surface/wsi.adoc`): "VK_PRESENT_MODE_FIFO_KHR specifies that the presentation engine waits for the next vertical blanking period to update the current image" (`:4418–4419`); "one request is removed from the beginning of the queue and processed during each vertical blanking period in which the queue is non-empty" (`:4422–4424`); it is "the only value of pname:presentMode that is required: to be supported" (`:4425–4426`). A late frame is shown at the next vertical blank, the previous image held one more period.
- **A video frame** (`gstreamer`; `gstbasesink.c` at `83e7df91`, byte-identical to the registry's copy): "If the frame is later than max-lateness, the sink will drop the buffer without calling the render method" (`:123–124`).
- **An audio buffer:** an xrun, "clicks, pops and crackles" (D35; S2-57).
- 9.11 D17 kept the late-tick rule as GStreamer's sink for video playback and as design for the audio and game TIMER tasks.
- **Restated:** `:414` — MLFQ has no concept of a deadline: it knows priority, not "this must complete by the end of its period"; `:820` — a game rendering at 60 fps has a deadline every 16.7 ms; a frame that misses it is shown a vertical blank late under FIFO presentation, and a video sink drops a frame later than its allowed lateness; an audio buffer's miss is audible (D35); `docs/background-guide.md:207` — each job must finish within its period, or the frame is shown late or dropped, or the audio clicks.

Hands to 9.15: `docs/research-proposal.md:414`, `:820` and `docs/background-guide.md:207` restated as above, with D35's deadline lengths.

Compiled effect: none.

## D91 — D6 amended: "a faithful reproduction of what shipping systems do today" and "the whitelist approach real operating systems currently use" restated to the two conditions (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D6 on the 9.12 audit's coverage finding: `docs/research-proposal.md:60` ("Does the signal actually improve CPU scheduling, against a faithful reproduction of what shipping systems do today?") names no `whitelist`, so D6's sweep (`grep -rn -i whitelist docs`) does not reach it; `:216`'s "(b) the whitelist approach real operating systems currently use" is reached by the word, not by its clause. No operating system is documented as shipping a name table (D1); a Linux distribution, CachyOS, ships one enabled by default (D3).

- **Restated:** `:60` — against the name-keyed catalogue a shipping Linux distribution enables by default, and the strongest name table in its design (D3, D6); `:216` — (b) the same two conditions; "real operating systems currently use" leaves.

Hands to 9.15: `docs/research-proposal.md:60`, `:216` restated as above, with D6's sweep.

Compiled effect: none.

## D92 — D34 amended: "so the encoder must not drop frames" (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D34 (scope-card item 35) on the 9.12 audit's coverage finding: `docs/research-proposal.md:160`'s "There is no "gaming while streaming to Twitch, so the encoder must not drop frames" mode" carries the clause D34 restated at `:176`; D1 kept the line's "Game Mode is on or off".

- D34: an encoder that falls behind skips frames, which OBS counts and reports ("Skipped frames due to encoding lag", S2-55).
- **Restated:** there is no "gaming while streaming, so the encoder keeps its frame deadline" mode.

Hands to 9.15: `docs/research-proposal.md:160`'s clause restated as above.

Compiled effect: none.

## D93 — D32 amended: FIFO's "maximum cache locality" and the background guide's "real context switches trash CPU caches" stated to the measured cost (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D32 (scope-card item 31) on the 9.12 audit's coverage finding: `docs/research-proposal.md:416`'s FIFO row ("Throughput wants minimum context switching and maximum cache locality; MLFQ keeps interrupting") and `docs/background-guide.md:119`'s "no cache effects (real context switches trash CPU caches; our timetable doesn't model that)" carry the claim D32 restated at `:111`, and were not handed.

- **OSTEP §7.7, p. 8** (D32): switching "causes this state to be flushed and new state relevant to the currently-running job to be brought in, which may exact a noticeable performance cost".
- **Li, Ding & Shen** (A5-08; ExpCS '07, the copy the audit re-downloaded, SHA-256 `8b7a6069…`, equal to S1-21's): while every process's data fit in the 512 KB L2 cache, "context switch times ranging from 4.2µs to 8.7µs" — "the context switch does not cause any visible cache interference" (p. 2); when the communicating processes' data no longer fit, "from 38.6µs to 203.2µs" (p. 2); with a 128-byte access stride, "between 133.8µs and 1496.1µs" (p. 3).
- **Restated:** `:416` — a job switched out loses cache state it built, at a cost that depends on whether its data still fit in the cache and on how it accesses them; FIFO switches only when a job blocks or ends (the row's note on the simulator stands); `docs/background-guide.md:119` — a real context switch can cost the cache state a program built, nothing visible while the data fit in the cache, up to hundreds of microseconds or more when they do not; the timetable models none of it. "trash" leaves.

Hands to 9.15: `docs/research-proposal.md:416`'s first clause and `docs/background-guide.md:119`'s parenthesis restated as above.

Compiled effect: none.

## D94 — D1 amended: the macOS Game Mode row's versions — Game Mode on macOS Sonoma 14 or later; the `LSSupportsGameMode` declaration listed for macOS 26.0 and later (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D1 (scope-card item 21) on the 9.12 audit's coverage finding: D1 restated `docs/research-proposal.md:148`'s row ("macOS 14+ | Game Mode | Hardcoded detection of full-screen games") to "full screen, with the app's `LSSupportsGameMode` declaration"; D2 records the key as listed for macOS 26.0 and later. Apple's two pages re-read (A5-06).

- **Apple Support "Use Game Mode"** (support.apple.com/en-us/105118, byte-identical to S2-18): Game Mode requires a "Mac with Apple silicon and macOS Sonoma 14 or later and a game that supports macOS full-screen mode"; "When your game enters full screen, Game Mode automatically turns on for that game."
- **`LSSupportsGameMode`** (the developer documentation's JSON, byte-identical to S2-20): platforms iOS and iPadOS from 18.6, macOS from 26.0; "If you don't include this key in your Info.plist, Game Mode might not turn on for your game." The app-category key, `LSApplicationCategoryType` (macOS 10.0, its game categories listed), says nothing of Game Mode. How macOS 14 and 15 decide an app is a game is not stated in any page read.
- **Restated:** `:148`'s row — macOS (Sonoma 14 or later, Apple silicon) | Game Mode | turns on when a game enters full screen; from macOS 26 an app declares support with `LSSupportsGameMode`; how the system recognises a game is not documented. D2's related-work sentence already states both.

Hands to 9.15: `docs/research-proposal.md:148` restated as above, with D1's row restatement.

Compiled effect: none.

## D95 — "A CPU core runs exactly one thread at a time … hundreds of processes that could run" stated to the kernel's document and the dataset's session census (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding: `docs/research-proposal.md:79`'s "A CPU core runs exactly one thread at a time. But a typical machine has hundreds of processes that *could* run."

- **One task per CPU** (A5-02; `sched-design-CFS.rst:26–27`): "On real hardware, we can run only a single task at once, so we have to introduce the concept of "virtual runtime."" The kernel's unit is the CPU it schedules on, not the core.
- **How many** (A5-09; the 9.9 session census, `meas-ci:session:2026-09-24`, the 24 adopted repeats 47–49, 51, 58, 60–63, 68, 69, 71–77, 79, 83, 85–88, each the census at the start of `steady`, `dataset/tools/meas/session/census.py` at `a7ad2f29`): the idle, locked Ubuntu 24.04 GNOME session runs 66 processes with 319–321 threads in the user's session; the machine runs 125 user-space processes with 501–505 threads in all (the runner's own services among them), beside 113–118 kernel threads, on the EPYC 7763's four vCPUs.
- **Restated:** each CPU runs one task at a time; an idle desktop session on the dataset's machine holds about 66 processes and 320 threads, the machine about 125 processes and 500 threads beside some 115 kernel threads, and the scheduler chooses among those ready to run. "a typical machine has hundreds of processes that could run" leaves — hundreds of threads exist on the measured machine; how many are ready to run at once the census does not record.

Hands to 9.15: `docs/research-proposal.md:79` restated as above.

Compiled effect: none.

## D96 — the percentile sentences: "a good average with a bad P99 feels terrible" attributed to what Shneiderman's review finds; "reached roughly once per second" restated to the arithmetic (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the 9.12 audit's coverage finding: `docs/research-proposal.md:700`'s "Report percentiles, not just means. For interactive work the tail is the experience; a good average with a bad P99 feels terrible to a human." and `:953`'s "At 60 fps the 99th percentile is reached roughly once per second — often enough to be perceived as stutter while the mean still looks healthy."

- **Shneiderman** (A5-11; `shneiderman-csur84`, §5.3, p. 282, the 9.11 S1-07 copy, SHA-256 `7ea65246…`): "In summary, modest variations in response time (plus or minus 50 percent of the mean) appear to be tolerable and to have little impact on performance. As the variability grows, there may be some decrease in performance speed. Frustration may emerge only if delays are unusually long--at least twice the anticipated time." The studies reviewed in §5.2 used mean response times of 1 to 32 seconds.
- **The arithmetic** (`:953`): the 99th percentile is exceeded by one frame in a hundred; at 60 frames a second, 0.6 frames a second, one about every 1.7 s. No source read states the perception of a late frame.
- **Restated:** `:700` — report percentiles, not just means: a mean hides the rare long waits, and the review of response-time studies finds modest variation tolerable, with frustration emerging when delays are unusually long — at least twice the anticipated time (studies of second-scale responses); "feels terrible to a human" leaves. `:953` — at 60 fps one frame in a hundred, about one every 1.7 s, lands past the 99th percentile while the mean looks healthy; "often enough to be perceived as stutter" leaves. The rest of `:953` and the §6.1 requirement are design and stand.

Hands to 9.15: `docs/research-proposal.md:700`, `:953` restated as above; `shneiderman-csur84`'s role line gains §5.3 where the prose cites it.

Compiled effect: none.

## D97 — vol-02's quotations counted by D53's own rule: 277 passages, 238 exact, 39 differ, none missing; `:1032` re-graded, `:949` and `:582` re-described, `:1967` filed with `:865` (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D53 (scope-card item 60), on the 9.12 audit's re-check of the three readers' verdicts (A3-01, A3-02): all 38 "differs" re-read against their copies, 45 "exact" verdicts sampled character by character (Python `random.Random(20261009)`, one per source group and 13 more; all 45 confirmed), and all 239 "exact" verdicts machine-matched against their copies.

- **The counting rule**, stated: a block-quote line of `docs/guidebook/vol-02-related-work.md` whose text opens with a quotation mark (`^>\s*["“]`; 277 lines at `a7ad2f29`, the file unchanged since `2f7c7b58`), less `:3360` (the guidebook's own commentary, in Korean), plus the nested source quotation `:2715` (`> > "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."`); continuation lines (`:1119–1121`, `:3236–3237`, `:3250–3251`) belong to the quotation they continue. 277 passages: 92 in chapters 2–3, 133 in 4–6, 52 in 7–8. `:2609` — TuneAgent v1's title, quoted inline in the guidebook's "인용 정보 정정" callout — leaves the count under D53's rule ("the guidebook's own callouts excluded"); its text, checked exact by reader 2, stands. Reader 3's "the 51 entries … whose `sec` starts with 7. or 8." are 52 (23 in chapter 7, 29 in chapter 8); its count of 52 quotations stands.
- **Re-graded:**
  - `:1032` (ghOSt §1, p. 589) — exact → differs, markers only. The source: "…these overheads allow just a single ghOSt agent to schedule over 2 million threads per second (Fig. 5)."; the guidebook ends "…per second." with no elision mark — the class reader 1 graded differs at `:887`, `:931`, `:949`, `:993`.
  - `:1967` (ASA, Abstract) — "locator wrong" → exact, with a locator nuance, as `:867` is. The text is exact; `:1965`'s "초록의 첫 문장입니다" introduces the first sentence and the start of the second ("…This "one-policy-fits-all" approach leads to significant compromises in fairness, throughput, and latency", the source continuing ", particularly with the rise of heterogeneous hardware…"), as `:865`'s "논문의 초록 첫 문장입니다" introduces ghOSt's first two. It leaves D53's substantive corrections.
- **Re-described:**
  - `:949` (ghOSt §3, p. 591) — drops "[40]" and, at its end, "(see §3.4)": "…such as per-NUMA-socket or per-AMD-CCX [40]. Enclaves also help in isolating faults, limiting the damage of an agent-crash to the enclave it belongs to (see §3.4)."
  - `:582` (EEVDF TR, p. 3) — "virtual dead line" for "virtual deadline" is a spelling change, no word added or dropped: it moves from D53's substantive corrections to its small corrections, beside `:1048` and `:2551`; the fix is unchanged.
- **Counts** (277): exact 238 (83, 103, 52); differs 39 (9, 30, 0), 28 of them only dropping citation or cross-reference markers without an elision mark; not found 0. Substantive corrections: `:1080`, `:1867`, `:2579`, `:2568`. The claims around the quotes, the nuances (with `:1965` beside `:865`) and the registry points stand as D53 lists them.
- **"Seven code-block passages in chapter 7"**: six code blocks in chapter 7 (`:2864`, `:2878`, `:2925`, `:2944–2990`, `:3071–3074`, `:3082–3086`) and one inline output line in chapter 8 (`:3229`, `Time: 0.890`, `hackbench.8:72`), all exact.

Hands to 9.15: `docs/guidebook/vol-02-related-work.md` — `:1032` "(Fig. 5)" kept or its drop marked; `:949` both drops marked; `:865` "첫 두 문장", `:1965` the first sentence and the start of the second; `:582` "virtual deadline"; the rest as D53 lists them.

Compiled effect: none.

## D98 — vol-02's copies: two record copies gone, fixed captures kept; the copies V60 first recorded unchanged; the ghOSt repository gets an entry (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D53 (scope-card item 60), on the audit's provenance check (A3-03). D53's "Every copy equals its record's SHA-256 except two live pages whose quoted text is unchanged" is restated:

- **Two record copies are not on this machine as recorded.**
  - Nielsen (`nielsen-ue93`, `:698`): the 9.11 search record S1-05 gives `sources/S1-05/nngroup.html`, 120 613 bytes, SHA-256 `ee93bba73ca6307f8bdea3ba918d7959ef39a8c8cea6f43484b6ff078fc9ee83`; the file at that path is 121 941 bytes, `cd24ce28eaf2c4ded93a1a45ae9c2a939b896b30e9887ecd1d939c24785e43a8`, written 2026-10-07. V60's re-fetch is `075f609c…`. The fixed copy kept is the Internet Archive capture of the record's access date, `sources/nielsen-ue93/audit-2026-10-09/nngroup-wayback-20260924002157.html`, SHA-256 `e6a7eb4f888cfc9a58b8ee3b1d5a6883f1bf84b657c5f5d7d68f22084ae8324f`; "0.1 second is about the limit for having the user feel that the system is reacting instantaneously" and "Excerpt from Chapter 5 in my book Usability Engineering, from 1993" are in it verbatim.
  - Microsoft's Game Mode concept page (`gamemode-docs`, the twelve concept-page quotations of ch. 7.2): S2-16's copies (`sources/S2-16/`, the portal `20bb5394…17d0`) were made in the stage-2 sandbox and are not on this machine; V60's re-fetch is `d18e2969…`. The twelve are verbatim in V60's re-fetch, in the 2026-09-13 verification's copy (`_dev/research/jioh/2026-09-13-verification/sources/gamemode-docs/game-mode-portal.html`, `ea08757d68e15e1ea6ed66f3706646b3a06c366c2673c9213ac2548e9cf1cc74`) and in the fixed copy kept, the Internet Archive capture of 2026-09-07, `sources/gamemode-docs/audit-2026-10-09/game-mode-portal-wayback-20260907131311.html`, SHA-256 `329382052bc020258a9d3a616134c0137167cacec00ceb61df1d0d9638df62c3`.
- **Copies first recorded in V60** — no earlier record to equal; each re-hashed 2026-10-09 and equal to V60's record:
  - the ghOSt repository README, `google/ghost-userspace` at `9ca0a1fb6ed88f0c4b0b40a5a35502938efa567f` (2023-11-08; `sources/V60/ghost-sosp21/ghost-userspace/README.md`, `ebac49bb2f82a6f4ef17f133bee0285eb054ccbb4d73b623c4d5109c39e3e14a`) — the only source of `:873`, `:875`, `:911`, `:917`, `:955`, `:957`, `:975`, `:1003`, which vol-02 attributes to "저장소" (the repository);
  - Microsoft Learn's `ReleaseExclusiveCpuSets` page (`sources/V60/gamemode-docs/releaseexclusivecpusets.html`, `77de8a946e47b1796b16c2f8a722ac7167cff9c12fbbbb00b09826b16b6e5618`) — the only source of `:2777`;
  - rt-app's `README.in` at `d6f8be4` (`_dev/research/jioh/2026-09-13-verification/sources/rt-app/README.in`, `a35dec3593020b2fcb0be7ac17ede7c16c06e2a289623db3e582635ff3d3ad93`) — `:3299`;
  - SchedCP's arXiv e-print sources v1–v4 (`sources/V60/schedcp-mlsys25/eprint-v{1,2,3,4}.bin`: `df54a986…f791`, `3421050c…d327`, `3a1a1aaf…5939`, `289b0d4a…ca46`) — `:2457`, a line commented out in v1's and v2's `sections/evaluation.tex:13` (`% \item \textbf{RQ5}: How effectively can \sys understand workloads?`), as vol-02 says.
- **The ghOSt repository** is a citable artifact of its own — "A project with several citable artifacts (paper + slides + repo) gets several entries" (`docs/references.md`, the id-minting rule); the registry has the paper only (`ghost-sosp21`).

Hands to 9.15: `docs/references.md` — a deployed-system entry for the `google/ghost-userspace` repository pinned at `9ca0a1fb` (its README, SHA-256 `ebac49bb…`), cited by vol-02's eight README quotations; `nielsen-ue93`'s and `gamemode-docs`' status lines name the fixed captures above; `schedcp-mlsys25`'s status line names the e-print sources read for `:2457`; D53's `gamemode-docs` (the fifth page) and `rt-app` (`README.in`) points stand.

Compiled effect: none.

## D99 — the `gamemode` key: five Learn pages and the Xbox Support entry; D45's and D6's changes to D1, D2 and D5 marked (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D2 and D25 (scope-card items 16, 20), on the audit's finding that D45, D53 and D6 changed what D1, D2, D5 and D25 state without marking them.

- **`gamemode-docs`' pages.** D2 hands "the four Learn URLs of S2-16"; D25's map lists "`gamemode-docs` (Microsoft Learn, four pages)"; D53 adds the `ReleaseExclusiveCpuSets` page, the only source of vol-02 `:2777` ("After this function is called, the app will still have access to other Game Mode resources, such as increased GPU prioritization."). The entry's Learn pages are five: the Game Mode portal, the `expandedresources.h` header page, `HasExpandedResources`, `GetExpandedResourceExclusiveCpuCount` and `ReleaseExclusiveCpuSets`. S2-16 kept the first four; the registry's status line counts the portal and three function pages, as vol-02 `:2711` does — each a subset of the five.
- **D25's `gamemode` row**, restated: `gamemode-docs` (Microsoft Learn, five pages, the deprecation note carried), the Xbox Support article (D45, a deployed-system entry of its own) and Apple's two Game Mode entries — D1, D2, D45, D53.
- **D45's changes to D1 and D2**, marked: D1's §2.1 Windows row (`docs/research-proposal.md:148–149`) and D2's `docs/related-work.md:40` sentence gain the Windows Update deferral; D1's "The Xbox Support article (S2-17) renders by script and was not read" is superseded by S2-58, its rendered read.
- **D5's "which `whitelist` reproduces"** reads, after D6, "which the shipped-catalogue condition reproduces".

Hands to 9.15: `docs/related-work.md:54–73` — the `gamemode` row as above; `docs/references.md` `gamemode-docs`' cite line — the five Learn URLs in place of "[Exact URLs to pin.]" (D2).

Compiled effect: none.

## D100 — `lavd-ossna24`'s pairing clause leaves with `corbet-lwn24`'s "prose-citable" (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D11 (scope-card item 58): D11 restates `corbet-lwn24`'s role from "prose-citable secondary" to an attributed report, qualitative only, and leaves `lavd-ossna24` "unchanged". `lavd-ossna24`'s role (`docs/references.md:220`) ends "Talk slides — footnote tier despite carrying numbers; pair with `corbet-lwn24` for prose-citable coverage." After D11 every LAVD source is footnote tier and none is a prose-citable secondary, so the pairing clause leaves; "Talk slides — footnote tier despite carrying numbers" stays.

Hands to 9.15: `docs/references.md:220`'s last sentence as above, with D11's `corbet-lwn24` restatement.

Compiled effect: none.

## D101 — four pointers corrected: scope-card item 34, D15, D18 and D19's lines; the 9.7 D17 hand-off is `ananicy-rules`' (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the audit's locator check (A3-08); the claims the pointers carry are unchanged.

- **Scope-card item 34** cites `docs/research-proposal.md:315`, a blank line at `60149db`; the quoted text ("The Steam process is downloading, which / the user started deliberately") is at `:312–313`, where D16 places it.
- **D15** hands `:178`, a blank line; the sentence ("Rows 3 and 4 are the sharpest pair in the table: same process count, same behavioural signature, opposite correct policy") is at `:179`.
- **D18** hands "`docs/related-work.md:16`'s first sentence"; the sentence it restates is `:16`'s second ("Classic interactivity heuristics — MLFQ's demotion by CPU consumption, and the sleep/wake accounting behind CFS and EEVDF — classify tasks by how they use the CPU [mlfq, eevdf]"). **D19** hands "`:24`'s first sentence"; the sentence it restates is `:24`'s second ("Decima learns cluster scheduling policies via RL over job DAGs [decima]; Firm …; Park generalizes the setting [park]"). The first sentences — `:16` "Where situational awareness exists in deployed schedulers today, it is inferred from runtime behavior." and `:24` "A second lineage replaces hand-written heuristics with learned policies." — are restated by neither.
- **The 9.7 D17 hand-off** (`scope-card.md:15`, item 67) is attributed to `interbench`'s entry; 9.7 D17 (b) says it of `ananicy-rules`: "its `docs/references.md` entry stays while the scenario catalog and prose cite it (9.10, 9.12, 9.15)". Answered by D3 and D25: the related-work prose cites `ananicy-rules`, so its entry stays. 9.7 D17 (a) concerns `interbench`'s `sources.yaml` lines; the card's `interbench` answer (neither owned file cites it; the Role B prose and vol-02 ch. 8.3 do) stands as D47 records it.

Hands to 9.15: D15's, D18's and D19's lines as above.

Compiled effect: none.

## D102 — 9.10's hand-offs to 9.12 answered: which leaving and references-only entries the prose still cites; the workload-doc rows pass through (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the scope card's boundary ("9.10 D169/D170 (which references-only entries the prose still cites…)") and the "To 9.12" lines of 9.10 D12, D34, D90, D100, D111, D125 and D169, which no 9.12 decision acknowledged (A3-04, A3-05). "9.12's related-work and proposal prose" (9.10 D34) is read as the four owned files — `docs/related-work.md`, `docs/research-proposal.md`, `docs/research-claims.md`, `docs/background-guide.md` — and the guidebook's related-work volume, whose quotations the scope card puts in 9.12.

- **9.10 D34** ("Hands to 9.12: which leaving entries its prose still cites"; a leaving entry "keeps its `docs/references.md` entry, corrected to its verdicts, only where 9.12's related-work and proposal prose still cites it; otherwise 9.15 removes it"):
  - `procyon` — cited by vol-02 ch. 8.4 (`:3421`, `:3449`) and `:3897`. Its entry stays, corrected to its verdicts (D53: the page lists ten benchmarks, not nine). The workload docs cite it too: `docs/workload/source-vetting.md:42`, `:93`, `:114`; `grounding-sources.md:16`; `scenario-catalog.md:23`, `:33`.
  - `dkms-man`, `dkms-debian`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10` — cited by none of the four owned files nor vol-02 (each id and author or product name, `grep -i` at `60149db` and `a7ad2f29`: no line). 9.15 removes them under 9.10 D34, restating in the same edit the lines that still cite them: `docs/workload/scenario-catalog.md:22` (`dkms-man`, `dkms-debian`); `docs/workload/building-plan.md:82`, `:189`, `archetype-plan.md:40`, `measurement-overview.md:162`, guidebook vol-06 `:1162`, `:1180`, `:2519`, `:3954–3956` (the three tab-count entries). The dated memos keep their text.
- **9.10 D169** (`czerwinski-chi04`, `mark-chi08`, `mark-chi14`, `mark-gallup06`, `videogui-arxiv24`, "once 9.12 says which its prose still cites"): cited by none of the four owned files nor vol-02 — the scope card's answer (`scope-card.md:104`), confirmed at `a7ad2f29`. 9.15 corrects or removes them per 9.10 D169, `mark-gallup06` with the lines citing it (`docs/workload/source-vetting.md:76`, `building-plan.md:136`). The dropped `zhang-chb15`: cited by none (`scope-card.md:104`).
- **9.10 D12 and D90** (9.6 D32's wording rule restated on the new run; the scenario catalog's S12 row; `measurement-overview.md`'s venue and huge-page mode): the owned prose's wording is D14's — "an actual training run that does not claim desktop users train MNIST" (9.10 D12); the S12 row and `measurement-overview.md` pass through to 9.15 as 9.10 decided them, no owned sentence naming either (`grep -i "S12\|huge.page\|THP"`: no line).
- **9.10 D100** (the S8 row; "prose citing that workload as H.265"; `cpu-batch`'s scope): no doc names H.265 (`grep -rn -i "H\.265\|hevc\|x265" docs dataset/README.md`: no line); the S8 row and the scope pass through.
- **9.10 D111** (the S7 row; `building-plan.md` §3 C1 and C2 P3; `cpu-batch`'s scope) and **9.10 D125** (the S15 row; `building-plan.md` §3 C1, C2 P3 and C7's backup sentence; `measurement-overview.md`'s `file-backup` rows): workload-doc lines whose verdicts are 9.10's; no owned sentence names `kdenlive`, `ffmpeg`, `deja-dup`, `borg`, `cpu-batch` or `file-backup` (grep: no line); they pass through to 9.15. The owned prose's generic "a backup" and "a video encode" (`docs/research-proposal.md:97`) are D41's.

Hands to 9.15: `docs/references.md` — `procyon` kept and corrected; the five D34 entries removed with the lines listed restated; the D169 entries per 9.10 D169; the workload-doc lines of 9.10 D12, D90, D100, D111 and D125 as 9.10 decided them.

Compiled effect: none.

## D103 — item 63's pass-through lines handed (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D47 (scope-card item 63): D47 reads item 63's `docs/workload/grounding-sources.md:32` and hands "items 62 and 66–69's lines"; item 63's other lines, pass-through by the card, are in no hand-off: `docs/workload/source-vetting.md:47`, `:70`, `:95`, `:123`; `grounding-sources.md:15`; `archetype-plan.md:31`, `:39`, `:53–54`, `:86`; `building-plan.md:61–62`; `interpretation-contract.md:56`; `scenario-catalog.md:22` (K1 and K3 verdicts). C-schedcp-4 is D25's; C-kernelbuild-2 is D47's.

Hands to 9.15: item 63's lines above, applied from their recorded verdicts.

Compiled effect: none.

## D104 — citation forms: Li, Ding & Shen's DOI verified; Tam et al. and Atil et al. cited to their published versions; `schedcp-mlsys25`'s journal-ref quoted as the field reads (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the audit's citation check (A3-06): the scholarly entries D32, D40, D50 and D52 hand to 9.15, in the minting rule's form ("scholarly → `<label>-<venue><yy>` … arXiv-only works use `arxiv` in the venue slot", `docs/references.md`).

- **Li, Ding & Shen** (S1-21; D32, D50): the DOI 10.1145/1281700.1281702, recorded "from search-result listing; not on the copy", is verified at Crossref (2026-10-09; `sources/S1-21/audit-2026-10-09/crossref-1281700.1281702.json`, SHA-256 `83081c17e17ffcb2cdb5f102eefccdb621a4af8f6941787220eeaad74d58fdc8`): "Quantifying the cost of context switch", *Proceedings of the 2007 workshop on Experimental computer science* (ExpCS07, 2007-06-13), article 2; Li, Ding, Shen. Id `li-expcs07`.
- **Tam et al.** (S1-27; D40): arXiv 2408.02442v3 states no venue; Crossref lists the paper in *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track*, pp. 1218–1236, DOI 10.18653/v1/2024.emnlp-industry.91, titled "Let Me Speak Freely? A Study On The Impact Of Format Restrictions On Large Language Model Performance." (record SHA-256 `6b87fa0c83ca2c193ef43b030a942fbc20f9a9966cba2e4b9560c5a85723bc32`). The ACL Anthology copy (`sources/S1-27/audit-2026-10-09/2024.emnlp-industry.91.pdf`, SHA-256 `c8145f4d94b4112833a3f6f90535a60671864408dce0d0479d2fb6e6bdf80d6e`) carries D40's passage verbatim on p. 1224 — "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy." — and the key-order finding on p. 1221 — "…placed the "answer" key before the "reason" key, resulting in zero-shot direct answering instead of zero-shot chain-of-thought reasoning." Id `tam-emnlp24`, cited to the published version, D40's locator "arXiv 2408.02442v3, p. 7" read as p. 1224.
- **Atil et al.** (S1-25; D52): arXiv 2408.04667v5 states no venue; Crossref lists *Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems* (Eval4NLP 2025), pp. 135–148, DOI 10.18653/v1/2025.eval4nlp-1.12, titled "Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments" (record SHA-256 `0a6d98a0dfee363c2ab6376c78d10e72049cf52aab3361a49bfe144e0b29ca31`). The ACL Anthology copy (`sources/S1-25/audit-2026-10-09/2025.eval4nlp-1.12.pdf`, SHA-256 `d94638d0e14f1e936cb3c980427221a588628c53d5f8075b81206b2e9b56adc5`) carries D52's claim: "Experiments reveal accuracy variations of up to 15% across runs" (Abstract, p. 135), "We set temperature at 0, top-p at 1, and we fix the seed." (p. 138), its models API-based ("We apply five API-based LLMs configured to be deterministic", p. 135). Id `atil-eval4nlp25`, cited to the published version, its models described as hosted.
- **`schedcp-mlsys25`'s cite line** reads "ML for Systems 2025 (arXiv journal-ref)"; the field on arXiv's abstract page reads "MLforSystem 2025" (`sources/V60/schedcp-mlsys25/abs.html`; D53). The cite names the venue as D25 does — the NeurIPS 2025 Workshop on ML for Systems, as the NeurIPS virtual site lists it — and where it gives the journal-ref field, quotes "MLforSystem 2025".

Hands to 9.15: `docs/references.md` — `li-expcs07`, `tam-emnlp24` and `atil-eval4nlp25` minted as above where the prose cites them (D32, D40, D50, D52); `schedcp-mlsys25`'s cite line restated.

Compiled effect: none.

## D105 — D6's open points: ananicy-cpp matches a rule by `argv[0]`'s basename, untruncated; the rest homed with the build of the two rule lists (2026-10-09)
> Amended by D109 (the recount on that key: 19 of 35, 7 of 50 files).

Taken under 인지오's delegation (2026-10-09), amending D6, on the audit's finding that D6's open points have no home (A3-07).

- **How ananicy-cpp names a process** (D6: "the 15-character `comm` or the executable's basename … (not read; S3-19)"), read at tag `v1.2.0` (`cf5ac2eb`, 2026-03-26), the version CachyOS's ISO installs (S2-46; its pacman record: `ananicy-cpp` `1.2.0-1`, packager Peter Jung `<ptr1337@archlinux.org>`, depending on `pcre2` and `libbpf`). `get_command_from_pid` (`src/platform/linux/process.cpp:193`) returns, in order: the basename of the first `/proc/<pid>/cmdline` argument ("Cmdline method", `:197`, `find_last_of('/')` at `:201`); failing that, the basename of the `/proc/<pid>/exe` link ("Exe method", `:217`); failing that, `/proc/<pid>/comm` ("Comm method", `:250`). A name ending `.exe` is cut to its file name (`:61–64`). The rule is looked up by that name exactly (`src/rules.cpp:184`, `m_program_rules.contains(name)`; called at `src/worker.cpp:80`). A `name_regex` fallback (`rules.cpp:186`) is compiled only with `ENABLE_REGEX_SUPPORT` (default `OFF`, `cmake/StandardProjectSettings.cmake:40`), which Arch's `ananicy-cpp` 1.2.0-1 build turns on (`-DENABLE_REGEX_SUPPORT=ON`); the catalogue at `03ef03fb` carries no `name_regex` rule. A matched rule's nice value is set on every thread of the process (`src/platform/linux/priority.cpp:41–50`, over `/proc/<pid>/task`). These files are the same at `3554447c` (S2-31) but for one `#include`.
  So the shipped catalogue matches a rule's `name` against the process's `argv[0]` basename, untruncated, and applies it to the process's threads; a thread's own name (`dxvk-cs`, `Task worker thr`) is never the key. The dataset binds `comm`-style names (`tracker-miner-f`, `thunderbird-bin`, the game chain's threads; S3-19): the shipped-catalogue list is built by mapping each bound task to its process's `argv[0]` basename before the lookup, and S3-19's 14-of-35 exact matches and "none more after truncation" are a count on the dataset's names, not on the key ananicy-cpp uses.
- **Homed:** the two conditions' identifiers — 9.14 (D6, D54); the type-to-vocabulary mapping, the strongest table's names at the familiarity tiers' boundary, and the name mapping above — the build of the two rule lists, which has no phase yet; its owner is the whitelist baseline's, 박이안 (`docs/research-proposal.md:538`, `:755`).

Hands to: `_dev/TODO.md` — a line for the build of the two rule lists carrying the three points above (the coordinator places it).

Compiled effect: none.

## D106 — two stale clauses of the 9.15 line: 9.6 D32's training-run wording and 9.10 D169's wait (2026-10-09)

Taken under 인지오's delegation (2026-10-09), on the audit's consistency finding: two clauses of `_dev/TODO.md`'s 9.15 line still carry instructions later decisions replaced.

- **"from 9.6 (D32): text naming the `python3` binding of `cpu-batch` calls it a CPU-saturating training-loop stand-in, never an observed ML training workload"** — 9.10 D12 replaced the synthetic loop with PyTorch's basic MNIST example: "The files show an actual training run and do not claim that desktop users train MNIST." D14 states the owned prose that way, and D54 marked 9.6 D32 answered on 9.12's line; 9.15's clause was left. It becomes 9.10 D12's rule: an actual training run, PyTorch's basic MNIST example on the CPU, without the claim that desktop users train MNIST.
- **"from 9.10 (D169): … once 9.12 says which its prose still cites (D34's split)"** — answered by D102: the owned prose cites none of the five.

Hands to: `_dev/TODO.md` 9.15 line — the two clauses as above.

Compiled effect: none.

## D107 — D51 amended: the published latency figures stated as their pages compute them — Artificial Analysis's per-provider 72-hour medians, 0.66–1.14 s to first token on a ~10 000-token prompt as read 2026-10-07; LocalScore's 0.88 s the 12 GB RTX 3060's mean over submitted runs (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D51 (scope-card item 29) on the 9.12 audit's re-read of S3-05 and S3-18 (A2-21). D51 said: "LocalScore's crowd-submitted runs of Llama 3.1 8B Q4_K_M give an RTX 3060's average time to first token as 0.88 s, averaged over nine tests of 16–4 096 prompt tokens (S3-05) … the one hosted figure found is a ~10 000-token prompt's 0.84 s to first token on Groq (S3-18)".

- **Artificial Analysis** (S3-18): "Figures represent median (P50) measurement over the past 72 hours to reflect sustained changes in performance." The page gives one median per provider; as read 2026-10-07 (S3-18): CoreWeave 0.661 s, Groq 0.840 s, Novita 0.913 s, DeepInfra 1.074 s and 1.143 s (Turbo, FP8). The figures move: Groq 0.922 s in the capture of 2026-09-26 and 0.870 s live on 2026-10-09, CoreWeave 0.711 s and 0.658 s (A2-21). The 2026-10-07 copy is not on this machine and no capture lies nearer than 2026-09-26, so the record's values stand as read on its date.
- **LocalScore** (S3-05): the 0.88 s is the 12 GB "NVIDIA GeForce RTX 3060" (accelerator 43), 881.7 ms in the capture of 2026-09-26 and live on 2026-10-09; an 8 GB RTX 3060 is listed separately. The site's figure for a card is a mean over the runs submitted for it (`cjpais/LocalScore` at `bd6ffe9d`, `src/db/queries.ts:816`), each run's value the mean of its nine tests (llamafile `localscore/localscore.cpp:293–328` at `a3ccf098`); how many runs stand behind it the page does not show.
- **Restated D51's "Elsewhere":** LocalScore's submitted runs of Llama 3.1 8B Q4_K_M give the 12 GB RTX 3060 a time to first token of 0.88 s, a mean over the runs submitted, each the mean of nine tests of 16–4 096 prompt tokens; no hosted API was measured — Artificial Analysis's 72-hour medians of time to first token on a ~10 000-token prompt ran from 0.66 s (CoreWeave) to 1.14 s across the providers listed on 2026-10-07, Groq's 0.84 s.

Hands to 9.15: `docs/references.md` — LocalScore and Artificial Analysis, where the prose cites them, with the date read and the window each figure is computed over.

Compiled effect: none.

## D108 — batch: the audit's hand-off pointers (2026-10-09)

Taken under 인지오's delegation (2026-10-09), stage 4, as D54: D55–D107's hand-offs reach their tasks through `_dev/TODO.md`.

- **9.14** — D59: `pool.py` keys the LLM values by the formatted prompt's hash if the campaign is re-pooled, and the 8B's runner figures read the 9 Oct prompt alone (43.18 s, the reasoning field 6.81 s); D60: the latency figures carry their scope — one Apple M1 Pro, one stand-in request, an answer that stops at `system` — and Layer 1 measures the recognizer's real prompt with its `subsystems` block; D71: the with/without-`reasoning` comparison holds only if `reasoning` is generated before `system`; D105: the build of the two rule lists (no phase yet; with 박이안) carries the type-to-vocabulary mapping, the strongest table's names at the familiarity tiers' boundary, and each bound task mapped to its process's `argv[0]` basename before the catalogue lookup.
- **9.15** — every "Hands to 9.15" of D55–D107. The 9.15 line states that the changelog's "Hands to 9.15" lines of D1–D107 are the complete list and names the files and registry entries they touch; D106's two stale clauses are replaced.

Applied: `_dev/TODO.md` — the 9.14 and 9.15 lines.

Hands to: as listed.

Compiled effect: none.

## D109 — D6 amended: on ananicy-cpp's key the catalogue keys 19 of the 35 bound names, and every name in 7 of 50 files — a different seven; "after truncation" leaves (2026-10-09)

Taken under 인지오's delegation (2026-10-09), amending D6 (scope-card item 21) and D105 on the 9.12 audit's recount of S3-19 on the key ananicy-cpp 1.2.0 looks up (A3-09). D6 said: "of the 35 process names the 50 compiled core-set files bind, the catalogue at `03ef03fb` carries 14 exactly and none more after truncation to 15 characters; every name of a file is carried in 7 of 50 files. Unmatched include `kdenlive`, `make`, `python`, `HandBrakeCLI`, `deja-dup`, `tracker-miner-f`, `thunderbird-bin` and most of the game chain's threads." D105 read the key: the basename of the process's `argv[0]`, untruncated, the rule applied to every thread of the process.

- **The recount** (A3-09): each of the 35 names mapped to the process it stands for in the measured runs, and that process's `argv[0]` basename looked up exactly. Four are invented names with no process (`audio-stream-he`, `video-playback-`, `qzvd`, `xkrr`; `dataset/timelines/coreset/c5.variant.yaml`). 19 are keyed:
  - twelve through their program's own entry — `7z`, `baloo_file`, `code`, `element-desktop`, `gimp`, `gnome-shell`, `mpv`, `pipewire`, `soffice.bin`, `steam`, `Troy.exe`, `wineserver`;
  - six game-chain thread names — `dxvk-cs`, `dxvk-submit`, `FAudio_AudioCli`, `Task worker thr`, `winepulse_mainl`, `winepulse_timer` — through their process's `Troy.exe` entry, which takes the `.exe` cut of ananicy-cpp's BPF build (`src/platform/linux/process.cpp:61–65`, under `USE_BPF_PROC_IMPL`; off by default, on in Arch's 1.2.0-1 build); without the cut the game's Windows-path `argv[0]` is not keyed and these seven fall out;
  - `dkms` through `bash`, its interpreter (`#!/bin/bash`) — the interpreter's rule, not its own.
- **Not keyed:** `chrome` — the browser runs as `/usr/bin/google-chrome` (the catalogue has `chrome`, not `google-chrome`) and its children under titles Chromium rewrites; `dbus-daemon` — the carried system bus runs as `@dbus-daemon` (the session bus, `/usr/bin/dbus-daemon`, is keyed: 20 with it); `thunderbird-bin` (the catalogue has `thunderbird`); `tracker-miner-f` (`tracker-miner-fs-3`); `unattended-upgr` (`python3`, its interpreter); `python`; `systemd`; `make`; `kdenlive`; `kdenlive_render`; `HandBrakeCLI`; `deja-dup`.
- **Files:** every bound name keyed in 7 of 50 files — c1-dev, c1-gaming, c1-media, c1-photo, c2-p2a, c4-gaming, c7-compile; S3-19's seven were c1-browsing, c1-dev, c1-media, c1-meeting, c1-photo, c6-fold, c6-spoof.
- **Not established** (A3-09): no cmdline was captured for the game chain or `wineserver`, whose rows rest on Wine's source and the LAVD slide's thread list; VS Code's main process is taken as not retitled, as Chrome's and Element's main processes are not under the same harness; a launch through a `.desktop` Exec line was not read.
- **Restated D6's bullet:** of the 35 process names the 50 compiled core-set files bind — four invented, with no process — mapped to the `argv[0]` basename of the process each stands for, the key ananicy-cpp looks up, the catalogue at `03ef03fb` keys 19, six of them game threads through their game's entry and `dkms` through its interpreter's; every bound name of a file is keyed in 7 of 50 files. Unkeyed include `chrome` (run as `google-chrome`), `thunderbird-bin`, `tracker-miner-fs-3`, `kdenlive`, `make`, `python`, `HandBrakeCLI` and `deja-dup`. "none more after truncation to 15 characters" leaves: ananicy-cpp does not truncate. D6's case — the shipped catalogue is not the strongest name table — stands on the unkeyed names.

Applied: `search/S3-traces-datasets.md` — the audit note on S3-19 points here; `_dev/TODO.md` — the 9.14 and 9.15 lines' audit ranges extended to D109.

Hands to 9.15: wherever the prose states the catalogue's coverage of the dataset, the figures above. **9.14:** the build of the two rule lists (D105) maps each bound task as above.

Compiled effect: none.

## D110 — the laptop measurement gets a registry form, `meas-local`, its records released with the hostname removed; the laptop figures stay with their scope (2026-10-09)

By 인지오's decision (2026-10-09), on the 9.12 audit's finding that the laptop figures of D50 and D51 (S3-22) have no form under the id rule: the rule types a source as scholarly, deployed-system, or measurement → `meas-ci`, "with campaign identification in the locator" and "its raw records are one release" (`docs/references.md:14`); `meas-ci`'s role admits "machine-relative absolutes [that] carry the runner spec" (`:505`). S3-22 is the runner campaign's request run five times on 인지오's Apple M1 Pro, not a CI campaign, and its records are not released (`machine.txt` carries the machine's hostname).

- **Decided:** a measurement on a named local machine is minted as `meas-local`, its locator `meas-local:<machine>-<subject>:<date>`, the date the run started (UTC) as for a `meas-ci` campaign; as with `meas-ci`, its raw records are one release, the machine's specification is stated with every figure, and its spread over its repeats is reported. S3-22 is `meas-local:m1pro-llm:2026-10-08`.
- **The records prepared:** S3-22's 55 files with two substitutions — the earlier session's scratch path of the model files → `<models>/`, the machine's hostname → `<host>`. 21 files change (the bench JSON, the server logs, `machine.txt`); the request records, `summary.txt`, `loads.txt` and the scripts are byte-identical to the record's copy. `MANIFEST.txt` lists each file's SHA-256 before and after. Archive `meas-local-m1pro-llm-2026-10-08.tar.gz`, SHA-256 `0f41f42b89fd1913f2dad827be9bfa7fb8bc7eb2a5a794df997e2b614e858ada`, published on 인지오's go-ahead (2026-10-09) as the GitHub release `meas-local-m1pro-llm-2026-10-08`, tag at `58c909fb`; GitHub's asset digest equals the archive's SHA-256.
- **The laptop figures** stay in D50's and D51's restatements with D60's scope: one Apple M1 Pro with Metal and its own work beside it, one stand-in request, the answer stopping at `system`, five repeats with their spread — one machine's observation, not a campaign held to the 5 % rule.

Hands to 9.15: `docs/references.md` — the id rule gains `meas-local` as above; a `meas-local` entry whose role admits machine-relative absolutes stated with the machine's specification and spread, never as a population's figure; the laptop figures cited `meas-local:m1pro-llm:2026-10-08`.

Compiled effect: none.

## D111 — related-work cites TuxBot, LumOS and Vulcan, each by what it does, without superlatives (2026-10-09)

By 인지오's decision (2026-10-09), amending D42 (scope-card items 48, 49) on the 9.12 audit's question whether the owned prose cites these works at all (D42 took it under delegation; the card had recorded "Cited by owned prose? no" for items 48 and 49) and its full read of LumOS (S1-20, A2-17).

- **TuxBot** (S1-17, A2-16): an LLM tuning up to 41 Linux parameters online, "out of band", "not kernel fast-path controllers such as the CPU scheduler, a packet scheduler, or a TCP congestion controller" (v2 p. 1), on hosted Gemini 2.5 Flash and Flash-Lite, each change through typed validation.
- **LumOS** (S1-20, A2-17; Liargkovas, Jabrayilov, Franke and Kaffes, "An Expert in Residence: LLM Agents for Always-On Operating System Tuning", NeurIPS 2025 Workshop: Machine Learning for Systems; read from the authors' PDF linked from the project page, a draft-watermarked copy, OpenReview returning 403): an LLM loop (Gemini 2.5 Flash) adjusting CFS's `latency_ns` and `min_granularity_ns` online to minimise a PostgreSQL workload's p99 latency, one proposal per "10-second workload run" (p. 2), "reduces p99 by 5.0% in 1-parameter tuning … and by 7.1% in 2-parameter tuning" against Bayesian optimisation (p. 3).
- **Vulcan** (S1-18, A2-15): offline LLM synthesis of small policy functions, evaluated on spot-VM scheduling, cache eviction and tiered memory (§3.2); CPU scheduling an example task in its interface table (v3 Table 1), not evaluated; its cite line as D42 and D72 state it — the arXiv id, the DOI left out until it resolves.
- **Decided:** `docs/related-work.md` cites all three, each by what it does — TuxBot and LumOS beside the adjacent LLM tuning efforts (D24) as LLM tuning of a live host's parameters out of the fast path, LumOS the scheduler instance; Vulcan beside the synthesis line, its evaluated domains named — with no superlative. None measures recognition, so D12's scoped claim stands.

Hands to 9.15: `docs/related-work.md:32`'s sentences as above (with D42's and D72's restatements); `docs/references.md` — `tuxbot-arxiv26`, `vulcan-arxiv25` (D42, D72) and an entry for LumOS under the id rule, the workshop the same as `schedcp-mlsys25`'s, its status naming the copy read (the authors' draft-watermarked PDF; OpenReview unreachable on 2026-10-09).

Compiled effect: none.

## D112 — the citation-tier rule: a deployed-system source may support its own documented design or behaviour, attributed at its pinned version, and a figure it publishes as its report with date, window and computation (2026-10-09)

By 인지오's decision (2026-10-09), amending D44 (scope-card items 56, 57) on the 9.12 audit's finding that the citation-tier rule — deployed-system: "footnote with URL + accessed date + pinned version. Supports **existence claims only** ("this scenario/setting/category exists in shipped software") — never behavioral or statistical claims"; "An entry's `role:` line states what claims it may support; do not cite outside the role" (`docs/references.md:20–22`) — is exceeded by sentences 9.12's decisions ground on deployed-system sources:

- **Documented design or behaviour:** the kernel's sched_ext documentation, "The system integrity is maintained no matter what the BPF scheduler does" (`schedext-docs`, D7); scx_lavd's mechanism from its README and `lat_cri.bpf.c` (`scx`, D10, D44); who sets a Linux scheduling class (man-pages, D26); undeclared work running as `default` (Apple's QoS page, D28); Game Mode holding back Windows Update's driver installs and restart notifications (the Xbox Support article and Xbox Wire, D45, D74).
- **Published figures:** LocalScore's 0.88 s for the 12 GB RTX 3060 and Artificial Analysis's per-provider 72-hour medians (D51, D107).
- **Decided:** the rule admits, beside existence claims, (i) a deployed system's own documented design or behaviour, stated as that source's at its pinned version or accessed date ("the kernel's documentation states …"), and (ii) a figure the source publishes, stated as its report with the date read, the window and how it is computed (D107's form); never a behavioural or statistical claim stated as the paper's own or as a population's. The sentences above stand in their attributed form.

Hands to 9.15: `docs/references.md:20–22` — the deployed-system tier restated as above; the role lines of `schedext-docs`, `scx`, the man-pages, Apple's QoS, Microsoft's Game Mode and Xbox entries, LocalScore and Artificial Analysis stating which design statements or figures each supports, attributed.

Compiled effect: none.

## D113 — the id rule gains a type for talks, conference abstracts and news reports: `<label>-<venue><yy>`, footnote tier, their claims the speaker's or reporter's (2026-10-09)

By 인지오's decision (2026-10-09), amending D8 and D11 (scope-card items 3, 58) on the 9.12 audit's finding that the id rule (`docs/references.md:10–16`: scholarly, deployed-system, measurement) has no type for a talk, a conference abstract or a news report, while two entries already are one — `lavd-ossna24` (Min's OSS NA 2024 talk slides; its role "Talk slides — footnote tier despite carrying numbers") and `corbet-lwn24` (an LWN article), both with scholarly-form ids in the deployed-system section (`:218–227`) — and D8 and D11 hand three more "as `lavd-ossna24`": the LPC 2024 slides "sched_ext status and plans", the LPC 2025 abstract on Meta's Reality Labs fleet, LWN 1051430.

- **Decided:** a fifth type, talk, conference abstract or news report → `<label>-<venue><yy>`, the label the speaker's or author's surname or the system's name; footnote tier; its claims stated as the speaker's or reporter's (D11: "LWN articles carry only what they report, attributed as reports"), never as the paper's own; a number it carries stated only as its report, with its date (D112's published-figure clause).
- `lavd-ossna24` and `corbet-lwn24` are this type; the three handed entries are minted under it.

Hands to 9.15: `docs/references.md` — the id rule (`:10–16`) and the citation-tier rule (`:18–22`) gain the type as above; `lavd-ossna24` and `corbet-lwn24` moved to it; the LPC 2024 slides, the LPC 2025 abstract and LWN 1051430 minted under it (D8, D11).

Compiled effect: none.

## D114 — §4.7 stays as D30 and D79 state it; `:756`, 인경민's team area, leaves 9.12's restatements (2026-10-09)

By 인지오's decision (2026-10-09), amending D30 (scope-card item 71) on the 9.12 audit's question about its two lines: D30 removed `docs/research-proposal.md:473`'s "It cannot remove starvation protection" from §4.7's list and stated what holds (D79: the cap the driver table's under every condition but `llm_full`, to be enforced, not yet; no executor starvation window; FIFO and EDF's deadline class without a horizon; the idle class's wait by design; the 30 s `starvation_floor` guard), and restated `:756`'s "Bandwidth caps and starvation protection" in 인경민's area (§8.1) to "the batch class's bandwidth cap". The scope card's boundary puts team areas outside 9.12 ("Not 9.12: the proposal's design statements (vocabulary, validator, conditions, metrics definitions, milestones, team areas)"); 9.11 D19's hand-off named the line.

- **Decided:** §4.7 as D30 and D79 state it. `:756` is a team assignment, left to 인지오 and 인경민; it leaves D30's hand-off. No executor starvation bound is stated as planned (9.11 D7 took no executor net; 9.11 D19 reconsiders one with 인경민 only if 9.14's dry runs show waits near 30 s).

Applied: `_dev/TODO.md` — the 9.15 line's "§4.7 starvation protection and §8.1's duty (D30)" → "§4.7 starvation protection (D30, D79)".

Hands to 9.15: `docs/research-proposal.md:473` and `:287` as D30 and D79 state them; not `:756`.

Compiled effect: none.

## D115 — `:536`'s "the one that matters most … Beating it is the claim" restated per condition: the shipped catalogue answers RQ2, the strongest name table carries the claim (2026-10-09)

By 인지오's decision (2026-10-09), amending D6 (scope-card item 21) on the 9.12 audit's finding that no decision says which of D6's two conditions `docs/research-proposal.md:536` refers to: "The `whitelist` condition is the one that matters most for the paper. It is not a strawman we invented — it is what shipping operating systems actually do today. Beating it is the claim; failing to beat it is a legitimate finding." D6's conditions: the shipped catalogue (`ananicy-rules` at `03ef03fb`, as CachyOS installs and enables it; on ananicy-cpp's key 19 of the 35 bound names, D109) and the strongest name table in the catalogue's design. RQ2 asks "Does that reading beat what shipping systems do?" (`docs/research-claims.md:128`); `docs/research-proposal.md:538` and `:758` call the whitelist baseline "the strongest counter-hypothesis".

- **Decided:** `:536` is restated per condition — beating the shipped catalogue answers RQ2, a comparison with what a deployed daemon does on a distribution that enables it (D1, D3); beating the strongest name table is the paper's claim, "the one that matters most"; failing to beat either is a finding. "what shipping operating systems actually do today" is D1's and D3's restatement.

Hands to 9.15: `docs/research-proposal.md:536` restated as above; `docs/research-claims.md:128–132` ("The second is the claim") per condition with it.

Compiled effect: none.
