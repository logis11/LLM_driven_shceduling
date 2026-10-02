# Task 9.10 — Scenarios and timelines: decisions and remaining work

The decisions taken at stage 3 of 9.10 (`_dev/TODO.md`, (jioh, 9), 9.10; `_dev/research/jioh/research-slice-workflow.md`), recorded in full with their grounds in `_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md` as D1–D35 (stage 3) and D36 on (the campaigns), and the work they leave: the runner campaigns they create and the rebinding of the core-set timelines to the entries those campaigns produce.

## Scope

- The 50 core-set timelines, their five recipes, the scenario catalog and the registry entries that ground scenario and timeline claims, as the scope card (`_dev/research/jioh/task-9.10-scenarios-timelines/scope-card.md`, items 1–83) lists them.
- The runner campaigns D3–D5, D8, D10–D12, D15 and D21 create, each under `_dev/research/jioh/measurement-campaign-workflow.md`, their entries owned by 9.10.
- Rebinding each file to its new entry when the entry lands, with the sizes, names, tiers and source tags the decisions fix.
- The hand-offs each decision names to 9.12, 9.13, 9.14 and 9.15.

## Locked decisions

### 1. What the core set claims

The task sets and co-occurrence of the core-set files are design (D2), and so are the arcs' order (D29) and the calibration sizes: `lane_share`, file and segment lengths, arrival times, focus windows, the injections' identities, `c6-dual`'s co-occurrence and `c6-spoof`'s job (D31). What stays a realism claim: each program's existence under the name a file shows, each situation a file presents as happening, each bound entry's state against the state the file depicts, and counts.

### 2. References without a reachable copy

A reference or work whose copy is unreachable or paywalled is dropped; `zhang-chb15` leaves the registry (D1).

### 3. Unasked and user-started jobs

- **The unwanted job of the ten interactive attribute counterparts and `c2-p2b`** is the stock Ubuntu 24.04 unattended upgrade, observed on the runner, in place of `clamscan` (D3). It installs one real day's security updates, 2026-07-27's `glibc`, rebuilt from Ubuntu's snapshot service (D36), in a chroot of an English default install (D37), `apt.systemd.daily install` measured (D38), carried as a new entry, `package-upgrade`, in the batch-loop form over the whole process tree (D39), its task showing `unattended-upgr` (D40); each interactive counterpart is one segment as long as the job's CPU total, the job from 0 s (D41); pair P2's segment 1 takes the same length in both files (D42); `unattended-upgr` is tier 1 (D43); a cut counterpart keeps its base's focus margins and operation placement in proportion (D44).
- **`c7-compile`'s job** is an observed DKMS autoinstall of a real module (D4): NVIDIA's, installed by the driver package, measured in a campaign of its own (D46): `nvidia-dkms-595-open`, the production branch's open flavour (D47), built for 2026-09-23's security kernel `7.0.0-34` (D48), the state taken at 2026-09-22T17:00Z (D51), in D37's chroot with the installer's kernel and the driver package added (D49); the job is every process under the two DKMS hooks of the kernel day's install stage (D50).
- **The indexing files** show Tracker indexing a real user's file set, the Mahoney set, from an empty database: the first index at login (unasked) and the same work after the user's reset (asked) (D5). `c2-p1b`'s indexer carries that measured indexer's own tables (D6).
- **`c2-p2a`'s wanted download** is an install of another game the user starts during play (D7).
- **The scheduled backup** is Déjà Dup's periodic incremental run (D8). `c7-backup` stays the scheduled run's label flip, a pre-committed miss, its premise restated (D9).
- **The render** is Kdenlive's export of the `video-editor` entry's project (D10). **The transcode** is `HandBrakeCLI` on CpsMark+'s HandBrake workload (D11). **The training run** is PyTorch's basic MNIST example on the CPU (D12).

### 4. Sizes

Each batch job runs its measured whole at the input its decision fixed, and files lengthen to hold it (D17). The user's build is the measured kernel build whole: 2,908 object jobs at cap 8 (D18).

### 5. Operations, the mail send and the call

- The mail send is one `send` operation per mail file, and `network-bulk` has left the library (D13).
- The meeting files bind one `video-call` task (D14).
- Every focus window on an application that has an operation holds one of it, and an operation starts only inside focus (D20).
- `c6-fold`'s meeting segment carries a `chrome` task on `video-call` from 30 s (D30).

### 6. The browser

The tab count is Firefox's Linux telemetry median per-client peak, 4.67, so five tabs, with the renderer count observed on the runner for that tab set (D15). A file shows one browser window: `renderer-visible` has left the files and the library (D16).

### 7. Games

- A gaming file carries the game chain only, the game's other threads omitted and stated (D19).
- The logged-out Steam client stays beside the game, its state stated (D22).
- The chain's members carry the names of slide 16 of the chain's source, through a timeline binding (D26).

### 8. Launch work

An application a file starts mid-file runs its observed launch phase first. Applications whose source holds no launch data arrive steady, stated (D21).

### 9. Names, states and tiers

- The chat client is shown idle, its ids `chat` (D23).
- A task shows the observed program's name: `chrome` for the call, `mpv` for music, `element-desktop` for the chat client. `gamescope` leaves the gaming files, and the download keeps `steam`, stated (D24).
- A name is the kernel's `comm` (D25).
- New names take tiers by one rule: the same program keeps its tier, and a new program is placed by the ladder's definitions (D27).
- The session processes appear only in the idle files (D28).

### 10. Provenance

A timeline's bound values carry a source tag or a design label, checked by the linter (D32). The scenario catalog lists what the dataset binds, each line an existence claim that holds (D33). The registry's scenario entries are kept, restated, removed or minted as D34 sets out. The naturalistic generator's grounding and the negative result are restated to their sources (D35).

## Invariants

- Reliability of the dataset comes before development effort, by 인지오's direction at stage 3.
- Phase decisions 1–5 hold: verified citations, one observation per situation, design labelled as design, a four-class search before declaring an observation absent, and measurement on CI runners only.
- Every campaign follows `_dev/research/jioh/measurement-campaign-workflow.md`; its decisions are logged in 9.10's changelog.
- No Steam account is used (9.8 D6).

## Open items

Each flagged open in its decision, for the campaign's method or the rebinding:

- **D4, the DKMS build:** the entry's form and the comm, read from the dry run (D50).
- **D5, the Tracker index:** the file set's placement under the indexed directories; the job window.
- **D8, the backup:** the change set and its ground; the first backup's destination; Déjà Dup's process names.
- **D10, the export:** its process and names; the render profile's settings.
- **D11, the transcode:** the source clip and its length; the encoder settings that realise CpsMark+'s definition.
- **D12, the training run:** the dataset's placement; whether the run fits `cpu-batch`'s criterion.
- **D15, the renderers:** the sites, the window, and when the processes are counted.
- **D21, the launch phases:** the applications, cold or warm launch, and the launch phase's form.
- **The download's size** in `c2-p2a`: not among D17's jobs; design at scope-card item 56 until decided (D42).
- **At rebinding:** each file's length set by its jobs (D17); the new names' observed `comm`s (D25) and tiers (D27); the source tags (D32); the registry entries minted (D34).
- **Declared class:** the indexer's declared scheduling class, 9.11's.
- **Hub-and-spoke switching:** unsourced, left to the naturalistic generator's own search (D35).
