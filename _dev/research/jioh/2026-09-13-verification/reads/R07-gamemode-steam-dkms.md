# Read R07-gamemode-steam-dkms

All copies retrieved 2026-09-13 unless a Wayback capture date is given. `SRC` = `_dev/research/jioh/2026-09-13-verification/sources`.

Quoting convention: web-page quotes are copied from the saved HTML with tags removed and runs of whitespace collapsed to one space (inline `<code>`/`<b>`/`<i>` markup dropped, text unchanged). Man-page quotes are copied from the roff source with roff macros removed and `\-` rendered as `-`.

## Copies used

| source-id | copy | exact URL | printed date on page / page metadata | local copy |
|---|---|---|---|---|
| gamemode-docs | Microsoft Learn, "Game Mode" (archived, Previous Versions) | https://learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal | printed "Last updated on 2018-05-31" (`data-article-date-source="ms.date"`); meta ms.date 2018-05-31; updated_at 2021-10-26; git_commit_id e9bd509db9417c85e860c816106da3ee77a08a71; section TOC metadata `"is_archived":true` | `SRC/gamemode-docs/game-mode-portal.html` / `.txt`; TOC `prevver-toc.json` |
| gamemode-docs | Microsoft Learn, "expandedresources.h header" | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/ | printed "Last updated on 2023-01-24" (calculated); meta ms.date 2019-01-11; updated_at 2025-10-01 | `SRC/gamemode-docs/expandedresources-index.html` / `.txt` |
| gamemode-docs | Microsoft Learn, "Game Mode" technology overview (API index) | https://learn.microsoft.com/en-us/windows/win32/api/_gamemode/ | printed "Last updated on 2023-01-24"; meta ms.date 2019-01-11 | `SRC/gamemode-docs/win32api-_gamemode.html` / `.txt` |
| gamemode-docs | Microsoft Learn, "HasExpandedResources function (expandedresources.h)" | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-hasexpandedresources | printed "Last updated on 2024-02-22" (calculated); meta ms.date 2018-12-05; updated_at 2025-07-01 | `SRC/gamemode-docs/win32api-nf-hasexpandedresources.html` / `.txt` |
| gamemode-docs | Microsoft Learn, "GetExpandedResourceExclusiveCpuCount function (expandedresources.h)" | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-getexpandedresourceexclusivecpucount | printed "Last updated on 2024-02-22"; meta ms.date 2018-12-05 | `SRC/gamemode-docs/win32api-nf-getexpandedresourceexclusivecpucount.html` / `.txt` |
| gamemode-docs | Microsoft Learn, "ReleaseExclusiveCpuSets function (expandedresources.h)" | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-releaseexclusivecpusets | printed "Last updated on 2024-02-22"; meta ms.date 2018-12-05 | `SRC/gamemode-docs/win32api-nf-releaseexclusivecpusets.html` / `.txt` |
| gamemode-docs | (note) the archived-TOC function links `/en-us/previous-versions/windows/desktop/api/expandedresources/nf-…` return 301 to `/en-us/windows/desktop/api/…` and land on the same win32/api pages (byte-identical downloads) | — | — | `SRC/gamemode-docs/prevver-nf-*.html` |
| gamemode-docs | GitHub markdown source of the API pages (MicrosoftDocs/sdk-api, branch `docs`; last commit touching the folder 22c49e67b354…, 2025-09-23) | https://raw.githubusercontent.com/MicrosoftDocs/sdk-api/docs/sdk-api-src/content/expandedresources/<file>.md | ms.date 12/05/2018 in front matter | `SRC/gamemode-docs/sdkapi-*.md` |
| gamemode-docs (supplementary, not Microsoft Learn) | Xbox Support, "Use Game Mode while gaming on your Windows device" — page is a JS app; the article body was taken from the site's own content API that the page calls | page: https://support.xbox.com/en-US/help/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc ; content: https://content.support.xboxlive.com/content?path=/SXC/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc&language=en-US&market=US | no date in page or content JSON | `SRC/gamemode-docs/xboxsupport-content-api-use-game-mode.json`; shell `xboxsupport-use-game-mode-SPA-SHELL.html` |
| gamemode-docs (supplementary, historical) | Microsoft Support KB 4028293 "Using Game Mode on your PC", Wayback capture | https://web.archive.org/web/20200813071329/https://support.microsoft.com/en-us/help/4028293/windows-using-game-mode-on-your-pc (capture 2020-08-13); also capture 20171113235418 | printed "Last Updated: Nov 20, 2017"; "Applies to: Windows 10" | `SRC/gamemode-docs/wayback-msupport-4028293-20200813071329.html` / `.txt` |
| steam-downloads | Steam Support, "Downloads automatically pause when launching a game" | https://help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9 | no date printed on rendered page; embedded `data-faqstore` JSON: `"version":"3"`, `"timestamp":1625946595` (= 2021-07-10T19:49:55Z) | `SRC/steam-downloads/faq-4F9E-6328-E9B8-47F9.html` (raw), `-faqstore.json`, `-rendered-dom.html` / `-rendered.txt` (headless Chrome) |
| steam-downloads | Steam Support, "Managing Steam Downloads & Updates" | https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C | no date printed; embedded JSON `"version":"4"`, `"timestamp":1727216103` (= 2024-09-24T22:15:03Z) | `SRC/steam-downloads/faq-71AB-698D-57EB-178C.*` |
| dkms-man | Ubuntu Manpage Repository, dkms(8), noble, "Provided by: dkms (Version: 3.0.11-1ubuntu13)" | https://manpages.ubuntu.com/manpages/noble/man8/dkms.8.html | HTML prints no date; roff source `.TH DKMS 8 "27 April 2023" dkms-3.0.11` | `SRC/dkms-man/manpages-ubuntu-noble-dkms.8.html` / `.txt` |
| dkms-man | roff source served by the same site | https://manpages.ubuntu.com/manpages.gz/noble/man8/dkms.8.gz | `.TH` line 40: "27 April 2023" dkms-3.0.11 | `SRC/dkms-man/manpages-ubuntu-noble-dkms.8.gz`, `dkms.8.roff` |
| dkms-man | upstream dkms git, tag v3.0.11 (commit 782bd07641b957012f9b8d621bf9b51f82bfc728, 2023-04-27 "Bump release"); `dkms.8.in` is identical to the Ubuntu roff except the `.TH` placeholder line | https://github.com/dell/dkms (tag v3.0.11) | — | `SRC/dkms-man/dkms-upstream/` |
| dkms-man | Ubuntu noble dkms package file list | https://packages.ubuntu.com/noble/all/dkms/filelist | page shows no version | `SRC/dkms-man/packages-ubuntu-noble-dkms-filelist.html` |
| dkms-debian | Debian packages, "Details of package dkms in bookworm" (plain curl hit a JS challenge page; rendered with headless Chrome) | https://packages.debian.org/bookworm/dkms and https://packages.debian.org/en/bookworm/dkms | no page date; "Package: dkms (3.0.10-8+deb12u1)"; breadcrumb "bookworm (oldstable)" | `SRC/dkms-debian/packages-debian-en-bookworm-dkms-rendered-dom.html` / `.txt`; challenge page `packages-debian-bookworm-dkms-CHALLENGE.html` |

