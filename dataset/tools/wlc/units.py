"""Human-suffixed durations -> integer microseconds (canonical time unit)."""

import re

_TOKEN = re.compile(r"(\d+(?:\.\d+)?)(us|ms|s|m|h)")
_FACTOR = {"us": 1, "ms": 1_000, "s": 1_000_000, "m": 60_000_000, "h": 3_600_000_000}


def parse_us(value):
    """Parse '8m30s', '50ms', '1.5s', or a bare integer (already µs)."""
    if isinstance(value, bool):
        raise ValueError(f"not a duration: {value!r}")
    if isinstance(value, int):
        if value < 0:
            raise ValueError(f"negative duration: {value}")
        return value
    if not isinstance(value, str):
        raise ValueError(f"not a duration: {value!r}")
    text = value.strip().replace(" ", "")
    pos, total = 0, 0
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"bad duration {value!r} at {text[pos:]!r}")
        total += float(m.group(1)) * _FACTOR[m.group(2)]
        pos = m.end()
    if pos == 0:
        raise ValueError(f"empty duration: {value!r}")
    return round(total)
