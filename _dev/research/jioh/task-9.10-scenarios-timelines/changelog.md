# Task 9.10 — Scenarios and timelines: changelog

The slice's decision record (`research-slice-workflow.md`, Records). Scope card `scope-card.md`; stage-2 records `search/`.

## D1 — unreachable or paywalled references and literature are dropped (2026-10-01)

By 인지오's decision, given after stage 2: a reference or a work of literature whose copy is technically unreachable or paywalled is dropped — it is neither a candidate of this slice nor a ground of the dataset.

- `zhang-chb15` (Zhang, Sun, Chai and Aghajan, *Computers in Human Behavior* 49, 2015) has no reachable copy: closed access, ScienceDirect 403, Elsevier API 429, only publisher metadata saved (`2026-09-13-verification/reads/R10-task-switching.md`; K4, C-zhang-1…5 UNVERIFIABLE). Its `dataset/sources.yaml` entry and its `docs/references.md` entry leave. No archetype value or timeline cites it; `make lint` reports only the five demand-window files the branch carries until 9.14.
- Stage-2 candidates S1-58 (CpsMark+, abstract only), S3-05 (a Windows dataset not released) and S3-06 (a Linux field study with no released data) are marked dropped in their records; the works the searches met without a readable copy are listed under "Dropped" in `search/candidates.md`. The search logs keep the queries that met them.
- Checked and kept, each with a copy that answers on 2026-10-01: `cpsmark-tbench23` (the publisher PDF from the Wayback capture of ScienceDirect's `main.pdf`, re-fetched byte-identical, SHA-256 `04d9f106862dfaaa8188dedfe06479c9742a578b4dcfb9d4e4dbde687c90f067`, the copy `reads/R04-cpsmark.md` read); `sysmark25` and the SYSmark 2018 documents (the Wayback copies of the user guides and white papers `reads/R05-vendor-benchmarks.md` read, HTTP 200); `chang-chi21` (the publisher PDF, CC BY 4.0, from a Wayback capture, S1-36). The other registry and reference entries in the scope card's group H were read in full from the copies the 2026-09-13 reads or the stage-2 records name.

Hands to 9.15: the prose that cites `zhang-chb15` is rewritten without it — `docs/workload/building-plan.md:137` (the planned naturalistic generator's hub-and-spoke switching, whose only source it was), `docs/workload/source-vetting.md:75`, `docs/workload/grounding-sources.md:81`.

## D2 — the core set's task sets are design (2026-10-01)

By 인지오's decision, scope-card items 22–44 (the task sets of the 23 authored timelines, and through them the 27 derived files) and the Source column of the scenario catalog's rows (items 3–20): which programs share a segment of a core-set file is the experiment's composition, chosen for the claim the file makes, and is labelled design (phase decision 3). No core-set file presents its task set as how desktops behave. Grounds: the core set is built "one file per claim (coverage grid)", and "every file exists to make a specific measurement possible", with ecological validity assigned to the naturalistic set (`docs/workload/building-plan.md` §0, §3). The stage-2 search over the four classes found no observation of which programs run together on Linux desktops (`search/candidates.md`, "Not found across classes"). The nearest candidates: SWELL-KW (S3-01: a Windows 7 lab, 2012, prescribed tasks; {Outlook, Word, IE} open together 63.4 % of working time, reader's own), BEHACOM (S3-02: the foreground program per minute and the count of top-level windows, not the open set), and benchmark definitions (S2-14, S2-15: existence only).

Each of these stays a realism claim, decided at its own item:

- each program's existence on Ubuntu 24.04 under the name the file shows (items 64–66);
- a situation a file presents as happening — an unasked scan, a module rebuild after a kernel update, a scheduled or user-started job (items 67–71; the card's boundary call (a));
- the state each bound entry describes, against the state the file depicts (item 63);
- counts (items 50–55), the arcs' order (items 41–43) and the recipes' premises (items 45–49).

No binding or value changed; the timeline headers state calibration and lineage, not observed sets, and are unchanged.

Hands to 9.15:

- `docs/workload/building-plan.md` §3's C1 paragraph ("Task sets are lifted from the segment that already carried the mode, the source named in each file's header", and its per-mode sets) restated as design;
- the scenario catalog's Source column states existence only;
- the limitation stated beside the venue limitation (`docs/workload/measurement-overview.md` §11): the scheduling-benefit result holds on these compositions, which are not shown to be typical.

## D3 — the unasked anti-virus scan is replaced by the stock unattended upgrade (2026-10-01)

By 인지오's decision, scope-card items 19 and 67: the unwanted job the eleven scan files add — `clamscan` on `cpu-batch`, `background: av-scan`, in the ten interactive attribute counterparts (`c7.variant.yaml`) and in `c2-p2b` (`c2-pairs.variant.yaml`), eight of them judging files — is replaced by the stock Ubuntu 24.04 unattended upgrade, observed in a runner campaign of its own under `measurement-campaign-workflow.md`. The campaign and its entry are 9.10's, the domain slices being closed.

Grounds (S2-30, read at stage 3; S2-03; S3-35; S3-30):

- **The scan's premise.** ClamAV's documentation describes "an open source (GPLv2) anti-virus toolkit, designed especially for e-mail scanning on mail gateways" and states "ClamAV is not a traditional anti-virus or endpoint security suite" (`Introduction.md:10`, `:12`, at `26dceb2`); it names "scheduled malware scanning" as a feature of endpoint security suites (`Terminology.md:13`) and documents `clamscan` as a one-time scan (`Scanning.md:152–156`); no ClamAV package examined ships a scheduled scan (S2-03). A scheduled `clamscan` on a desktop exists through ClamTk's scheduler, a daily user crontab line (`lib/Schedule.pm:424`, at `694833d`); ClamTk "is no longer maintained" (`README.md:3`) and is in regular use on 0.11 % of Debian popcon submissions, `clamav` on 0.85 % (S3-30's copy, reader's own).
- **The replacement's existence.** `unattended-upgrades` is in the default layer of the stock Ubuntu 24.04.5.1 desktop (S2-01), enabled by default (debconf default `true`), run daily at 06:00 with up to 60 min random delay, `Persistent=true` (a missed run is caught up at the next boot or resume), on AC power only (`apt-daily-upgrade.timer`, `.service`; S2-03); it installs from the release and security pockets and ESM where present (`50unattended-upgrades:6–14`, S2-30).
- **Observed with a user present.** On one ThinkPad it started at resume and ran 103 s wall, 763.98 s of CPU (S3-35b; one observation, the pending set not stated).
- **Its priority.** It lowers its own nice only while calculating the upgrade and restores it before downloading and installing (`unattended-upgrade:2150–2173`, S2-30); its unit sets no `Nice=` (S2-03).
- **The label.** `background_wanted` `false` is "work nobody asked for right now" (`docs/recognition-vocabulary.md` §1); a job the system schedules and the user did not start is that.
- **Against the other stock jobs.** `mandb` ran 1–11 s wall on two machines (S3-35a, S3-35c) and declares nice 19 with idle I/O; the apt list update 2–42 s wall on two machines (S3-35a, S3-35b); Tracker re-crawls in full only after an unclean shutdown (S2-04).

Open, for the campaign's method: the state measured — which pending set, grounded on sources read then (Ubuntu's security-update and kernel-update cadence); a run with nothing pending is short, one installing a kernel update rebuilds the initramfs — the form of the entry, and the comm the job shows (`unattended-upgr` by the kernel's 15-byte rule, S2-11; to be observed). Then, against the job's measured size: the counterparts' structure, which today has the job fill the 60 s segment so the label holds at every instant (`docs/workload/building-plan.md` §3; item 56), and the new name's familiarity tier (items 64–66). The kernel update the job installs is the event that runs DKMS's autoinstall (S2-03), the premise of `c7-compile` (item 68).

No file changed yet: the eleven files keep `clamscan` until the entry exists, then rebind together with the `background` key.

Hands to 9.14: the prior table, its pair review and the RQ0 gate spec's wording on the scan, and the eight judging files' unwanted job. Hands to 9.15: the scenario catalog's S17 row replaced; `docs/recognition-vocabulary.md`'s examples ("a scheduled scan", `av-scan`); `building-plan.md` §3 C7.

## D4 — `c7-compile`'s module rebuild is an observed DKMS autoinstall of a real module (2026-10-01)

By 인지오's decision, scope-card items 49 (its compile counterpart), 53 (a module's object count) and 68: the unwanted job of `c7-compile` — today `c1-compile`'s build renamed `make` → `dkms`, carrying the kernel build's `build-orchestrator` and `compiler-child` values and the user's 100 jobs — becomes a DKMS autoinstall of a real module observed on the runner as its own entry. The hook path fires it, as a kernel or headers install does: `/etc/kernel/postinst.d/dkms` or `header_postinst.d/dkms` → `dkms autoinstall`. The module is built at the desktop's `-j` (`make -j$(nproc)`, 9.6 D4's eight-thread desktop), and the whole run is one observation: the `dkms` script, kbuild's probes, the object jobs, modpost, link and `depmod`. `c7-compile` binds that entry in place of the rename. The campaign and the entry are 9.10's.

Grounds:

- **The trigger.** DKMS's kernel hooks run `dkms autoinstall` on a kernel or headers install, `make -j$(nproc)` per module, modules one after another (S2-03: `dkms:2295–2300`, `:2593–2597`; S4-07). The kernel security updates the unattended upgrade installs (D3) are that trigger.
- **The precondition is the user's, and common.** DKMS is in no layer of the stock Ubuntu 24.04 desktop (S2-01). It is installed on 14.70 % of Debian popcon submissions and in regular use on 7.07 %; by module, `nvidia-kernel-dkms` 3.76 %, `zfs-dkms` 1.87 %, `v4l2loopback-dkms` 0.86 %, `virtualbox-dkms` 0.42 % (S3-30, reader's own). Ubuntu's NVIDIA route is prebuilt signed modules: "We don't recommend using the DKMS modules unless you are running a custom kernel" (S2-28).
- **Real module builds differ in size.** Ubuntu autopkgtest on 2-vCPU VMs at `-j2` (S3-32, reader's own): v4l2loopback 2 objects in ≈ 3 s; VirtualBox 20 objects in 3 modules in ≈ 12 s; NVIDIA 580 open 213 objects in 5 modules in ≈ 158–174 s; ZFS 285 objects in ≈ 200 s configure plus ≈ 203 s make.
- **A module run differs in shape from a kernel build.** 9.6's structural check, v4l2loopback at `-j1` in 14 repeats: ≈ 2.9 s wall, 505 processes, 3 object jobs among 98, 434 kbuild compiler probes against 42 real `cc1` (`task-9.6-compile/campaign/results.md`, section `dkms`).
- **One observation per situation.** Phase decision 2: the rename carried the kernel build's behaviour, and a resized count would add autopkgtest's.

Open, for the campaign's method: which module, on prevalence grounded for Ubuntu desktops (NVIDIA is Debian's most installed DKMS module, Ubuntu steers NVIDIA to prebuilt modules); and whether it is measured in D3's campaign, the same event chain — the unattended upgrade installs a kernel, the hook builds the module.

`c7-compile` then differs from `c1-compile` in behaviour as well as name, the vocabulary's reading of the compile mode's `false` cell: "a module rebuild after a kernel update in place of the user's build" (`docs/recognition-vocabulary.md` §1). 9.6 D6's binding of `dkms` to `build-orchestrator` and 9.6 D32's stated limitation give way to the observation.

No file changed yet: `c7-compile` keeps the rename until the entry exists.

Hands to 9.14: `c7-compile`'s judging term and the prior table's and pair review's lines on the module rebuild. Hands to 9.15: `building-plan.md` §3 C7 ("`compile` renames `make` to `dkms`") and the scenario catalog's S11 row.

## D5 — the indexing files show Tracker indexing a real user's file set from an empty database (2026-10-01)

By 인지오's decision, scope-card item 69 (feeding items 38 and 45): the indexer state the three indexing files depict — today "a scheduled rescan" (`c7-indexing`, `c2-p1b`: `initiated: scheduled`, unwanted) and a reindex the user started (`c1-indexing`: wanted, a pre-committed miss) — is Tracker indexing every file from an empty database:

- **On the unasked side** (`c7-indexing`, `c2-p1b`): the first index of a home at login.
- **On the asked side** (`c1-indexing`): the same work after the user's own reset.

It is re-measured in a runner campaign of its own, on a real machine's files in place of the kernel's `Documentation` tree (9,462 files, 9.6 D16). The candidate is the Mahoney set (`mahoney-10gb`, 79,431 files from one laptop), which `file-backup` and `file-archiver` read. The campaign and the entry, or the `tracker` program of `cpu-batch` re-measured, are 9.10's.

Grounds:

- **No scheduled rescan.** Tracker Miners 3.7.1, the version in the default install of Ubuntu 24.04 (S2-01, S2-03), schedules none by default: `DEFAULT_CRAWLING_INTERVAL -1` (`tracker-config.c:49`) is "Maybe (depends on a clean last shutdown)" — it crawls at each start, and compares every directory's mtime against the database only after an unclean shutdown (`tracker-main.c:240–284`, `:964–995`; `tracker-miner-files.c:1341–1370`; S2-04 at `eae431e`).
- **The empty-database index.** File monitors index new files as they appear (S2-03). An empty database — a first start, a new account, a reset — is crawled and every file indexed, the state 9.6's campaign observed (9.6 D16).
- **The other reports.** Full re-indexes reported on desktops are regressions or kernel-change effects (S3-36a, S3-37); one report of a bulk import driving the indexer to all cores (S3-36c).
- **Not the re-check after an unclean shutdown.** It compares mtimes and re-indexes only what changed, at a crash rate no source gives.
- **Not newly arrived content.** Its size is a chosen batch on one report.

One measured state serves both labels: the user's reset and the first login run the same work, so the wanted and unwanted files differ by intent alone — what `c1-indexing`'s pre-committed miss states.

Open:

- the campaign's method (the file set's placement under the indexed directories, the job window as 9.6 D16 read it);
- whether `c2-p1b` takes these tables or keeps `python3`'s (9.6 D21; the next item);
- the indexer's declared class, `SCHED_IDLE` at nice 19 (9.6 D17), 9.11's.

The unasked side's `initiated: scheduled` is restated when the files rebind; it is a first login, not a schedule.

No file changed yet.

Hands to 9.15: the scenario catalog's S14 row ("unwanted-deferrable", "shipped defaults … plocate timers"); `docs/recognition-vocabulary.md`'s example "an indexer's scheduled rescan".

## D6 — `c2-p1b`'s indexer carries the measured indexer's own tables (2026-10-01)

By 인지오's decision, scope-card items 38 and 45 (answering 9.6 D21's hand-off): `c2-p1b`'s indexer takes the tables of D5's measured Tracker index, and the declared class too if 9.11 adds the field, in place of `python3`'s tables carried by the rename. The load-bearing pair then differs in segment 1 by name, behaviour and label, as the two real jobs do. The one-segment discipline holds: the files stay identical outside segment 1.

Grounds:

- **The recognizer reads identity only** — names and the post-fold annotation, never a parameter distribution (`docs/memos/2026-09-20-dataset-validity-review.md` §1) — so a recognition difference comes from the name under either set of tables.
- **The two programs differ.** The share of each program's CPU past the 10 ms boot slice without a voluntary block is `tracker` 0.530–0.536 against `python3` 0.917–0.920 in every repeat (9.6 D21). The indexer's threads exit `SCHED_IDLE` at nice 19, `python3` at the default policy (9.6 D17). "Behaviorally identical" held by construction only, and the file showed an indexer behaving as another program measured.

The pair's claim becomes two real jobs beside an editor with opposite correct policies. If 9.11 has the simulated baselines honour a declared class, a baseline may deprioritize the indexer without recognition; the RQ0 gate then measures that headroom as it is.

Applied when D5's entry exists: `c2-pairs.variant.yaml`'s P1b rename-only operation becomes a patch binding the measured indexer, its comment and `c2-p1a`'s header restated. No file changed yet.

Hands to 9.14: the pair review and prior-table rows that argue on P1's identical behaviour. Hands to 9.15: `building-plan.md` §3 C2 ("behaviorally identical CPU saturation"), scenario-catalog note 2, `cpu-batch`'s `modeling_notes` sentence on `c2-p1b` inheriting `python3`'s tables (at the fold-in of D5's entry).

## D7 — `c2-p2a`'s wanted download is an install of another game the user starts during play (2026-10-01)

By 인지오's decision, scope-card items 12 and 39: the download in `c2-p2a`'s segment 1 depicts the user starting to install another game while playing — wanted, `initiated: user` — and no longer a background update download during play.

Grounds:

- **Valve's stated default.** Valve: "Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself. You can turn this feature off by navigating to your download settings: Steam > Settings > Downloads. From here, check the Allow Downloads During Gameplay box." (FAQ 4F9E-6328-E9B8-47F9, the registry's `steam-downloads`, verified 2026-09-13, K3 C-steam-2 SUPPORTED; `2026-09-13-verification/sources/steam-downloads/faq-4F9E-6328-E9B8-47F9.txt`, SHA-256 `03d733b7…34c8c4`). Stage 2's "the default not found in any class" is answered by this source.
- **What downloads during play with the box off** (steam-for-linux #8821; S3-27). "if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately" — one user's repeated observation, SteamOS 3.4 on a Steam Deck — and Valve's issue triager's reply, "this is not specific to SteamOS or the Steam Deck".
- **The label.** `background_wanted` `true` is "work the user deliberately initiated" (`docs/recognition-vocabulary.md` §1).
- **The bound entry's state.** `game-download` measured a fresh install of a 10.4 GB depot (9.7 D4, D12).
- **What the other observations show.** Desktop reports of a game patching during its own play come from users with the box off and are reported as bugs (S3-28a, S3-28c); shader-cache jobs during play (S3-26, S3-27) are unasked and no entry describes them.

Applied: `c2-p2a.timeline.yaml` — header comment restated; segment 1 gains `initiated: user`. `c2-p2b`'s `patch-segment` replaces the segment's attributes whole, so the key does not reach it.

Open at their own items: the download's displayed name `steam` against the SteamCMD program measured (item 66), the Steam client behind a game, measured logged out with no library (item 63), the download's size (item 56).

Hands to 9.15: the scenario catalog's S10 row and the `steam-downloads` role line (`docs/references.md`, `dataset/sources.yaml`) restated — the source grounds the default pause, not a "wanted toggle" (C-steam-4); a `docs/references.md` entry minted for steam-for-linux #8821 where the docs cite it.

## D8 — the scheduled backup is Déjà Dup's periodic incremental run (2026-10-01)

By 인지오's decision, scope-card items 40, 45 and 70: the scheduled, wanted backup of `c1-backup` and `c2-p3b` — today `borg` on `file-backup`, a first backup into a new repository (9.7 D6) — becomes Déjà Dup's periodic backup, observed as the incremental run its schedule makes, in a runner campaign of its own (9.10's). The campaign runs a first backup of the Mahoney set (`mahoney-10gb`), then the periodic incremental after a stated change set. The change set is design unless the method's search finds a source.

Grounds:

- **A schedule runs incrementals.** On a repeat Borg recognises unchanged files from its files cache and "does not read their contents"; a first and a repeat backup are different loads (9.7 D6). A first backup happens once per repository.
- **Ubuntu's own backup tool.** Déjà Dup 45.2 is in Ubuntu 24.04's extended install (S2-01) with `duplicity` its default tool (gschema key `tool`, default `'duplicity'`; S4-05); its periodic backup is off by default, every 7 days once turned on, and its monitor autostarts 120 s after login (`org.gnome.DejaDup.gschema.xml:48–56`, `org.gnome.DejaDup.Monitor.desktop`; S2-03). `borg` is in no install layer (S2-01).
- **Prevalence** (Debian popcon, S3-30's copy, reader's own over 291,196 submissions). `deja-dup` installed on 4.07 %, in regular use on 2.81 % (which may count its monitor's start at login); `borgbackup` 2.78 % and 1.26 %; `restic` 1.46 % installed.
- **How backups run** (S1-90; Kljun, Mariani and Dix, JASIST 2016: 319 people, 542 computers, 2013, self-report, mixed operating systems). Of backed-up computers, 37.1 % fully automated, 14.4 % semi-automated, 48.5 % manual.
- **No weekly change set in the sources read.** `meyer-fast11` gives "about 20% are modified within the last month" (§4.4.2, p. 9; Windows file systems, 2009), not a weekly change set.

Open, for the campaign's method:

- the change set and its ground;
- the first backup's destination and Déjà Dup's settings left at their defaults;
- the process names the run shows (item 64).

Then: whether `file-backup` (`borg`'s first backup) stays in the library, which turns on whether any file binds it once the backup files rebind.

No file changed yet.

Hands to 9.14: the backup files' judging terms; the pair review's P3 lines. Hands to 9.15: the scenario catalog's S15 row; `building-plan.md` §3 C1 (backup {kdenlive, borg}) and C2 P3 ({kdenlive + borg}).

## D9 — `c7-backup` stays the scheduled run's label flip, its premise restated (2026-10-01)

By 인지오's decision, scope-card items 49 (its backup counterpart) and 70: `c7-backup` remains a pre-committed miss, with the label flipped alone on the same scheduled run as `c1-backup` (D8's Déjà Dup periodic incremental): a scheduled backup firing while nobody wants it right now — the vocabulary's `false`, "work nobody asked for right now" (`docs/recognition-vocabulary.md` §1).

Its premise is restated. An unasked backup under its own name exists — Debian's and Ubuntu's `dpkg` enables `dpkg-db-backup.timer` (`OnCalendar=daily`, `Persistent=true`), the C-plain-5 finding — but the job compares four dpkg database files with yesterday's copies, and only if one changed copies them into `/var/backups` and rotates seven generations with `savelog`, then tars the alternatives database (`/usr/libexec/dpkg/dpkg-db-backup:50–80`, S2-03's copy of dpkg 1.22.6ubuntu6.6). It finished in the second it started on one Mint 22.1 desktop (S3-35a). A sub-second job cannot hold a backup segment, so binding it would label 60 s for a job the source puts at 0 s.

The respondent quoted in S1-90 describes the situation the file depicts: a scheduled backup that "uses a significant chunk of your computers resources (slowing down everything, and make YouTube videos jumpy for example)".

Applied when D8's entry exists: `c7-backup` rebinds with `c1-backup`; `c7.variant.yaml`'s comment on the backup counterpart restated. Its judging status and its layer-1 exclusion are unchanged.

Hands to 9.15: `building-plan.md` §3 C7's sentence ("`ml-train`, `render`, `transcode`, `backup` have no same-mode unwanted name a distro or vendor runs under a distinct string") restated for backup.

## D10 — the render files bind an observed Kdenlive export (2026-10-01)

By 인지오's decision, scope-card items 9, 64 and 71: the user-started render of `c1-render` and `c2-p3a` (and `c7-render` by its flip) — today `ffmpeg` on `cpu-batch`, an encode of a generated 60 s clip (9.6 D7) standing for Kdenlive's export — becomes Kdenlive's own export of the `video-editor` entry's project, observed on the runner. Kdenlive 23.08.5, the project of that entry's scope, the default render profile; the export's process confirmed from Kdenlive 23.08's source and the run, the files binding it under the name it shows. The campaign is 9.10's, an export phase on 9.5's Kdenlive setup.

Grounds:

- **The export was left to a stand-in.** 9.5's follow-ups spec, decision 7: an operation is "Kdenlive's timeline preview render (not its export, which the batch archetypes stand for)" (`_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md:43`).
- **Kdenlive renders in its own process.** 9.5's campaign observed the preview render in an external `kdenlive_render` process, one per render (9.5 changelog, the `load_rows` fix; `dataset/tools/meas/probe/ops_driver.py:128`, "The render runs in an external kdenlive_render process"); Kdenlive ships `kdenlive_render` (S2-12).
- **The project has a measured state.** The `video-editor` entry: Kdenlive 23.08.5, one 20 s 1920×1080 30 fps H.264 clip with an unsharp effect at PCMark 10's Video Editing settings (its scope; the clip's content design).
- **"ffmpeg (render children)" has no source** (scope card item 9).
- **One situation, one observation.** The editor's project, rendered by the editor's renderer at its defaults, holds phase decision 2 where the job today pairs Kdenlive's scenario with a CLI encode's behaviour.

Open, for the campaign's method:

- the export's process and its names (item 64);
- the render profile's settings as Kdenlive 23.08 ships them.

Then:

- the job's size against the segments (item 56; the project's 20 s clip is design);
- whether `cpu-batch`'s `ffmpeg` program stays bound anywhere (the transcode files are the next item).

No file changed yet.

Hands to 9.14: the render files' judging terms; the pair review's P3 lines. Hands to 9.15: the scenario catalog's S7 row ("ffmpeg (render children)"); `building-plan.md` §3 C1 (render {kdenlive, ffmpeg}) and C2 P3.

## D11 — the transcode is `HandBrakeCLI` on CpsMark+'s workload definition (2026-10-01)

By 인지오's decision, scope-card items 10 and 71: the user-started transcode of `c1-transcode` (and `c7-transcode` by its flip) and `c3-creation`'s last segment — today `cpu-batch`'s `HandBrakeCLI` program as 9.6 measured it, `HandBrakeCLI -i clip.mp4 -o out.mp4 --preset "Fast 720p30"` on "a generated 60 s 1280×720 30 fps test pattern with a sine tone (design)" (`task-9.6-compile/campaign/method.md:20–21`) — is re-measured on CpsMark+'s HandBrake workload, in a runner campaign of its own (9.10's). The workload: an H.264 4K source transcoded to H.265 at 2K in an MP4 container, by `HandBrakeCLI` as Ubuntu 24.04 packages it. The source clip's content and length are design unless a public 4K H.264 clip is chosen, and are stated either way.

Grounds:

- **CpsMark+'s definition** (`cpsmark-tbench23`, read in full 2026-09-13, `2026-09-13-verification/reads/R04-cpsmark.md`). It lists "HandBrake" "CLI 1.3.0" in Table 2 (p. 5), and §4.3.4 (p. 6) defines the workload: "Convert the H.264 encoded source video with 4K resolution to the H.256 [sic] encoded target video with 2K resolution, the container format is MP4. Hardware acceleration will be leveraged if enabled." It is the last workload of the multimedia module's sequence.
- **No other benchmark read defines a transcode at 720p with a fast preset.** PCMark 10's Video Editing uses FFmpeg for sharpening and deshaking (S2-13).
- **The program exists on Ubuntu.** `HandBrakeCLI` is its executable (S2-12). Debian popcon has HandBrake's GUI package on 1.94 % of submissions and `handbrake-cli` on 0.66 % (S3-30's copy, reader's own). The CLI is the program CpsMark+ names.
- **The precedent.** 9.5 put its operations on benchmark definitions where no recording exists (GIMP's unsharp mask on PCMark 10's image size; `docs/workload/measurement-overview.md` §4).

Open, for the campaign's method:

- the source clip and its length;
- the encoder settings that realise "H.265 … 2K, MP4" in HandBrakeCLI, with no hardware acceleration on the runner;
- the program's tables under `cpu-batch`'s criterion (9.6 D7).

Then the job's size against the segments (item 56).

No file changed yet.

Hands to 9.14: `c1-transcode`'s and `c7-transcode`'s judging terms. Hands to 9.15: the scenario catalog's S8 row; `cpu-batch`'s scope at the re-measurement's fold-in.

## D12 — the training job is PyTorch's own basic MNIST example on the CPU (2026-10-01)

By 인지오's decision, scope-card items 14, 32 and 71: the user-started training run of `c1-ml-train`, `c2-p1a` (segment 1) and `c7-ml-train` (by its flip) — today `cpu-batch`'s `python3` program, "a PyTorch 2.14 CPU training loop of 300 steps over synthetic images" that "reads no data and writes no checkpoint" (`cpu-batch` scope; 9.6 D7, D32) — is re-measured on PyTorch's own "Basic MNIST Example" at its defaults, in a runner campaign of its own (9.10's). The run is `python main.py`: a small convolutional network trained on the real MNIST dataset, 14 epochs of batch 64, a test pass per epoch, the checkpoint written (`--save-model`), on the CPU in one process (S2-31, `pytorch/examples` at `acc295d`, `mnist/main.py:75–137`).

Grounds:

- **No observed workload exists.** No class found an observed ML training workload that desktop users run (stage 2; `search/candidates.md`, item 14); Procyon's AI benchmarks measure inference (S2-14).
- **A definition that is not ours.** The framework project's documented example, reading real data and writing a checkpoint, takes the place of the project's synthetic images and step count. The same form as D11's CpsMark+ transcode and 9.5's benchmark-defined operations (`docs/workload/measurement-overview.md` §4).
- **What is not claimed.** The files show an actual training run and do not claim that desktop users train MNIST. On the runner the run is CPU-only; GPU training, and the CPU side of it, are unobservable (`docs/workload/measurement-overview.md` §11), a stated limitation.

Open, for the campaign's method:

- the dataset's placement and download before the measured phase;
- the program's tables under `cpu-batch`'s criterion (9.6 D7) or an entry of its own if the run shows another shape (its test passes, its dataset reads).

Then how much of the 14-epoch run a file shows (item 56).

9.6 D32's hand-off on `c1-ml-train`'s id is answered: the files depict a real training run, its scope stated.

No file changed yet.

Hands to 9.14: the ml-train files' judging terms; the P1 pair's training side. Hands to 9.12 and 9.15: the wording rule of 9.6 D32 restated on the new run; the scenario catalog's S12 row.

## D13 — the mail send is one `send` operation per mail file, inside focus; `network-bulk` leaves (2026-10-01)

By 인지오's decision, scope-card items 55 and 61 (the send), applying 9.7 D3 and D30: each mail file carries one `send` operation of its `mail-client` task, started inside the task's focus window — `c1-mail` at 40 s (focus 2–58 s), inherited by `c7-mail`, and `c3-workday` at 400 s (focus 362–418 s). The separate `thunderbird` send tasks on `network-bulk` are dropped, and `network-bulk` leaves `dataset/archetypes.yaml`, its last bindings gone. One send per file is the file's calibration — the mail mode's characteristic operation shown once — and is labelled design.

