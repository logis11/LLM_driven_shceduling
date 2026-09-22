#!/usr/bin/env python3
"""The session census of the 9.9 campaign (method §2.4) and the idle-state queries its edge check and probe use.

  census.py snapshot <uid> <label> <out.json>    as root: every process, the units, the session, the state
  census.py state <uid>                          one JSON line: SessionIsActive, shield, PowerSaveMode, presence
  census.py check <state.json>                   exit 0 when the state is the terminal idle state (method §3)
  census.py others <uid>                         the pinned units' processes that are none of the entries', one
                                                 "<manager> <pid>" per line, for the sweep to adopt (changelog D15)
  census.py mask <cpu-list>                      a CPU list as the `ay` bitmask StartTransientUnit takes

Every query here reaches a measured process — `systemctl` pid 1 and the user manager, `loginctl` logind over the
system bus, the state queries the session bus, gnome-session and GNOME Shell — so the run calls this outside the
`perf` recording only (changelog D13); the probe's 10 s polls are the stated exception.

The instances the analysis carries are named here, from each process's cgroup (method §4; changelog D4, D6, D7):
pid 1 against the user manager, the system bus against the session bus, the three PipeWire services. A process in a
pinned unit that is not the unit's own program — an Xwayland GNOME Shell starts, a helper it forks — is listed
under `in_unit_other`: on the measured CPU by the pin, in no entry, reported (method §2.4, the held display-server
question).
"""

import json
import os
import re
import subprocess
import sys
import time

PF_KTHREAD = 0x00200000

# entry -> instance -> (cgroup suffix regex, the program's comm regex). `{uid}` is the measured user's.
ENTRIES = {
    "gnome-shell": {"gnome-shell": (r"/user@{uid}\.service/(.*/)?org\.gnome\.Shell@wayland\.service$", r"^gnome-shell$")},
    "pipewire": {"pipewire": (r"/user@{uid}\.service/(.*/)?pipewire\.service$", r"^pipewire$"),
                 "wireplumber": (r"/user@{uid}\.service/(.*/)?wireplumber\.service$", r"^wireplumber$"),
                 "pipewire-pulse": (r"/user@{uid}\.service/(.*/)?pipewire-pulse\.service$", r"^pipewire-pulse$")},
    "systemd": {"pid1": (r"^/init\.scope$", r"^systemd$"),
                "user-manager": (r"/user@{uid}\.service/init\.scope$", r"^systemd$")},
    "dbus-daemon": {"system-bus": (r"^/system\.slice/dbus(-broker)?\.service$", r"^dbus-(daemon|broker)"),
                    "session-bus": (r"/user@{uid}\.service/(.*/)?dbus(-broker)?\.service$", r"^dbus-(daemon|broker)")},
}

# the user units the pin names (method §2.5); `dbus.service` resolves to dbus-broker.service where that is the bus
USER_UNITS = ("dbus.service", "org.gnome.Shell@wayland.service", "pipewire.service", "wireplumber.service",
              "pipewire-pulse.service")


def read(path):
    try:
        with open(path) as handle:
            return handle.read()
    except OSError:
        return ""


def proc(pid):
    raw = read(f"/proc/{pid}/stat")
    if not raw:
        return None
    close = raw.rfind(")")
    comm = raw[raw.find("(") + 1:close]
    rest = raw[close + 2:].split()
    status = read(f"/proc/{pid}/status")
    field = lambda k: next((ln.split(":", 1)[1].strip() for ln in status.splitlines() if ln.startswith(k + ":")), "")
    cg = next((ln[3:] for ln in read(f"/proc/{pid}/cgroup").splitlines() if ln.startswith("0::")), "")
    return {"pid": pid, "ppid": int(rest[1]), "comm": comm,
            "cmd": read(f"/proc/{pid}/cmdline").replace("\0", " ").strip(),
            "uid": int((field("Uid").split() or ["-1"])[0]), "cgroup": cg,
            "cpus_allowed": field("Cpus_allowed_list"), "threads": int(field("Threads") or 0),
            "start_ticks": int(rest[19]), "kthread": bool(int(rest[6]) & PF_KTHREAD)}


def processes():
    out = []
    for p in os.listdir("/proc"):
        if p.isdigit():
            pr = proc(int(p))
            if pr:
                out.append(pr)
    return sorted(out, key=lambda x: x["pid"])


