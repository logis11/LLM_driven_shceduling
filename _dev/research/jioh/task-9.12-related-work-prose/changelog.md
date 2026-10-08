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

Taken under 인지오's delegation (2026-10-09), scope-card item 31: `docs/research-proposal.md:87`, `:95`, `:111` and `:113` are restated to their sources. OSTEP's chapters 7 and 8 re-read from copies byte-identical to S1-03 and S1-02 (SHA-256 `0912b1a3…`, `96241b4e…`; re-downloaded 2026-10-09).

- **SJF's optimality** (`:87`: "The theoretically optimal policy — Shortest Job First — requires knowing job lengths in advance, which nobody ever does"). OSTEP §7.4, p. 5: "given our assumptions about jobs all arriving at the same time, we could prove that SJF is indeed an optimal scheduling algorithm" (for turnaround, under §7.1's five assumptions, p. 2); §7.5, p. 6: "STCF is provably optimal". §7.9 "No More Oracle", p. 10: "in a general-purpose OS (like the ones we care about), the OS usually knows very little about the length of each job"; ch. 8, p. 1: "the OS doesn't generally know how long a job will run for, exactly the knowledge that algorithms like SJF (or STCF) require". Restated: SJF minimises average turnaround when every job arrives at once and its length is known, STCF without the simultaneous arrival; a general-purpose OS usually knows little of a job's length. "which nobody ever does" leaves.
- **What interactive work does per key** (`:95`: "works for a millisecond or two, and goes back to sleep"). The dataset's measured CPU per keystroke — the window rule: the process tree's run time until the next key, less the idle rate (9.5 D13) — on the EPYC 7763 runner under Xvfb with no GPU, so rendering runs on the CPU (each entry's venue bound), SWELL-KW keystrokes replayed (`dataset/archetypes.yaml` `input_run`): median 3.23 ms for LibreOffice Writer (p10–p90 2.53–9.55 ms), 4.07 ms for a Chrome text field (2.93–5.53 ms), 4.65 ms for Thunderbird's compose window (3.21–6.74 ms), 79.7 ms for VS Code, its TypeScript language server re-checking the file (15.3–179 ms). While typing, the three use 0.2–1.4 % of their CPU (`driven cpu-share`), VS Code 14–45 %. Restated: a few milliseconds of CPU per key for an office editor, a browser field and a mail composer, most of the time asleep; an IDE's language server can make it tens of milliseconds and a sizeable share of the CPU — named as the dataset's measurements, this software on this machine (9.5 D10).
- **The 100 ms** (`:111`: "a 100 ms delay before the screen responds is perceived as lag"). 9.11 D1: Miller's guideline, key-to-echo "no more than 0.1 to 0.2 seconds" and control feedback "No more than 0.1 second", his "best calculated guesses" (`miller-fjcc68`, p. 271); Deber et al. measured a latency detection threshold of 96 ms for indirect tapping, among which they place key typing behind "the textbook threshold of 100 ms" (`deber-chi15`, p. 1831). Restated: about 100 ms is the guideline's limit for a keystroke's echo, near a measured detection threshold for indirect input; "is perceived as lag" attributed to them.
- **The cost of interruption** (`:111`: "being interrupted frequently wastes cycles on context switches and destroys cache locality"). OSTEP §7.7, p. 8: programs "build up a great deal of state in CPU caches, TLBs, branch predictors, and other on-chip hardware. Switching to another job causes this state to be flushed and new state relevant to the currently-running job to be brought in, which may exact a noticeable performance cost"; Li, Ding & Shen measured the total cost per switch at 4.2–8.7 µs for working sets of 1–200 KB and 38.6–203.2 µs at 256–512 KB, past 1 000 µs at the largest (S1-21, p. 2; Linux 2.6.17, dual 2.0 GHz Pentium Xeon). Restated: each switch costs the switch itself and the cache state the program built, by an amount that grows with its working set; "destroys" leaves. Item 28 gives the switch's own cost on the dataset's machine.
- **Short turns at high priority** (`:113`: "The standard resolution is: give interactive work high priority but a very short turn on the CPU; give batch work low priority but a long turn"). OSTEP §8.5, pp. 8–9: "most MLFQ variants allow for varying time-slice length across different queues. The high-priority queues are usually given short time slices … (e.g., 10 or fewer milliseconds). The low-priority queues … longer time slices work well (e.g., 100s of ms)"; Solaris's TS table, 20 ms at the top to a few hundred at the bottom (p. 9); CTSS, 2^ℓ quanta at level ℓ (`corbato-sjcc62`, D18). Linux's EEVDF gives a latency-sensitive task a shorter slice without a priority level (`sched-eevdf.rst`, D18). Restated as MLFQ's resolution, as OSTEP describes most of its variants, not "the standard" of every scheduler.

Hands to 9.15: `docs/research-proposal.md:87`, `:95`, `:111`, `:113` restated as above; `:818`'s glossary "discards cache locality" with `:111` (its "1–5 μs" is item 28's). The guidebook vol-01 ch. 7.3 (`:1522–1524`) already states SJF's conditions and stays.

