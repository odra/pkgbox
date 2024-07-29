import hashlib

import pytest

from pkgbox import errors
from pkgbox.containerfile import types


def test_instruction_ok():
    inst = types.Instruction('RUN', 'echo hello')
    hashed = hashlib.sha256(b'RUNecho hello').hexdigest()

    assert inst.name == 'RUN'
    assert inst.value == 'echo hello'
    assert inst.digest == 'sha256:' + hashed
    assert str(inst) == 'RUN echo hello'


def test_instruction_ephemeral_ok():
    inst = types.Instruction('ENV', 'echo hello')

    assert inst.is_ephemeral() is True


def test_instruction_ephemeral_error():
    inst = types.Instruction('RUN', 'echo hello')

    assert inst.is_ephemeral() is False


def test_containerfile_minimal_ok():
    c = types.Containerfile('localhost/fedora:40', [])

    assert c.base_image == 'localhost/fedora:40'
    assert c.instructions == []
    assert c.labels == {}
    assert c.build_args == {}
    assert c.env_vars == {}


def test_containerfile_full_ok():
    c = types.Containerfile('localhost/fedora:40',
                            [],
                            labels={'foo': 'bar'},
                            build_args={'arch': 'amd64'},
                            env_vars={'HOME': '/root'})

    assert c.base_image == 'localhost/fedora:40'
    assert c.instructions == []
    assert c.labels == {'foo': 'bar'}
    assert c.build_args == {'arch': 'amd64'}
    assert c.env_vars == {'HOME': '/root'}


def test_containerfile_image_error():
    with pytest.raises(errors.PBValidationError) as err:
        types.Containerfile('fedora:40', [])

    assert err.value.data.get('base_image') is not None


def test_containerfile_build_args_error():
    with pytest.raises(errors.PBValidationError) as err:
        types.Containerfile('localhost/fedora:40', [],
                            build_args={'': 'amd64'})

    assert err.value.data.get('build_args[""]') is not None


def test_containerfile_labels_error():
    with pytest.raises(errors.PBValidationError) as err:
        types.Containerfile('localhost/fedora:40', [],
                            labels={'': 'bar'})

    assert err.value.data.get('labels[""]') is not None


def test_containerfile_env_vars_error():
    with pytest.raises(errors.PBValidationError) as err:
        types.Containerfile('localhost/fedora:40', [],
                            env_vars={'': '/home'})

    assert err.value.data.get('env_vars[""]') is not None
