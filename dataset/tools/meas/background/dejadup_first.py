#!/usr/bin/env python3
"""dejadup_first.py <out dir> — the first backup's driver (9.10 D118), run on the harness CPUs, not measured.

`deja-dup --backup` with no backup made yet opens its "Back Up" assistant on the folders page and the location page
(S2-62 AssistantBackup.vala, add_custom_config_pages, when last-run is empty), then, once the first collection-status
finds no backup, the password page (AssistantOperation.vala:336–375). The driver gives the window the X input focus —
Xvfb runs no window manager — and works it from screenshots, as the Kdenlive export's driver does. The page's text is
read by tesseract's word boxes. The page's default button — "Forward" on a normal page, "Continue" on the password page,
an interrupt page (Assistant.vala:262–300), "Close" on the summary — is drawn in Adwaita's suggested-action blue in the
header bar, white text on blue, which tesseract does not read on the whole window (dry run #177): the button is found
as the blue box in the header bar and its label read from that box alone, thresholded and inverted. "Forward" is
clicked on the folders and location pages as they open; on the password page the password, from DD_BACKUP_PW, goes into
"Encryption password" and "Confirm password", "Remember password" is clicked — its row toggles its switch
(SwitchRow.ui, activatable-widget) — and then "Continue" (D117). The driver waits for deja-dup to exit; a summary page
that stays open, when Déjà Dup has a detail to show, is closed by its "Close". The window is found by its process: the
assistant retitles it per page (Assistant.vala:204–209). Writes first.json: the windows, the pages seen, the clicks,
the steps' times, notes. Exit status: 0 the backup ran and deja-dup exited; 2 no window; 3 no password page; 4
deja-dup still running at the cap.
"""

import json
import os
import re
import subprocess
import sys
import time

from kdenlive_export import centre, geometry, ocr_words, pids_named, stamp, xdo

PROGRAM = "deja-dup"
CAP_S = int(os.environ.get("DD_CAP_S", 4 * 3600))   # run.sh: 20 min on the 100 MB subset
BLUE = "rgb(53,132,228)"   # the default button's fill in the screenshots of dry run #177
HEADER_PX = 56             # the header bar's height in those screenshots


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


def default_button(png, out, name):
    """The header bar's blue box and the label read from it alone, or None."""
    r = subprocess.run(["convert", png, "-crop", f"10000x{HEADER_PX}+0+0", "+repage", "-fuzz", "12%", "-fill", "black",
                        "+opaque", BLUE, "-fill", "white", "-opaque", BLUE, "-format", "%@", "info:"],
                       capture_output=True, text=True)
    m = re.fullmatch(r"(\d+)x(\d+)\+(\d+)\+(\d+)", r.stdout.strip())
    if not m:
        return None
    w, h, x, y = map(int, m.groups())
    if w < 20 or h < 15:
        return None
    lab = os.path.join(out, f"first.{name}.button.png")
    subprocess.run(["convert", png, "-crop", f"{w}x{h}+{x}+{y}", "+repage", "-colorspace", "Gray", "-threshold", "70%",
                    "-negate", "-resize", "300%", "-bordercolor", "white", "-border", "30", lab], capture_output=True)
    text = subprocess.run(["tesseract", lab, "-", "--psm", "7"], capture_output=True, text=True).stdout.strip()
    return {"left": x, "top": y, "w": w, "h": h, "label": text}


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
    time.sleep(3.0)   # the window grows to its first page (dry run #177: 450 × 57 when first found, 450 × 316 after)
    rec["windows"] = [{"wid": w_, "name": xdo("getwindowname", w_).stdout.strip(), "geometry": geometry(w_)}
                      for p in pids_named(PROGRAM) for w_ in xdo("search", "--onlyvisible", "--pid", str(p)).stdout.split()]
    x, y, w, h = geometry(wid)
    xdo("mousemove", str(x + w // 2), str(y + h // 2))
    xdo("windowfocus", wid)
    time.sleep(1.0)
    filled = False
    for n in range(30):   # the password page follows the first collection-status, a few seconds after the location page
        png = shot(out, f"page{n}", wid)
        words = ocr_words(png, out, f"first.page{n}")
        btn = default_button(png, out, f"page{n}")
        page = {"n": n, "words": " ".join(t["text"] for t in words)[:400], "button": btn}
        rec["pages"].append(page)
        enc = phrase(words, ("Encryption", "password"))
        if enc:
            page["kind"] = "password"
            conf = phrase(words, ("Confirm", "password"))
            rem = phrase(words, ("Remember", "password"))
            if not (conf and rem):
                rec["notes"].append(f"password page without its rows: confirm {bool(conf)}, remember {bool(rem)}")
                done(3)
            rec["clicks"].append(["encryption", click_at(wid, enc)])
            xdo("type", "--delay", "40", pw)
            rec["clicks"].append(["confirm", click_at(wid, conf)])
            xdo("type", "--delay", "40", pw)
            rec["clicks"].append(["remember", click_at(wid, rem)])
            time.sleep(1.0)
            png = shot(out, "password-filled", wid)
            go = default_button(png, out, "password-filled")
            rec["password_button"] = go
            rec["steps"]["password"] = stamp()
            if go and go["label"] in ("Continue", "Forward"):
                rec["clicks"].append([go["label"], click_at(wid, go)])
            else:
                rec["notes"].append(f"the filled password page's button read {go and go['label']!r}: Return pressed")
                xdo("key", "Return")
            filled = True
            break
        if btn and btn["label"] == "Forward":
            page["kind"] = "forward"
            rec["clicks"].append([f"forward-{n}", click_at(wid, btn)])
            time.sleep(1.5)
            continue
        page["kind"] = "waiting"
        time.sleep(2.0)
    if not filled:
        subprocess.run(["import", "-window", "root", os.path.join(out, "first.root-nopassword.png")], capture_output=True)
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
            btn = default_button(png, out, "progress")
            if btn and btn["label"] == "Close":
                rec["summary"] = " ".join(t["text"] for t in ocr_words(png, out, "first.summary"))[:600]
                shot(out, "summary", win)
                rec["clicks"].append(["close", click_at(win, btn)])
    rec["steps"]["end"] = stamp()
    if pids_named(PROGRAM):
        shot(out, "cap", dd_window(1) or "root")
        rec["notes"].append(f"deja-dup still running after {CAP_S} s")
        done(4)
    done(0)


if __name__ == "__main__":
    main()
