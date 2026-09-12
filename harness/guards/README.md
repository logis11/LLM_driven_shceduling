# guards

A guard is a check that must pass before a run's numbers are read. It does not say whether a configuration was good; it says whether the run is evidence at all. A condition that scored well while most of its configurations were fallbacks, a simulator whose rerun differs from its first run, a task starved past the executor's own safety net: each of those is a run whose numbers say nothing about recognition, and each has a guard.

Two files live here. `guard-spec.yaml` is the list of guards with their thresholds, the conditions each applies to, the C2 pairs, and a grounding for every threshold. `schema/guards.schema.json` is the shape of the guards file the checks write.

**The guard spec is frozen at version 1.0** (2026-09-12, `../CHANGELOG.md`). The RQ0 gate spec pins its bytes and its version. Exemptions are never written here: they are the experiment's data, with a reason each, in the per-experiment spec.

## The eight guards

| guard | what it catches |
|---|---|
| `provenance_share` | a run that spent most of its time on `fallback` or `held` configurations |
| `config_age` | a configuration taking effect after the situation it was computed for had ended |
| `starvation_floor` | a ready task waiting longer than the executor's starvation window |
| `determinism` | a rerun trace that is not byte-identical to the first |
| `utilisation_sanity` | delivered CPU exceeding the lane's elapsed time, or a scored file that delivered none: an empty trace that parsed |
| `tick_count` | any consistency message from the records build: a chain tail's iterations not matching its head's ticks, the deadline cross-check, stimulus counts against the run file, applied config lines against the schedule |
| `validation_matches_provenance` | the log's `validation` sequence not equal, entry by entry, to the schedule's `provenance` sequence after the boot entry |
| `c2_pair` | the two files of a C2 pair producing identical trace bodies under a recognition-driven condition, or different ones under `fixed`; identical under `oracle` means the configuration never changed between wanted and unwanted |

Each threshold's grounding is written in the spec's header: an arithmetic identity, a structural rule, or a stated assumption marked as such. The starvation window is the one stated assumption still waiting on its owner, and the RQ0 gate spec records that.

## The guards file

One row per (run, guard), dense: `result` is `pass`, `fail`, or `not_applicable`, with the measured `value`, the `threshold` in force, the `partner` for the two pair guards, and a `reason` on every fail. A guard whose input is missing fails: it has not cleared the run. `not_applicable` is reserved for runs the guard's scope excludes by construction.

## Running the guards

```
python3 tools/guards.py --manifest guards-manifest.json --out guards.csv     # exit 2 if any guard failed
python3 tools/guards_lint.py                                                   # the spec against schema, registry, and the C2 recipe
```

The manifest lists every run in the set with its records, schedule, log, workload, rerun trace, and the guard messages the records build produced; the pair guards need the whole set at once because they need a partner. The runner writes the manifest and runs the guards for every experiment. A non-exempt failure on a run the RQ0 criterion reads turns the verdict into `invalid`, naming the guard and the run.
