"""close_window.py <window-id> — the window's own close, as its title bar's close button asks for it (9.10 D135, the
launch dry run #77): an ICCCM WM_DELETE_WINDOW client message. Xvfb runs no window manager, and Qt fires a window's
shortcuts only in its active window, so Kdenlive took no Ctrl+Q there (as the export's dry run #157 found for its Render
shortcut). Prints whether the window offers WM_DELETE_WINDOW; exit status 0 sent, 2 not offered, 3 no window."""

import sys

from Xlib import X, display, error, protocol


def main():
    d = display.Display()
    try:
        w = d.create_resource_object("window", int(sys.argv[1], 0))
        protocols = w.get_wm_protocols() or []
    except (error.BadWindow, ValueError, IndexError):
        print("no-window")
        sys.exit(3)
    delete = d.intern_atom("WM_DELETE_WINDOW")
    if delete not in protocols:
        print("not-offered")
        sys.exit(2)
    ev = protocol.event.ClientMessage(window=w, client_type=d.intern_atom("WM_PROTOCOLS"),
                                      data=(32, [delete, X.CurrentTime, 0, 0, 0]))
    w.send_event(ev, event_mask=X.NoEventMask)
    d.flush()
    print("sent")


if __name__ == "__main__":
    main()