---

## gamemode-docs

### C-gamemode-1 — what Game Mode does for games and which resources it affects

(a) Verbatim:
- "Game Mode provides customers with the best possible gaming experience by fully utilizing the capacity of their current hardware. It does this by granting a game exclusive or priority access to hardware resources. These resources being dedicated to the game help it hit performance targets more consistently. The performance increase that comes from Game Mode is directly related to the number and impact of other activities running on the device."
- "However, the game would still get access to other Game Mode resources, such as increased GPU prioritization."
- "While CPU resources may be revoked if the game exits Game Mode, memory resources, once granted, will never be revoked."
- (function reference) "Gets the expected number of exclusive CPU sets that are available to the app when in Game Mode."

(b) Locator: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal, article "Game Mode", body paragraphs after the first Note (printed date 2018-05-31). Last quote: https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-getexpandedresourceexclusivecpucount, description line.

(c) Reading: Game Mode gives the foreground game exclusive or priority access to hardware. The resources the page names are CPU (exclusive CPU sets), GPU (prioritization) and memory. The page is in Microsoft's archived Previous Versions section, written for Windows 10, and carries the notice that the Game Mode APIs are deprecated from Windows 10 version 1809 (see C-gamemode-3). It says the benefit depends on how much other activity is running on the device. It does not quantify the benefit or name any other resource type (disk, network, etc.).

(d) Verdict: FOUND.

### C-gamemode-2 — resources granted, grant condition, when each is revoked

(a) Verbatim:
- "The app must be in the foreground and have focus before exclusive resources are granted."
- "Games should call HasExpandedResources once per frame or game tick to determine whether exclusive resources have been granted."
- "When exclusive resources are revoked, such as when the game loses focus, the game will discover this by polling with HasExpandedResources, and can re-scale as appropriate."
- "Based on the developer's judgment, they may opt-out of CPU exclusivity by calling ReleaseExclusiveCpuSets to get access to all cores, but at a higher latency due to other processes and system activities being scheduled on the same cores as the game. However, the game would still get access to other Game Mode resources, such as increased GPU prioritization."
- "While CPU resources may be revoked if the game exits Game Mode, memory resources, once granted, will never be revoked. Games can use APIs such as AppMemoryUsageLimit to understand what is available."
- (GetExpandedResourceExclusiveCpuCount remarks) "This function returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10."

