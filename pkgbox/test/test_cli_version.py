from pkgbox.cli import cli


def test_version(clirunner):
    res = clirunner.invoke(cli, ['version'])

    assert 0 == res.exit_code
    assert 'v0.0.1\n' == res.output
