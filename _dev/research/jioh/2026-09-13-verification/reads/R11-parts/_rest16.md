# R11 part — C-plain-1 (Chromium process model) and C-plain-6 (Proton/Wine process names)

Retrieval date for every copy: 2026-09-13. `S` = `_dev/research/jioh/2026-09-13-verification/sources`.

---

## C-plain-1 — Chromium's documented process model: which processes a browser session runs, how renderer processes map to tabs or sites, process name on Linux

### Sub-item 1a — which processes a browser session runs

(a) Verbatim.

Row 8, `website_multi-process-architecture_index.md` (chromium/website @ a88b32e4):

> We refer to the main process that runs the UI and manages renderer and other
> processes as the "browser process" or "browser." Likewise, the processes
> that handle web content are called "renderer processes" or "renderers."

> ## Additional Process Types
>
> Chromium has split out a number of other components into separate processes as
> well, sometimes in platform-specific ways. For example, it now has a separate
> GPU process, network service, and storage service. Sandboxed utility processes
> can also be used for small or risky tasks, as one way to satisfy the [Rule of
> Two](https://chromium.googlesource.com/chromium/src/+/master/docs/security/rule-of-2.md)
> for security.

Row 3, `content/public/common/content_switches.cc` (@ 2060fcb7), lines 452–453, 568–570, 615–616, 778–779, 783–787, 827–828:

> // Makes this process a GPU sub-process.
> const char kGpuProcess[]                    = "gpu-process";

> // The value of this switch determines whether the process is started as a
> // renderer or plugin host.  If it's empty, it's the browser.
> const char kProcessType[]                   = "type";

> // Causes the process to run as renderer instead of as browser.
> const char kRendererProcess[]               = "renderer";

> // Causes the process to run as a utility subprocess.
> const char kUtilityProcess[]                = "utility";

> // This switch indicates the type of a utility process. It does not affect the
> // services offered by the process, but is added to the command line to make
> // it easier to identify the purpose of the utility process.
> const char kUtilitySubType[] = "utility-sub-type";

> // Causes the process to run as a zygote.
> const char kZygoteProcess[] = "zygote";

Row 2, `docs/linux/zygote.md` lines 31–39:

> Instead, we exec the prototypical renderer at the beginning of the browser
> execution. When we need more renderers, we signal this prototypical process (the
> zygote) to fork itself. The zygote is always the correct version and, by
> exec'ing one, we make sure the renderers have a different address space
> randomisation than the browser.
>
> The zygote process is triggered by the `--type=zygote` command line flag, which
> causes `ZygoteMain` (in `chrome/browser/zygote_main_linux.cc`) to be run.

Row 1, `docs/process_model_and_site_isolation.md` lines 476–479:

> * **Spare Process**: Chromium often creates a spare RenderProcessHost with a
>     live but unlocked renderer process, which is used the next time a renderer
>     process is needed. This avoids the need to wait for a new process to
>     start.

Row 7, `sandbox/policy/mojom/sandbox.mojom` (enum `Sandbox`, excerpt):

> // The audio service process. May be disabled by policy.
> kAudio,

> // The network service. May be disabled by policy.
> kNetwork,

> // Hosts the GPU service and can talk to GPU drivers and other OS APIs which
> // may not be expecting untrusted input.
> kGpu,

> // Hosts untrustworthy web content. Blocks as much OS access as possible.

(b) Locators: as given above per file and commit.

(c) Reading. The design doc names one browser process (UI, manages the others), renderer processes (web content), and "additional process types": a GPU process, a network service, a storage service, and sandboxed utility processes. The command-line switch file shows the kinds are distinguished by `--type=` (`renderer`, `gpu-process`, `utility`, `zygote`; empty = browser), with `--utility-sub-type=` added to label which service a utility process hosts. On Linux a zygote process (`--type=zygote`) is started at browser start and forks renderers. A spare, not-yet-used renderer is often kept. The sandbox enum lists more service-process kinds (audio, network, GPU, print compositor, CDM, etc.), some platform-gated. Caveats: the docs do not give a fixed count of processes per session; the exact set depends on platform, flags and policy ("sometimes in platform-specific ways", "May be disabled by policy"). The zygote.md path `chrome/browser/zygote_main_linux.cc` is stale — at this commit the zygote code lives under `content/zygote/` (row 6); the doc's description is still what it states.

(d) Verdict: FOUND.

### Sub-item 1b — how renderer processes map to tabs or sites

(a) Verbatim, row 1 (`docs/process_model_and_site_isolation.md` @ 2060fcb7).

Lines 141–150:

> ### Full Site Isolation (site-per-process)
>
> _Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._
>
> In (one-)site-per-process mode, each process is locked to documents from a
> single site. Sites are defined as scheme plus eTLD+1, since different origins
> within a given site may have synchronous access to each other if they each
> modify their document.domain. This mode provides all sites protection against
> compromised renderers and Spectre-like attacks, without breaking backwards
> compatibility.

Lines 115–118:

> Note that the user may visit multiple instances of a given principal in the
> browser, sometimes in unrelated tabs (i.e., separate browsing context
> groups). These separate instances do not need synchronous access to each
> other and can safely run in separate processes.

Lines 322–331:

> * **Soft Process Limit**: On desktop platforms, Chromium sets a "soft" process
>     limit based on the memory available on a given client. While this can be
>     exceeded (e.g., if Site Isolation is enabled and the user has more open
>     sites than the limit), Chromium makes an attempt to start randomly reusing
>     same-site processes when over this limit. For example, if the limit is 100
>     processes and the user has 50 open tabs to `example.com` and 50 open tabs to
>     `example.org`, then a new `example.com` tab will share a process with a
>     random existing `example.com` tab, while a `chromium.org` tab will create a
>     101st process. Note that Chromium on Android does not set this soft process
>     limit, and instead relies on the OS to discard processes.

Lines 332–342:

> * **Aggressive Reuse**: For some cases (including on Android), Chromium will
>     aggressively look for existing same-site processes to reuse even before
>     reaching the process limit. Out-of-process iframes (OOPIFs) and [fenced
>     frames](https://developer.chrome.com/en/docs/privacy-sandbox/fenced-frame/)
>     use this approach, such that an `example.com` iframe in a cross-site page
>     will be placed in an existing `example.com` process (in any browsing context
>     group), even if the process limit has not been reached.

Lines 269–273 (under "Historical Modes"):

> * **Process-per-tab**: This model used a separate process for each browsing
>     context group (i.e., possibly multiple related tabs), but did not attempt
>     to switch processes on cross-site navigations. In practice, though, this
>     model still needed to swap processes for privileged pages like `chrome://`
>     URLs.

Row 8 (`website_multi-process-architecture_index.md`), lines 100–111:

> ## Sharing the renderer process
>
> In general, each new window or tab opens in a new process. The browser will
> spawn a new process and instruct it to create a single `RenderFrame`, which
> may create more iframes in the page (possibly in different processes).
>
> Sometimes it is necessary or desirable to share the renderer process between
> tabs or windows. For example, a web application can use `window.open` to
> create another window, and the new document must share the same process if
> it belongs to the same origin. Chromium also has strategies to assign new
> tabs to existing processes if the total number of processes is too large.

(b) Locators: as above.

(c) Reading. On desktop Linux the current documented mode is full Site Isolation: a renderer process is locked to one site (scheme + eTLD+1). The mapping is therefore to sites/browsing-context-groups, not strictly one-per-tab: one tab can use several renderer processes (cross-site iframes go out of process), and several tabs can share one (same-site pages over the soft process limit, `window.open` relatives, process-per-site cases like the New Tab Page and extensions, and aggressive reuse for same-site iframes). "Process-per-tab" is listed only as a historical mode. The older design doc says "In general, each new window or tab opens in a new process", qualified by the sharing rules. Caveats: the soft limit depends on client memory and no number is fixed except the illustrative "100"; Android and WebView differ.

(d) Verdict: FOUND. (If a topic premise says "one renderer per tab", that is PARTIAL against the source: the source maps renderers to sites with sharing and splitting across tabs; per-tab is historical.)

### Sub-item 1c — process name on Linux

(a) Verbatim.

Row 4, `base/process/set_process_title.cc` (@ 2060fcb7), lines 64–105 (excerpt, contiguous pieces):

> // In Linux we sometimes exec ourselves from /proc/self/exe, but this makes us
> // show up as "exe" in process listings. Read the symlink /proc/self/exe and
> // use the path it points at for our process title. Note that this is only for
> // display purposes and has no TOCTTOU security implications.

>     base::FilePath::StringType base_name =
>         base::FilePath(title).BaseName().value();
>     // PR_SET_NAME is available in Linux 2.6.9 and newer.
>     // When available at run time, this sets the short process name that shows
>     // when the full command line is not being displayed in most process
>     // listings.
>     prctl(PR_SET_NAME, base_name.c_str());

>   const base::CommandLine* command_line =
>       base::CommandLine::ForCurrentProcess();
>   for (size_t i = 1; i < command_line->argv().size(); ++i) {
>     if (!title.empty()) {
>       title += " ";
>     }
>     title += command_line->argv()[i];
>   }
>   // Disable prepending argv[0] with '-' if we prepended it ourselves above.
>   setproctitle(have_argv0 ? "-%s" : "%s", title.c_str());

Row 6, `content/app/content_main.cc` line 252:

> base::SetProcessTitleFromCommandLine(argv);

Row 6, `content/zygote/zygote_linux.cc` lines 601–609:

>     // Reset the process-wide command line to our new command line.
>     base::CommandLine::Reset();
>     base::CommandLine::Init(0, nullptr);
>     base::CommandLine::ForCurrentProcess()->InitFromArgv(args);
>
>     // Update the process title. The argv was already cached by the call to
>     // SetProcessTitleFromCommandLine in ChromeMain, so we can pass NULL here
>     // (we don't have the original argv at this point).
>     base::SetProcessTitleFromCommandLine(nullptr);

Row 5, `base/threading/platform_thread_linux.cc` lines 210–226:

> void PlatformThreadBase::SetName(const std::string& name) {
>   SetNameCommon(name);
>
>   // On linux we can get the thread names to show up in the debugger by setting
>   // the process name for the LWP.  We don't want to do this for the main
>   // thread because that would rename the process, causing tools like killall
>   // to stop working.
>   if (PlatformThread::CurrentId().raw() == getpid()) {
>     return;
>   }
>
>   // http://0pointer.de/blog/projects/name-your-threads.html
>   // Set the name for the LWP (which gets truncated to 15 characters).

>   int err = prctl(PR_SET_NAME, name.c_str());

Row 9, Debian `chromium` 150.0.7871.181-1~deb13u1 file list (from `tar -tvf data.tar.xz`), lines:

> -rwxr-xr-x  0 root   root     5064 Jul 22 12:21 ./usr/bin/chromium

> -rwxr-xr-x  0 root   root 314612488 Jul 22 12:21 ./usr/lib/chromium/chromium

Row 9, `/usr/bin/chromium` from that package, lines 9, 12, 153:

> APPNAME=chromium

> LIBDIR=/usr/lib/$APPNAME

>     exec $LIBDIR/$APPNAME $CHROMIUM_FLAGS "$@"

(b) Locators: as above.

(c) Reading. Chromium does not give its child processes distinct short names. Every content process (browser, and each zygote-forked child after it rewrites its command line) sets the kernel short name (`comm`, via `PR_SET_NAME`) to the basename of its own executable, and rewrites the long command-line title to the executable path plus arguments. Process kinds are therefore told apart only by the `--type=…` argument in `/proc/<pid>/cmdline`, not by `comm`. For the Debian trixie package the executable is `/usr/lib/chromium/chromium` (started by the shell wrapper `/usr/bin/chromium` via `exec`), so the short name is `chromium` for browser, zygote, renderer, GPU and utility processes alike. Non-main threads get their own per-thread names (truncated to 15 characters); the main thread is deliberately not renamed. Caveats: (1) the executable basename depends on the build/package — for the Debian package it is `chromium`; Google's own Chrome build was not package-verified here (zygote.md's appendix only shows example paths `/opt/google/chrome-beta/chrome`, which is not packaging evidence). (2) Whether `/proc/self/exe` is readable inside the sandboxed zygote child was not verified; if it is not, the child keeps the `comm` inherited by fork, which is the same executable basename. (3) No documentation page states the Linux process name directly; this is read from code.

(d) Verdict: FOUND (from source code and the Debian package; no prose doc states it).

---

## C-plain-6 — process names under which Windows games run through Proton/Wine on Linux; whether all game threads/processes share one name

### Sub-item 6a — name of the game process itself (Wine, upstream)

(a) Verbatim, row 10 (Wine `wine-11.17`, commit 36b6a2cf).

`dlls/ntdll/unix/env.c` lines 481–505:

> /***********************************************************************
>  *           set_process_name
>  *
>  * Change the process name in the ps output.
>  */
> static void set_process_name( const char *name )
> {
>     const char *p;
>
> #ifdef HAVE_SETPROCTITLE
>     setproctitle("-%s", name );
> #endif
>     if ((p = strrchr( name, '\\' ))) name = p + 1;
>     if ((p = strrchr( name, '/' ))) name = p + 1;
> #ifdef HAVE_SETPROGNAME
>     setprogname( name );
> #endif
> #ifdef HAVE_PRCTL
> #ifndef PR_SET_NAME
> # define PR_SET_NAME 15
> #endif
>     prctl( PR_SET_NAME, name );
> #endif
> }

`dlls/ntdll/unix/env.c` lines 508–535 (`rebuild_argv`, head comment and last lines):

>  * Build the main argv by removing argv[0].

>     main_argv[--main_argc] = NULL;
>     set_process_name( main_argv[0] );
> }

`dlls/ntdll/unix/env.c` lines 2120–2126 (in `init_startup_info`, the path for a process created by another Wine process):

>     status = load_main_exe( &nt_name, machine, &module );
>     if (!NT_SUCCESS(status))
>     {
>         MESSAGE( "wine: failed to start %s: %x\n", debugstr_us(&params->ImagePathName), status );
>         NtTerminateProcess( GetCurrentProcess(), status );
>     }
>     rebuild_argv();

`dlls/ntdll/unix/env.c` lines 1951–1962 (first process started from a Unix command line):

>     if (status)  /* try launching it through start.exe */
>     {
>         static const char *args[] = { "start.exe", "/exec" };
>         free( nt_name.Buffer );
>         if (*module) NtUnmapViewOfSection( GetCurrentProcess(), *module );
>         load_start_exe( &nt_name, module );
>         prepend_argv( args, 2 );
>     }
>     else
>     {
>         rebuild_argv();

`dlls/ntdll/unix/process.c` (`spawn_process`, grandchild) lines 441–443:

>             argv = build_argv( &params->CommandLine, 2 );
>
>             exec_wineloader( argv, socketfd, pe_info );

`loader/preloader.c` lines 1372–1382:

> /* set the process name if supported */
> static void set_process_name( int argc, char *argv[] )
> {
>     int i;
>     unsigned int off;
>     char *p, *name, *end;
>
>     /* set the process short name */
>     for (p = name = argv[1]; *p; p++) if (p[0] == '/' && p[1]) name = p + 1;
>     if (wld_prctl( 15 /* PR_SET_NAME */, (long)name ) == -1) return;

Row 13, `PR_SET_NAME(2const)`:

> Set the name of the calling thread,
> using the value in the location pointed to by
> .IR name .
> .IP
> The name can be up to 16 bytes long,
> .\" TASK_COMM_LEN in include/linux/sched.h
> including the terminating null byte.
> If the length of the string, including the terminating null byte,
> exceeds 16 bytes, the string is silently truncated.

(b) Locators: as above.

(c) Reading. A Windows program run under Wine is a Unix process started from the Wine loader (`wine`, possibly via `wine-preloader`), but once ntdll has loaded the Windows executable it drops the loader from argv and sets the kernel short name to the last path component of the new argv[0] — which is the first token of the Windows command line (e.g. `C:\Games\Game.exe` → `Game.exe`), stripping both `\` and `/` separators. The kernel keeps at most 15 bytes, so long names are cut (e.g. a hypothetical `SomeLongGameName.exe` would show as its first 15 bytes). Caveats: the name comes from the command-line's first token, not necessarily from the image file name; a launch that falls back to `start.exe /exec` gets `start.exe` as argv[0] in that process; the long `/proc/<pid>/cmdline` is also rewritten (setproctitle where available, otherwise in-place argv rewriting). The concrete name of any particular game is not in the source — only the rule.

(d) Verdict: FOUND.

### Sub-item 6b — the Wine helper processes and their names

(a) Verbatim, row 10.

`dlls/ntdll/unix/loader.c` lines 506–524 (`exec_wineserver`, excerpt):

>     if (!build_path_and_exec( pid, bin_dir, "wineserver", argv )) return 0;
>     if ((path = getenv( "WINESERVER" )) && !build_path_and_exec( pid, "", path, argv )) return 0;

>     return build_path_and_exec( pid, BINDIR, "wineserver", argv );

`programs/wineboot/wineboot.c` lines 1465–1472:

> static BOOL start_services_process(void)
> {
>     static const WCHAR svcctl_started_event[] = SVCCTL_STARTED_EVENT;
>     PROCESS_INFORMATION pi;
>     HANDLE wait_handles[2];
>
>     if (!create_native_process( L"C:\\windows\\system32\\services.exe", NULL,
>                                 TRUE, DETACHED_PROCESS, L"C:\\windows\\system32", &pi))

`programs/services/services.c` lines 837–841:

>     if (!(*path = malloc(wcslen(system_dir) * sizeof(WCHAR) + sizeof(L"\\winedevice.exe"))))
>        return ERROR_NOT_ENOUGH_SERVER_MEMORY;
>
>     lstrcpyW(*path, system_dir);
>     lstrcatW(*path, L"\\winedevice.exe");

`dlls/win32u/winstation.c` lines 828–832:

>         static const WCHAR appnameW[] = {'\\','?','?','\\','C',':','\\','w','i','n','d','o','w','s',
>             '\\','s','y','s','t','e','m','3','2','\\','e','x','p','l','o','r','e','r','.','e','x','e',0};
>         static const WCHAR cmdlineW[] = {'"','C',':','\\','w','i','n','d','o','w','s','\\',
>             's','y','s','t','e','m','3','2','\\','e','x','p','l','o','r','e','r','.','e','x','e','"',
>             ' ','/','d','e','s','k','t','o','p',0};

`loader/wine.inf.in` lines 976–979 and 1064–1069:

> [RpcSsService]
> Description="RPC service"
> DisplayName="Remote Procedure Call (RPC)"
> ServiceBinary="%11%\rpcss.exe"

> [PlugPlayService]
> Description="Enables automatic configuration of devices"
> DisplayName="Plug and Play Service"
> ServiceBinary="%11%\plugplay.exe"
> ServiceType=32
> StartType=2

(b) Locators: as above.

(c) Reading. Besides the game, a Wine prefix runs `wineserver` (a native Unix binary exec'd by that name) and Windows-side helper programs that go through the same process-creation path and hence the same naming rule: `services.exe` (started by wineboot), `winedevice.exe` (driver host started by services), `explorer.exe` (started with `/desktop` for the desktop window), and service binaries such as `rpcss.exe`, `plugplay.exe` (auto-start, StartType=2) and `svchost.exe` entries in wine.inf. By the rule in 6a their short names are those `.exe` names. Caveat: which helpers are alive at a given moment depends on prefix state and what the game uses; no single source lists "the processes of a running game".

(d) Verdict: FOUND (per named helper: wineserver FOUND, services.exe FOUND, winedevice.exe FOUND, explorer.exe FOUND, rpcss.exe/plugplay.exe FOUND as service binaries; their runtime short name is an inference from the 6a rule, not a separate statement).

### Sub-item 6c — Proton's launch chain and the names it adds

(a) Verbatim, row 11 (Proton `proton-11.0-2`).

`toolmanifest_x86_64.vdf`:

> "manifest"
> {
>   "version" "2"
>   "commandline" "/proton %verb%"
>   "require_tool_appid" "4183110"
>   "use_sessions" "1"
>   "compatmanager_layer_name" "proton"
> }

`proton` lines 543–544:

>         self.wine_bin = self.bin_dir + "wine"
>         self.wineserver_bin = self.bin_dir + "wineserver"

`proton` lines 2055–2085 (excerpt):

>     def run(self):
>         if shutil.which('steam-runtime-launcher-interface-0') is not None:
>             adverb = ['steam-runtime-launcher-interface-0', 'proton']
>         else:
>             adverb = []

>             if g_proton.host_pe_arch == "x86_64-windows":
>                 #run with winepreloader directly to avoid restart through start.exe
>                 self.env["WINELOADERNOEXEC"] = "1"
>                 argv = [g_proton.lib_dir + "/wine/x86_64-unix/wine-preloader", g_proton.lib_dir + "/wine/x86_64-unix/wine", "c:\\windows\\system32\\steam.exe"]
>             else:
>                 argv = [g_proton.wine_bin, "c:\\windows\\system32\\steam.exe"]
>
>         rc = self.run_proc(adverb + argv + sys.argv[2:] + self.cmdlineappend)

`proton` lines 2126–2130:

>     elif sys.argv[1] == "waitforexitandrun":
>         #wait for wineserver to shut down
>         g_session.run_proc([g_proton.wineserver_bin, "-w"])
>         #then run
>         rc = g_session.run()

`steam_helper/steam.c` lines 417–419 and 637:

> static HANDLE run_process(BOOL *should_await, BOOL game_process)
> {
>     WCHAR *cmdline = GetCommandLineW();

>         if (!CreateProcessW(NULL, new_cmdline, NULL, NULL, FALSE, flags, NULL, NULL, &si, &pi))

Row 12, Valve Wine fork @ dc26e618, `dlls/ntdll/unix/env.c` lines 488–507 (same logic as upstream):

> static void set_process_name( const char *name )
> {
>     char *p;
>
> #ifdef HAVE_SETPROCTITLE
>     setproctitle("-%s", name );
> #endif
>     if ((p = strrchr( name, '\\' ))) name = p + 1;
>     if ((p = strrchr( name, '/' ))) name = p + 1;
> #ifdef HAVE_SETPROGNAME
>     setprogname( name );
> #endif
> #ifdef HAVE_PRCTL
> #ifndef PR_SET_NAME
> # define PR_SET_NAME 15
> #endif
>     prctl( PR_SET_NAME, name );
> #endif
> }

(b) Locators: as above.

(c) Reading. Steam starts Proton through the `proton` Python script (short name of that process would be the interpreter's, not verified here), optionally through `steam-runtime-launcher-interface-0`, inside a tool with app id 4183110 (a Steam Linux Runtime container; its identity is only the number in this source). The script runs Wine on Proton's built-in `c:\windows\system32\steam.exe` helper, which then `CreateProcessW`s the game's command line. So under Proton the process tree has at least a `steam.exe` process (Proton's helper, not the real Steam client) and the game process, plus `wineserver` and the Wine helpers from 6b. Valve's Wine fork at the pinned commit uses the same `set_process_name` code, so the game's short name follows the 6a rule (`<first command-line token basename>`, ≤15 bytes). Caveat: `reaper` and pressure-vessel wrapper names are covered in 6c-bis; the Steam client's own process name was not verified (closed source).

(d) Verdict: FOUND for `proton` → `steam.exe` → game chain and naming rule. (`reaper` / pressure-vessel names: see 6c-bis.)

### Sub-item 6c-bis — `reaper`, pressure-vessel and Steam Linux Runtime wrapper process names (added in the resumed pass)

Copy: steam-runtime-tools, https://gitlab.steamos.cloud/steamrt/steam-runtime-tools.git, tag `v0.20260903.0` = commit `06a2477429fe271c5b254399caffdab8b7737e99` (2026-09-03; highest tag in `git ls-remote` on 2026-09-13), shallow clone at `S/C-plain-6/steam-runtime-tools/`.

(a) Verbatim.

`docs/steam-compat-tool-interface.md` lines 528–530:

> In recent versions of Steam, the game process is wrapped in a `reaper`
> process which sets itself as a subreaper using `PR_SET_CHILD_SUBREAPER`
> (see [**prctl**(2)][prctl] for details).

Same file lines 567–570:

> Some Windows games, such as Soldat (638490), do not have an
> "install script" in their metadata. Running these games behaves much the
> same as a native Linux game: it is wrapped in a subreaper, version 1
> compat tools are not invoked specially, and version 2 compat tools

Same file lines 517–522:

> For example, when using Proton with "Steam Linux Runtime 2.0 (soldier)", the
> "outer" compatibility tool "Steam Linux Runtime 2.0 (soldier)" is run with
> `LD_LIBRARY_PATH` set by the Steam Runtime to point to mixed host and
> scout libraries. After setting up the container, it runs the "inner"
> compatibility tool (Proton) with an entirely new `LD_LIBRARY_PATH`
> pointing to mixed host and soldier libraries.

`pressure-vessel/wrap.1.md` line 28 and lines 1757–1760:

> **pressure-vessel-wrap** runs *COMMAND* in a container, using **bwrap**(1).

> The **pressure-vessel-wrap** process replaces itself with a **bwrap**(1)
> process. Fatal signals to the resulting **bwrap**(1) process will result
> in `SIGTERM` being received by the **pressure-vessel-wrap** process
> that runs *COMMAND* inside the container.

`pressure-vessel/adverb.1.md` lines 46–58:

> **pv-adverb** acts as the top-level process inside a Steam Linux Runtime
> container
> (the direct child of **bwrap**(1))
> with any other processes that will run inside the container,
> for example a game or an interactive shell,
> as its children.
> This means that it can supervise those processes and alter their execution
> environment.
>
> **pv-adverb** acts as a subreaper.
> This means that if the *COMMAND* starts background processes,
> they will be reparented to **pv-adverb** instead of to **init**
> when their parent process exits.

`pressure-vessel/meson.build` lines 141–142 and 232–233 (executable names):

```
pv_bin += executable(
  'pv-adverb',
```
```
pv_bin += executable(
  'pressure-vessel-wrap',
```

`bin/meson.build` line 37, line 122, and lines 252–261 (excerpt):

```
  { 'name': 'launcher-interface-0', 'glib': false },
```
```
  name_prefix = bin_details.get('prefix', 'steam-runtime-')
```
```
bubblewrap_subproject = subproject(
  'bubblewrap',
...
    'program_prefix=srt-',
```

(b) Locators: steam-runtime-tools v0.20260903.0, files and lines as given.

(c) Reading. Under Steam, the game (native or Proton) is wrapped by a Steam-client process named `reaper` that acts as a subreaper; the `reaper` binary is part of the closed-source Steam client, so its name here rests on this Valve-maintained interface document, not on its code. When Proton runs inside a Steam Linux Runtime container, the outer tool starts `pressure-vessel-wrap`, which replaces itself with `bwrap` (the bundled build is named `srt-bwrap` by `program_prefix=srt-`; whether the bundled or a host `bwrap` is used in a given run was not checked), and inside the container `pv-adverb` is the top-level process and subreaper, with Proton's `proton` script, Wine and the game below it. Proton's `proton` script calls `steam-runtime-launcher-interface-0` when present (6c); that executable name comes from the `steam-runtime-` default prefix plus `launcher-interface-0`. Short names (`comm`) by the 15-byte truncation rule (row 13), derived, not observed: `reaper`, `pv-adverb`, `bwrap`/`srt-bwrap` unchanged; `pressure-vessel-wrap` → `pressure-vessel`; `steam-runtime-launcher-interface-0` → `steam-runtime-l`. Caveat: whether `pressure-vessel-wrap` itself or `steam-runtime-launcher-interface-0` stays alive as a separate process during play (vs `exec`) was only read for `pressure-vessel-wrap` (it replaces itself).

(d) Verdict: FOUND for `reaper` (documented wrapper, closed-source binary), `pressure-vessel-wrap` → `bwrap`, `pv-adverb`; PARTIAL for which `bwrap` build runs and for whether `steam-runtime-launcher-interface-0` persists.

### Sub-item 6d — whether all game threads/processes share one name

(a) Verbatim, row 10.

`dlls/kernelbase/thread.c` lines 463–478:

> HRESULT WINAPI DECLSPEC_HOTPATCH SetThreadDescription( HANDLE thread, PCWSTR description )
> {

>     return HRESULT_FROM_NT(NtSetInformationThread( thread, ThreadNameInformation, &info, sizeof(info) ));
> }

`dlls/ntdll/unix/thread.c` lines 2640 and 2666 (in `NtSetInformationThread`):

>     case ThreadNameInformation:

>         set_native_thread_name( handle, &info->ThreadName );

`dlls/ntdll/unix/thread.c` lines 2076–2111 (Linux branch of `set_native_thread_name`, excerpt):

> static void set_native_thread_name( HANDLE handle, const UNICODE_STRING *name )
> {
> #ifdef linux

>     if (unix_pid != getpid())
>     {
>         static int once;
>         if (!once++) FIXME("cross-process native thread naming not supported\n");
>         return;
>     }
>
>     len = ntdll_wcstoumbs( name->Buffer, name->Length / sizeof(WCHAR), nameA, sizeof(nameA), FALSE );
>     snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);
>     if ((fd = open( path, O_WRONLY )) != -1)
>     {
>         write( fd, nameA, len );
>         close( fd );
>     }

`include/winternl.h` lines 4096–4098:

>    undocumented exception understood by MS VC debugger, allowing the program
>    to name a particular thread. */
> #define EXCEPTION_WINE_NAME_THREAD     0x406D1388

`dlls/ntdll/exception.c` lines 257–268:

>     case EXCEPTION_WINE_NAME_THREAD:
>         if (rec->ExceptionInformation[0] == 0x1000)
>         {
>             const char *name = (char *)rec->ExceptionInformation[1];
>             DWORD tid = (DWORD)rec->ExceptionInformation[2];
>
>             if (tid == -1 || tid == GetCurrentThreadId())
>                 WARN_(threadname)( "Thread renamed to %s\n", debugstr_a(name) );
>             else
>                 WARN_(threadname)( "Thread ID %04lx renamed to %s\n", tid, debugstr_a(name) );
>             set_native_thread_name( tid, name );
>         }

`dlls/rpcrt4/rpc_server.c` line 554 (one example of Wine naming its own threads):

>   SetThreadDescription(GetCurrentThread(), L"wine_rpcrt4_io");

Row 12, Valve Wine fork @ dc26e618, `dlls/ntdll/unix/thread.c` line 2043:

>     snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);

(b) Locators: as above.

(c) Reading. No. Threads do not all share the process name. On Linux, Wine (upstream 11.17 and Valve's fork used by Proton 11.0-2) writes a thread's Windows name into that thread's `/proc/<pid>/task/<tid>/comm` whenever the program names it — via `SetThreadDescription` or via the MSVC debugger exception `0x406D1388` — and Wine names its own internal worker threads (e.g. `wine_rpcrt4_io`). Threads that are never named keep the name inherited at creation, which for threads created after `set_process_name` is the game's short name. Processes also do not share one name: each process (game, `steam.exe`, `wineserver`, `services.exe`, `winedevice.exe`, `explorer.exe`, …) gets its own short name per 6a/6b. Caveats: names are truncated to 15 bytes by the kernel (man page row 13); cross-process thread renaming is not supported (FIXME branch); whether a given game names its threads is game-specific and not in the source. Chromium, by contrast, deliberately never renames its main thread (C-plain-1c).

(d) Verdict: FOUND.

---

## Verdict summary for this part

- C-plain-1a (processes in a session): FOUND
- C-plain-1b (renderer ↔ tab/site mapping): FOUND
- C-plain-1c (process name on Linux): FOUND (code + Debian package; no prose doc)
- C-plain-6a (game process name rule, Wine): FOUND
- C-plain-6b (Wine helper process names): FOUND
- C-plain-6c (Proton chain): FOUND for proton → steam.exe → game
- C-plain-6c-bis (reaper / pressure-vessel / pv-adverb names): FOUND; PARTIAL on which bwrap build runs and whether steam-runtime-launcher-interface-0 persists
- C-plain-6d (shared name for threads/processes): FOUND — they do not all share one name

Unreachable: packages.debian.org file-list and package pages (PoW challenge page, HTTP 200) — replaced by the .deb from deb.debian.org.