(b) Locator: game-mode-portal (URL above), Note box after the overview paragraph and the body paragraphs before "Example: Benchmark on startup". The foreground/focus sentence is also in the "Remarks" of all three function pages under https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/. The last quote is from the GetExpandedResourceExclusiveCpuCount page, "Remarks".

(c) Reading:
- **Resources named:** exclusive CPU sets, increased GPU prioritization, memory.
- **Grant condition:** the app is in the foreground and has focus. This is stated for "exclusive resources".
- **Revocation:**
  - CPU: "may be revoked if the game exits Game Mode"; the example given is losing focus.
  - Memory: "once granted, will never be revoked".
  - GPU prioritization: the page gives no revocation rule.
- **App opt-out:** an app can give up CPU exclusivity itself (ReleaseExclusiveCpuSets) and keep the other Game Mode resources.
- **User opt-out:** the user can turn Game Mode off in Windows 10 Settings, and the CPU-count query then returns 0.
- **Caveat:** "exclusive resources" is not defined further, so it is not stated whether the foreground/focus condition also governs GPU priority.

(d) Verdict: PARTIAL. Resources, the grant condition, and the CPU and memory revocation rules are found. No revocation rule is documented for GPU prioritization.

### C-gamemode-3 — functions in expandedresources.h; user opt-out and how reported; deprecation notice

(a) Verbatim:
- (header page) "expandedresources.h contains the following programming interfaces:" … "GetExpandedResourceExclusiveCpuCount Gets the expected number of exclusive CPU sets that are available to the app when in Game Mode." … "HasExpandedResources Gets the current resource state (that is, whether the app is running in Game Mode or shared mode)." … "ReleaseExclusiveCpuSets Opts out of CPU exclusivity, giving the app access to all cores, but at the cost of having to share them with other processes."
- (GetExpandedResourceExclusiveCpuCount, Remarks) "This function returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10."
- (HasExpandedResources, Parameters) "True if the app is running in Game Mode; otherwise, false."
- (ReleaseExclusiveCpuSets, Remarks) "This is a Win32 API that's only supported in UWP desktop and Xbox apps. It also requires the expandedResources restricted capability, …"
- (Game Mode portal, "Important" box at top) "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."
- (Game Mode portal, Note) "These are Win32 APIs that are supported in UWP desktop and Xbox apps, as well as Win32 apps (except for ReleaseExclusiveCpuSets, which isn't supported in Win32 apps)."
- (all three function pages, Requirements table) "Header expandedresources.h", "Library Windowsapp.lib", "DLL Gamemode.dll".

(b) Locator:
- https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/ ("Functions" table)
- the three `nf-expandedresources-*` pages ("Parameters", "Remarks", "Requirements")
- https://learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal ("Important" box, first element of the article)

(c) Reading:
- **Functions:** the header documents exactly three — GetExpandedResourceExclusiveCpuCount, HasExpandedResources and ReleaseExclusiveCpuSets.
- **User opt-out:** exists ("opted out of Game Mode via the Settings in Windows 10"). It is reported indirectly: GetExpandedResourceExclusiveCpuCount returns 0, and 0 also means "no exclusive CPU sets are available", so the two cases are not told apart. HasExpandedResources reports only whether the app is currently in Game Mode.
- **Deprecation notice:** appears only on the archived portal page ("deprecated in Windows 10, version 1809 and later"). The current win32/api header page and function pages (printed 2023-01-24 / 2024-02-22) carry no deprecation notice. The grep for "deprecat" matched only the portal page.
- **Platform support inconsistency:** the portal Note says ReleaseExclusiveCpuSets "isn't supported in Win32 apps", and its function page says it is "only supported in UWP desktop and Xbox apps". The other two function pages say they are supported in Win32 apps as well.

(d) Verdict: FOUND.

### C-gamemode-4 — how Game Mode recognizes a game; default coverage; how `expandedResources` is granted

(a) Verbatim:
- "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer."
- "By using the expandedResources capability, you can explicitly declare that the game will work with Game Mode. As part of launching the game, the process will go into Game Mode with a set of defaults, and you can use the APIs to see what resources are available on the customer's device."
- "ReleaseExclusiveCpuSets requires the expandedResources restricted capability, which you can select by opening Package.appxmanifest in Visual Studio and navigating to the Capabilities tab."
- "This capability is granted on a per-title basis; contact your account manager for more information. You can publish a UWP app with this capability to the Store if it targets desktop, but if it targets Xbox it will be rejected in certification."
- (supplementary, Microsoft Support KB 4028293 as captured 2020-08-13, "Last Updated: Nov 20, 2017", "Applies to: Windows 10") "To use Game Mode, make sure it's turned on for each game you play." … "In the General tab, select the Game Mode check box." … "Note: Some games automatically turn on Game Mode. If so, the check box will already be selected."

