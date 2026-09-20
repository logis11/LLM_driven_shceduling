#!/usr/bin/env python3
"""The chat client's traffic phase driver (9.8 method §2 subject 4): a second Matrix client, against the
client-server API, sending messages into the room the measured client is in.

It is not an Element window and never touches the measured CPU — `desktop/run.sh` runs it through `phase.sh`
with `MEAS_PIN=harness`. The rate is an instrument setting stated as design, not a claim about users: no source
states how often a real client receives messages, so it is chosen high enough that the traffic phase separates
measurably from idle, its purpose being to quantify the gap the idle entry's stated limitation otherwise only
declares. The traffic phase feeds no archetype (changelog D11); it is recorded and released.

Standard library only, as the rest of the meas tree's Python is.
"""

import argparse
import json
import time
import urllib.error
import urllib.request

ROOM_ALIAS = "meas-9-8"


def call(base, path, token=None, body=None, method=None):
    url = f"{base}/_matrix/client/v3{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def login(base, user, password):
    st, body = call(base, "/login", body={"type": "m.login.password",
                                          "identifier": {"type": "m.id.user", "user": user},
                                          "password": password})
    if st != 200:
        raise SystemExit(f"login failed: {st} {body}")
    return body["access_token"]


def room(base, token):
    """The room the measured client sits in: created by alias if it is not there yet, joined otherwise."""
    st, body = call(base, f"/directory/room/%23{ROOM_ALIAS}%3Ameas.local", token)
    if st == 200:
        rid = body["room_id"]
        call(base, f"/join/{rid}", token, body={})
        return rid
    st, body = call(base, "/createRoom", token,
                    body={"room_alias_name": ROOM_ALIAS, "name": "meas 9.8", "preset": "public_chat"})
    if st != 200:
        raise SystemExit(f"createRoom failed: {st} {body}")
    return body["room_id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--per-min", type=float, required=True)
    ap.add_argument("--seconds", type=float, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    token = login(a.base, a.user, a.password)
    rid = room(a.base, token)
    gap = 60.0 / a.per_min
    end = time.monotonic() + a.seconds
    n = 0
    with open(a.out, "w") as f:
        while time.monotonic() < end:
            t = time.monotonic()
            st, body = call(a.base, f"/rooms/{rid}/send/m.room.message/{int(time.time()*1000)}-{n}", token,
                            body={"msgtype": "m.text", "body": f"meas 9.8 traffic {n}"}, method="PUT")
            f.write(json.dumps({"n": n, "mono": t, "status": st,
                                "event_id": body.get("event_id")}) + "\n")
            f.flush()
            n += 1
            time.sleep(max(0.0, gap - (time.monotonic() - t)))
    print(f"traffic: {n} messages at {a.per_min}/min into {rid}")


if __name__ == "__main__":
    main()
