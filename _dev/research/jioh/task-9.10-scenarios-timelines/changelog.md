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

> Amended by D95 (the codec is H.264, CpsMark+'s own code's; the paper's "H.256" is not read as H.265).

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

## D55 — the task shows `dkms`; members carry their observed `comm`s; the entries are `module-build-orchestrator` and `module-compiler-child` (2026-10-02)

By 인지오's decision, D54's open items on the names, tiers and ids. The orchestrator task shows `dkms`, its bound child name is `cc1`, and each spawned member carries its observed `comm`: `sh`, `x86_64-linux-gn`, `cc1`, `as`, `fixdep`, `rm`, and `mkdir` and `dirname` in the probes. The archetype is `module-build-orchestrator`. It spawns `module-compiler-child`, which holds the three job kinds' tables (D53).

Grounds:

- **D24 and D25.** `/usr/sbin/dkms` (`comm` `dkms`) runs the `make` and is the parent of the serial tail (D54). The hook's own process, `dkms_autoinstaller` (`comm` `dkms_autoinstal`), only waits on it. In every job the compiler driver is `/usr/bin/x86_64-linux-gnu-gcc-13`, `comm` `x86_64-linux-gn` (the dry run; the kernel build's was `gcc`).
- **The C7 rename.** `make` would give `c7-compile` the same names as `c1-compile` (`code`, `make`, `cc1`) and drop the rename the C7 pair is built on (`docs/workload/building-plan.md` §3 C7).
- **Tiers (D27).** `dkms` keeps tier 3 and `cc1` tier 3 (`grid.py`'s `NAME_TIERS`). The grid reads a task's name and its bound child name (`segment_tier`), so the segment stays at tier 3 (`code` 1, `dkms` 3, `cc1` 3), as `c1-compile`'s, and the pair keeps its tier. The other members' names show in the spawn table and carry no tier.
- **The ids.** They mirror 9.6's `build-orchestrator` and `compiler-child`.

Open, for the campaign's method: `c7-compile`'s structure against `c1-compile`; the stability rule's list.

## D56 — `c7-compile` is its base's first C seconds, the module build from 0 s in place of the user's build (2026-10-02)

By 인지오's decision, D55's open item on `c7-compile`'s structure against `c1-compile`, D41's rule applied to the compile pair. `c7-compile` is `c1-compile`'s first C seconds: the editor `code` from 0 to C, its focus window from 2 s to C − 2 s (D44). The user's build is replaced by the DKMS build, task `dkms` on `module-build-orchestrator` (D55), arriving at 0 s and bound whole. One segment, labelled `background_wanted: false`, `initiated: scheduled`. C is the module build's CPU total as the entry carries it, its jobs, dispatch and tail (D52–D54), about 218 s from the dry run. It is set at fold-in from the job's demand as compiled under the file's seed, so the job is alive at every instant of the segment. The base is unchanged.

Grounds:

- **D41 and D44.** The ten interactive counterparts are their bases' first C seconds with the unwanted job from 0 s, bound whole, the focus window 2 s to C − 2 s. On one lane a job of C seconds of CPU is alive for at least C seconds under every policy, so the label holds at every instant.
- **In place of the user's build.** D4: `c7-compile` binds the module build "in place of the rename"; the vocabulary's compile `false` cell is "a module rebuild after a kernel update in place of the user's build" (`docs/recognition-vocabulary.md` §1).
- **Against the alternatives.** With the build arriving at 2 s, as the user's build does, the first 2 s are labelled `false` with no unwanted work. At the base's length (about 23 min once D18's 2,908-job build is bound), the file would carry the label for about 19 min with no unwanted work after the module build ends.

Hands to 9.14: the pair review and the scoring spec compare `c7-compile` with `c1-compile`'s first C seconds, as for the interactive counterparts (D41). Hands to 9.15: `building-plan.md` §3 C7 ("`compile` renames `make` to `dkms`").

## D57 — the module build's fork cap is cap × 6, 9.6 D19's rule; the `conftest` phase runs fewer jobs at once, stated (2026-10-02)

By 인지오's decision, raised by the compiler work for D53's three job kinds. `module-build-orchestrator`'s `fork_cap` is `parallelism_cap` × 6, as `build-orchestrator`'s (9.6 D19). The simulator's format is unchanged. While `conftest` tests are in flight, the cap holds fewer jobs than eight, and the entry's `modeling_notes` state it.

Grounds:

- **The cap counts tasks.** A FORK blocks while `fork_cap` children are alive (`docs/simulator/simulator-guide.md`, the spawn-table rules). A job's members are forked together and live until the job ends (9.6 D19), so cap × members bounds the jobs in flight only when every job has the same member count. Object jobs and kbuild's probes have 6 members; `conftest` tests have 8 or 10 (D53).
- **What it costs** (the second dry run; the measured job lifetimes, each job counted at its kind's member count). Live tasks exceed 48 for 40.1 s of the 210.5 s the jobs run, 19.1 %, almost all while a `conftest` test is live (57.7 s, 27.4 %). Over the build, live tasks average 49.0, against cap × 6 = 48.
- **Against the alternatives.** At cap × 10 the object phases would allow up to 13 jobs at once, overstating `-j8` for most of the build. A cap counted in jobs would change the simulator's format, shared with 인경민 and 박이안, beyond this campaign.

Tooling: `dataset/tools/wlc/compiler.py`'s module-build constructor.

## D58 — the serial tail's block per run is carried over the 26 landings with its half-width, its spread the machine's (2026-10-02)

By 인지오's decision, under the campaign workflow's exception for a value whose spread follows the machine, not the program (9.6 D29). The DKMS campaign's pool holds 26 landings: repeats 1–23, with 7, 10 and 11 landing twice, as below. It holds the stability rule on 59 of its 60 values. The 60th, the serial tail's block per run (D54), is carried over the landings obtained in place of the 5 % tolerance. Its 95 % half-width ±8.35 %, the range of its per-landing means 38.5–87.4 µs, the 26 landings, what its spread follows, and its share of the job (at most 0.06 %) are stated in `module-build-orchestrator`'s scope and `validation_stats`. No reported result rests on it.

Grounds:

- **What the blocks are.** About 1,500 blocks per landing. One of them, 32–49 ms, follows `dkms`'s progress indicator: `invoke_command` (`dkms:91–108`, S2-03) runs a backgrounded command beside a loop of `sleep 3 & wait $!; echo -en "."` and kills the loop when the command ends; the block is the wait from that `sleep` to `dkms` resuming. It is about two thirds of the mean. The rest are disk waits: `rm` and `depmod` in uninterruptible sleep, a few ms in all. Repeat 10's copy from run #111 had more of them (81 ms against 25–37 ms elsewhere); without that copy the spread is ±3.86 %.
- **Its weight.** The blocks total 57.5–130.5 ms per landing (median 63.3), at most 0.0605 % of the build's CPU. The carried CPU total holds at 224.6 s ±1.46 %.
- **Against the alternatives.** Adding repeats one at a time would take about 43 more jobs (projection 69). Reading the progress-loop block as a rare event within a run (9.5 D64) leaves repeat 10's disk waits at the tolerance's edge.

**Every landing pooled.** One push (`a6f08f7e`) started two runs, #111 (36987468347) and #112 (36987471634), each relaunching repeats 7, 10, 11 and 12. Repeat 12 landed in #112 only; 7, 10 and 11 landed in both. The campaign workflow pools every landing, keyed `<index>@<run id>` (9.8 D24). An earlier pool that kept only #111's copies, as 9.5 D66 had for a recorded-input window, is superseded. Tooling: `dataset/tools/meas/background/pool.py` keys a repeat that landed more than once per landing, as `desktop/pool.py` does.

## D59 — the DKMS campaign holds at 26 landings; `module-build-orchestrator` and `module-compiler-child` folded in, `c7-compile` rebound (2026-10-02)

The campaign of D46–D58, `meas-ci:background:2026-10-02`, run under `../measurement-campaign-workflow.md` and recorded in `campaign/dkms/` (method, machine draws, `results/pooled.json`, `results/results.md`) and in `measurement-campaign-record.md`.

- **Runs.** Two dry runs: #106, whose state held the new kernel already (D51), and #107. The first batch, repeats 1–5 (runs #108–#109, the gated index 4 relaunched once), was all valid; 37 of the 60 values failed and the pool projected 23. Repeats 6–23 were added as one batch (9.7 D26, runs #110–#114). One push started #111 and #112 together, so repeats 7, 10 and 11 landed twice; every landing is pooled (D58). 37 jobs: 26 landed on the EPYC 7763, 11 stopped by the machine gate.
- **The rule** holds over the 26 landings on 59 of the 60 values. The 56 step tables hold at ±0.67 % to ±4.13 %. Make's dispatch run is 754.3 µs ±0.72 %, the tail's run between voluntary blocks 6.151 ms ±1.82 %, the CPU total carried 224.627 s ±1.46 % (210.6–238.9 s). The tail's block per run, 44.4 µs ±8.35 %, is carried with its half-width (D58).
- **Every landing valid.** The layer built with no package missing or extra; the state was on `7.0.0-31-generic` with `nvidia/595.91.07` built for it; the stage installed the kernel `7.0.0-34` and `xdg-desktop-portal`, with the same change set in every landing, "All upgrades installed"; `nvidia/595.91.07` was installed for `7.0.0-34-generic`, its five modules present. The headers' hook built the module in every landing; the image's hook ran after it, 0.13–0.145 s.
- **Reported.** In every landing: 200 object jobs, 1,125 kbuild probes, 145 and 87 `conftest` tests. Jobs fitting their tree exactly: 194, 1,124, 95 and 82; the rest folded (D53). The carried share is 0.9818–0.9825, the unmodelled remainder 3.89–4.32 s, the tail 9.29–11.14 s, the build's hook run at 0.997 CPU over its span. The landings' job orders differ only by adjacent swaps.
- **Release.** The raw records are release `meas-ci-background-2026-10-02`, published on 인지오's go-ahead.
- **Fold-in.** `module-build-orchestrator` and `module-compiler-child` in `dataset/archetypes.yaml`, their 59 tables written by `batch_fold_in.py` from `results/pooled.json`. The orchestrator's `job_order` is landing 23's, the medoid of the 26. `tail_work` is the tail's pooled CPU, 10.028 s. Scope, stats and notes state D46–D58.
- **Rebound.** `c7-compile` (`c7.variant.yaml`, D56): `dkms` on `module-build-orchestrator` from 0 s, `parallelism_cap` 8, `child_name` `cc1`, in place of the user's build. C is 225.458 s: the build's CPU as compiled under the file's seed (225.4586 s), rounded down to the millisecond. The editor departs at C, focus runs 2 s to 223.458 s, one segment `background_wanted: false`, `initiated: scheduled`. The build compiles to 9,980 spawn-table tasks under `fork_cap` 48 (D57).

Recompiled (`compile.py --allow-window`): 2 of 100 artifacts change beyond the library's hash, `c7-compile` in both modes, demand 0.8803 → 1.1138 (calibration). Lint reports the three demand-window files of D20 and nothing else. Tests: 372 passed, 1 skipped, 1 xfailed, after `test_c7_compile_is_a_rename_only` was restated as `test_c7_compile_is_the_module_build_in_place_of_the_users_build` (D56), the batch-table count went to 89, and the background list test took the DKMS list.

Hands to 9.14: `c7-compile`'s judging term and the pair review against `c1-compile`'s first C seconds (D4, D56); the module build's `fork_cap` shortfall in the `conftest` phase as a sensitivity item (D57). Hands to 9.15: `building-plan.md` §3 C7 and the scenario catalog's S11 row (D4).

## D60 — the Tracker campaign's file set is a real user's set other than Mahoney's, chosen by a four-class search, amending D5 (2026-10-02)

By 인지오's decision, D5's candidate. The Tracker campaign does not read Mahoney's 10 GB set (`mahoney-10gb`). Its file set is another real user's file set, chosen from a search of the four classes (phase decision 4). D5's state stands: Tracker indexing a real user's file set from an empty database. 9.7's use of the set for `borg` and `7z` is unchanged.

Grounds:

- **The set's licence** (S3-61, "License"): "Please do not use this data set for any purpose other than benchmarking data compression and archiving programs and related research." It follows "Many of the files in this data set are copyrighted by other people and licensed under varying terms", and, of files hosted on the author's website, "I do not have written copies of such permissions". A desktop indexer is neither a compression nor an archiving program.
- **The set's contents** (S3-61, the contents table): 3,240 MB of the human genome in FASTA format, 1,998 MB of compression benchmarks, 1,584 MB of MinGW compilers, 1,212 MB of a website backup and 730 MB of the same site's 2011 subdirectory, 678 MB of open-source applications, 502 MB of Cygwin and a 52 MB file of zero bytes: "designed to test archivers in realistic backup scenarios".

Open: the file set, from the search; then D5's method items, its placement under the indexed directories and the job window.

No file changed yet.

## D61 — the Tracker campaign runs in D37's chroot: Tracker and its extractors as the English default install holds them (2026-10-02)

By 인지오's decision, D5's environment. Each repeat builds, on the harness CPUs, D37's chroot: the default layer of an English install, 1,445 binaries (S2-33), from the archive at a fixed time. Tracker runs in it as the layer holds it: `tracker-miner-fs` and `tracker-extract` 3.7.1-1ubuntu0.1 with the extraction stack beside them. Nothing is installed for the measurement.

Grounds:

- **The layer holds the indexer and its extractors** (S2-41): `tracker`, `tracker-extract` and `tracker-miner-fs` 3.7.1; `gstreamer1.0-plugins-base` and `gstreamer1.0-plugins-good` 1.24.2; `libpoppler-glib8t64` 24.02; `libgsf-1-114`, `libexif12`, `libgexiv2-2` and `libtotem-plparser18`.
- **The plugins are not dependencies.** `tracker-extract` depends on GStreamer's libraries and on no plugin package, and has no `Recommends:` (S2-41). Its media extractor reads a file through GStreamer's discoverer (`tracker-extract-gstreamer.c:1178`, S2-41), so which media files it reads follows the plugins installed.
- **D37's ground holds.** The snapshot fixes the state; the runner's own installed set is its weekly image's and cannot hold it.
- **The settings are the shipped ones.** `ubuntu-settings` 24.04.6 overrides nothing of Tracker's (S2-41).

How the miner runs in the chroot — its session bus, its view of `/proc`, its inotify limit — is the tooling's, checked at the dry run.

Open: the archive time; the file set (D60); its placement under the indexed directories; the job window.

No file changed yet.

## D62 — the Tracker job ends at the extractor's "Extraction finished", amending 9.6 D16's end for this campaign (2026-10-02)

By 인지오's decision, D5's job window, its end. The measured job ends when the extractor logs "Extraction finished": every file of the set crawled and its metadata extracted. The miner's `Idle`, 9.6 D16's end, falls inside the job. The extractor's 10 s wait before it exits is outside.

Grounds:

- **`Idle` ends the crawl, not extraction** (S2-42). `process_stop` sets the status `Idle` once crawling is done; beside the exit taken there, the source reads "FIXME: wait for extractor to finish".
- **Extraction is work of both processes** (S2-42). The extractor is the miner's subprocess, started with `--socket-fd 3`, and writes through an endpoint the miner serves on its own connection.
- **The extractor marks its end** (S2-42): "Extraction finished in %s" when its queue empties; off a terminal it exits after "10 seconds inactivity".
- **9.6's window left some out.** On the kernel's `Documentation` tree, 0.34–0.41 s of CPU followed the miner's `Idle`, against 4.78–4.94 s in the job (9.6 D16).

Open: the job's start (the shipped 15 s initial sleep); the archive time (D61); the file set (D60); its placement under the indexed directories.

No file changed yet.

## D63 — the Tracker job starts at the miner's first schedule-in, the shipped 15 s initial sleep kept (2026-10-02)

By 인지오's decision, D5's job window, its start. The measured job starts at the miner's first schedule-in. It holds the miner's start-up — its `SCHED_IDLE` priority, the database created from the ontology, the graphs — then the shipped initial sleep of 15 s, the crawl, and extraction up to D62's end. `initial-sleep` keeps its shipped value; 9.6's override to 0 is not carried.

Grounds:

- **An empty database takes the sleep** (S2-43). The miner skips the initial sleep only when no mtime check is needed, and it needs one when the clean-shutdown marker `no-need-mtime-check.txt` is absent from its cache directory, as it is on an empty database. The crawl starts once the sleep and the graphs are both done.
- **Both labels start the same way** (S2-43). `tracker3 reset --filesystem` kills the miner with SIGKILL and empties `~/.cache/tracker3/files/`, the marker with it; the unit does not restart after a SIGKILL. The next start finds an empty database and no marker, as a first login does (D5).
- **The settings are the shipped ones** (D61; S2-41: `initial-sleep` 15).

How the sleep appears in the entry or the timeline — a block within the job or the job's offset — is a form question after the dry run.

Open: the archive time (D61); the file set (D60); its placement under the indexed directories.

No file changed yet.

## D64 — the Tracker campaign's chroot is the archive at 2026-09-22T17:00Z, the DKMS campaign's state (2026-10-02)

By 인지오's decision, D61's archive time. Each repeat builds D37's chroot from the archive at 2026-09-22T17:00Z (D51), the time the DKMS campaign's state was built from.

Grounds:

- **Tracker is the same at every candidate time** (S2-44): `tracker-miners` and `tracker` have no publication since 2026-06-01, so the layer holds `tracker-miner-fs` and `tracker-extract` 3.7.1-1ubuntu0.1 at 2026-07-27, at 2026-09-22 and at 2026-10-02.
- **What the time changes is five libraries' security updates** (S2-44). At 2026-09-22T17:00Z the layer holds `gst-plugins-good1.0` 1.24.2-1ubuntu1.7, `gst-plugins-base1.0` 1.24.2-1ubuntu0.5, `glib2.0` 2.80.0-6ubuntu3.9, `libxml2` 2.9.14+dfsg-1.3ubuntu3.9 and `sqlite3` 3.45.1-1ubuntu2.8; a time after 2026-10-01T17:38Z adds `gst-plugins-good1.0` 1.24.2-1ubuntu1.8.
- **The tooling has built this state** in every one of the DKMS campaign's 26 landings (D59); the DKMS and Tracker campaigns run on one layer.

Open: the file set (D60); its placement under the indexed directories.

No file changed yet.

## D65 — the Tracker job is every process in the miner's tree (2026-10-02)

By 인지오's decision, D5's job, its processes: the miner, the extractor it starts, and every process either starts, such as GStreamer's registry scanner. The session bus's `dbus-daemon` is outside, as in 9.6.

Grounds:

- **D50's rule:** the job is every process under the event's own start.
- **The extractor is the miner's subprocess** and writes through the miner over a peer-to-peer connection, not the session bus (S2-42).
- **9.6's program** was the miner, the extractor and the miner's `gst-plugin-scan` child (9.6 D16).
- **The registry scan is the first index's work.** GStreamer forks at startup to update its plugin registry, a cache in the user's home (S2-45); a new home has none.

Read at the dry run: the registry scan's CPU in D61's layer, which holds the base and good plugin sets. The scan runs on a new home's first index and not after `tracker3 reset --filesystem`, which empties only `~/.cache/tracker3/files/` (S2-43). If its CPU matters, the two labels' difference is a form question.

No file changed yet.

## D66 — the Tracker campaign indexes a HippoCamp profile; D5's "a real user's file set" restated, amending D5 and D60 (2026-10-02)

By 인지오's decision, D60's search. No real person's own home directory with real content is reachable under terms that allow the measurement (S3-62–S3-77). The file set is a profile of HippoCamp (S3-76): a home-like file system its authors aggregated from participants' files, public benchmark documents and synthetic content. D5's state is restated: Tracker indexing a home-like file set from an empty database. The entry's scope states what the set is, its file count, and that no source grounds its count as a home's.

Grounds:

- **The search** (S3, "T5 — a file set for the indexer's first index"): the four classes of phase decision 4; the Real Data Corpus "is no longer available" (S3-66); the L3S desktop set was not released (S3-73); UMass's collections are internal-use by request (S3-72); real-machine studies publish metadata or hashes only; a runner holds no user's files.
- **What HippoCamp is** (S3-76): "derived from interviews with 100+ participants"; the participants' files aggregated "into coherent archetypal profiles by matching file-type/modality distributions and high-level organizational patterns"; "rather than a verbatim dump of a single person's machine"; privacy-relevant content "synthetically generated"; folders carrying public benchmark sets (`caud`, `maud`, `contractnli` in Adam's tree, `financebench` in Victoria's).
- **Its terms** (S3-76): the licence permits "non-commercial research" and "benchmarking and evaluation of … retrieval systems"; it forbids publicly mirroring the raw files, and allows "aggregate statistics … provided they do not enable reconstruction or redistribution of the raw-file release". The campaign's release carries the measurement's records, not the files.
- **The other candidates** (S3-67, S3-70): the Enron attachments are one real person's documents from a mailbox, not a home; M57-Patents' homes were filled by actors in a scripted scenario.

Hands to the entry's scope at fold-in: a profile's few hundred files are HippoCamp's; a home's file count needs its own source — Dinneen, Julien & Frissen, "The scale and structure of personal file collections" (CHI 2019), to be verified against its primary text and entered in `docs/references.md` if the scope states a count. At fold-in, `docs/references.md` gains a `hippocamp` entry under its citation rule.

Open: which profile; its placement under the indexed directories.

No file changed yet.

## D67 — the indexed profile is HippoCamp's Bei (2026-10-02)

By 인지오's decision, D66's open item. The campaign indexes the `bei_fullset` tree of HippoCamp (`Bei/Fullset/Bei/`): 875 files, 40.66 GB, 76 directories, 42 top folders and 61 loose files, up to 7 levels deep (S3-76, reader's own).

Grounds (S3-76):

- **No public benchmark set inside.** Bei's folders are topical (`Mount Fuji`, `Cat-Vlog`, `study music`, `IELTS`, `Receipts`, …); Adam's tree holds `caud`, `maud` and `contractnli` (83 of 344 files) and Victoria's `financebench` (368 of 711).
- **Every extractor family.** mp4 157, jpg and jpeg 265, pdf 123, mp3 86, docx 68, png 61, txt 27: GStreamer's media extractors, the image, PDF, Office and text extractors; Adam's and Victoria's are mostly PDF.
- **The persona.** "a student and content-creator" (paper, page 5); the core set's media timelines are design (D2), so this is a fit, not a ground.

Checked at the dry run: the 40.66 GB download per repeat under the tooling's work root.

Open: the tree's placement under the indexed directories.

No file changed yet.

## D68 — Bei's tree is `~/Documents`, the other folders empty (2026-10-02)

By 인지오's decision, D5's last method item. The tree `Bei/Fullset/Bei/` as released — its 42 folders and 61 loose files — is the content of `~/Documents`; Desktop, Downloads, Music, Pictures, Videos, Public and Templates exist and are empty. Design: HippoCamp does not place a profile in a home.

Grounds:

- **Every file is indexed** (D62's job): `~/Documents` is one of the miner's recursive roots (S2-41), and no path of the tree matches the shipped `ignored-files`, `ignored-directories` or `ignored-directories-with-content`, nor is hidden (reader's own, over `hf-hippocamp-api.json`, S3-76).
- **HippoCamp's layout as released.** Splitting the topical folders into Pictures, Music and Videos would sort them by a judgement no source gives; Tracker treats a file alike in any recursive root.
- **The tree as the home** would leave 813 of the 875 files under `$HOME`, which the miner reads one level deep (S2-41): 61 loose files and one in the tree's own `Documents` would be indexed.
- **The folders exist.** The default layer holds `xdg-user-dirs` 0.18 (S2-01), which creates them at first login.

The method is complete: `campaign/tracker/method.md`.

No file changed yet.

## D69 — the Tracker job's end read from the extractor's status, the per-file debug output dropped, amending D62's reading (2026-10-02)

By 인지오's decision, on dry run 2 (run 37002910488, #119). The session runs the miner with `TRACKER_DEBUG=status` only; `G_MESSAGES_DEBUG` is not set. D62's end — the moment the extractor logs "Extraction finished" — is read as the extractor's last status change to `Idle` after `Extracting metadata`, which the status trace logs in the same millisecond.

Grounds (dry run 2's log, `tracker.log`):

- **The debug output is the measured processes' own work.** Of 13,399 lines, 13,215 are `Tracker-DEBUG` lines written per file by the miner and the extractor on the measured CPU ("[v24] Processing frame …" 883, "Parsing … XML file" 847, "MIME type guessed as …" 378); a stock desktop writes none.
- **The status trace marks the same moment.** `(Miner:'TrackerExtractDecorator') set property:'status' to 'Idle'` at 12:04:04.787, .794 and .795, each in the millisecond of an "Extraction finished"; 113 lines in all (43 status, the rest progress), the initial sleep shown as the miner's `Idle` then `Initializing` 15 s later, each extractor start as `Extracting metadata`. Warnings print without any debug setting.
- **The perf rows alone give no clean end.** Around it the miner and the extractor exchange some forty runs within 4 ms, and their threads run again inside the extractor's final 10 s.

Method §8 carries the amendment; a third dry run checks it.

No file changed yet.

## D70 — the Tracker index is a new entry in the batch-loop form; `cpu-batch`'s `tracker` tables leave at fold-in (2026-10-02)

By 인지오's decision, D5's open item on the entry: the index is a new archetype with `cpu-batch`'s batch-loop constructor (9.7 D29), as D39 made `package-upgrade` — one task; a run drawn from the tree's runs between voluntary blocks, pooled over every process of the miner's tree (D65), then the block that followed it, the tree's own off-CPU time, zero when another of its processes runs on or is runnable — until the job's CPU is spent. The CPU total is the measured whole (D17) and is carried. The tree's structure — the miner, the extractor runs, the deadline exits and the registry scan — is stated in `modeling_notes`. Once the three indexing files rebind to it, no file binds `cpu-batch`'s `tracker` tables; they leave at fold-in, with the `tracker` figures of `cpu-batch`'s `validation_stats` and `modeling_notes`.

Grounds (dry run 3, run 37010496980, #121):

- **The job does not meet `cpu-batch`'s sharing criterion** (9.6 D7: "runnable for the whole of its lifetime on one dominant thread; a program showing a distinct shape … gets its own entry"): saturation 0.659 over the job (the initial sleep one 14.9 s block), 0.891 from the miner's `Initializing`; three extractor processes in turn, two ended by the 5 s deadline, each restart after the miner's 1 s grace; the dominant thread (the extractor's `single`) 0.553 of the CPU. `cpu-batch`'s programs run at 0.925–0.9998 over their jobs (its `validation_stats`).
- **The library's precedent:** `package-upgrade` (D39), `file-backup`, `file-archiver` and `game-download` carry the batch-loop form in entries of their own.
- **D6 holds:** `c2-p1b`'s indexer carries the measured indexer's own tables, now this entry's.

Open: how the initial sleep appears (D63); the deadline exits; the registry scan between the two labels (D65); the entry's id and the name its task shows.

No file changed yet.

## D71 — the initial sleep is the task's arrival: the entry's block table leaves out its one block (2026-10-02)

By 인지오's decision, D63's open item. The entry carries the job without the initial sleep: its block table leaves out the one block that spans the miner's `Initializing` (the shipped 15 s sleep); the start-up's runs stay in the run table and the CPU total stays whole. The scope states that the shipped 15 s initial sleep precedes the work, so a file's arrival time reads as the end of that sleep.

Grounds (dry run 3, run 37010496980, #121; `wlc/compiler.py`):

- **The job's order.** A start-up of 0.335 s of CPU in its first 1.03 s (the database created, the registry scan), one block of 14.9 s, then the crawl and extraction: 39.09 s of CPU in 43.87 s.
- **The batch loop cannot hold the sleep in place.** It draws each run and each block independently until the CPU total is spent (`_batch_ops`, `compiler.py:408`); the 14.9 s block is one of 17,944 and 74 % of all block time — the mean block per run 1,122 µs with it, 292 µs without.
- **The batch-loop constructor runs its loop only** (`_batch_loop`, `compiler.py:386`): a fixed step before it would be a compiler, schema, lint and test change for the order of a 0.335 s burst, 0.85 % of the CPU.
- **The arrival is already design.** The indexing files place the indexer's arrival as a calibration size (D31; `c1-indexing` `arrive: 2s`), and no file shows the login or the reset.

Tooling: `analyze.py` leaves the block out of `batch_block_us` and reports it as `initial_sleep_block_us`.

No file changed yet.

## D72 — the extractor's deadline exits are carried as observed (2026-10-02)

By 인지오's decision. The two extractions the extractor's stock deadline ends, and the restarts after them, stay in the entry's run and block tables and in its CPU total. The scope states the 5 s per-file deadline, the exits and restarts, and the files skipped, as the outcome on the EPYC 7763's core; whether they recur in every repeat is read from the pool, the CPU total's stability showing any repeat that differs.

Grounds:

- **The deadline is shipped behaviour** (S2-04; D61): `DEFAULT_DEADLINE_SECONDS 5` (`tracker-extract.c:46`); past it the extractor logs "took too long to process. Shutting down everything" and calls `_exit (EXIT_FAILURE)` (`:332–341`); `TRACKER_EXTRACT_DEADLINE` alone overrides it. The miner restarts the extractor after its 1 s grace (`tracker-miner-files.c:244–245`); the new extractor skips the file ("failed in previous execution, ignoring") and Tracker records it ("Crash/hang handling file").
- **On the runner it ends the same two files** in dry runs 2 and 3: `Book/TenYearsInJapan.pdf` and `Book/IslandOfBali.pdf`. In dry run 3 the two ended extractor processes ran 5.50 s and 4.92 s, 10.4 s of the job's 39.4 s; each restart adds a 0.98 s block and a process's start-up.
- **Not taken:** removing them describes a job that did not run on this machine; raising the deadline changes the depicted state and leaves the two books' whole extraction unmeasured. The deadline is wall-clock, so a faster or busier core can end more or fewer files; no source gives these files' extraction time elsewhere.

No file changed yet.

## D73 — the GStreamer registry scan stays in the one entry both labels bind (2026-10-02)

By 인지오's decision, D65's open item. The registry scan stays in the entry's tables and CPU total; both labels bind the one entry (D5). The scope states its CPU as first-login work that a reset may not repeat.

Grounds:

- **Its weight:** the miner's `gst-plugin-scanner` child ran 94 ms and 93 ms in dry runs 2 and 3, about 0.24 % of the job's 39.4 s (69 ms on dry run 1's empty home), inside the stability rule's 5 % tolerance.
- **When it runs:** GStreamer forks at startup to update its plugin registry, a cache in the user's home (S2-45); the campaign's home is new, as a first login's is. `tracker3 reset --filesystem` empties only `~/.cache/tracker3/files/` (S2-43), so the registry outlives a reset; whether GStreamer then forks the scanner was not observed.
- **Not taken:** a second table set for the asked side, made by taking one process out of the pool, carries a state not observed.

No file changed yet.

## D74 — the task shows `tracker-miner-f`; the entry is `file-indexer` (2026-10-02)

By 인지오's decision, the last open item of the form: the one task of D70's form shows `tracker-miner-f`, the `comm` of `/usr/libexec/tracker-miner-fs-3` as the dry runs observed it (the kernel's 15-byte rule, D25), and the archetype's id is `file-indexer`.

Grounds:

- **D40's rule:** the task shows the program the unit runs, alive across the job and the parent of the rest — the miner is the user unit's `ExecStart` (S2-41), alive from the job's start to its end, the parent of every extractor and of the registry scanner.
- **The other observed name:** `tracker-extract` runs 96 % of the job's CPU (37.82 s of 39.43 s, dry run 3) as the miner's subprocess, started three times within the job; it is the work under the name, as `localedef` was under `unattended-upgr`.
- **The files and the tier:** the three indexing files already show `tracker-miner-f`, tier 3 by D27's rule.
- **The id names the role,** beside `file-backup` and `file-archiver`.

The entry's `modeling_notes` state that the name stands for the miner's tree and that most of its CPU is the extractor's.

The form is complete: the campaign's list is fixed in method §8.

No file changed yet.

## D75 — the index starts cold: the page cache dropped before the phase, its fraction recorded; the first batch is not pooled (2026-10-03)

By 인지오's decision, on the first batch (runs #122–#125, repeats 1–5, six landings, every one valid). Before the phase, `sync; sysctl vm.drop_caches=3`, which drops the clean page cache (9.7 D8, S4-24); the set's cached fraction is measured with `fincore` and recorded, so the state is verified, not assumed. The first batch ran in an uncontrolled state and is not pooled; the campaign's repeats are the cold ones, from the next batch.

Grounds (the first batch's pool, `background-tracker-from122`):

- **The rule fails on one value, from the cache.** The run between voluntary blocks holds at ±1.66 % and the CPU total at ±0.58 %; the block per run (254.7 µs) is at ±14.5 %, projecting 32 repeats. Every landing carries the same two restart graces (1.95 s) and 1.3–2.0 s of blocks under 10 ms; the blocks of 10 ms to 0.5 s run from 3 (0.43 s) in repeat 2 to 31 (2.08 s) in repeat 5, and they are disk waits — waits of 10 ms or more 0 s in repeats 2 and 3, 0.13–1.63 s in the others.
- **The state was the download's.** The runner has 16.4 GB of memory (`spec.json`), the set is 40.7 GB fetched by eight threads just before the index: at most some 40 % of it can sit in the page cache, which part following the download's order.
- **A cold start is the unasked side's state:** the first index at a first login, after a boot (D5).
- **Warm is not available:** the set is 2.5 times the runner's memory.

The disk waits then follow the runner's disk; if the block per run still spreads, the stability rule's exception for a value whose spread follows the machine is 인지오's call (9.6 D29, D58).

No file changed yet.

## D76 — the Tracker campaign is `meas-ci:background:2026-10-02b` (2026-10-03)

By 인지오's decision. The campaign's tag is `meas-ci:background:2026-10-02b` and its raw records are release `meas-ci-background-2026-10-02b`. The `meas-ci` locator's campaign gains a letter for a second campaign of the same workflow launched on one date (`YYYY-MM-DDb`): `docs/references.md`'s id-minting rule and `meas-ci` entry, and `dataset/sources.yaml`'s `meas-ci.locator_pattern` (`\d{4}-\d{2}-\d{2}[a-z]?`).

Grounds:

- **The rule's date** (9.5 D27; method §1): the campaign is the launch date of its first batch — 2026-10-02, the first batch (#122, 13:32Z) and the first pooled batch (#130, 23:26Z) alike.
- **The date is taken:** `meas-ci:background:2026-10-02` is the DKMS campaign's (D59), 60 uses in the dataset, release `meas-ci-background-2026-10-02` published; each tag resolves to one release, a campaign's raw records being one (9.6 D18).
- **Not taken:** the app in the workflow field names something that is not a workflow; the next date is not the launch date; one tag for two campaigns breaks one campaign per release.

Method §1's tag line reads the campaign's tag.

No file changed yet.

## D77 — the Tracker campaign's raw records are release `meas-ci-background-2026-10-02b`, the records naming the set's paths included (2026-10-03)

By 인지오's decision, method §7's open item and the release's go-ahead. The release is created at the fold-in commit and holds, each archive without its `pool-cache/`: the 18 pooled landings (runs #130–#140), the three dry runs (#118, #119, #121), the twelve landings of the first and cold batches that were not pooled (#122–#129; D75 and method §8 rest on them), and the reports of the 24 jobs the machine gate stopped. The records that name the set's paths are included: `tracker.set.tsv` (the 875 paths, sizes and SHA-256 hashes), `tracker.log` and `tracker.status.txt` (the deadline exits' and the ten failures' URIs), and dry run 2's debug log (per-file lines naming URIs, extractor modules and MIME types). No file of the set is released.

Grounds:

- **HippoCamp's licence** (S3-76): §4 forbids publicly mirroring "the raw-file release or a substantially similar copy of it"; §5 allows "aggregate statistics … and limited excerpts reasonably necessary for scientific discussion, provided they do not enable reconstruction or redistribution of the raw-file release". Paths, sizes and hashes enable neither; the paths are in HippoCamp's own ungated listing (`hf-hippocamp-api.json`).
- **The records show what the numbers rest on:** which set, verified file by file, and which files the deadline ended and Tracker recorded as failures.
- **The precedent:** the DKMS release held its dry runs, every landing and the gated reports (D59).

No file changed yet.

## D78 — `c1-indexing` binds the index whole at its length; `c7-indexing` is its first C seconds, the index from 0 s (2026-10-03)

By 인지오's decision, D56's form for the indexing pair. `c1-indexing` keeps its 60 s segment and its 2 s arrival and binds `file-indexer` whole, `total_work` C, the task shown `tracker-miner-f` (D70, D74): the job ends inside the segment under every policy, so the `true` cell's turnaround term reads a finished job. `c7-indexing` becomes `c1-indexing`'s first C seconds: the editor `code` from 0 to C, its focus window 2 s to C − 2 s (D44), `file-indexer` arriving at 0 s and bound whole, one segment labelled `background_wanted: false`. C is the index's CPU total as the entry carries it, set at fold-in from the job's demand as compiled under the file's seed, so the job is alive at every instant of the segment (D56).

Grounds:

- **D41 and D56:** a C7 counterpart is its base's first C seconds, the unwanted job from 0 s, bound whole, so the label holds at every instant; the base keeps its own structure.
- **The base still finishes the job.** `c1-indexing` runs at 0.59 of the lane today with a 30 s job (`build.manifest.json`), the editor about 0.09; the index alone needs about 44 s (39.4 s of CPU and 4.8 s of its own blocks), so arriving at 2 s it ends by about 52 s under any policy, inside 60 s, the lane about 0.75.
- **A flip alone would not hold the label:** `c7-indexing` as `c1-indexing` relabelled carries `false` for its first 2 s and some 8 s at its end with no unwanted work.
- **D5 holds:** both files carry the same job under the same name and entry; the work they depict differs by intent alone.

Open: `c7-indexing`'s `initiated`, a first login and not a schedule (D5); `c2-p1b`'s segment 1.

No file changed yet.

## D79 — `c7-indexing`'s segment says `initiated: session` (2026-10-03)

By 인지오's decision, D5's restatement. The descriptive key `initiated` gains a third value, `session`: work the desktop session itself starts, unasked, at login. `c7-indexing`'s segment carries it in place of `scheduled`; `scheduled` keeps meaning a timer's job in every file that carries it.

Grounds:

- **The key** (`docs/recognition-vocabulary.md:50`): `initiated` (`user` | `scheduled`), a descriptive key "used for grading splits and failure analysis only", not the recognizer's output and not checked by the linter.
- **The job is not a schedule** (D5): Tracker 3.7.1 schedules no rescan (`crawling-interval` -1, S2-41); the user unit starts with the GNOME session (`WantedBy=gnome-session.target`, S2-41), and an empty database makes that start a full index (S2-43).
- **The other files:** `c1-indexing` says `user` (the reset); every other `scheduled` in the core set is a timer's job.

Hands to 9.15: `docs/recognition-vocabulary.md`'s list of `initiated` values gains `session`, with D5's item on its example "an indexer's scheduled rescan".

No file changed yet.

## D80 — pair P1's segment 1 is as long as the index's CPU total in both files (2026-10-03)

By 인지오's decision, D42's form for pair P1. `c2-p1b`'s segment 1 carries `file-indexer`, arriving at 60 s and bound whole, the task shown `tracker-miner-f` (D6, D70, D74), and is C seconds long — C the index's CPU total, as D78 — so the file is 60 s plus C. `c2-p1a`'s segment 1 takes the same length, so the pair still shares segment 0 and differs only in segment 1's job and label. `c2-p1a`'s `python3` keeps its binding until D12's item; with 130 s of CPU it is alive throughout a segment of C.

Grounds:

- **The label at every instant** (D41, D42): on one lane the index, C seconds of CPU, is alive for at least C seconds under every policy; in the 120 s segment it ends by about 110 s and `false` would hold some 70 s with no unwanted work.
- **One diff per pair** (`docs/workload/building-plan.md` §3, "Counts and reuse"): C2 pairs share all but one segment; equal lengths keep the editor's terms read over equal windows.
- **D6 applied:** P1b's indexer carries the measured indexer's own tables, in place of `python3`'s under a rename.

Hands to D12's item: P1's segment 1 is read again against both jobs when `python3`'s measured job lands. Hands to 9.14: P1's terms on the new length, and the pair review that argued on P1's identical behaviour (D6).

No file changed yet.

## D81 — the Tracker campaign holds at 18 repeats; `file-indexer` folded in, the three indexing files rebound (2026-10-03)

The campaign of D60–D80, `meas-ci:background:2026-10-02b`, run under `../measurement-campaign-workflow.md` and recorded in `campaign/tracker/` (method, machine draws, `results/pooled.json`, `results/results.md`) and in `measurement-campaign-record.md`.

- **Runs.** Three dry runs (#118, the set's fetch refused and the home empty; #119, the per-file debug output dropped after it, D69; #121). A first batch, repeats 1–5 (#122–#125), ran with the page cache as the download left it: every landing valid, the block per run at ±14.5 %, its spread disk waits; it is not pooled (D75). A cold batch (#126–#129) is not pooled either, its cached fraction unrecorded (method §8). The campaign's first batch, repeats 1–5 (#130–#132), every one valid and cold: the rule held on the run between voluntary blocks and the CPU total, not on the block per run (±12.08 %), whose spread was the cold start's some 14,000 disk waits a landing; the pool projected 18 and repeats 6–18 were added as one batch (9.7 D26, #133–#140). 38 jobs: 18 landed on the EPYC 7763, 20 stopped by the machine gate.
- **The rule holds at 18** on the three values of the list: the run between voluntary blocks 1.876 ms ±1.12 %, the block per run 227.0 µs ±3.58 % (the initial sleep left out, D71), the CPU total 39.435 s ±0.28 % (39.10–40.07 s). Every repeat valid: the layer built with no package missing or extra; the set whole, each file checked by its SHA-256; the cached fraction 0.0000; the initial sleep 14.91–15.73 s; "Currently indexed: 875 files, 92 folders"; ten failures recorded.
- **Reported.** Five processes in every repeat; the extractor 37.47–38.35 s of CPU, the miner 1.53–1.62 s, the registry scan 93–106 ms; the job 58.3–60.3 s; saturation 0.655–0.676 over the job, 0.891–0.919 from the miner's `Initializing`; in every repeat the deadline ended `Book/TenYearsInJapan.pdf` and `Book/IslandOfBali.pdf` (D72).
- **Release.** The raw records are release `meas-ci-background-2026-10-02b`, published on 인지오's go-ahead (D77). D77's count is corrected: the gated reports are 32 jobs — the campaign's 20 and 12 from the dry runs and the unpooled batches — not 24.
- **Fold-in.** `file-indexer` in `dataset/archetypes.yaml`, its two tables written by `batch_fold_in.py` from `results/pooled.json`; scope, stats and notes state D60–D80. `cpu-batch`'s `tracker` tables leave with its `tracker` figures, and its scope and notes read four programs (D70); `batch_fold_in.py` drops the set. `docs/references.md` gains `hippocamp` (deployed-system, verified).
- **Rebound.** `c1-indexing`: `tracker-miner-f` on `file-indexer` from 2 s, `total_work` 39.435 s, the 60 s segment kept (D78). `c7-indexing` (`c7.variant.yaml`): `c1-indexing`'s first C seconds, the index from 0 s, the editor departing at C, focus 2 s to 37.435 s, one segment `background_wanted: false`, `initiated: session` (D78, D79). Pair P1: `c2-p1b` (`c2-pairs.variant.yaml`) binds `file-indexer` whole from 60 s in place of the rename, segment 1 39.435 s long in both files, `c2-p1a`'s `python3` keeping its binding until D12 (D80). C is 39.435 s: `total_work`, which the batch loop compiles exactly.

Recompiled (`compile.py --allow-window`): 8 of 100 artifacts change beyond the library's hash, the four files in both modes. Demand (`-single`): `c1-indexing` 0.5905 → 0.7477, `c7-indexing` 0.5905 → 1.1016 (both calibration), `c2-p1a` 1.1509 → 1.8346, `c2-p1b` 1.1509 → 0.9238. Lint reports five demand-window files: the three of D20 and now `c2-p1a` and `c2-p1b`, P1's segment 1 at the index's length (D17's hand-off to 9.14: the demand window re-read on the new lengths). Tests: 375 passed, 1 skipped, 1 xfailed, after `test_p1_pair_rename_only` was restated as `test_p1_pair_differs_in_segment_one_only` (D80), indexing left `C7_SAME_NAME` for `test_c7_indexing_is_its_bases_first_c_seconds` (D78), and the fold-in test names `file-indexer.tracker_block` (D70).

Hands to D12's item: P1's segment 1 read again against both jobs. Hands to 9.14: `c7-indexing`'s and P1's terms on the new lengths; the pair review and prior-table rows that argued on P1's identical behaviour (D6); `c2-p1a` and `c2-p1b` in the demand window. Hands to 9.15: `building-plan.md` §3 C2 ("behaviorally identical CPU saturation") and C7, the scenario catalog's S14 row and note 2, `docs/recognition-vocabulary.md`'s `initiated` values and its example "an indexer's scheduled rescan" (D5, D6, D79).

## D82 — the MNIST campaign's state: D37's chroot at D64's T0, `python3-venv` added, `torch` 2.14.0 and `torchvision` 0.29.0 by PyTorch's own command (2026-10-03)

Taken under 인지오's delegation (2026-10-03), D12's open item "the dataset's placement" and the state it needs. The campaign runs in D37's chroot of the English default install, built from the archive at D64's T0 (2026-09-22T17:00Z), with `python3-venv` added from the same snapshot. A user with a home, as the Tracker campaign's (D68). In that home, a venv into which `pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu` installs `torch` 2.14.0 and `torchvision` 0.29.0, the two versions pinned. The example's three files, `pytorch/examples` at `acc295d` (`mnist/main.py`, `README.md`, `requirements.txt`), as `~/examples/mnist`, each checked by its SHA-256 (S2-31).

Grounds:

- **One state across 9.10's campaigns.** The upgrade, DKMS and Tracker campaigns ran in this chroot (D37, D49, D61), the last two at this T0 (D51, D64).
- **The release current at T0.** `torch` 2.14.0 and `torchvision` 0.29.0 were uploaded on 2026-09-02, and 2.14.1 and 0.29.1 on 2026-09-30, after T0 (S2-48). Both have CPU wheels for CPython 3.12, the default layer's Python. 9.6's stand-in ran a 2.14 CPU build (`cpu-batch` scope).
- **The project's own command.** PyTorch's install matrix gives `pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu` for Linux, pip and no accelerator (S2-47). The example's `requirements.txt` names `torch` and `torchvision` unversioned (S2-31).
- **What the default layer lacks.** It holds `python3.12` but neither `python3-pip` nor `python3-venv` (`dataset/tools/meas/background/upgrade-layer.txt`). `python3-venv` is the archive's package for `python3 -m venv`; the packages it adds to the layer are recorded per repeat (`upgrade.layer.extra`).
- **What pip resolves beside the pair.** The dependencies come from the CPU index at the job's date. The installed set (`pip3 freeze --all`) is recorded and must be one set across the pooled repeats.

No file changed yet.

## D83 — the dataset is placed by the example's own download in an unmeasured start; the measured run starts warm (2026-10-03)

Taken under 인지오's delegation (2026-10-03), D12's open item. Before the phase, the example runs once unmeasured on the harness CPUs as `python main.py --dry-run --epochs 1`: its own "quickly check a single pass", one training batch and one test pass. Its `datasets.MNIST('../data', train=True, download=True, …)` downloads the four MNIST files into `~/examples/data/MNIST/raw`, the example's own path, and the start pages `torch`'s files into the page cache. The measured run then finds the files and downloads nothing. Before the phase, the uncompressed files' cached fraction is measured with `fincore`, and validity asks at least 0.99. The fraction of `torch`'s and `torchvision`'s shared libraries is recorded beside it.

Grounds:

- **What the example reads** (S2-31 `main.py:120–123`; S2-49). `torchvision` downloads the four files once into `<root>/MNIST/raw`. A later start finds them by existence alone, downloads nothing, and reads each uncompressed file whole into memory. A run on a machine where the example has run reads local files. The download is network work, once per machine, ahead of any training.
- **A warm start, 9.6 D28's ground.** The batch-loop compiler draws each run and each block independently (9.6 D21; `wlc/compiler.py` `_batch_ops`), so the start's page-ins would be spread over the whole simulated job. 9.6's cold `python3` start put 3,852 of its 3,900 sleeps in the first 3.3–3.6 s (9.6 D28).
- **The cache state decided and checked before the first batch.** The Tracker campaign's first batch ran in the state the download left; its block per run spread with disk waits and was not pooled (D75).

No file changed yet.

## D84 — the measured job is `python main.py --save-model` at the example's defaults, as the user, the venv activated; the job is the tree from its first schedule-in to its exit (2026-10-03)

Taken under 인지오's delegation (2026-10-03), D12's run. The phase runs `python main.py --save-model` in `~/examples/mnist`, as the user in the chroot, with the venv activated: its `bin` first on `PATH` and `VIRTUAL_ENV` set, as its `bin/activate` sets them (recorded from each job). `taskset` places the command on the measured CPU. Every other argument is the example's default: 14 epochs of batch 64, a test pass of batch 1,000 after each, Adadelta at 1.0 with a step decay of 0.7, seed 1, no data-loader workers and no shuffle on the CPU (S2-31 `main.py:75–114`). The job is every process of the tree `taskset` launched into `chroot`, from its first schedule-in on the measured CPU to its exit, the checkpoint written. The phase has no cap of its own; the workflow's job limit is 330 minutes.

Grounds:

- **D12:** the example at its defaults, the checkpoint written (`--save-model`), on the CPU in one process.
- **The README's command** is `python main.py` (S2-31 `README.md:1–5`). A venv's `bin` holds `python`, so the process's `comm` is the name executed. The name the files show follows the observed `comm` at fold-in (D25).
- **Identical work in every repeat.** The seed is fixed and the input is the same four files, so an added repeat is the next index (the campaign workflow, "What a repeat is").
- **One CPU,** as every campaign (9.5 D21). What `torch` sees under the pin — its intra-op and inter-op thread counts and its parallel backend — is recorded from a probe on the measured CPU before the phase.

The entry's form — `cpu-batch`'s `python3` tables re-measured, or an entry of its own (9.6 D7's criterion, D12) — and the list are fixed after the dry run.

No file changed yet.

## D85 — the training run is `cpu-batch`'s `python3` program re-measured; its blocks carried as observed (2026-10-03)

By 9.6 D7's criterion, fixed before 9.6's run, applied under 인지오's delegation (2026-10-03) to the dry run (run 37089156376, #142, the EPYC 7763). The training run is `cpu-batch`'s `python3` program re-measured: at fold-in its two tables, the run between voluntary blocks and the block after each run, come from this campaign in place of 9.6's stand-in. Its blocks are carried as observed. The list is the Tracker campaign's: over the job, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it, and the CPU total, tested by its per-repeat values (D17).

Grounds (the dry run):

- **One thread, runnable throughout.** The job is one process with one thread, `python`, from its first schedule-in to its exit: 1,379.4 s, 1,379.2 s of CPU (perf; taskstats 1,379.2 s), saturation 0.9999. Under the pin `torch` runs one intra-op and one inter-op thread, its backend OpenMP, MKL at one thread (the probe). 9.6 D7's criterion: a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread.
- **The blocks are few and the kernel's.** 21 voluntary blocks in 1,379 s. Two are sleeps of 102 µs in the first 0.22 s. The other 19 are uninterruptible waits of 233–489 µs with no block-I/O, each ended by a wakeup from `khugepaged`, the kernel's huge-page daemon. The runs between them are 10.2–420 s, the long ones close to whole multiples of 10.24 s. The kernel's huge-page settings and its collapse counters are recorded from the next job (method §8).
- **The precedent for carrying what the job shows:** the Tracker extractor's deadline exits (D72). Where a value's spread follows the machine, 9.6 D29's exception carried `python3`'s blocks with their half-width.

Also recorded: 14 test passes, the last "Average loss: 0.0256, Accuracy: 9916/10000 (99%)"; the checkpoint 4,803,113 B; the warm start 8 s; the dataset's eight files, the four archives and the four uncompressed files, cached fraction 1.0000, the venv's shared libraries 1.0000; the layer plus `python3-venv`, `python3.12-venv`, `python3-pip-whl` and `python3-setuptools-whl`; pip's set, 14 packages (`torch` 2.14.0+cpu, `torchvision` 0.29.0+cpu, `numpy` 2.5.2, `pillow` 12.3.0 among them).

The block count per repeat follows the kernel's daemon, not the program. If the run between voluntary blocks does not hold the tolerance, the exception for a value whose spread follows the machine is 인지오's call (9.6 D29). The process shows `python`, the name the venv executes (D84). The task's name and the `program` key the files bind are set at fold-in (D25).

No file changed yet.

## D86 — pair P1's segment 1 stays the index's CPU total in both files; `c2-p1a` binds the whole training job (2026-10-03)

By 인지오's decision, D80's hand-off to D12's item: P1's segment 1 read again against both jobs. Segment 1 stays C seconds long in both files, C the index's CPU total (D80; 39.435 s, D81). `c2-p1a`'s training job arrives at 60 s and is bound whole, `total_work` its measured CPU total (the dry run's 1,379.2 s, D85). The file ends while it runs. `c2-p1b` is unchanged.

Grounds:

- **The label at every instant** (D41, D56, D78, D80). On one lane a job of more than C seconds of CPU is alive throughout a segment of C under every policy. With segment 1 at the training's length, `c2-p1b`'s index, 39.4 s of CPU, would end some 40 s in, and `false` would hold some 1,335 s with no unwanted work alive.
- **One diff per pair** (`docs/workload/building-plan.md` §3, "Counts and reuse"; D80). Equal lengths keep the editor's terms read over equal windows. Two lengths would make the pair differ in length as well as in job and label.
- **D17's ground holds.** No `total_work` describes part of a job: `c2-p1a` binds the whole run. Not held for `c2-p1a`: D17's "a file's and its segments' lengths follow the job". The file shows the training's first C seconds, as it showed the 130 s stand-in's (D80).

Not taken: segment 1 at the training's length in both files (the label above); each file at its own job's length (one diff per pair).

Hands to 9.14: `c2-p1a` carries no finished training job, so no turnaround term reads one; P1's terms over C. Hands to 9.15: `building-plan.md` §3 C2 on P1.

No file changed yet.

## D87 — the campaign keeps the runner's huge-page mode; the two block values carried with their half-widths; five jobs under the desktop kernel's `madvise` checked beside (2026-10-03)

By 인지오's decision, on the first batch (runs 37091275421 and 37091313419, #143 and #144; repeats 1–5, every one valid on the EPYC 7763):

- The campaign runs under the runner's kernel as recorded, its transparent huge pages in `always` mode, the venue of every other campaign.
- The run between voluntary blocks and the block per run are carried over the repeats obtained, at least five, with their half-widths and ranges, the tolerance not applied. This is the workflow's exception for a value whose spread follows the machine (9.6 D29).
- Repeats are added until the CPU total holds.
- Five more jobs run with the kernel's mode set to `madvise` before the phase, as app `mnist-madvise`. They are never repeats of the campaign. Their CPU totals and blocks are reported beside the pool, the difference read against its 95 % interval.
- The entry's scope states the runner's mode, the desktop kernel's default and the check's result.

Grounds:

- **The blocks are the kernel's.** In every repeat, every block but the two sleeps at the start was ended by a wakeup from `khugepaged`. The blocks per repeat number 11, 21, 20, 23 and 15, and the mean run between them 54–115 s by repeat: ±33.7 %, 116 repeats projected. The block per run is ±14.8 %, 25 projected.
- **The runner's mode** (recorded in every job). `enabled` is `[always] madvise never`, `defrag` is `madvise`, and `khugepaged` scans 4,096 pages every 10,000 ms. Each phase fault-allocated 168k–249k huge pages, with 133–145 collapses.
- **The desktop's mode.** Ubuntu 24.04's kernel boots with `CONFIG_TRANSPARENT_HUGEPAGE_MADVISE=y` (S2-50). PyTorch 2.14.0's allocator asks for huge pages only under `THP_MEM_ALLOC_ENABLE` (S2-51), glibc 2.39's only under `glibc.malloc.hugetlb=1` (S2-52). On the desktop's kernel, then, the training heap is not collapsed.
- **One venue.** A measured value is "this software on this machine" (9.5 D10), and the composition seam has one venue (9.5 follow-ups decision 13). Every measured value in the library is the runner's; the earlier campaigns did not record its mode.
- **The CPU total** ranges 1,293.8–1,455.8 s (±5.32 %), and its spread does not follow the huge-page counters. At this spread the pool projects 6 repeats.

Not taken: setting `madvise` for the campaign. The first batch would leave the pool, and this campaign's venue would differ in one setting from every other's.

Hands to 9.14: the check's measured ratio, for the RQ0 gate spec's venue sensitivity check. Hands to 9.15: `docs/workload/measurement-overview.md`'s venue, the runner's huge-page mode against the desktop kernel's.

No file changed yet.

## D88 — the `madvise` check: the training run takes ×1.144 the CPU under the desktop kernel's mode; D87 kept (2026-10-03)

By 인지오's decision, on the check D87 set (runs #146, #148, #149; five jobs on the EPYC 7763, every one valid, `enabled` read `always [madvise] never` before the phase). D87 stands: the campaign is the runner's `always` mode. The check's result is stated in the entry's scope and handed to 9.14.

The check's result, against the campaign's six repeats:

- **CPU total.** 1,589.7 s under `madvise` (1,555.8–1,626.5 s, ±2.01 %) against 1,389.9 s under `always` (1,293.8–1,455.8 s, ±4.04 %). The difference is 199.8 s, ×1.144, its 95 % Welch interval 142.2–257.4 s, ×1.102–×1.185.
- **Blocks.** None but the two sleeps at the start, 99–111 µs, in every check job. No huge page was fault-allocated and none was collapsed in the phase (`thp_fault_alloc`, `thp_collapse_alloc` unchanged). The run is one run of the whole job, 1,555.6–1,626.3 s.
- **The work is the same.** Every job of the campaign and of the check wrote the same checkpoint, SHA-256 `18f1b8f5…`, and ended at "Average loss: 0.0256, Accuracy: 9916/10000 (99%)".
- **The rule holds on the check's own five,** all three values within 5 % (±2.01 %, ±2.77 %, ±2.01 %), so its spread is not the campaign's.

Grounds for keeping D87: one venue for every measured value in the library (9.5 D10; 9.5 follow-ups decision 13). This entry alone at the desktop kernel's mode would differ in one setting from every other entry, while the others' sensitivity to the mode stays unmeasured.

Hands to 9.14: ×1.144 (×1.102–×1.185) is a measured venue effect on one entry's CPU, for the RQ0 gate spec's venue sensitivity check. Hands to 9.15: `docs/workload/measurement-overview.md`'s venue, the runner's huge-page mode against the desktop kernel's, with this result.

No file changed yet.

## D89 — the MNIST campaign's raw records are release `meas-ci-background-2026-10-03` (2026-10-03)

By 인지오's decision, the method's §7. The release is created at the fold-in commit. It holds, each archive without its `pool-cache/`: the 6 pooled landings (runs #143, #144, #147), the dry run (#142, its `perf.data` kept), the five `madvise` check jobs (#146, #148, #149; D87, D88) and the reports of the 7 jobs the machine gate stopped. No data file is in it: the MNIST files appear as their SHA-256 hashes and listing, the checkpoint as its size and hash.

No file changed yet.

## D90 — the MNIST campaign holds at 6 repeats; `cpu-batch`'s `python3` re-measured, the three training files rebound (2026-10-03)

The campaign of D82–D89, `meas-ci:background:2026-10-03`, run under `../measurement-campaign-workflow.md` and recorded in `campaign/mnist/` (method, machine draws, `results/pooled.json`, `results/results.md`, the check's `results/madvise-pooled.json` and `results/madvise-results.md`) and in `measurement-campaign-record.md`.

- **Runs.** The dry run, #142, after one stop at the gate (#141; D85). The first batch, repeats 1–5 (#143, #144), every one valid: the rule failed on all three values, the blocks `khugepaged`'s and the CPU total ±5.32 % (D87). Repeat 6 was added, the pool's projection (#145 stopped at the gate, #147 landed). In all, 8 jobs: 6 landed on the EPYC 7763, 2 stopped by the machine gate. The `madvise` check, never a repeat, was 9 jobs: 5 landed, 4 stopped (D87, D88).
- **The rule holds at 6** on the CPU total, 1,389.885 s ±4.04 % (1,293.8–1,455.8 s). The run between voluntary blocks, 69.49 s ±27.3 %, and the block per run, 311.5 µs ±10.8 %, are carried with their half-widths (D87). Every repeat is valid:
  - the layer built, with `python3-venv`'s four packages added;
  - the example's three files matching their SHA-256;
  - `torch` 2.14.0+cpu and `torchvision` 0.29.0+cpu, one installed set;
  - the dataset cached at 1.0000;
  - the kernel's mode `always`;
  - 14 test passes, the checkpoint the same SHA-256 in every repeat.
- **Reported.**
  - The job is one process with one thread, `python`, saturation 0.99988–0.99991.
  - Each repeat shows 11–24 voluntary blocks, every one but the two sleeps at the start ended by `khugepaged`, with 168k–249k huge pages fault-allocated and 133–145 collapses a phase.
  - The `madvise` check: ×1.144 the CPU (×1.102–×1.185), no block but the two at the start (D88).
- **Release.** The raw records are release `meas-ci-background-2026-10-03`, published on 인지오's go-ahead (D89).
- **Fold-in.**
  - `cpu-batch`'s `python3_run` and `python3_block` are written by `batch_fold_in.py` from `results/pooled.json`, their source `meas-ci:background:2026-10-03`. The scope, stats, run and notes state D82–D88, and 9.6's stand-in's `python3` figures leave.
  - `docs/references.md` gains `pytorch-examples` (deployed-system, verified).
  - `dataset/tools/wlc/grid.py` places `python` at tier 1, `python3`'s (D27: the same program keeps its tier).
- **Rebound.**
  - `c1-ml-train`: `python` on `cpu-batch`, program `python3`, from 2 s, `total_work` 1,389.885 s. The segment is 1,612 s, the smallest whole second by which the run ends under every policy: 2 s plus 1,389.885 s of CPU plus 0.012 s of its blocks plus the editor's 219.263 s as compiled under the file's seed, 1,611.161 s (D17; D78's arithmetic). Focus runs from 2 s to 1,610 s.
  - `c7-ml-train` (`c7.variant.yaml`): `c1-ml-train`'s first C seconds, the run from 0 s, the editor departing at C, focus 2 s to C − 2 s, one segment `background_wanted: false`, `initiated: scheduled`, still a pre-committed miss (D78's form).
  - `c2-p1a`: `python` bound whole, `total_work` 1,389.885 s, segment 1 still 39.435 s (D86).
  - C is 1,389.885 s, the run's `total_work`, which the batch loop compiles exactly.

Recompiled (`compile.py --allow-window`): 6 of 100 artifacts change beyond the library's hash, the three files in both modes. Demand (`-single`):

| file | before | after | |
|---|---|---|---|
| `c1-ml-train` | 0.5426 | 0.9982 | calibration |
| `c7-ml-train` | 0.5426 | 1.1357 | calibration |
| `c2-p1a` | 1.8346 | 14.505 | the estimate counts the whole run, which goes on past the file's end (D86) |

Lint reports the same five demand-window files: `c3-creation`, `c3-evening`, `c3-workday`, `c2-p1a` and `c2-p1b`. Tests: 378 passed, 1 skipped, 1 xfailed. Restated tests: `test_p1_pair_differs_in_segment_one_only` names `python`; `ml-train` leaves `C7_SAME_NAME` for `test_c7_ml_train_is_its_bases_first_c_seconds`; the background tests add the `mnist` job, its exception and the `madvise` check's own name.

Hands to 9.14:
- `c1-ml-train`'s and `c7-ml-train`'s terms on the new lengths;
- `c2-p1a`'s training side, which carries no finished job (D86);
- the check's ×1.144, for the venue sensitivity check (D88);
- `c2-p1a` in the demand window.

Hands to 9.12 and 9.15: 9.6 D32's wording rule restated on an actual training run; the scenario catalog's S12 row; `measurement-overview.md`'s venue, the huge-page mode (D88).

## D91 — the source clip is Big Buck Bunny's 4K 30 fps edition, as the Blender Foundation publishes it (2026-10-03)

By 인지오's decision, D11's open item "the source clip and its length". The transcode's source is `bbb_sunflower_2160p_30fps_normal.mp4`, from `bbb_sunflower_2160p_30fps_normal.mp4.zip` on `download.blender.org/demo/movies/BBB/`, the zip and the clip each checked by its SHA-256 (S2-53). The clip: H.264 High profile, level 5.1, 3840×2160, 30 fps, 19,036 frames, 634.5 s, two audio tracks (MP3 and AC-3), in MP4. Whether the job encodes the whole clip or a cut of it is fixed with the encoder settings, on the cost a probe measures on the runner.

Grounds:

- **CpsMark+'s source** is "the H.264 encoded source video with 4K resolution" (`cpsmark-tbench23` §4.3.4, p. 6; D11). It names no clip, so the clip is design unless a public one is chosen (D11).
- **The one 4K open-movie file in MP4.** Blender's server holds Big Buck Bunny's 4K editions at 30 and 60 fps in MP4, Sintel's 4K as a 4.5 GB MKV and a 5.5 GB `.mov`, and Tears of Steel's as a 6.7 GB `.mov` (S2-53). The 30 fps edition is the smallest download and has half the 60 fps edition's frames for the same film.
- **What the file is,** read from its own boxes, not from a listing (S2-53).

Not taken: the 60 fps edition (twice the encode for the same content); Sintel's and Tears of Steel's 4K files (4.5–6.7 GB per job, and Tears of Steel's codec unread).

No file changed yet.

## D92 — "2K" is DCI's 2048×1080 container, the picture kept whole inside it: 1920×1080 for the clip (2026-10-03)

By 인지오's decision, D11's open item "the encoder settings that realise 'H.265 … 2K, MP4'": the target picture is the largest that fits DCI's 2K container, 2048×1080, at the source's aspect ratio. For the 16:9 clip (D91) that is 1920×1080, its height filling the container's.

Grounds:

- **DCI's definition** (S2-54). "A 2K distribution – the resolution of the DCDM container is 2048x1080" (§4.3.1, p. 31), and a picture fills "the full horizontal pixel count or the full vertical pixel count of the image container" (§8.2.2.7, p. 72).
- **The Blender Foundation's own usage agrees.** Sintel's "2k cinema release version" is 2048 × 872, its 2.39:1 picture filling the container's width (S2-53).
- **CpsMark+ gives no pixel count** for its "2K" (D11). HandBrake 1.7.2's presets never say "2K": they call 2160p "4K" and 1440p "2.5K" (S2-55).

Not taken: 2560×1440, a consumer usage of "2K" for which no source was read, and which HandBrake calls 2.5K; 2048 wide at the source's ratio (2048×1152), which no source's rule gives and which overflows the container's height.

The encoder settings that realise it are open, with the clip's length (D91).

No file changed yet.

## D93 — the encoder settings are HandBrake's default preset with H.265 chosen; the job encodes the whole clip (2026-10-03)

> Amended by D95 (`--encoder x265` leaves: HandBrake's default preset unchanged, x264). The whole clip and the probe stand.

By 인지오's decision, D11's open item "the encoder settings that realise 'H.265 … 2K, MP4'" and D91's length, on the probe below. The transcode runs HandBrake 1.7.2's default preset, "Fast 1080p30", with its video encoder set to `x265`, the plain H.265 entry: `--preset "Fast 1080p30" --encoder x265`. Every other setting is the preset's own (S2-55). The picture is 1920×1080, D92's size, inside the preset's 1920×1080 bound. The frame rate is the source's 30 fps under the preset's peak of 30. x265 runs at the preset's "fast", RF 22, profile main, level 4.0. Audio is the first track as AAC stereo at 160 kb/s, in MP4. The job encodes the whole clip, 19,036 frames (D17, D91).

Grounds:

- **HandBrake's own default.** "Fast 1080p30" is the preset HandBrake 1.7.2 marks `Default` (S2-55). Its size is D92's and its container is CpsMark+'s MP4. One change, the codec, realises CpsMark+'s "H.265 … 2K, MP4" (D11). No built-in preset is software H.265 at a 2K-class size in MP4 (S2-55).
- **The whole clip fits the workflow's job.** The probe (below) puts every candidate's whole-clip encode at 1,530–3,700 s of CPU on one CPU of the EPYC 7763. The workflow's job limit is 330 minutes. D17's "each batch job runs whole" then holds with the clip as published (D91).
- **No hardware acceleration on the runner.** Ubuntu's HandBrakeCLI 1.7.2 lists software encoders and reports "qsv: not available on this system" (run #151's `handbrake.help.txt`).

The probe (`run.sh` mode `probe`, never a repeat; run #150 stopped at the gate on an Intel Xeon 8370C, run #151's two jobs on the EPYC 7763). In D82's chroot with `handbrake-cli` added, the clip warm, 30 s of the clip from its start and from 300 s were encoded on the measured CPU at four of HandBrake's H.265 presets. The 4K presets were held to `--maxWidth 2048 --maxHeight 1080`. Per source second of CPU, the two jobs within 1.5 % of each other:

| preset | x265 | CPU s per source s | whole clip, projected |
|---|---|---|---|
| "Very Fast 2160p60 4K HEVC" | 10-bit superfast, RF 26 | 2.41–2.58 | 1,530–1,640 s |
| "Fast 2160p60 4K HEVC" | 10-bit faster, RF 24 | 4.20–4.32 | 2,670–2,740 s |
| "HQ 2160p60 4K HEVC Surround" | 10-bit medium, RF 22 | 4.49–4.67 | 2,850–2,960 s |
| "H.265 MKV 1080p30" with `--format av_mp4` | 10-bit slow, RF 22 | 5.24–5.83 | 3,320–3,700 s |

Also read from the probe:

- **The picture.** Held only by the maximum size, the 4K presets stored 2048×1080 at a pixel aspect of 15:16, shown as 1920×1080 (their `PicturePAR` "auto"). "H.265 MKV 1080p30", bounded at 1920×1080, stored 1920×1080.
- **The thread shape under the pin.** One process of 26–33 threads, saturation 0.991–0.997. The busiest thread held 0.23–0.34 of the CPU and the next 0.19–0.24. x265 created a pool of 4 threads with 2 frame threads: x265 3.5 sizes its pool from the NUMA node's CPUs, not from the process's affinity (S2-57).
- **Determinism.** Each cut's x265 summary (frames, kb/s, average QP) was the same in both jobs. The output files' SHA-256 differed.
- **The cross-check.** For the multi-threaded process, taskstats' thread-group row gave 2.5–3.8× perf's CPU, and its per-thread rows summed to 0.90–1.00 of it. The CPU total read is perf's, the sum of the program's runs on the measured CPU (saturation above).

Not taken: "Fast 2160p60 4K HEVC" held to 1920×1080 (HandBrake's MP4 H.265 preset of the default's tier, the size changed); "H.265 MKV 1080p30" in MP4 (HandBrake's H.265 preset of the size, the container changed). Neither is HandBrake's default.

The chosen settings were not probed; the dry run measures them. The thread shape is read against 9.6 D7's criterion after the dry run.

No file changed yet.

## D94 — the transcode's state, warm start and job: D82's chroot with `handbrake-cli`, the clip warm, the encode as the user from its first schedule-in to its exit (2026-10-03)

> Amended by D95 (the command drops `--encoder x265`; the output is `bbb_sunflower_2160p_30fps_normal.out.mp4`).

Taken under 인지오's delegation (2026-10-03), on D82–D84's precedents.

- **The state.** D37's chroot at D64's T0 (2026-09-22T17:00Z), with `handbrake-cli` added from the same snapshot: 1.7.2+ds1-1build2, with x265 3.5-2build1 and FFmpeg 6.1.1 (S2-56). Its 67 packages are recorded per repeat. The Tracker campaign's user, with its XDG folders made by the layer's `xdg-user-dirs-update`. The clip (D91) is fetched and unzipped on the harness CPUs, the zip and the clip each checked by its SHA-256, and placed as `~/Videos/bbb_sunflower_2160p_30fps_normal.mp4`.
- **The warm start.** Before the phase, on the harness CPUs: the clip is read whole, and HandBrakeCLI's own scan of it runs once (`HandBrakeCLI -i … --scan`). The clip's cached fraction is measured with `fincore`, and validity asks at least 0.99. The fraction for HandBrakeCLI and its codec libraries is recorded beside it.
- **The job.** `HandBrakeCLI -i bbb_sunflower_2160p_30fps_normal.mp4 -o bbb_sunflower_2160p_30fps_normal.h265.mp4 --preset "Fast 1080p30" --encoder x265` in `~/Videos`, as the user in the chroot, `taskset` placing it on the measured CPU. The output's name is design. The job is every process of the tree `taskset` launched into `chroot`, from its first schedule-in on the measured CPU to its exit: the CLI's own scan, the encode and the mux. The phase has no cap of its own; the workflow's job limit is 330 minutes.
- **The venue.** The runner's kernel as recorded, its transparent huge pages in `always` mode. The settings and counters are recorded before and after the phase.

Grounds:

- **One state across 9.10's campaigns** (D82). The chroot and T0 are the DKMS, Tracker and MNIST campaigns'. "As Ubuntu 24.04 packages it" (D11) is the archive's package at T0 (S2-56).
- **A warm start** (D83; 9.6 D28's ground). The batch-loop compiler draws each run and each block independently, so the start's page-ins would be spread over the whole simulated job. A clip the user has just downloaded or copied is in the page cache. The probe's warm starts held the clip and the libraries at 1.0000.
- **The job as D84's.** The tree from its first schedule-in to its exit, as the user, one CPU (9.5 D21). HandBrakeCLI scans its source before it encodes, so the scan is the program's own work. What x265 sees under the pin, its pool and frame threads, is recorded from each job's log (D84's "what `torch` sees under the pin").
- **One venue** (D87's ground: 9.5 D10; 9.5 follow-ups decision 13). The MNIST campaign showed the mode can end a job's blocks (D85, D87). Whether this job's blocks are the kernel's is read from the dry run.

The entry's form — `cpu-batch`'s `HandBrakeCLI` tables re-measured, or an entry of its own (9.6 D7's criterion) — and the list are fixed after the dry run.

No file changed yet.

## D95 — the transcode is H.264, CpsMark+'s own code's codec: HandBrake's default preset unchanged, amending D11's reading and D93 (2026-10-03)

By 인지오's decision, on CpsMark+'s source code (S2-58). The transcode runs HandBrake 1.7.2's default preset, "Fast 1080p30", unchanged: `--preset "Fast 1080p30"`. Its settings (S2-55):

- x264 0.164.3108 as the archive packages it (S2-56), at "fast", RF 22, profile main, level 4.0;
- 1920×1080 at most, D92's size;
- a peak frame rate of 30, so the clip's 30 fps are kept;
- the first audio track as AAC stereo at 160 kb/s;
- MP4.

D11's workload is read as an H.264 4K source transcoded to H.264 at 2K in MP4. The clip stays Big Buck Bunny's 4K 30 fps edition, whole (D91, D93). D92 stands. D93's `--encoder x265` leaves, and with it D94's output name: the output is `bbb_sunflower_2160p_30fps_normal.out.mp4` (design). Everything else in D94 stands.

Grounds:

- **The benchmark's code is H.264 throughout** (S2-58). Its software preset is `fast_1080p_h264_sw`, and its hardware presets are `fast_1080p_h264_nvenc`, `fast_1080p_h264_vce` and `fast_1080p_qsv`. It confirms hardware use by HandBrake reporting `qsv_h264`, `nvenc_h264` or `vce_h264`. A commented-out earlier command used the built-in x264 preset "HQ 1080p30 Surround". The paper's "H.256" (`cpsmark-tbench23` §4.3.4, p. 6), which D11 read as H.265, is the one H.265 reading against all of these, and it is itself a typo.
- **The code's "2K" is 1080p.** Every preset it names targets 1080p, and it logs the run as "4K->2K". D92's 1920×1080 agrees.
- **HandBrake's default preset is "Fast 1080p30"** (S2-55). The code's preset name, `fast_1080p_h264`, matches it, but the preset file is not in the repository and the resource package was not reached (S2-58). The preset's exact settings are therefore HandBrake's own default, not read from CpsMark+.
- **The code's clip is not obtainable** (S2-58): a 10 s 4K 24 fps cut of Tears of Steel in the unreached package. D91's public clip stays.

Not taken:

- D93's H.265 with the paper's text: the weaker of the two sources, its codec word a typo.
- A 10 s cut of Tears of Steel of our own: the cut and its H.264 encoding would be design, and Blender's 4K `.mov`'s codec is unread.

The dry run of D93's settings (run #152) is superseded and is not pooled. D93's probe stands as a record of HandBrake's H.265 presets on the runner.

No file changed yet.

## D96 — a lengthened base keeps its operation at its fraction of the focus window: `c1-transcode`'s preview render at the window's middle (2026-10-03)

By 인지오's decision, at the transcode files' rebinding. `c1-transcode` lengthens to hold the whole encode (D17), its length set as D90 set `c1-ml-train`'s: the smallest whole second by which the job ends under every policy. Its focus window keeps the 2 s margins, 2 s to T − 2 s. Its one operation, `preview-render` on `video-editor`, sits at the same fraction of the window as in the 60 s base: the middle, the base's 30 s in 2–58 s. `c7-transcode`, cut to C, places it by D44 as written, also at its window's middle.

Grounds:

- **D44's rule is the dataset's one placement rule for a re-timed file.** "A cut counterpart keeps its base's placement in proportion … each operation at its fraction of the window." The rule extends to a base re-timed the other way.
- **D20 holds either way.** One operation per focus window on an application that has one, inside focus.
- **The pair stays aligned.** Base and counterpart both place the render mid-job. At the base's literal 30 s, the render would meet the encode in its first 28 s, which hold HandBrakeCLI's own scan of the clip (D94). `c7-transcode` would then place it 28/(T − 4) of the way into its window.

Not taken: the base's literal 30 s.

No file changed yet.

## D97 — the transcode is a new entry in the batch-loop form; `cpu-batch`'s `HandBrakeCLI` tables leave at fold-in (2026-10-03)

By 인지오's decision, 9.6 D7's criterion applied to the dry run of D95's settings (run 37105339193, #153, the EPYC 7763). The encode is an entry of its own in the batch-loop form: a run drawn from the program's runs between voluntary blocks, pooled over its threads, then the block that followed it, until `total_work` of CPU is spent (9.6 D21, D22, D25). At fold-in, `cpu-batch`'s `handbrakecli_run` and `handbrakecli_block` leave, with the `handbrakecli` program, and the transcode files bind the new entry. The list is the MNIST campaign's: over the job, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it, and the CPU total, tested by its per-repeat values (D17).

Grounds (the dry run):

- **Runnable throughout, not on one dominant thread.** The job is one process, `HandBrakeCLI`, 2,974.0 s from its first schedule-in to its exit, with 2,972.35 s of CPU (perf; taskstats 2,973.32 s): saturation 0.9994. Its 23 threads, all named `HandBrakeCLI`, hold 0.335, 0.207, 0.101, 0.088, 0.067, 0.056 and 0.043 of the CPU. 9.6 D7's criterion: a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread, and sustained I/O waits or several equal threads give it its own entry. 9.6's 720p x264 encode, bound to `cpu-batch` (9.6 D12), had its main thread at 0.61 of 22 and the next at 0.09.
- **The precedent.** Tracker's index failed the criterion and became `file-indexer`, a batch-loop entry of its own, while `cpu-batch`'s `tracker` tables left (D70).
- **The blocks are rare and short.** 742,663 runs between voluntary blocks, mean 4.00 ms. The block after a run, the program's off-CPU time, has mean 0.602 µs and is zero at the 99th percentile. There are 3 uninterruptible waits of 0.37–0.47 ms, each ended by a wakeup from `khugepaged` (333 collapses in the phase, `thp_collapse_alloc` 60 → 393), and no disk wait. The threads' other sleeps are pipeline hand-offs: another thread of the program runs on.

Also recorded:

- **The state and clip.** The layer plus `handbrake-cli`'s 67 packages; `handbrake-cli` 1.7.2+ds1-1build2, `libx264-164` 2:0.164.3108+git31e19f9-1; the zip and the clip matching their SHA-256; the clip and the libraries cached at 1.0000 after the warm start.
- **The encoder and picture.** `+ encoder: H.264 (libx264)`, preset fast, profile main, level 4.0, RF 22; x264's "profile Main, level 4.0, 4:2:0, 8-bit"; stored 1920 × 1080 at 1 : 1.
- **The frames.** The decoder's 19,036 frames with no error; 19,038 frames synced and muxed, 276,311,652 B of video; the output 289,921,239 B.
- **The superseded dry run of D93's settings** (run 37103205438, #152, the EPYC 7763, not pooled). x265's 4-thread pool encoded 19,038 frames with 2,483.81 s of CPU, saturation 0.9993, one process of 29 threads, the busiest 0.282 of the CPU.

The entry's id is open.

No file changed yet.

## D98 — the task shows `HandBrakeCLI`; the entry is `video-transcoder` (2026-10-03)

By 인지오's decision, D97's open item. The one task of D97's form shows `HandBrakeCLI`, the `comm` of `/usr/bin/HandBrakeCLI` as the dry run observed it, under 15 bytes (D25). The archetype's id is `video-transcoder`.

Grounds:

- **D24 and D25.** A task shows the observed program's name, as its kernel `comm`. The job is that one process and its 23 threads, all named `HandBrakeCLI` (D97).
- **The files and the tier.** `c1-transcode` and `c3-creation` already show `HandBrakeCLI`; its familiarity tier is unchanged (D27: the same program keeps its tier).
- **The id names the role** (D74's ground), beside `file-indexer`, `file-archiver` and `file-backup`. The job is a video transcode; `media-transcoder` would also claim audio-only work.

Not taken: `video-transcode` (the activity, as `package-upgrade`); `media-transcoder`.

No file changed yet.

## D99 — the HandBrakeCLI campaign's raw records are release `meas-ci-background-2026-10-03b` (2026-10-03)

By 인지오's decision, the method's §7. The release is created at the fold-in commit. It holds, each archive without its `pool-cache/`:

- the 5 pooled landings (runs #154, #156);
- the dry run #153 of D95's settings, its `perf.data` kept;
- the dry run #152 of D93's settings, superseded by D95, its `perf.data` kept;
- the probe's two jobs (#151; D93);
- the reports of the 5 jobs the machine gate stopped.

No video is in it: the clip appears as its SHA-256 and size, and each output as its size and hash.

No file changed yet.

## D100 — the HandBrakeCLI campaign holds at 5 repeats; `video-transcoder` folded in, the three transcode files rebound (2026-10-03)

The campaign of D91–D99, `meas-ci:background:2026-10-03b`, run under `../measurement-campaign-workflow.md`. It is recorded in `campaign/handbrake/` (method, machine draws, `results/pooled.json`, `results/results.md`) and in `measurement-campaign-record.md`.

- **Runs.**
  - The probe: #150 stopped at the gate; #151, two jobs (D93).
  - The dry runs: #152 of D93's settings, superseded (D95); #153 (D97).
  - The first batch, repeats 1–5 (#154; repeats 4 and 5 stopped at the gate on the AMD EPYC 9V74 in #154 and #155, then landed in #156).
  - In all, 9 jobs: 5 landed on the EPYC 7763, 4 stopped by the machine gate.
- **The rule holds at 5 on all three values.** The CPU total is 2,970.871 s ±2.64 % (2,863.5–3,023.8 s). The run between voluntary blocks is 4.002 ms ±1.79 %. The block per run is 0.605 µs, within the 1 µs floor. Every repeat is valid:
  - the layer built, with `handbrake-cli`'s 67 packages added;
  - `handbrake-cli` 1.7.2+ds1-1build2 and `libx264-164` 2:0.164.3108+git31e19f9-1;
  - the zip and the clip matching their SHA-256, the clip cached at 1.0000;
  - the kernel's mode `always`;
  - `libx264` at fast and RF 22, the picture 1920 × 1080 at 1 : 1;
  - the clip's 19,036 frames decoded with no error, and one video track, 19,038 frames and 276,311,652 B.
- **Reported.**
  - The job is one process of 23 threads, `HandBrakeCLI`, saturation 0.99938–0.99947. The busiest thread holds 0.334–0.338 of the CPU, the next 0.205–0.208.
  - 733k–746k runs a repeat, up to 96–101 s. About 2 in 100,000 are followed by a block, 0.26–0.60 s of blocks a job.
  - 2–12 uninterruptible waits and 0–1 disk wait a repeat.
- **Release.** The raw records are release `meas-ci-background-2026-10-03b`, published on 인지오's go-ahead (D99).
- **Fold-in.**
  - `video-transcoder`, a batch-loop entry, is added after `file-indexer`. Its `handbrake_run` and `handbrake_block` are written by `batch_fold_in.py` from `results/pooled.json`, their source `meas-ci:background:2026-10-03b`. Its scope, stats, run and notes state D91–D98.
  - `cpu-batch`'s `handbrakecli_run` and `handbrakecli_block` leave (D97). Its scope, stats, run and notes are restated: two programs from 9.6's campaign, and the notes point to `video-transcoder`.
  - `docs/references.md` gains `big-buck-bunny`, `handbrake`, `dci-dcss` and `cpsmarkplus` (deployed-system, verified). `cpsmark-tbench23`'s artifact note points to `cpsmarkplus`.
  - `dataset/tools/wlc/grid.py` is unchanged: `HandBrakeCLI` keeps its tier (D27, D98).
- **Rebound.**
  - `c1-transcode`: `HandBrakeCLI` on `video-transcoder` from 2 s, `total_work` 2,970.871 s. The segment is 4,762 s, the smallest whole second by which the encode ends under every policy: 2 s plus 2,970.871 s of CPU plus 0.522 s of its blocks plus the editor's 1,787.903 s as compiled under the file's seed, 4,761.296 s (D17; D78's arithmetic, D90's form). Focus runs 2–4,760 s, and the preview render is at 2,381 s, the window's middle (D96).
  - `c7-transcode` (`c7.variant.yaml`): `c1-transcode`'s first C seconds, the encode from 0 s, the editor departing at C, focus 2 s to C − 2 s, the preview render at 1,485.4355 s, its window's middle (D44, D96). One segment, `background_wanted: false`, `initiated: scheduled`, still a pre-committed miss (D78's form, as D90's `c7-ml-train`).
  - `c3-creation`: the transcode segment runs from 240 s to 3,212 s, the smallest whole second by which the encode ends under every policy: 240 s plus 2,970.871 s plus 0.416 s of its blocks plus the other tasks' 0.228 s after 240 s, 3,211.514 s (D17). `kdenlive` stays open to the segment's end, as it did to 420 s; taken under 인지오's delegation, the file's structure kept.
  - C is 2,970.871 s, the encode's `total_work`, which the batch loop compiles exactly.

Recompiled (`compile.py --allow-window`): 6 of 100 artifacts change beyond the library's hash, the three files in both modes. Demand (`-single`):

| file | before | after | |
|---|---|---|---|
| `c1-transcode` | 0.9445 | 0.9993 | calibration |
| `c7-transcode` | 0.9445 | 1.3727 | calibration |
| `c3-creation` | 0.8843 | 0.9410 | the demand window (D17) |

Lint reports the same five demand-window files: `c2-p1a`, `c2-p1b`, `c3-creation` (now 0.94), `c3-evening` and `c3-workday`. `compile.py --check --allow-window` and `batch_fold_in.py --check` pass. Tests: 380 passed, 1 skipped, 1 xfailed.

Restated tests:
- `transcode` leaves `C7_SAME_NAME` for `test_c7_transcode_is_its_bases_first_c_seconds`;
- `test_the_batch_tables_regenerate_from_the_pooled_records` names `video-transcoder`, its table count unchanged at 89;
- `test_zero_inclusive_block_table_leaves_the_program_running` reads HandBrakeCLI's table from `video-transcoder`, and `cpu-batch` holds three table sets;
- the background tests add the `handbrake` job, its list and its name.

Hands to 9.14:
- `c1-transcode`'s and `c7-transcode`'s terms on the new lengths;
- `c3-creation` in the demand window at 0.94.

Hands to 9.12 and 9.15:
- the scenario catalog's S8 row, CpsMark+'s HandBrake workload H.264 per its own code (D95);
- prose citing that workload as H.265;
- `cpu-batch`'s scope without `HandBrakeCLI` (D11's hand-off).

## D101 — the export is started through Kdenlive's render dialog in every repeat; the job is the tree of the `kdenlive_render` it starts (2026-10-03)

By 인지오's decision, D10's open item "the export's process and its names" and how the campaign starts it. In every repeat Kdenlive is open on the `video-editor` project. Its Render action (Ctrl+Return) opens the render dialog, and "Render to File" is pressed on the dialog as it opens: the default profile (D103), the full project, the dialog's default output file. Kdenlive writes its own playlist and starts the renderer. The job is every process of the tree rooted at the process that executes `/usr/bin/kdenlive_render`, from its first schedule-in on the measured CPU to its exit. The playlist Kdenlive writes is kept from each job.

Grounds:

- **Kdenlive 23.08.5's export** (S2-59). The dialog starts `kdenlive_render delivery <melt> <playlist> --pid <Kdenlive's pid>` detached. `kdenlive_render` runs `melt-7 -progress <playlist>` as its child and sends the progress to Kdenlive over D-Bus. 23.08.5 has no command-line export. Started detached, `kdenlive_render` is not Kdenlive's child, so the job's root is the process that executes it; it keeps Kdenlive's CPU affinity.
- **D10's terms.** "Kdenlive's own export of the `video-editor` entry's project, observed on the runner"; "an export phase on 9.5's Kdenlive setup". The dialog, the playlist and the progress path are Kdenlive's own.
- **PCMark 10's Video Editing has no export step** (S2-13 p. 55; `pcmark10` pp. 76–77). Its parts are a Media Foundation downscale and FFmpeg command lines that sharpen and deshake, the output codec unstated. The project already takes the sharpening's parameters (`video-editor`'s scope).
- **The names are read from the run** (D25): the `comm`s of `kdenlive_render` and of the `melt` it starts, `melt-7` by Kdenlive's own lookup (S2-59 `mltconnection.cpp:106`; S2-60).

Not taken: Kdenlive writes the playlist once, in a probe, and each repeat runs `kdenlive_render` on it with no window open. It is steadier, but Kdenlive's part shrinks to one recorded file and the progress path is lost.

No file changed yet.

## D102 — the export's state is D37's chroot at T0 with Kdenlive installed by apt; 9.5's project, settings and launch carried in (2026-10-03)

By 인지오's decision. The campaign runs in D37's chroot of the English default install, built from the archive at D64's T0 (2026-09-22T17:00Z). On the harness CPUs, `apt-get install kdenlive ffmpeg` installs from the same snapshot with apt's defaults: 9.5's install line (`dataset/tools/meas/probe/appdefs.sh`), run as the DKMS campaign installed its driver package (D49). The user is the Tracker campaign's. 9.5's per-user UI file, its `kdenliverc` and its project writer (`appdefs.sh`; `dataset/tools/meas/probe/kdenlive_project.py`) are carried into the user's home. Xvfb runs on the harness CPUs, its socket visible in the chroot, and Kdenlive runs as the user under a session bus of its own.

Grounds:

- **One state across 9.10's campaigns** (D82, D94). The upgrade, DKMS, Tracker, MNIST and HandBrakeCLI campaigns ran in this chroot, the last four at this T0.
- **The render stack is the one 9.5 measured** (S2-60). At T0 the archive holds Kdenlive 4:23.08.5-0ubuntu4, the version in 9.5's install logs (`video-editor`'s scope), with MLT 7.22.0, FFmpeg 6.1.1 and x264 0.164.3108, all in the release pocket with no update in either pocket.
- **Kdenlive's recommends** (S2-60). `kdenlive` recommends `frei0r-plugins`, which carries the project's `frei0r.cairoblend` transition, with `mediainfo` and `swh-plugins`; apt's defaults install them. The packages added are recorded per repeat.
- **D10's "9.5's Kdenlive setup"** is read as 9.5's project, its settings and its launch.

Not taken: 9.5's install on the runner. The rest of the runner image is not a desktop install, and its packages are the archive's on the day.

No file changed yet.

## D103 — the render profile is Kdenlive 23.08.5's shipped default, MP4-H264/AAC as the dialog opens: x264 at `veryfast`, CRF 23 (2026-10-03)

Taken under 인지오's delegation (2026-10-03), D10's open item "the render profile's settings, as Kdenlive 23.08 ships its default", read from the source (S2-59). The dialog opens on `renderProfile`'s default, MP4-H264/AAC, since the project names no profile. Its settings with the dialog's defaults:

- `f=mp4 movflags=+faststart`;
- `vcodec=libx264`, `crf=23` (the preset's default quality, "Custom Quality" off), `g=15`, `preset=veryfast` (speed index 6);
- `acodec=aac ab=160k`: the project's empty audio track exported as silence;
- `real_time=-1` (one processing thread, "Parallel Processing" off) and `threads=0` (`encodethreads`' default);
- the full project, one pass, no proxy clips, no metadata, at the project's 1920×1080 at 30 fps.

Grounds:

- **D10 fixes the default render profile.** The settings are its, read, not chosen.
- **The playlist is checked against them.** The `<consumer>` element Kdenlive writes into each job's playlist carries the profile's settings (S2-59 `renderrequest.cpp`); validity asks the settings above in every pooled repeat.

What x264 and the decoder make of `threads=0` under the pin is read from the run: x264's options string in the output, and the threads perf records.

No file changed yet.

## D104 — the export's start: Kdenlive open on the project on the measured CPU, the clip warm; the runner's kernel (2026-10-03)

Taken under 인지오's delegation (2026-10-03), on 9.5 D21, D83 and D94.

- **The project.** 9.5's: the clip, 20 s of 1920×1080 at 30 fps H.264 (`testsrc`, `libx264` `veryfast`, `yuv420p`, no audio; design), and `kdenlive_project.py`'s project over its 600 frames with the unsharp effect at PCMark 10's parameters. The clip is generated by the chroot's `ffmpeg` on the harness CPUs, as `~/Videos/clip.mp4`, and the project is written as `~/Videos/project.kdenlive`. The clip's SHA-256 is recorded and must be one across the pooled repeats.
- **The launch.** `kdenlive ~/Videos/project.kdenlive` as the user in the chroot, with 9.5's environment (`QT_QPA_PLATFORM=xcb`, `KDE_FULL_SESSION=true`). Kdenlive's whole tree is on the measured CPU (9.5 D21: the application's process tree pinned to one CPU), and the export inherits it. Kdenlive's own CPU in the phase is outside the job and reported beside it, as the runner's agent processes are (D94).
- **The warm start.** Before the phase: Kdenlive open on the project, its own load of the clip, and left to settle; the clip read whole. The clip's cached fraction is measured with `fincore`, and validity asks at least 0.99. The fractions for `melt-7`, MLT's modules and the codec libraries are recorded beside it.
- **The phase.** From the Render shortcut to the exit of `kdenlive_render`; no cap of its own. The workflow's job limit is 330 minutes.
- **The venue.** The runner's kernel as recorded, its transparent huge pages in `always` mode, recorded before and after the phase (D94).

Grounds:

- **One CPU, the application's tree** (9.5 D21). The export is Kdenlive's child by affinity (D101), so the window and the render share the CPU, as on a one-CPU desktop. The editor's own CPU in the files is `video-editor`'s, beside the job.
- **A warm start** (D83; D94). A user exporting a project they have open has its clip in the page cache. The batch-loop compiler would spread a cold start's page-ins over the whole simulated job.
- **9.5's project** (D102). The clip's content and length are design (D10, D17: "the project's 20 s clip is design").

The entry's form — by 9.6 D7's criterion — and the list are fixed after the dry run. The job's size against the segments is read from it (D17).

No file changed yet.

## D105 — the export is `cpu-batch`'s new program `kdenlive_render`; `cpu-batch`'s `ffmpeg` tables leave at fold-in (2026-10-03)

By 인지오's decision, 9.6 D7's criterion applied to the dry run (run 37123567963, #161, the EPYC 7763). The export is a new program in `cpu-batch`: its two tables, the run between voluntary blocks and the block after each run, pooled over every process of the job's tree (D101), and the job's CPU total, carried as measured (D17). At fold-in `cpu-batch`'s `ffmpeg_run` and `ffmpeg_block` leave with the `ffmpeg` program, which no file binds once the render files rebind. The list is the MNIST and HandBrakeCLI campaigns': over the job, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it, and the CPU total, tested by its per-repeat values (D17).

Grounds (the dry run):

- **Runnable throughout, on one dominant thread.** The job is the tree of `kdenlive_render`, 16.095 s from its first schedule-in to its exit, with 15.972 s of CPU (perf; taskstats 15.995 s): saturation 0.9924. `melt-7` holds 15.913 s in 9 threads; the busiest thread holds 0.689 of the job's CPU, the next 0.184, four others 0.026–0.030 each, the rest under 0.011. `kdenlive_render` holds 54 ms. 9.6 D7's criterion: a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry. 9.6's encode, bound to `cpu-batch` as `ffmpeg` (9.6 D12), had its main thread at 0.61 and the next at 0.09 (D97).
- **The blocks are short and the waits few.** 8,555 runs between voluntary blocks, mean 1.867 ms; the block after a run mean 4.9 µs, 42 ms over the job. One disk wait of 0.1 ms (`kdenlive_render`), no uninterruptible wait ended by `khugepaged`.
- **The tree is one program's work.** `melt-7` holds 99.6 % of the CPU. The unattended upgrade's own entry (D39) rested on 923 processes across many programs.
- **What the stand-in's tables become.** After the rebinding no file binds `ffmpeg` (D10's open item). D97 retired `cpu-batch`'s `HandBrakeCLI` tables when their files bound the measured job.

Also recorded:

- **The dialog.** Ctrl+Return opened "Rendering" once Kdenlive's window held the X input focus; `kdenlive_render` was seen 115 ms after the click on "Render to File". Its arguments: `delivery /usr/bin/melt-7 /tmp/kdenlive-OcFcGp-1.mlt --pid 32402`.
- **The profile** (D103). The playlist's `<consumer>`: `mlt_service=avformat f=mp4 movflags=+faststart vcodec=libx264 crf=23 preset=veryfast g=15 acodec=aac ab=160k channels=2 real_time=-1 threads=0`, `in=0 out=599`, target `~/Videos/project.mp4`. x264's options string: `threads=1 lookahead_threads=1 sliced_threads=0`, `keyint=15`, `rc=crf crf=23.0`.
- **The output.** 600 H.264 High frames at 1920 × 1080 and 938 AAC frames, in MP4, 966,107 B.
- **`kuiserver`.** `kdenlive_render` logs "No org.kde.JobViewServer registered, trying to start kuiserver" and "Failed to start kuiserver" (S2-59 `renderjob.cpp:206–222`): two forks of it, 0.8 and 1.1 ms, execute nothing. They are part of the tree.
- **The state.** The layer plus the 427 packages `apt-get install kdenlive ffmpeg` added, Kdenlive's recommends among them; the clip and the render stack's libraries cached at 1.0000.
- **Beside the job.** Kdenlive's window held 65 ms of the measured CPU during the job, the session bus 3 ms.
- **The dry runs before it.** Run 37121829327 (#157): Ctrl+Return opened no dialog. Xvfb runs no window manager, and Kdenlive's window did not hold the input focus. The driver now gives it the focus, with the Project menu's "Render…" as a fallback (method §8). Run #158 stopped at the gate (an AMD EPYC 9V74).

The program's name and the task's are open.

No file changed yet.

## D106 — the task shows `kdenlive_render`; the program key is `kdenlive_render` (2026-10-03)

By 인지오's decision, D105's open item. The task shows `kdenlive_render`, the `comm` of `/usr/bin/kdenlive_render` as the dry run observed it, 15 bytes (D25). `cpu-batch`'s program key is the same: `kdenlive_render_run` and `kdenlive_render_block`.

Grounds:

- **A tree's task shows its root.** `unattended-upgr` (D40) over a tree whose CPU went mostly to `localedef` and `dpkg`; `dkms` (D55) over its compile jobs; `tracker-miner-f` (D74) over its extractor. `kdenlive_render` is the process Kdenlive's dialog starts, and `melt-7` its child (D101, D105).
- **The name says what the job is:** Kdenlive's renderer, the process a desktop's process list shows while Kdenlive exports.

Not taken: `melt-7`, the child that holds 99.6 % of the CPU, with the program key `melt`.

No file changed yet.

## D107 — `kdenlive_render` is familiarity tier 1 (2026-10-03)

By 인지오's decision, D27's rule applied to D106's name: `kdenlive_render` is a new program's name, placed by the ladder's definitions at tier 1, transparent. The name says what the job is, Kdenlive rendering. Labelled design, as D27's tiers are.

Grounds:

- **The ladder's definitions** (`docs/workload/building-plan.md` §3 C5): 1 transparent (`firefox`, `blender`), 2 semi-opaque (`soffice.bin`, `gamescope`), 3 opaque (`tracker-miner-fs-3`, `cc1`, `baloo_file`). `kdenlive` is tier 1, as is `unattended-upgr` (D43).
- **The C7 property** (`building-plan.md` §3 C7, as D43 cites it): "tier 1 so no pair changes familiarity tier". Pair P3 keeps one tier in both files, `kdenlive` and `kdenlive_render` in `c2-p3a` against `kdenlive` and `borg` in `c2-p3b`.

Applied at rebinding: `dataset/tools/wlc/grid.py`'s `NAME_TIERS`.

## D108 — pair P3's segment 1 stays 60 s in both files; `c2-p3a` binds the whole export (2026-10-03)

By 인지오's decision, D10's open item "the job's size against the segments" for pair P3. Segment 1, the second, keeps its 60 s, 60–120 s, in both files. `c2-p3a`'s render binds the whole export from 60 s: `kdenlive_render` on `cpu-batch`, `total_work` its measured CPU total (D105, D106). `c2-p3b`'s `borg` is unchanged until D8's item.

Grounds:

- **The render ends inside the segment.** With the dry run's 16.0 s of CPU, it ends by about 99 s under every policy: 60 s, plus the job's CPU and blocks, plus the editor's 23.0 s of CPU released after 60 s (D78's arithmetic). The `true` cell's turnaround term then reads a finished job, as D78 kept `c1-indexing`'s segment for a job that fits it.
- **One diff per pair** (`docs/workload/building-plan.md` §3, "Counts and reuse"; D80). Both files keep one length and still differ only in segment 1's job and label.
- **The label at every instant concerns `false`.** D41's counterparts and D80's `c2-p1b` sized a segment to its job so that `false` never held with no unwanted work alive. Both of P3's segments say `true`.

Not taken: segment 1 at the export's CPU total in both files, D42's and D80's form (the render could not finish inside it on a shared lane); segment 1 at the render's smallest finishing length in both files (the pair sized to one half's job while the other half is still a stand-in).

Hands to D8's item: P3's segment 1 is read again against both jobs when the backup is measured.

No file changed yet.

## D109 — the block per run is settled by running on to the pool's projection, not by 9.6 D29's exception (2026-10-03)

By 인지오's decision. At the first batch's five landings (runs #162, #163, `meas-ci:background:2026-10-03c`), every repeat valid, the run between voluntary blocks (1.930 ms ±1.6 %) and the CPU total (16.498 s ±1.7 %) hold the rule and the block per run does not: its per-repeat means are 4.91, 0.21, 5.56, 5.47 and 0.74 µs, ±98 % against the 1 µs floor, 30 repeats projected. The campaign runs on in one batch up to the projection, repeats 6–30 (9.7 D26), the rule read after each landing.

Grounds:

- **The spread is melt's own timer.** Repeats 1, 3 and 4 each end with one block of 40.05 ms, `melt-7`'s main thread about 16.39 s into the job, and repeats 2 and 5 with none; the block per run's other values are alike across repeats. With `-progress`, which `kdenlive_render` passes (S2-59 `renderjob.cpp:59`), melt's `transport` loop prints its progress and sleeps `{0, 40000000}`, 40 ms, until the consumer stops (MLT 7.22.0, `src/melt/melt.c:413`, `:480`; S2-61). Whether a job ends on one such sleep with nothing else of the tree running follows where the last sleep falls against the encode's end.
- **The exception's ground does not fit.** 9.6 D29's exception carries "a value whose spread follows the machine, not the program" with its half-width; its two uses here followed the runner's disk (D58) and `khugepaged` (D87).

Not taken: the block per run carried with its half-width at five repeats under the exception.

No file changed yet.

## D110 — the Kdenlive export campaign's raw records are release `meas-ci-background-2026-10-03c` (2026-10-04)

By 인지오's decision, the method's §7. The release is created at the fold-in commit. It holds, each archive without its `pool-cache/`:

- the 30 pooled landings (runs #162–#174);
- the dry runs #160 and #161 of the fixed driver (D105), their `perf.data` kept;
- the dry run #157 of the first driver, whose shortcut opened no dialog, its `perf.data` kept;
- the reports of the 28 jobs the machine gate stopped, 26 of the campaign's and 2 of the dry runs'.

No video is in it: the clip and the output appear as their size and SHA-256. The archives carry the project file, the playlist Kdenlive wrote and the dialog's screenshots.

No file changed yet.

## D111 — the Kdenlive export campaign holds at 30 repeats; `cpu-batch`'s `kdenlive_render` folded in, `ffmpeg`'s tables retired, the three render files rebound (2026-10-04)

The campaign of D101–D110, `meas-ci:background:2026-10-03c`, run under `../measurement-campaign-workflow.md`. It is recorded in `campaign/kdenlive/` (method, machine draws, `results/pooled.json`, `results/results.md`) and in `measurement-campaign-record.md`.

- **Runs.**
  - The dry runs: #157, the first driver, whose shortcut opened no dialog; #158 and #159 stopped at the gate; #160 and #161, the fixed driver (D105).
  - The first batch, repeats 1–5 (#162–#164).
  - The batch to the projection, repeats 6–30 (#165–#174; D109).
  - In all, 56 campaign jobs: 30 landed on the EPYC 7763, 26 stopped by the machine gate.
- **The rule holds at 30 on all three values.** The CPU total is 16.545 s ±0.8 % (16.055–17.305 s). The run between voluntary blocks is 1.932 ms ±0.8 %. The block per run is 4.593 µs ±13.1 %, within the 1 µs floor. Every repeat is valid:
  - the layer built, with the 427 packages `apt-get install kdenlive ffmpeg` added, one set across the landings;
  - `kdenlive` 4:23.08.5-0ubuntu4, `melt` and `libmlt7` 7.22.0-1build6, `libavcodec60` 7:6.1.1-3ubuntu5, `libx264-164` 2:0.164.3108+git31e19f9-1, `frei0r-plugins` 1.8.0-1build3;
  - the clip one SHA-256 across the landings, cached at 1.0000;
  - the kernel's mode `always`;
  - the dialog opened by the shortcut, `kdenlive_render delivery /usr/bin/melt-7`, the playlist's consumer D103's settings;
  - the same output in every landing, 600 H.264 frames at 1920 × 1080 and 938 AAC frames, 966,107 B, one SHA-256 and one x264 options string.
- **Reported.**
  - The job is 4 processes of 14 threads, 16.181–17.427 s, saturation 0.9920–0.9946. `melt-7` holds 0.9960–0.9963 of the CPU; its busiest thread 0.682–0.691, the next 0.183–0.192.
  - 8,454–8,641 runs a repeat; 1.8–50.5 ms of blocks a job, 26 of 30 jobs ending on one 40 ms block, melt's progress sleep (D109); 47 disk waits over the 30 landings, 3 uninterruptible waits.
  - Kdenlive's window held 66.9–78.7 ms of the measured CPU during the job.
- **Release.** The raw records are release `meas-ci-background-2026-10-03c`, published on 인지오's go-ahead (D110).
- **Fold-in.**
  - `cpu-batch` gains the program `kdenlive_render`. Its `kdenlive_render_run` and `kdenlive_render_block` are written by `batch_fold_in.py` from `results/pooled.json`, their source `meas-ci:background:2026-10-03c` (D105, D106).
  - `cpu-batch`'s `ffmpeg_run` and `ffmpeg_block` leave, with the `ffmpeg` program (D105). Its scope, stats, run and notes are restated: `clamscan` from 9.6's campaign, `python3` and `kdenlive_render` from 9.10's.
  - `docs/references.md` gains `kdenlive` and `mlt` (deployed-system, verified).
  - `dataset/tools/wlc/grid.py` places `kdenlive_render` at tier 1 (D107).
  - The test fixture `fx-mixed` binds `kdenlive_render` in place of `ffmpeg`.
- **Rebound.**
  - `c1-render`: `kdenlive_render` on `cpu-batch` from 2 s, `total_work` 16.545 s, `program: kdenlive_render`. The segment keeps its 60 s: the export ends by 46.039 s under every policy, 2 s plus 16.545 s of CPU plus 0.008 s of its blocks plus the editor's 27.486 s as compiled under the file's seed (D17; D78's arithmetic and form). Taken under 인지오's delegation, on D78. The preview render stays at 30 s.
  - `c7-render` (`c7.variant.yaml`): `c1-render`'s first C seconds, the export from 0 s, the editor departing at C, focus 2 s to C − 2 s, the preview render at 8.2725 s, its window's middle (D44, D96). The compiler cuts the render at the editor's departure (`wlc/compiler.py`, the operation window's end at the task's `depart`): about 8.3 s of it. One segment, `background_wanted: false`, `initiated: scheduled`, still a pre-committed miss (D78's form, as D90's and D100's).
  - `c2-p3a`: segment 1 keeps its 60 s; `kdenlive_render` from 60 s, `total_work` 16.545 s, ending by 99.55 s under every policy (D108). `c2-p3b` is unchanged.
  - C is 16.545 s, the export's `total_work`, which the batch loop compiles exactly.

Recompiled (`compile.py --allow-window`): 6 of 100 artifacts change beyond the library's hash, the three files in both modes. Demand (`-single`):

| file | before | after | |
|---|---|---|---|
| `c1-render` | 0.9581 | 0.7339 | calibration |
| `c7-render` | 0.9581 | 1.6189 | calibration |
| `c2-p3a` | 1.0423 | 0.5552 | the demand window (D17) |

Lint reports six demand-window files: `c2-p1a`, `c2-p1b`, `c2-p3a` (now 0.56), `c3-creation`, `c3-evening` and `c3-workday`. `compile.py --check --allow-window` and `batch_fold_in.py --check` pass. Tests: 383 passed, 1 skipped, 1 xfailed.

Restated tests:
- `render` leaves `C7_SAME_NAME` for `test_c7_render_is_its_bases_first_c_seconds`;
- `test_the_batch_tables_regenerate_from_the_pooled_records` names `cpu-batch`'s `kdenlive_render`, its table count unchanged at 89;
- the background tests add the `kdenlive` job, its root rule, its list and its settings' text against 9.5's.

Hands to 9.14:
- `c1-render`'s, `c7-render`'s and `c2-p3a`'s terms on the measured export;
- P3's terms over segment 1 (D108);
- `c2-p3a` in the demand window at 0.56.

Hands to 9.12 and 9.15:
- the scenario catalog's S7 row ("ffmpeg (render children)"): Kdenlive's `kdenlive_render` and its `melt-7`;
- `building-plan.md` §3 C1 (render {kdenlive, ffmpeg}) and C2 P3;
- `cpu-batch`'s scope without `ffmpeg` (D10's hand-off).

## D112 — the periodic backup is started by Déjà Dup's own monitor in every repeat; the job is the tree of the `deja-dup` it starts (2026-10-04)

> Corrected by D119: every backup runs the `--dry-run` sizing pass, automatic ones included (`ToolJob.Flags` is a plain enum).

By 인지오's decision, how D8's campaign starts the scheduled run. In every repeat, after the first backup and the change set (D115, D118), `deja-dup-monitor` is started in the user's session with `last-backup` older than the schedule's last slot. When its own 120 s wait ends it finds the backup due and starts it. The job is every process of the tree rooted at the process the monitor starts, from its first schedule-in on the measured CPU to its exit.

Grounds:

- **Déjà Dup 45.2's scheduled run** (S2-62). The monitor autostarts at login and waits 120 s before its first check (`monitor/monitor.vala`, `begin_monitoring`). It counts the backup due once `last-backup` is older than the latest slot of the period, a fixed time between 2 and 4 AM drawn from the machine id (`libdeja/CommonUtils.vala:196–254`). It checks game mode, power saver and, for a remote location only, the network (`monitor/ReadyWatcher.vala`). Then it runs `chrt --idle 0 ionice -c3 deja-dup --backup --auto` (`monitor/BackupInterface.vala:39`; `CommonUtils.vala:107–149`, `nice_prefix`), so the whole tree runs in the kernel's idle CPU class and idle I/O class.
- **What `deja-dup --backup --auto` runs** (S2-62, S2-63). `duplicity collection-status`, then `duplicity incremental … --volsize=200`; an automatic run skips the dry run that sizes a progress bar unless the backup is a full one (`app/AssistantBackup.vala`, `create_op`; `libdeja/duplicity/DuplicityJob.vala:370–415`). After a successful backup it chains a verify, `duplicity restore` of its own check file (`libdeja/OperationBackup.vala`, `operation_finished`; `libdeja/OperationVerify.vala`). An encrypted backup runs `gpg --symmetric` for each volume (`duplicity/gpg.py:134–210`).
- **The program's own trigger** (D101's form). Kdenlive's export was started through its render dialog, not by running `kdenlive_render`.

Not taken: the driver running the monitor's command line itself, with no monitor. The tree and the classes are the same, but the trigger would be the driver's, and the prefix copied from the source rather than applied by Déjà Dup.

The names the run shows are read from it (D25).

No file changed yet.

## D113 — the backup's state is D37's chroot at T0 with Déjà Dup installed by apt (2026-10-04)

By 인지오's decision. The campaign runs in D37's chroot of the English default install, built from the archive at D64's T0 (2026-09-22T17:00Z). On the harness CPUs, `apt-get install deja-dup` installs from the same snapshot with apt's defaults, as the DKMS campaign installed its driver package (D49) and the Kdenlive campaign Kdenlive (D102). The user is the Tracker campaign's.

Grounds:

- **One state across 9.10's campaigns** (D82, D94, D102).
- **The same backup stack as the extended install** (S2-01, S2-64). The extended layer (`minimal.standard`) adds `deja-dup` 45.2-1build2, `duplicity` 2.1.4-3ubuntu2, `librsync2t64` 2.3.4-1.1ubuntu2, `python3-fasteners`, `python3-monotonic`, and `python3-paramiko`, `python3-bcrypt` and `python3-nacl`, `duplicity`'s recommends. At T0 the archive's release pocket has `deja-dup` and `duplicity` at those versions with no update in either pocket. `deja-dup`'s own recommends, `gvfs-backends` and `packagekit`, and the keyring, `gnome-keyring`, are in the default layer.
- **Ubuntu ships Déjà Dup unpatched** (S2-62). The source package 45.2-1build2 has an empty patch series; its build enables PackageKit, with borg and restic off.

Not taken: the default layer plus the extended layer's 223 packages. Its other ~215 are applications that leave the home untouched until run, among them Thunderbird as a snap, which a chroot cannot install.

No file changed yet.

## D114 — the backups go to an external drive, the location Déjà Dup's help points to; a loop-mounted ext4 stands in (2026-10-04)

By 인지오's decision, D8's open item "the first backup's destination", in two steps. Déjà Dup's default location, `auto`, resolves to Google Drive (`libdeja/BackendAuto.vala`), which needs an account the runner does not use. The backups go to an external drive. The stand-in is an ext4 filesystem in a sparse image on a loop device with direct I/O, mounted in the chroot at `/media/<user>/<label>`. Déjà Dup uses it through its `local` backend, the folder at the drive backend's default `$HOSTNAME` under the mount (`org.gnome.DejaDup.Drive` `folder`, default `'$HOSTNAME'`).

Grounds:

- **Déjà Dup's help** (S2-62, `help/C/prefs.page:29–30`): "If you'd like to use an external drive as a storage location, plug it in and it will show up in the list." And: "While you can choose a local folder for your backups, this is not recommended. If your hardware fails, you will lose both your original data and your backups all at once."
- **The two backends hand `duplicity` the same location** (S2-62). Both `local` and `drive` are file backends, and `duplicity` gets `gio+file://<path>` (`DuplicityJob.vala:213–220`), so it writes the same way to either. The `drive` backend finds its drive by UUID through GIO's volume monitor, which needs udisks, absent in a chroot. What it adds over `local` is that readiness check and the mount, both outside the job.
- **A separate filesystem and block device** (Q6, by 인지오's decision). `duplicity` stages each volume in a temporary folder on the home's filesystem (`CommonUtils.vala:654–719`, `get_tempdir`) and copies it to the location through GIO. Onto a drive the copy crosses filesystems, and the volume's flush waits on that drive's device. A loop device with direct I/O keeps both.

The first decision, an external drive on the runner's second disk, rested on a second disk that today's runners do not have. The Kdenlive campaign's landings record one 150 GB virtual disk, `sda`, with `/` and `/mnt` both on `/dev/root` (run 37124818629). 인지오 then chose the loop-mounted filesystem.

Stated: the drive is the runner's own disk behind a loop device. The loop driver's kernel threads carry its I/O, outside the job, and are reported beside it when they run on the measured CPU.

Not taken: a folder outside the home on the chroot's own filesystem (no separate filesystem or device); the `local` backend's own default, `~/<hostname>`, on the home's filesystem, the location the help warns against.

No file changed yet.

## D115 — the change set is seven days of Cumulus's personal-machine rates, by 9.7's method (2026-10-04)

By 인지오's decision, D8's open item "the change set and its ground". Between the first backup and the measured incremental, the set takes seven days of the daily rates of the one personal-machine trace in the records. That is Cumulus (Vrable, Savage and Voelker, FAST 2009; 9.7's T9-S1-05): 10.3 MB new and 29.9 MB changed a day over a 2.37 GB home directory, 223 days. Scaled to the set: new files totalling 7 × 0.4346 % = 3.042 % of its bytes (304.2 MB), and changed files totalling 7 × 1.2616 % = 8.831 % (883.1 MB). Which files change, how, and the new files' content follow 9.7's seeded method and seed (`fileset.py change`; 9.7 method §2). The changed part is an upper bound, stated.

Grounds:

- **The period is Déjà Dup's.** The periodic backup runs every 7 days once turned on (D8; S2-03, `periodic-period` default 7).
- **The rates are the one personal-machine trace's.** 9.7's search for bytes changed between consecutive backups found no population figure and one personal machine's daily rates (9.7 `search/T9-S1-literature.md`, synthesis (c)). Its weekly figures are shared servers': students' home directories, an unmodified file modified within a week with 0.14 % probability (Tarasov et al., ATC 2012, Table 2; 9.7's T9-S1-19; file counts); university home-directory servers, more than 98.5 % of bytes repeated week to week (Meister and Brinkmann, SYSTOR 2009; 9.7's T9-S1-27).
- **New data adds up; changed data is bounded.** Each day's new files are new, so a week's new data is seven days'. The trace counts a file once for each day its hash changes (Cumulus §5.2.1), and a weekly incremental takes it once. Seven days' changed data is the week's upper bound, and no source gives the union.

Not taken: 9.7's one-day change set unchanged, a day's change under a weekly schedule; seven days of new data with one day's changed files, the lower bound, as if the same files changed every day. Cumulus names two such files (§5.4.4), and two examples do not make a weekly union.

No file changed yet.

## D116 — the incremental starts warm (2026-10-04)

By 인지오's decision, on 9.7 D8. After the change set, the set and Déjà Dup's cache folder (`~/.cache/deja-dup`, its signature chain) are read whole on the harness CPUs before the monitor starts. The set's cached fraction is measured with `fincore`, and validity asks at least 0.99. The cache folder's fraction is recorded beside it.

Grounds:

- **The backup archetype's precedent** (9.7 D8). The same set and the same kind of job read the warm phase: a cold phase's read waits would be the runner's datacentre disk, documented only as "SSD", not a desktop drive. The export started warm too (D104).
- **No source states the cache state a desktop backup starts in.** Both states are design. Déjà Dup's help puts scheduled backups "in the middle of the night if possible" (`help/C/prefs.page:38`). A desktop off at night runs the overdue backup at the monitor's first check after the next login, when the cache is cold.
- **Warm fits the runner.** 9.7 held the set at a cached fraction of 1.0000 in 16 GB. D75 chose cold for the Tracker index partly because its set was 2.5 times the runner's memory.

Not taken: cold, `sync; sysctl vm.drop_caches=3` before the monitor starts (D75's form).

No file changed yet.

## D117 — Déjà Dup's settings are its defaults, the backup encrypted and its password remembered (2026-10-04)

Taken under 인지오's delegation (2026-10-04), D8's open item "Déjà Dup's settings left at their defaults", read from the source (S2-62), as D103 read Kdenlive's profile.

- **Folders:** `include-list` `[ '$HOME' ]` and `exclude-list` `[ '$TRASH', '$DOWNLOAD' ]`, with Déjà Dup's own exclusions (`OperationBackup.vala`, `add_always_excluded_dirs`: `~/.cache` and its own cache, `~/.ccache`, `~/.steam/root`, `~/.xsession-errors`, its temporary folders, among others).
- **Tool:** `duplicity` (`tool` default `'duplicity'`), volumes of 200 MB (`DuplicityJob.vala:1333–1356`).
- **Schedule:** `periodic-period` 7. A fresh full backup is made after 90 days (`full-backup-period` 90). `delete-after` 0: backups kept forever.
- **Encryption on,** the first-backup page's default ("always default to encrypted", `app/AssistantOperation.vala:345`): `duplicity` runs `gpg --symmetric --force-mdc --pinentry-mode=loopback`, gpg's own compression on (S2-63).
- **"Remember password" on,** its one departure from the defaults. The switch is off by default (`AssistantOperation.vala:370–373`). An automatic run that finds no stored password emits `passphrase_required` and waits for the user (`libdeja/Operation.vala:291–317`), so with the default no scheduled run finishes unattended. The password goes to the default layer's `gnome-keyring` through libsecret (`CommonUtils.vala:605–630`). The keyring's and the backup's passwords are design strings.
- **Location:** D114.

The idle classes (D112) are recorded as 9.6 D17 recorded Tracker's SCHED_IDLE: in the entry's notes, the task model carrying no declared class (9.11's).

No file changed yet.

## D118 — the incremental's start: the first backup through Déjà Dup's assistant, a week's passing written into its settings, the session on the measured CPU; the runner's kernel (2026-10-04)

Taken under 인지오's delegation (2026-10-04), on D101, D104 and D112.

- **The set.** Mahoney's 10 GB set (`mahoney-10gb`, 9.7 D7), fetched, checked against its pinned SHA-256 and manifest and extracted on the harness CPUs by 9.7's tooling. Its tree `10gb/`, as `zpaq` restores it, is placed directly in the user's home as `~/10gb`.
- **The first backup.** Run by Déjà Dup's own first-backup path, `deja-dup --backup` ("Back Up Now"), as the user on the harness CPUs, in a session of its own with the keyring unlocked. The location is written beforehand with `gsettings` as the location page stores it (`backend` `'local'`, `local` `folder` `/media/<user>/<label>/$HOSTNAME`). The assistant's folders and location pages are taken as they open, and its password page filled: the password twice, "Remember password" turned on (D117). The driver works the window from the harness CPUs by its screenshots, as the Kdenlive export's did. Not measured; its duration, log and the files it wrote are recorded.
- **A week passing.** After the first backup, "Back Up Automatically" (`periodic`) is turned on with `gsettings`, the change set is applied (D115), and `last-backup` and `last-run` are set back 8 days. The monitor then finds the backup overdue at its first check. `nag-check`, which the first backup's verify sets, is left as written: the two-monthly restore test, with its password prompt and fresh cache (`OperationVerify.vala`; `CommonUtils.vala:352–373`), is not due. The measured run is the ordinary weekly incremental. The restore test, about one weekly run in nine, is stated as not depicted.
- **The warm start** (D116).
- **The session.** Xvfb on the harness CPUs, its socket visible in the chroot; a session bus of the user's own (`dbus-run-session`), the keyring unlocked in it, and `deja-dup-monitor` started in it with `DISPLAY` set, the whole session on the measured CPU. The monitor's child inherits its affinity, so the backup runs on the measured CPU, as on a one-CPU desktop (D104's form). No session manager starts the monitor, so the desktop file's own 120 s autostart delay (`X-GNOME-Autostart-Delay=120`) is not applied; it falls before the job.
- **The job** (D112): every process of the tree rooted at the first process in the phase that executed `/usr/bin/deja-dup`, the one the monitor starts through `chrt` and `ionice`, from its first schedule-in to its exit. A process of the tree that outlives `deja-dup`, such as an agent `gpg` starts, counts only until that exit. The monitor, the session bus, the keyring daemon, anything the bus starts and the loop device's kernel threads are outside the job, reported by `comm` beside it.
- **What the chroot lacks.** No system bus: PackageKit's dependency check (`Operation.vala:362–440`) and GIO's volume monitor fail at once, and Déjà Dup goes on by design. No notification server for its notices.
- **The phase.** From the session's start to the exit of that `deja-dup`, the monitor's 120 s wait inside it; no cap of its own. The workflow's job limit is 330 minutes.
- **The venue.** The runner's kernel as recorded, its transparent huge pages in `always` mode, recorded before and after the phase (D104). The disk's I/O scheduler is recorded: the idle I/O class takes effect only under a scheduler that implements I/O priorities.

The entry's form — by 9.6 D7's criterion — and the list are fixed after the dry run. The job's size against the segments is read from it (D17).

No file changed yet.

## D119 — the incremental is a new entry in the batch-loop form over the whole tree; `file-backup` leaves at fold-in (2026-10-04)

By 인지오's decision, 9.6 D7's criterion applied to the dry run on the 10 GB set (run 37174980221, #182, the EPYC 7763). The incremental is a new entry in the batch-loop form. Its two tables are the run between voluntary blocks and the block after each run, pooled over every process of the job's tree (D112), and it carries the job's CPU total as measured (D17). At fold-in `file-backup`, `borg`'s first backup into a new repository (9.7 D6), leaves `dataset/archetypes.yaml`: once the backup files rebind, no file binds it (D8's last item), the rule D16 applied to `renderer-visible` and 9.7 D30 to `network-bulk`. The list is the HandBrakeCLI and Kdenlive campaigns': over the job, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it, and the CPU total, tested by its per-repeat values (D17).

Grounds (the dry run):

- **Runnable throughout, on no dominant thread.** The job is the tree of `deja-dup`, 170.70 s from its first schedule-in to its last row, with 169.686 s of CPU (perf; taskstats 169.670 s): saturation 0.9940. By program, `duplicity` holds 0.569 of the CPU over its eight runs, `deja-dup` 0.291, `gpg` 0.135 and `gpg-agent` 0.004. The busiest threads are the incremental's `duplicity` at 0.322, `deja-dup`'s main thread at 0.291 and the dry run's `duplicity` at 0.232; each `gpg` holds about 0.03. 9.6 D7's criterion: a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry. The transcode took its own entry with 23 threads, the busiest at 0.334 and the next at 0.205 (D97); the export stayed in `cpu-batch` with its busiest thread at 0.689 (D105).
- **`deja-dup` runs beside each `duplicity`.** In the dry run's 64.5 s, `duplicity` took 39.36 s of CPU and `deja-dup` 24.72 s. In the incremental's 100.7 s, `duplicity` took 54.68 s, `deja-dup` 24.51 s and `gpg` 20.42 s. The verify took 4.2 s.
- **The blocks are short and the waits few.** 114,809 runs between voluntary blocks, mean 1.478 ms; the block after a run has a mean of 2.77 µs, 0.318 s over the job. 285 disk waits, 0.204 s in all; 95 uninterruptible waits.
- **A different program from the one `file-backup` describes.** Déjà Dup and `duplicity` making a weekly incremental replace `borg`'s first backup. D97 and D105 retired `cpu-batch`'s `HandBrakeCLI` and `ffmpeg` tables when their files bound the measured job.

Also recorded:

- **The run's order,** from the command lines the driver read (method §8):
  1. `duplicity --version`;
  2. `collection-status --no-encryption`, then an `incremental --dry-run` without the password, ending within 0.3 s. Déjà Dup takes `duplicity`'s asking for the password as a bad password and restarts the job with the keyring's (S2-62 `DuplicityJob.vala:1034–1038`; `Operation.vala`, `connect_to_job`);
  3. `collection-status`, then `incremental --dry-run`, 64.5 s, with one `gpg --decrypt`;
  4. `incremental`, 100.7 s, with one `gpg --decrypt` and six `gpg --symmetric`, writing four new volumes;
  5. the verify's `collection-status` and `restore --path-to-restore=home/user/.cache/deja-dup/metadata`, 4.2 s, with two `gpg --decrypt`.
- **Other processes in the tree.** A `gpg-agent`, started by the incremental's first `gpg --symmetric`, outlives the job. At its start `deja-dup` runs the monitor through `chrt` and `ionice`, and that monitor exits on finding the bus name held (S2-62 `WidgetUtils.vala:30–47`).
- **D112 corrected.** Every backup runs the dry run, automatic ones included. `ToolJob.Flags` is a plain enum, `{ NO_PROGRESS, NO_CACHE, }`, so `NO_PROGRESS` is 0 (S2-62 `ToolJob.vala:43–46`). `Operation.vala:131–132`'s `job.flags |= ToolJob.Flags.NO_PROGRESS` sets no bit, and the dry run's test, `(flags & NO_PROGRESS) == 0`, holds for every job. D112 read the code's intent, not its effect.
- **The state.**
  - The layer, plus the 9 packages `apt-get install deja-dup` added.
  - The first backup by the assistant: 526 s, 5,025,070,033 B in 24 volumes, the password in the keyring.
  - The week's change set: 9,729 changed files (883,122,363 B, 480,780,930 B of them rewritten) and 304,219,409 B of new files.
  - The set cached at 0.9995 and Déjà Dup's cache folder at 1.0000.
- **The classes.** `deja-dup` runs in `SCHED_IDLE` and the idle I/O class on the measured CPU. The disks' I/O scheduler is `none`, under which the I/O class has no effect (D118).
- **Beside the job,** on the measured CPU: the runner's agents (`provjobd…` 492 ms, `.NET TP Worker` 141 ms), the session's bus-started services (`xdg-desktop-portal` 80 ms, `dbus-daemon` 61 ms, `gdbus` 51 ms) and kernel workers.
- **The dry runs before it** (method §8): #176 and #177 fixed the first backup's driver; #180 ran the whole job on the 100 MB subset, 6.8 s; #175, #178, #179 and #181 stopped at the gate.

No file changed yet.

## D120 — the task shows `deja-dup`; the entry is `incremental-backup` (2026-10-04)

By 인지오's decision, D119's open names. The task shows `deja-dup`, the `comm` of `/usr/bin/deja-dup` as the dry run observed it (D25). The entry is `incremental-backup`.

Grounds:

- **A tree's task shows its root.** `unattended-upgr` (D40) shows over a tree whose CPU went mostly to `localedef` and `dpkg`; `dkms` (D55) over its compile jobs; `tracker-miner-f` (D74) over its extractor; `kdenlive_render` (D106) over `melt-7`. `deja-dup` is the process the monitor starts (D112), and its own main thread holds 0.291 of the CPU (D119).
- **The id names what was measured.** It is a weekly incremental, the counterpart of the leaving `file-backup`'s "first backup into a new repository" (9.7 D6). The files state the trigger, `initiated: scheduled`, and `c7-backup` flips only the wanted label on the same run (D9).

Not taken: the task showing `duplicity`, which holds 0.569 of the CPU over its eight runs; the id `scheduled-backup`, which would put into the entry what the files' labels carry.

No file changed yet.

## D121 — `deja-dup` is familiarity tier 1 (2026-10-04)

By 인지오's decision, D27's rule applied to D120's name: `deja-dup` is a new program's name, placed by the ladder's definitions at tier 1, transparent. Labelled design, as D27's tiers are.

Grounds:

- **The ladder's definitions** (`docs/workload/building-plan.md` §3 C5): 1 transparent (`firefox`, `blender`), 2 semi-opaque (`soffice.bin`, `gamescope`), 3 opaque (`tracker-miner-fs-3`, `cc1`, `baloo_file`); familiarity "defined corpus-relative, not human-relative". `deja-dup` is the program's own name, which its package describes as "a simple backup tool" (S2-03, `deja-dup` 45.2-1build2's control). `borg`, the backup name the files bound until now, is tier 1.
- **The C7 property** (`building-plan.md` §3 C7): "tier 1 so no pair changes familiarity tier". Pair P3 keeps one tier in both files, `kdenlive_render` in `c2-p3a` against `deja-dup` in `c2-p3b` (D107).

Not taken: tier 2, on the name being a pun whose role the string does not state.

Applied at rebinding: `dataset/tools/wlc/grid.py`'s `NAME_TIERS`.

## D122 — the run between voluntary blocks splits in two modes: a batch to 30 repeats, then 9.6 D29's exception if it still fails (2026-10-04)

By 인지오's decision. At the first batch's five landings (runs #183–#186, `meas-ci:background:2026-10-04`), every repeat is valid. The CPU total (167.492 s ±2.8 %) and the block per run (3.24 µs, within the 1 µs floor) hold the rule; the run between voluntary blocks does not, 1.734 ms ±26.3 %, 72 repeats projected. The campaign runs on in one batch to 30 repeats, repeats 6–30 (9.7 D26), the Kdenlive campaign's count (D109). If the value still fails there, it is carried over the 30 repeats under 9.6 D29's exception with its 95 % half-width, the two modes' shares stated.

Grounds:

- **The value splits in two modes.** Its per-repeat means are 1.40 and 1.41 ms in repeats 2 and 4 and 2.02–2.09 ms in repeats 1, 3 and 5, with 118,619 and 117,944 runs against 81,341–83,209. The CPU totals agree (165.2–174.0 s).
- **The split is `deja-dup`'s, in the dry run.** `deja-dup`'s main thread holds the same CPU in every landing (47.5–50.7 s). In the dry-run stage of repeat 1 it runs 16,723 times, median 1.49 ms, between blocks of median 2.46 ms; in repeat 4 it runs 53,464 times, median 0.055 ms, between blocks of 0.072 ms. The incremental stage is the same in both, about 19,000 runs of median 1.4 ms. `duplicity`, whose `--verbosity=9` log `deja-dup` reads through a pipe (`--log-fd`, S2-62 `DuplicityInstance.vala:61–90`), wakes it 36,276 times in repeat 1 and 71,836 in repeat 4. The two processes share one CPU, both in `SCHED_IDLE`. In one mode the reader reads after nearly every write; in the other it reads in batches. The dry run #182 was in the ping-pong mode (114,809 runs).
- **The exception's ground, if taken.** 9.6 D29 carries "a value whose spread follows the machine rather than the program" with its half-width; its uses followed the runner's disk (9.6 D29, D58) and `khugepaged` (D87). Here the spread follows the kernel's interleaving of a pipe's writer and reader on the one measured CPU, the venue's, as D87 read `khugepaged`. It is stated as that, not as the program's own timer, which D109 did not take under the exception.
- **Thirty landings weigh the modes as drawn.** A table pooled over five landings mixes the modes 3:2.

Not taken: running on to the projection, 72 repeats, about 15 hours of jobs at the gate's rate (D109's choice for melt's timer); the exception at five repeats.

No file changed yet.