(b) Locator: game-mode-portal (URL above), the paragraphs after the second Note and the Note that follows the member list. The same capability text is in the "Remarks" of https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-releaseexclusivecpusets. The supplementary quote is from https://web.archive.org/web/20200813071329/https://support.microsoft.com/en-us/help/4028293/windows-using-game-mode-on-your-pc, article body.

(c) Reading:
- **Default coverage:** "works by default for most Windows games", with no customer or developer action.
- **Explicit declaration:** a developer can declare Game Mode support through the `expandedResources` restricted capability in the app package manifest. A declared title enters Game Mode "as part of launching the game".
- **How the capability is granted:** Microsoft grants it "on a per-title basis" through the developer's account manager. Store publication with the capability is allowed for desktop targets and rejected for Xbox targets.
- **Recognition of undeclared games:** none of the Learn pages says how Windows recognizes a game that has not declared the capability. There is no allow-list, no executable-name matching and no heuristic. I grepped all saved Game Mode pages for recogni/detect/identif/list/whitelist/match/executable/process name/declar/automatic, and the only hits were the declaration sentence and unrelated code-sample text.
- **Older support article (Windows 10, 2017):** it describes a per-game Game bar check box and says only that "Some games automatically turn on Game Mode", without saying how.
- **Current Xbox Support article:** says only "Game Mode is turned on by default" (see C-gamemode-5).

(d) Verdict: PARTIAL. Default coverage and capability granting are found. The recognition mechanism is NOT FOUND in any Microsoft copy obtained.

### C-gamemode-5 — treatment of background processes; deferral of updates, driver installs, restarts, notifications

(a) Verbatim:
- (Learn portal) "The performance increase that comes from Game Mode is directly related to the number and impact of other activities running on the device."
- (Learn portal) "… to get access to all cores, but at a higher latency due to other processes and system activities being scheduled on the same cores as the game."
- (ReleaseExclusiveCpuSets description) "Opts out of CPU exclusivity, giving the app access to all cores, but at the cost of having to share them with other processes."
- (supplementary, Xbox Support article, content JSON `ContentList[0]` and `ContentList[1].ListItems`) "When you use Game Mode, Windows prioritizes your gaming experience by turning things off in the background. When you’re running a game, Game Mode:" / "Prevents Windows Update from performing driver installations and sending restart notifications" / "Helps achieve a more stable frame rate depending on the specific game and system"
- (same article, final note) "Note Game Mode is turned on by default." (markup: `<b>Note</b> Game Mode is turned on by default.`)

(b) Locator:
- Learn: game-mode-portal (URL above), overview paragraph and the paragraph after the "revoked" paragraph; ReleaseExclusiveCpuSets page description.
- Xbox Support: https://support.xbox.com/en-US/help/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc, body retrieved from https://content.support.xboxlive.com/content?path=/SXC/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc&language=en-US&market=US (title "Use Game Mode while gaming on your Windows device"; no date).

(c) Reading:
- **Learn pages:** they treat other processes only through CPU exclusivity. The game gets exclusive cores, so other processes and system activity are not scheduled on those cores unless the game releases them. The Learn pages do not mention Windows Update, driver installs, restarts or notifications. I grepped for update/driver/restart/notification/background, and the only hits were code-comment words.
- **Xbox Support article (a Microsoft page, not Microsoft Learn, undated, Windows 10/11):** it says Game Mode turns "things off in the background". It names two effects: Windows Update does not perform driver installations, and Windows Update does not send restart notifications.
- **What the Xbox article does not say:** that ordinary Windows updates in general are deferred, that restarts themselves are deferred, or that other kinds of notifications are suppressed. It also does not say how background processes are treated beyond "turning things off".

(d) Verdict: PARTIAL. The Learn pages cover background processes only via CPU exclusivity. The driver-install and restart-notification items appear only in the Xbox Support article. General update deferral and non-restart notifications are not stated anywhere.

---

## steam-downloads

### C-steam-1 — name and menu location of the setting controlling downloads while a game runs

(a) Verbatim: "You can turn this feature off by navigating to your download settings: [i]Steam > Settings > Downloads[/i]. From here, check the [i]Allow Downloads During Gameplay[/i] box." The rendered page shows the same sentence as "You can turn this feature off by navigating to your download settings: Steam > Settings > Downloads. From here, check the Allow Downloads During Gameplay box."

(b) Locator: https://help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9, article "Downloads automatically pause when launching a game", third paragraph (FAQ JSON `content`, version 3).

