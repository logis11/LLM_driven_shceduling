"""The recognition daemon: visible projection → telemetry → recognizer →
validator (docs/daemon/daemon-guide.md).

The package is split along the guide's §2.1 information rule, not along
convenience: `projection` may read a canonical workload file and `groundtruth`
may read the answer key, and nothing imports both. Only the oracle recognizer
is entitled to the second one; `tests/test_isolation.py` enforces that.
"""
