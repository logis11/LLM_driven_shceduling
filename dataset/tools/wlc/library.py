"""Archetype library loader (dataset/archetypes.yaml)."""

import hashlib
import pathlib

import yaml


def git_blob_hex(path):
    """Git blob sha1 of a file's content — the deterministic `@<hex>` pin
    used in canonical meta (matches `git hash-object`)."""
    data = pathlib.Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


class Library:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.blob_hex = git_blob_hex(self.path)
        self.entries = yaml.safe_load(self.path.read_text())["archetypes"]

    def __contains__(self, archetype_id):
        return archetype_id in self.entries

    def entry(self, archetype_id):
        return self.entries[archetype_id]

    def binding_params(self, archetype_id):
        return list(self.entries[archetype_id].get("binding_params") or [])

    def lifetime(self, archetype_id):
        return self.entries[archetype_id]["lifetime"]

    def has_input_channel(self, archetype_id):
        """True iff the archetype's program waits on exogenous input."""
        return _mentions_wait(self.entries[archetype_id]["pattern"]["program"],
                              "input")


def _mentions_wait(program, channel):
    for step in program:
        (op, operand), = step.items()
        if op == "loop" and _mentions_wait(operand, channel):
            return True
        if op == "WAIT" and operand == channel:
            return True
    return False
