from pkgbox.oci import common


def test_is_valid_rdn_custom_ok():
    rdn = 'org.pkgbox.artifact'

    assert common.is_valid_rdn(rdn) is True


def test_is_valid_rdn_oci_ok():
    rdn = 'org.opencontainers.image.version'

    assert common.is_valid_rdn(rdn) is True


def test_is_valid_error():
    rdn = 'org-us.pkgbox.artifact'

    assert common.is_valid_rdn(rdn) is False


def test_is_reserved_rdn_ok():
    rdn = 'org.opencontainers.image.version'

    assert common.is_reserved_rdn(rdn) is True


def test_is_reserved_rdn_noval_ok():
    rdn = 'org.opencontainers.image'

    assert common.is_reserved_rdn(rdn, validate=False) is True


def test_is_reserved_rdn_error():
    rdn = 'org.opencontainers.image.foobar'

    assert common.is_reserved_rdn(rdn) is False


def test_is_reserved_rdn_noval_error():
    rdn = 'org.opencontainer.image.foobar'

    assert common.is_reserved_rdn(rdn, validate=False) is False
