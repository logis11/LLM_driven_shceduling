import pathlib
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

REPO = TOOLS.parents[1]
FIXTURES = pathlib.Path(__file__).parent / "fixtures"
MOCKS = ("mock-office", "mock-media", "mock-p1a", "mock-chain")


@pytest.fixture(scope="session")
def repo_root():
    return REPO


@pytest.fixture
def fixture_dir():
    return lambda mock: FIXTURES / mock
