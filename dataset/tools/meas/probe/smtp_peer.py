#!/usr/bin/env python3
"""The local SMTP peer of Thunderbird's `send` operation (9.5 changelog D31): aiosmtpd on loopback, started on the
harness CPUs by the `thunderbird-send` appdef. Every message is accepted and discarded; its arrival — the end of the
SMTP data — is stamped on CLOCK_MONOTONIC, the clock perf records on, as one line of a JSONL file:
{"t_us", "bytes", "rcpt"}. No authentication, no TLS: the profile's SMTP server points here in the clear.

smtp_peer.py <port> <out.jsonl>
"""

import json
import signal
import sys
import time

DATA_LIMIT = 256 * 2**20   # above aiosmtpd's 32 MiB default: the message carries the Writer document Base64-encoded


def now_us():
    return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1e6)


class Stamp:
    def __init__(self, out):
        self.out = out

    async def handle_DATA(self, server, session, envelope):
        t = now_us()
        body = envelope.original_content or envelope.content or b""
        with open(self.out, "a") as f:
            f.write(json.dumps({"t_us": t, "bytes": len(body), "rcpt": list(envelope.rcpt_tos)}) + "\n")
        return "250 OK"


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    from aiosmtpd.controller import Controller
    port, out = int(sys.argv[1]), sys.argv[2]
    ctl = Controller(Stamp(out), hostname="127.0.0.1", port=port, server_kwargs={"data_size_limit": DATA_LIMIT})
    ctl.start()
    print(f"smtp peer on 127.0.0.1:{port}", flush=True)
    signal.signal(signal.SIGTERM, lambda *_: (ctl.stop(), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (ctl.stop(), sys.exit(0)))
    while True:
        signal.pause()


if __name__ == "__main__":
    main()