(c) Reading: the client-wide setting is a check box named "Allow Downloads During Gameplay" under Steam > Settings > Downloads. Checking it turns off the automatic pause. The article names no Steam client version or platform.

(d) Verdict: FOUND.

### C-steam-2 — what Steam does with downloads when a game launches, by default

(a) Verbatim: "Why do downloads in Steam stop when I begin playing a game?" / "Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself." / "If the download is affecting the network performance of the game, you can also consider setting a bandwidth limit from the download settings."

(b) Locator: same URL, paragraphs 1–2 and 4.

(c) Reading: when a game is launched, Steam automatically pauses downloads, and the stated reason is to prioritize the game's network activity. The article presents this as automatic behaviour that the user can switch off with the check box above, so it is the default. The literal words "by default" do not appear. The article says "pauses", not "cancels". It does not say whether downloads resume when the game exits. It also does not mention CPU or disk; the only reason given is network.

(d) Verdict: FOUND. The behaviour is found; "default" follows from "automatically" plus the opt-out check box rather than from explicit wording.

### C-steam-3 — per-game setting for downloads during gameplay and what it does

(a) Verbatim: "[h4]Customizing settings per game[/h4]Games are automatically put into your download queue when a game releases an update. Here's how you can customize updates per game:" … "Select the [b]Updates[/b] tab and make your choice from [b]Automatic updates[/b]" … "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing." Rendered text of the last sentence: "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing."

(b) Locator: https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C, article "Managing Steam Downloads & Updates", section "Customizing settings per game" (`[section id=customize]`), last sentence.

(c) Reading: the article says a per-game setting exists that allows or prevents downloading "other updates" while that game is being played. It does not name the setting or give its values, and it does not say exactly where it sits. It appears in the same section as the Manage > Properties > Updates tab, but the sentence does not explicitly place it there. The 4F9E article does not mention a per-game setting.

(d) Verdict: PARTIAL. Existence and effect are found; name and location are not stated.

### C-steam-4 — the setting's existence and user control (C-steam-1 to C-steam-3)

(a) Verbatim: as in C-steam-1 ("check the [i]Allow Downloads During Gameplay[/i] box"), C-steam-2 ("Steam automatically pauses your downloads when a game is launched …") and C-steam-3 ("There's also a per-game setting to allow/prevent the downloading of other updates while you're playing.").

(b) Locator: as above.

(c) Reading: the setting exists and is under user control at two levels. The client-wide one is a named check box. The per-game one is unnamed in the article. A bandwidth limit is offered as an alternative.

(d) Verdict: FOUND. The per-game setting is unnamed, as noted in C-steam-3.

### C-steam-5 — title and last-updated date of the named article

(a) Verbatim: `<title>Steam Support :: Downloads automatically pause when launching a game</title>`; rendered heading "Downloads automatically pause when launching a game". Embedded page data: `"version":"3"`, `"timestamp":1625946595`, `"url_code":"4F9E-6328-E9B8-47F9"`. For the secondary article: heading "Managing Steam Downloads & Updates", `"version":"4"`, `"timestamp":1727216103`.

(b) Locator: https://help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9 (HTML `<title>`, rendered `role="heading"` element, `data-faqstore` attribute); https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C (same elements).

(c) Reading:
- **Title:** "Downloads automatically pause when launching a game".
- **Printed date:** neither the raw HTML nor the JavaScript-rendered page (headless Chrome DOM) shows any "updated" or last-updated date. A grep of the rendered text for years and month names found only the footer copyright year.
- **Machine timestamps:** the only date-like values are in the embedded FAQ JSON. For 4F9E, 1625946595 = 2021-07-10T19:49:55Z (version 3). For 71AB, 1727216103 = 2024-09-24T22:15:03Z (version 4), which matches the 2024-09-24 given in the input entry for the secondary article.
- **Caveat:** the meaning of `timestamp` is not documented on the page. It is plausibly the revision time, but that is an inference.

(d) Verdict: PARTIAL. The title is found. No last-updated date is printed; only an undocumented machine timestamp exists.

### C-steam-6 — process name(s) under which the Steam client performs downloads on Linux

(a) Verbatim: none.

(b) Locator: both articles, full text (raw FAQ JSON and rendered text).

(c) Reading: neither article mentions Linux, process names, executables or client internals. A grep for linux|process|steamwebhelper|steam.sh|executable|binary|SteamOS|Deck returned no matches. Both articles describe the client UI only, with no platform distinction.

(d) Verdict: NOT FOUND (in the cited Steam Support articles).

---

## dkms-man

### C-dkms-man-1 — dkms(8) description of what DKMS is

(a) Verbatim: NAME: "dkms - Dynamic Kernel Module Support". DESCRIPTION: "dkms is a framework which allows kernel modules to be dynamically built for each kernel on your system in a simplified and organized fashion."