Grounds:

- **The send is an operation.** 9.7 D3 made it an operation `send` of `mail-client`, now in the library (`dataset/archetypes.yaml`, `mail-client.operations.send`), and 9.7 D30 kept `network-bulk` for these three tasks only.
- **One send is within the entry's state.** The measured send is a reply with a Word attachment (kind from `cpsmark-tbench23`, size design), carried as the mean over the campaign's 25 sends, and a timeline placing many more than 25 binds a state the entry does not describe (9.5 D87).
- **The observed rates assert nothing about a minute.** SWELL-KW's Outlook "Send" clicks were 3.66 an hour in the e-mail-interruption condition alone, eight e-mails sent to each participant, and none in the other two (S3-01, reader's own); the Enron corpus gives a median of 3.21 sends per sending day across users (S3-46, reader's own). A single file asserts no rate; drawing sends at a rate from a prompted lab condition would leave a 60 s file almost always without one.
- **A send is the user's click in the focused composer**, so it starts inside a focus window. Whether every operation must is decided with operations (item 61).

Applied:

- `c1-mail.timeline.yaml` — the send task dropped, `operations: [{at: 40s, task: mailer, name: send}]` added, the header restated;
- `c3-workday.timeline.yaml` — the send task dropped, `operations: [{at: 400s, task: mailer, name: send}]` added;
- `c7-mail` re-derived;
- `network-bulk` and its section removed from `dataset/archetypes.yaml`;
- the compiler's finite-jobs comment.

The dataset was recompiled (`compile.py --allow-window`; lint reports the branch's five demand-window files and nothing else; tests 371 passed, 1 skipped, 1 xfailed). Demand: `c1-mail` 0.0549 → 0.0287, `c7-mail` 1.0549 → 1.0287, `c3-workday` 4.6602 → 4.6546.

Hands to 9.14: the three files' demand moves (the send's components in place of a 3 s `network-bulk` job). Hands to 9.15: the docs naming `network-bulk` — `building-plan.md` §2.1, `archetype-plan.md`, `coreset-guide.md` (its compiled SLEEP "~5.7 ms", memo C) and `dataset/README.md`.

## D14 — the meeting files bind one `video-call` task per call (2026-10-01)

By 인지오's decision, scope-card item 54: `c1-meeting` carries one `video-call` task, and `c7-meeting` inherits it. The duplicate task is dropped — the two `zoom` tasks `video` and `voice` both bound one measured call — and the header is restated to the current bindings; it named `video-playback`, `audio-playback` and a helper task, all three gone (9.5 D11, 9.8 D8).

Grounds:

- **The measured call is one tree.** `video-call` is a loopback WebRTC call in Chrome whose tree carries its audio and video threads together, with one periodic job, the 10 ms audio frame (9.5 D19, D75).
- **One task per application tree.** 9.5 D14 gives an application's whole process tree to one task. Two tasks ran the call twice, with two trees and two 10 ms audio-frame deadlines for one call (9.5 D75's hand-off).

The call's displayed name `zoom` against the measured Chrome WebRTC call is item 66's.

The two meeting files are reporting files (`harness/experiments/rq0-gate.yaml`); their demand falls with the dropped task.

Applied: `c1-meeting.timeline.yaml` keeps the task `voice` — the frozen scoring spec's weight-1.0 term on `voice` reads the call's 10 ms audio-frame job — and drops `video`; the header restated; `c7-meeting` re-derived. The dataset was recompiled with D13. Demand: `c1-meeting` 0.476 → 0.2387, `c7-meeting` 1.476 → 1.2387. The manifest also records D7's `c2-p2a` artifact.

Hands to 9.14: the scoring spec's `c1-meeting` and `c7-meeting` term on `video` (weight 0.5) has no task.

## D15 — the renderer count follows Firefox's Linux tab telemetry and an observed Chrome (2026-10-01)

By 인지오's decision, scope-card item 50: the number of `renderer-hidden` tasks a file showing Chrome carries is no longer a placeholder (today 11, 7, 7, 9 and 5 across `c1-browsing`, `c1-office`, `c3-workday`, `c3-evening` and `c4-compile`'s injection, and the files derived from them). The count is set in two steps.

- **Tabs** — the median per-client peak of concurrent tabs in Firefox's Linux telemetry, 4.67 (S3-40: GLAM, Firefox Desktop on Glean, release 152, Linux slice, 7,535,303 clients; `browser.engagement.max_concurrent_tab_count`, "The count of maximum number of tabs open during a subsession, across all windows"), so 5 tabs: the page in use, which is `web-browser`'s own renderer (9.5 D84), and 4 others. One statistic from one observation, the same in every file that shows a browser.
- **Renderers** — Chrome observed on the runner with that tab set, distinct sites, counting the renderer processes it keeps, the spare included if one shows. Each file then carries that count of `renderer-hidden` tasks.

Grounds:

- **No count carried a citation.** The tab studies the building plan names give tab counts only, nothing about processes (scope card item 50; K4 §2.2; C-tabs-1). The old totals, 6, 8, 10 and 12, coincide with four Chang figures, three of them not open-tab counts (9.8 card).
- **The tab count is a user-side value** and a candidate from any browser and platform (stage-2 reader rule). The Linux median holds at 3.4–5.0 across releases 137–156 (S3-40). Test Pilot's 2010 logs give a time-weighted median of 4.76 for 154 Linux users (S3-41).
- **The renderer count is a program-side value and needs Linux.** Chromium's model is one process per site (scheme plus eTLD+1), a soft limit near 96 at 16 GiB, and one spare renderer kept (S2-16, Chromium 154 source). No class found a renderer listing for a known tab set on Linux, and a runner can observe one (S4, check 12).
- **A stated choice.** The median of a per-client peak errs high for a random instant; the per-client average of those peaks, 2.79, was the alternative not taken.

Open, for the observation's method: the sites, the window, how long after the tabs load the processes are counted.

No file changed yet.

Hands to 9.14: every Chrome file's demand moves. Hands to 9.15: `building-plan.md` §3's browser-default paragraph; `data-contracts.md:159` ("one per tab group", C-plain-1); the `chang-chi21`, `dubroy-chi10`, `mozilla-testpilot10` role lines (item 77).

## D16 — one browser window: no `renderer-visible` task; the entry leaves the library (2026-10-01)

By 인지오's decision, scope-card item 51: a file showing Chrome depicts one browser window, at the statistic D15 took — the median per-client peak in Firefox's Linux telemetry. The only visible page is the one in use, whose renderer `web-browser` carries (9.5 D84), and the other tabs are hidden. The `renderer-visible` task, which 9.5 D84 fixed as "another window's page", leaves the ten files that placed it: `c1-browsing`, `c1-office`, `c3-workday` and `c3-evening` (authored), `c4-compile` (by its recipe's injection), and the derived `c4-office`, `c6-fold`, `c6-spoof`, `c7-browsing` and `c7-office`. Bound nowhere then, `renderer-visible` leaves `dataset/archetypes.yaml` under the rule 9.7 D30 applied to `network-bulk`. Its campaign stays released as `meas-ci-desktop-2026-09-20`, and 9.8's fold-in can still regenerate it from the pooled record.

Grounds:

- **Windows.** Firefox's Linux telemetry, release 152, 7,535,303 clients (S3-40; `browser.engagement.max_concurrent_window_count`, "This includes private windows and the ones opened when starting the browser"): per-client peak of concurrent windows p25 1, median 1, p75 1.93, p95 3.74; the per-client average of the daily peaks median 1, p75 1.39.
- **Test Pilot, 2010, Linux** (S3-41, 154 users, reader's own): the share of time with more than one window has a median of 0.03 (mean 0.15); the time-weighted mean of windows a median of 1.03.
- **What a second window would carry.** Chromium on Linux tracks no cross-application occlusion, so a page in another window stays visible to Blink and unthrottled when covered (9.8 D4) — the state the entry describes, which the median user's session does not hold.
- **The same statistic as D15.** One observation and one statistic set both the tab count and the window count.

Applied:

- the `renderer-shown` task dropped from `c1-browsing`, `c1-office`, `c3-workday` and `c3-evening`, and from `c4.variant.yaml`'s `c4-compile` injection;
- the derived files re-derived;
- `renderer-visible` removed from `dataset/archetypes.yaml`;
- `dataset/tools/meas/desktop/fold_in.py` folds the three entries the library carries (`chrome-visible` leaves `IDS`; its pooled values stay in the record), with its tests restated;
- `web-browser`'s scope and notes, generated by `dataset/tools/meas/campaign/fold_in.py`, name `renderer-hidden` alone for other tabs' renderers.

The dataset was recompiled (`compile.py --allow-window`). 20 of 100 artifacts change beyond the library's hash, the ten files in both modes, and no demand moves at the manifest's four decimals. Lint reports the branch's five demand-window files and nothing else; tests 371 passed, 1 skipped, 1 xfailed.

Hands to 9.14: the ten files' compiled artifacts. Hands to 9.15: 9.5 D84's sentence in the docs, `docs/workload/measurement-overview.md` §2 and §9 (`renderer-visible` among the measured archetypes), `coreset-guide.md`.

## D17 — each batch job runs whole, at the input its decision fixed; files lengthen to hold it (2026-10-01)

By 인지오's decision, scope-card items 56 and 53: a batch job in a core-set file runs its measured whole, at the input its decision fixed — the jobs below. A file's and its segments' lengths follow the job. No `total_work` or `spawn_count` describes part of a job.

- the unattended upgrade's pending set (D3)
- a real module's DKMS build (D4)
- Tracker's index of the Mahoney set (D5)
- Déjà Dup's incremental (D8)
- the `video-editor` project's export (D10)
- CpsMark+'s transcode (D11)
- PyTorch's 14-epoch MNIST run (D12)

Grounds:

- **A slice describes part of a job.** The measured entries describe whole jobs. A `total_work` below a job's measured size describes part of a job, and how large a user's job is has no source (scope card item 56). The compiled audit at `e3d3c9a` found `c1-backup`'s `borg` could not finish even alone in its 60 s file (132.2 s uncontended; J2).
- **File length is the design part.** It is design under phase decision 3, and the core set's segment durations are "compressed event-time (long enough to generate query points; realism not required)" (`docs/workload/building-plan.md` §0). Lengthening the files moves only what is already design.
- **The inputs keep their grounding.** Inputs sized to fit the current lengths would turn the decisions' grounded inputs — a real file set, a benchmark's and a framework's definitions — into design.

9.6 D7's and 9.7 D13's "`total_work` stays timeline design" give way: the size a file binds is the measured job's.

Open:

- **Each campaign's method states the job size it measured.**
- **The compile files' `spawn_count` follows the measured build** — how much of a kernel build the user's build shows is its own question (item 53).
- **The lengths are set when each job is measured**, the files rebinding with them. The scoring spec's `turnaround` terms then hold for every whole job.

No file changed yet.

Hands to 9.14: the demand window and the per-file oracle-against-random test re-read on the new lengths; the scoring spec's windows. Hands to 9.15: `building-plan.md` §3 C1 ("batch jobs are sized to finish inside the segment").

## D18 — the user's build runs the measured kernel build whole: 2,908 object jobs at cap 8 (2026-10-01)

By 인지오's decision, scope-card item 53, under D17: every file binding the user's build on `build-orchestrator` runs the measured build whole — `spawn_count` 2,908 object jobs, `parallelism_cap` 8. Today the files bind 100 jobs (`c1-compile`, and `c4-compile` by derivation), 4,200 (`c3-workday`) and 85 (`c6-dual`). The files lengthen to hold the build, and `c3-workday`'s compile segment lengthens with it.

Grounds:

- **The measured build.** The Linux kernel's defconfig, warm, `-j8`, 14 repeats on the EPYC 7763 (9.6 D5, D30, D31). `build-orchestrator`'s `validation_stats`: "5 254 jobs per build: 2 908 object, 681 archive, 1 537 helper, 90 probe, 38 link"; "live jobs at cap 8: mean 7.87, peak 11". `spawn_count` counts object jobs, and the cap counts jobs as make's jobserver does (its `modeling_notes`). The cap is 9.6 D4's eight-thread desktop.
- **The counts were sized for something else.** They were sized when a spawn-table entry was one process of about 89 ms; a job is now six processes of about 471 ms (9.6 D31's hand-off). 4,200 exceeds a whole build.
- **No source on what users build.** An incremental rebuild after an edit would need a new observation and an edit of our design; no class found local object counts, incremental or full (`search/candidates.md`, item 53).

The whole build's object jobs hold about 2,908 × 471 ms ≈ 23 min of CPU on one lane (arithmetic on the two figures above).

The unmodelled archive, helper, probe and link jobs stay `build-orchestrator`'s stated limitation (9.6). The name the files show for each job (`child_name: cc1`, a six-process job) is item 64's.

No file changed yet: the lengths are set with the other jobs' (D17), the files rebinding together.

Hands to 9.14: `c1-compile`'s turnaround term and `c3-workday`'s and `c6-dual`'s demand on the new lengths. Hands to 9.15: `building-plan.md` §3 C1 (compile {code, make, cc1×N}).

## D19 — a gaming file carries the game chain only; the game's other threads are omitted and stated (2026-10-01)

By 인지오's decision, scope-card item 52 (9.4 D3's hand-off): a gaming file carries no game thread beyond `game-task-chain` — its 16 game members and `wineserver`. The files state that the game's remaining threads are omitted, the share of scheduling the source puts outside its busiest tasks.

Grounds:

- **The chain's source counts system-wide.** "Around 300 tasks are scheduled while running a game", system tasks included, and "Top 30-40 most frequently scheduled tasks take 95% of scheduling" (`lavd-ossna24`, slide 12; 9.4 D3).
- **No source describes the threads outside the busiest set.** No observation describes the tasks outside the deck's top 30–40 (K2 C-lavd-12 NOT IN SOURCE), so a thread count from a listing would need a behaviour no source gives — the placeholder 9.4 D3 removed.
- **Listings exist, but not with behaviour.** Monster Train 2's 105 tasks under GE-Proton (S3-22, reader's own), Dota 2's `GlobPool` workers (S3-23), Zenless Zone Zero's main thread at 95–98 % of a core (S3-25), about 125 tasks in the LAVD author's talks (S1-62, S1-63), 95 and 108 pids (9.4's S3-01, S3-02). No class found a Proton game's full thread inventory in normal play with each thread's CPU.
- **A runner game would not be a desktop game.** A game re-observed on the runner would render on the CPU, there being no GPU (S4, checks 8 and 9). A desktop game's frame loop is not what that shows, and replacing the chain would reopen 9.4's one-source decision.
- **Grafting would combine observations.** Threads taken from another game or a placeholder would join a second observation to the chain's in one situation (phase decision 2).

The chain members' displayed name `game.exe` against the real thread names (S2-18; S3-20, S3-22, S1-62, S1-63) is item 64's.

No file changed.

Hands to 9.15: `game-task-chain`'s `modeling_notes` and the gaming files' scope state the omitted share; the scenario catalog's S9 row.

## D20 — one operation per focus window on an application that has one; operations start inside focus (2026-10-01)

