"""The compiled workload corpus, and the hashes a run was made against.

The daemon's inputs are the dataset tree's build output (`make -C dataset
dataset`), which is deliberately not committed — `dataset/build.manifest.json`
carries a sha256 per artifact instead. Two things follow, and both are this
module's job.

**Verify before reading.** A daemon sweep that silently ran against a stale or
locally-modified build would produce recognition logs that no one can reproduce,
which is the failure mode the manifest exists to prevent.

**Pin what was read.** `pin()` returns the digest of every file a run consumed,
for the run's own provenance record. When the recognition logs are regenerated
months later, this is what says whether the inputs were the same.

`coreset-single` is the default variant because the experiments run on the
single-lane compile mode (workload/building-plan §2); `coreset-native` is built
too and is selectable, but nothing in the experiment reads it.
"""

import hashlib
import json
import pathlib

from .errors import CorpusError

DEFAULT_VARIANT = "coreset-single"
CORESET_SIZE = 24


def _digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def _manifest(manifest_path):
    try:
        with open(manifest_path, encoding="utf-8") as handle:
            document = json.load(handle)
    except OSError as exc:
        raise CorpusError(f"{manifest_path}: cannot be opened ({exc.strerror}). "
                          f"Run `make -C dataset dataset`.") from exc
    except json.JSONDecodeError as exc:
        raise CorpusError(f"{manifest_path}: not JSON ({exc})") from exc
    artifacts = document.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise CorpusError(f"{manifest_path}: no artifacts map")
    return artifacts


class Corpus:
    """The workload files of one build variant, checked against the manifest."""

    def __init__(self, build_dir, manifest_path, variant=DEFAULT_VARIANT):
        self.build_dir = pathlib.Path(build_dir)
        self.manifest_path = pathlib.Path(manifest_path)
        self.variant = variant
        self._expected = {
            key.split("/", 1)[1]: digest
            for key, digest in _manifest(self.manifest_path).items()
            if key.startswith(f"{variant}/")
        }
        if not self._expected:
            raise CorpusError(f"{self.manifest_path}: no artifacts for variant "
                              f"{variant!r}")

    @property
    def workload_ids(self):
        return tuple(sorted(name[: -len(".workload.json")]
                            for name in self._expected))

    def path(self, workload_id):
        return self.build_dir / self.variant / f"{workload_id}.workload.json"

    def verify(self):
        """Return the list of problems — missing files and digest mismatches —
        empty when the build on disk is exactly the manifest's."""
        problems = []
        for name in sorted(self._expected):
            path = self.build_dir / self.variant / name
            if not path.exists():
                problems.append(f"{self.variant}/{name}: missing "
                                f"(run `make -C dataset dataset`)")
                continue
            actual = _digest(path)
            if actual != self._expected[name]:
                problems.append(f"{self.variant}/{name}: sha256 {actual[:12]}… "
                                f"≠ manifest {self._expected[name][:12]}…")
        count = len(self._expected)
        if self.variant == DEFAULT_VARIANT and count != CORESET_SIZE:
            problems.append(f"{self.variant}: manifest lists {count} files, "
                            f"expected the {CORESET_SIZE}-file coreset")
        return problems

    def pin(self):
        """`{artifact key: sha256}` for every file of this variant, as read from
        disk — the provenance stamp of one daemon run."""
        return {f"{self.variant}/{name}": _digest(self.build_dir / self.variant / name)
                for name in sorted(self._expected)
                if (self.build_dir / self.variant / name).exists()}


def open_corpus(repo_root, variant=DEFAULT_VARIANT):
    """The corpus at its conventional place in the repo."""
    repo_root = pathlib.Path(repo_root)
    return Corpus(repo_root / "dataset" / "build",
                  repo_root / "dataset" / "build.manifest.json",
                  variant=variant)
