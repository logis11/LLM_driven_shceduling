# Task 9.8 — changelog

One entry per decision applied to `dataset/archetypes.yaml` (and the registry lines it owns). Parameter, old value, new value, source id and locator or the label, commit. References are the search records' candidate ids (`search/candidates.md`); the 2026-09-20 retrieval retry and the `scx_lavd` column semantics are `search/S1-literature.md` §4 and `search/S3-traces-datasets.md` §4.

## D1 — `electron-comms` split per bound program (2026-09-20)

By 인지오's decision, scope-card items 11–14 (with items 1–10 and 15–17 depending on them): `electron-comms` is replaced by one archetype per bound program, each grounded on one observation of that program under phase decision 2, the form 9.5 D2 gave `desktop-interactive` and 9.7 D1 gave `io-stream` and `network-bulk`. Across the coreset the entry carries 125 tasks: `chrome` renderers 102, `steamwebhelper` 9, `steam` 6, `thunderbird` 3, `discord` 3, `zoom` 2. Grounds: the entry's two values describe no process that was observed — the measurement audit classes both X, `heartbeat.median_us` 1 850 000 being the geometric centre between the Element main process (wake gap 0.40–0.43 s) and its GPU and network-service helpers (3.84–3.92 s) with a plain median of 3.86 s and no process waking near 1.85 s, and `heartbeat_work.median_us` 289 sitting between helpers (128–197 µs) and main processes (531–857 µs), with no Element renderer process in any repeat; the bound programs' documented structures differ from each other and from the measured one — Chromium's site-per-process model and its background-page throttling (S2-01, S2-06) against an Electron main process that inherits that throttling only where `backgroundThrottling` is kept (S2-08), against the Steam client's CEF browser-engine helper with no documented options or helper counts (S2-19…S2-22); and no class found an observation covering the archetype whole, or any bound program as a per-wake distribution (`search/candidates.md`, Not found). Not taken: one archetype re-measured on a single program with every binding kept under stated binding notes (the form of 9.5 D11 and 9.7 D4) — the renderer family is 102 of the 125 bound tasks and is directly observable on a pinned runner (S4-08), so the substitution would carry the dataset's heaviest binding where grounding is obtainable, against phase decision 4; one entry re-anchored to the renderer with the other families rebound. The archetype ids, each program's observation and the parameters are decided in the entries that follow. Hands to 9.10: every `electron-comms` binding in the C1, C2, C3, C4, C6 and C7 timelines rebinds. No value changed by this entry.

## D2 — Chrome's renderer processes keep a task of their own, as a measured archetype (2026-09-20)

By 인지오's decision, scope-card item 11: Chrome's renderer processes do not fold into `web-browser`'s one task; they take a measured archetype of their own, and the 102 renderer-bound tasks keep their identity as tasks. Grounds: 9.5 D14's carve-out is deference to this binding rather than a claim about renderers — it gives a measured archetype's task "every process of the application's tree, all threads merged into one event stream, except processes another archetype already owns — today Chrome's renderer processes (`electron-comms`, 9.8's, bound separately in every timeline that carries `chrome`)", and hands 9.8 "the Chrome runs' renderer rows as an observation of Chrome renderers on a static local page (stated scope)"; the same entry records VS Code's task carrying main, renderer, GPU and five utility processes merged, with its renderer holding idle CPU 0.011 of the application's 0.020, so an Electron renderer already sits inside its application's single task elsewhere in the dataset and Chrome's renderers are singled out only by the binding being dissolved here. The decision rests on the experiment's subject: the number of independently schedulable entities is a first-order property of a scheduling workload, and merging 102 renderer tasks into the browser tasks beside them changes what contends for the CPU, not only where the values come from. Not taken: folding the renderers into `web-browser` under 9.5 D9 and D14's merge rule, measured on a Chrome holding loaded tabs so that the renderers fall inside the observation — consistent with the dataset's one-application-one-task rule, and rejected on the entity-count ground above; it would also make the tab count a scope statement of the measurement rather than a per-file quantity. Hands to 9.10: the per-file renderer counts, and that under Chromium's documented process model a renderer task stands for one site-locked process rather than one tab (S2-01), so a count is a count of sites. No value changed by this entry.

## D3 — the renderer archetype's subject is the terminal steady state of a backgrounded, loaded renderer (2026-09-20)

By 인지오's decision, scope-card items 1–5 and the phase design of the campaign that will fill them: the renderer archetype of D2 describes a loaded, site-locked renderer that has been backgrounded past Chromium's intensive-wake-up-throttling grace period, and its values are measured in that state. Grounds: the regime boundary is documented rather than inferred (S2-06, chromium/src commit `999361f1b2e1018113fae76d308ea0e6c677fc31`) — a hidden page's timer wake-ups are aligned to one per second (`kDefaultThrottledWakeUpInterval`), intensive throttling drops them to one per minute (`kIntensiveThrottledWakeUpInterval`) after a grace period of five minutes by default and **sixty seconds for a page that has finished loading**, a throttled wake-up window is 3 ms (`kThrottledWakeUpDuration`), a CPU-time budget of 1 % of wall time applies ten seconds after backgrounding (`kDefaultBackgroundBudgetAsCPUFraction`, `kThrottlingDelayAfterBackgrounding`), and freezing of background task queues is enabled by default only on Android (`kStopInBackground`), so a Linux background tab keeps running; a hidden renderer is renice'd to 5 only where the browser can undo it and is otherwise left at its priority (S2-03). The archetype form cannot express a behaviour valid only for an opening stretch of a task's life — `lifetime` is segment-bound and the parameters carry no expiry, and the only time-bounded mechanism the dataset has is an operation, a span the compiler swaps in for a triggered action (9.5 spec decisions 8–10) — so an archetype must hold for as long as the task bound to it lives. The pre-grace regime always ends; the post-grace regime does not. The settle is therefore the documented grace, the same rule 9.5 D34 set when it required a steady phase to begin after launch and ramp-up work, with a stated boundary in place of a trace-set one, and it is confirmed rather than assumed by a long-phase probe (`meas-long-probe.yml`; `campaign/slices.py` prints the steady phase's CPU and wakes per 10 s slice), per 9.5 D35. Stated limit, from S2-06's own coverage: the documented budgets bind page JavaScript on the renderer's main thread, not the renderer process — its compositor and other threads are outside them — so the documentation fixes the state the measurement must hold, not the values it will report. Not taken: the just-backgrounded regime (one wake per second under the 1 % budget) as the subject, which is real but time-limited by construction and unexpressible in the archetype form; one measurement spanning the transition, which would centre a gap distribution between a one-second and a one-minute mode and describe neither — the defect this slice is replacing; the two regimes as two entries. Hands to 9.10: a timeline depicting a tab the user has just switched away from is not covered by this entry and would need its own observation. No value changed by this entry.

## D4 — the renderer archetype is two entries, one per terminal state of an idle renderer (2026-09-20)

By 인지오's decision, widening D3's scope: the renderer archetype of D2 is two entries — an **idle hidden renderer**, D3's subject, a loaded site-locked renderer past Chromium's intensive-wake-up-throttling grace, and an **idle visible renderer**, one whose page Blink still counts as visible because it is unattended or merely covered by another window. Grounds: both are terminal states under D3's rule that an archetype must hold for as long as the task bound to it lives, and they are distinguished by something a timeline can assert. The visible state is not a transient on Linux: Chromium tracks cross-application window occlusion only on Windows — every body of `ui/aura/native_window_occlusion_tracker.cc` is wrapped in `#if BUILDFLAG(IS_WIN)` and `IsNativeWindowOcclusionTrackingAlwaysEnabled` returns false in the `#else` branch, while aura's own tracker counts a window occluded only when covered by other aura windows (S2 §4.2, chromium/src commit `30010bf0577ed988b2598b70465d708523064712`) — so a renderer whose window sits behind another application's window stays visible to Blink indefinitely and is never throttled. Not taken: one entry with the visible state carried as an approximation of the hidden one — the two differ by the throttling budgets of S2-06, one wake per second against one per minute, about sixtyfold in wake rate, which is not an approximation; the visible state as an operation (it is a standing state, not a triggered span). Both entries come from the same campaign, each its own phase, so each rests on one observation under phase decision 2. Hands to 9.10: a timeline binding a renderer task states which of the two states it depicts. No value changed by this entry.

## D5 — `steamwebhelper` binds to the idle visible renderer by stated approximation (2026-09-20)

