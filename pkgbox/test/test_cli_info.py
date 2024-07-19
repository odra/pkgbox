import os
from unittest import mock

from pkgbox import errors
from pkgbox.cli import cli


def test_ok(clirunner):
    res = clirunner.invoke(cli, ['info'])
    
    assert res.exception == errors.PBNotImplementedError()
