import pytest

from pkgbox import errors
from pkgbox.oci.v1 import MediaType


def test_str_ok():
    o = MediaType('application', 'vnd.oci.image.config.v1', 'json')

    assert str(o) == 'application/vnd.oci.image.config.v1+json'


def test_eq_obj_ok():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = MediaType('application', 'vnd.oci.image.config.v1', 'json')

    assert o1 == o2


def test_eq_str_ok():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = 'application/vnd.oci.image.config.v1+json'

    assert o1 == o2


def test_eq_obj_err():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = MediaType('application', 'vnd.oci.image.config.v1', None)

    assert not o1 == o2


def test_eq_str_err():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = 'application/vnd.oci.image.config.v1'

    assert not o1 == o2


def test_ne_obj_ok():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = MediaType('application', 'vnd.oci.image.manifest.v1', 'json')

    assert o1 != o2


def test_ne_str_ok():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = 'application/vnd.oci.image.manifest.v1+json'

    assert o1 != o2


def test_ne_obj_err():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = MediaType('application', 'vnd.oci.image.manifest.v1', 'json')

    assert o1 != o2


def test_ne_str_err():
    o1 = MediaType('application', 'vnd.oci.image.config.v1', 'json')
    o2 = 'application/vnd.oci.image.manifest.v1'

    assert o1 != o2


def test_from_str_ok():
    o = MediaType.from_str('application/vnd.oci.image.config.v1+json')

    assert o.top == 'application'
    assert o.sub == 'vnd.oci.image.config.v1'
    assert o.structure == 'json'


def test_from_str_err():
    with pytest.raises(errors.PBValidationError) as err:
        MediaType.from_str('application/vnd.oci.image.config.v1')

    assert err.value.data.get('media_type') is not None