By 인지오's decision, scope-card items 60 and 61: every focus window on a task whose entry carries an operation holds one of it, starting 28 s after the window opens. That is 30 s in a window opening at 2 s, and 150 s in `c3-creation`'s window opening at 122 s. An operation starts only inside its task's focus window. One operation per window is the file's calibration and is labelled design. D13's send follows the same rule.

Grounds:

- **Each carried operation is the mean over its campaign's run.** `web-browser`'s first page load "takes 739 ms and 545 ms of CPU against 485 ms and 341 ms for each of the other 55", and past the first six each block holds within 2 %; the filter and the preview render are level across their runs (9.5 D87). A page load in the middle of a session is one of the 55, and the carried mean holds the first at 1/56: (739 + 55 × 485) / 56 ≈ 489.5 ms, 0.9 % above a warm load (arithmetic on 9.5 D87's figures). One per window stays within each entry's state, against 9.5 D87's hand-off on a single page load.
- **The one observed rate.** SWELL-KW's `Browser URL changed` events run at 66.7–85.7 an hour by condition, about one a minute (S3-01: lab, Internet Explorer, reader's own). No class found a rate for image filters or preview renders. One per window asserts no rate and matches the one observed.
- **An operation is the user's action in the focused application** (D13).

Applied:

- page load — `c1-browsing`, `c3-evening` and `c3-workday` (`browser`, 30 s);
- unsharp mask — `c1-photo` (30 s), `c3-creation` (`photo-editor`, 30 s);
- preview render — `c1-backup`, `c1-render`, `c1-transcode`, `c1-video-edit`, `c2-p3a` (30 s), `c3-creation` (`video-editor`, 150 s).

The derived files inherit through their bases (`c2-p3b`, `c6-fold`, `c6-spoof`, the C7 counterparts). In `c6-fold` the inherited page load starts at 30 s, the instant its segments turn from browsing to meeting.

The dataset was recompiled (`compile.py --allow-window`). 38 of 100 artifacts change beyond the library's hash. Lint reports three demand-window files — `c3-creation`, `c3-evening` and `c3-workday` — and `c2-p3a` and `c2-p3b` move into the window (0.9997 → 1.0423). Tests: 371 passed, 1 skipped, 1 xfailed.

Demand moves (`-single`):

| file | before | after |
|---|---|---|
| `c1-backup` | 0.8442 | 0.9692 |
| `c1-browsing` | 0.012 | 0.0164 |
| `c1-photo` | 0.0029 | 0.0442 |
| `c1-render` | 0.8393 | 0.9581 |
| `c1-transcode` | 0.821 | 0.9445 |
| `c1-video-edit` | 0.3527 | 0.4586 |
| `c2-p3a` and `c2-p3b` | 0.9997 | 1.0423 |
| `c3-creation` | 0.8601 | 0.8843 |
| `c3-evening` | 0.8757 | 0.8765 |
| `c3-workday` | 4.6546 | 4.6555 |
| `c6-fold` | 0.012 | 0.0164 |
| `c6-spoof` | 0.512 | 0.5164 |
| `c7-backup` | 0.8442 | 0.9692 |
| `c7-browsing` | 1.012 | 1.0164 |
| `c7-photo` | 1.0029 | 1.0442 |
| `c7-render` | 0.8393 | 0.9581 |
| `c7-transcode` | 0.821 | 0.9445 |
| `c7-video-edit` | 1.3527 | 1.4586 |

Hands to 9.14: the demand moves; the operations' windows against the scoring spec's terms. Hands to 9.15: `coreset-guide.md` on operations.

## D21 — an application started mid-file runs its observed launch phase first (2026-10-01)

By 인지오's decision, scope-card item 62 (9.5 D34's hand-off): each application a file starts mid-file has its launch observed on the runner — from exec to the end of the settle its entry was measured after — as a launch phase of its entry. A file that starts the application mid-file runs that phase first, then the steady state. Applications whose source holds no launch data arrive steady and the file states it: the game chain from the LAVD deck (D19). The files start these mid-file:

- `c3-workday` — the writer at 60 s, Thunderbird at 360 s;
- `c3-evening` — the game, the Steam client and the chat client at 60 s, the two players at 300 s;
- `c3-creation` — `kdenlive` at 120 s;
- `c4-compile` — the Chrome injection at 30 s;
- `c4-gaming` — the chat client's injection at 30 s.

The single-situation files start every application at 0 s already steady and are unchanged. The launch campaigns are 9.10's.

Grounds:

- **The launch work in 9.5's traces.** Launch work is large and lands at fixed points in every repeat (`task-9.5-interactive-typing/campaign/launch-work.md`, the 2026-09-18 campaigns in 10 s slices at a 30 s settle; 9.5 D34):
  - Chrome: a burst 20–40 s into the idle phase and one ≈ 880 ms `ThreadPoolForeground` run at 65–180 s, idle CPU 9.8 ms/s over the phase against ≈ 1.4 ms/s after the burst;
  - Thunderbird: bursts at 10–30 s and 70–90 s, 4.0 ms/s against 0.1–0.2 ms/s;
  - the WebRTC call: saturated at 0–40 s, ≈ 60–90 s and ≈ 140–170 s;
  - VS Code: a burst at 50–70 s;
  - flat: `soffice`, `kdenlive` and both `mpv` players.
- **The entries carry only steady behaviour.** Each entry describes steady behaviour after its settle — Chrome 420 s, Thunderbird 390 s, the call 210 s, the Steam client 900 s, VS Code from 200 s (`docs/workload/measurement-overview.md` §4) — and the settle's traces were never carried.
- **Outside sources.** Cold starts on Linux average 2.4 s over 22 applications (S1-80; Fedora 12, SSD); Steam's shader pre-caching runs 30–60 min at a game's launch (S3-56).
- **The arcs exist for the instant an application arrives.** The arcs' segment boundaries are the query points where the process set changes (`docs/workload/building-plan.md` §3 C3); starting every application at 0 s would remove them.

Open, for the campaigns' method:

- the applications: Chrome, Thunderbird, LibreOffice Writer, Kdenlive, `mpv`, Element, the Steam client;
- whether the launch is cold or warm, and its ground;
- the launch phase's form in each entry.

A file that ends inside a launch shows the observed profile up to its end — `c3-workday`'s Thunderbird starts 60 s before the file ends; its launch work is a time-indexed phase, not a job (D17 does not apply).

No file changed yet.

Hands to 9.14: the arcs' and the injection files' demand and terms. Hands to 9.15: `measurement-overview.md` §4's "steady behaviour, not launch work" with the launch phases added.

## D22 — the gaming files keep the logged-out Steam client, its state stated (2026-10-01)

By 인지오's decision, scope-card item 63 (the client behind a game; 9.8 D25's hand-off): the gaming files keep `steam` on `game-client` beside the game chain — `c1-gaming`, `c2-p2a`, `c2-p2b`, `c3-evening`, `c4-gaming`, `c7-gaming`. Each file's scope states the client's measured state: no account, no library, no game behind it, no `gameoverlayui`.

Grounds:

