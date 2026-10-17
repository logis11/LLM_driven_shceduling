#!/usr/bin/env python3
"""A training loop stand-in for the `python3` ml-train binding (9.6 changelog
D7; campaign method §2). A small convolutional network trained on synthetic
32×32 images for a fixed number of steps — design: no source states the job;
what is measured is the process's CPU, threads and waits while it runs.

train.py <steps> [--batch 64] [--record out.json]
"""
import argparse
import json
import os
import sys
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("steps", type=int)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--record", default=None)
    args = ap.parse_args()
    rec = {"steps": args.steps, "batch": args.batch, "affinity": sorted(os.sched_getaffinity(0)),
           "cpu_count": os.cpu_count()}
    try:
        import torch
        import torch.nn as nn
    except ImportError as exc:
        rec["torch"] = None
        rec["error"] = str(exc)
        if args.record:
            json.dump(rec, open(args.record, "w"), indent=1)
        print("torch unavailable:", exc, file=sys.stderr)
        return 3
    rec["torch"] = torch.__version__
    rec["threads"] = torch.get_num_threads()
    rec["interop_threads"] = torch.get_num_interop_threads()
    torch.manual_seed(20260917)
    net = nn.Sequential(
        nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(64 * 8 * 8, 256), nn.ReLU(), nn.Linear(256, 10))
    opt = torch.optim.SGD(net.parameters(), lr=0.01, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()
    x = torch.randn(args.batch, 3, 32, 32)
    y = torch.randint(0, 10, (args.batch,))
    t0 = time.monotonic()
    for step in range(args.steps):
        opt.zero_grad()
        loss = loss_fn(net(x), y)
        loss.backward()
        opt.step()
    rec["wall_s"] = time.monotonic() - t0
    rec["final_loss"] = float(loss)
    if args.record:
        json.dump(rec, open(args.record, "w"), indent=1)
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
