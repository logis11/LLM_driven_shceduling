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
