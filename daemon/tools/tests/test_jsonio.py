"""Canonical JSON (daemon-guide §2.7).

Byte-identical reruns are a Phase 1 milestone condition, and formatting is the
cheapest way to lose them: one call site that forgets `sort_keys` produces
files that differ without differing.
"""

from daemon.jsonio import dumps, write


def test_key_order_never_reaches_the_file():
    assert dumps({"b": 1, "a": 2}) == dumps({"a": 2, "b": 1})


def test_sorted_and_newline_terminated():
    text = dumps({"b": 1, "a": 2})
    assert text.startswith('{\n  "a": 2,\n  "b": 1\n}')
    assert text.endswith("}\n")


def test_compact_form_is_one_line():
    text = dumps({"b": 1, "a": 2}, indent=None)
    assert text == '{"a":2,"b":1}\n'


def test_non_ascii_survives_unescaped(tmp_path):
    path = tmp_path / "x.json"
    write(path, {"name": "한글"})
    assert path.read_text(encoding="utf-8") == '{\n  "name": "한글"\n}\n'


def test_writing_twice_is_byte_identical(tmp_path):
    payload = {"queries": [{"t": 1, "a": None}, {"t": 2, "a": True}]}
    first, second = tmp_path / "a.json", tmp_path / "b.json"
    write(first, payload)
    write(second, dict(reversed(list(payload.items()))))
    assert first.read_bytes() == second.read_bytes()
