import pathlib
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

REPO = TOOLS.parents[1]
FIXTURES = pathlib.Path(__file__).parent / "fixtures"
MOCKS = ("mock-office", "mock-media", "mock-p1a", "mock-chain", "mock-switch")


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "coreset_wide: reads all 51 compiled coreset files and builds every record row of each; "
        "needs more memory than a 16 GB runner holds (c6-dual), so `make test` leaves these out and "
        "`make test-full` runs them (9.21 D13)")


@pytest.fixture(scope="session")
def repo_root():
    return REPO


@pytest.fixture
def fixture_dir():
    return lambda mock: FIXTURES / mock
