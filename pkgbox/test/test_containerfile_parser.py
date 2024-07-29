import pathlib

import pytest

from pkgbox import errors
from pkgbox.containerfile import parser


def test_from_filepath_ok(fixdir):
    containerfile_path = f'{fixdir}/Containerfile.simple'
    with open(containerfile_path, 'r') as f:
        containerfile_content = f.read()

    path = pathlib.Path(containerfile_path)
    p = parser.from_path(path)

    assert p.content == containerfile_content


def test_from_filepath_error():
    path = pathlib.Path('/tmp/Containerfile.404')

    with pytest.raises(errors.PBError) as err:
        parser.from_path(path)

    assert err.value.message == 'No such file or directory'
    assert err.value.errno == 2


def test_parser_ok(fixdir):
    containerfile_path = f'{fixdir}/Containerfile.simple'
    with open(containerfile_path, 'r') as f:
        containerfile_content = f.read()

    c1 = parser.ContainerfileParser()
    c2 = parser.ContainerfileParser()
    c2.content = containerfile_content

    assert c1.content == ''
    assert c2.baseimage == 'quay.io/fedora/fedora:latest'
