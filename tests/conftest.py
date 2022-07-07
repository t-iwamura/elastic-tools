from pathlib import Path

import pytest

tests_dir_path = Path(__file__).resolve().parent
INPUTS_DIR_PATH = tests_dir_path / "data" / "inputs"


@pytest.fixture()
def al_dir_path():
    return INPUTS_DIR_PATH / "Al"
