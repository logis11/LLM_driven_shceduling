#!/usr/bin/env python3
"""Visible-projection CLI — the hand-check tool for the parse boundary.

    project.py --verify              # corpus on disk == dataset/build.manifest.json
    project.py c1-compile            # that workload's projection, as JSON
    project.py --summary             # one line per workload: tasks, children, departs

The projection is what a recognizer is allowed to see (daemon-guide §3), so
printing it is how a human confirms, by eye against the timeline, that nothing
behavioral leaks and nothing visible is lost.
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from daemon.corpus import DEFAULT_VARIANT, open_corpus  # noqa: E402
from daemon.errors import DaemonError  # noqa: E402
from daemon.jsonio import dumps  # noqa: E402
from daemon.projection import read_projection  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def verify(corpus):
    problems = corpus.verify()
    if problems:
        print(f"{len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"corpus clean ({len(corpus.workload_ids)} workloads, {corpus.variant})")
    return 0


def summary(corpus):
    for workload_id in corpus.workload_ids:
        projection = read_projection(corpus.path(workload_id))
        children = sum(child.count for task in projection.tasks
                       for child in task.children)
        pinned = sum(1 for task in projection.tasks if task.t_depart is not None)
        names = len({task.name for task in projection.tasks})
        print(f"  {workload_id:<14} {len(projection.tasks):>3} tasks "
              f"({names} distinct name(s)), {pinned} pinned depart(s), "
              f"{children} child process(es)")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workload_id", nargs="?")
    parser.add_argument("--verify", action="store_true",
                        help="check the build against the manifest and exit")
    parser.add_argument("--summary", action="store_true",
                        help="one line per workload in the corpus")
    parser.add_argument("--variant", default=DEFAULT_VARIANT)
    args = parser.parse_args()

    try:
        corpus = open_corpus(REPO, variant=args.variant)
        if args.verify:
            return verify(corpus)
        if args.summary:
            return summary(corpus)
        if not args.workload_id:
            parser.error("give a workload id, --summary, or --verify")
        if args.workload_id not in corpus.workload_ids:
            parser.error(f"unknown workload {args.workload_id!r}; "
                         f"known: {', '.join(corpus.workload_ids)}")
        projection = read_projection(corpus.path(args.workload_id))
        sys.stdout.write(dumps(projection.to_json()))
        return 0
    except DaemonError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
