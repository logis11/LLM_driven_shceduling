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