- **No other state is observable.** A client behind a game cannot be observed: 9.8 D6 decided "no account is used, and none may be" on the Steam Subscriber Agreement §4.C and §1.C.
- **The client is beside every Steam game listed on Linux.** Flatpak Steam beside a Proton game shows `steam`, 9 `steamwebhelper`, 2 `steam-runtime-l`, `reaper` and `gameoverlayui` (S3-21, reader's own); Steam's helpers beside Monster Train 2 are 11 `steamwebhelper` processes with 126 tasks (S3-22, reader's own); the LAVD talks show a Steam-client thread among the game's (S1-63). No class gives the client's per-thread CPU beside a game.
- **The carried phase fits a covered window.** The entry carries the client's window shown, and Chromium on Linux tracks no cross-application occlusion (9.8 D4), so a client window covered by a fullscreen game still counts as shown to its CEF helpers. The minimised phase was measured beside it, at 244 against 299 wakes/s (9.8 D5).

No file changed.

Hands to 9.15: the gaming files' scope statements, and the scenario catalog's S9 row.

## D23 — the chat client is shown idle; the overlay ids become `chat` (2026-10-01)

By 인지오's decision, scope-card items 7, 46 and 63 (9.8 D25's hand-off: the overlay ids, a chat client under traffic): the chat-client task in `c3-evening` (id `overlay`) and in `c4-gaming`'s injection (`c4.variant.yaml`, id `injected-overlay`) depicts Element idle, as measured, with no messages arriving. Its id becomes `chat` (`injected-chat` in the injection), and each file states that no messages arrive.

Grounds:

- **The overlay role cannot exist on Linux.** Discord's own support article states "The overlay is compatible with Windows OS only; it does not function on Mac OS or Linux" (9.8 D7), so the ids named a role the platform cannot hold.
- **The idle state is fixed by the program alone.** The entry reads Element idling against a Matrix homeserver with no messages, the one state fixed by the client and the homeserver alone. A traffic phase stayed in the campaign results because "no class found any statement of how often a real user's chat client receives messages" (9.8 D11).
- **Stage 2 found only dated rates.** 17.6 IMs per recorded hour (S1-50, 16–19 users, 2005); 1.7 conversations a day × 17.2 turns (S1-51, 2000–2001). Neither is a current chat client's rate or the traffic phase's. No class found a voice-chat client beside a game on Linux (`search/candidates.md`, item 7).
- **The ids are unscored**, so no term moves (`harness/scoring/scoring-spec.yaml`).

The displayed name `discord` over Element's measurement is item 66's.

Hands to 9.15: the scenario catalog's S5 row ("Voice chat companion (overlay on S9/S2)").

Applied: `c3-evening.timeline.yaml` (`chat`) and `c4.variant.yaml` (`injected-chat`); `c4-gaming` re-derived; `test_c4_injection_only` restated to the new id. Recompiled with D24–D27.

## D24 — a task shows the observed program's name, with two stated exceptions (2026-10-01)

By 인지오's decision, scope-card item 66 (with 5, 11, 15 and 63): of the five bindings that show one program's name over another program's measured behaviour, three take the observed program's name, one task leaves, and one keeps its name stated.

- **`zoom` → `chrome`** (`c1-meeting`, `c7-meeting`). The meeting is a call in the browser, the program `video-call` observed (a loopback WebRTC call in Chrome, 9.5 D11, D25).
- **`spotify` → `mpv`** (`c1-media`, `c3-evening`, `c7-media`). The program `audio-player` observed. `c5.variant.yaml` renames the two players by task id, the ladder's names unchanged.
- **`discord` → `element-desktop`** (`c3-evening`, `c4-gaming`). Element's processes keep the executable's name, `element-desktop` (`chat-client`'s components; Chromium never renames a process's main thread, S2-16).
- **`gamescope` leaves `c1-gaming`** (and `c4-gaming`, `c7-gaming`, derived) rather than showing `mpv`. The compositor's work during a game is unobservable on the runner — no display, no refresh (`docs/workload/measurement-overview.md` §11) — and is stated.
- **The download keeps `steam`** (`c2-p2a`), the substitution stated. SteamCMD, observed, is the Steam client's content system without its interface (9.7 D4, D12). On a desktop the work runs inside the process named `steam`, and `steamcmd`, a server tool, would be the less real name during a game.

Grounds:

- **Names are realism.** Process names are realism under phase decision 3, one observation per situation; a name and the behaviour it carries then come from one observation.
- **Calls run in the browser on Linux.** Teams on Linux is a browser web app (S2-26), and Meet and Jitsi run in the browser. Zoom's native client (`zoom` and CEF helpers, S2-25) and Spotify need an account the runner does not use (9.5 D11).
- **gamescope is not a stock desktop's compositor.** It is not packaged on Ubuntu 24.04 (S2-12, S4-06). Nested on a desktop it ticks at the host's refresh, not the clip's 30 fps (S2-21, S3-29; 9.5 D75). A stock Ubuntu desktop composites a game with GNOME Shell (S2-01).

The meeting files' recognizability shifts toward the browser, which is what Linux shows.

Hands to 9.14: the scoring spec's `c1-gaming` term on `compositor` (weight 0.5) and its derived files' have no task; the meeting files' recognition. Hands to 9.15: the scenario catalog's S3, S5, S9 and S13 rows; `building-plan.md` §3 C1 ({mpv, spotify}, {steam, game.exe, wineserver, gamescope}); `coreset-guide.md`.

Applied: `c1-meeting` (`chrome`), `c1-media` and `c3-evening` (`mpv`), `c3-evening` and `c4.variant.yaml` (`element-desktop`), `c1-gaming`'s `compositor` task and its header line removed; `c5.variant.yaml` patches the two players by task id; derived files re-derived. Recompiled with D23, D25–D27.

## D25 — a task's name is its kernel `comm` (2026-10-01)

By 인지오's decision, scope-card item 64: the name a task shows is the kernel's `comm` for its process — the exec'd file's basename cut to 15 bytes, a script keeping its own name, a process that renames itself with `prctl` taking its new name (S2-11, the kernel source). For a program a campaign ran, it is the `comm` the campaign observed; for one no campaign ran, it is derived by the rule and confirmed by observation where a campaign or the names workflow (`meas-ci:names:2`) shows it.

Grounds:

- **It is Linux's own name for the process.** The `comm` is what `/proc/<pid>/comm`, `ps`, `top` and the scheduler's task name show, and the string the campaigns recorded.
- **Truncation is what a recognizer faces.** A name-based recognizer on a real desktop meets `tracker-miner-f`, not `tracker-miner-fs-3` (`2026-09-13-verification/meas-report.md` §4; S2-12).
- **Nothing settled it before.** The schema carries names only (`docs/workload/scenario-catalog.md`, header), and no document fixed which string.

Applied now:

- `tracker-miner-fs-3` → `tracker-miner-f` (`c1-indexing`, `c2-pairs.variant.yaml`'s P1b, `c5.variant.yaml`'s tier 3; `c2-p1b`, `c7-indexing`, `c5-t3` re-derived);
- `thunderbird` → `thunderbird-bin`, the main process `mail-client`'s campaign observed (Thunderbird 156, its components; `c1-mail`, `c1-office`, `c3-workday`; `c7-mail`, `c4-office`, `c7-office` re-derived);
- C5's tier-4 names, invented, cut by the same rule so they remain strings a process could carry: `video-playback-svc` → `video-playback-`, `audio-stream-helper` → `audio-stream-he`.

Every other shown name is within 15 bytes and is the observed `comm` where an entry records one (`soffice.bin`, `code`, `chrome`, `kdenlive`, `gimp`, `steam`, `gnome-shell`, `systemd`, `dbus-daemon`). `7z` is checked against 9.7's raw records (release `meas-ci-background-2026-09-19`) when `c4-office` rebinds. The names of D3–D12's new entries take their observed `comm` when their campaigns run (`unattended-upgr` derived for D3's script).

Hands to 9.15: the scenario catalog's name strings; `coreset-guide.md`. Hands to the grid: the familiarity tiers re-read on the new strings.

## D26 — the game chain's members carry the names of the chain's own source (2026-10-01)

By 인지오's decision, scope-card item 64 (9.4's hand-off on `game.exe`): the chain's members take the names the LAVD deck's slide 16 shows for the game process's tree, in place of `game.exe` for every member.

- the head (the task's name): `Troy.exe`, the game's main thread and `wineserver`'s partner;
- `wineserver`, after the head as before;
- four `Task worker thr` → `dxvk-cs` → `dxvk-submit`, in slide 16's edge order;
- `winepulse_mainl`, `winepulse_timer` → `FAudio_AudioCli`;
- the six members slide 16 does not name keep the process's `comm`, `Troy.exe`.

The names bind in the timeline (a `member_names` binding of `game-task-chain`), keeping the library's rule that an archetype fixes no process name (`docs/workload/building-plan.md` §2.2).

Grounds:

- **Slide 16's game tree** (`lavd-ossna24`; 9.4's record, nodes as `name[pid/tgid]`, tgid 7781). Ten nodes: `Troy.exe`, four `Task worker thr`, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli`.
- **Its edges.** `wineserver → Troy.exe` epoll 134,200 and `Troy.exe → wineserver` pipe_read 58,134; each `Task worker thr → dxvk-cs` about 10,000; `dxvk-cs → dxvk-submit` 30,970; `winepulse_timer → FAudio_AudioCli` 10,213 (`task-9.4-gaming/search/candidates.md`).
- **Wine's naming.** Wine renames each process to its `.exe` name, and Windows thread names become Linux thread `comm`s (S2-18); a Linux thread created without a name of its own carries its process's `comm`.
- **One observation per situation.** The members' names and behaviour then come from one observation — 9.4 took the deck as one — under D25's `comm` rule.
- **The chain's length** is 16, "a point chosen inside the source's '15-20 game-specific tasks'" (s12; the entry's notes).

Stated: the deck's figures draw on at least three process trees (9.4's record), and the chain's linear order beyond slide 16's edges is the entry's own linearisation.

Applied: `game-task-chain` gains the `member_names` binding (`dataset/archetypes.yaml`); the chain constructor names the members from it and checks its length (`dataset/tools/wlc/compiler.py`); `c1-gaming`, `c2-p2a`, `c3-evening` and `c6-dual` bind `Troy.exe` and the fifteen names; the fixture `fx-game` and `test_chain_population` restated. Recompiled with D23–D25 and D27.

## D27 — familiarity tiers for the new names: same program keeps its tier, new names placed by the ladder (2026-10-01)

By 인지오's decision, following D24–D26: the grid's name-to-tier map (`dataset/tools/wlc/grid.py`, `NAME_TIERS`; the familiarity ladder of `docs/workload/building-plan.md` §3 C5) takes the new names by one rule, labelled design.

**The rule.** A new string for the same program keeps the old name's tier: `thunderbird-bin` tier 1 (was `thunderbird`), `tracker-miner-f` tier 3 (was `tracker-miner-fs-3`). A new program's name is placed by the ladder's definitions and examples — tier 1 transparent (`firefox`, `blender`), 2 semi-opaque (`soffice.bin`, `gamescope`), 3 opaque (`tracker-miner-fs-3`, `cc1`, `baloo_file`):

- tier 2 — `element-desktop`, a product name that does not say what it is; `Troy.exe`, a game's title in place of the word `game`;
- tier 3 — the engine internals `Task worker thr`, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer` and `FAudio_AudioCli`.

C5's tier-4 names keep their tier through C5's explicit annotation. The names of D3–D12's entries are placed by the same rule when their campaigns name them.

Grounds:

- **The tiers are design.** No source ranks names; the ladder defines familiarity as corpus-relative, and the map is authored.
- **A measured tier was not adopted.** A string's count in a public corpus would measure recall, while the ladder's tiers 1–3 grade whether a name reveals its purpose; a threshold would still be design, and it would re-tier every existing name and the C5 files built on them.

Effect: the gaming segments move from tier 2 to tier 3 (the most opaque name present); coverage, which counts cells, is unchanged.

Applied: `dataset/tools/wlc/grid.py`'s `NAME_TIERS`; the grid counts bound `member_names` toward a segment's tier; `coverage-grid.json` regenerated — `c1-gaming`, `c2-p2a`, `c2-p2b`, `c3-evening`'s gaming segment, `c4-gaming` and `c7-gaming` from tier 2 to 3, every cell still covered; `test_grid` restated to `tracker-miner-f`.

The five entries D23–D27 were recompiled together (`compile.py --allow-window`). 44 of 100 artifacts change beyond the library's hash. Lint reports the three demand-window files of D20 and nothing else; tests 371 passed, 1 skipped, 1 xfailed, after `test_c4_injection_only` was restated. Demand (`-single`): `c1-gaming` 1.0376 → 0.9153, `c4-gaming` 1.038 → 0.9158, `c7-gaming` 2.0376 → 1.9153 (the `gamescope` task gone), `c3-evening` 0.8765 → 0.8766.

## D28 — the session processes appear only in the idle files; every other file states them omitted (2026-10-01)

By 인지오's decision, scope-card items 20 and 65 (9.9 D26's hand-off: which of the four names a file carries; X11 sessions; a scheduled system job's session): the four session entries — `compositor-shell`, `audio-server`, `service-manager`, `message-bus` — are carried only by the idle files, `c1-idle` and `c7-idle`, where their measured state holds. Every other file states that the desktop's session processes are omitted, their active state being unobservable on the runner. The scenario catalog's S18 claim, "present in every segment by construction", is withdrawn. No file depicts an X11 session or an X11 client.

Grounds:

- **The entries' state is an empty, blanked session.** The entries are "observed in one idle Ubuntu 24.04 desktop session", nobody present past the idle delay, the screen blanked (9.9 D9; `docs/workload/measurement-overview.md` §2).
- **A session in use is another state.** While someone uses the desktop the compositor composes frames at the display's refresh, PipeWire runs a graph while sound plays, and the buses carry the applications' traffic — magnitudes 9.9 D1's sources put orders apart from the idle ones.
- **That state is unobservable on the runner,** which has "no display refresh, no sound device" (`docs/workload/measurement-overview.md` §11). A headless shell on a virtual monitor would render on the CPU without a GPU.
- **Non-user programs are most of what runs.** Dodier-Lazaro's Xubuntu field study counts about 92 % of process instances as non-user programs (S1-19, context), so the omission is stated where it applies, as D19 states the game's omitted threads.

A scheduled system job's session is D3's unattended upgrade, a system service.

No file changed.

Hands to 9.15: the scenario catalog's S18 row and building-plan's "[system] scope"; the files' scope statements. 9.9 D26's X11 question closes here.

## D29 — the arcs' order is design; benchmark sequences cited for their transitions' existence (2026-10-01)

By 인지오's decision, scope-card items 41–43: the order of the three arcs — `c3-workday` browsing → office → compile → mail, `c3-creation` photo → video-edit → transcode, `c3-evening` browsing → gaming → media — is design, as D2 made the core set's composition. The files and `docs/workload/building-plan.md` §3 C3 stop presenting an order as grounded. A benchmark that defines a transition is cited for that transition's existence only:

- CpsMark+'s CA workflow for browsing → office → mail (`cpsmark-tbench23`; C-cpsmark-5);
- SYSmark 30 Advanced Content Creation for photo editing beside a background encode — "A video encode is started in Adobe Premiere and sent to the background while Adobe Photoshop is launched and used to manipulate photos in the foreground" (S2-15; C-sysmark30-3).

Grounds:

- **The arcs are built for their boundaries.** Their segment boundaries are the label changes the recognizer must follow — "query points that must flip" (`docs/workload/building-plan.md` §3 C3) — built for those boundaries, not sampled; D2's ground.
- **The claimed grounds do not hold as stated.**
  - `c3-workday`'s compile segment, its longest, has no CpsMark+ counterpart (C-cpsmark-5).
  - CpsMark+'s order holds photo → video → transcode only as a subsequence, with no handoff stated (C-cpsmark-12).
  - SYSmark 30 defines an overlap, not a sequence.
  - `c3-evening` has no candidate in any class.
- **Benchmark sequences are definitions, existence only** (stage-2 reader rule).
- **The one ordering observation is partial.** It is SWELL-KW's, a Windows lab with prescribed tasks, its transitions dominated by Word ↔ IE at 66.7 % of switches (S3-01), and it covers part of one arc.

Applied: the headers of `c3-workday` and `c3-creation` restated (comments only; no compiled change).

Hands to 9.15: `building-plan.md` §3 C3's "Ordering grounded in the CpsMark+ CA cooperative workflow" and "grounded in CpsMark+ CC and SYSmark 30 ACC's photo↔video multitasking workload"; the `cpsmark-tbench23` and `sysmark30` role lines.

## D30 — `c6-fold`'s meeting segment shows the call it is labelled: a `chrome` task on `video-call` from 30 s (2026-10-01)

By 인지오's decision, scope-card item 48: `c6-fold` — `c1-browsing` split into browsing 0–30 s and meeting 30–60 s — gains a `chrome` task bound to `video-call` from 30 s to 60 s. The process names stay `{chrome}`, so the canonical set does not change at the boundary and the file stays the guaranteed miss it was built as. Its meeting segment now carries the call it is labelled.

Grounds:

- **The premise now has a ground.** Since D24 the meeting is a call in the browser, shown under the program observed. Teams on Linux is a browser web app (S2-26), and Chromium runs a call's WebRTC and audio threads in its own processes (S2-16), so a call started in the browser adds no new process name. The scope card's premise item 48 — browser tabs becoming a call while the process set stays unchanged — is then a real state.
- **The behaviour comes with the name.** Before this entry the meeting segment held only the browser's idle and typing behaviour under a meeting label. Name and behaviour now come from one observation (D24).

The call arrives mid-file, so its observed launch phase runs first once D21's launch campaigns have run.

Applied: `c6.variant.yaml`'s `c6-fold` adds the task (`id: call`) and its comment is restated; `c6-fold` re-derived; `test_c6_fold_tasks_unchanged` restated as `test_c6_fold_names_unchanged` (the base's tasks unchanged, `call` added, every name `chrome`). Recompiled (`compile.py --allow-window`): `c6-fold`'s demand 0.0164 → 0.135; `c3-creation`'s artifacts also move, carrying D29's header change into the manifest, with no demand change. Lint reports D20's three demand-window files and nothing else; tests 371 passed, 1 skipped, 1 xfailed, after the restated test.

Hands to 9.14: `c6-fold`'s demand (reporting, excluded from aggregation). Hands to 9.15: `building-plan.md` §3 C6's fold sentence.

## D31 — the remaining calibration sizes recorded as design, each with its premise (2026-10-01)

By 인지오's decision, scope-card items 44, 46 and 57–60: these are design under phase decision 3 ("label flips, injections, renames, file length, `lane_share`" are the experiment's own interventions and calibration sizes), recorded with the premises below. No file changes.

