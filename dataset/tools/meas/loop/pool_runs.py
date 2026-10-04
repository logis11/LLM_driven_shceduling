#!/usr/bin/env python3
"""Pool one application's landed repeats across a campaign's runs, check each repeat's validity, report the stability rule.

pool_runs.py <family>/<app> [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]
pool_runs.py build [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]
pool_runs.py background/<app> [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]

Every landed artifact (common.GATE_S or longer, success) of runs numbered N or later is downloaded under the work
directory — one folder per run for families with apps, one flat folder for build (its repeat indices never repeat) —
and pooled with the family's pool.py and --cpu-model common.MACHINE. Options after -- go to pool.py. Validity per repeat (_dev/research/jioh/measurement-campaign-workflow.md, the loop,
step 4): gate open on the machine; the replay sent every event of its window; operations completed; non-zero return
codes other than perf record's 130 (its SIGINT stop) and freshclam's 2 with a recorded database; for build, one
ClamAV signature database across the repeats whose clamscan is pooled (9.6 D27); for background, the set's archive and manifest matching their pins and the
tree verified after each change set, every SteamCMD phase reporting its install complete, one app build across repeats;
for desktop, the renderer count meeting the minimum the job wanted, the page server answering, Element's session having
reached the homeserver, and one origin count across repeats (9.8 D13); for session, the steady edge found the terminal idle state, the pin
applied without failure and no user-space work outside the four entries on the measured CPU (9.9 D12–D14).

--exclude leaves a repeat out of the pool, --exclude-why states why in the printed lines and in the pooled record
(`excluded_repeats`); a repeat the validity step fails counts for nothing (workflow guide, the loop, step 4), and the
rule, the projection and every value are then read over the rest. The artifact is moved to <pool folder>-excluded, out
of the folder pool.py reads, and is not downloaded again.
"""

import json
import os
import subprocess
import sys

import common


# the phases run.sh starts under shape_on (9.7 D11, D27): each must record its shaper installed
SHAPED_PHASES = ("steam-fresh-shaped", "steam-fresh-untraced", "steam-update-shaped")


def shaping_notes(r):
    """9.7 D27: the shaper carried the download — in every phase run under shape_on the shaper installed (shape.<phase>
    1), and the bytes through ifb0 are at least 90 % of the bytes received."""
    notes = [f"{ph} not shaped: the shaper did not install" for ph in SHAPED_PHASES
             if f"shape.{ph}" in r and r[f"shape.{ph}"] != "1"]
    for x, v in r.items():
        if x.startswith("shape.") and x.endswith(".through_ifb_bytes"):
            ph = x[len("shape."):-len(".through_ifb_bytes")]
            rx = r.get(f"net.{ph}.rx_bytes")
            if rx and int(rx) > 0 and int(v or 0) < 0.9 * int(rx):
                notes.append(f"{ph} not shaped: {v} B through ifb0 of {rx} B received")
    return notes


def kv(path):
    try:
        return dict(line.rstrip("\n").split("=", 1) for line in open(path) if "=" in line)
    except OSError:
        return {}


def lines(path):
    try:
        return sum(1 for _ in open(path))
    except OSError:
        return None


