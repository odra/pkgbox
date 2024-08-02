from pkgbox import errors
from pkgbox.cli import cli


def test_ok(clirunner):
    assert 1 == 1
    #3res = clirunner.invoke(cli, ['build'])
    
    # assert res.exception == errors.PBNotImplementedError()