- **`lane_share`** (item 57) — the game chain's share of the lane per frame: 0.9 (`c1-gaming`), 0.95 (the download pair), 1.45 (`c3-evening`), 0.6 (`c6-dual`). At 1.45 the chain cannot meet its frames alone (`docs/workload/coreset-guide.md` §12).
- **File and segment lengths** (item 58). 60 s for the interactive single-situation files; the batch files' lengths follow their whole jobs (D17); the arcs and the limit files as authored, compressed event-time (`docs/workload/building-plan.md` §0).
- **Arrival and departure times** (item 59) — the batch jobs at 2 s or 60 s, the injections at 30 s, the spoof at 20 s; the applications started mid-file run their launch phase first (D21).
- **Focus windows** (item 60) — one per focused segment, opening 2 s after and closing 2 s before it; the compiler replays a contiguous slice of recorded input for each window (9.5 D18). Observed dwell per focus has a median of 9.1 s and a p90 of 55.6 s in SWELL-KW (S3-01, lab, reader's own), so a 56 s window sits near the lab's p90; that distribution is the naturalistic set's.
- **The C4 injections' identities** (item 46) — the chat client launched during gaming, `7z` during office work (now run whole, D17; SYSmark 30 defines archive creation, S2-15, existence), Chrome opened during a compile. Mid-session launches are observed at a median of 2.86–6.00 an hour (S3-01, lab) and 19 % of window openings launch a new application (S1-13). C-focal-1's DesktopBench precedent stays the wording fix it is: there the interruption is a separately labelled task.
- **`c6-dual`'s co-occurrence** (item 44) — gaming while actively awaiting a compile, the limit file the oracle cannot label. A kernel build beside a game appears as a stress test (S1-61, `make -j30`), a demonstration and not usage.
- **`c6-spoof`'s `chrome`-named batch job** — design by construction (9.6 D7).

Hands to 9.15: `building-plan.md` §3 C4 ("discord launch during gaming"; the DesktopBench precedent) and C6, `coreset-guide.md`, `grounding-sources.md`'s Role C line on DesktopBench.

## D32 — a timeline's bound values carry the library's rule: a source tag or a design label (2026-10-01)

By 인지오's decision, scope-card item 83: each value a timeline binds carries `source: <id>:<locator>` or a label for what it is (design, convention, arithmetic), checked by the linter against `dataset/sources.yaml` as Layer 1's numerics are. The values are `count`, `spawn_count`, `parallelism_cap`, `total_work`, `lane_share`, `member_names` and the bound program. 9.10 sets the content; the field and the lint are a schema change, 9.13's.

Grounds:

- **The provenance claim covers only the library today.** `docs/workload/building-plan.md` §6 states that "every numeric parameter in the dataset traces to an external source or to our released measurements", and the linter enforces it for the library only. Timeline bound values have no source slot (`dataset/tools/wlc/timeline.py`; memo B7), while `docs/workload/archetype-plan.md:40` calls static counts "binding-time parameters with a source tag".
- **This slice's decisions ground several bound values** — the renderer count (D15), the build's object jobs (D18), the jobs' sizes (D17), the chain's member names (D26). Others are design (D31).
- **Labelling is what phase decision 1 asks** of a value no source states: it "is labelled for what it is".

Applied when the files rebind with their measured entries; each new ground minted under `docs/references.md`'s rule.

Hands to 9.13: the field and its lint. Hands to 9.15: `archetype-plan.md:40`, `building-plan.md` §6.

## D33 — the scenario catalog lists what the dataset binds, each line an existence claim that holds (2026-10-01)

By 인지오's decision, scope-card items 1–21: `docs/workload/scenario-catalog.md` lists, per row, the names the files bind after D3–D32. Each name carries its existence ground — its package on Ubuntu 24.04 and the observation that showed its `comm` (D25) — and the scenario's existence is cited from a benchmark definition only where one defines it.

**What leaves.** The names no file binds, and every source line the 2026-09-13 verification found wrong:

- **unbound names:** `evince`, `firefox`, `teams-for-linux`, `slack`, `darktable`, `blender`, `transmission-daemon`, `cargo`, `rustc`, `ollama`, `vlc`, `updatedb`, `rsync`, `rclone`, `tar`, `xz`, `freshclam`, `Xorg`;
- **wrong source lines:** the 2,430-process figure, a DynamoRio build (memo A1); interbench's Compile load, which forks nothing (C-interbench-9); ananicy types read as categories (C-ananicy-rules-4, -7); LAVD's "companion apps" (C-lavd-16); SchedCP's ML workloads (C-schedcp-3); the Steam toggle as a wanted/unwanted decision (C-steam-4); SYSmark's "archiving analogue" (C-sysmark30-2); the ClamAV scheduled-scan pattern (C-plain-2; D3).

The rows' content, for 9.15 to write:

| Row | Names | Existence of the scenario (definition) and of the names |
|---|---|---|
| S1 office | `soffice.bin` | PCMark 10 Productivity runs LibreOffice Writer (S2-13); SYSmark 30 Office Applications; CpsMark+ document manipulation lists products, not process names (C-cpsmark-3); `comm` observed (`office-writer`) |
| S2 browsing | `chrome` | PCMark 10 Web Browsing (S2-13); CpsMark+ Internet service; `comm` observed (`web-browser`) |
| S3 meeting | `chrome` (a call in the browser) | PCMark 10 Video Conferencing (S2-13); Teams on Linux a browser web app (S2-26); D24 |
| S4 mail | `thunderbird-bin` | CpsMark+ Internet service (Outlook); SYSmark 30 keeps Outlook open (S2-15); `comm` observed (`mail-client`); D25 |
| S5 chat client | `element-desktop` | no benchmark defines it; the composition is design (D2); the overlay role withdrawn (9.8 D7; D23) |
| S6 photo | `gimp` | PCMark 10 Photo Editing (S2-13); CpsMark+ graphic design |
| S7 video edit, export | `kdenlive`, the export's process (D10) | PCMark 10 Video Editing (S2-13); SYSmark 30 Advanced Content Creation (S2-15) |
| S8 transcode | `HandBrakeCLI` | CpsMark+'s HandBrake workload (D11) |
| S9 gaming | `Troy.exe` and its threads, `wineserver`, `steam` | the chain's source `lavd-ossna24` slide 16 (D26); the Steam client logged out, its state stated (D22); the game's other threads omitted (D19) |
| S10 game install during play | `steam` | Valve's default pause (`steam-downloads`); a user-started install proceeds (steam-for-linux #8821; D7) |
| S11 development and compile | `code`, `make` and its jobs' members, `dkms` | the kernel build (9.6); DKMS's hooks (D4); SYSmark 25 names compilation only in a scenario description (C-sysmark25-1) |
| S12 ML training | `python3` | PyTorch's basic MNIST example (S2-31; D12) |
| S13 media | `mpv` (video and audio) | PCMark 10's Video playback, Battery Life Profile (S2-13); D24 |
| S14 indexing | `tracker-miner-f` | Tracker 3.7.1 in the default install (S2-01), its crawl rule (S2-04); D5 |
| S15 backup | Déjà Dup's processes (observed with D8) | Déjà Dup in the extended install, periodic every 7 days once on (S2-03, S4-05); D8 |
| S16 archive | `7z` | SYSmark 30 General Productivity's archive workload (S2-15) |
| S17 → the stock unattended upgrade | `unattended-upgr` (observed with D3) | in the default install, enabled by default (S2-01, S2-03, S2-30); D3 |
| S18 session | `gnome-shell`, `pipewire`, `systemd`, `dbus-daemon` | the idle files only (D28) |

The notes:

- note 1's coverage check is restated against the definitions above;
- note 2's P1 pair is two real jobs (D6);
- note 3's spoof stands;
- note 4's name verification is D25's `comm` rule.

Hands to 9.15: the catalog rewritten to this content; `docs/recognition-vocabulary.md:11`'s claim that the catalog's co-occurrence patterns are grounded in cited sources (D2).

## D34 — the registry entries behind scenarios: what stays, what leaves, what is minted (2026-10-01)

By 인지오's decision, scope-card items 72–78, after D2–D33. `dataset/sources.yaml` holds the sources the dataset derives values or structure from; `docs/references.md` holds every citation, under its own minting rule.

| Entry | Disposition | Ground |
|---|---|---|
| Mozilla GLAM, Firefox Desktop Glean telemetry (S3-40) | minted in both | the tab count and the window count derive from it (D15, D16) |
| PyTorch's basic MNIST example (S2-31) | minted at D12's fold-in | the training job's definition |
| Ubuntu's package sources for D3, D4, D5, D8 (unattended-upgrades, dkms's hooks, Tracker 3.7.1, Déjà Dup) | minted at each campaign's fold-in | the job definitions those campaigns derive from them |
| `cpsmark-tbench23` | kept, role restated | the existence of the S1, S2, S4, S6, S8 and S16 scenarios, and D11's transcode definition; its registry note's 1.77× restated as the CC-module figure (C-cpsmark-6) |
| `pcmark10`, `sysmark30`, `sysmark25` | kept, roles restated to scenario existence (D33) | C-pcmark-5 and C-sysmark25-2 fixed; their `to-pin` statuses pinned |
| `steam-downloads` | kept, role restated | Valve's default pause (D7) |
| `procyon` | leaves `sources.yaml` | no row or job cites it after D12 |
| `dkms-man`, `dkms-debian` | leave `sources.yaml` | D4's premise rests on Ubuntu's dkms package hooks (S2-03) |
| `gamemode-docs` | leaves `sources.yaml` | no value derives from it; its wanted/unwanted half is NOT IN SOURCE (C-gamemode-1, -4, -5) |
| `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10` | leave `sources.yaml` | no count derives from them after D15 |
| `ananicy-rules`, `interbench` | no longer cited by the catalog (D33) | — |

Every entry that leaves `sources.yaml` keeps its `docs/references.md` entry, corrected to its verdicts, only where 9.12's related-work and proposal prose still cites it; otherwise 9.15 removes it. Minting follows `docs/references.md`'s rule when each value lands.

Hands to 9.12: which leaving entries its prose still cites. Hands to 9.13: the `sources.yaml` removals with the rebuild. Hands to 9.15: the `docs/references.md` corrections and removals.

## D35 — the naturalistic generator's grounding and "the negative result" restated to their sources (2026-10-01)

By 인지오's decision, scope-card items 79–82: `docs/workload/building-plan.md` §4 and `docs/workload/grounding-sources.md` (Role C, "The negative result") are restated to what their sources support. The observations stage 2 found are named as the naturalistic generator's candidates. The generator's design stays open (Backlog); only its grounding claims change.

- **Segment durations.** `gonzalez-chi04` stays with its statistics as they are: about 3 min per *event* — one continuous use of a device or one interaction with a person, observed by shadowing (C-gonzalez-3) — and 11 min 28 s as the mean continuous segment of central and peripheral working spheres only (C-gonzalez-1); `mark-chi05` with its wording fixes (C-mark05-2, -3).
- **Hub-and-spoke switching.** Its only source was `zhang-chb15`, dropped (D1). It is marked unsourced, for the generator's own search.
- **The A→B→A interruption.** DesktopBench (`focal-arxiv26`) sessions are "assembled through template-based composition grounded in realistic creative workflows" and are not observed; its inter-action timings are a fixed 6.0 s per action (S3-03; C-focal-1, C-focal-4). It is cited only as the precedent for an evaluation shape.
- **The generator's candidate observations.**
  - SWELL-KW (`swell-icmi14`): focus sequences, a dwell median of 9.1 s, switches per hour, A → B → A returns after 83.4 % of episodes — 25 students and interns in a Windows 7 lab, 2012, open under CC BY-NC-SA 4.0 (S3-01; C-swell-1 CONTRADICTED its "registration required").
  - BEHACOM: the foreground program and switches per minute for 12 users on their own computers, 4 on Linux (S3-02).
- **The negative result, narrowed.** No public trace gives desktop process trees with names over time. BEHACOM publishes foreground executable names per minute from natural use on Linux and Windows (S3-02), and DARPA OpTC publishes process-create events with image paths on Windows 10 enterprise endpoints (C-plain-7). Mobile datasets stay excluded for foreground exclusivity; Carat's several running apps per sample are noted (C-plain-8).

Hands to 9.15: `building-plan.md` §4 and `grounding-sources.md` Role C and the negative result rewritten to this; the `swell-icmi14`, `gonzalez-chi04`, `mark-chi05` and `focal-arxiv26` role lines corrected; a `docs/references.md` entry minted for BEHACOM where the docs cite it. Hands to the Backlog item "Naturalistic generator": these candidates and the open switching shape.

## D36 — the unattended upgrade's pending set: one real day's security updates, 2026-07-27 (2026-10-01)

By 인지오's decision, D3's first open item (the state measured): the campaign measures the stock unattended upgrade installing the security updates of one real day — the latest day before the campaign at the median of the past year's working days, 2026-07-27: `glibc` 2.39-0ubuntu8.8, four binaries of the default layer (`libc-bin`, `libc6`, `libc6-dbg`, `locales`). Each repeat rebuilds the state from Ubuntu's snapshot service: the default layer as the archive stood at 2026-07-27T00:00Z, upgraded against the archive at 2026-07-28T00:00Z.

Grounds:

