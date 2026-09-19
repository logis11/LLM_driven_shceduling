"""Constructed cases for Thunderbird's `send` operation (9.5 changelog D31): the completion wait and the SMTP peer."""

import json
import smtplib
import socket
import subprocess
import sys
import time
from email.message import EmailMessage
from pathlib import Path

import pytest

from meas.probe import ops_driver

PROBE = Path(__file__).resolve().parents[1] / "meas" / "probe"


def _fake_clock():
    t = [0.0]
    return (lambda: t[0]), (lambda s: t.__setitem__(0, t[0] + s * 1e6)), t


def test_completion_is_the_first_poll_at_the_final_size():
    clock, sleep, t = _fake_clock()
    size = lambda: 0 if t[0] < 100_000 else 100 if t[0] < 140_000 else 500   # the copy lands in two writes
    t1, grew = ops_driver.wait_settled(size, timeout_s=10, settle_s=1.0, poll_s=0.02, clock=clock, sleep=sleep)
    assert t1 == pytest.approx(140_000) and grew == 500


def test_no_growth_is_no_completion():
    clock, sleep, _ = _fake_clock()
    t1, grew = ops_driver.wait_settled(lambda: 42, timeout_s=2, settle_s=1.0, poll_s=0.02, clock=clock, sleep=sleep)
    assert t1 is None and grew == 0


def test_peer_rows_skip_a_missing_file(tmp_path):
    assert ops_driver.peer_rows(str(tmp_path / "none.jsonl")) == []


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_the_peer_stamps_every_message(tmp_path):
    pytest.importorskip("aiosmtpd")
    port, out = _free_port(), tmp_path / "smtp.jsonl"
    peer = subprocess.Popen([sys.executable, str(PROBE / "smtp_peer.py"), str(port), str(out)], stdout=subprocess.PIPE)
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), 0.2).close()
                break
            except OSError:
                time.sleep(0.1)
        m = EmailMessage()
        m["From"], m["To"], m["Subject"] = "measure@example.invalid", "reply@example.invalid", "Re: send-000"
        m.set_content("body")
        m.add_attachment(b"x" * 40_000_000, maintype="application", subtype="octet-stream", filename="big.bin")
        with smtplib.SMTP("127.0.0.1", port) as s:
            s.send_message(m)
        rows = [json.loads(line) for line in out.read_text().splitlines()]
        assert len(rows) == 1 and rows[0]["rcpt"] == ["reply@example.invalid"] and rows[0]["bytes"] > 40_000_000
    finally:
        peer.terminate()
        peer.wait(5)
