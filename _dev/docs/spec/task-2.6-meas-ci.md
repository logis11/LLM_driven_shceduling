# Task 2.6 — meas-ci measurement campaign

Fixes the measurement instruments, workflow structure, and data-handling rules for the CI campaign (building-plan §7). Parent: `2.6` in `_dev/TODO.md`; phase spec: `_dev/docs/spec/phase-2-workload-dataset-generation.md`. The scope-discipline package (structural/shape claims only, runner spec recorded, N-run spread, characterization-not-performance framing) is building-plan §7's and binds everything here.

## Scope

- Three workflow families in `.github/workflows/` plus the sidecar tools they run (released, re-runnable by anyone).
- First batches dispatched; the analysis fold-in (replacing the 15 `meas-pending` params) is this sub-task's tail, landing before 2.4's final compile.

## Locked decisions

### 1. Sidecar instruments

Two sidecars, both released: a process-lifecycle event tracer (netlink proc events — exact fork/exec/exit timestamps, giving true lifetime CDFs and fork rates even for sub-second processes) and a 1 s `/proc` state sampler (duty cycles, concurrent counts, runner state). Building-plan §7's sampler sentence is amended accordingly.

### 2. Data home: artifacts only, CI never writes to the repo

Workflows upload raw data as Actions artifacts. The fold-in is a human commit that downloads the cited runs, fits distributions, replaces the `meas-pending` values, and archives the used runs' raw data + summary in-repo (artifact expiry makes archiving part of fold-in, not optional).

### 3. Batches: N=5 matrix, dispatch-only

Each workflow runs its 5 repeats as matrix jobs inside one workflow run — one run id per citable batch (`meas-ci:<workflow>:<run>`), spread computed within the batch. Trigger is `workflow_dispatch` only; batches exist only when deliberately dispatched.

### 4. CLI workflow: kernel anchor, single corpus

Kernel `defconfig` build at `make -j8` (directly comparable to `ocallahan-atc17`'s characterization); the kernel source tree is the single corpus for `tar`/`xz`, `rsync`, `updatedb`/`plocate`, `clamscan`; the kernel.org tarball download doubles as the `network-bulk` measurement; a quiet-period capture grounds the `system-daemon` baseline.

### 5. Xvfb workflow: Chromium + Element Desktop

Chromium (renderer side of the OQ-3 comparison + renderer-count structure under opened tabs) and Element Desktop as the open-source `electron-comms` substitute — substitution and the unauthenticated-idle limitation stated at fold-in. No editor-class or toy Electron apps.

### 6. Name verification: three distros, two verification levels

`ubuntu` + `fedora` + `archlinux` containers; best-effort execution — headless-launchable processes verified live via `/proc` `comm`/`cmdline`, container-hostile desktop daemons verified binary-only from package manifests — with the level recorded per name. Output: a JSON table per distro (catalog name → observed strings → level), consumed by 2.4 authoring.

## Open items

- Distribution-fitting choices (estimators, censoring handling) are decided at fold-in with the data in hand.
- If Element's unauthenticated idle is too quiet to characterize `electron-comms`, the fold-in states the finding and the placeholder stays until a better substitute exists.