def instances(procs, uid):
    """entry -> instance -> [pids], and the other processes found in those units. A process whose cgroup is an
    instance's unit but whose comm is not the program is the unit's other process, not the instance."""
    out, other = {e: {i: [] for i in insts} for e, insts in ENTRIES.items()}, []
    for pr in procs:
        if pr["kthread"]:
            continue
        for e, insts in ENTRIES.items():
            for i, (cg_rx, comm_rx) in insts.items():
                if not re.search(cg_rx.format(uid=uid), pr["cgroup"]):
                    continue
                if i == "pid1" and pr["pid"] != 1:
                    other.append({"entry": e, "instance": i, "pid": pr["pid"], "comm": pr["comm"], "cmd": pr["cmd"]})
                elif re.search(comm_rx, pr["comm"]):
                    out[e][i].append(pr["pid"])
                else:
                    other.append({"entry": e, "instance": i, "pid": pr["pid"], "comm": pr["comm"], "cmd": pr["cmd"]})
    return out, other


def sh(cmd, user_env=None, timeout=20):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=user_env)
        return {"rc": p.returncode, "out": p.stdout.strip(), "err": p.stderr.strip()[-400:]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"rc": -1, "out": "", "err": str(e)[-400:]}


def as_user(uid):
    """argv prefix and env for a command in the measured user's session (its user manager and session bus)."""
    name = sh(["id", "-nu", str(uid)])["out"]
    run = f"/run/user/{uid}"
    prefix = ["sudo", "-u", name, "env", f"XDG_RUNTIME_DIR={run}", f"DBUS_SESSION_BUS_ADDRESS=unix:path={run}/bus"]
    return prefix


def busctl_value(res):
    """`busctl` prints a property or a reply as `<signature> <value>`: "b true", "i 3", "u 0"."""
    if res["rc"] != 0 or not res["out"]:
        return None
    sig, _, val = res["out"].partition(" ")
    if sig == "b":
        return val.strip() == "true"
    if sig in ("i", "u"):
        try:
            return int(val.split()[0])
        except (ValueError, IndexError):
            return None
    return val


def state(uid):
    """The idle-state queries of method §3: gnome-session's SessionIsActive (S2-31), the shield (S2-13), Mutter's
    PowerSaveMode (S2-32; 0 on, 1 standby, 2 suspend, 3 off, -1 unknown), the presence status (0 available, 3 idle),
    and logind's LockedHint for the user's session."""
    u = as_user(uid)
    q = {
        "session_active": u + ["busctl", "--user", "get-property", "org.gnome.SessionManager", "/org/gnome/SessionManager",
                               "org.gnome.SessionManager", "SessionIsActive"],
        "shield_active": u + ["busctl", "--user", "call", "org.gnome.ScreenSaver", "/org/gnome/ScreenSaver",
                              "org.gnome.ScreenSaver", "GetActive"],
        "power_save_mode": u + ["busctl", "--user", "get-property", "org.gnome.Mutter.DisplayConfig",
                                "/org/gnome/Mutter/DisplayConfig", "org.gnome.Mutter.DisplayConfig", "PowerSaveMode"],
        "presence": u + ["busctl", "--user", "get-property", "org.gnome.SessionManager",
                         "/org/gnome/SessionManager/Presence", "org.gnome.SessionManager.Presence", "status"],
    }
    out = {"mono_ns": time.monotonic_ns(), "raw": {}}
    for k, cmd in q.items():
        res = sh(cmd, timeout=10)
        out[k] = busctl_value(res)
        if out[k] is None:            # what the query answered instead, so a failed check can be read
            out["raw"][k] = {"rc": res["rc"], "out": res["out"][-200:], "err": res["err"][-300:]}
    sess = user_session(uid)
    out["session"] = sess
    out["locked_hint"] = (sh(["loginctl", "show-session", sess, "-p", "LockedHint", "--value"])["out"] == "yes") if sess else None
    return out


def is_idle(st):
    """The terminal idle state at the steady edge (method §3, changelog D13): the shield up, the monitor not on, the
    session active. PowerSaveMode 1–3 are the three DPMS states other than on."""
    return bool(st.get("session_active")) and bool(st.get("shield_active")) and st.get("power_save_mode") in (1, 2, 3)


