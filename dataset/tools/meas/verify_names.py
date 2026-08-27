#!/usr/bin/env python3
"""Name-verification instrument (task-2.6 spec §6; scenario-catalog Note 4).

For each catalog process name: install its package (done by the workflow
step), query the package manifest for the shipped binaries, and — where the
process is headless-launchable — run it while a fast /proc watcher records
the comm/cmdline strings that actually appear. Output: one JSON table,
catalog name -> observed strings -> verification level
(runtime | binary-only | package-not-found | not-attempted).

Container-hostile desktop daemons stay binary-only; account-gated apps stay
not-attempted — stated, never conflated (task-2.6 spec §6).
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

# name -> {pkg: {distro: package}, run: argv or None, watch: comm prefixes,
#          note: optional}
CANDIDATES = {
    "soffice.bin": {
        "pkg": {"ubuntu": "libreoffice-core", "fedora": "libreoffice-core",
                "arch": "libreoffice-fresh"},
        "run": ["soffice", "--headless", "--invisible"], "run_secs": 15,
        "watch": ["soffice"],
    },
    "cc1": {
        "pkg": {"ubuntu": "gcc", "fedora": "gcc", "arch": "gcc"},
        "run": "COMPILE", "run_secs": 10, "watch": ["cc1", "gcc", "as", "ld"],
    },
    "updatedb": {
        "pkg": {"ubuntu": "plocate", "fedora": "plocate", "arch": "plocate"},
        "run": ["updatedb"], "run_secs": 30, "watch": ["updatedb"],
        "note": "expect updatedb.plocate on plocate systems",
    },
    "clamscan": {
        "pkg": {"ubuntu": "clamav", "fedora": "clamav", "arch": "clamav"},
        "run": ["clamscan", "--version"], "run_secs": 5, "watch": ["clamscan"],
    },
    "rsync": {"pkg": {"ubuntu": "rsync", "fedora": "rsync", "arch": "rsync"},
              "run": ["rsync", "--version"], "run_secs": 5, "watch": ["rsync"]},
    "make": {"pkg": {"ubuntu": "make", "fedora": "make", "arch": "make"},
             "run": ["make", "--version"], "run_secs": 5, "watch": ["make"]},
    "tar": {"pkg": {"ubuntu": "tar", "fedora": "tar", "arch": "tar"},
            "run": ["tar", "--version"], "run_secs": 5, "watch": ["tar"]},
    "xz": {"pkg": {"ubuntu": "xz-utils", "fedora": "xz", "arch": "xz"},
           "run": ["xz", "--version"], "run_secs": 5, "watch": ["xz"]},
    "python3": {"pkg": {"ubuntu": "python3", "fedora": "python3",
                        "arch": "python"},
                "run": ["python3", "--version"], "run_secs": 5,
                "watch": ["python3", "python"]},
    "mpv": {"pkg": {"ubuntu": "mpv", "fedora": "mpv", "arch": "mpv"},
            "run": ["mpv", "--no-config", "--version"], "run_secs": 5,
            "watch": ["mpv"]},
    "tracker-miner-fs-3": {
        "pkg": {"ubuntu": "tracker-miner-fs", "fedora": "tracker-miners",
                "arch": "tracker3-miners"},
        "run": None, "watch": ["tracker-miner"],
        "note": "desktop-session daemon; binary-only in containers",
    },
    "baloo_file": {
        "pkg": {"ubuntu": "baloo-kf5", "fedora": "kf5-baloo", "arch": "baloo"},
        "run": None, "watch": ["baloo_file"],
        "note": "desktop-session daemon; binary-only in containers",
    },
    "wineserver": {
        "pkg": {"ubuntu": "wine", "fedora": "wine-core", "arch": "wine"},
        "run": None, "watch": ["wineserver"],
        "note": "binary-only; runtime topology decided at constructor time",
    },
    "gamescope": {
        "pkg": {"ubuntu": "gamescope", "fedora": "gamescope",
                "arch": "gamescope"},
        "run": None, "watch": ["gamescope"],
        "note": "needs a session/GPU; binary-only",
    },
    "HandBrakeCLI": {
        "pkg": {"ubuntu": "handbrake-cli", "fedora": None,
                "arch": "handbrake-cli"},
        "run": ["HandBrakeCLI", "--version"], "run_secs": 5,
        "watch": ["HandBrakeCLI", "handbrake"],
        "note": "fedora needs rpmfusion; recorded as package-not-found there",
    },
    "transmission-daemon": {
        "pkg": {"ubuntu": "transmission-daemon", "fedora": "transmission-daemon",
                "arch": "transmission-cli"},
        "run": None, "watch": ["transmission"],
    },
    "borg": {"pkg": {"ubuntu": "borgbackup", "fedora": "borgbackup",
                     "arch": "borg"},
             "run": ["borg", "--version"], "run_secs": 5, "watch": ["borg"]},
    "rclone": {"pkg": {"ubuntu": "rclone", "fedora": "rclone", "arch": "rclone"},
               "run": ["rclone", "version"], "run_secs": 5, "watch": ["rclone"]},
    "thunderbird": {
        "pkg": {"ubuntu": "thunderbird", "fedora": "thunderbird",
                "arch": "thunderbird"},
        "run": None, "watch": ["thunderbird"],
        "note": "GUI; binary-only (ubuntu 24.04 apt package is a snap stub — "
                "recorded as found only if a real binary ships)",
    },
    "gimp": {"pkg": {"ubuntu": "gimp", "fedora": "gimp", "arch": "gimp"},
             "run": None, "watch": ["gimp"], "note": "GUI; binary-only"},
    "kdenlive": {"pkg": {"ubuntu": "kdenlive", "fedora": "kdenlive",
                         "arch": "kdenlive"},
                 "run": None, "watch": ["kdenlive"], "note": "GUI; binary-only"},
    "ffmpeg": {"pkg": {"ubuntu": "ffmpeg", "fedora": None, "arch": "ffmpeg"},
               "run": ["ffmpeg", "-version"], "run_secs": 5, "watch": ["ffmpeg"],
               "note": "fedora needs rpmfusion for full ffmpeg"},
}

NOT_ATTEMPTED = {
    "steam": "proprietary/account-gated", "steamwebhelper": "ships with steam",
    "discord": "proprietary", "zoom": "proprietary",
    "teams-for-linux": "third-party packaging", "spotify": "proprietary",
    "code": "microsoft branding build", "chrome": "measured in meas-gui",
    "slack": "proprietary", "ollama": "not packaged in distro repos",
    "evince": "GUI; covered by name only", "darktable": "GUI",
    "blender": "GUI", "vlc": "GUI",
    "gnome-shell": "session infra", "Xorg": "session infra",
    "pipewire": "session infra", "systemd": "pid 1", "dbus-daemon": "session infra",
    "game.exe": "placeholder name by construction",
}


class CommWatcher(threading.Thread):
    """Fast /proc scan (~5 ms) recording every comm/cmdline seen."""

    def __init__(self):
        super().__init__(daemon=True)
        self.seen = {}
        self.running = True

    def run(self):
        while self.running:
            for entry in os.listdir("/proc"):
                if not entry.isdigit():
                    continue
                try:
                    with open(f"/proc/{entry}/comm", "rb") as handle:
                        comm = handle.read().decode("ascii", "replace").strip()
                    if comm not in self.seen:
                        with open(f"/proc/{entry}/cmdline", "rb") as handle:
                            cmdline = handle.read().decode(
                                "ascii", "replace").replace("\0", " ").strip()
                        self.seen[comm] = cmdline[:200]
                except OSError:
                    continue
            time.sleep(0.005)


def distro_id():
    with open("/etc/os-release") as handle:
        for line in handle:
            if line.startswith("ID="):
                raw = line.strip().split("=", 1)[1].strip('"')
                return {"ubuntu": "ubuntu", "debian": "ubuntu",
                        "fedora": "fedora", "arch": "arch"}.get(raw, raw)
    return "unknown"


def package_binaries(distro, package):
    commands = {
        "ubuntu": ["dpkg", "-L", package],
        "fedora": ["rpm", "-ql", package],
        "arch": ["pacman", "-Qlq", package],
    }
    try:
        result = subprocess.run(commands[distro], capture_output=True,
                                text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines()
            if "/bin/" in line or "/libexec/" in line or "/lib/" in line]


def run_and_watch(candidate, workdir):
    watcher = CommWatcher()
    watcher.start()
    argv = candidate["run"]
    if argv == "COMPILE":
        source = os.path.join(workdir, "probe.c")
        with open(source, "w") as handle:
            handle.write("#include <stdio.h>\n"
                         "int main(void){printf(\"x\\n\");return 0;}\n")
        argv = ["gcc", "-O2", "-c", source, "-o", source + ".o"]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=candidate.get("run_secs", 10))
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    except OSError as err:
        watcher.running = False
        return {"error": str(err)}
    time.sleep(0.05)
    watcher.running = False
    watcher.join(timeout=2)
    prefixes = tuple(candidate["watch"])
    return {comm: cmdline for comm, cmdline in sorted(watcher.seen.items())
            if comm.startswith(prefixes)}


def main():
    distro = distro_id()
    workdir = tempfile.mkdtemp(prefix="meas-names-")
    table = {"distro": distro, "results": {}, "not_attempted": NOT_ATTEMPTED}
    for name, candidate in CANDIDATES.items():
        package = candidate["pkg"].get(distro)
        record = {"package": package, "note": candidate.get("note")}
        if package is None:
            record["level"] = "package-not-found"
            table["results"][name] = record
            continue
        binaries = package_binaries(distro, package)
        if binaries is None:
            record["level"] = "package-not-found"
            table["results"][name] = record
            continue
        record["binaries"] = [b for b in binaries
                              if any(part in os.path.basename(b).lower()
                                     for part in (name.lower().split(".")[0],
                                                  *candidate["watch"]))][:10]
        if candidate["run"] and (shutil.which(candidate["run"][0])
                                 if candidate["run"] != "COMPILE" else True):
            observed = run_and_watch(candidate, workdir)
            record["observed"] = observed
            record["level"] = ("runtime" if observed and "error" not in observed
                              else "binary-only")
        else:
            record["level"] = "binary-only"
        table["results"][name] = record
    json.dump(table, sys.stdout, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
