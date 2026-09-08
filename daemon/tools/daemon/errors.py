"""Every refusal the daemon raises at an input boundary.

They subclass `ValueError` so a caller may catch the family, and they carry
the offending file's name, because a daemon run covers 24 workloads and "which
file" is the first question asked.
"""


class DaemonError(ValueError):
    """Base for every input-boundary refusal."""


class ProjectionError(DaemonError):
    """The canonical workload file cannot be projected (data-contracts §4)."""


class GroundTruthError(DaemonError):
    """The answer key cannot be read (data-contracts §4, `ground_truth`)."""


class CorpusError(DaemonError):
    """The compiled corpus is missing, or does not match the build manifest."""
