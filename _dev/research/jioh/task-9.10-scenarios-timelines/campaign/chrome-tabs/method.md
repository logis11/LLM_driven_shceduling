# Task 9.10 — Chrome's renderer count for five tabs: method (2026-10-04)

The observation behind the number of `renderer-hidden` tasks every file showing Chrome carries — `c1-browsing`, `c1-office`, `c3-workday`, `c3-evening`, `c4.variant.yaml`'s `c4-compile` injection and the files derived from them (changelog D15, D16, D126–D129) — run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/desktop/` — the `chrome-tabs` subject of `run.sh` (`tabs_subject`, `tabs_arm`, `tabs_hold`), its `appdefs.sh` arm beside 9.8's renderer subjects, the listing and summary `tabs.py`, and `pool.py`'s count branch — workflow `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, loop family `desktop`, app `chrome-tabs`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:desktop:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date; each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: two launches of Chrome on the tab set, the spare renderer off and on, each in a fresh profile, their order alternating by index — odd indices the spare off first (D128). Identical work, so an added repeat is the next index. Artifact `meas-desktop-chrome-tabs-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, the phases shortened to `run.sh`'s dry lengths (launch settle 20 s, grace 75 s, steady 45 s), the tab set unchanged; `full` — the campaign.
- **What is carried** (D127, D129). The number of page renderers beyond the page in use that the spare-off launch holds through the steady phase: the `renderer-hidden` tasks a file carries. Beside it: the spare, the spare-on launch's plain renderers beyond the spare-off launch's; Chrome's WebUI and extension renderers per phase. A count is not on the stability rule's list — the workflow carries thread counts as their observed range — so it is carried as observed.
- **First batch.** Repeats 1–5, the workflow's floor (`kalibera-ismm13` §11). The count holds when every pooled repeat gives one hidden count and one spare count; if they disagree, the decision returns to 인지오 (D129).
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; Chrome's version recorded; both launches run, each with a window; the measured tree holding no harness process (`check_tree`, per launch); the page server answering 200; one request for the page per tab in each launch (`tabs.<arm>.page_loads` = `tabs.tabs`); each launch's steady phase listed. A steady phase whose plain renderers moved, or changed pids, is reported with the repeat.
- **Recorded per job.** The runner spec, pin and kernel; Chrome's version; each launch's command line, affinity and exit time; the page server's log; every listing of Chrome's tree (`tabs.tsv`: launch, phase, seconds from the launch, pid, parent, `--type`, role, renderer client id, start time, threads, CPU ticks); every renderer's whole command line at each launch's end (`renderers.tsv`); screenshots after each launch's settle and steady phase; the edges of every phase.

## 2. Inputs (D126, D129)

- **Chrome.** The runner image's preinstalled Google Chrome, its version recorded per job (154.0.8037.57 on the image of 2026-09-27; S2-65). A fresh profile for each launch (`/tmp/chrome-data` removed before it), `--no-first-run`.
- **The flags** (D128). Spare off: 9.8's renderer subjects' `CHROME`, `--no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data --disable-features=SpareRendererForSitePerProcess`. Spare on: the same less the last flag, the `chrome` arm's flags, 9.5's launch.
- **The tabs** (D126). One window: the first tab `http://127.0.0.1:8099/idle-page.html?ms=100`, selected from launch, the page in use; four background tabs at 127.0.0.2 to 127.0.0.5 on the same port and query — five sites. The page is 9.8's `idle-page.html`: a 100 ms `setInterval` whose callback only counts.
- **The page server.** `python3 -m http.server 8099 --bind 0.0.0.0` on the harness CPUs, serving `idle-page.html` from `/tmp/idle-page`.
- **The display.** Xvfb `:99`, 1280×800×24, on the harness CPUs.

## 3. Phases

In each launch, in the job's order:

| Step | Length | CPUs | Instruments |
|---|---|---|---|
| launch | to Chrome's window, at most 120 s | measured (Chrome); harness (the rest) | listing from its end |
| launch settle | 20 s | as above | listing every 10 s; the tree check; the page loads counted |
| grace | 630 s, the tabs background pages from the launch | as above | listing every 10 s |
| steady | 600 s | as above | listing every 10 s; renderers' command lines at its end |
| exit | the session killed, up to 30 s for its processes to leave | harness | none |

The phase lengths are 9.8's hidden-tab subject's: the grace 630 s, the documented five-minute default before intensive throttling and 300 s of design (9.8 D15), the steady 600 s (9.8 D15). The listings run from the harness CPUs; each takes one pass over `/proc`.

## 4. Instruments

`tabs.py list`, every 10 s: every process whose command line holds `chrome-data`, its role read from the command line as 9.8's analysis reads it — `--top-chrome-webui` a WebUI renderer, `--extension-process` an extension renderer, any other renderer `plain` (`analyze.NOT_PAGE_RENDERER`). No `perf`.

## 5. Analysis rules

- **Page renderers** (D128). In the spare-off launch, every plain renderer hosts a page.
- **The count** (D127). The spare-off launch's plain renderers in the steady phase, when they hold one count through it, less one, the page in use: `tabs.hidden`.
- **The spare** (D128). The spare-on launch's plain renderers in the steady phase less the spare-off launch's: `tabs.spare`.
- **Also reported.** Each phase's WebUI and extension renderers (minimum and maximum over its listings); whether the steady phase's plain renderers are one pid set from its first listing to its last; the first listing at which the plain count reached the steady phase's; the per-repeat table and the counts across repeats (`pool.py`, `tabs.pool`).

## 6. Scope, written into the files' notes

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); Chrome as the runner image ships it, the build per repeat; one window of five tabs, the first selected, at five loopback addresses serving one local page with no subframes (D126) — a floor for real sites, whose cross-site iframes take processes of their own; a fresh profile on its first run, no extensions installed, no variations seed; counted through the phases `renderer-hidden`'s values come from. The spare and Chrome's own renderers are `web-browser`'s (9.5 D84).

## 7. Release

Raw records per job are released as a GitHub release named in the record at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-04, dry run #72 (37193532949; an Intel Xeon Platinum 8370C, a dry run opening the gate on any model; Google Chrome 154.0.8037.57). Every listing read every process as the browser, so every count read 0: Chrome rewrites a child's process title, and its `cmdline` is then one string, the arguments joined by spaces. The renderers' whole command lines (`renderers.tsv`) held, in the spare-off launch, the WebUI renderer and five plain renderers; in the spare-on launch, the WebUI renderer and six, the sixth started later (renderer client id 34, against 5–10). Five page loads in each launch; no extension renderer. The first launch's window took 43.7 s to map, the second's 0.5 s. Amending §4: the listing splits a command line on spaces as well as NULs.
- 2026-10-04, dry run #73 (37193972113; the AMD EPYC 7763; Google Chrome 154.0.8037.57), the listing amended. Spare off: five plain renderers and one WebUI renderer in every listing from 7.4 s after the launch, the plain renderers one pid set through the steady phase; extension renderers up to four in the launch settle, up to two in the grace, none in the steady phase. Spare on: six plain renderers from the first listing, 0.6 s after the launch, and the same WebUI and extension renderers. Five page loads in each launch. `tabs.hidden` 4, `tabs.spare` 1. The tooling holds; no further amendment.
