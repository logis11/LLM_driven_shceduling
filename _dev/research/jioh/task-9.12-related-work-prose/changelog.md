# Task 9.12 — Related-work and proposal prose: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — `whitelist` reproduces the name-keyed catalogue, `ananicy-rules`; Game Mode is cited for its category only (2026-10-08)

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
