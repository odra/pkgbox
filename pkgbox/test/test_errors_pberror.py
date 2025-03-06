import pytest

from pkgbox.errors import PBError


def test_simple():
    e = PBError('error')

    assert 'error' == e.message
    assert 1 == e.code
    assert 'error' == str(e)
    assert 'PBError("error", code=1)' == repr(e)


def test_exception():
    with pytest.raises(PBError) as err:
        raise PBError('err', code=10)
    e = err.value

    assert 'err' == e.message
    assert 10 == e.code
    assert 'err' == str(e)
    assert 'PBError("err", code=10)' == repr(e)