(b) Locator: https://manpages.ubuntu.com/manpages/noble/man8/dkms.8.html, sections NAME and DESCRIPTION. roff source `dkms.8.gz` lines 41–42 (NAME) and 52–55 (DESCRIPTION), `.TH DKMS 8 "27 April 2023" dkms-3.0.11`. Identical text in upstream `dkms.8.in` at tag v3.0.11 (commit 782bd076…).

(c) Reading: DKMS is a framework for building kernel modules dynamically for each kernel installed on the system. The page is Ubuntu 24.04 (noble), package dkms 3.0.11-1ubuntu13, and its manpage text is unchanged from upstream 3.0.11.

(d) Verdict: FOUND.

### C-dkms-man-2 — autoinstall action and autoinstaller service: what they do, when they run, whether user action is required

(a) Verbatim (man page):
- ACTIONS / autoinstall: "Attempt to install the latest revision of all modules that have been installed for other kernel revisions. dkms_autoinstaller is a stub that uses this action to perform its work."
- DKMS.CONF / AUTOINSTALL=: "If this directive is set to yes then the service /etc/rc.d/init.d/dkms_autoinstaller will automatically try to install this module on any kernel you boot into. See the section on dkms_autoinstaller for more information."
- BUILD_EXCLUSIVE_KERNEL=: "Note that dkms autoinstall will ignore this type of error condition and simply skip the respective modules."
- /etc/dkms/framework.conf / $autoinstall_all_kernels: "Used by the common postinst for DKMS modules. It controls if the build should be done for all installed kernels or only for the current and latest installed kernel. It has no command line equivalent."
- dkms_autoinstaller section: "This boot-time service automatically installs any module which has AUTOINSTALL="yes" set in its dkms.conf file. The service works quite simply and if multiple versions of a module are in your system's DKMS tree, it will not do anything and instead explain that manual intervention is required."

Verbatim (upstream source, tag v3.0.11, for behaviour):
- `kernel_postinst.d_dkms:3` "# We're passed the version of the kernel being installed"; `:37-38` "if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then" / "    exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern""
- `kernel_install.d_dkms:3-4` "if [ "$1" = "add" ]; then" / "	/etc/kernel/postinst.d/dkms "$2""
- `dkms_autoinstaller:6-7` "# description: Compiles and install kernel modules automatically for new \" / "#              kernels at boot."; `:69-76` "if [ -f /etc/dkms/no-autoinstall ]; then" … "log_action_msg "$prog: autoinstall for kernel $kernel was skipped since the kernel headers for this kernel do not seem to be installed"" … "dkms autoinstall --kernelver $kernel"
- `dkms.service:1-12` "[Unit]" / "Description=Builds and install new kernel modules through DKMS" / "Documentation=man:dkms(8)" / "Before=network-pre.target graphical.target" / "[Service]" / "Type=oneshot" / "RemainAfterExit=true" / "ExecStart=/usr/sbin/dkms autoinstall --verbose --kernelver %v" / "[Install]" / "WantedBy=multi-user.target"
- `Makefile:51-52` "install -D -m 0755 kernel_install.d_dkms $(KCONF)/install.d/dkms" / "install -D -m 0755 kernel_postinst.d_dkms $(KCONF)/postinst.d/dkms"; `:56,59` "install-redhat: install" … "install -D -m 0644 dkms.service $(SYSTEMD)/dkms.service"; `:61,63` "install-debian: install" … "install -D -m 0755 kernel_postinst.d_dkms $(KCONF)/header_postinst.d/dkms"
- `dkms.in:2219-2223` (inside `autoinstall()` starting at line 2207) "    # Walk through our list of installed and built modules, and create" / "    # a list of modules and their latest version." … `:2226` "        elif [[ ("$(VER "$v")" > "$(VER "${latest["$m"]}")") ]]; then"

(b) Locator:
- Man page: https://manpages.ubuntu.com/manpages/noble/man8/dkms.8.html, sections ACTIONS (autoinstall), DKMS.CONF (AUTOINSTALL=, BUILD_EXCLUSIVE_KERNEL=), /etc/dkms/framework.conf, dkms_autoinstaller. roff lines 234–238, 637–644, 662–663, 786–788, 806–812.
- Source: https://github.com/dell/dkms at tag v3.0.11 (782bd07641b957012f9b8d621bf9b51f82bfc728), files and lines as given.
- Ubuntu noble file list: https://packages.ubuntu.com/noble/all/dkms/filelist.

(c) Reading:
- **Man page, what each does:**
  - `autoinstall` action: installs the latest revision of every module that was installed for other kernel revisions.
  - dkms_autoinstaller: a "stub" around that action.
  - It acts only on modules whose dkms.conf sets AUTOINSTALL="yes".
