"""Which compiled artifacts change beyond the library's hash, and which demands move (beyond_hash.py)."""
import hashlib

import beyond_hash


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def test_an_artifact_that_differs_only_by_the_library_s_hash_has_not_moved():
    old, new = "a" * 40, "b" * 40
    head = {"x.json": _sha(f'{{"lib": "@{old}", "v": 1}}'.encode()), "y.json": _sha(f'{{"lib": "@{old}", "v": 1}}'.encode())}
    built = {"x.json": f'{{"lib": "@{new}", "v": 1}}'.encode(), "y.json": f'{{"lib": "@{new}", "v": 2}}'.encode()}
    assert beyond_hash.beyond_hash(built, head, new, old) == ["y.json"]


def test_a_demand_moves_when_its_value_differs_from_head_s():
    assert beyond_hash.demand_moves({"a": 1.0, "b": 2.0}, {"a": 1.0, "b": 2.5, "c": 3.0}) == {"b": (2.0, 2.5), "c": (None, 3.0)}
