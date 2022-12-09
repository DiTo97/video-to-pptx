import pathlib

import pytest

from video2pptx import ROOT


@pytest.fixture
def ROOT_tests() -> pathlib.Path:
    return ROOT.parents[1] / "tests"


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "unit: A marker for unit tests")
    config.addinivalue_line("markers", "integration: A marker for integration tests")
    config.addinivalue_line("markers", "e2e: A marker for end-to-end tests")
