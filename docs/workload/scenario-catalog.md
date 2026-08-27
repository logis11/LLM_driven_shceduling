# Workload Scenario Catalog — Scenarios, Processes, and Source Attribution
> Status: normative · Created 2026-08-25 · Updated 2026-08-27

> Companion to source-vetting and Q7. Naming decision: **Linux-native process names** (the daemon reads Linux /proc; canonicalization and cgroup logic assume the Linux process model). Where a taxonomy source names a Windows application, the mapping is recorded in the Source column.
>
> **Schema decision — names only, no paths.** The grounding sources attest to process *names* (CpsMark+ Table 2, SYSmark app lists, the ananicy catalog); none attest to executable paths. Paths would be authored values with no external source, violating the grounding rule, and would contaminate the recognition claim (name semantics vs. path heuristics). The workload schema therefore carries names only. Consequences: (a) recognizer and whitelist receive identical name-only input — clean comparison; (b) Family 5 spoofing is authored as *name collision* (a process simply bearing a trusted name), which is exactly the stated resolution limit; path-mismatch detection is future work; (c) Role D /proc snapshots will capture paths anyway as raw data, outside the dataset schema.
>
> Scenario ≠ segment: a segment in a workload file is one scenario (or a scenario + background combination) with a mode/attribute label attached. This catalog is the parts bin; workload files compose from it.

| # | Scenario | Processes (names) | Taxonomy source(s) |
|---|---|---|---|
| S1 | Document / office work | soffice.bin · evince | CpsMark+ Table 2 document manipulation (Word/Excel/PowerPoint/Acrobat → LibreOffice/evince); SYSmark 30 Office Applications; PCMark 10 Productivity (Writing, Spreadsheets) |
| S2 | Web browsing | chrome (+ renderer/gpu children) · firefox | PCMark 10 Essentials (Web Browsing); CpsMark+ Internet service (Chrome 73); SYSmark 30 General Productivity (Chrome 106) |
| S3 | Video conferencing | zoom · teams-for-linux | PCMark 10 Essentials (Video Conferencing) |
| S4 | Email / async communication | thunderbird · slack | CpsMark+ Internet service (Outlook → Thunderbird); CpsMark+ CA workflow (email delivery stage) |
| S5 | Voice chat companion (overlay on S9/S2) | discord (+ renderer children) | ananicy/CachyOS catalog (comms class); LAVD gaming context (companion apps observed alongside games) |
| S6 | Photo / image editing | gimp · darktable | PCMark 10 DCC (Photo Editing, ImageMagick); SYSmark 30 Photo Editing (Lightroom/Photoshop → darktable/GIMP); CpsMark+ graphic design (Photoshop CC 2019 → GIMP) |
| S7 | Video editing / rendering | kdenlive · blender · ffmpeg (render children) | PCMark 10 DCC (Video Editing, Rendering & Visualization); CpsMark+ multimedia processing (Premiere/After Effects/3ds Max → kdenlive/Blender); SYSmark 30 Advanced Content Creation |
| S8 | Batch transcode (background bulk) | HandBrakeCLI · ffmpeg | CpsMark+ multimedia processing (HandBrake CLI 1.3.0 — verbatim, cross-platform); SchedCP batch workloads (video transcoding) |
| S9 | Gaming (native + Proton) | steam · steamwebhelper · gamescope · wineserver · <game>.exe (Proton) | PCMark 10 Gaming; Windows Game Mode (foreground-game category); LAVD characterization (wine/graphics/audio task chains); ananicy/CachyOS (Proton vs linux-native game classes) |
| S10 | Game/content download (background, wanted) | steam (download workers) · transmission-daemon | Steam client "Allow downloads during gameplay" setting (Valve — documents both the scenario and the wanted/unwanted decision as a real user-facing toggle); ananicy catalog (download class) |
| S11 | Software development: edit + compile | code · make · gcc · cc1 · ld · cargo · rustc | SYSmark 25 Productivity (software development / code compilation); kernel-build characterization (2,430 short-lived procs, arXiv 1705.05937); interbench Compile load; SchedCP (make -j) |
| S12 | ML training / local AI (background CPU/GPU hog, wanted) | python3 (pytorch train) · ollama | UL Procyon (local AI inference scenario); SchedCP evaluation (batch/ML-adjacent workloads on desktops-class machines) |
| S13 | Media playback (audio/video) | mpv · vlc · spotify | PCMark 10 Battery Video profile; interbench Audio (50 ms/5%) + Video (16.7 ms/40%) task models; ananicy audio class (nice −11) |
| S14 | File indexing (background, unwanted-deferrable) | tracker-miner-fs-3 · baloo_file · updatedb | ananicy/CachyOS catalog (ioclass idle indexer class); shipped defaults (GNOME tracker-miner, KDE baloo, plocate timers are stock background services) |
| S15 | Backup / sync (background) | rsync · borg · rclone | ananicy catalog (backup class, ioclass idle); SYSmark 30 General Productivity (archiving analogue) |
| S16 | Archive / compression burst | 7z · tar · xz | SYSmark 30 General Productivity (file compression/unpacking, WinZip → 7z); CpsMark+ document manipulation (WinRAR 5.91 → 7z); SchedCP batch (file compression) |
| S17 | Malware scan (background, unwanted-now) | clamscan · freshclam | ananicy catalog (AV/scan class); ClamAV stock scheduled-scan deployment pattern |
| S18 | System baseline (always-on, [system] scope) | gnome-shell · Xorg · pipewire · systemd · dbus-daemon | Canonicalization [system] scope (Q7); interbench "None/X" baseline; present in every segment by construction |

## Notes

1. **Coverage check against the taxonomy sources.** PCMark 10's three groups map to S1–S3, S6–S7, S13; SYSmark 30's four scenarios to S1, S2+S16, S6, S7; SYSmark 25 adds S11; CpsMark+'s four scenarios to S1+S16, S2+S4, S6, S7+S8; Procyon adds S12; Game Mode/LAVD/ananicy add S9–S10, S14–S17. Every scenario row cites external sources only — our own Family/driver-table definitions never appear in the Source column, since they are what this catalog exists to ground (citing them would be circular).
2. **Internal cross-references live here, not in the Source column.** Which experiments consume which scenarios is design intent, not grounding: the F2 load-bearing pair is S12 vs S14 (both one CPU-saturating process beside S11's editor, opposite correct policies); S10's wanted-download cell and S5's companion overlay are the F2 combination rows.
3. **Family 5 spoofing is authored by name collision** — a scripted process bearing a trusted name (e.g. chrome) with non-browser behavior. This is precisely the stated resolution limit of name-based recognition. Path-mismatch spoofing is out of scope (no path field in the schema); path-based verification is noted as future work.
4. **Verification tasks before freeze:** the meas-ci name-verification workflow (docs/workload/building-plan.md §7) confirms each name as it actually appears in comm/cmdline across distro containers (e.g. soffice.bin vs soffice, updatedb vs updatedb.plocate, cc1 visibility). Browser default: decided — chrome wherever a file needs "a browser," firefox only where the coverage-grid fill wants name variety (building plan §3).
