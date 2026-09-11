"""Machine-readable copy of the frozen `cpu_scheduler` config schema and the
recognizer vocabulary (docs/recognition-vocabulary.md §1–§2, frozen 2026-08-28).

This is the first importable form of that schema; the daemon's validator and
the driver-table lint both read it from here so the two never drift from each
other. Changing anything in this file is a change to a frozen contract.
"""

from dataclasses import dataclass

MODES = (
    "browsing", "office", "mail", "dev", "photo", "meeting", "gaming", "media",
    "video-edit", "compile", "ml-train", "render", "transcode", "indexing",
    "backup", "idle",
)

ATTRIBUTES = ("background_wanted",)


@dataclass(frozen=True)
class Field:
    json_type: str      # "integer" | "number"
    lo: float
    hi: float
    default: float

    def check(self, value):
        """Returns a violation string, or None."""
        if isinstance(value, bool):
            return "must be a number"
        if self.json_type == "integer":
            if not isinstance(value, int):
                return "must be an integer"
        elif not isinstance(value, (int, float)):
            return "must be a number"
        if not self.lo <= value <= self.hi:
            return f"{value} outside [{self.lo:g}, {self.hi:g}]"
        return None


ALGORITHMS = {
    "MLFQ": {
        "num_queues":        Field("integer", 2, 8, 3),
        "timeslice_us":      Field("integer", 500, 100000, 10000),
        "timeslice_growth":  Field("number", 1, 8, 2),
        "boost_interval_us": Field("integer", 10000, 10000000, 100000),
    },
    "EDF": {
        "residual_timeslice_us": Field("integer", 500, 100000, 10000),
    },
    "LOTTERY": {
        "batch_share":  Field("number", 0.01, 0.90, 0.15),
        "timeslice_us": Field("integer", 500, 100000, 10000),
    },
    "FIFO": {},
}

CAP_RANGE = (0.05, 0.95)     # batch_bandwidth_cap: null or within this range

BASES = ("theory", "schema-default", "tuned")
ROLES = ("prior", "calibrated")


def schema_default(algorithm):
    """The boot-default params for an algorithm — what the mapper composes when
    a row has no entry for the algorithm `llm_algo` named."""
    return {name: spec.default for name, spec in ALGORITHMS[algorithm].items()}


def check_params(algorithm, params):
    """Validator rule 2 + rule 3 as a lint: exactly the declared fields, in range.
    Returns a list of violation strings."""
    fields = ALGORITHMS[algorithm]
    errors = []
    for name in fields:
        if name not in params:
            errors.append(f"{algorithm} params: missing {name!r}")
    for name in params:
        if name not in fields:
            errors.append(f"{algorithm} params: unexpected {name!r}")
    for name, spec in fields.items():
        if name in params:
            problem = spec.check(params[name])
            if problem:
                errors.append(f"{algorithm} params.{name} {problem}")
    return errors