By 인지오's decision, scope-card item 13, the `steamwebhelper` half: the nine `steamwebhelper` tasks bind to D4's idle visible renderer entry by stated approximation, under D1's fallback that a program with no obtainable observation binds to the nearest observed archetype with the limitation in its `modeling_notes` — 9.7 D1's rule, in the form of 9.5 D11 and 9.7 D4. Grounds: `steamwebhelper` is the client's Chromium Embedded Framework host, its renderer children carry Chromium's own `--type=renderer` marker (S3-28), and CEF neither disables nor exposes Blink's background-page throttling — a repository-wide search at commit `5df187ece78562092d93801c7004e2c583818ffa` returns no hit for `disable-background-timer-throttling`, `background_throttling`, `IntensiveWakeUpThrottling` or `kDisableBackgroundTimerThrottling` against a control query that does return its files, and CEF ships no equivalent of Electron's `backgroundThrottling` preference (S2 §4.1) — so a Steam helper renderer is a Chromium renderer. Which of D4's two states it occupies behind a game is stated by no Valve source, and three findings point to the visible one: on Linux nothing marks a covered window's pages hidden (S2 §4.2); the shipped client carries an explicit `background_throttling_disabled` browser-view field (S2 §4.3); and the one `scx_lavd` row of a `steamwebhelper` thread sampled while a Steam-launched Proton game ran gives a run-plus-wait cycle of about 18 ms (S3 §4.2 with the column semantics of §4.4), three orders of magnitude from one wake per minute. Stated limits for the modeling note: Steam carries its own `CMsgWasHidden` and `CMsgSetWindowVisibility` message types, so it can hide its views and no source says whether it does behind a game; the single in-game row cannot be attributed to a renderer rather than to the CEF browser process, because the log records the thread comm and not the command line and the one in-game `ps` snapshot shows a separate `steamwebhelper --type=renderer` at 0.0 % CPU (S3-28); and the direction of the error — if Steam's views are hidden and throttled behind a game, this binding overstates their wake rate. Not taken: binding to D3's hidden entry, which the three findings point away from; retiring the binding in the form of 9.7 D5, when the helper is a real named process of the session 9.10 depicts; measuring the Steam client on the runner as this binding's source, since the depicted state — the client behind a running game — is not obtainable there (S4 §3). Open and settleable on our own venue without a game: which CEF mode the client uses and which switches it passes, by running the client under Xvfb and reading `/proc/<pid>/cmdline` for every helper, and whether the helper's wake behaviour changes when the client window is minimised (S2 §4.4); if that probe runs before the fold-in its result replaces the inference above. The `steam` client-process binding, six tasks, is decided separately. No value changed by this entry.

## D6 — `steam` takes its own entry, measured on the desktop client run logged out on the runner (2026-09-20)

By 인지오's decision, scope-card item 13, the `steam` half: the six `steam` tasks take an archetype of their own, its values measured on Valve's desktop client run on a pinned single-core runner under Xvfb, **logged out**, in the same probe that settles D5's open questions — the client's CEF mode, the switches it passes to each helper, and whether the helper's wake behaviour changes when the client window is hidden. The entry carries a scope statement in the form of 9.7 D4: the client observed holds no account and no library and is not behind a running game, against timelines that depict a client behind a game, with the direction of the error stated. Grounds for an entry rather than a rebinding: `steam` is the client's own native process and matches no measured archetype in the dataset — the nearest by shape, `system-daemon`, is a pool of 51 stock system services (systemd family, dbus, cron) from the same four-vCPU `meas-ci:gui:2` run this slice is dismantling, with a wake gap of 11.24 s against the sub-millisecond cycle of the one in-game sample, so binding to it would repeat at class level the defect D1 removes; and the probe that D5 already requires makes the marginal cost of the observation one analysis pass rather than a campaign. **No account is used, and none may be.** Steam Subscriber Agreement §4.C, Automation: "You may not use any form of scripts, bots, macros, or other non-human-controlled systems ("Automation") to interact with Content and Services on Steam in any manner, including but not limited to: Automating the Steam account creation process, Faking gameplay statistics (e.g., inflated wins or losses, XP, playtime), Earning rewards or progress without genuine user input"; §1.C, Your Account: "Your Account … is strictly personal" and "You may not reveal, share or otherwise allow others to use your password or Account except as otherwise specifically authorized by Valve" (copy read: `https://store.steampowered.com/subscriber_agreement/`, fetched 2026-09-20, HTTP 200, 85 954 bytes, SHA-256 `4ece1a95168e325719ea60499bbdb6225b18872b2351074b28199fd16ff475cd`, under `sources/A-2026-09-20/`). The probe therefore signs into nothing, drives no store and performs no account action; it installs and launches the client and observes it. Fallback, recorded as the probe's result rather than decided in advance: if the client does not hold a stable state logged out under Xvfb — which the search could source only to forum posts (S4-18, S4-22) — the binding is retired to 9.10 in the form of 9.7 D5. Not taken: binding to `system-daemon` (unrelated observation, and 9.9 has not landed); retiring the binding outright, which would foreclose 9.10's choice of whether a gaming timeline names a Steam process, a timeline question rather than this slice's. Hands to 9.7: its D4 escape clause — "A probe of the desktop client under Xvfb with a dedicated account is not scheduled: it runs only if 인지오 provides an account, and if the client can be driven, a measured archetype replaces the approximation" — is foreclosed by the two clauses above and should be withdrawn, so that the SteamCMD stand-in is stated as the basis rather than as provisional; its "Not taken" parenthetical "Valve's terms on automated use of an account unchecked" is now checked and should carry the passages above; and this probe's process tree supplies the observation D4's binding note currently asserts without one, namely what the desktop client runs that SteamCMD does not. No value in 9.7 changes: its campaign logs in with `+login anonymous` at every call site of `dataset/tools/meas/background/run.sh` and fetches only depots from the anonymous dedicated-server list Valve publishes, so §1.C does not reach it, and SteamCMD is Valve's own client published for scripted deployment while §4.C's enumerated prohibitions are account-abuse cases. Hands to 9.10: whether a gaming timeline names a `steam` process at all, and in which state. No value changed by this entry.

## D7 — a measured Electron chat-client archetype; `discord` binds to it and the overlay role is withdrawn (2026-09-20)

By 인지오's decision, scope-card item 12, the `discord` half: an Electron chat-client archetype is created and measured on Element Desktop against a Matrix homeserver run on the harness's own CPUs — idle and under scripted message traffic — in this slice's campaign; the three `discord` tasks bind to it by stated approximation under D1's fallback; and the `injected-overlay` role those tasks carry is withdrawn. Grounds: Discord's game overlay does not exist on the platform this dataset models. Discord's own support article "Game Overlay 101" states "NOTE: The overlay is compatible with Windows OS only; it does not function on Mac OS or Linux" and, in its FAQ, "A: The overlay is compatible with Windows 10 & 11 only; it does not function on Mac OS or Linux" (S2 §5; Wayback memento 2026-01-02T16:50:30Z, the live page answering 403 to scripted access as it did for the S3 reader). The response side of this dataset is Linux only, so a task standing for an injected Discord overlay describes something that cannot happen. Discord itself cannot be observed on our venue: its Linux package is a bootstrapper that downloads an unpinned client at first run and reaches only a login screen without an account, and no self-hosted server exists for the official client (S2-18, S4-15, S4 §3). Element is the substitute this dataset already declares in `electron-comms`'s present notes — "stated substitute for account-gated comms apps" — and unlike Discord it is observable whole: Element Desktop from the unauthenticated apt repository, pointed through its config environment variable at Synapse, Conduit or Dendrite on the harness CPUs with registration enabled, driven by a script sending `m.room.message` events (S4-11…S4-14). The binding note carries what Discord does that Element does not — a gateway heartbeat at a server-assigned interval, documented example 45 s (S2-10), against Matrix's 30 s `/sync` long poll (S2-12, S2-13) — that no class found any Linux observation of Discord with a wake cadence or CPU per wake (`search/candidates.md`, Not found T2), and the direction of the error as the run shows it. Not taken: retiring the binding, when what the finding removes is the task's role and not its existence — a chat client running during a gaming session is an ordinary Linux desktop situation; binding to either renderer entry of D4, since an Electron client's main process is not a renderer and that distinction is what D1 exists to keep. Hands to 9.10: the `injected-overlay` role is withdrawn from the `c3-evening`, `c4-gaming` and `c4.variant` task entries, and what those tasks depict is a chat client running during the session. No value changed by this entry.

## D8 — the `zoom` helper binding is retired (2026-09-20)

