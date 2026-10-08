# Task 9.12 — Related-work and proposal prose: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — `whitelist` reproduces the name-keyed catalogue, `ananicy-rules`; Game Mode is cited for its category only (2026-10-08)
> Amended by D3 (CachyOS installs ananicy-cpp with the catalogue and enables it by default: the design point ships in a distribution; `:536` and the `whitelist` lines restated to it).
> Amended by D6 (the `whitelist` condition becomes two conditions: the shipped catalogue, and the strongest name table in its design).

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

By 인지오's decision, scope-card item 4 (and the `mlfq` and `eevdf` keys of item 20): `docs/related-work.md:16`'s "Classic interactivity heuristics — MLFQ's demotion by CPU consumption, and the sleep/wake accounting behind CFS and EEVDF — classify tasks by how they use the CPU [mlfq, eevdf]" keeps MLFQ as a classifier and restates CFS and EEVDF as accounting.

- **MLFQ** (`ostep`, ch. 8, Version 1.10; S1-02): "If, for example, a job repeatedly relinquishes the CPU while waiting for input from the keyboard, MLFQ will keep its priority high … If, instead, a job uses the CPU intensively for long periods of time, MLFQ will reduce its priority" (p. 2); Rules 4a/4b (p. 3), revised to Rule 4: "Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced" (p. 8). The original (`corbato-sjcc62`; S1-04, printed p. 341–342): a program not done within 2^ℓ quanta moves to level ℓ+1, and "the level classification procedure for programs is entirely automatic, depending on performance and program size rather than on the declarations (or hopes) of each user".
- **CFS** (`Documentation/scheduler/sched-design-CFS.rst` at mainline `7b63ef2d`; S2-04): "CFS basically models an "ideal, precise multi-tasking CPU" on real hardware" (`:18–19`); "has no heuristics whatsoever" (`:96–105`), beside "various algorithm variants to recognize sleepers" (`:51–53`) in the same document.
- **EEVDF** (`sched-eevdf.rst` at `7b63ef2d`, S2-03; `eevdf-tr95`, S1-05): a virtual run time and a lag per task, the eligible task with the earliest virtual deadline run next, "latency-sensitive tasks with shorter time slices" favoured (`:13–22`); a sleeping task's lag decays (`:24–32`). The report bounds the lag by a quantum (Corollary 2, p. 20) and leaves the compensation of a rejoining client a policy choice (§5, p. 11–12).
- **The key map:** `mlfq` → `ostep` with `corbato-sjcc62`; `eevdf` → `eevdf-tr95` with the kernel's `sched-eevdf.rst` and `sched-design-CFS.rst`.

Hands to 9.15: `docs/related-work.md:16`'s first sentence restated as above, its keys resolved; the guidebook vol-02 ch. 2.2 and 2.5 checked against the same passages (item 60).

Compiled effect: none.

## D19 — the learned-scheduler sentence: Decima and FIRM kept; Park restated as an open platform of twelve environments (2026-10-08)

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
