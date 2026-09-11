"""The driver table as the harness reads it (data-contracts §10): the rows keyed
by (mode, background_wanted) and the composition of a row's default entry into
the configuration the simulator receives — canonical bytes, kept byte-identical
with the daemon's own `compose`, which a test pins (8.4 spec, decision 7).

Separate from the grader so that a program which needs only the table — the
mock daemon — does not import numpy and pandas through it (8.6).
"""

import json
import pathlib
from dataclasses import dataclass, field
from typing import Dict, Optional

import yaml


class DriverTableError(ValueError):
    pass


def compose_row(row) -> str:
    """The configuration a `system`-only condition receives from this row: the
    envelope the simulator sees, as canonical bytes (data-contracts §10). Kept
    byte-identical with the daemon's own `compose`, which a test pins."""
    algorithm = row["default"]
    entry = row["entries"][algorithm]
    config = {"algorithm": algorithm, "params": entry["params"],
              "batch_bandwidth_cap": row["batch_bandwidth_cap"]}
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


@dataclass
class DriverTable:
    role: str
    rows: Dict[tuple, dict] = field(default_factory=dict)

    def row(self, mode, wanted) -> Optional[dict]:
        return self.rows.get((mode, bool(wanted)))

    def default_algorithm(self, mode, wanted) -> Optional[str]:
        row = self.row(mode, wanted)
        return None if row is None else row["default"]


def read_driver_table(path) -> DriverTable:
    doc = yaml.safe_load(pathlib.Path(path).read_text())
    if not isinstance(doc, dict) or not isinstance(doc.get("rows"), list):
        raise DriverTableError(f"{path}: not a driver table")
    rows = {}
    for r in doc["rows"]:
        rows[(r["mode"], bool(r["background_wanted"]))] = r
    return DriverTable(role=doc.get("role", ""), rows=rows)