- **Man page, when it runs:**
  - It calls dkms_autoinstaller a "boot-time service" that tries to install the module "on any kernel you boot into".
  - Kernel-install time is mentioned only indirectly: `$autoinstall_all_kernels` is "Used by the common postinst for DKMS modules", which controls whether builds cover all installed kernels or only the current and latest.
- **Man page, user action:** none is required in the normal case ("automatically"). The stated exception is multiple versions of a module in the DKMS tree: then the service "will not do anything and instead explain that manual intervention is required". Modules excluded by BUILD_EXCLUSIVE_* are skipped silently.
- **Man page caveat:** it gives the service path as `/etc/rc.d/init.d/dkms_autoinstaller`, a Red Hat-style init path.
- **Upstream 3.0.11 source, when it runs:**
  - Kernel install: the kernel `postinst.d` hook (and `install.d` "add", which calls it) runs `dkms_autoinstaller start <new kernel>`. That in turn runs `dkms autoinstall --kernelver <kernel>`, unless `/etc/dkms/no-autoinstall` exists or the kernel headers are missing (then it logs a skip).
  - Boot: the systemd unit `dkms.service` runs `dkms autoinstall --verbose --kernelver %v` as a oneshot before `network-pre.target graphical.target`. The Makefile installs it only in the `install-redhat` target, not `install-debian`.
  - Header install: `install-debian` additionally installs the hook as `/etc/kernel/header_postinst.d/dkms`.
- **Ubuntu noble package file list:** contains `/etc/kernel/postinst.d/dkms`, `/etc/kernel/install.d/dkms`, `/etc/kernel/header_postinst.d/dkms` and `/usr/lib/dkms/dkms_autoinstaller`. It contains no `dkms.service` and nothing under `/etc/rc.d/init.d/`. So on Ubuntu noble the documented "boot-time service" path does not exist as written; the automatic trigger shipped is the kernel/header install hooks. The file-list page does not print the package version.
- **Discrepancy:** the `autoinstall()` code at v3.0.11 builds a per-module "latest version" and installs that. The man page's "if multiple versions … it will not do anything" therefore appears not to describe the 3.0.11 code path; the man page text looks older than the code. This is an observation from reading the code, not something either source states.

(d) Verdict: FOUND for the man page's own statements (what, boot-time, user action). Kernel-install triggering is only indirect in the man page and explicit in the upstream source at v3.0.11.

### C-dkms-man-3 — command/executable name DKMS runs under; script or binary

(a) Verbatim:
- (man page SYNOPSIS) "dkms [action] [options] [module/module-version] [/path/to/source-tree] [/path/to/tarball.tar] [/path/to/driver.rpm]"
- (man page DKMS.CONF) "Note that the dkms.conf is really only a shell-script of variable definitions which are then sourced in by the dkms executable (of the format, DIRECTIVE="directive text goes here")."
- (man page /etc/dkms/framework.conf) "It is sourced in every time the dkms command is run."
- (upstream `dkms.in:1-3` at v3.0.11) "#!/bin/bash" / "#" / "#  Dynamic Kernel Module Support (DKMS) <dkms-devel@dell.com>"
- (upstream `Makefile:36-37`) "dkms: dkms.in" / "	sed -e 's/#RELEASE_STRING#/$(RELEASE_STRING)/' $^ > $@"; (`Makefile:45`) "install -D -m 0755 dkms $(SBIN)/dkms" where `Makefile:11` "SBIN = $(DESTDIR)/usr/sbin"

(b) Locator: man page (URL above), SYNOPSIS (roff 43–51), DKMS.CONF (roff 436–446), /etc/dkms/framework.conf section. Source: https://github.com/dell/dkms tag v3.0.11, `dkms.in` lines 1–3, `Makefile` lines 11, 36–37, 45. Ubuntu noble file list shows `/usr/sbin/dkms`.

(c) Reading:
- **Command name:** `dkms`. The man page calls it "the dkms executable" and "the dkms command".
- **Man page on implementation:** it does not say whether `dkms` is a script or a compiled binary. It only says dkms.conf is a shell-script fragment that `dkms` sources, which requires a shell implementation but is not stated as such.
- **Upstream 3.0.11 source:** `dkms` is a Bash script. `dkms.in` starts with `#!/bin/bash`; the Makefile generates `dkms` from it with `sed` and installs it to `/usr/sbin/dkms`. No compilation step exists.
- **Invocation from hooks and unit:** the autoinstaller and the systemd unit call `/usr/sbin/dkms`.

(d) Verdict: PARTIAL. The man page gives the name; script vs binary is NOT stated in the man page and is FOUND only in the upstream source at v3.0.11.

