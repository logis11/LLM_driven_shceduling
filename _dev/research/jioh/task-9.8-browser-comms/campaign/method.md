# Task 9.8 — measurement campaign method (draft, 2026-09-20)

The observation behind the four entries that replace `electron-comms` — the idle hidden renderer, the idle visible renderer, the Electron chat client and the Steam desktop client (changelog D4, D6, D7, D10, D11) — run on GitHub-hosted runners (phase decision 5) under `../../measurement-campaign-workflow.md`, pinned to one CPU (9.5 follow-ups decision 3). Written before any measurement; amended only by a dated entry in §10.

Tooling is not yet written. This method names what it needs: a tool tree `dataset/tools/meas/desktop/` (`run.sh`, `analyze.py`, `pool.py`), workflow `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, and a loop family `desktop` in `dataset/tools/meas/loop/common.py` with the four subjects of §2 as its apps. `meas-gui.yml` — the unpinned 0.2 s `/proc` sampler under forkstat that produced `meas-ci:gui:2`, which the measurement audit found unable to give per-wake distributions — retires with `electron-comms`, as 9.7 retired `meas-cli.yml`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat (campaign workflow).
- **Tag.** `meas-ci:desktop:<YYYY-MM-DD>`, the launch date of the first batch (9.5 D27); each repeat's run id in the pooled record and in each archetype's `validation_stats.run`.
- **Repeat.** One job per subject per repeat index, that subject's phases in the order of §3. The work is identical in every repeat — this slice carries no `stimulus` and no focus windows (D10), so nothing is driven by recorded input and there are no windows to cut. An added repeat is therefore the next index, not the next window.
- **Modes.** `dry` — one job per subject on shortened phases, to verify the tooling, not pooled; `full` — the campaign. The long-phase probe of §3 is not a mode here: it runs in the existing `long-probe` family and is never a repeat (9.5 D35, D42).
- **Recorded per job.** `spec.json` (runner spec), the report with `gate` and `machine.model`, CPU model and kernel, the version of every program observed (Chrome or Chromium, Element Desktop, the homeserver, the Steam client build id), and the kernel-config lines for `PERF_EVENTS`, `SCHED_TRACER`, `TASKSTATS`, `TASK_DELAY_ACCT` and `HZ`.

## 2. Subjects

Four, one per entry. Each is run in its own job so that one subject's failure does not cost the others.

1. **Renderer, hidden** — Chrome with N distinct locally served sites open, every tab backgrounded, observed past the intensive-throttling grace. Under Chromium's documented process model a renderer is one site-locked process, so N counts sites and not tabs; the pages are served over local HTTP or placed under `$HOME`, never `/tmp`, because a snap-confined browser has a private `/tmp` and that is the recorded cause of the Phase 2 run's tabs never loading.
2. **Renderer, visible** — the same page set with the page still visible to Blink, nothing interacting with it.
3. **Chat client** — Element Desktop from the unauthenticated apt repository, pointed through `ELEMENT_DESKTOP_CONFIG_JSON` at a Matrix homeserver running on the harness's own CPUs with registration enabled. Two phases: idle, which the archetype reads, and under scripted message traffic, which is recorded and released but feeds no archetype (D11).
4. **Steam desktop client** — Valve's client installed from the launcher package or `steam-installer`, started under Xvfb and **logged out**. The job signs into nothing, drives no store and performs no account action; the Steam Subscriber Agreement §4.C prohibits automated interaction with Steam's services and §1.C makes an account strictly personal (D6). Beyond its own values this job records, for D5's open question, each helper's `--type=` role and full command line from `/proc/<pid>/cmdline`, and the helper's wake behaviour with the client window shown against minimised.

## 3. Phases

Every subject runs launch → settle → steady, and only the steady phase is carried. A settle is design and is stated per subject (9.5 D34).

- **Renderer, hidden.** The settle is documented rather than guessed: a hidden page's timers align to one wake per second, and intensive throttling takes them to one per minute after a grace of five minutes by default and **sixty seconds for a page that has finished loading**. The settle therefore ends after the grace elapses from the moment the tabs are backgrounded, measured from the load completing.
- **Phase length.** Open, and set from evidence before the first batch. At one wake per minute a short phase yields of the order of ten wakes on the throttled thread — too few for a quantile table, and too noisy a per-repeat mean for the stability rule's half-width to converge at any repeat count. One long-phase probe runs first and its steady phase is read per 10 s slice (`meas-long-probe.yml`, `campaign/slices.py`); the phase is set from what it shows and written into §10 as a dated amendment before the first batch (9.5 D35).
- **Renderer, visible; chat client; Steam client.** Nothing throttles these, so their phase lengths are not expected to need the probe, but each is stated here before the first batch rather than chosen during it. Their settles follow 9.5 D34: set from each subject's own traces, after launch and ramp-up work ends.

## 4. Instruments

`perf sched record` on the measured CPU, giving per-schedule run, wait and delay and the wakeups behind them — the instrument 9.5 and 9.6 used, and the one the audit found `meas-gui.yml`'s sampler could not substitute for. Process roles are classified from `/proc/<pid>/cmdline`, whose `--type=` marker distinguishes browser, renderer, GPU and utility processes for Chrome, Chromium, Electron and CEF alike. Affinity inherits across fork and execve, so zygote-forked renderers, Electron utilities and CEF helpers all inherit the pin. No screenshots are needed: no subject takes input.

## 5. Analysis rules, fixed before the run

- **One wake** is a schedule-in preceded by a wakeup event for that thread since its last sleep; a resume after preemption folds into the wake it continues. Decided by the thread's previous switch-out state where the timehist carries it, otherwise by a wakeup row (campaign workflow).
- **Components** are per thread comm (9.5 D16), each carrying `wakes_per_s` and measured `gap` and `run` quantile tables (D17), with a pooled residual for the comms below the coverage cut.
- **Thread counts** are carried as their observed range and are not on the stability list.
- **No pooling across subjects.** Each entry's values come from its own subject's steady phase alone; nothing is averaged across the four, which is the defect the entry being replaced carried.

## 6. The list, the tolerance, the first batch

The four items the campaign workflow requires before a first run.

1. **The list — every value the fold-in carries.** Per entry, per component: the `gap` quantile table, the `run` quantile table and `wakes_per_s`; and the pooled residual's tables. Thread counts are excluded, as above.
2. **The smallest effect the slice reports.** The slice reports two comparisons: hidden against visible renderer, whose documented separation is about sixtyfold in wake rate; and Element under traffic against idle, which under D11 feeds no archetype and lives only in the campaign results. No carried value rests on resolving a difference smaller than 10 %, so the standing tolerance is grounded for this slice unchanged: 5 % of the mean, or 1 µs where larger, `TOLERANCE` in `stability.py` with the trace's resolution as the floor. If a measured difference falls below 10 % it is reported as not resolved at this tolerance rather than as an effect.
3. **First batch.** Five repeats per subject — the rule's minimum — because no prior run of these phases exists to size the batch from, unlike 9.6, which took its first count from the spread of an earlier run. Repeats are added one at a time afterwards until every value on the list holds. A job the gate stops is not a repeat, so a batch may land fewer than five and the gated indices are relaunched together.
4. **What a repeat is.** The next repeat index, as in §1.

9.6 D29's exception — a value whose spread follows the machine rather than the program, carried over the repeats obtained with its half-width, observed range, repeat count and share of the job's time stated — is available but is not invoked in advance. It applies only by 인지오's explicit decision per value, and only to a value carrying none of the effects above.

## 7. Scope, written into every archetype

Each entry states: the runner spec and the CPU model and kernel it was measured on; the version of the program observed; the state it was observed in — hidden past the grace, visible, idle against a local homeserver, or logged out — and what that state is not; and the stated limitations. Specifically: the renderer entries are Chrome on a hosted runner without a GPU and without display vsync under Xvfb; the chat-client entry carries no message-traffic wakes and stands in for account-gated clients; the Steam entry is a client that is neither logged in nor behind a running game.

## 8. Release

The raw records of the campaign are one release, as 9.5, 9.6 and 9.7 released theirs. Pooled `results.md` and `pooled.json` go in this folder; each entry's row — repeats, the values on the list, the widest half-width among them, what stopped it, jobs and gated draws — goes into `../../measurement-campaign-record.md`. Publishing the raw records outward is asked before it is done.

## 9. Open before the first batch

- The phase length of each subject, the hidden renderer's from the long probe (§3).
- N, the number of distinct sites for the renderer subjects, and whether the browser is the preinstalled Google Chrome or the unconfined Chromium.
- Which Matrix homeserver, and the scripted traffic's rate, which is design and stated (D11).
- The tooling named in the header, and whether the Steam client holds a stable state logged out — if it does not, D6's fallback retires that binding instead.

## 10. Amendments

None yet.
