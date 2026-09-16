#!/usr/bin/env python3
"""Operation driver (9.5 follow-ups spec, decisions 7–10): triggers an
application's heavy operation repeatedly inside the `op` phase and records
each as one line of ops.jsonl — {"op", "i", "trigger_us", "done_us",
"rc", "note"} on the monotonic clock, the clock perf records on — so the
analysis can cut the operation's window [trigger, done) and its duration.

ops_driver.py <app> <window-id> <seconds> <out.jsonl> [--count N] [--pause S]

Operations (the trigger is design; the cost and duration are the observation):
  gimp      unsharp mask on the open image through GIMP's Script-Fu server
            (plug-in-unsharp-mask, radius 4.0 / amount 0.32 / threshold 8 —
            PCMark 10's batch unsharp parameters mapped onto GIMP's PDB, see
            method §3); done when the server answers.
  kdenlive  timeline preview render of the whole clip: Remove All Preview
            Zones, then Start Preview Render, which adds the timeline zone
            itself when no preview zone is defined (TimelineController::
            startPreviewRender, 23.08) and renders it in an external
            kdenlive_render process; done when that process has appeared and
            exited. The actions are triggered over D-Bus — KXmlGuiWindow
            exports the action collection at /kdenlive/MainWindow_1/actions/
            <name> (kxmlguiwindow.cpp), so `trigger` on
            clear_render_timeline_zone and prerender_timeline_zone needs no
            focus and no shortcut; Shift+Return through xdotool is the
            fallback when the bus is unavailable (probe 35087191213: seeded
            shortcuts in kdenliverc did not fire).
  chrome    load the scripted feed page from the local server (a fresh query
            string per load); done when the page sets its title to
            "loaded …" after building the feed.
"""

import argparse
import json
import socket
import subprocess
import sys
import time


def now_us():
    return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1e6)


def xdo(*args, check=False):
    return subprocess.run(["xdotool", *args], check=check, capture_output=True, text=True)


def pgrep(comm):
    return subprocess.run(["pgrep", "-x", comm], capture_output=True).returncode == 0


# ---- GIMP: Script-Fu server protocol (docs.gimp.org, "Script-Fu Server": request 'G' + 2-byte big-endian length +
#      script; response 'G' + error byte + 2-byte big-endian length + message)
def gimp_send(script, host="127.0.0.1", port=10008, timeout=600):
    body = script.encode()
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall(b"G" + bytes([len(body) >> 8, len(body) & 255]) + body)
        hdr = b""
        while len(hdr) < 4:
            chunk = s.recv(4 - len(hdr))
            if not chunk:
                raise ConnectionError("server closed")
            hdr += chunk
        err, n = hdr[1], (hdr[2] << 8) | hdr[3]
        msg = b""
        while len(msg) < n:
            chunk = s.recv(n - len(msg))
            if not chunk:
                break
            msg += chunk
        return err, msg.decode(errors="replace")


GIMP_PREP = ('(let* ((img (vector-ref (cadr (gimp-image-list)) 0))) (gimp-image-undo-disable img) img)')
GIMP_OP = ('(let* ((img (vector-ref (cadr (gimp-image-list)) 0)) (drw (car (gimp-image-get-active-drawable img)))) '
           '(plug-in-unsharp-mask RUN-NONINTERACTIVE img drw 4.0 0.32 8) (gimp-displays-flush) drw)')


def op_gimp(i, wid, args):
    if i == 0:
        err, msg = gimp_send(GIMP_PREP)
        if err:
            return None, None, 3, f"prep: {msg}"
    t0 = now_us()
    err, msg = gimp_send(GIMP_OP)
    t1 = now_us()
    return t0, t1, (1 if err else 0), msg[:120]


# ---- Kdenlive
def wait_proc(comm, appear_s, gone_s):
    t = time.monotonic()
    while time.monotonic() - t < appear_s:
        if pgrep(comm):
            break
        time.sleep(0.05)
    else:
        return None, False
    t_seen = now_us()
    t = time.monotonic()
    while time.monotonic() - t < gone_s:
        if not pgrep(comm):
            return t_seen, True
        time.sleep(0.05)
    return t_seen, False


_KDENLIVE_BUS = {}


