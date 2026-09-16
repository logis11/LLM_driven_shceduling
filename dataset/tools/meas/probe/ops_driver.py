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
  kdenlive  timeline preview render of the whole clip through Kdenlive's
            default shortcuts: Start Preview Render (Shift+Return) adds the
            timeline zone itself when no preview zone is defined
            (TimelineController::startPreviewRender, 23.08); before every
            later render, a click on the clip, Delete, Undo dirty the zone's chunks
            (manual: any change to the video under a preview zone triggers a
            new render pass). Done when the external kdenlive_render process
            has appeared and exited. Probes 35087191213 and 35088110333:
            seeded [Shortcuts] never fired, and the KXMLGUI D-Bus action
            export does not reach Kdenlive's actions (they are parented to the
            main window, not to the exported collection).
  chrome    load the scripted feed page from the local server (a fresh query
            string per load); done when the page sets its title to
            "loaded …" after building the feed.
"""

import argparse
import json
import os
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


def shot(args, label):
    out_dir = os.path.dirname(os.path.abspath(args.out))
    subprocess.run(["import", "-window", "root", os.path.join(out_dir, f"op-{label}.png")], capture_output=True)


def op_kdenlive(i, wid, args):
    """First render: Start Preview Render (Shift+Return) adds the timeline zone itself when no preview zone is defined
    (TimelineController::startPreviewRender, 23.08). Later renders, two attempts with a screenshot after each step:
    (A) Remove All Preview Zones through the shortcut seeded in the per-user ui file (Ctrl+Shift+F10), then Shift+Return;
    (B) click the clip on V1, Delete, Undo (a change under the zone dirties its chunks; manual "Timeline Preview
    Rendering"), then Shift+Return. The render runs in an external kdenlive_render process."""
    xdo("windowactivate", "--sync", wid)
    time.sleep(0.5)
    if i == 0:
        t0 = now_us()
        xdo("key", "--clearmodifiers", "shift+Return")
        seen, gone = wait_proc("kdenlive_render", appear_s=30, gone_s=args.op_timeout)
        how = "shift+Return"
    else:
        xdo("key", "--clearmodifiers", "ctrl+shift+F10"); time.sleep(1.0); shot(args, f"{i}-a-clear")
        t0 = now_us()
        xdo("key", "--clearmodifiers", "shift+Return")
        seen, gone = wait_proc("kdenlive_render", appear_s=15, gone_s=args.op_timeout)
        how = "A: ctrl+shift+F10, shift+Return"
        if seen is None:
            xdo("mousemove", str(args.clip_x), str(args.clip_y)); time.sleep(0.2)
            xdo("click", "1"); time.sleep(0.6); shot(args, f"{i}-b-click")
            xdo("key", "--clearmodifiers", "Delete"); time.sleep(1.0); shot(args, f"{i}-b-delete")
            xdo("key", "--clearmodifiers", "ctrl+z"); time.sleep(1.0); shot(args, f"{i}-b-undo")
            t0 = now_us()
            xdo("key", "--clearmodifiers", "shift+Return")
            seen, gone = wait_proc("kdenlive_render", appear_s=15, gone_s=args.op_timeout)
            how = f"A failed; B: click ({args.clip_x},{args.clip_y}), Delete, ctrl+z, shift+Return"
    t1 = now_us()
    if seen is None:
        shot(args, f"{i}-end")
        return t0, t1, 2, f"kdenlive_render never appeared; {how}"
    return t0, t1, (0 if gone else 4), f"renderer seen at +{(seen - t0) / 1000:.0f} ms; {how}" + ("" if gone else "; timeout")


# ---- Chrome
def window_title(wid):
    r = xdo("getwindowname", wid)
    return r.stdout.strip()


def op_chrome(i, wid, args):
    """First load through the omnibox (from the typing page to feed.html?i=0); every later load by pressing "n" on the
    feed page, which navigates itself to ?i=<i+1> — the omnibox's history suggestions are never involved again
    (run 35092593907: typing ?i=12 loaded the suggested ?i=1 and the driver waited out its timeout)."""
    xdo("windowactivate", "--sync", wid)
    time.sleep(0.3)
    if i == 0:
        xdo("key", "--clearmodifiers", "ctrl+l")
        time.sleep(0.2)
        xdo("type", "--clearmodifiers", "--delay", "5", f"{args.url}?i=0")
        t0 = now_us()
        xdo("key", "--clearmodifiers", "Return")
    else:
        t0 = now_us()
        xdo("key", "--clearmodifiers", "n")
    t = time.monotonic()
    while time.monotonic() - t < args.op_timeout:
        title = window_title(wid)
        if title.startswith(f"loaded {i} "):
            return t0, now_us(), 0, title[:80]
        time.sleep(0.02)
    return t0, now_us(), 4, f"timeout; title {window_title(wid)[:60]!r}"


OPS = {"gimp": ("unsharp-mask", op_gimp), "kdenlive": ("preview-render", op_kdenlive), "chrome": ("page-load", op_chrome)}


def tree_procs(pattern):
    """pid -> process type of every live process whose command line matches the appdef's PAT, read from /proc right
    after an operation: the roles of processes that live only during the operation (a navigation's renderer, a
    render helper), which the phase snapshots never see (dry run 35091798507: eight transient Chrome pids)."""
    out = {}
    if not pattern:
        return out
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")
        except OSError:
            continue
        if pattern not in cmd:
            continue
        m = [a for a in cmd.split() if a.startswith("--type=")]
        out[int(pid)] = m[0][7:] if m else "main"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app"); ap.add_argument("wid"); ap.add_argument("seconds", type=float); ap.add_argument("out")
    ap.add_argument("--count", type=int, default=0, help="stop after N operations (0: run for --seconds)")
    ap.add_argument("--pause", type=float, default=10.0, help="seconds between operations")
    ap.add_argument("--op-timeout", type=float, default=None,
                    help="seconds to wait for one operation's completion (default: 60 for chrome, 600 otherwise)")
    ap.add_argument("--url", default="http://127.0.0.1:8088/feed.html")
    ap.add_argument("--clip-x", type=int, default=300); ap.add_argument("--clip-y", type=int, default=640)
    ap.add_argument("--pat", default="", help="the appdef's PAT: command-line pattern of the application's tree")
    args = ap.parse_args()
    name, fn = OPS[args.app]
    if args.op_timeout is None:
        args.op_timeout = 60.0 if args.app == "chrome" else 600.0
    t_end = time.monotonic() + args.seconds
    i = 0
    with open(args.out, "a") as out:
        while (args.count and i < args.count) or (not args.count and time.monotonic() < t_end):
            try:
                t0, t1, rc, note = fn(i, args.wid, args)
            except Exception as exc:  # a failed trigger is recorded, never fatal
                t0, t1, rc, note = now_us(), now_us(), 9, f"{type(exc).__name__}: {exc}"[:160]
            rec = {"op": name, "i": i, "trigger_us": t0, "done_us": t1, "rc": rc, "note": note}
            try:
                rec["procs"] = tree_procs(args.pat)
            except Exception:  # never touches the operation's own record
                pass
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
