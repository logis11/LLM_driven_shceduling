#!/usr/bin/env python3
"""The 9.10 desktop sections' shared pieces: the tracer, with the scripted peers each job names by a pid file, and
the per-component tally in the census's form (`census_campaign.tally`), extended with the chain rule's split.

Peers, by the pid files the jobs write: `synapse.pid` (Element's Matrix homeserver) is `stand-in`, as the census has
it; `httpd.pid` (the loopback page server Chrome's pages come from) and `smtp.pid` (Thunderbird's SMTP peer) are
long-lived `python3` processes the census classes `harness-python` by their name — they are kept in that class and
labelled by what they serve, counted apart from `outside`.

Per component: n, run, span, classes {class: {n, run}}, labels, `split` {direct, inherited: {n, run}} over the
outside-cause wakes (direct: the wake's own wakeup row names the outside waker — chain_roots' `direct_row`), `how`
{direct, chain, relay, D: n} over the outside-cause wakes (how the cause reached the wake), and the largest group of
outside-cause wakes one root row reached.
"""

import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402

PEER_FILES = {"synapse.pid": ("stand-in", "Synapse, the Matrix homeserver (the scripted peer)"),
              "httpd.pid": ("harness-python", "the loopback page server (httpd.pid, python3)"),
              "smtp.pid": ("harness-python", "the SMTP peer (smtp.pid, python3)")}


class PeerTracer(cr.RootTracer):
    """chain_roots.RootTracer with each scripted peer classed and labelled by its pid file."""

    def __init__(self, *a, servers=None, **k):
        super().__init__(*a, **k)
        self.servers = dict(servers or {})

    def process(self, pid, comm):
        if pid in self.servers:
            return self.servers[pid]
        return super().process(pid, comm)


def servers_of(D):
    out = {}
    for f, v in PEER_FILES.items():
        p = cc.read_pid(os.path.join(D, f))
        if p:
            out[p] = v
    return out


def tally(traced, name_of, span_of):
    """traced: chain_roots.RootTracer.trace's rows. name_of(row) -> component; span_of(component) -> its span (s)."""
    out = {}
    groups = collections.defaultdict(lambda: collections.Counter())
    for r, cls, lab, how, root, hops, direct in traced:
        name = name_of(r)
        c = out.setdefault(name, {"n": 0, "run": 0.0, "span": span_of(name), "classes": {}, "labels": {},
                                  "split": {"direct": {"n": 0, "run": 0.0}, "inherited": {"n": 0, "run": 0.0}},
                                  "how": {}, "largest_root": 0, "gone": []})
        c["n"] += 1
        c["run"] += r.run
        k = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        k["n"] += 1
        k["run"] += r.run
        if cls != "own":
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls == "outside":
            s = c["split"]["direct" if direct else "inherited"]
            s["n"] += 1
            s["run"] += r.run
            c["how"][how] = c["how"].get(how, 0) + 1
            if root is not None:
                groups[name][root] += 1
        if cls in ("outside", "harness-python"):
            c["gone"].append([round(r.t_in, 6), r.comm, r.tid, round(r.run, 3), cls, lab, how, bool(direct)])
    for name, g in groups.items():
        out[name]["largest_root"] = max(g.values())
    return out


def merge_counts(dst, src):
    """Add one tally's numbers into another (the same component over two streams)."""
    for name, c in src.items():
        d = dst.setdefault(name, {"n": 0, "run": 0.0, "span": c["span"], "classes": {}, "labels": {},
                                  "split": {"direct": {"n": 0, "run": 0.0}, "inherited": {"n": 0, "run": 0.0}},
                                  "how": {}, "largest_root": 0, "gone": []})
        d["n"] += c["n"]
        d["run"] += c["run"]
        for cls, x in c["classes"].items():
            y = d["classes"].setdefault(cls, {"n": 0, "run": 0.0})
            y["n"] += x["n"]
            y["run"] += x["run"]
        for lab, n in c["labels"].items():
            d["labels"][lab] = d["labels"].get(lab, 0) + n
        for s in ("direct", "inherited"):
            d["split"][s]["n"] += c["split"][s]["n"]
            d["split"][s]["run"] += c["split"][s]["run"]
        for h, n in c["how"].items():
            d["how"][h] = d["how"].get(h, 0) + n
        d["largest_root"] = max(d["largest_root"], c["largest_root"])
        d["gone"].extend(c["gone"])
    return dst