def kdenlive_bus():
    """(bus name, main-window path) of the running Kdenlive on the session bus, or None."""
    if "v" in _KDENLIVE_BUS:
        return _KDENLIVE_BUS["v"]
    found = None
    try:
        r = subprocess.run(["dbus-send", "--session", "--print-reply", "--dest=org.freedesktop.DBus", "/org/freedesktop/DBus",
                            "org.freedesktop.DBus.ListNames"], capture_output=True, text=True, timeout=10)
        names = [l.split('"')[1] for l in r.stdout.splitlines() if 'string "org.kde.kdenlive' in l]
        for name in names:
            r2 = subprocess.run(["dbus-send", "--session", "--print-reply", f"--dest={name}", "/kdenlive",
                                 "org.freedesktop.DBus.Introspectable.Introspect"], capture_output=True, text=True, timeout=10)
            for l in r2.stdout.splitlines():
                if 'node name="MainWindow' in l:
                    found = (name, "/kdenlive/" + l.split('"')[1]); break
            if found:
                break
    except Exception:
        found = None
    _KDENLIVE_BUS["v"] = found
    return found


def kdenlive_action(bus, action):
    name, path = bus
    r = subprocess.run(["dbus-send", "--session", "--print-reply", f"--dest={name}", f"{path}/actions/{action}",
                        "org.qtproject.Qt.QAction.trigger"], capture_output=True, text=True, timeout=10)
    return r.returncode == 0


def op_kdenlive(i, wid, args):
    bus = kdenlive_bus()
    if bus:
        ok1 = kdenlive_action(bus, "clear_render_timeline_zone")   # Remove All Preview Zones (drops rendered chunks)
        time.sleep(1.0)
        t0 = now_us()
        ok2 = kdenlive_action(bus, "prerender_timeline_zone")      # Start Preview Render (adds the timeline zone when none is defined)
        how = f"dbus {bus[1]} clear={int(ok1)} start={int(ok2)}"
    else:
        xdo("windowactivate", "--sync", wid)
        time.sleep(0.5)
        t0 = now_us()
        xdo("key", "--clearmodifiers", "shift+Return")               # fallback: Start Preview Render's default shortcut
        how = "keys (no session bus)"
    seen, gone = wait_proc("kdenlive_render", appear_s=30, gone_s=args.op_timeout)
    t1 = now_us()
    if seen is None:
        return t0, t1, 2, f"kdenlive_render never appeared; {how}"
    return t0, t1, (0 if gone else 4), f"renderer seen at +{(seen - t0) / 1000:.0f} ms; {how}" + ("" if gone else "; timeout")


# ---- Chrome
def window_title(wid):
    r = xdo("getwindowname", wid)
    return r.stdout.strip()


def op_chrome(i, wid, args):
    url = f"{args.url}?i={i}"
    xdo("windowactivate", "--sync", wid)
    time.sleep(0.3)
    xdo("key", "--clearmodifiers", "ctrl+l")
    time.sleep(0.2)
    xdo("type", "--clearmodifiers", "--delay", "5", url)
    t0 = now_us()
    xdo("key", "--clearmodifiers", "Return")
    t = time.monotonic()
    while time.monotonic() - t < args.op_timeout:
        title = window_title(wid)
        if title.startswith(f"loaded {i} "):
            return t0, now_us(), 0, title[:80]
        time.sleep(0.02)
    return t0, now_us(), 4, f"timeout; title {window_title(wid)[:60]!r}"


OPS = {"gimp": ("unsharp-mask", op_gimp), "kdenlive": ("preview-render", op_kdenlive), "chrome": ("page-load", op_chrome)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app"); ap.add_argument("wid"); ap.add_argument("seconds", type=float); ap.add_argument("out")
    ap.add_argument("--count", type=int, default=0, help="stop after N operations (0: run for --seconds)")
    ap.add_argument("--pause", type=float, default=10.0, help="seconds between operations")
    ap.add_argument("--op-timeout", type=float, default=600.0)
    ap.add_argument("--url", default="http://127.0.0.1:8088/feed.html")
    args = ap.parse_args()
    name, fn = OPS[args.app]
    t_end = time.monotonic() + args.seconds
    i = 0
    with open(args.out, "a") as out:
        while (args.count and i < args.count) or (not args.count and time.monotonic() < t_end):
            try:
                t0, t1, rc, note = fn(i, args.wid, args)
            except Exception as exc:  # a failed trigger is recorded, never fatal
                t0, t1, rc, note = now_us(), now_us(), 9, f"{type(exc).__name__}: {exc}"[:160]
            rec = {"op": name, "i": i, "trigger_us": t0, "done_us": t1, "rc": rc, "note": note}
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(f"op {name} #{i}: rc={rc} {((t1 or 0) - (t0 or 0)) / 1000:.0f} ms {note}", file=sys.stderr, flush=True)
            i += 1
            if rc == 3:
                break
            if time.monotonic() + args.pause >= t_end and not args.count:
                break
            time.sleep(args.pause)


if __name__ == "__main__":
    main()
