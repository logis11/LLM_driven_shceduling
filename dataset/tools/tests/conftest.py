import pathlib
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from wlc import Library  # noqa: E402
from wlc.linter import load_schema  # noqa: E402

REPO = TOOLS.parents[1]
FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def repo_root():
    return REPO


@pytest.fixture(scope="session")
def library():
    return Library(REPO / "dataset" / "archetypes.yaml")


@pytest.fixture(scope="session")
def schema():
    return load_schema(REPO / "dataset" / "schema" / "workload.schema.json")


@pytest.fixture
def fixture_path():
    return lambda name: FIXTURES / name
