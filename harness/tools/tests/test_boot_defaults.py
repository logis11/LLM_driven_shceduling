"""The boot-default files (8.5 spec, decisions 8, 9, 19): the frozen
configuration shape under their own schema, and `ostep.json` pinned to the
composition of the daemon's config-schema defaults."""

import json
import sys

import jsonschema

from conftest import REPO

BOOT_DIR = REPO / "harness" / "boot-defaults"
SCHEMA = BOOT_DIR / "schema" / "boot-default.schema.json"


def _schema():
    return json.loads(SCHEMA.read_text())


SWEEP_US = (500, 750, 900, 1200, 2000, 3000, 5000, 20000, 100000)   # the RQ0 gate spec's sweep (8.8)


def test_every_boot_default_validates_against_the_schema():
    files = sorted(BOOT_DIR.glob("*.json"))
    assert [f.name for f in files] == sorted(["ostep.json"] + [f"ostep-slice-{us}us.json" for us in SWEEP_US])
    for f in files:
        jsonschema.Draft202012Validator(_schema()).validate(json.loads(f.read_text()))


def test_each_sweep_point_is_ostep_with_only_the_slice_swapped():
    """The alternative boot defaults of the RQ0 gate spec's sensitivity sweep
    (8.8 spec, decision 1): named by content, the slice in the name is the
    slice in the file, every other value OSTEP's."""
    ostep = json.loads((BOOT_DIR / "ostep.json").read_text())
    for us in SWEEP_US:
        alt = json.loads((BOOT_DIR / f"ostep-slice-{us}us.json").read_text())
        assert alt["params"]["timeslice_us"] == us
        assert alt == {**ostep, "params": {**ostep["params"], "timeslice_us": us}}


def test_the_schema_refuses_a_foreign_field_and_a_bad_cap():
    v = jsonschema.Draft202012Validator(_schema())
    good = json.loads((BOOT_DIR / "ostep.json").read_text())
    bad = dict(good, extra=1)
    assert next(v.iter_errors(bad), None) is not None
    bad = dict(good, batch_bandwidth_cap=1.5)
    assert next(v.iter_errors(bad), None) is not None
    bad = dict(good, algorithm="RR")
    assert next(v.iter_errors(bad), None) is not None


def test_ostep_is_the_composition_of_the_daemons_schema_defaults():
    """The harness never imports the daemon's modules; the test pins the two
    (8.5 spec, decision 19, on the `compose_row` precedent)."""
    sys.path.insert(0, str(REPO / "daemon" / "tools"))
    from drivertable.config_schema import schema_default
    ostep = json.loads((BOOT_DIR / "ostep.json").read_text())
    assert ostep == {"algorithm": "MLFQ", "params": schema_default("MLFQ"),
                     "batch_bandwidth_cap": None}