def user_session(uid):
    for line in sh(["loginctl", "list-sessions", "--no-legend"])["out"].splitlines():
        f = line.split()
        if len(f) >= 2 and f[1] == str(uid):
            return f[0]
    return None


def effective_cpus(procs, uid):
    """cpuset.cpus.effective of every unit an instance lives in: what the pin actually applied (changelog D14)."""
    out = {}
    for pr in procs:
        for insts in ENTRIES.values():
            for cg_rx, _ in insts.values():
                if re.search(cg_rx.format(uid=uid), pr["cgroup"]) and pr["cgroup"] not in out:
                    out[pr["cgroup"]] = read(f"/sys/fs/cgroup{pr['cgroup']}/cpuset.cpus.effective").strip() or None
    return out


def snapshot(uid, label):
    procs = processes()
    inst, other = instances(procs, uid)
    u = as_user(uid)
    sess = user_session(uid)
    cmds = {
        "units.system": ["systemctl", "list-units", "--all", "--no-legend", "--plain", "--no-pager"],
        "units.user": u + ["systemctl", "--user", "list-units", "--all", "--no-legend", "--plain", "--no-pager"],
        "sessions": ["loginctl", "list-sessions", "--no-legend"],
        "session": ["loginctl", "show-session", sess] if sess else ["true"],
        "user": ["loginctl", "show-user", str(uid)],
        "settings": u + ["sh", "-c", "for k in 'org.gnome.desktop.session idle-delay' "
                                     "'org.gnome.desktop.screensaver lock-enabled' 'org.gnome.desktop.screensaver lock-delay' "
                                     "'org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type' "
                                     "'org.gnome.settings-daemon.plugins.power idle-dim'; do "
                                     "echo \"$k $(gsettings get $k 2>&1)\"; done"],
    }
    return {
        "label": label, "uid": uid, "mono_ns": time.monotonic_ns(), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "procs": procs, "instances": inst, "in_unit_other": other,
        "kthreads": [p["pid"] for p in procs if p["kthread"]],
        "effective_cpus": effective_cpus(procs, uid),
        "display_servers": [{"pid": p["pid"], "comm": p["comm"], "cmd": p["cmd"]} for p in procs
                            if p["comm"] in ("Xwayland", "Xorg")],
        "greeter": [{"pid": p["pid"], "comm": p["comm"], "cmd": p["cmd"]} for p in procs
                    if p["comm"].startswith("gdm") or "gdm-" in p["cmd"]],
        "buses": sorted({p["comm"] for p in procs if re.match(r"^dbus-(daemon|broker)", p["comm"])}),
        "commands": {k: sh(c) for k, c in cmds.items()},
        "state": state(uid),
    }


def others(uid):
    """The processes in a pinned unit that are not its program (changelog D15), by the manager that owns their unit:
    `user` under the measured user's manager, `system` otherwise."""
    _, other = instances(processes(), uid)
    for o in sorted(other, key=lambda o: o["pid"]):
        cg = proc(o["pid"]) and proc(o["pid"])["cgroup"] or ""
        yield ("user" if f"/user@{uid}.service/" in cg else "system"), o["pid"]


def mask(cpus):
    """'0-2' -> 'ay 1 7': the bytes of the CPU bitmask, least significant first, as busctl writes an `ay`."""
    bits = set()
    for part in cpus.split(","):
        a, _, b = part.partition("-")
        bits.update(range(int(a), int(b or a) + 1))
    n = max(bits) // 8 + 1
    by = [sum(1 << (c % 8) for c in bits if c // 8 == i) for i in range(n)]
    return "ay " + " ".join(str(x) for x in [n] + by)


def main():
    a = sys.argv[1:]
    if a[:1] == ["snapshot"] and len(a) == 4:
        json.dump(snapshot(int(a[1]), a[2]), open(a[3], "w"), indent=1)
    elif a[:1] == ["state"] and len(a) == 2:
        print(json.dumps(state(int(a[1]))))
    elif a[:1] == ["check"] and len(a) == 2:
        raise SystemExit(0 if is_idle(json.load(open(a[1]))) else 1)
    elif a[:1] == ["others"] and len(a) == 2:
        for mgr, pid in others(int(a[1])):
            print(mgr, pid)
    elif a[:1] == ["mask"] and len(a) == 2:
        print(mask(a[1]))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
