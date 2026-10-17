# Reader input R07-gamemode-steam-dkms

## gamemode-docs
### Bibliographic entry
- cite: Microsoft. Game Mode documentation, Microsoft Learn (+ `<expandedresources.h>` APIs). [Exact URLs to pin.]
### Topics
- C-gamemode-1: in Microsoft's Game Mode documentation, what Game Mode does for games and which resources it affects.
- C-gamemode-2: the resources Game Mode grants, the condition for granting them, and when each resource is revoked.
- C-gamemode-3: which functions the expandedresources header documents, whether users can opt out and how that is reported, and any deprecation notice.
- C-gamemode-4: whether Microsoft documents how Game Mode recognizes a game (list, name matching, declaration, other), what it says about default coverage of games, and how the `expandedResources` capability is granted.
- C-gamemode-5: what Microsoft documentation says about how background processes are treated during Game Mode, and whether it mentions deferring updates, driver installs, restarts or notifications.

## steam-downloads
### Bibliographic entry
- cite: Valve. "Downloads automatically pause when launching a game." Steam Support, help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9 (accessed 2026-08-26). Secondary: "Managing Steam Downloads & Updates", …/71AB-698D-57EB-178C (updated 2024-09-24).
### Topics
- C-steam-1: in Steam Support articles, the name and menu location of the setting controlling downloads while a game runs.
- C-steam-2: what Steam does with downloads when a game launches, by default.
- C-steam-3: whether Steam offers a per-game setting for downloads during gameplay, and what it does.
- C-steam-4: see C-steam-1 to C-steam-3 (the setting's existence and user control).
- C-steam-5: the title and last-updated date of the named Steam Support article.
- C-steam-6: under what process name(s) the Steam client performs downloads on Linux.

## dkms-man
### Bibliographic entry
- cite: dkms(8) manual page, dkms 3.0.11. Ubuntu Manpage Repository (noble), manpages.ubuntu.com/manpages/noble/man8/dkms.8.html (accessed 2026-09-10).
### Topics
- C-dkms-man-1: the dkms(8) man page's description of what DKMS is.
- C-dkms-man-2: in dkms(8), what the autoinstall action and the autoinstaller service do, when they run (boot, kernel install, other), and whether user action is required.
- C-dkms-man-3: the command/executable name DKMS runs under and how it is implemented (script or binary).

## dkms-debian
### Bibliographic entry
- cite: Debian package `dkms` 3.0.10-8+deb12u1 (bookworm). packages.debian.org/bookworm/dkms (accessed 2026-09-10).
### Topics
- C-dkms-debian-1: the Debian bookworm `dkms` package description text.
- C-dkms-debian-2: the version of `dkms` packaged in Debian bookworm (and whether the cited page speaks to other distributions).
