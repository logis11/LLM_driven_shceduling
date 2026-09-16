#!/usr/bin/env python3
"""Splice fold_in.py's YAML fragment into dataset/archetypes.yaml: every entry
in the fragment replaces the entry of the same id in the library, text for
text, so hand-written entries and comments elsewhere are untouched. An entry
missing from the library is appended under `archetypes:`.

splice.py <fragment.yaml> <archetypes.yaml>
"""

import re
import sys

import yaml


def blocks(text):
    """id -> (start, end) of each top-level entry (two-space indented key) in a YAML text."""
    out = {}
    starts = [(m.start(), m.group(1)) for m in re.finditer(r"^  ([A-Za-z0-9_-]+):\n", text, re.M)]
    for i, (pos, aid) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        out[aid] = (pos, end)
    return out


def main():
    frag_path, lib_path = sys.argv[1], sys.argv[2]
    frag = open(frag_path, encoding="utf-8").read()
    lib = open(lib_path, encoding="utf-8").read()
    fb = blocks(frag)
    replaced, added = [], []
    for aid, (a, b) in fb.items():
        entry = frag[a:b].rstrip("\n") + "\n\n"
        lb = blocks(lib)
        if aid in lb:
            la, lbnd = lb[aid]
            # keep the blank-line spacing the library had after the entry
            lib = lib[:la] + entry + lib[lbnd:].lstrip("\n")
            replaced.append(aid)
        else:
            lib = lib.rstrip("\n") + "\n\n" + entry
            added.append(aid)
    yaml.safe_load(lib)  # must stay loadable
    open(lib_path, "w", encoding="utf-8").write(lib)
    print(f"replaced {replaced}; added {added}")


if __name__ == "__main__":
    main()
