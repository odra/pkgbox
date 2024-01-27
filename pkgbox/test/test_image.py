import os
import pathlib

from pkgbox import image


def test_from_str():
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name)

    assert img.registry == 'registry.fedoraproject.org'
    assert img.namespace == 'fedora'
    assert img.tag == '39'
    assert str(img) == name
    assert img == image.Image('registry.fedoraproject.org', 'fedora', '39')


def test_info():
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name)
    info = image.info(img)

    assert info.schema_version == 1
    assert info.name == 'fedora'
    assert info.tag == '39'
    assert info.architecture == 'amd64'
    assert len(info.layers) == 1
    assert len(info.history) == 1
    assert len(info.signatures) == 1


def test_fetch():
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name)
    info = image.info(img)
    dest = pathlib.Path('/tmp/pkgbox-test')

    image.fetch(img, info, dest)

    for layer in info.layers:
        assert os.path.exists(f'{dest}/{layer.digest}.tar.gz')
