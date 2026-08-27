import pytest

from wlc.units import parse_us


def test_suffixed_forms():
    assert parse_us("250us") == 250
    assert parse_us("50ms") == 50_000
    assert parse_us("1.5s") == 1_500_000
    assert parse_us("8m30s") == 510_000_000
    assert parse_us("1h") == 3_600_000_000


def test_bare_integer_is_us():
    assert parse_us(1234) == 1234


@pytest.mark.parametrize("bad", ["", "10", "5 minutes", "-3s", True, None, 1.5])
def test_rejects(bad):
    with pytest.raises(ValueError):
        parse_us(bad)
