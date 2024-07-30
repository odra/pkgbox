import os
import uuid

import pytest
from click.testing import CliRunner


@pytest.fixture
def clirunner():
    return CliRunner()


@pytest.fixture
def tmpdir(tmp_path):
    tmp_path.mkdir(exist_ok=True)

    return tmp_path


@pytest.fixture
def basedir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixdir(basedir):
    return os.path.join(basedir, 'fixtures')


@pytest.fixture
def testdir(basedir):
    return f'{basedir}/testdir'


@pytest.fixture
def manifest_json(fixdir):
    with open(f'{fixdir}/manifest.json', 'r') as f:
        return f.read()


@pytest.fixture
def uid():
    return str(uuid.uuid4())
