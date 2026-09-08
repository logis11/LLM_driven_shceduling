"""The oracle's structural isolation (daemon-guide §2.1).

The guide asks for "a separate module that other recognizers cannot even
import" rather than a shared code path with a flag. A module boundary is only
as good as the thing that notices when someone crosses it, so this test is that
thing: it reads the package's own source with `ast` and fails the build the
moment `groundtruth` acquires an importer outside the allowlist.

Adding a name to `ALLOWED_IMPORTERS` is therefore a deliberate, reviewable act
— which is exactly the property the information rule needs. The oracle
recognizer will be added here in 1.3; nothing else should ever be.
"""

import ast
import pathlib

import pytest

PACKAGE = pathlib.Path(__file__).resolve().parents[1] / "daemon"
GUARDED = "groundtruth"

# Relative to the package root. The oracle lands in 1.3.
ALLOWED_IMPORTERS = {
    "groundtruth.py",          # itself
    "recognizers/oracle.py",   # the one condition entitled to the answer key
}


def _modules():
    return sorted(PACKAGE.rglob("*.py"))


def _imports_guarded(tree):
    """True if this module pulls in `groundtruth` by any import spelling."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[-1] == GUARDED for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[-1] == GUARDED:
                return True
            if any(alias.name == GUARDED for alias in node.names):
                return True
    return False


def test_the_guard_can_see_something():
    """A guard that scans an empty tree passes forever and protects nothing."""
    assert len(_modules()) >= 4


@pytest.mark.parametrize("path", _modules(), ids=lambda p: p.name)
def test_only_the_oracle_reads_the_answer_key(path):
    relative = path.relative_to(PACKAGE).as_posix()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    if _imports_guarded(tree) and relative not in ALLOWED_IMPORTERS:
        pytest.fail(
            f"{relative} imports {GUARDED}. Only the oracle recognizer may read "
            f"ground truth (daemon-guide §2.1). If this is the oracle, add it to "
            f"ALLOWED_IMPORTERS; if it is not, the information rule is broken.")


def test_projection_never_mentions_the_answer_key_content():
    """`projection.py` names the `ground_truth` *key* (to refuse a file that
    lacks it) but must never read a label out of it."""
    source = (PACKAGE / "projection.py").read_text(encoding="utf-8")
    for label in ("t_start", "t_end", "attributes", "familiarity"):
        assert label not in source, f"projection.py touches ground-truth field {label}"
