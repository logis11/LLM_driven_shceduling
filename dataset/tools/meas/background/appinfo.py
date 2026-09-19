#!/usr/bin/env python3
"""SteamCMD's `app_info_print` read for the 9.7 campaign (method §2 "The depot"; changelog D4, D12).

appinfo.py summary <app-id> <steamcmd-output>...   key=value: the app's Linux install size and its branches
appinfo.py smallest <steamcmd-output>...           the app id whose Linux install size is smallest among the outputs
appinfo.py older <app-id> <steamcmd-output>        the branch to stage for the update phase, or nothing
appinfo.py buildid <app-id> <steamcmd-output> <branch>   that branch's build id

The output holds the app's appinfo as Valve's text KeyValues: quoted keys, quoted values, braces. The install size of
an app on Linux is the sum over its depots whose `config.oslist` is empty or names linux, of the public manifest's
`size` (the installed bytes) where the appinfo carries it, else the depot's `maxsize`; `download` (the bytes fetched)
is summed beside it. The branch to stage (D12) is the non-password branch with the highest build id below the public
one — the nearest older public build.
"""

import re
import sys

TOKEN = re.compile(r'"((?:[^"\\]|\\.)*)"|([{}])')


def parse_kv(text):
    """Nested dicts from KeyValues text (the first top-level key and its block)."""
    toks = [(m.group(1), m.group(2)) for m in TOKEN.finditer(text)]
    pos = 0

    def block():
        nonlocal pos
        out = {}
        while pos < len(toks):
            s, brace = toks[pos]
            if brace == "}":
                pos += 1
                return out
            if brace == "{":   # a stray brace: skip it
                pos += 1
                continue
            pos += 1
            if pos < len(toks) and toks[pos][1] == "{":
                pos += 1
                out[s] = block()
            elif pos < len(toks):
                out[s] = toks[pos][0]
                pos += 1
        return out
    return block()


def app_block(text, app):
    """The appinfo block of one app in a steamcmd output (the last one printed: steamcmd may print a stale copy first)."""
    found = None
    for m in re.finditer(r'^\s*"%s"\s*$' % re.escape(str(app)), text, re.M):
        body = parse_kv(text[m.start():])
        if str(app) in body and isinstance(body[str(app)], dict):
            found = body[str(app)]
    return found


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def summary(info):
    depots = info.get("depots", {}) if info else {}
    size = download = 0
    rows = []
    for key, d in depots.items():
        if not key.isdigit() or not isinstance(d, dict):
            continue
        oslist = (d.get("config", {}) or {}).get("oslist", "") if isinstance(d.get("config"), dict) else ""
        if oslist and "linux" not in oslist.split(","):
            continue
        pub = (d.get("manifests", {}) or {}).get("public") if isinstance(d.get("manifests"), dict) else None
        s = _int(pub.get("size")) if isinstance(pub, dict) else None
        dl = _int(pub.get("download")) if isinstance(pub, dict) else None
        if s is None:
            s = _int(d.get("maxsize"))
        rows.append({"depot": key, "oslist": oslist, "size": s, "download": dl, "from_app": d.get("depotfromapp")})
        size += s or 0
        download += dl or 0
    branches = {}
    for name, b in (depots.get("branches", {}) or {}).items():
        if isinstance(b, dict):
            branches[name] = {"buildid": _int(b.get("buildid")), "timeupdated": _int(b.get("timeupdated")),
                              "pwdrequired": b.get("pwdrequired") == "1", "description": b.get("description")}
    return {"size": size, "download": download, "depots": rows, "branches": branches,
            "name": (info.get("common", {}) or {}).get("name") if info else None}


def older_branch(branches):
    pub = (branches.get("public") or {}).get("buildid")
    if pub is None:
        return None
    cands = [(b["buildid"], n) for n, b in branches.items()
             if n != "public" and not b["pwdrequired"] and b["buildid"] is not None and b["buildid"] < pub]
    return max(cands)[1] if cands else None


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    if a[0] == "summary":
        app, text = a[1], "".join(open(p, errors="replace").read() for p in a[2:])
        s = summary(app_block(text, app))
        print(f"name={s['name']}\nsize={s['size']}\ndownload={s['download']}\ndepots=" +
              ",".join(f"{r['depot']}:{r['size']}" for r in s["depots"]))
        print("branches=" + ",".join(f"{n}:{b['buildid']}{':pwd' if b['pwdrequired'] else ''}" for n, b in sorted(s["branches"].items())))
        print(f"older_branch={older_branch(s['branches']) or ''}")
        return 0
    if a[0] == "smallest":
        best = None
        for p in a[1:]:
            app = re.search(r"(\d+)", p.rsplit("/", 1)[-1])
            if not app:
                continue
            s = summary(app_block(open(p, errors="replace").read(), app.group(1)))
            if s["size"] and (best is None or s["size"] < best[0]):
                best = (s["size"], app.group(1))
        print(best[1] if best else "")
        return 0
    if a[0] == "older":
        s = summary(app_block(open(a[2], errors="replace").read(), a[1]))
        print(older_branch(s["branches"]) or "")
        return 0
    if a[0] == "buildid":   # buildid <app-id> <steamcmd-output> <branch>
        s = summary(app_block(open(a[2], errors="replace").read(), a[1]))
        print((s["branches"].get(a[3]) or {}).get("buildid") or "")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
