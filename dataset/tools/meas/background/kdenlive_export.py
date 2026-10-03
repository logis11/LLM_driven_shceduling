#!/usr/bin/env python3
"""kdenlive_export.py <chroot> <out dir> — the export phase's driver (9.10 D101), run on the harness CPUs.

Kdenlive's window is raised under the pointer and its Render action, Ctrl+Return (Kdenlive 23.08.5's `project_render`;
S2-59 mainwindow.cpp:1483–1484), opens the "Rendering" dialog. "Render to File" is a Qt widget, not an X window, so
it is found in a screenshot of the dialog by tesseract's word boxes and clicked. The dialog starts `kdenlive_render`
detached (renderwidget.cpp:790). The driver waits for it, copies the playlist its arguments name — kdenlive_render
erases a playlist under the temporary directory when it ends (renderjob.cpp:44) — and waits for it to exit.
Writes export.json: the steps' times (CLOCK_MONOTONIC and wall, ns), the renderer's pid and arguments, the button's
box, notes. Exit status: 0 the render ran and exited; 2 no dialog; 3 no button; 4 no renderer.
"""

import json
import os
import shutil
import subprocess
import sys
import time

DIALOG = "^Rendering$"          # renderwidget_ui.ui's windowTitle (S2-59)
BUTTON = ("Render", "to", "File")
RENDERER = "kdenlive_render"


def xdo(*args):
    return subprocess.run(["xdotool", *args], capture_output=True, text=True)


def stamp():
    return {"mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}


def shot(out, name, wid=None):
    path = os.path.join(out, f"export.{name}.png")
    subprocess.run(["import", "-window", wid or "root", path], capture_output=True)
    return path


def geometry(wid):
    r = xdo("getwindowgeometry", "--shell", wid)
    g = dict(line.split("=", 1) for line in r.stdout.split() if "=" in line)
    return int(g.get("X", 0)), int(g.get("Y", 0)), int(g.get("WIDTH", 0)), int(g.get("HEIGHT", 0))


def find_window(rx, secs, by="--name"):
    """The largest visible window matching, waiting up to secs."""
    end = time.monotonic() + secs
    while time.monotonic() < end:
        ids = xdo("search", "--onlyvisible", by, rx).stdout.split()
        if ids:
            return max(ids, key=lambda w: geometry(w)[2] * geometry(w)[3])
        time.sleep(0.25)
    return None


def find_button(png, out, scale=2):
    """The box of the words "Render to File" on one line of tesseract's TSV, in the image's pixels; read from the
    screenshot scaled up (the dialog's text is small for tesseract at the screen's size)."""
    big = os.path.join(out, "export.dialog.x2.png")
    subprocess.run(["convert", png, "-resize", f"{scale * 100}%", big], capture_output=True)
    tsv = subprocess.run(["tesseract", big, "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout
    open(os.path.join(out, "export.dialog.tsv"), "w").write(tsv)
    words = []
    for line in tsv.splitlines()[1:]:
        f = line.split("\t")
        if len(f) == 12 and f[11].strip():
            words.append({"text": f[11].strip(), "left": int(f[6]), "top": int(f[7]), "w": int(f[8]), "h": int(f[9]),
                          "line": (f[2], f[3], f[4])})
    for i in range(len(words) - 2):
        trio = words[i:i + 3]
        if tuple(w["text"] for w in trio) == BUTTON and len({w["line"] for w in trio}) == 1:
            left, top = trio[0]["left"], min(w["top"] for w in trio)
            right = trio[2]["left"] + trio[2]["w"]
            bottom = max(w["top"] + w["h"] for w in trio)
            return {"left": left // scale, "top": top // scale, "right": right // scale, "bottom": bottom // scale}
    return None


def pids_named(name):
    r = subprocess.run(["pgrep", "-x", name], capture_output=True, text=True)
    return [int(p) for p in r.stdout.split()]


def main():
    root, out = sys.argv[1], sys.argv[2]
    rec = {"steps": {}, "notes": []}

    def done(rc):
        rec["rc"] = rc
        json.dump(rec, open(os.path.join(out, "export.json"), "w"), indent=1)
        sys.exit(rc)

    main_wid = find_window("kdenlive", 10, "--class")
    rec["main_wid"] = main_wid
    if main_wid:
        x, y, w, h = geometry(main_wid)
        xdo("mousemove", str(x + w // 2), str(y + h // 2))
        xdo("windowactivate", "--sync", main_wid)
    time.sleep(0.5)
    before = set(pids_named(RENDERER))
    rec["steps"]["shortcut"] = stamp()
    xdo("key", "--clearmodifiers", "ctrl+Return")
    dlg = find_window(DIALOG, 30)
    rec["steps"]["dialog"] = stamp()
    rec["dialog_wid"] = dlg
    if not dlg:
        shot(out, "no-dialog")
        rec["notes"].append("no Rendering dialog within 30 s")
        done(2)
    time.sleep(2.0)   # the dialog's profiles and output path filled before the shot
    dx, dy, dw, dh = geometry(dlg)
    rec["dialog_geometry"] = [dx, dy, dw, dh]
    png = shot(out, "dialog", dlg)
    box = find_button(png, out)
    rec["button"] = box
    if not box:
        shot(out, "no-button")
        rec["notes"].append("no 'Render to File' in the dialog's words")
        done(3)
    bx, by = dx + (box["left"] + box["right"]) // 2, dy + (box["top"] + box["bottom"]) // 2
    rec["click"] = [bx, by]
    xdo("mousemove", str(bx), str(by))
    time.sleep(0.3)
    rec["steps"]["click"] = stamp()
    xdo("click", "1")
    pid, end = None, time.monotonic() + 30
    while pid is None and time.monotonic() < end:
        new = [p for p in pids_named(RENDERER) if p not in before]
        if new:
            pid = new[0]
        else:
            time.sleep(0.05)
    rec["steps"]["renderer_seen"] = stamp()
    if pid is None:
        shot(out, "no-renderer")
        rec["notes"].append(f"{RENDERER} never appeared within 30 s of the click")
        done(4)
    rec["renderer_pid"] = pid
    try:
        argv = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
        rec["renderer_argv"] = [a.decode(errors="replace") for a in argv if a]
    except OSError as e:
        rec["notes"].append(f"argv unread: {e}")
        rec["renderer_argv"] = []
    args = rec["renderer_argv"]
    playlist = next((a for a in args if a.endswith(".mlt")), None)
    rec["playlist"] = playlist
    if playlist:
        try:
            shutil.copyfile(root + playlist, os.path.join(out, "export.playlist.mlt"))
        except OSError as e:
            rec["notes"].append(f"playlist not copied: {e}")
    shot(out, "rendering")
    while os.path.exists(f"/proc/{pid}"):
        time.sleep(0.2)
    rec["steps"]["renderer_gone"] = stamp()
    time.sleep(1.0)
    shot(out, "after")
    done(0)


if __name__ == "__main__":
    main()
