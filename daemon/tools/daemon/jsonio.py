"""Canonical JSON writing — the daemon's byte-identical-rerun guarantee.

The Phase 1 milestone is that a rerun reproduces every output byte for byte
(daemon-guide §2.7), and the harness cross-checks daemon files against each
other. That only holds if *one* function writes them, with the formatting fixed
here rather than at each call site:

  * `sort_keys=True` — dict insertion order must never reach a file.
  * `separators=(",", ":")` for compact bodies, or a fixed 2-space indent for
    files a human hand-checks; both are stable, neither is negotiable per call.
  * `ensure_ascii=False` with an explicit UTF-8 encoding — process names are
    ASCII today, but the escaping must not silently depend on that.
  * a trailing newline, so the files are diffable and `git` stops warning.

Deliberately the standard library and not `orjson`: the daemon writes a few
dozen small files, so serialisation speed is worth nothing here, while a
compiled dependency whose output could shift across versions costs the exact
guarantee this module exists to provide. `orjson`'s key sort is also documented
as unstable for duplicate keys.
"""

import json


def dumps(value, *, indent=2):
    """Canonical text for `value`, newline-terminated.

    `indent=None` gives the compact form (for JSONL, where one record is one
    line); the default indents, for files that get read by a person.
    """
    separators = (",", ": ") if indent is not None else (",", ":")
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      indent=indent, separators=separators) + "\n"


def write(path, value, *, indent=2):
    """Write `value` to `path` canonically. Returns the bytes written."""
    text = dumps(value, indent=indent)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return len(text.encode("utf-8"))