By 인지오's decision, scope-card item 12, the `zoom` half: the two `zoom` helper tasks in `c1-meeting` and `c7-meeting` are retired, in the form of 9.7 D5. Grounds: the task's role is stated nowhere except by analogy to the Discord overlay — `c1-meeting.timeline.yaml:6–7` reads "the call's audio path binds audio-playback as S9's does; one electron-comms helper **as C4's discord overlay does**" — and that overlay does not exist on Linux (D7, S2 §5). No source in any class states what a second process beside a Zoom call does (`search/candidates.md` item 12; Not found T2), and the call itself is already carried by 9.5's `video-call`, measured as a loopback WebRTC call in Chrome (9.5 D25). Putting a measured value under a role no observation describes is the defect D1 removes, and it would be worse here than removing the task, because the value would look grounded while the role stayed invented. Not taken: binding to D7's chat-client entry — Zoom is not a Matrix client, and what is missing is the helper's role rather than its program; measuring Zoom on the runner — a guest or test-meeting join reaches Zoom's servers and a call with media needs a `v4l2loopback` module whose load on the runner's Azure kernel is undocumented (S4-19, S4-23), and none of that would supply the missing role. Hands to 9.10: the meeting timelines lose the helper task; if a second process beside a call is wanted there, 9.10 states what it represents and this slice binds it then. No archetype value changed by this entry.

## D9 — the `thunderbird` tasks rebind to `mail-client` (2026-09-20)

By 인지오's decision, scope-card item 14: the three `thunderbird` tasks bound to `electron-comms` in `c1-office`, `c4-office` and `c7-office` rebind to `mail-client`, 9.5's per-application archetype measured on Thunderbird. Grounds: this is an identity binding — the task names the program the archetype is measured on — so it needs neither an approximation nor a stated role, which is what D1 asks of every binding it can get. In each of the three files the `thunderbird` task is the only mail task, so the rebinding duplicates nothing. The depicted state fits the form: a measured per-application archetype carries `components` for the application's idle behaviour and `focus_components` with `stimulus` for its focus windows (9.5 D16–D18), so a mail task with no focus window draws the idle components, which is what a background mail client in an office file is. Together with 9.7 D3, which makes the send an operation of `mail-client` instead of a `network-bulk` task, this collapses all nine `thunderbird` bindings in the coreset — three on `mail-client`, three on `network-bulk`, three on `electron-comms` — onto one archetype, and closes the open item that `thunderbird` is bound three ways with each non-identity binding needing a stated role. Not taken: binding to D7's Electron chat-client entry because the ananicy catalogue files `thunderbird` under `Chat` beside `discord`, `element-desktop`, `slack` and `zoom` (S2-23) — that catalogue is a treatment profile and not a behaviour class, and the binding would put a Thunderbird-named task on an Element measurement while a Thunderbird measurement exists. Hands to 9.10: the office files' mail tasks carry `mail-client`; whether an office timeline holds a mail task at all, and whether a send operation is placed in one, stays 9.10's. No value changed by this entry.

## D10 — the four entries take the per-thread-comm component form with no focus side; the hidden renderer's phase length comes from a long-phase probe (2026-09-20)

By 인지오's decision, scope-card item 17 and the form half of items 1–5: the four entries created by D4, D6 and D7 carry 9.5's measured per-application form — `components`, one per thread comm, each with its `wakes_per_s` and its measured `gap` and `run` quantile tables (9.5 D16–D17), with a pooled residual for the comms below the coverage cut — and the old two-parameter shape of `electron-comms`, one lognormal `heartbeat` period and one lognormal `heartbeat_work` burst, is retired with the entry. Grounds: the instrument produces this form directly, since `perf sched` yields per-thread gap and run distributions per phase; it preserves the thread structure of each program, which is the quantity a scheduling experiment contends over; and the header of `dataset/archetypes.yaml` already states this form for every `category_source: meas` archetype, so adopting it makes a sentence true that `electron-comms` has been contradicting. **None of the four carries `focus_components` or `stimulus`**, and that absence is a statement rather than an omission: all four describe unattended states by construction — a hidden renderer is never focused, a visible idle renderer is not being interacted with, Element under scripted traffic receives messages rather than user input, and a logged-out Steam client has nothing driving it — so the input-driven half of 9.5's form does not apply to them. Consequence carried into the campaign method, named here rather than met mid-campaign: an intensively throttled page's documented budget is one wake per minute (S2-06), so a phase of a few minutes would yield of the order of ten wakes on the throttled thread, which is too few for a quantile table and too noisy a per-repeat mean for the stability rule's half-width to converge at any repeat count. The hidden renderer's phase length is therefore set from evidence — one long-phase probe first, its steady phase read per 10 s slice (`meas-long-probe.yml`, `campaign/slices.py`), the phase set from what it shows — which is the rule 9.5 D35 established for exactly this case, rather than chosen in advance. The other three entries are not throttled and are not expected to need it, but each phase length is stated in the method before the first batch either way. Not taken: keeping a two-parameter lognormal shape for the new entries, which would discard the per-thread structure the instrument measures and repeat the form whose averaging across a mixed process set produced the defect D1 removes. Hands to 9.13: the four entries' fields follow this form at the rebuild. No value changed by this entry.

## D11 — the chat-client entry reads the idle state; the traffic phase is measured beside it and kept in the results (2026-09-20)

By 인지오's decision, refining D7: the Electron chat-client archetype takes its values from Element idling against a Matrix homeserver on the harness CPUs with no messages sent, and every repeat also runs a phase under scripted message traffic whose values stay in the campaign results without feeding the archetype. Grounds: no class found any statement of how often a real user's chat client receives messages. What the search found are keep-alive cadences — Discord's gateway heartbeat at a server-assigned interval, documented example 45 s (S2-10), and Matrix's 30 s `/sync` long poll (S2-12, S2-13) — which are the client holding its connection open, not a message rate. A carried under-traffic value would therefore rest on a rate we chose, and that rate would drive the values, which is the ground on which 9.7 D5 retired `background-crawler`. The idle state needs no such number: it is fixed by the client and the homeserver alone. The two-phase shape is 9.7 D6's for `borg`, where every repeat runs a first backup and a repeat backup, the archetype reads the first because only its values are determined by the input alone, and the second stays in the campaign results so a later entry can be made from it. Stated limitation, inherited but for the first time quantified: the entry being replaced already concedes that an idle client "lacks message-traffic wakes"; under this decision the traffic phase is measured beside the idle one, so the size of that gap is recorded rather than only declared, with its rate labelled design. Not taken: carrying an under-traffic state at a chosen rate; two entries, idle and under traffic, the second still resting on an invented rate; message rate as a `binding_params` entry, which would look parameterised while no measurement supports interpolating across rates. Hands to 9.10: if a timeline needs a chat client under message traffic, the campaign results hold that phase and its rate is stated design. No value changed by this entry.

## D12 — the run design: the browser, the page set, the homeserver and the traffic rate (2026-09-20)

By 인지오's decision, the run design the method left open. **The browser** is Google Chrome, launched as 9.5's campaign launches it, not the preinstalled unconfined Chromium: `web-browser` carries Chrome's process tree minus its renderers (9.5 D14) and D2's entries carry the renderers, so the two archetypes are two halves of one application, which every browsing and office timeline composes as a single browser — one `web-browser` task and N renderer tasks, all named `chrome`. Measuring the halves on different programs would put a montage inside one application, the defect D1 removes, merely relocated. Reusing 9.5's launch path keeps a configuration already proven on this image, whose user-namespace restriction aborts an unprofiled Chromium-based binary unless an AppArmor profile names it, and avoids `--no-sandbox`, which would change the process tree being measured. **The page** is one stated local page, identical at every origin, served over local HTTP and never from `/tmp`, a snap-confined browser's private `/tmp` being the recorded cause of the Phase 2 run's tabs never loading; its timer runs faster than the throttling cap. Grounds: page content drives a renderer's wakes and no source states what a background tab contains, so a chosen "representative" page would drive the values exactly as D11's invented message rate would have. Above the cap that dissolves for the hidden entry, whose wake rate is then Chromium's documented budget — one per second, one per minute past the grace, 3 ms per wake, 1 % of CPU (S2-06) — rather than our content. Stated asymmetry rather than papered over: nothing throttles the visible entry, so its values do depend on the stated page and its scope says so; live web content was not taken, being both invented as a population and unreproducible across repeats. **The homeserver** is Synapse, on the harness's own CPUs and pinned away from the measured CPU with the driver and perf — 9.5 recorded the runner's own agent processes already sharing the measured CPU uncontrolled, about 1 100 schedule rows against the application's 18 865 over a 60 s phase, and a server we control should not add to that. Dendrite was excluded because its repository is archived upstream, last pushed 2024-11-25, and a campaign that must be re-runnable should not pin an abandoned server. Synapse over Conduit because the archetype reads the idle phase (D11), where the server only holds a `/sync` long poll open, behaviour the Matrix specification fixes rather than the implementation, so reproducibility decides and Synapse is the maintained reference implementation packaged for Ubuntu; Conduit is the fallback if Synapse's startup proves heavy on the runner, a dry-run finding and not a method decision. **The traffic rate** is stated as an instrument setting rather than a claim about users: no source states a real client's message rate, so it is chosen high enough that the traffic phase separates measurably from idle, its purpose being to quantify the gap the idle entry's stated limitation otherwise only declares. Left open on purpose and set from the long-phase probe rather than chosen: each subject's phase length and N, which trade directly against each other for sample count, and whether throttled wakes coincide across renderer processes, which the probe's 10 s slice profile shows as clustering. Written into `campaign/method.md` §2 with the amendment entries in its §10. No value changed by this entry.

