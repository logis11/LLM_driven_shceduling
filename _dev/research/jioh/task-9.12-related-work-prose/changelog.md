# Task 9.12 — Related-work and proposal prose: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — `whitelist` reproduces the name-keyed catalogue, `ananicy-rules`; Game Mode is cited for its category only (2026-10-08)
> Amended by D3 (CachyOS installs ananicy-cpp with the catalogue and enables it by default: the design point ships in a distribution; `:536` and the `whitelist` lines restated to it).

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