Compiled effect: none.

## D33 — the MLFQ illustration stated with the dataset's measured pair: an editor's runs between blocks against `cc1`'s object compile (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 32: `docs/research-proposal.md:123`'s "`bash` given a 10 ms slice uses 0.5 ms of it, while `cc1plus` burns all 10 ms" and `docs/background-guide.md:115`'s "The editor wakes for a keystroke, computes 0.5 ms of a 10 ms slice … The compiler chews through its full 10 ms slice" carry no source; the dataset measured both kinds of program on its machine, so the illustration is stated with them.

- **The editor** (9.5's `office-writer`, `meas-ci:interactive:2026-09-18`, 14 repeats, `task-9.5-interactive-typing/campaign/results-same-machine.md`, the driven phase): LibreOffice Writer's `soffice.bin` threads, while SWELL-KW keystrokes are typed, run 0.046 ms between blocks at the median, 1.13 ms at p90 and 2.98 ms at p99 (238 329 runs); the first run after a key 0.062 ms at the median; all of a key's CPU 3.23 ms at the median (D32).
- **The compiler** (9.6's `compiler-child`, `meas-ci:build:2026-09-18`, 14 repeats, `dataset/archetypes.yaml` `cc1_step_1`): `cc1` compiling one object of a warm `-j8` linux-6.6 build wakes once in 99.3 % of jobs and runs 367.6 ms of CPU at the median (p10 165.9 ms, p90 778.3 ms) before it next blocks.
- **Restated:** on the dataset's machine an editor's threads run a few hundredths of a millisecond between blocks, a few milliseconds at the 99th percentile, while `cc1` runs hundreds of milliseconds without blocking — the first gives up a 10 ms slice almost at once, the second uses every slice it is given. `bash` (not measured) and `cc1plus` (the C++ compiler; the dataset's build is C) leave the sentence. The measurements are this software on this machine (9.5 D10).

Hands to 9.15: `docs/research-proposal.md:123` and `docs/background-guide.md:115` restated as above, the diagram `:101–108` labelled with the same two programs; found in the sweep (`grep -n cc1plus docs`): `:177`'s §2.3 row "cc1plus ×8, bash" named for the build the dataset depicts (`cc1`, `-j8`).

Compiled effect: none.

## D34 — the world-knowledge examples restated: OBS encodes live and skips frames when it falls behind; `cargo build` compiles a Rust package; `updatedb` leaves the list, its unit declaring its class (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 35, after a stage-3 read (S2-55, S2-56): `docs/research-proposal.md:185`'s "knowing things about software that an operating system has no way to learn on its own: that OBS is a real-time encoder, … that `cargo build` is a compiler and `updatedb` is maintenance", and `:176`'s row "LoL, Discord, OBS | Gaming while streaming | Encoder is now latency-critical too — it cannot drop frames", are restated to the sources. The Steam and antivirus clauses of `:185` are D16's and D15's.

- **OBS** (S2-55): "free and open source software for video recording and live streaming" (obsproject.com); when its encoder falls behind it warns "Encoding overloaded! Consider turning down video settings or using a faster encoding preset." and counts "Skipped frames due to encoding lag" (obs-studio `7d98bebe`, `frontend/data/locale/en-US.ini:58`, `:271`). Restated: OBS records and streams, encoding as it goes, so its encoder has a deadline per frame; "it cannot drop frames" leaves — an encoder that falls behind skips frames, which OBS counts and reports.
- **`cargo build`** (S2-56): "cargo-build — Compile the current package"; "Compile local packages and all of their dependencies"; Cargo is "the Rust package manager". Restated: `cargo build` compiles a Rust package and its dependencies, Cargo driving the compiler.
- **`updatedb`** leaves the list of what "an operating system has no way to learn on its own": its installed unit declares its class — plocate's `Nice=19`, `IOSchedulingClass=idle`; findutils' the same with `IOSchedulingPriority=7` (S3-02; D13). What the declaration leaves unsaid stays the point of `:185` — whether the user is waiting on the work, which D13's count shows is declared for some background tools and not others.
- **"None of that is observable from process behaviour"** (`:187`) restated as D14 and D15 state the pairs: what a process is for, and whether the user is waiting on it, is not stated by its behaviour; its run shape and declared class are, and the experiment tests what recognition adds over them.

Hands to 9.15: `docs/research-proposal.md:176`, `:185`, `:187` restated as above; `docs/references.md` — entries for OBS Studio (the locale file at `7d98bebe`; the home page) and the Cargo Book's `cargo build` page where the prose cites them, under the id-minting rule; the KB page quoted, not linked, at its own request. The sweep (`grep -rn -w -i obs docs`) finds no guidebook line on OBS; `docs/background-guide.md:20` ("what OBS does") and `docs/terminology.md:151` ("the model knows what OBS is") stay.

Compiled effect: none.

## D35 — the media deadlines stated as arithmetic on named rates: 16.7 ms at 60 Hz, 2.67 ms for 128 frames at 48 kHz; the audio workstation's "1–3 ms" restated to its buffer and Ardour's 5 ms target (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 36: `docs/research-proposal.md:414` ("this must complete within 3 ms or a frame drops"), `:640` ("Its deadlines are 1–3 ms rather than gaming's 16 ms, buffer underruns are audible rather than a dropped frame") and `:820` ("A game rendering at 60 fps has a 16 ms deadline every frame … An audio buffer at 128 samples has a deadline nearer 3 ms; missing it is audible") are restated to arithmetic on rates their sources name.

- **The frame** (arithmetic): 1 / 60 Hz = 16.67 ms. Steam Deck's LCD runs "up to 60Hz", adjustable 40–60 Hz; its OLED "up to 90Hz" (S2-39), 11.1 ms. The dataset's game chain ticks every 16 667 µs (`steamos-refresh`, design, 9.4). Restated: "16.7 ms at 60 Hz".
- **The audio buffer** (arithmetic): 128 / 48 000 Hz = 2.67 ms. 48 kHz is PipeWire's and JACK's default rate; their default buffer is 1 024 frames, 21.3 ms (`default.clock.quantum = 1024`, S2-36; `jackd -p` "(default: 1024)", S2-37); a smaller buffer is the user's low-latency choice — "If you need low latency, set -p as low as you can go without seeing xruns" (S2-37). Restated: a 128-frame buffer at 48 kHz, a low-latency setting below the 1 024-frame default, comes due every 2.67 ms.
- **The audio workstation** (`:640`): no source states "1–3 ms". Ardour's manual: the A/D/A conversion alone is "about 1.5–2 ms", and "Latency below 5 ms should be suitable for a professional recording setup", which needs "extremely low buffer sizes" (S2-38). Restated: recording through a 64–128-frame buffer at 48 kHz gives a period of 1.33–2.67 ms (arithmetic), the buffer Ardour's 5 ms target calls for; "gaming's 16 ms" as the 60 Hz frame above.
- **"audible"** kept, cited: a missed audio deadline is an xrun, "leaving its merry trail of clicks, pops and crackles" (S2-57, Ardour's manual).
- **`:414`'s EDF row** restated without mixing the two: a periodic job's deadline is its next period — a frame every 16.7 ms at 60 Hz, a 128-frame audio buffer every 2.67 ms at 48 kHz.

Hands to 9.15: `docs/research-proposal.md:414`, `:640`, `:820` restated as above (`:640`'s Game Mode and whitelist clauses are D5's); `docs/references.md` — PipeWire's and JACK's defaults (S2-36, S2-37), the Ardour manual's two pages (S2-38, S2-57) and the Steam Deck page (S2-39) where the prose cites them, under the id-minting rule.

Compiled effect: none.

## D36 — lottery scheduling as the paper states it: shares proportional in expectation, starvation absent for any client holding tickets, O(n) selection with a list and O(lg n) with a tree; "Stride" leaves the menu row (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 38: `docs/research-proposal.md:415` ("Lottery / Stride … MLFQ cannot guarantee proportions. "Roughly less" is easy; "exactly 15% to background" is not"), `:422` ("its advantage is proportional guarantees and starvation-freedom, not speed. Selection is O(n) in the number of processes (O(log n) with a tree)") and `:828` ("Gives proportional CPU shares and freedom from starvation, at O(n) selection cost") are restated to `waldspurger-osdi94` (S1-09; the copy re-downloaded 2026-10-09, SHA-256 `e704678e…`, equal to the record's).

- **Proportional, in expectation** (§2.2, p. 2): "Scheduling by lottery is probabilistically fair. The expected allocation of resources to clients is proportional to the number of tickets that they hold. … the actual allocated proportions are not guaranteed to match the expected proportions exactly. However, the disparity between them decreases as the number of allocations increases"; throughput proportional to tickets "with accuracy that improves with √n". "proportional guarantees" and "exactly 15% to background" restated: lottery gives the background an expected 15 %, its error shrinking as lotteries accumulate.
- **Starvation** (p. 2): "Since any client with a non-zero number of tickets will eventually win a lottery, the conventional problem of starvation does not exist." Kept, scoped to a client holding tickets.
- **Selection cost** (§4.2, p. 3): "O(n) operations to traverse a client list of length n"; with "a tree of partial ticket sums … only O(lg n) operations". Kept. "slower per decision than popping an MLFQ queue head" kept as the complexity comparison it is: MLFQ runs the jobs of the highest non-empty queue in round-robin (OSTEP ch. 8, Rules 1–2).
- **"Stride"** leaves `:415`'s row: no registry entry and no read carries stride scheduling, and the frozen menu's algorithm is `LOTTERY` (`docs/recognition-vocabulary.md` §2). "It earns its place because ticket allocation is the natural way to express something like `batch_bandwidth_cap`" (`:422`) is a design statement and stays.

Hands to 9.15: `docs/research-proposal.md:415`, `:422`, `:828` restated as above; `docs/references.md` `waldspurger-osdi94`'s role line with the selection cost (§4.2) beside the quantum it quotes.

Compiled effect: none.

## D37 — EDF's optimality stated with its conditions: one processor, Liu and Layland's (A1)–(A5), utilisation at most 1 (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 40: `docs/research-proposal.md:824`'s "Optimal for meeting deadlines on a single core, but requires deadlines to be declared" is restated to `liu-jacm73` (S1-10; the scan re-downloaded 2026-10-09, SHA-256 `de9fb725…`, equal to the record's).

- **The conditions** (printed p. 48): (A1) periodic requests at constant intervals; (A2) "each task must be completed before the next request for it occurs"; (A3) independent tasks; (A4) constant run-time; (A5) no critical non-periodic tasks — on "a single processor" (Abstract).
- **The result** (printed p. 55–56): "if a set of tasks can be scheduled by any algorithm, it can be scheduled by the deadline driven scheduling algorithm"; "THEOREM 7. For a given set of m tasks, the deadline driven scheduling algorithm is feasible if and only if (C1/T1) + (C2/T2) + ··· + (Cm/Tm) ≤ 1." The paper says nothing of behaviour above a utilisation of 1 (`liu-jacm73`'s registry line).
- **"requires deadlines to be declared"**: under (A2) a task's deadline is its next request, so the algorithm needs each task's period; Linux's `SCHED_DEADLINE` takes a declared runtime, deadline and period through `sched_setattr(2)` (D26).
- **Restated:** on one processor, for independent periodic tasks whose deadline is the next request, EDF schedules every task set any algorithm can — exactly those whose utilisation is at most 1 — and it needs each task's period or deadline.

Hands to 9.15: `docs/research-proposal.md:824` restated as above; `:414`'s EDF row read with it (D35).

Compiled effect: none.

## D38 — the "70 % fallbacks" example stated through the guard that judges it (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 41: `docs/research-proposal.md:718`'s "A condition that scores well while 70% of its configurations were fallbacks did not demonstrate anything about recognition; it demonstrated that MLFQ is fine" is an example with no source, and the project has since fixed the line it illustrates.

- **The line, as designed** (`harness/guards/guard-spec.yaml:115–124`; 9.11 D10): `provenance_share`, the time-weighted share of `fallback` and `held` configuration intervals, below 0.5 under every condition but `fixed`; design, reading appendix B.3's "most of its configurations were fallbacks" (`:916`) as a majority of the run's time. A failing guard on a run the RQ0 criterion reads makes the verdict invalid (D30).
- **What a fallback is** (`docs/data-contracts.md` §6): "the default, from boot or after repeated failures" — the boot default configuration, plain MLFQ (`docs/recognition-vocabulary.md` §2), so "it demonstrated that MLFQ is fine" holds of a fallback-heavy run.
- **Restated:** a condition whose run spent half or more of its time under fallback or held configurations fails the `provenance_share` guard — it demonstrated nothing about recognition, only that the boot default is fine. "70%" leaves, or stays marked as an example above the guard's line.

Hands to 9.15: `docs/research-proposal.md:718`, and `:916` (B.3) with it, stated as above.

Compiled effect: none.

## D39 — "a gaming session lasts an hour" restated to the two measured games; "stable for the whole thing" stated as the premise it is (2026-10-09)

Taken under 인지오's delegation (2026-10-09), scope-card item 42, after a stage-3 read (S3-23): `docs/research-proposal.md:303` ("A gaming session may last an hour; polling every 30 seconds would produce 120 identical answers") and `:732` ("A gaming session lasts an hour; the situation is stable for the whole thing") are restated to what the sources measure.

- **The measured sessions:** on one World of Warcraft realm over three years, per-avatar mean session time 2.8 h, median 1.8 h, 5th–95th percentile 0.4–5.5 h, with a "knee" at about one hour — "a high probability that players will stay for at least one hour, but usually no longer than 5 hours" (S3-11, WoWAH, MMSys 2011, Table 4 and p. 126; 10-minute sampling); on one Counter-Strike server over 13 months, "more than 99% of all sessions last less than 2 hours" (S3-23, Chambers et al., IMC 2005). Both are server-side connection time to one game, not a PC's process activity. No measurement of PC gaming sessions in general was found (S3, "Not found", T12; the 2026-10-09 search).
- **Restated `:303`:** a gaming session can run an hour or more — a median 1.8 h on one MMO realm, under 2 h for more than 99 % on one shooter's server — so polling every 30 s would ask the same question about 120 times an hour (arithmetic).
- **Restated `:732`:** "the situation is stable for the whole thing" leaves as a statement of fact. It is the premise of the risk: if the process set stays unchanged through a session, the moments where recognition matters are its transitions — which is why the workloads are built around transitions. How often a desktop's process set changes is not measured by any source found (only foreground-window switching, S3-12, S3-16).

Hands to 9.15: `docs/research-proposal.md:303`, `:732` restated as above; `docs/references.md` entries for WoWAH (S3-11) and Chambers et al. (S3-23) where the prose cites them, under the id-minting rule.

Compiled effect: none.
