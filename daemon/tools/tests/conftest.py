import copy
import pathlib
import sys

import pytest
import yaml

TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from drivertable.config_schema import ALGORITHMS, MODES  # noqa: E402

REPO = TOOLS.parents[1]


def schema_default_params(algorithm):
    return {name: spec.default for name, spec in ALGORITHMS[algorithm].items()}


def make_table(role="prior"):
    """A minimal valid table: every row defaults to MLFQ; wanted=false rows
    differ from wanted=true rows by their cap so the pair check passes.
    The calibrated role fills all four entries from the schema defaults."""
    rows = []
    for mode in MODES:
        for wanted in (True, False):
            entries = {"MLFQ": {"params": schema_default_params("MLFQ"),
                                "basis": "theory",
                                "justification": "MLFQ keeps the editor responsive."}}
            cap = 0.30 if wanted else 0.05
            if role == "calibrated":
                for alg in ALGORITHMS:
                    params = schema_default_params(alg)
                    if alg == "LOTTERY":   # validator rule 5: batch_share ≤ cap
                        params["batch_share"] = min(params["batch_share"], cap)
                    entries[alg] = {"params": params, "basis": "tuned",
                                    "justification": f"best {alg} on the tuning pool"}
            rows.append({"mode": mode, "background_wanted": wanted,
                         "batch_bandwidth_cap": cap,
                         "default": "MLFQ",
                         "justification": "Interactive work dominates; MLFQ default.",
                         "entries": entries})
    return {"role": role, "rows": rows}


@pytest.fixture
def repo_root():
    return REPO


@pytest.fixture
def table_file(tmp_path):
    def write(table, name="table.yaml"):
        path = tmp_path / name
        path.write_text(yaml.safe_dump(table, sort_keys=False))
        return path
    return write


@pytest.fixture
def prior():
    return make_table("prior")


@pytest.fixture
def calibrated():
    return make_table("calibrated")


def row(table, mode, wanted):
    return next(r for r in table["rows"]
                if r["mode"] == mode and r["background_wanted"] is wanted)


def clone(table):
    return copy.deepcopy(table)
