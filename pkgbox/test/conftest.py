import pytest
from click.testing import CliRunner


@pytest.fixture
def clirunner():
    return CliRunner()


@pytest.fixture
def tmpdir(tmp_path):
    tmp_path.mkdir(exist_ok=True)

    return tmp_path
