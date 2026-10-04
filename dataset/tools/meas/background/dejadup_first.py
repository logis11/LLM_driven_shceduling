#!/usr/bin/env python3
"""dejadup_first.py <out dir> — the first backup's driver (9.10 D118), run on the harness CPUs, not measured.

`deja-dup --backup` with no backup made yet opens its "Back Up" assistant on the folders page and the location page
(S2-62 AssistantBackup.vala, add_custom_config_pages, when last-run is empty), then the password page
(AssistantOperation.vala:336–375). The driver gives the window the X input focus — Xvfb runs no window manager — and
works it by tesseract's word boxes in screenshots, as the Kdenlive export's driver does: "Forward" on the folders and
location pages as they open; on the password page the password, from DD_BACKUP_PW, into "Encryption password" and
"Confirm password", and a click on "Remember password", whose row toggles its switch (SwitchRow.ui,
activatable-widget), then "Forward" (D117). It waits for deja-dup to exit; a summary page that stays open — when
Déjà Dup has a detail to show — is closed by its "Close". Writes first.json: the pages seen, the clicks, the steps'
times, notes. Exit status: 0 the backup ran and deja-dup exited; 2 no window; 3 no password page; 4 deja-dup still
running at the cap.
"""

import json
import os
import subprocess
import sys
import time

from kdenlive_export import centre, geometry, ocr_words, pids_named, stamp, xdo

PROGRAM = "deja-dup"          # the window is found by its process: the assistant retitles it per page (Assistant.vala:204–209)
CAP_S = 4 * 3600


def dd_window(secs):
    """The largest visible window of a deja-dup process, waiting up to secs."""
    end = time.monotonic() + secs
    while True:
        ids = [w for p in pids_named(PROGRAM) for w in xdo("search", "--onlyvisible", "--pid", str(p)).stdout.split()]
        if ids:
            return max(ids, key=lambda w: geometry(w)[2] * geometry(w)[3])
        if time.monotonic() >= end:
            return None
        time.sleep(0.25)


def shot(out, name, wid):
    path = os.path.join(out, f"first.{name}.png")
    subprocess.run(["import", "-window", wid, path], capture_output=True)
    return path


def phrase(words, want):
    """The box of the words `want` in order on one line, in the screenshot's pixels."""
    n = len(want)
    for i in range(len(words) - n + 1):
        run = words[i:i + n]
        if tuple(w["text"].strip(".…:") for w in run) == want and len({w["line"] for w in run}) == 1:
            return {"left": run[0]["left"], "top": min(w["top"] for w in run),
                    "w": run[-1]["left"] + run[-1]["w"] - run[0]["left"], "h": max(w["h"] for w in run)}
    return None


def click_at(wid, box):
    x, y, _w, _h = geometry(wid)
    cx, cy = centre(box)
    xdo("mousemove", str(x + cx), str(y + cy))
    time.sleep(0.3)
    xdo("click", "1")
    time.sleep(0.8)
    return [x + cx, y + cy]


def main():
    out = sys.argv[1]
    pw = os.environ.get("DD_BACKUP_PW", "")
    rec = {"steps": {}, "notes": [], "pages": [], "clicks": []}

    def done(rc):
        rec["rc"] = rc
        json.dump(rec, open(os.path.join(out, "first.json"), "w"), indent=1)
        sys.exit(rc)

    rec["steps"]["start"] = stamp()
    wid = dd_window(180)
    rec["wid"] = wid
    if not wid:
        subprocess.run(["import", "-window", "root", os.path.join(out, "first.no-window.png")], capture_output=True)
        rec["notes"].append("no deja-dup window within 180 s")
        done(2)
    rec["steps"]["window"] = stamp()
    x, y, w, h = geometry(wid)
    xdo("mousemove", str(x + w // 2), str(y + h // 2))
    xdo("windowfocus", wid)
    time.sleep(2.0)
    filled = False
    for n in range(12):
        png = shot(out, f"page{n}", wid)
        words = ocr_words(png, out, f"first.page{n}")
        texts = " ".join(t["text"] for t in words)
        page = {"n": n, "words": texts[:400]}
        rec["pages"].append(page)
        fwd = phrase(words, ("Forward",))
        enc = phrase(words, ("Encryption", "password"))
        if enc and not filled:
            page["kind"] = "password"
            conf = phrase(words, ("Confirm", "password"))
            rem = phrase(words, ("Remember", "password"))
            if not (conf and rem and fwd):
                rec["notes"].append(f"password page without its rows: confirm {bool(conf)}, remember {bool(rem)}, forward {bool(fwd)}")
                done(3)
            rec["clicks"].append(["encryption", click_at(wid, enc)])
            xdo("type", "--delay", "40", pw)
            rec["clicks"].append(["confirm", click_at(wid, conf)])
            xdo("type", "--delay", "40", pw)
            rec["clicks"].append(["remember", click_at(wid, rem)])
            shot(out, "password-filled", wid)
            rec["steps"]["password"] = stamp()
            rec["clicks"].append(["forward", click_at(wid, fwd)])
            filled = True
            break
        if fwd:
            page["kind"] = "forward"
            rec["clicks"].append([f"forward-{n}", click_at(wid, fwd)])
            time.sleep(1.5)
            continue
        page["kind"] = "waiting"
        time.sleep(2.0)
    if not filled:
        rec["notes"].append("no password page among the assistant's pages")
        done(3)
    rec["steps"]["backing_up"] = stamp()
    end, k = time.monotonic() + CAP_S, 0
    while pids_named(PROGRAM) and time.monotonic() < end:
        time.sleep(30)
        k += 1
        win = dd_window(1)
        if win and k % 2 == 0:   # every minute: a summary page left open is closed by its button
            png = shot(out, "progress", win)
            words = ocr_words(png, out, "first.progress")
            close = phrase(words, ("Close",))
            if close and (phrase(words, ("Backup", "Finished")) or phrase(words, ("Backup", "Failed"))):
                rec["summary"] = " ".join(t["text"] for t in words)[:600]
                shot(out, "summary", win)
                rec["clicks"].append(["close", click_at(win, close)])
    rec["steps"]["end"] = stamp()
    if pids_named(PROGRAM):
        shot(out, "cap", dd_window(1) or "root")
        rec["notes"].append(f"deja-dup still running after {CAP_S} s")
        done(4)
    done(0)


if __name__ == "__main__":
    main()