def validity(family, dirs, entry):
    """One line per repeat; returns the number of repeats with a problem."""
    streams = os.path.join(common.REPO, "dataset/meas/streams")
    win = json.load(open(os.path.join(streams, "windows.json")))["windows"] if os.path.exists(os.path.join(streams, "windows.json")) else {}
    alt = json.load(open(os.path.join(streams, "aalto-windows.json")))["windows"] if os.path.exists(os.path.join(streams, "aalto-windows.json")) else {}
    bad, dbs, origins = 0, set(), set()
    op = (entry or {}).get("phases", {}).get("op", {}).get("operation")
    reps = (entry or {}).get("phases", {}).get("op", {}).get("repeats") or (entry or {}).get("repeats", [])
    # every phase present (the loop, step 4): a repeat past the recording's end runs the idle phase alone (9.5 D32);
    # any other repeat has every phase some repeat of the application has
    has = {k: {f.split(".")[1] for f in os.listdir(d) if f.startswith("perf.") and ".timehist.txt" in f} for k, d in dirs.items()}
    full = set().union(*has.values()) if has else set()
    for k, d in sorted(dirs.items(), key=lambda kv: (int(str(kv[0]).partition("@")[0]), str(kv[0]))):
        rep, r = json.load(open(os.path.join(d, "report.json"))), kv(os.path.join(d, "report.kv"))
        notes, info = [], []
        if r.get("recording.past_end") == "1":
            info.append("idle phase only, past the recording's end (9.5 D32)")
        elif family in ("interactive", "playback") and has[k] != full:
            notes.append(f"phases missing {sorted(full - has[k])}")
        if r.get("recording.window") == "uncut":
            notes.append("input window not cut")
        if rep.get("gate") != "open" or common.MACHINE not in (rep.get("machine.model") or ""):
            notes.append(f"gate {rep.get('gate')} on {rep.get('machine.model')}")
        # explained: perf record's 130 is its SIGINT stop; freshclam's 2 is the system service holding the update lock,
        # harmless when the scan's signature database was recorded (and is compared across repeats below)
        rcs = {x: v for x, v in r.items() if x.endswith(".rc") and v not in ("0", "")
               and not (x.startswith("perf.") and x.endswith(".record.rc") and v == "130")
               and not (x == "freshclam.rc" and v == "2" and r.get("clamav.db"))}
        if rcs:
            notes.append(f"rc {rcs}")
        if r.get("stream_file"):
            w = win.get(r["stream_file"].removesuffix(".jsonl"), {})
            want = w.get("keys") if r.get("stream_kinds") == "key" else w.get("events")
            sent = lines(os.path.join(d, "replay.jsonl"))
            if want is not None and sent is not None and sent < want:
                notes.append(f"replay sent {sent} of {want}")
        if r.get("stream_alt_file"):
            want, sent = alt.get(r["stream_alt_file"].removesuffix(".jsonl"), {}).get("keys"), lines(os.path.join(d, "replay-alt.jsonl"))
            if want is not None and sent is not None and sent < want - 2:   # a 136M window may run a key past 600 s
                notes.append(f"driven-alt sent {sent} of {want}")
        if op and k in reps and op["n_failed"][reps.index(k)]:
            notes.append(f"operations failed {op['n_failed'][reps.index(k)]} of {op['n_ok'][reps.index(k)] + op['n_failed'][reps.index(k)]}")
        if family == "build":   # 9.6 D27: the repeats whose clamscan is pooled read one signature database
            if k in (entry or {}).get("phases", {}).get("clamscan", {}).get("repeats", []):
                dbs.add((entry or {}).get("clamav_daily", {}).get(str(k)) or (entry or {}).get("clamav_daily", {}).get(k))
        elif r.get("clamav.db"):
            dbs.add(r["clamav.db"])
        if family == "background":
            pins = {x: v for x, v in r.items() if x.startswith("set.") and x.endswith("_pin") and v != "ok"}
            if pins:
                notes.append(f"set pins {pins}")
            bad_verify = {x: v for x, v in r.items() if x.startswith("set.verify.") and v != "ok"}
            if bad_verify:
                notes.append(f"set not restored {bad_verify}")
            incomplete = [x for x, v in r.items() if x.startswith("steam.") and x.endswith(".success") and v != "1"]
            if incomplete:
                notes.append(f"SteamCMD install not reported complete {incomplete}")
            notes += shaping_notes(r)
            if r.get("steam.buildid"):
                dbs.add(r["steam.buildid"])
            if r.get("app") == "upgrade":   # 9.10 D36, D37: the state as built, and the four packages installed
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "0"), ("upgrade.downloaded", "4"),
                                ("upgrade.changed", "4"), ("upgrade.uu.all_installed", "1"), ("upgrade.run_systemd_system", "absent")):
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                if r.get("upgrade.changed_sha256"):
                    dbs.add(r["upgrade.changed_sha256"])
            if r.get("app") == "dkms":   # 9.10 D48, D49, D51: the state on 7.0.0-31 with the module built, the stage
                # installing 7.0.0-34 and DKMS building the module's five files for it
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "0"), ("dkms.state.kernels", "7.0.0-31-generic"),
                                ("dkms.state.status", "nvidia/595.91.07, 7.0.0-31-generic, x86_64: installed"),
                                ("dkms.after.installed_new", "1"), ("dkms.after.modules", "5"),
                                ("upgrade.uu.all_installed", "1"), ("upgrade.run_systemd_system", "absent")):
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                if r.get("upgrade.changed_sha256"):
                    dbs.add(r["upgrade.changed_sha256"])
            if r.get("app") == "tracker":   # 9.10 D61–D68: the state, the set whole, the index run to its end
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "0"), ("upgrade.run_systemd_system", "absent"),
                                ("tracker.miner.version", "3.7.1-1ubuntu0.1"), ("tracker.extract.version", "3.7.1-1ubuntu0.1"),
                                ("tracker.set.files", "875"), ("tracker.set.bytes", "40662407070"), ("tracker.set.verified", "875"),
                                ("tracker.set.failed", "0"), ("tracker.set.files_on_disk", "875"),
                                ("tracker.gst_registry.before", "absent"), ("tracker.db.before", "absent"),
                                ("tracker.done", "1"), ("tracker.db.files", "875"), ("tracker.log.debug_lines", "0")):
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                try:   # the index starts cold (D75)
                    if float(r.get("cache.tracker-index.fraction") or "") > 0.01:
                        notes.append(f"cached fraction {r.get('cache.tracker-index.fraction')} at the start (want <= 0.01)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                try:   # the shipped 15 s initial sleep, from the miner's status trace (D63, D69); GLib lands a seconds
                    # timer on a per-session mark 0.25 s before to 0.75 s after its interval (gmain.c 2.80.0, S2-46)
                    if not 14.75 <= float(r.get("tracker.log.sleep_s") or "") < 15.8:
                        notes.append(f"initial sleep {r.get('tracker.log.sleep_s')} s (want 14.75-15.8)")
                except ValueError:
                    notes.append("initial sleep not in the status trace")
            if r.get("app") in ("mnist", "mnist-madvise"):   # 9.10 D82–D84: the state, the example, the pinned release, the warm start, the run whole
                # the layer plus python3-venv and the three packages it brings (dry run, #142)
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "4"), ("upgrade.run_systemd_system", "absent"),
                                ("mnist.example.main.py.pin", "ok"), ("mnist.example.README.md.pin", "ok"),
                                ("mnist.example.requirements.txt.pin", "ok"),
                                ("mnist.torch.version", "2.14.0+cpu"), ("mnist.torchvision.version", "0.29.0+cpu"),
                                ("mnist.train.epochs", "14"),
                                # D87: the runner's mode for the campaign, the desktop kernel's for the check
                                ("thp.before.enabled", "always [madvise] never" if r.get("app") == "mnist-madvise" else "[always] madvise never")):
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                try:   # the run starts warm (D83): the dataset's files in the page cache
                    if float(r.get("cache.mnist-train.fraction") or "") < 0.99:
                        notes.append(f"cached fraction {r.get('cache.mnist-train.fraction')} at the start (want >= 0.99)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                if r.get("mnist.pip-freeze.sha256"):   # one installed set across repeats
                    dbs.add(r["mnist.pip-freeze.sha256"])
            if r.get("app") == "handbrake" and r.get("mode") != "probe":   # 9.10 D91–D95: the state, the clip, the warm start, the encode whole
                # the layer plus handbrake-cli and the 66 packages it brings (the probe, run #151)
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "67"), ("upgrade.run_systemd_system", "absent"),
                                ("handbrake.cli.version", "1.7.2+ds1-1build2"), ("handbrake.x264.version", "2:0.164.3108+git31e19f9-1"),
                                ("handbrake.zip.pin", "ok"), ("handbrake.clip.pin", "ok"),
                                ("handbrake.handbrake-transcode.done", "1"),
                                # D95: HandBrake's default preset unchanged
                                ("handbrake.handbrake-transcode.encoder", "+ encoder: H.264 (libx264)"),
                                ("handbrake.handbrake-transcode.encoder_preset", "+ preset:  fast"),
                                ("handbrake.handbrake-transcode.quality", "+ quality: 22.00 (RF)"),
                                # the dry run, #153: the clip's 19,036 frames decoded whole
                                ("handbrake.handbrake-transcode.decoder", "h264-decoder done: 19036 frames, 0 decoder errors"),
                                ("handbrake.handbrake-transcode.picture", "storage dimensions: 1920 x 1080"),
                                ("handbrake.handbrake-transcode.par", "pixel aspect ratio: 1 : 1"),
                                ("thp.before.enabled", "[always] madvise never")):   # D94: the runner's mode, D87's venue
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                try:   # the encode starts warm (D94): the clip in the page cache
                    if float(r.get("cache.handbrake-transcode.fraction") or "") < 0.99:
                        notes.append(f"cached fraction {r.get('cache.handbrake-transcode.fraction')} at the start (want >= 0.99)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                if r.get("handbrake.handbrake-transcode.video_track"):   # one stream across repeats: the video track's frames and bytes
                    dbs.add(r["handbrake.handbrake-transcode.video_track"])
            if r.get("app") == "kdenlive":   # 9.10 D101–D104: the state, the project, the warm start, the dialog's export whole
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "0"), ("upgrade.run_systemd_system", "absent"),
                                ("kdenlive.state.install.rc", "0"), ("kdenlive.state.added", "427"),   # the dry run, #161
                                # S2-60: the archive's render stack at T0, with Kdenlive's recommends (D102)
                                ("kdenlive.pkg.kdenlive", "4:23.08.5-0ubuntu4"), ("kdenlive.pkg.melt", "7.22.0-1build6"),
                                ("kdenlive.pkg.libmlt7", "7.22.0-1build6"), ("kdenlive.pkg.libavcodec60", "7:6.1.1-3ubuntu5"),
                                ("kdenlive.pkg.libx264-164", "2:0.164.3108+git31e19f9-1"), ("kdenlive.pkg.frei0r-plugins", "1.8.0-1build3"),
                                ("kdenlive.clip.rc", "0"), ("kdenlive.project.rc", "0"), ("kdenlive.export.rc", "0"),
                                ("kdenlive.export.mode", "delivery"),
                                # D103: the default profile as the dialog opens, in the playlist's consumer
                                ("kdenlive.consumer.mlt_service", "avformat"), ("kdenlive.consumer.f", "mp4"),
                                ("kdenlive.consumer.vcodec", "libx264"), ("kdenlive.consumer.crf", "23"),
                                ("kdenlive.consumer.preset", "veryfast"), ("kdenlive.consumer.g", "15"),
                                ("kdenlive.consumer.acodec", "aac"), ("kdenlive.consumer.ab", "160k"),
                                ("kdenlive.consumer.real_time", "-1"), ("kdenlive.consumer.threads", "0"),
                                ("kdenlive.consumer.in", "0"), ("kdenlive.consumer.out", "599"),
                                # the project's 600 frames exported whole, with the silence of its audio track
                                ("kdenlive.output.video.codec", "h264"), ("kdenlive.output.video.frames", "600"),
                                ("kdenlive.output.video.size", "1920x1080"), ("kdenlive.output.audio.codec", "aac"),
                                ("thp.before.enabled", "[always] madvise never")):   # D104: the runner's mode, D87's venue
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                try:   # the export starts warm (D104): the clip in the page cache
                    if float(r.get("cache.kdenlive-export.fraction") or "") < 0.99:
                        notes.append(f"cached fraction {r.get('cache.kdenlive-export.fraction')} at the start (want >= 0.99)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                # one clip, one installed set and one encoder setup across repeats
                dbs.add((r.get("kdenlive.clip.sha256"), r.get("kdenlive.state.added_sha256"), r.get("kdenlive.output.x264")))
            if r.get("app") == "dejadup":   # 9.10 D112–D118: the state, the set, the first backup, the week, the monitor's run
                for x, want in (("upgrade.layer.missing", "0"), ("upgrade.layer.extra", "0"), ("upgrade.run_systemd_system", "absent"),
                                ("dejadup.state.install.rc", "0"),
                                # S2-64: the archive's backup stack at T0 (D113)
                                ("dejadup.pkg.deja-dup", "45.2-1build2"), ("dejadup.pkg.duplicity", "2.1.4-3ubuntu2"),
                                ("dejadup.pkg.librsync2t64", "2.3.4-1.1ubuntu2"),
                                # 9.7 D7: the set as pinned, verified where Déjà Dup reads it (D118)
                                ("set.archive_pin", "ok"), ("set.manifest_pin", "ok"), ("set.verify.placed", "ok"),
                                ("dejadup.drive.mount.rc", "0"), ("dejadup.drive.dio", "1"),   # D114
                                # the first backup through the assistant: one full chain, the password remembered (D117, D118)
                                ("dejadup.first.driver.rc", "0"), ("dejadup.first.first_rc", "0"),
                                ("dejadup.first.keyring_items", "1"), ("dejadup.drive.first.full_manifests", "1"),
                                ("dejadup.drive.first.inc_manifests", "0"),
                                ("dejadup.week.rc", "0"), ("change.week.rc", "0"), ("change.week.days", "7"),   # D115
                                # the monitor's child (D112): deja-dup --backup --auto in the idle classes, advancing last-backup
                                ("dejadup.run.rc", "0"), ("dejadup.run.argv", "deja-dup --backup --auto"),
                                ("dejadup.run.policy", "SCHED_IDLE"),
                                ("dejadup.run.io_class", "idle"), ("dejadup.after.advanced", "1"),
                                ("dejadup.drive.after.full_manifests", "1"), ("dejadup.drive.after.inc_manifests", "1"),
                                ("thp.before.enabled", "[always] madvise never")):   # D118: the runner's mode, D87's venue
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want})")
                try:   # the incremental starts warm (D116): the set in the page cache
                    if float(r.get("cache.dejadup-incremental.fraction") or "") < 0.99:
                        notes.append(f"cached fraction {r.get('cache.dejadup-incremental.fraction')} at the start (want >= 0.99)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                # one set, one installed set and one change set across repeats
                dbs.add((r.get("set.manifest_sha256"), r.get("dejadup.state.added_sha256"), r.get("change.week.sha256")))
        if family == "desktop":   # 9.8 D13 (the gate itself is checked for every family above)
            want, got = r.get("renderers.wanted_min"), r.get("renderers.observed")
            if want and got and int(got) < int(want):
                notes.append(f"renderers {got} < {want}")
            if r.get("mode") == "probe":
                info.append("long-phase probe, never a repeat")
            if r.get("page.server") not in (None, "200"):
                notes.append(f"page server answered {r.get('page.server')}")
            if r.get("app") == "chrome-tabs":   # 9.10 D128, D129: both launches, every tab loaded, one count held
                tabs = r.get("tabs.tabs")
                for arm in ("off", "on"):
                    if r.get(f"tabs.{arm}.page_loads") != tabs:
                        notes.append(f"spare {arm}: {r.get(f'tabs.{arm}.page_loads')} page loads for {tabs} tabs")
                    if r.get(f"tabs.{arm}.steady.plain_min") is None:
                        notes.append(f"spare {arm}: no steady phase listed")
                    elif r.get(f"tabs.{arm}.steady.plain_min") != r.get(f"tabs.{arm}.steady.plain_max"):
                        info.append(f"spare {arm}: the steady phase's plain renderers moved "
                                    f"{r.get(f'tabs.{arm}.steady.plain_min')}–{r.get(f'tabs.{arm}.steady.plain_max')}")
                    if r.get(f"tabs.{arm}.steady.plain_pids_stable") not in (None, "1"):
                        info.append(f"spare {arm}: the steady phase's plain renderers changed pids")
            if (r.get("app") or "").startswith("launch-"):   # 9.10 D132–D135: both launches, a clean quit, warm, traced whole
                subj = r["app"][len("launch-"):]
                # perf stopped by SIGINT exits 130, as the background family's phases record it
                for x, want in (("launch.first.left_after_quit", "0"), ("tree.traced.harness_procs", "0"),
                                ("perf.launch.record.rc", "130"), ("perf.launch.lost", "")):
                    if r.get(x) != want:
                        notes.append(f"{x} {r.get(x)} (want {want or 'none'})")
                try:   # the relaunch starts warm (D132): the files the first launch mapped, in the page cache
                    if float(r.get("cache.launch.fraction") or "") < 0.99:
                        notes.append(f"cached fraction {r.get('cache.launch.fraction')} before the traced launch (want >= 0.99)")
                except ValueError:
                    notes.append("cached fraction not recorded")
                if r.get("launch.analysis"):
                    notes.append(f"analysis: {r['launch.analysis']}")
                if subj == "webrtc" and r.get("launch.traced.call_connected") != "1":
                    notes.append(f"the call did not connect: {r.get('launch.traced.call_title')}")
                if subj == "element" and r.get("matrix.sync_rows") in (None, "0"):
                    notes.append("no /sync reached the homeserver — the client was not signed in")
                if subj == "steam" and r.get("launch.traced.steamid") != "0":
                    notes.append(f"steamid {r.get('launch.traced.steamid')} (want 0, logged out)")
                if subj == "chrome-hidden" and int(r.get("launch.traced.gate.page_renderers") or 0) < 13:
                    notes.append(f"{r.get('launch.traced.gate.page_renderers')} renderers at the traced launch's gate (want >= 13)")
                if subj == "chrome-hidden" and r.get("launch.renderer_streams") != "12":
                    notes.append(f"{r.get('launch.renderer_streams')} renderer streams (want 12, the background tabs')")
                if subj == "thunderbird-send" and not r.get("launch.traced.postwindow"):
                    notes.append("no compose window in the traced launch")
                if r.get("launch.quit_dialog"):
                    info.append(f"the quit put up a dialog: {r['launch.quit_dialog']}")
            if r.get("app") == "element" and r.get("matrix.sync_rows") in (None, "0"):
                notes.append("no /sync reached the homeserver — the client was not signed in")
            # every repeat of one subject must have run at one N, or the pool is not a pool. A probe is never a
            # repeat and its N may differ by design, so it stays out of the comparison.
            if r.get("settings.origins") and r.get("mode") != "probe":
                origins.add(r["settings.origins"])
        if family == "session":   # 9.9 D12–D14 (the gate itself is checked for every family above)
            if r.get("mode") == "probe":
                info.append("long-phase probe, never a repeat")
            if r.get("edge.idle") not in (None, "1"):
                notes.append("steady edge not in the terminal idle state")
            if r.get("pin.fails") not in (None, "0"):
                notes.append(f"pin failed {r.get('pin.fails')} time(s)")
            # D21: the placement read from the processes, and the bus answering after it was restarted into
            # meas.slice. A full job stops on either, so this states what the record was judged on.
            for field, what in (("placement.pinned", "at the pin"), ("placement.edge", "at the steady edge")):
                if r.get(field) not in (None, "1"):
                    notes.append(f"the entries were not alone on the measured CPU {what}")
            if r.get("bus.login1.rc") not in (None, "0"):
                notes.append("org.freedesktop.login1 did not answer after the bus was restarted")
            fu = [x for x in ((entry or {}).get("foreign_user") or []) if str(x.get("repeat")) == str(k)]
            if fu:
                notes.append(f"user-space work on the measured CPU over the bound (D20, D22): "
                             f"{fu[0]['schedule_ins']} schedule-ins, {fu[0]['share_of_phase'] * 100:.4f}% of the "
                             f"phase against {(fu[0]['bound'] or 0) * 100:.2f}%")
        bad += bool(notes)
        print(f"   r{k}: {'ok' if not notes else '; '.join(notes)}{''.join(f' ({x})' for x in info)}")
    if len(dbs) > 1:
        what = ("SteamCMD app builds, upgrade and DKMS change sets, MNIST installed sets or HandBrake streams" if family == "background" else "ClamAV signature databases")
        print(f"   {what} differ across repeats: {sorted(dbs)}"); bad += 1
    if len(origins) > 1:
        print(f"   origin counts differ across repeats: {sorted(origins)}"); bad += 1
    return bad


def main():
    a = sys.argv[1:]
    passthrough = a[a.index("--") + 1:] if "--" in a else []
    a = a[:a.index("--")] if "--" in a else a
    if not a:
        raise SystemExit(__doc__)
    family, app, _ = common.parse_target(a[0])
    since = int(a[a.index("--since") + 1]) if "--since" in a else 1
    base = os.path.join(common.WORK, "pool", f"{family}-{app or 'build'}-from{since}")
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(base, "pooled.json")
    # K leaves every copy of window K out; K@RUNID only the copy measured in that run (a window measured twice)
    items = a[a.index("--exclude") + 1].split(",") if "--exclude" in a else []
    excluded = {int(x) for x in items if "@" not in x}
    excluded_runs = {(int(x.split("@")[0]), int(x.split("@")[1])) for x in items if "@" in x}
    why = a[a.index("--exclude-why") + 1] if "--exclude-why" in a else ""
    if (excluded or excluded_runs) and not why:
        raise SystemExit('--exclude needs --exclude-why "<reason>": the pooled record states why a repeat is left out')
    landed = {}
    for r in common.runs(family, since):
        names = None
        for j in common.jobs(family, r["databaseId"]):
            if j["state"] != "landed" or (app and j["app"] != app):
                continue
            name = common.artifact(family, j["app"], j["k"])
            names = common.artifact_names(r["databaseId"]) if names is None else names
            if name not in names:   # a dry check or another mode: not a repeat of this campaign
                print(f"   run #{r['number']} ({r['databaseId']}): no {name} (has {', '.join(names) or 'none'}); not pooled")
                continue
            dest = os.path.join(base, name) if family == "build" else os.path.join(base, str(r["databaseId"]), name)
            if j["k"] in excluded or (j["k"], r["databaseId"]) in excluded_runs:   # out of the folder pool.py reads, kept beside it, never downloaded again
                aside = os.path.join(base + "-excluded", str(r["databaseId"]), name)
                if os.path.exists(dest) and not os.path.exists(aside):
                    os.makedirs(os.path.dirname(aside), exist_ok=True)
                    os.replace(dest, aside)
                print(f"   r{j['k']}: left out of the pool — {why}; its artifact under {base}-excluded")
                continue
            got = common.download(r["databaseId"], name, dest)
            if got not in (d for _, d in landed.get(j["k"], [])):   # build's flat folder: one path per index
                landed.setdefault(j["k"], []).append((r["databaseId"], got))
    # every landing is checked: an index that landed more than once (a retry relaunched while an earlier launch was
    # still queued) is keyed <index>@<run id> per landing, as the desktop pool keys it
    dirs = {(k if len(ls) == 1 else f"{k}@{rid}"): d for k, ls in landed.items() for rid, d in ls}
    if not dirs:
        raise SystemExit("no landed repeat")
    cmd = ["python3", common.FAMILIES[family]["pool"], base, out, "--cpu-model", common.MACHINE, *passthrough]
    if family in ("build", "background", "desktop", "session") and "--md" not in passthrough:
        cmd += ["--md", os.path.join(os.path.dirname(out), "results.md")]
    p = subprocess.run(cmd, cwd=common.REPO, capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(p.stderr[-3000:])
    pooled = json.load(open(out))
    entry = pooled if family == "build" else pooled["runs"].get(app)
    st = (entry or {}).get("stability")
    if excluded or excluded_runs:
        (entry if entry is not None else pooled)["excluded_repeats"] = {
            **{str(k): why for k in sorted(excluded)}, **{f"{k}@{rid}": why for k, rid in sorted(excluded_runs)}}
        json.dump(pooled, open(out, "w"), indent=1)
        md = next((cmd[i + 1] for i, a in enumerate(cmd) if a == "--md"), None)   # the pool rendered before this key existed
        if md and os.path.exists(md):
            with open(md, "a") as handle:
                handle.write(f"\n## Left out of this pool\n\nRepeat(s) {', '.join([str(k) for k in sorted(excluded)] + [f"{k}@{rid}" for k, rid in sorted(excluded_runs)])}: {why}\n")
    if family == "build":
        crit = st["quantities"]
        print(f"build: repeats {pooled['repeats']}; stability rule {'holds' if st['passes'] else 'does not hold yet'}; "
              f"repeats needed at this spread {st.get('needed') or 'over 200'}"
              + (f"; not estimable yet: {', '.join(st['not_estimable'])}" if st.get("not_estimable") else ""))
        for ph, P in pooled["phases"].items():
            if P.get("not_pooled"):
                print(f"   {ph} pooled over {P.get('repeats', [])}; not pooled: {({r: x['why'] for r, x in P['not_pooled'].items()})} (9.6 D27, D28)")
        for q, c in crit.items():
            print(f"   {q}: k {c['k']}, mean {c['mean']}, half-width {c['half_width']} (abs {c['half_width_abs']}), "
                  f"needed {c.get('needed')}, "
                  + ("carried with its half-width (9.6 D29)" if c.get("excepted") and c.get("carried")
                     else ("passes" if c["passes"] else "fails")))
    elif st and "quantities" in st:
        print("\n".join(stability_lines(app, entry)))
    elif st:
        print(f"{app}: repeats {entry['repeats']}; {st['quantity']} over {st['k']}: half-width {st['half_width']} "
              f"(tolerance {st['tolerance']}) — {'holds' if st['passes'] else 'does not hold yet'}")
        print(f"   values {st['values']}")
    print(f"   phases {list((entry or {}).get('phases', {}))}; pooled record {out}")
    print("validity:")
    bad = validity(family, dirs, entry)
    if excluded or excluded_runs:
        print(f"   left out of this pool: {sorted(excluded) + [f'{k}@{rid}' for k, rid in sorted(excluded_runs)]} — {why}")
    print(f"   {'every repeat valid' if not bad else f'{bad} repeat(s) with a problem'}")


def stability_lines(app, entry):
    """The rule's reading of one application's pooled entry, a line per value, as the pool report prints it."""
    st = entry["stability"]
    lines = [f"{app}: repeats {entry['repeats']}; stability rule {'holds' if st['passes'] else 'does not hold yet'}"
             + (f"; first batch at this spread {entry['first_batch']['count']}" if entry.get("first_batch") else "")]
    for q, c in st["quantities"].items():
        lines.append(f"   {q}: k {c['k']}, half-width {c['half_width']}, "
                     f"{'passes' if c['passes'] else 'at the window limit, reported (D46)' if c.get('limited') else 'carried with its half-width, its spread between sessions (D57)' if c.get('session_spread') and c.get('carried', True) else 'carried with its half-width, its spread the machine (9.8 D17)' if c.get('excepted') and c.get('carried') else 'fails'}"
                     + (f", needed {c.get('needed') or 'over 200'}" if not c["passes"] and not c.get("carried") and "needed" in c else ""))
    return lines


if __name__ == "__main__":
    main()