- **What the job installs.** By default the release and security pockets (`50unattended-upgrades:6–8`, S2-30), from packages the update stage has already fetched: `apt-daily.service` runs `apt-get update`, then `unattended-upgrade --download-only`; `apt-daily-upgrade.service` runs `unattended-upgrade` (`apt.systemd.daily:437–505`, S2-03).
- **What is pending on a day** (S3-58, reader's own; 2025-10-01 to 2026-09-30; the 1,488 binaries of the 24.04.5.1 default layer; one UTC day standing for one daily run): nothing on 222 days (61 %); non-kernel updates on 125 (34 %), a median of 2 source packages and 4 binaries, quartiles 2 and 8 binaries; a new kernel — the `linux-image-generic-hwe-24.04` meta binary published to security — on 18 (5 %), 2 to 61 days apart, median 18.
- **The median working day.** 4 binaries, the count apt reports, is the median of the 125 non-kernel days, which are 125 of the 143 days the job installs anything. Of the year's eight days at 4 binaries, 2026-07-27 is the latest.
- **Reproducible.** The snapshot service serves noble-security as it stood at a timestamp (S3-58: `InRelease` at 20260727T000000Z dated 2026-07-26 20:44:37 UTC, at 20260728T000000Z dated 2026-07-27 23:20:41 UTC).

Open, for the campaign's method: whether a kernel day is measured as well, as the trigger of D4's DKMS autoinstall (D4's open item); the environment the state is rebuilt in; the job's boundaries; the entry's form; the comm.

No file changed yet.

## D37 — the state is rebuilt in a chroot of an English default install; the measured job is the upgrade unit's own commands (2026-10-01)

By 인지오's decision, D3's open item on the environment: each repeat builds, on the harness CPUs, a chroot of the default layer of an English install — the `minimal` layer less the 43 packages its English layer removes, 1,445 binaries (S2-33) — from the archive at 2026-07-27T00:00Z (D36), and runs in it the stock download stage, `apt.systemd.daily update`, against the archive at 2026-07-28T00:00Z. The measured job is then the commands of `apt-daily-upgrade.service` — `apt-helper wait-online`, then `apt.systemd.daily install` — run in the chroot on the measured CPU. The English install is design.

Grounds:

- **The unit.** `ExecStartPre=-/usr/lib/apt/apt-helper wait-online`, `ExecStart=/usr/lib/apt/apt.systemd.daily install` (`apt-daily-upgrade.service`, S2-03); the update stage fetches the lists and the packages first (`apt.systemd.daily:437–489`, S2-03; D36).
- **What the job runs that day** (S2-32): `locales`' postinst runs `locale-gen`, which compiles every locale in `/var/lib/locales/supported.d/*` — the 18 `en_*` locales of `language-pack-en-base` on an English install; `libc-bin`'s postinst runs `ldconfig`.
- **What a chroot changes.** `libc6`'s postinst skips, when `ischroot` holds, `systemctl daemon-reexec` — systemd re-executing itself, work done in PID 1 outside the job's tree — and the reboot-required notice (`postinst:27`, `:146–170`, S2-32). The scope states both.
- **Identical in every repeat.** The snapshot fixes the state and the pending set (D36); the runner's own installed set is its weekly image's and cannot hold it.
- **The language layer.** The image installs its `minimal` layer with one language layer of eight (`casper/`, S2-33; `preinstalled_langs`, S2-01); D36's count over the English install is unchanged (S3-58).
- **What the layer holds.** No kernel and no boot loader: the installer adds them from the live session's layer (S2-33). None of the four packages' triggers reaches them — `libc6` activates only `ldconfig` (`triggers`, S2-32) — and the chroot holds the layer as the image ships it.

No file changed yet.

## D38 — the measured job starts at `apt.systemd.daily install`; the unit's wait-online step is not run (2026-10-01)

By 인지오's decision, amending D37's boundaries after the campaign's dry run (run 36843481310, repeat 1, `dry`, on the EPYC 7763): the measured job is `apt.systemd.daily install` alone, run in the chroot on the measured CPU. `apt-helper wait-online`, the unit's `ExecStartPre`, is not run; the scope states it is not carried.

Grounds:

- **What the step does** (`apt-helper.cc:216–242`, S2-34): for each of `systemd-networkd.service`, `NetworkManager.service` and `connman.service`, a `systemctl is-active -q` query, and that manager's wait-online command with a 30 s timeout only if it answers active.
- **What it did in the chroot.** `systemctl` answers every query in a chroot with "Running in chroot, ignoring command 'is-active'" and success, so all three waiters ran: `nm-online` failed ("Could not create NMClient object"), `connmand-wait-online` was absent (exit 100), and `systemd-networkd-wait-online` reported "Timeout occurred while waiting for network connectivity" — 27 s of the 56 s phase with no CPU, before the install stage's first tree row at 30 s (`cmd.upgrade-install.log`; the per-second profile of the dry run).
- **What it is on an online desktop.** Only the active manager's waiter runs, and it returns once the network is online (S2-34); the 27 s is the chroot's, a network-down state none of the files depict.

The dry run otherwise held D36 and D37: the layer built from the snapshot in 581 s with the 1,445 packages and none extra; the download stage fetched the four packages; the install stage installed `libc-bin`, `libc6`, `libc6-dbg` and `locales` 2.39-0ubuntu8.7 → 2.39-0ubuntu8.8 and nothing else, in 26.1 s of CPU over 923 processes — the 18 `localedef` runs of `locale-gen` 19.8 s (76 %), `unattended-upgrade` 2.4 s, everything else 3.9 s — the CPU saturated from the install stage's start to its end.

Tooling: `dataset/tools/meas/background/run.sh`, the `upgrade` job's phase command.

## D39 — the unattended upgrade is a new entry in the batch-loop form, over the whole process tree (2026-10-01)

By 인지오's decision, D3's open item on the entry's form: the job is a new archetype with `cpu-batch`'s batch-loop constructor (9.7 D29) — one task; a run drawn from the tree's runs between voluntary blocks, pooled over every process of the tree, then the block that followed such a run, the tree's own off-CPU time, zero when another of its processes runs on or is runnable — until the job's CPU is spent. The CPU total is the measured whole (D17) and is carried. The tree's structure — its process count, its stages and the dominant program — is stated in the entry's `modeling_notes`, as `file-archiver` states its flattened threads (9.7 D22).

Grounds:

- **The job is one saturated chain** (the dry run, D38): 26.1 s of CPU over 923 processes, the measured CPU busy from the install stage's start to its end — `unattended-upgrade` computing the upgrade, `dpkg` unpacking and configuring the four packages, `locale-gen`'s 18 `localedef` runs back to back (19.8 s), then `mandb`, `apt-check` and `unattended-upgrade`'s close.
- **The form keeps that character.** Over the dry run's tree: 14,746 runs between voluntary blocks, median 7 µs, the `localedef` runs above the 99.9th percentile (over 1 s each); the block after a run zero through the 75th percentile, so consecutive runs merge into long ones, as the job is.
- **The library's precedent.** `cpu-batch`, `file-backup`, `file-archiver` and `game-download` carry the same form (9.7 D29); `analyze.py` computes it for the tree (`batch_run_us`, `batch_block_us`).
- **What the form drops.** The stages' order and the process count; the task shows one name (the next open item).

Open, for the campaign's method: the name the task shows and the entry's id.

Tooling: `dataset/tools/meas/background/analyze.py`, every process of the `upgrade` tree counted as the program's.

## D40 — the task shows `unattended-upgr`; the entry is `package-upgrade` (2026-10-01)

By 인지오's decision, D3's last open item: the one task of D39's form shows `unattended-upgr`, the `comm` of `/usr/bin/unattended-upgrade` as the dry run observed it (979 schedule rows; the kernel's 15-byte rule, D25), and the archetype's id is `package-upgrade`.

Grounds:

- **D24 and D25.** A task shows the observed program's name, as its kernel `comm`; D25 derived `unattended-upgr` for this job in advance.
- **The program the unit runs.** `apt.systemd.daily install` runs `unattended-upgrade` (`apt.systemd.daily:491–505`, S2-03); in the dry run it is alive across the install stage and the parent of every `dpkg`.
- **The other observed names.** `apt.systemd.dai` (the unit's script, cut to 15 bytes) names a wrapper; `localedef` holds 76 % of the CPU but is this day's content, glibc's locales, not the job.

The entry's `modeling_notes` state that most of the CPU under the name is `locale-gen`'s 18 `localedef` runs and that the name stands for the tree. The familiarity tier follows D27's rule at rebinding.

## D41 — each interactive counterpart is one segment as long as the job's CPU total, the job from 0 s (2026-10-01)

By 인지오's decision, D3's hand-off on the counterparts' structure (scope-card item 56): each of the ten interactive attribute counterparts becomes its base's first C seconds — C the `package-upgrade` job's CPU total as the campaign pools it — with the job arriving at 0 s, bound whole, and one segment labelled `background_wanted: false`. The bases are unchanged.

Grounds:

- **The label at every instant.** On one lane a job of C seconds of CPU is alive for at least C seconds under every policy, so the job is present throughout a segment of length C — the property the C7 design states (`docs/workload/building-plan.md` §3 C7: "arriving at 0 s with `total_work` equal to the segment so the label holds at every instant").
- **The whole job** (D17). The job is bound whole and the length follows it; under a policy that gives it the whole lane it ends one block-total after the file, the batch loop's own blocks, about 0.13 s (corrected at fold-in, D45).
- **A 60 s file would not hold the label.** The bases' own load is 0.0004 (`c1-idle`) to 0.46 (`c1-video-edit`) and 0.92 (`c1-gaming`) of the lane (`build.manifest.json`); with the job at 0 s in a 60 s file, some policies end it 13–34 s before the segment ends in nine of the ten files.
- **The smallest change to C7.** One segment, the job from 0 s, as before; only the length moves.

C is set at fold-in, from the pool whose rule holds: 26.385 s, nine repeats (D45).

Hands to 9.14: the pair review and the scoring spec compare each counterpart with its base's first C seconds; the RQ0 gate spec's eight judging counterparts on the new length. Hands to 9.15: `building-plan.md` §3 C7 (the job, its length).

## D42 — pair P2's segment 1 is as long as the upgrade's CPU total in both files (2026-10-01)

By 인지오's decision, D3's hand-off on `c2-p2b` (scope-card item 56): `c2-p2b`'s segment 1 carries the `package-upgrade` job, arriving at 60 s and bound whole, and is C seconds long — C the job's pooled CPU total, as D41 — so the file is 60 s plus C. `c2-p2a`'s segment 1 takes the same length, so the pair still shares segment 0 and differs only in segment 1's job and label. `c2-p2a`'s download keeps its size until its own item.

Grounds:

- **The label at every instant** (D41). The game holds 0.95 of the lane (`lane_share`); under a policy that favours the job it ends near 60 s plus C, and a 60 s segment would then carry `false` with no unwanted work for about 33 s.
- **One diff per pair.** C2 pairs share all but one segment (`docs/workload/building-plan.md` §3, "Counts and reuse"); equal lengths keep the game's terms read over equal windows.
- **The download's size is not D17's.** D17 lists seven jobs; the wanted download is not among them, and its size stays design at scope-card item 56 until decided there.

C is set at fold-in with D41's.

Hands to 9.14: P2's terms and windows on the new length. Hands to 9.15: the scenario catalog's P2 rows.

## D43 — `unattended-upgr` is familiarity tier 1 (2026-10-01)

By 인지오's decision, D27's rule applied to D40's name (scope-card items 64–66): `unattended-upgr` is a new program's name, placed by the ladder's definitions at tier 1, transparent — the name says what the job is, an upgrade nobody attended, at the kernel's 15 bytes. Labelled design, as D27's tiers are.

Grounds:

- **The ladder's definitions** (`docs/workload/building-plan.md` §3 C5): 1 transparent (`firefox`, `blender`), 2 semi-opaque (`soffice.bin`, `gamescope`), 3 opaque (`tracker-miner-fs-3`, `cc1`, `baloo_file`); D27 placed `element-desktop` at tier 2 as "a product name that does not say what it is".
- **The program is common.** `unattended-upgrades` is installed on 18.18 % of Debian popcon submissions and in regular use on 12.96 % (S2-30, reader's own).
- **The C7 property.** "tier 1 so no pair changes familiarity tier" (`building-plan.md` §3 C7): with the upgrade at tier 1, as `clamscan` was, every counterpart keeps its base's tier.

Applied at rebinding: `dataset/tools/wlc/grid.py`'s `NAME_TIERS`.

## D44 — a cut counterpart keeps its base's placement in proportion: focus 2 s to C − 2 s, each operation at its fraction of the window (2026-10-01)

By 인지오's decision, D41's cut against D20: in each interactive counterpart cut to C seconds, a focus window runs from 2 s to C − 2 s — the base's 2 s margins — and each operation sits at the same fraction of its window as in its base: `c7-browsing`'s page load, `c7-photo`'s unsharp mask and `c7-video-edit`'s preview render at the window's middle (the base's 30 s in 2–58 s), `c7-mail`'s send at 0.679 of it (the base's 40 s in 2–58 s). The times are written explicitly into the recipe, the rule in its header. Design (D31).

Grounds:

- **D20.** Every focus window on an application that has an operation holds one of it, and an operation starts only inside focus; a literal cut at C ≈ 26.5 s drops the four operations at 30 s and 40 s and leaves four windows without one.
- **The bases' own placement.** All ten bases are one 0–60 s segment with every task 0–60 s; the five focused ones hold a 2–58 s window, and the four with an operation place it at 30 s or 40 s (`c1-*.timeline.yaml`).

Tooling: `dataset/tools/wlc/deriver.py` gains `set-focus` and `set-operations`, which replace a derived file's focus windows and operations as `set-segments` replaces its segments.

## D45 — the unattended-upgrade campaign holds at nine repeats; `package-upgrade` folded in, the eleven files rebound (2026-10-01)

The campaign of D36–D40, `meas-ci:background:2026-10-01`, run under `../measurement-campaign-workflow.md` and recorded in `campaign/upgrade/` (method, machine draws, `results/pooled.json`, `results/results.md`) and in `measurement-campaign-record.md`.

- **Runs.** The first batch, repeats 1–5 (runs #100–#104, the gated indices relaunched together): every repeat valid; the block per run held, the run between voluntary blocks (±6.31 %) and the CPU total (±7.72 %) did not, the pool projecting nine. Repeats 6–9 were added as one batch up to that projection (9.7 D26, run #105). 15 jobs, 9 landed, 6 stopped by the machine gate.
- **The rule holds at nine** on the three values of the list: the tree's run between voluntary blocks 1.798 ms ±3.10 %, the block per run 8.90 µs ±0.53 µs (inside the 1 µs floor), the CPU total 26.385 s ±3.78 %. Every repeat valid: the layer built with no package missing or extra, the four packages downloaded and installed 2.39-0ubuntu8.7 → 8.8 with one change set in every repeat, "All upgrades installed".
- **Reported.** 916 processes in every repeat; CPU over the stage 0.990–0.994; `localedef` 72.8–76.5 % of the CPU; 13.2–14.1 % of runs followed by a non-zero block, 0.11–0.13 s of blocks a job. Repeats 4, 5 and 9 used 6–14 % more CPU than the mean of the other six in identical work — `unattended-upgrade`'s Python 21–50 % more in 4 and 5 — on the one CPU model; the rule absorbs it at nine.
- **Release.** The raw records are release `meas-ci-background-2026-10-01`, published on 인지오's go-ahead.
- **Fold-in.** `package-upgrade` in `dataset/archetypes.yaml`, its two tables written by `batch_fold_in.py` from `results/pooled.json`.
- **C** (D41, D42) is the CPU total, 26.385 s. D41's grounds sentence on finishing is corrected: the batch loop sleeps through the job's own blocks as well, so with the whole lane the job ends about 0.13 s after a file of length C; it is alive at every instant of the segment under every policy, as D41 states.
- **Rebound.** The ten interactive counterparts (`c7.variant.yaml`, D41, D44) and `c2-p2b` (`c2-pairs.variant.yaml`), `c2-p2a`'s segment 1 to 86.385 s (D42), `unattended-upgr` at tier 1 in `grid.py` (D43); `test_c7_interactive_counterparts_inject_the_upgrade` restates the C7 test for D41.

Recompiled (`compile.py --allow-window`): 24 of 100 artifacts change beyond the library's hash — the ten counterparts, `c2-p2a` and `c2-p2b` in both modes. Demand (`-single`): `c2-p2a` 1.1735 → 1.2545, `c2-p2b` 1.1735 → 1.2706 (both inside the window); `c7-browsing` 1.0164 → 1.0176, `c7-office` 1.027 → 1.0255, `c7-mail` 1.0287 → 1.0545, `c7-dev` 1.3319 → 1.295, `c7-photo` 1.0442 → 1.0967, `c7-meeting` 1.2387 → 1.24, `c7-gaming` 1.9153 → 1.9149, `c7-media` 1.128 → 1.1267, `c7-video-edit` 1.4586 → 1.5618, `c7-idle` 1.0004 → 1.0007. Lint reports the three demand-window files of D20 and nothing else; tests 372 passed, 1 skipped, 1 xfailed, after the two count tests took the new entry's tables and list.

Hands to 9.14: the eight judging counterparts and P2 on their new lengths; `cpu-batch`'s `clamscan` tables are bound by no file. Hands to 9.15: `building-plan.md` §3 C7 and the scenario catalog's S17 row (D3).

## D46 — the DKMS build is NVIDIA's module, measured in a campaign of its own (2026-10-02)

By 인지오's decision, D4's two open items. The module `c7-compile`'s autoinstall builds is NVIDIA's DKMS module. On Ubuntu 24.04 the module is installed as `nvidia-dkms-<branch>`, which `apt install nvidia-driver-<branch>` pulls in when no prebuilt `linux-modules-nvidia-<branch>-*` package is installed. The entry's `modeling_notes` state that premise: the user installed the driver package directly, not through `ubuntu-drivers`. The build is measured in a campaign of its own. D3's campaign installed 2026-07-27's `glibc` update (D36), which carries no kernel, so no DKMS hook fired in it.

Grounds:

- **Prevalence.** Debian popcon is the only per-module count (S3-30; Ubuntu's popcon is stale since 2021). `nvidia-kernel-dkms` is installed on 3.76 % of submissions and `nvidia-kernel-open-dkms` on 0.74 %, against `zfs-dkms` 1.87 %, `v4l2loopback-dkms` 0.86 %, `broadcom-sta-dkms` 0.44 % and `virtualbox-dkms` 0.42 %.
- **ZFS and v4l2loopback do not build through DKMS on Ubuntu.** Every HWE kernel install depends on `linux-main-modules-zfs-<abi>` and `linux-main-modules-v4l2loopback-<abi>`. These ship the modules prebuilt and provide `zfs-dkms` and `v4l2loopback-dkms` (S2-35).
- **The NVIDIA DKMS route on Ubuntu.** `nvidia-driver-580` depends on `nvidia-dkms-580`, which depends on `dkms`. The prebuilt `linux-modules-nvidia-580-generic-hwe-24.04` provides `nvidia-dkms-580` (S2-35). `ubuntu-drivers install` takes the prebuilt package and drops a DKMS-only driver unless given `--include-dkms` (S2-36). Ubuntu's NVIDIA page: "We don't recommend using the DKMS modules unless you are running a custom kernel" (S2-28).
- **The alternatives.** Ubuntu's VirtualBox builds through DKMS on every install, and the Broadcom STA driver is DKMS only and auto-installed by `ubuntu-drivers` (S2-35, S2-36). Each is about a ninth of NVIDIA's count on Debian.

Open, for the campaign's method: the branch and the flavour (proprietary or open); the kernel the hook fires for; the environment the build runs in; the job's boundaries; the entry's form; the comm.

No file changed yet.

## D47 — the module is NVIDIA's 595 branch, open flavour: `nvidia-dkms-595-open` (2026-10-02)

By 인지오's decision, D46's first open item: the module the hook builds is `nvidia-dkms-595-open`, the open kernel module of NVIDIA's production branch 595. D46's user installs it as `apt install nvidia-driver-595-open`, whose dependency resolves to it.

Grounds:

- **Ubuntu's recommendation.** Ubuntu 24.04's desktop driver branches are 580 (long-term support, `restricted`), 595 (production) and 610 (new feature), both in `multiverse`. Each has a proprietary and an `-open` flavour, and every one of them declares `Prefer-Variant: Open` (S2-35). An installed desktop has `multiverse` enabled (S2-38). `ubuntu-drivers` ranks the preferred `-open` flavour first, then a production or long-term branch over a new-feature one, then the higher name (S2-36). So it recommends `nvidia-driver-595-open` for every GPU in 595's device list, and `nvidia-driver-580` only for the 160 device ids that 580 lists and 595 and 610 do not.
- **NVIDIA's recommendation.** "We recommend the use of open kernel modules on all GPUs that support it." Its installer defaults to the open flavour. The open modules run on Turing and later; in 595 the proprietary flavour covers only Turing to Hopper (S2-37).
- **Users' GPUs.** In Steam's August 2026 Linux survey, 87.0 % of the listed NVIDIA share (21.16 % of 24.32 %) is a GPU the open modules support. The remaining 3.16 % are GeForce GTX 10xx and 970 cards (S3-59, reader's own).
- **Against 580.** Ubuntu's autopkgtest sized the 580 builds (S3-32): open, 213 objects in 5 modules, ≈ 174 s at `-j2`; proprietary ≈ 158 s. 595's size is the campaign's to observe. Debian popcon counts the proprietary flavour most, 3.76 % against 0.74 % (S3-30).

Open, for the campaign's method: the kernel the hook fires for; the environment the build runs in; the job's boundaries; the entry's form; the comm.

No file changed yet.

## D48 — the hook fires for 2026-09-23's security kernel, `7.0.0-31` → `7.0.0-34` (2026-10-02)

By 인지오's decision, D47's first open item: the kernel the hook builds the module for is the one the security pocket published on 2026-09-23. This is the latest security-kernel day before the campaign. The state is the archive at 2026-09-23T00:00Z: the desktop on HWE kernel `7.0.0-31.31~24.04.1`, with `nvidia-dkms-595-open` 595.91.07 installed and built for it. The unattended upgrade against the archive at 2026-09-24T00:00Z installs `7.0.0-34.34~24.04.1`, and the hook builds 595.91.07 for `7.0.0-34-generic`.

Grounds:

- **Unasked.** The stock unattended upgrade installs from the release and security pockets (`50unattended-upgrades:6–8`, S2-30; D36). `7.0.0-34` reached security on 2026-09-23T15:49:46, replacing `7.0.0-31` (2026-09-04). `7.0.0-38` is in the updates pocket only (2026-10-01), which the job does not install from (S3-60).
- **The driver on that day.** 595.91.07 is in the updates pocket from 2026-09-15 (S3-60). A desktop's sources include the updates pocket (S2-38), and the user's own updates install from it.
- **The day rule.** D36's state was the latest day before the campaign meeting its criterion. A security kernel arrived on 18 days of the past year, a median of 18 days apart (S3-58).
- **Reproducible.** The snapshot service serves the pockets as they stood at a timestamp (S3-58; D36).

Open, for the campaign's method: the environment the build runs in; the job's boundaries; the entry's form; the comm.

No file changed yet.

## D49 — the state is D37's chroot plus the kernel the installer adds and the NVIDIA driver package (2026-10-02)

By 인지오's decision, D48's open item on the environment. Each repeat builds, on the harness CPUs, D37's chroot from the archive at 2026-09-23T00:00Z (D48): the default layer of an English install, 1,445 binaries (S2-33). It then installs the kernel the installer adds, `linux-generic-hwe-24.04` (`7.0.0-31` at that time), followed by `apt install nvidia-driver-595-open`, the install D46's user makes. That install pulls in `dkms` and `nvidia-dkms-595-open` 595.91.07 and builds the module for `7.0.0-31`, unmeasured. The sources then point at the archive at 2026-09-24T00:00Z. The kernel install that fires the hook is the stock unattended upgrade, as D3 and D4 describe the event.

Grounds:

- **One environment for both campaigns.** D37's grounds hold: the snapshot fixes the state and the pending set, and the runner's own installed set is its weekly image's.
- **What the layer lacks.** The layer has no kernel and no boot loader: the installer adds `linux-generic-hwe-24.04` from the live session's layer (S2-33). It has no DKMS and no NVIDIA driver (S2-01). The kernel and the driver package are what this premise adds. The boot loader stays out, as in D37.
- **The trigger is the event's.** Installing `7.0.0-34` from the security pocket runs the kernel's and the headers' postinst, which run DKMS's hooks (D4; S2-03).

Open, for the campaign's method: the job's boundaries; the entry's form; the comm.

No file changed yet.

## D50 — the measured phase is the kernel day's install stage; the job is every process under the two DKMS hooks (2026-10-02)

By 인지오's decision, D49's open item on the job's boundaries. The measured phase is the stock install stage of 2026-09-23 (D48), `apt.systemd.daily install` in the chroot on the measured CPU, as D38's. The job is every process rooted at a `dkms_autoinstaller` run the kernel install causes. The kernel image's postinst runs `/etc/kernel/postinst.d/dkms`, and the headers' postinst runs `/etc/kernel/header_postinst.d/dkms`. Each runs `dkms_autoinstaller start 7.0.0-34-generic`, which runs `dkms autoinstall` (S2-03). One run builds and installs the module; the other finds it installed. The rest of the stage is recorded and reported, not carried: `unattended-upgrade`, dpkg, the initramfs rebuild and `xdg-desktop-portal`, the day's other default-layer update (S3-58).

Grounds:

- **D4's observation.** "The whole run is one observation: the `dkms` script, kbuild's probes, the object jobs, modpost, link and `depmod`." Both hook runs are DKMS work the kernel install causes.
- **The hooks** (S2-03, `dkms` 3.0.11-1ubuntu13): `postinst.d/dkms:37–38` and `header_postinst.d/dkms:37–38` run `exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"`; `dkms_autoinstaller:71–75` skips when `/lib/modules/$kernel/build/include` is absent, and otherwise runs `dkms autoinstall --kernelver $kernel`.
- **The parallelism is D4's.** NVIDIA's `dkms.conf` runs its own `make -j$PROCS_NUM`, with ``PROCS_NUM=`nproc` `` capped at 16 (S2-39), and `dkms`'s default `parallel_jobs` is `nproc` too (`dkms:180–187`, `:2594`, S2-03). On the one measured CPU `nproc` reads 1. `nproc` returns `OMP_NUM_THREADS` when it is set (S2-40), so the method passes `OMP_NUM_THREADS=8` in the measured stage's environment: D4's eight-thread desktop, labelled design. (Corrected the same day: `parallel_jobs` is not among the variables `framework.conf` may set, `dkms:43–46`, and NVIDIA's `make` does not read it.)

Which hook builds follows dpkg's configure order, recorded by the dry run. Whether the second run stays carried is read against its size after the dry run.

Open, for the campaign's method: the entry's form and the comm, read from the dry run as D39 and D40 were.

No file changed yet.

## D51 — the state is the archive at 2026-09-22T17:00Z, amending D48 (2026-10-02)

By 인지오's decision, after the DKMS campaign's dry run (run 36980404122, #106, repeat 1, `dry`, on the EPYC 7763), amending D48's state time. The state (D49) is built from the archive at 2026-09-22T17:00Z. That is after the security pocket's only default-layer update of 2026-09-22 (`sudo`, 14:57:05) and before the updates pocket published `7.0.0-34` (17:43:27). The upgrade's archive stays at 2026-09-24T00:00Z, so the pending set is 2026-09-23's security day, the kernel `7.0.0-34` and `xdg-desktop-portal`, as D48 describes. The premise, stated: the user last took updates from the updates pocket before the kernel reached it.

Grounds:

- **What the dry run showed.** With the state at 2026-09-23T00:00Z, the kernel install took `7.0.0-34` from the updates pocket. The state was on the new kernel with the module built for it, and the measured stage installed `xdg-desktop-portal` alone (`dkms.state.kernels=7.0.0-34-generic`; `upgrade.uu.log`: "Packages that will be upgraded: xdg-desktop-portal").
- **The two times** (S3-60; S3-58's copy). `7.0.0-34` reached the updates pocket at 2026-09-22T17:43:27 and the security pocket at 2026-09-23T15:49:46. The security pocket's default-layer publications were `sudo` on 2026-09-22 at 14:57:05, then the kernel and `xdg-desktop-portal` (18:33:16) on 2026-09-23.
- **Checked on the snapshot service.** At 2026-09-22T17:00Z, `linux-generic-hwe-24.04` is `7.0.0-31.31~24.04.1` in both pockets, `sudo` `1.9.15p5-3ubuntu5.24.04.3` in security, `xdg-desktop-portal` `1.18.4-1ubuntu2.24.04.2`, and `nvidia-dkms-595-open` `595.91.07-0ubuntu0.24.04.1` in updates. At 2026-09-24T00:00Z both pockets have `7.0.0-34.34~24.04.1` and `xdg-desktop-portal` `…24.04.3`.
- **Against the alternatives.** A state at 2026-09-22T00:00Z adds `sudo`, two security days in one run. A state at 2026-09-23T00:00Z with the kernel held back is current in every other package, which no ordinary user action produces.

The dry run otherwise held D49: the layer built from the snapshot in 519 s with the 1,445 packages and none extra; the kernel install and `nvidia-driver-595-open` installed (`dkms` 3.0.11, `gcc-13`); DKMS built the five modules, 200 `CC [M]` lines in the `make.log`; the stage's unattended upgrade read "All upgrades installed".

Tooling: `run.sh`'s `dkms` job takes T0 = `20260922T170000Z`, cleans apt's cache after the state install, and measures the chroot without crossing its mounts; `pool_runs.py` checks the state's kernel and the module built for the new one.

## D52 — the DKMS build is a new entry in the spawn form: an orchestrator and its object and probe jobs at cap 8 (2026-10-02)

By 인지오's decision, D50's open item on the entry's form, read from the second dry run (run 36982322419, #107, repeat 1, `dry`, on the EPYC 7763; every check of the method held). The DKMS build is a new orchestrator and child pair in `build-orchestrator`'s spawn form (9.6 D19), with its own tables from this campaign. A `make` dispatches six-process jobs at most eight in flight. Both the object compiles and the probe compiles are carried as jobs. What the jobs leave out is stated in the entry as unmodelled, as 9.6 stated the kernel build's.

Grounds (the dry run, `analyze.py` and 9.6's job classification, `jobs_of`, applied to each hook's subtree; a job's members stop at a nested `make`):

- **The build is a parallel `make` at cap 8.** The headers' hook built the module: 12,406 processes, 221.9 s of CPU on the measured CPU in a 222.5 s span. Object jobs live: mean 7.86, max 8, eight on 92.2 % of the build's time; all jobs live: mean 8.42. The kernel image's hook ran after it: 181 processes, 0.135 s.
- **What the CPU is.** 200 object jobs, 148.3 s (67 %), 194 of them `sh`, `x86_64-linux-gnu-gcc-13`, `cc1`, `as`, `fixdep`, `rm` (the kernel build's six-process chain, 9.6 D19), 6 with `objtool` added. 1,357 probe jobs, 58.1 s (26 %): NVIDIA's `conftest` and kbuild's probes, 1,124 of them the six-process shape with `mkdir` in `fixdep`'s place. Helpers, links and the rest, 15.5 s (7 %): 841 helper jobs 2.1 s, 13 link jobs 1.6 s, outside any job 11.8 s (the `dkms` script, `zstd` compressing the modules 7.4 s, `depmod` 1.75 s). `cc1` is 189.5 s of the whole.
- **The form keeps the parallel structure.** On one lane the build is about eight runnable tasks against the code editor, not one. `cpu-batch`'s batch loop (D39) would make it one task that is always runnable (the block after a run is 0 at the median, `batch_block_us`). That suited the unattended upgrade's sequential stages, not a parallel `make`.
- **One form for the pair.** `c1-compile`'s user build is `build-orchestrator`'s spawn form (9.6 D19). With the module build in the same form, the pair differs in the job's measured values and its name: the vocabulary's "a module rebuild after a kernel update in place of the user's build" (`docs/recognition-vocabulary.md` §1).
- **Against the kernel build's tables.** Binding `build-orchestrator` with 200 jobs would carry the kernel build's per-job values for NVIDIA's module (phase decision 2) and drop the probes' 26 %.

Open, for the campaign's method: how the probe jobs and the uncovered 7 % are carried; the names and tiers; the entry ids; `c7-compile`'s structure against `c1-compile`; the list the stability rule tests.

Tooling to follow: `analyze.py` gains the job classification per hook run (`jobs_of`, a job's members stopping at a nested `make`); the compiler gains the second job kind.

## D53 — the probes are two job kinds of their own: kbuild's probes and NVIDIA's `conftest` tests (2026-10-02)

By 인지오's decision, D52's open item on the probe jobs. The entry carries three job kinds, each its own chain with its own step tables from this campaign:

- **object jobs**, the kernel build's six-process chain (`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`; 9.6 D19);
- **kbuild's probes**, six processes: `sh` → `mkdir`; `sh` → `gcc` → `cc1`, `as`; `sh` → `rm`;
- **NVIDIA's `conftest` tests**: `sh` → `sh` (`conftest.sh`) → `dirname`, `gcc` → `cc1` (→ `as`), `rm`, `sh`, `sh`. A test that compiled more than once is drawn as one test, its extra processes' CPU folded into the matching members.

The spawn table keeps the kinds in the order the build ran them.

Grounds (the second dry run, D52):

- **Two populations.** 1,124 of the 1,357 probe jobs are kbuild's six-process probe, all 400 checked in that fork order, about 10 ms a job, 11.7 s in all; median CPU per process `cc1` 4.4 ms, `gcc` 2.1, `as` 1.7, the rest under 1. The other 233 are `conftest` tests, 46.4 s in all. Their commonest trees are 95 without `as` and 80 of 82 with it; `cc1` takes 230–286 ms at the median. 33 tests compiled twice, a few three times.
- **Pooling would mix them.** One probe table over both would make `cc1` about 83 % draws near 4 ms and 17 % near 250 ms, and give the `conftest` tests kbuild's tree and names (D25).
- **When they run.** Probes start from 0.3 s, at a median of 29.9 s; object jobs from 60.9 s, at a median of 129.9 s; some probes run among the objects, up to 210.2 s.

Open, for the campaign's method: the uncovered 7 %; the names and tiers; the entry ids; `c7-compile`'s structure against `c1-compile`; the stability rule's list.

Tooling to follow: the compiler's orchestrator draws a spawn table of the three kinds in order; `analyze.py` classifies probe jobs by tree.

## D54 — the serial tail is the orchestrator's own batch loop; helper and link jobs are stated unmodelled (2026-10-02)

By 인지오's decision, D53's open item on the uncovered CPU. After its jobs have finished, the orchestrator runs the build's serial tail in the batch-loop form (`cpu-batch`'s, 9.7 D29; D39): runs between voluntary blocks and the block after each, drawn from the tail's own tables, until the tail's measured CPU is spent. The helper and link jobs, the `dkms` script's work before the `make` and the second hook run are stated in the entry as unmodelled, as 9.6 stated the kernel build's helper, archive, probe and link jobs.

Grounds (the second dry run, D52):

- **The tail is a serial phase.** After the last object and link jobs end at 212.72 s, the hook run spends 9.73 s of CPU in 9.80 s: `strip` and `zstd` compressing the five modules (7.44 s, 212.80–220.30 s), `find`, then `depmod` (1.75 s, 220.76–222.52 s), one process at a time. It is 4.4 % of the build's CPU, and a phase in which the build is one runnable process after about eight.
- **What is left unmodelled.** 841 helper jobs (2.1 s), 13 link jobs (1.6 s), the `dkms` script before the `make` (0.22 s) and the kernel image's hook run (0.135 s): about 4 s, 1.8 % of the job. The `make` processes' own CPU, 1.81 s, is the dispatch table.
- **The precedent.** 9.6 left the kernel build's 681 archive, 1,537 helper, 90 probe and 38 link jobs unmodelled, "together under 3 % of the build's CPU" (`build-orchestrator`'s `modeling_notes`).
- **D17.** The job runs whole but for that stated 1.8 %.

Open, for the campaign's method: the names and tiers; the entry ids; `c7-compile`'s structure against `c1-compile`; the stability rule's list.