## D13 — the tooling design, and the `--no-sandbox` clause of D12 corrected (2026-09-20)

By 인지오's decision, the tooling the method named and three corrections to committed text, settled before any of it was written.

**The correction first.** D12 and `campaign/method.md` §2 both stated that reusing 9.5's launch path "avoids `--no-sandbox`, which would change the process tree being measured". That is wrong about the code it names: `dataset/tools/meas/probe/appdefs.sh` launches `google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data`, and the `webrtc` and `code` subjects pass the flag too. `web-browser` was therefore measured with the sandbox disabled, and these entries are measured the same way, which is what the same-program claim requires. The flag is kept and the ground for reusing the path is the same-program claim and the proven configuration alone. Each entry's scope states the flag rather than saying the sandbox was absent: 9.5's pooled `results/pool-webrtc.json` carries a `sandbox_ipc_thr` component with the flag passed, so the sandbox machinery is in the measured tree either way. D12 is not edited; this entry carries the correction.

**The tooling.** A tool tree `dataset/tools/meas/desktop/` (`run.sh`, `analyze.py`, `pool.py`), workflow `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, loop family `desktop` in `dataset/tools/meas/loop/common.py`, a `desktop` arm in `loop/pool_runs.py`'s `validity`, and tests in `dataset/tools/tests/test_meas_desktop.py`. The two Chrome subjects are new `chrome-hidden` and `chrome-visible` arms of `probe/appdefs.sh`, so that `web-browser` and these entries share one launch definition; a test asserts the flag portion is identical across the three Chrome arms, the existing `chrome` arm being left untouched. Element and the Steam client are defined in `desktop/run.sh`, neither having a twin in another archetype. `campaign/run.sh` is not modified and its `phase()` is copied rather than extracted, 9.5 still adding repeats through that file. `desktop/analyze.py` imports `load_rows`, `load_wakeups`, `merge_resumes`, `pid_roles`, `per_thread` and `dist` from `meas.campaign.analyze` and does its own phase discovery, `analyze_run`'s phase loop being fixed to 9.5's names; the renderer-only view is the inverse of the `exclude_roles=("renderer",)` filter that pools `web-browser`, so the same code computes both halves of the browser. `desktop/pool.py` follows `background/pool.py`'s structure and imports the coverage-cut helpers from `meas.campaign.pool`.

**The run design** is in `campaign/method.md` §2 and §3 with its §10 amendments: N loopback origins; a control tab plus N background tabs for the hidden state and N windows for the visible one; a trivial per-wake callback, so both renderer entries are floors; a second visible steady phase with the timer removed; a logged-in Element against a Synapse started outside systemd; a window manager in the Steam job alone; a settle with recorded edges whose Chrome half comes from the probe. The probe becomes a `probe` mode of the desktop family rather than a run of the `long-probe` family, keeping this slice's parameters out of a trigger file 9.5 launches from; it is still never a repeat. The trigger carries `mode`, `attempt`, `cpu_model`, `apps` and `repeats` only, every value the design fixes being a constant in `run.sh`, since a pool whose repeats ran at different N or different phase lengths is not a pool.

**Hands to 9.9:** `meas-gui.yml` is not retired by this slice. `system-daemon` also carries values from `meas-ci:gui:2`, and the workflow goes when the last entry citing that run goes.

**Hands to 9.13:** the two renderer entries carry a floor, not a ceiling — their `run` tables are the cost of a wake whose page does nothing, and a renderer showing live content does more. The visible entry's scope records whether it read the no-timer phase or the timer phase, and in the latter case that its `wakes_per_s` is our timer period and not an observation.

Not taken: extracting `phase()` or the Chrome flags into shared files (edits under an in-flight campaign); a knob per design value in the trigger; retiring `meas-gui.yml` here. No value changed by this entry.

## D14 — what the dry run established, and the four decisions it forced (2026-09-20)

The tooling of D13 run for the first time, `mode: dry`, thirteen attempts. A dry run is not pooled and is not a repeat, so it sets `cpu_model` to `""` and the machine gate opens on any model. No value of any archetype comes from it.

**Three of the method's open questions are answered.** *Synapse is not too heavy for the runner* (§2 subject 4): it installs from the matrix.org repository, starts outside systemd under the pin, answers `/health` with 200 and registers an account, so the Conduit fallback is not needed. *The Steam client does hold a stable state logged out* (D6): the client comes up with nine `steamwebhelper` processes, its window reads "Sign in to Steam", its helper's command line carries `-steamid=0`, and it holds that state across both phases — so D6's fallback, retiring the binding to 9.10, is not invoked. *D5's open question now has an observation rather than an inference*: minimising the client moved CPU share 2.647× (0.03807 → 0.01438) and the helper's wake rate 1.247× (315.0 → 252.5), both above method §6's 10 % resolution. The client's build id is in the helper's command line, `-buildid=1788652215`, the same build the stage-2 search read.

**Four decisions by 인지오, each forced by what the run showed.**

*The page drives its own steps.* `run.sh` retyped a URL into each window through the omnibox to remove the timer between the visible subject's two phases. Without a window manager `xdotool windowactivate` does not move X input focus, so all three navigations landed on the focused window: the run recorded three navigations and two renderers kept ticking at 10.6 wakes/s through the phase that was meant to have none. The page now walks a plan from its own load and the run waits until every window reports the step it wants, read from the window title, which `xdotool getwindowname` gives without focus. Nothing is typed at a renderer subject. The probe's period sweep becomes three probe pushes with `TIMER_MS` edited between them, which is what D13 says changing a design value looks like.

*One renderer's components, the N renderers pooled as its samples.* `per_thread` keys components by thread comm, and every renderer's main thread is named `chrome`, its hang watcher `HangWatcher`: over the whole tree it returned the sum across the N renderers a job measures, while the archetype describes one. The run read `HangWatcher` at 0.67 wakes/s where one renderer does 0.11. Components are computed per renderer process, exactly as `web-browser` has them computed over its tree, and pooled as samples — the rate their mean, with the per-renderer values kept for the spread the stability rule reads, and the gap and run tables `dist` over every renderer's samples together.

*The control tab carries the timer.* It cannot be separated any other way: a renderer's command line does not name the site it is locked to, and the components' coverage cut selects comms that every renderer shares. Being the selected tab it stays visible to Blink and is never throttled, so with the timer it wakes at the timer rate while the measured renderers fall to the budget — observed at 10.177 wakes/s against 0.178, a ratio of 57, where without the timer it was 6.5.

*The spare renderer is not created.* Chromium keeps one warm for the next navigation; it hosts no page, carries `--type=renderer` like any other, and the run measured it at 0.356 wakes/s beside three page renderers at ~10.6. It cannot be separated afterwards — `Compositor` marks visibility rather than page-hosting, and no renderer composites in the hidden subject — so the launch passes `--disable-features=SpareRendererForSitePerProcess`, one flag beyond 9.5's. That flag changes only the renderer population, which is the half `web-browser` excludes (9.5 D14) and these entries own.

**Three corrections to the analysis, each of which would have carried a plausible wrong number.** A renderer that died partway through a phase had its wakes divided by the whole span, so its rate was understated and it dragged the pooled mean down; presence is now taken from the snapshots at both ends. Chrome's own renderers — extension processes and the top-chrome WebUI — carry `--type=renderer` and were pooled into a page-renderer archetype; they are read from the whole command lines, `--extension-process` sitting about 129 characters in where the snapshot keeps 120. And `select_components` carries a component only where its gap and run means exist in every repeat (9.5 D43), testing that on raw sample lists the analysis was not passing, so the coverage cut selected nothing at all. Together with the spare renderer these moved the visible entry's per-renderer rate from 6.66 to 10.63 wakes/s.

**The probe's slice profile is computed by `desktop/analyze.py`.** Method §3 named `campaign/slices.py`, which reaches its data through `campaign.analyze_run`, whose phase loop is fixed to 9.5's names and raises `KeyError` on every phase this slice records.

**Conditions of the observation, all stated in the entries' scope.** Element runs with `--disable-gpu-sandbox`, `--disable-software-rasterizer` and `--disable-dev-shm-usage` beside the flags `meas-gui.yml` used, Electron 1.12.28 treating an unusable GPU process as fatal where Chrome tolerates it; its homeserver comes from `config.json` in Element's user-data directory, the environment variable alone not taking; and it stores its session with Electron's basic backend, a hosted runner having no keyring. The Steam job accepts `steam-installer`'s own installation dialog, which is the package's prompt and not an account action — no account is used, and none may be (D6).

**Hands to 9.13:** the two renderer entries carry a per-renderer value, not a sum over the N a job measures, and their scope states the renderer population they were pooled from.

**Hands to 9.16:** a `dry` repeat of the hidden subject can never enter a pool — its 75 s grace does not clear the five-minute default and the throttling gate rejects it — so that entry's pooling path is exercised only in `probe` or `full` mode.

**Correction, later the same day: the numbers above for the Steam client are withdrawn.** `snapshot.py` roots the
measured tree on any process whose command line or comm matches the subject's pattern and then walks its
descendants, and two patterns matched this script's own command line, which carries the subject name as an
argument: `steam` matched `run.sh steam 1 dry`, and `element-desktop|element` matched `run.sh element 1 dry`. The
tree was therefore rooted at the job itself and took in Xvfb, the window manager and — for the chat client — the
homeserver, which the method pins away precisely so that it is not measured. The chat client's largest component
read `python`, at 14.62 wakes/s idle and 110.77 under traffic: that is Synapse.

So the Steam figures — 315.0 against 252.5 wakes/s and 0.03807 against 0.01438 CPU share — are the application
and the harness together, and D5's comparison must be read again from a clean tree before anything rests on it.
The direction of the effect is not in doubt; the magnitudes are withdrawn. The patterns are now `debian-installation`
and `element-desktop`, neither of which appears in anything of ours, and every job checks its own tree before
measuring: a harness process inside it stops the job at `gate=harness-in-tree` rather than producing a number.
`chrome-hidden` and `chrome-visible` were never affected — their pattern is `chrome-data` and the argument is
`chrome-hidden`, so the roots were Chrome's processes alone, and their values above stand.

**Re-measured on clean trees, both jobs reporting no harness process in the tree.** The chat client was the more
contaminated: its wake rate halved and its CPU share fell by about two thirds, from 27.154 to 13.466 wakes/s idle
and 217.035 to 109.707 under traffic, CPU share 0.0034 to 0.00106 and 0.03442 to 0.00979. D11's comparison, which
feeds no archetype, reads idle against traffic at 8.1× in the rate and 9.2× in the share.

The Steam client's rates barely moved — its own tree is large, 29 components at about 300 wakes/s, so Xvfb and
the window manager were a small share of its wakes — but its CPU share was inflated, and the correction makes
D5's effect **larger** rather than smaller: minimising the client moves CPU share 3.338× (0.02884 → 0.00864)
against 1.277× in the wake rate (317.9 → 249.0), where the contaminated reading gave 2.647×. Both are above
method §6's 10 % resolution. D5's inference — that Steam controls its helper's throttling itself — now rests on
an observation of a clean tree.

No value changed by this entry.

## D15 — the long-phase probe, the gate it exposed, and the phase lengths it set (2026-09-20)

The probe of method §3 run for the first time, `mode: probe`, one job per subject on a single long steady
phase of 1800 s. Four subjects landed on the AMD EPYC 7763 in eight draws — `chrome-visible` first, then
`chrome-hidden` and `steam`, then `element` on its third — each reporting `gate=open` and no harness process
in its tree. A probe is never a repeat and no archetype value comes from it.

**A defect that would have emptied the hidden entry's pool.** `desktop/pool.py`'s `throttling_check` decided
whether intensive throttling engaged by taking the highest rate in `per_pid_wakes_per_s`, which
`desktop/analyze.py` computes before the control tab is dropped. The control tab carries the same timer and,
being the selected tab, stays visible to Blink and is never throttled — that is what it is for (§2 subject 1),
and the run identifies it at 55× the next renderer. The gate therefore tested the one renderer that cannot
pass it: on this probe it read the control's 10.193 wakes/s against a 0.5 limit while the worst measured
renderer was 0.184. Every repeat of a five-repeat batch would have gone into `not_throttled` and the entry
would have carried nothing, with each job reporting `gate=open` and each artifact the right shape. The check
now excludes the control tab and returns `(True, 0.184)` on this artifact; a measured renderer that never
throttled is still caught, and a phase holding only a control tab is rejected rather than passed.

This also corrects D14. A `dry` repeat of the hidden subject was rejected by this gate at any grace, not
because its 75 s grace left throttling unengaged. The probe reads 0.1817 wakes/s per renderer with the real
330 s grace against 0.178 in the dry run, and the page's own thread at 0.040 wakes/s where the unthrottled
control sits at 10.193 — throttling was engaged in both.

**What each subject showed.** The chat client is flat from its first slice, its first minute the lowest of the
thirty; its launch work is over before the phase begins. The visible subject reproduces the page's 100 ms
period exactly, 10.032 wakes/s on the thread the callback runs on, and falls to 0.130 per renderer with the
timer removed. The hidden subject sits at 0.1817 per renderer, of which 0.100 is `HangWatcher` — Chromium's
hang-detection thread, which polls whatever the page does — and 0.040 the page's own thread. The Steam client
holds 311.8 wakes/s over the phase with `steamwebhelper` at 72.9 and `steam` at 71.0, against 317.9 in the dry
run.

**Two subjects were still settling inside what the method treated as steady.** The Steam client steps from
about 325 to about 298 wakes/s at 900 s; dropping that step takes the spread of its 120 s windows from 4.8 %
to 0.2 %. The hidden subject settles for about 300 s past its 330 s grace; dropping it takes the spread of its
500 s windows from 11.3 % to 3.7 %.

**By 인지오's decision**, the steady phase is 600 s for every subject, N stays at 12, the launch-settle is 20 s
for the two renderer subjects and the chat client and 900 s for the Steam client, and the hidden subject's
grace-settle is 630 s — 330 s of Chromium's documented default and 300 s of design read from the probe.
`launch_settle_for()` and `steady_for()` in `desktop/run.sh` carry them, so a `full` job no longer stops at
`gate=no-phase-lengths`. Method §10 carries the amendment, which §9 requires before the first batch.

**The throttled renderers do not wake independently.** Counting the bins in which every one of the twelve woke
gives 243 bins of 1 s and 32 bins of 10 ms, against none at either width in draws that keep each renderer's own
wake count and place its wakes uniformly over the phase. §9's second item is read and answered. What it implies
for D14's decision to pool the N renderers of a job as N samples of one renderer is open.

**Open after this entry:** whether the visible entry reads the no-timer phase — the probe answers the yield
half, the no-timer phase holding a 3.1 % spread at 600 s against the 5 % tolerance — and what the alignment
above does to the pooling of N renderers as N samples.

No value changed by this entry.

## D16 — the visible entry reads the no-timer phase (2026-09-20)

By 인지오's decision, closing the third of method §9's items open before the first batch.

The visible entry takes the steady phase the page runs with its timer removed. §9 set the condition — that
phase if the probe shows it yields enough wakes for the quantile tables and for the half-width to converge,
otherwise the timer phase with `wakes_per_s` labelled design — and the probe meets it: at 600 s the no-timer
phase holds a 3.1 % spread of non-overlapping windows, a 3.9 % half-width across five repeats, against the 5 %
tolerance. The entry therefore carries an observation, 0.130 wakes/s per renderer, where the alternative was
our own timer period. The value is multiplied by every renderer task in every timeline, which is the ground
for preferring the observed one. `CARRIED` in `desktop/pool.py` already lists `steady-notimer` first and `LIST`
takes the first phase, so no tooling changes.

**What it does to the effect the slice reports.** Method §6 item 2 grounds the tolerance on the smallest effect
the slice reports and names the hidden-against-visible comparison as about sixtyfold in wake rate. That holds
for the two *states* with a timer running, and the probe measures it at 56× — 10.179 wakes/s per visible
renderer against 0.182 per hidden one, the same separation the control tab shows at 55.26 inside the hidden
job. But the two *entries* the slice carries are now the hidden renderer against a visible renderer with no
timer at all, and those differ by 39 %, 0.182 against 0.130. It stays above the 10 % below which §6 reports a
difference as not resolved rather than as an effect, so the tolerance is unchanged; §10 carries the corrected
statement.

**Hands to 9.13:** both renderer entries are majority `HangWatcher` — Chromium's hang-detection thread, which
polls whatever the page does — at 0.100 wakes/s of the hidden entry's 0.182 and of the visible entry's 0.130.
The page's own thread is 0.040 hidden and 0.020 visible. An entry's scope states this: what separates the two
is a fraction of each one's wakes, and most of what either carries is the browser's own housekeeping.

No value changed by this entry.

## D17 — the first batch read against the rule; the list per component, and run means excepted (2026-09-21)

All twenty jobs of the first batch landed on the AMD EPYC 7763 — five repeats per subject, every one valid.

**The rule was being tested on the wrong list.** `desktop/pool.py`'s criterion tested three numbers per phase: the
per-renderer wake rate and the unweighted means of the components' gap and run means. Method §6 item 1 lists every
value per component and the residual's, and `campaign/pool.py` tests 9.5's entries that way. The average weighted a
thread waking a handful of times a phase like one waking every ten seconds, let a failing component sit behind
stable ones, and never tested the residual: it reported the chat client done where 7 of its 18 per-component values
failed. The criterion now tests each carried component and the residual (`c7b8a72`).

**Run times follow the runner.** Within a repeat every thread's run mean moves together — the Steam client's
`steam`, `IPC:CSteamEngin` and `CJobMgr` threads all run about 30 % slower in repeats 1, 4 and 5 than in 2 and 3 —
while the same threads' wake rates hold within about 1 %. That is a per-runner speed on one CPU model, which added
repeats average over rather than remove.

**By 인지오's decision**, the rule's exception (measurement-campaign workflow; 9.6 D29) applies to every carried run
mean of the hidden renderer, the visible renderer and the chat client, the residual's included: carried over at
least five repeats with its half-width and range in place of the tolerance. The Steam client is not excepted —
its shown-against-minimised comparison (D5) is in part a CPU-share ratio built from run times, and the exception
applies only to a value no reported effect rests on — so its run means keep adding repeats. Each excepted value's
half-width, range, repeat count, what its spread follows and the share of the job's time it holds go into the
entry's scope at the fold-in.

**What still fails at five repeats**, with the count its present spread would need: the chat client's
`ThreadPoolForeg`, `Chrome_ChildIOT` and `ThreadPoolServi` gap means (9, 7, 7); the visible renderer's main thread
wake rate and gap mean (10, 11), its `Chrome_ChildIOT` (over 200) and residual (55); the hidden renderer's main
thread gap mean (6), its `Chrome_ChildIOT`, `Compositor` and `PerfettoTrace` (over 200 each) and residual (84); the
Steam client's run means and `ThreadPoolForeg`. The components past 200 wake about six times a phase and are in the
carried set only because the 0.95 coverage cut needs three equally small threads to reach it — a spread the
analysis makes (campaign workflow, step 6), open.

No value changed by this entry.

## D18 — D5 stated on the wake rate; the Steam client's run means excepted (2026-09-21)

D17 left the Steam client's run means under the tolerance, because D5's comparison was in part a CPU-share ratio
built from run times. Whether the per-runner speed cancels inside that ratio — both phases of a repeat running on
one runner — was checked against the five repeats, and it does not: the per-repeat CPU-share ratio of shown to
minimised is 1.382, 1.326, 1.274, 1.075, 1.493, a 12 % spread, about the spread of the shown share itself (11 %).
The wake-rate ratio is 1.226, 1.224, 1.217, 1.230, 1.241, a 0.7 % spread.

**By 인지오's decision**, D5's comparison is stated on the wake-rate ratio — throttling is a change in how often a
thread wakes, so the wake rate is the direct observable of D5's claim, and it is the precise one. The CPU-share
ratio is reported with its spread and no effect rests on it. With nothing reported resting on the Steam client's
run times, its run means join the rule's exception on the terms of D17. This also supersedes D14's 3.338× CPU-share
figure as D5's magnitude: that came from 45 s phases taken soon after launch, and the settled repeats read 1.075
to 1.493.

**Still failing at five repeats:** `steamwebhelper`'s gap mean (needs about 59) and `ThreadPoolForeg`'s wake rate
and gap mean (12, 31). Open.

No value changed by this entry.

## D19 — the renderer residual describes one renderer (2026-09-21)

For the two renderer entries the selected components are one renderer's with the renderers pooled as its samples
(D14), but the residual was built by `select_components`, which merges the residual comms' wake times over
everything it is given — every measured renderer at once. Its rate came out N times a renderer's and its gaps
interleaved N processes: on the hidden subject's repeat 2, 0.16 wakes/s and a 5.6 s gap mean for a residual whose
thread wakes 0.01 times a second with a 105 s gap in each renderer. `desktop/pool.py` now rebuilds the renderer
residual per renderer — the residual comms merged within each renderer, gaps within each renderer, the renderers
pooled as samples — and reports it sporadic, not carried, where it wakes fewer than twice in a repeat (D43). The
per-renderer residual reads 0.005–0.014 wakes/s.

It still does not hold at eleven repeats (hidden: wake rate and gap mean need about 161 and 143; visible: 125 and
72), and neither do the visible renderer's `Chrome_ChildIOT` and `ThreadPoolForeg`: these quiet threads' wake
counts per phase vary between runs — the hidden renderer's `Compositor` reads 0 to 48 gaps across the eleven — a
spread of the application between sessions, which is 9.5 D57's case. They carry 7 % of the hidden renderer's wakes
and 14 % of the visible renderer's. Open.

No value changed by this entry.

## D20 — where the Chrome quiet threads' spread lies, measured; the decision open (2026-09-21)

D19 left the renderer entries failing only on quiet threads: the hidden renderer's residual (`Chrome_ChildIOT`,
`MemoryInfra`), the visible renderer's `Chrome_ChildIOT`, `ThreadPoolForeg` and residual — 7 % of the hidden
renderer's wakes and 14 % of the visible one's. 9.5 D57 carries a component whose rate varies between sessions
with its half-widths, and places the spread by sliding a window along one long run. The same test on the
2026-09-20 probes (`desktop/within_run.py`, 600 s windows every 60 s, per renderer), the hidden probe's first 300 s
dropped because D15 found it still settling there:

| thread group | within one run | across the eleven repeats |
|---|---|---|
| visible `Chrome_ChildIOT` | ±18.6 % | ±105.8 % |
| visible residual | ±28.9 % | ±45.3 % |
| hidden residual | ±34.0 % | ±46.2 % |
| visible `ThreadPoolForeg` | barely present in the probe (mean 0.0001/s) | 0.0030–0.0070/s |

`Chrome_ChildIOT` in the visible renderer is D57's case: its rate barely moves within a run and moves a lot
between runs. The residuals are not cleanly so — about two thirds of their spread is already present within one
run, since they wake about six times per renderer per 600 s phase, so a 600 s phase is itself too short to average
them. Lengthening the phase would change the campaign and supersede all eleven repeats of both subjects.

**Open for 인지오:** carry the renderer entries' quiet threads with their half-widths — D57 as written for
`Chrome_ChildIOT`, extended to the residuals and `ThreadPoolForeg` with both spreads and the few-wakes-per-phase
limitation stated in the scope — or supersede both renderer subjects and rerun them on a longer phase.

No value changed by this entry.

## D21 — the renderer quiet threads carried with their half-widths; both renderer entries hold (2026-09-21)

By 인지오's decision on D20's open question: the quiet threads are carried with their half-widths over the eleven
repeats obtained, not rerun on a longer phase — which would change the campaign and supersede all twenty-two
renderer repeats for 7 % and 14 % of the two entries' wakes. 9.5 D57 applies as written to the visible renderer's
`Chrome_ChildIOT` (±18.6 % within a run, ±105.8 % across repeats). It is extended to the visible renderer's
`ThreadPoolForeg` and to both renderer residuals, whose spread is in part within a run: each entry's scope states
both spreads from D20, the three values of each such component carried together, and that these threads wake about
six times per renderer per 600 s phase. Tooling: `SESSION_SPREAD` in `desktop/pool.py`.

With D17's run-mean exception and this, **both renderer entries hold at eleven repeats** — `HangWatcher` and the
main thread pass on their own, and every other value is carried with its half-width under a stated exception.

No value changed by this entry.

## D22 — the Steam client's two failing gap means, placed; the decision open (2026-09-21)

The Steam client at twelve repeats, every one valid: the rule holds for every value but two gap means —
`steamwebhelper` (±10.2 %, needs about 46 repeats) and `ThreadPoolForeg` (±9.0 %, about 35). Both components' wake
rates pass. Placed by 9.5 D57's three tests (`desktop/within_run.py --tree`, the probe's shown phase past its 900 s
settle, 600 s windows every 60 s):

| component | gap mean within one run | across the twelve repeats | share of wakes | threads per repeat |
|---|---|---|---|---|
| `steamwebhelper` | ±0.1 % | ±21.0 % (28.5–42.2 ms) | 23.6 % | 4, or 6 in two repeats |
| `ThreadPoolForeg` | ±1.7 % | ±19.6 % (415.9–616.1 ms) | 2.1 % | 5 to 8 |

(a) It is not the analysis: `steamwebhelper`'s repeats 4 and 6 hold the same four threads and the same wake rate
(70.8, 71.1 /s) as the repeats reading 29 ms, and read 42.2 and 41.2 ms — the same threads spread their wakes
differently from one launch to the next. (b) It is not the phase's placement: within one run each gap mean moves
by ±0.1 % and ±1.7 %. (c) Their weight: `steamwebhelper` carries 23.6 % of the client's wakes, well above 9.5 D57's
6.5 %, though only its gap mean varies — its wake rate holds within ±0.5 % across the twelve.

**Where in the table the spread sits.** The rule tests a carried table by its per-repeat mean (campaign workflow,
from kalibera-ismm13 §9.3). The tables themselves hold:

| component | gap p50 | gap p90 | gap p99 | gap mean |
|---|---|---|---|---|
| `steamwebhelper` | 16.2 ms in all twelve | 16.2 ms in all twelve | 588.4–592.9 ms | 28.5–42.2 ms |
| `ThreadPoolForeg` | 1.1–22.8 ms | 576.1–579.3 ms | 583.0–599.6 ms | 415.9–616.1 ms |

`steamwebhelper`'s median is a 16.2 ms frame tick, identical in every repeat through its 99th percentile; its mean
moves on a handful of gaps past the 99th percentile out of about 42 000 a repeat (the high means fall in repeats
4, 6, 10, 11). For a heavy-tailed component the per-repeat mean summarises its rarest events rather than its table.

**Open for 인지오 (campaign workflow step 6):** carry both gap means with their half-widths under 9.5 D57, the
quantile stability stated in the scope; or add the repeats the rule projects (about 46, at 42 minutes each); or test
these tables at their quantiles rather than their means, which would change how the shared rule reads a table and
reaches beyond this slice.

No value changed by this entry.

## D23 — the Steam client's two components carried between sessions; every entry holds (2026-09-22)

By 인지오's decision on D22: 9.5 D57's exception applies as written to the Steam client's `steamwebhelper` and
`ThreadPoolForeg` — a component whose rate varies between sessions carried with its half-widths over the repeats
obtained, its three values together. D22 holds the evidence: within one run their gap means move ±0.1 % and ±1.7 %,
across the twelve repeats ±21.0 % and ±19.6 %; `steamwebhelper`'s wake rate holds within ±0.5 % and its gap table
is identical through its 99th percentile, the mean moved by a handful of gaps past it. Each entry's scope states
this, and that `steamwebhelper` carries 23.6 % of the client's wakes, well above 9.5 D57's 6.5 %. Tooling:
`SESSION_SPREAD` in `desktop/pool.py`.

**Every entry holds the rule:** the chat client at 17 repeats, the two renderers at 11, the Steam client at 12, all
on the AMD EPYC 7763 under campaign `meas-ci:desktop:2026-09-20`, no repeat excluded or superseded.

No value changed by this entry.

## D24 — every landing pooled; the hidden renderer's `Chrome_ChildIOT` carried between sessions (2026-09-22)

**Four landings were not pooled.** The retry driver relaunched the hidden renderer's repeat 10 in runs #33, #34, #36
and #37 and the chat client's repeat 17 in #49 and #50, and every launch landed on the AMD EPYC 7763 with the gate
open and passed the validity step. `desktop/pool.py` and `pool_runs.py` keyed repeats by index, so each read the
latest landing and dropped the others without a word, against the campaign workflow's "Every same-machine repeat
obtained is pooled and reported". By 인지오's decision all of them are pooled: an index that landed more than once is
keyed `<index>@<run id>` per landing (`ecd3244`). The hidden renderer pools 14 repeats and the chat client 18.

The chat client holds at 18, every value passing. The hidden renderer's coverage cut moved: `Chrome_ChildIOT`, in the
residual at eleven repeats (D20), is a carried component of its own at fourteen, and its wake rate (±38.1 %) and gap
mean (±25.7 %) fail. D20's test, the hidden probe's steady phase past its first 300 s in 600 s windows every 60 s per
renderer (`desktop/within_run.py`, which reproduces D20's ±34.0 % for the old residual), places the spread:

| hidden `Chrome_ChildIOT` | within one run | across the fourteen repeats | share of wakes |
|---|---|---|---|
| wake rate per renderer | ±17.7 % | ±76.9 % (0–0.010 wakes/s) | 3.8 % |

**By 인지오's decision**, 9.5 D57 applies to it as written, as D21 applied it to the visible renderer's
`Chrome_ChildIOT` (±18.6 % within, ±105.8 % across): its three values carried together with their half-widths over
the fourteen repeats. It wakes about six times per renderer per 600 s phase; the entry's scope states both spreads.
The residual is now `ThreadPoolServi` and `MemoryInfra` (±29.7 % within a run), still carried under D21. Tooling:
`SESSION_SPREAD` in `desktop/pool.py`.

**Every entry holds the rule over every landing:** the chat client at 18 repeats, the hidden renderer at 14, the
visible renderer at 11, the Steam client at 12.

No value changed by this entry.

## D25 — the fold-in: four entries replace `electron-comms`, every binding rebound or retired (2026-09-22)

**The entries.** By 인지오's decision the ids are `renderer-hidden`, `renderer-visible`, `chat-client` and
`game-client`, named for the kind of application as `web-browser`, `mail-client` and `video-call` are. They are
generated by `dataset/tools/meas/desktop/fold_in.py` from the tagged pooled record
(`campaign/results/pooled.json`, `meas-ci:desktop:2026-09-20`) in the form D10 set: per carried component and for
the residual, `wakes_per_s` and the pooled `gap` and `run` quantile tables — `desktop/pool.py` now writes each
selected component's pooled tables (`tables`), built with the `summary` that built 9.5's — tagged
`meas-ci:desktop:2026-09-20`; no `focus_components`, no `stimulus`. The carried phases: `steady` (hidden), `steady-notimer`
(visible, D16), `idle` (chat client, D11), `shown` (Steam client). Each entry's `validation_stats.scope` states the
runner, the program's version (Chrome 152.0.7977.82; Element 1.12.28 against Synapse 1.161.0; Steam build
1788652215), the state and what it is not, the renderer population (12 measured of 16 observed hidden, of 13–14
visible, D14), that both renderer entries are majority `HangWatcher` (0.100 of 0.169 and of 0.141 wakes/s per
renderer, D16), the floor clause and `--no-sandbox` (method §7), every value carried under an exception with its
half-width and range (D17, D18, D21, D23, D24), both spreads of each between-sessions component (D20, D22, D24),
and the comparison measured beside each entry. `electron-comms` is removed; `web-browser`'s two references to it
name the renderer entries. The campaign's release is `meas-ci-desktop-2026-09-20`.

**The renderer tasks: one visible, the rest hidden.** By 인지오's decision, each timeline's renderer task becomes a
`renderer-visible` task of one and a `renderer-hidden` task of N − 1. Grounds: in a window the selected tab is visible
to Blink and every other tab is a background page (method §2 subject 1), throttled past the grace (S2-06); a covered
window's selected tab stays visible on Linux (D4, S2 §4.2), so a window holds one visible renderer. How many windows
a session holds is read from `mozilla-testpilot10`'s logged data — `witl_small/events_small.csv` (the Wayback copy of
2011-07-11 that the 2026-09-13 verification read, R09 C-testpilot-4), event code 26 `NUM_TABS`, `data1` windows and
`data2` tabs, logged at startup, every 15 minutes and at every window or tab open or close: over 180,673 logged
states of 387 users, 82.9 % have exactly one window; per user the mean window count has quartiles 1.04, 1.11, 1.31
and the mean tab count 1.87, 2.67, 4.09; 78.5 % of all open tabs are not their window's selected tab. Stated limits:
Firefox 3.5–4.0 beta in November 2010, so the figures ground the spread of tabs over windows — a use pattern — not a
renderer's behaviour; and under site-per-process a renderer is a site, not a tab (S2-01). Not taken: every renderer
task to `renderer-hidden`, which misstates one renderer per window; every one to `renderer-visible`, which describes a
tab per window.

| source | renderers before | now |
|---|---|---|
| `c1-browsing` (and `c6-fold`, `c6-spoof`, `c7-browsing`) | 12 | 1 visible + 11 hidden |
| `c1-office` (and `c4-office`, `c7-office`) | 8 | 1 + 7 |
| `c3-workday` | 8 | 1 + 7 |
| `c3-evening` | 10 | 1 + 9 |
| `c4.variant.yaml` `injected-renderers` (`c4-compile`) | 6 | 1 + 5 |

**`steamwebhelper` retired.** By 인지오's decision the nine `steamwebhelper` tasks (three in each of `c1-gaming`,
`c4-gaming`, `c7-gaming`) are retired rather than bound to `renderer-visible` as D5 decided. Grounds: `game-client`'s
measured tree holds every `steamwebhelper` process — nine per phase, its `steamwebhelper` component 70.75 wakes/s,
23.6 % of the client's wakes (D22) — so a gaming file carrying the client and three helper tasks counted the helpers
twice. The client's tree is one task under 9.5 D14's merge rule, as VS Code's renderer sits in `code-editor` (D2);
D5 itself stated that the Steam probe's result, if it ran before the fold-in, replaces its inference. `c2-p2a` and
`c3-evening` already carried `steam` without helper tasks. Not taken: separating the helpers from `game-client` as D2
separated Chrome's renderers, which needs a new pool pass and entry. D5's observation of the helper's role remains in
`game-client`'s scope: minimising the client lowers its wake rate 1.225×.

**The other bindings, as decided:** the three `thunderbird` tasks → `mail-client` (D9); the three `discord` tasks
(`c3-evening`'s `overlay`, `c4.variant.yaml`'s `injected-overlay`, hence `c4-gaming`) → `chat-client` (D7), their task
ids unchanged; the six `steam` tasks → `game-client` (D6); the two `zoom` helper tasks retired (D8), with
`c1-meeting`'s header clause that described the helper. `fx-mixed`'s renderers → `renderer-hidden`. The variant files are
regenerated by `derive.py`; no variant op names a removed task.

**Demand.** No file changes demand class and no new file leaves the window: the five files outside it
(`c2-p3a`, `c2-p3b`, `c3-creation`, `c3-evening`, `c3-workday`) were outside it before (research-slice workflow, CI on
the branch; compiled with `--allow-window`). Moves, single-lane: browsing files −0.0047 (0.0272 → 0.0225), office
files +0.0048 (0.043 → 0.0478, `mail-client` for Thunderbird), gaming files +0.0067 (`c1-gaming` 1.024 → 1.0307),
`c2-p2a`/`c2-p2b` +0.0073, `c3-evening` +0.0030, `c3-workday` −0.0053, `c1-meeting` −0.0003, `c4-compile` −0.0004.

**Scope card, swept.** Items 1–5: the two lognormal parameters, their sigmas, their sampling and the unbounded-loop
rule that drew them are retired with the entry (D10). Item 6: `pattern` is the measured form, timer components merged
into one explicit stream at compile time. Item 7: `lifetime: segment-bound`, `binding_params: []`, `scalable: []` —
design, kept. Item 8: `validation_stats` carries the campaign's run, stats and scope; the OQ-3 note and the
"renderer-children count" are gone, the split having been decided by D1–D4. Item 9: `category_source: meas`, a
behaviour class observed in our measurements; the ananicy `Chat`, `Launcher` and `Doc-View` types stay treatment
profiles (D9). Item 10: `modeling_notes` rewritten — the Element-derived averages, the OQ-3 result, the "21-22
processes" figure and the tab-count sentence are removed; the renderer entries state the site-per-process unit
(S2-01) and leave counts to 9.10. Items 15–16: the entries state their scope as 9.5 D10 does — observations of that
software on that machine; the `meas-ci` registry note and `docs/references.md` role line keep their wording, which
9.5 D10 hands to 9.15 for one wording across slices; `references.md`'s "reserved" status is already corrected.
Item 17: the header's sentence on measured per-application archetypes now describes these entries too.

**Hands to 9.10:** the per-file renderer counts, now N − 1 hidden plus one visible, and any file depicting several
windows; the renderer of the page the user is using, which `web-browser` excludes (9.5 D14) and neither renderer entry
describes (D10) — in the browsing files, where the browser holds focus, the one visible renderer stands for it; the
`mozilla-testpilot10` registry lines for the window share above, and their K4 verdicts; the task ids `overlay` and
`injected-overlay`, which name a withdrawn role (D7); whether a gaming timeline's Steam client is behind a game, which
`game-client` does not describe (D6); a chat client under message traffic (the campaign results hold the phase, D11).
**Hands to 9.14:** the demand moves above. **Hands to 9.15:** the docs naming `electron-comms`, the renderer periods
and "one per tab group" (scope card, Out of 9.8). **Hands to 9.16:** the reproduction of the pooled set from the
release at the tooling commit.

Commit: this entry.

## D26 — one renderer's rates and merged gaps; the quiet threads carried (2026-09-24)

By 인지오's decision (9.5 D71: gaps over a component's merged wake times, wrapped round the span observed; tables that keep their mean; rates from exact counts). For the renderer entries a thread's gaps are merged within each renderer and the renderers measured laid end to end, one in which the thread never woke adding its time; its wake rate is the mean over every renderer measured, a renderer without it counting zero, from exact counts — where the per-renderer rates had been rounded to 0.01 wakes/s before averaging and averaged over only the renderers in which the thread woke. The residual of one renderer (D19) is built the same way.

By 인지오's decision, for a renderer entry 9.5 D43 reads over the renderers measured: a thread is carried if it wakes at least twice across them in every repeat; coverage (9.5 D16) is counted per renderer. With the rates exact:

| entry | carried components, before → after | into the residual |
|---|---|---|
| `renderer-hidden` | `HangWatcher`, `chrome`, `Chrome_ChildIOT` → and `Compositor`, `PerfettoTrace`, `ThreadPoolServi` (sporadic, not carried, before) | — |
| `renderer-visible` | `HangWatcher`, `chrome`, `Chrome_ChildIOT`, `ThreadPoolForeg` → `HangWatcher`, `chrome`, `Chrome_ChildIOT`, `PerfettoTrace` | `ThreadPoolForeg` (0.0014 wakes/s per renderer, not 0.0043) |

The four threads newly carried are carried with their three values together under 9.5 D57, by 인지오's decision, as `Chrome_ChildIOT` is (D21, D24). Placed by the long-phase probes (`desktop/within_run.py`, 600 s windows every 60 s per renderer, the hidden probe from 300 s as in D24): hidden `Compositor`, `PerfettoTrace` and `ThreadPoolServi`, which wake together, ±10.8 % within one run against ±63.6 % across the fourteen repeats, 3.9 wakes per renderer per phase, each 3.9 % of a renderer's wakes; visible `PerfettoTrace` ±4.0 % within against ±63.4 % across, 3.2 wakes per phase, 3.8 %.

`Chrome_ChildIOT`'s values on the exact rates: hidden 0.0071 wakes/s ±20.9 % (was 0.0065 ±38.1 %), visible 0.0060 ±26.4 % (was 0.0047 ±62.0 %); the "0–0.01 wakes/s" ranges the scopes stated were the rounding's. The residuals changed their comms — hidden `MemoryInfra` alone, visible `MemoryInfra`, `Compositor`, `ThreadPoolForeg`, `ThreadPoolServi` — and D20's and D24's within-run figures described the residuals as they were. Re-read on the probes: hidden ±134.2 % within against ±51.6 % across, visible ±181.3 % within against ±23.5 % across (its comms barely wake in the probe, 0.0009 against 0.0068 wakes/s in the campaign). Neither places the residual's spread between sessions as 9.5 D57 requires; the residuals stay carried under D21 and D24 with these figures stated, and whether they should is open, for 인지오.

Both renderer entries hold: hidden 21 values, 6 within the tolerance, the widest `ThreadPoolServi` run mean ±4.82 %; visible 15 values, 4 within, the widest `chrome` wake rate ±3.76 %. `chat-client` and `game-client` keep their components and repeats; the rule now reads their gap means over the carried gaps (`per_thread` given the phase's start), where it had read gaps within each thread beside a table built otherwise. `chat-client` holds 18 of 18, the widest its residual run mean ±4.32 %. `game-client` holds 27 of 33: `steamwebhelper`'s gap mean ±10.2 % → ±0.18 % and `ThreadPoolForeg`'s ±9.0 % → ±4.15 % are within the tolerance, their wake rates having passed all along, so of D23's two components only `steamwebhelper`'s run mean stays carried, under D18.

Tooling: `desktop/analyze.py` (`renderer_components` over every renderer measured, the phase's `t0` and `measured_renderer_pids` recorded); `desktop/pool.py` (exact per-renderer counts for coverage, the count across renderers for D43, the residual wrapped round every renderer, `SESSION_SPREAD`); `desktop/fold_in.py` (the table form, the within-run figures, the wakes per phase computed). Tests: `test_a_renderer_entry_counts_its_coverage_per_renderer`, `test_a_renderer_thread_that_wakes_twice_across_the_renderers_is_carried`, and four whose expectations had been the rounded rates.

Values changed: every table of the four entries (form; the gaps' values); the renderer entries' components and their values. **Hands to 9.14:** the demand moves (9.5 D71).

Commit: this entry.
