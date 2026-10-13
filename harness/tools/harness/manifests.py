"""The generated layer's manifests as the harness reads them (9.21 spec, decisions 1, 5, 6).

A generated set's manifest (`dataset/build.<set>.manifest.json`; 9.19 decisions 4–6) carries under `grid`, per
artifact, the file's coordinates — the set's axes (`a`, `b`, `form`, `middle`, `interval`, `relation`,
`focus_name_shared`, `mode`, `tier`, `carrier`, …), its `split` where the set is split — and, since 9.21, its
`placements` (the C1 task sets placed: mode, id suffix, labelled segments, input window) and its `segments`'
labels. The harness reads the manifest as its one source for three things:

- a generated file's axes (decision 5): the records keep their columns, and a reporting line that groups rows by
  an axis joins `workload_id` to the record here (`records`);
- the files an experiment spec selects by those axes (decision 6): `files.select` names a manifest pinned under
  `pins.generated` and a condition on the records' keys, expanded to ids before anything else runs (`select`,
  `expand`) — the selected files join the spec's reporting list, never its judging list (every generated file is
  reporting material);
- the placements the scoring rule expands (decision 1; `scoring.with_generated`).

The compiled artifact of a generated file lies under `dataset/build/<rel>`, `<rel>` the manifest's artifact key, so
`artifact_paths` resolves a workload id to its compiled file for the runner and the lints.
"""

import json
import pathlib

SELECT_KEYS = ("manifest", "where")


def load(path):
    return json.loads(pathlib.Path(path).read_text())


def workload_id(rel):
    """`<set>-<mode>/<id>.workload.json` -> `<id>`."""
    return pathlib.PurePosixPath(rel).name[:-len(".workload.json")]


def records(manifest):
    """{workload id: the file's grid record} over the manifest's artifacts (one artifact per file: the single-lane set)."""
    out = {}
    for rel, record in sorted((manifest.get("grid") or {}).items()):
        wid = workload_id(rel)
        if wid in out:
            raise ValueError(f"{wid}: the manifest lists the file under two artifacts; the harness reads one set per manifest")
        out[wid] = dict(record, _artifact=rel)
    return out


def keys(manifest):
    """The record keys every file of the manifest carries — the axes a selection may name."""
    recs = records(manifest)
    if not recs:
        return set()
    common = None
    for record in recs.values():
        ks = {k for k in record if not k.startswith("_")}
        common = ks if common is None else common & ks
    return common


def artifact_paths(manifest_path, manifest):
    """{workload id: the compiled artifact's path}: `dataset/build/<rel>` beside the manifest."""
    build = pathlib.Path(manifest_path).resolve().parent / "build"
    return {wid: build / record["_artifact"] for wid, record in records(manifest).items()}


def matches(record, where):
    """Every named key equal to its value (a list-valued key equal as a list)."""
    for key, value in where.items():
        if key not in record:
            raise KeyError(key)
        if record[key] != value:
            return False
    return True


def select(manifest, where):
    """The workload ids whose record satisfies `where`, sorted; a key no record carries is a `KeyError`."""
    missing = sorted(set(where) - keys(manifest))
    if missing:
        raise KeyError(f"the manifest's records carry no key {missing}; the keys are {sorted(keys(manifest))}")
    return sorted(wid for wid, record in records(manifest).items() if matches(record, where))


def selections(spec):
    return list(((spec.get("files") or {}).get("select")) or [])


def generated_pins(spec):
    return dict(((spec.get("pins") or {}).get("generated")) or {})


def expand(spec, root):
    """The spec with its selections expanded (decision 6): a copy whose `files.reporting` carries the selected ids
    (sorted, each once) and whose `files` has no `select`, plus {workload id: compiled path} for the selected files
    and {workload id: (manifest name, record)} for their axes. Raises `ValueError` on a selection that names no
    pinned manifest, a key the records lack, or a file already listed."""
    files = dict(spec.get("files") or {})
    judging = list(files.get("judging") or [])
    reporting = list(files.get("reporting") or [])
    variants = list(files.get("variants") or [])
    paths, axes = {}, {}
    pins = generated_pins(spec)
    loaded = {}
    for i, sel in enumerate(selections(spec)):
        name = sel.get("manifest")
        if name not in pins:
            raise ValueError(f"files/select/{i}: manifest {name!r} is not pinned under pins/generated "
                             f"({sorted(pins) or 'none'})")
        if name not in loaded:
            path = pathlib.Path(root) / pins[name]["path"]
            if not path.is_file():
                raise ValueError(f"pins/generated/{name}: {pins[name]['path']!r} is not a file under {root}")
            loaded[name] = (path, load(path))
        path, manifest = loaded[name]
        try:
            chosen = select(manifest, dict(sel.get("where") or {}))
        except KeyError as err:
            raise ValueError(f"files/select/{i}: {err.args[0]}") from None
        if not chosen:
            raise ValueError(f"files/select/{i}: no file of {name!r} satisfies {sel.get('where')!r}")
        compiled = artifact_paths(path, manifest)
        recs = records(manifest)
        for wid in chosen:
            if wid in judging or wid in variants:
                raise ValueError(f"files/select/{i}: {wid!r} is already listed as judging or a variant")
            if wid not in reporting:
                reporting.append(wid)
            paths[wid] = compiled[wid]
            axes[wid] = (name, {k: v for k, v in recs[wid].items() if not k.startswith("_")})
    files["reporting"] = reporting
    files.pop("select", None)
    return dict(spec, files=files), paths, axes


def workload_path(wid, paths, build_dir):
    """A listed file's compiled path: the manifest's for a selected file, `<build_dir>/<id>.workload.json` otherwise."""
    return paths.get(wid) or (pathlib.Path(build_dir) / f"{wid}.workload.json")


__all__ = ["artifact_paths", "expand", "generated_pins", "keys", "load", "matches", "records", "select",
           "selections", "workload_id", "workload_path"]
