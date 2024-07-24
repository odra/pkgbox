import pytest

from pkgbox import errors
from pkgbox.oci.v1 import Digest


def test_str_ok():
    o = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')

    assert str(o) == 'sha1:8843d7f92416211de9ebb963ff4ce28125932878'


def test_eq_obj_ok():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')

    assert o1 == o2


def test_eq_obj_err():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = Digest('sha1', '60518c1c11dc0452be71a7118a43ab68e3451b82')

    assert not o1 == o2


def test_eq_str_ok():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = 'sha1:8843d7f92416211de9ebb963ff4ce28125932878'

    assert o1 == o2


def test_eq_str_err():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = 'sha1:60518c1c11dc0452be71a7118a43ab68e3451b82'

    assert not o1 == o2


def test_ne_obj_ok():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = Digest('sha1', '60518c1c11dc0452be71a7118a43ab68e3451b82')

    assert o1 != o2


def test_ne_obj_err():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')

    assert not o1 != o2


def test_ne_str_ok():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = 'sha1:60518c1c11dc0452be71a7118a43ab68e3451b82'

    assert o1 != o2


def test_ne_str_err():
    o1 = Digest('sha1', '8843d7f92416211de9ebb963ff4ce28125932878')
    o2 = 'sha1:8843d7f92416211de9ebb963ff4ce28125932878'

    assert not o1 != o2


def test_from_str_ok():
    o = Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878')

    assert o.alg == 'sha1'
    assert o.value == '8843d7f92416211de9ebb963ff4ce28125932878'


def test_from_str_err():
    with pytest.raises(errors.PBValidationError):
        Digest.from_str('sha18843d7f92416211de9ebb963ff4ce28125932878')
