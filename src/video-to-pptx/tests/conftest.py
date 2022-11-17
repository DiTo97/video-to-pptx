import pathlib

import pytest

from video2pptx import ROOT


@pytest.fixture
def ROOT_tests() -> pathlib.Path:
    return ROOT.parents[1] / "tests"
