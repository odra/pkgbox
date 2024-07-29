import pytest
import pathlib

from pkgbox.containerfile import parser
from pkgbox import containerfile, errors


def test_from_parser_ok(fixdir):
    path = pathlib.Path(f'{fixdir}/Containerfile.simple')
    p = parser.from_path(path)

    c = containerfile.from_parser(p)

    assert c.base_image == 'quay.io/fedora/fedora:latest'
    assert c.labels == {'foo': 'bar'}
    assert c.build_args == {'TARGETARCH': 'amd64'}
    assert c.env_vars == {'HOME': '/root'}
    assert len(c.instructions) == 6


def test_from_path_ok(fixdir):
    c = containerfile.from_path(pathlib.Path(f'{fixdir}/Containerfile.simple'))

    assert c.base_image == 'quay.io/fedora/fedora:latest'


def test_from_path_error():
    with pytest.raises(errors.PBError):
        containerfile.from_path(pathlib.Path('/Containerfile.404'))


def test_from_str_ok(fixdir):
    with open(f'{fixdir}/Containerfile.simple', 'r') as f:
        content = f.read()

    c = containerfile.from_str(content)

    assert c.base_image == 'quay.io/fedora/fedora:latest'


def test_from_str_error(fixdir):
    with open(f'{fixdir}/Containerfile.simple', 'r') as f:
        content = f.read().replace('FROM', 'FRO')
    
    with pytest.raises(errors.PBError):
        containerfile.from_str(content)