---

## dkms-debian

### C-dkms-debian-1 — Debian bookworm `dkms` package description text

(a) Verbatim (description block `<div id="pdesc">`): heading "Dynamic Kernel Module System (DKMS)"; body "DKMS is a framework designed to allow individual kernel modules to be upgraded without changing the whole kernel. It is also very easy to rebuild modules as you upgrade kernels."

(b) Locator: https://packages.debian.org/bookworm/dkms (English copy https://packages.debian.org/en/bookworm/dkms), description section below "Similar packages". The page also has `<meta name="Description" content="Dynamic Kernel Module System (DKMS)">`.

(c) Reading:
- **Short description:** "Dynamic Kernel Module System (DKMS)". Note "System" here versus "Support" in the dkms(8) NAME line.
- **Long description:** DKMS lets individual kernel modules be upgraded without changing the whole kernel, and makes rebuilding modules across kernel upgrades easy.
- **Other facts on the same page:**
  - Debtags "Implemented in: C, implemented-in::shell".
  - Homepage link https://github.com/dell/dkms.
  - Dependencies: lsb-release, dpkg-dev, gcc | c-compiler, kmod | kldutils, make | build-essential, patch.
- **Access caveat:** a plain HTTP fetch returns an "I Challenge Thee" JavaScript challenge page, so the copy was rendered with headless Chrome.

(d) Verdict: FOUND.

### C-dkms-debian-2 — version of `dkms` in Debian bookworm; whether the page speaks to other distributions

(a) Verbatim: "Package: dkms (3.0.10-8+deb12u1)"; breadcrumb "/ bookworm (oldstable) / kernel / dkms"; suite selector "[ bullseye ] [ bookworm ] [ trixie ] [ forky ] [ sid ]"; source downloads "[dkms_3.0.10-8+deb12u1.dsc]", "[dkms_3.0.10.orig.tar.gz]", "[dkms_3.0.10-8+deb12u1.debian.tar.xz]"; `<meta name="Keywords" content="Debian,  bookworm, us, main, kernel, 3.0.10-8+deb12u1">`; download table "all 47.6 kB 186.0 kB".

(b) Locator: https://packages.debian.org/en/bookworm/dkms, page `<h1>` and the "Download Source Package dkms" list (retrieved 2026-09-13).

(c) Reading:
- **Version:** Debian bookworm, now labelled "oldstable", packages dkms 3.0.10-8+deb12u1, architecture "all". The upstream version is 3.0.10, one release before the 3.0.11 documented by the Ubuntu noble man page.
- **Other distributions:** the page covers only Debian. The suite selector links to other Debian suites (bullseye, trixie, forky, sid) without giving their versions on this page. No other distribution (Ubuntu, Fedora, etc.) is mentioned; a grep for ubuntu/fedora/red hat found nothing.
- **Time-dependence:** the page reflects the archive state on the retrieval date (bookworm point-release updates can change the version).

(d) Verdict: FOUND.

---

## Verdict counts

- FOUND: 9 — C-gamemode-1, C-gamemode-3, C-steam-1, C-steam-2, C-steam-4, C-dkms-man-1, C-dkms-man-2, C-dkms-debian-1, C-dkms-debian-2
- PARTIAL: 6 — C-gamemode-2, C-gamemode-4, C-gamemode-5, C-steam-3, C-steam-5, C-dkms-man-3
- NOT FOUND: 1 — C-steam-6
- PREMISE NOT IN SOURCE: 0
- COPY UNREACHABLE: 0

## Unreachable / degraded copies

- support.microsoft.com "Options to optimize gaming performance in Windows 11" (https://support.microsoft.com/en-us/windows/options-to-optimize-gaming-performance-in-windows-11-a255f612-2949-4373-a566-ff6f3f474613): HTTP 200 after redirect to https://support.microsoft.com/en-us/ (home page). No article content; not used.
- support.xbox.com Game Mode article, direct HTML: returns only a JavaScript app shell (2,847 bytes), and WebFetch saw only "XBOX Support". Article content was obtained instead from the site's content API (URL above).
- Microsoft Support KB 4028293 current URL (https://support.microsoft.com/help/4028293/windows-using-game-mode-on-your-pc): verified with curl on 2026-09-13: 301 to https://support.microsoft.com/en-us/windows/5c94107e-a537-206e-e9e9-20600523bc43, then final URL https://support.xbox.com/en-US/help/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc. So the KB now resolves to the Xbox Support article above, and the 2017/2020 KB wording was taken from Wayback only.
- packages.debian.org/bookworm/dkms via curl: served "I Challenge Thee" JS challenge (https://packages.debian.org/.internal/challenge.html?original=%2fbookworm%2fdkms). Full page obtained with headless Chrome.
