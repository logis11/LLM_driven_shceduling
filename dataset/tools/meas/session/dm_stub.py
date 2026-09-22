#!/usr/bin/env python3
"""A stand-in display manager on the system bus, for login mode `stub` (9.9 Q14 test).

GNOME Shell 46.0 creates its screen shield only `if (LoginManager.canLock())` (`js/ui/main.js:230`), and
`canLock()` (`js/misc/loginManager.js:38-53`) returns false unless someone answers the `Version` property of
`org.gnome.DisplayManager.Manager` on the system bus. With GDM masked (changelog D11) nothing does, so the
session never locks and the power daemon never blanks (S2-30) — the terminal idle state of D9 is unreachable.

This owns that name and answers that one property with the installed `gdm3` version. It is a measurement
stand-in, not Ubuntu's software, and is named in the entries' scope wherever it is used.

  dm_stub.py <version>
"""

import sys

import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib  # noqa: E402

NODE = """
<node>
  <interface name='org.gnome.DisplayManager.Manager'>
    <property name='Version' type='s' access='read'/>
  </interface>
</node>
"""


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "46.2"
    info = Gio.DBusNodeInfo.new_for_xml(NODE).interfaces[0]
    loop = GLib.MainLoop()

    def on_bus(connection, _name):
        connection.register_object(
            "/org/gnome/DisplayManager/Manager", info,
            None, None,
            lambda _c, _s, _o, _i, prop: GLib.Variant("s", version) if prop == "Version" else None)

    Gio.bus_own_name(Gio.BusType.SYSTEM, "org.gnome.DisplayManager", Gio.BusNameOwnerFlags.NONE,
                     on_bus, None, lambda *_: sys.exit(1))
    loop.run()


if __name__ == "__main__":
    main()
