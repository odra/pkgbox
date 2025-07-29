import pytest

from pkgbox.errors import PkgboxError


def test_minimal():
    e = PkgboxError('err')

    assert 1 == e.errcode
    assert 'err' == e.errmsg
    assert '[1] err' == str(e)
    assert 'PkgboxError("err", code=1)' == repr(e)


def test_full():
    e = PkgboxError('err', code=10)

    assert 10 == e.errcode
    assert 'err' == e.errmsg
    assert '[10] err' == str(e)
    assert 'PkgboxError("err", code=10)' == repr(e)


def test_exception():
    with pytest.raises(PkgboxError):
        raise PkgboxError('err')
