import pytest

from pkgbox import errors
from pkgbox.rootfs import types


def test_eq_true_ok():
    r1 = types.RootFS('/')
    r2 = types.RootFS('/')

    assert r1 == r2


def test_eq_false_ok():
    r1 = types.RootFS('/')
    r2 = types.RootFS('/', digest='12456')

    assert not r1 == r2


def test_eq_error():
    with pytest.raises(errors.PBError):
        types.RootFS('/') == 'not a rootfs object'


def test_ne_true_ok():
    r1 = types.RootFS('/', digest='1')
    r2 = types.RootFS('/', digest='2')

    assert r1 != r2


def test_ne_false_ok():
    r1 = types.RootFS('/', digest='123')
    r2 = types.RootFS('/', digest='123')

    assert not r1 != r2


def test_ne_error():
    with pytest.raises(errors.PBError):
        types.RootFS('/', digest='123') != 'aa'
