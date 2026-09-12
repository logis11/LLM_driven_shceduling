# boot-defaults

A boot default is the configuration in force at t = 0 before any recognition has happened, the one the `fixed` condition keeps for the whole run, and the one the daemon retreats to on fallback. The runner hands the daemon one of these files by path on every invocation, and the daemon copies it verbatim into the schedule's first entry.

Files are named by content, never by role, so a file's name says what is in it and the per-experiment spec says what it is for.

## The files

- `ostep.json` is the primary: OSTEP §8's worked MLFQ example whole, three queues, a 10 ms top slice, doubling per level, a 100 ms boost, no cap. A test pins it to the daemon's config-schema defaults, so the two cannot drift apart.
- `ostep-slice-<µs>us.json`, nine files, are the same configuration with only the top slice changed: 500, 750, 900, 1 200, 2 000, 3 000, 5 000, 20 000, and 100 000 µs. They are the points of the RQ0 gate spec's boot-default sensitivity sweep, and the reason for each point is written on the spec's sensitivity line. A test pins each to `ostep.json` with the one field swapped.

`schema/boot-default.schema.json` is the frozen configuration shape from the recognition vocabulary §2; `make lint` validates every file here against it.

## How the sweep is used

The runner runs `fixed` once under the primary and once under each alternative the experiment names, and nothing else changes: `oracle` and `random` run on the primary, and the driver table is pinned. The scorer re-scores every condition against each alternative `fixed` run, and the report prints the verdict count per boot default. Adding a point to a sweep is one file here and one line in the experiment spec; it never touches the daemon or the simulator.
