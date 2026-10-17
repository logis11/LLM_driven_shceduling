#!/usr/bin/env python3
"""Open an X window and log every KeyPress it receives with the server time
(ms) and the client monotonic clock (us). One JSON line per event to the
file named in argv[1]; exits after argv[2] seconds. probe tooling for the
9.5 campaign: measures how faithfully a replay driver delivers intervals.
"""

import json
import sys
import time

from Xlib import X, display

out_path, seconds = sys.argv[1], float(sys.argv[2])
disp = display.Display()
screen = disp.screen()
win = screen.root.create_window(
    10, 10, 400, 200, 1, screen.root_depth,
    background_pixel=screen.white_pixel,
    event_mask=X.KeyPressMask | X.ExposureMask)
win.set_wm_name("xkeylog")
win.map()
disp.flush()
t_end = time.monotonic() + seconds
with open(out_path, "w") as log:
    while time.monotonic() < t_end:
        while disp.pending_events():
            ev = disp.next_event()
            if ev.type == X.KeyPress:
                log.write(json.dumps({"server_ms": ev.time,
                                      "mono_us": int(time.monotonic() * 1e6),
                                      "keycode": ev.detail}) + "\n")
                log.flush()
        time.sleep(0.001)
