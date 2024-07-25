import pytest

from pkgbox import errors
from pkgbox.oci.v1 import Descriptor, Digest, Manifest, MediaType


@pytest.fixture
def ociv1_config():
    return Descriptor(
            MediaType.from_str('application/vnd.oci.image.config.v1+json'),
            Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
            10
        )


@pytest.fixture
def ociv1_layers():
    return [
        Descriptor(
            MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
            Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
            10
        )
    ]


@pytest.fixture
def ociv1_annotations():
    return {
        'org.pkgbox.artifact': 'true',
        'org.opencontainers.image.version': 'latest'
    }


def test_manifest_ok(ociv1_config, ociv1_layers):
    o = Manifest(
            2,
            ociv1_config,
            ociv1_layers
        )

    assert o.schema_version == 2
    assert o.config == ociv1_config
    assert o.layers == ociv1_layers
    assert o.annotations == {}


def test_manifest_schema_version_error(ociv1_config, ociv1_layers):
    with pytest.raises(errors.PBValidationError) as err:
        Manifest(1, ociv1_config, ociv1_layers)

    assert err.value.data.get('schema_version') is not None


def test_manifest_media_type_error(ociv1_config, ociv1_layers):
    ociv1_config.media_type = 'application/vnd.oci.image.layer.v1.tar'
    
    with pytest.raises(errors.PBValidationError) as err:
        Manifest(2, ociv1_config, ociv1_layers)

    assert err.value.data.get('config.media_type') is not None


def test_manifest_layers_error(ociv1_config, ociv1_layers):
    ociv1_layers[0].media_type = 'application/vnd.oci.image.config.v1+json'
    
    with pytest.raises(errors.PBValidationError) as err:
        Manifest(2, ociv1_config, ociv1_layers)

    assert err.value.data.get('layers[0].media_type') is not None


def test_manifest_annotations_ok(ociv1_config, ociv1_layers, ociv1_annotations):
    o = Manifest(
            2,
            ociv1_config,
            ociv1_layers,
            ociv1_annotations
        )

    assert o.schema_version == 2
    assert o.config == ociv1_config
    assert o.layers == ociv1_layers
    assert o.annotations == ociv1_annotations


def test_manifest_annotations_format_error(ociv1_config, ociv1_layers, ociv1_annotations):
    ociv1_annotations['org-pkgbox.artifact'] = 'true'

    with pytest.raises(errors.PBValidationError) as err:
        Manifest(
                2,
                ociv1_config,
                ociv1_layers,
                ociv1_annotations
        )

    assert err.value.data.get('annotations["org-pkgbox.artifact"]') is not None


def test_manifest_annotations_oci_error(ociv1_config, ociv1_layers, ociv1_annotations):
    ociv1_annotations['org.opencontainers.image.foo'] = 'bar'

    with pytest.raises(errors.PBValidationError) as err:
        Manifest(
                2,
                ociv1_config,
                ociv1_layers,
                ociv1_annotations
        )

    assert err.value.data.get('annotations["org.opencontainers.image.foo"]') is not None


def test_manifest_annotations_value_error(ociv1_config, ociv1_layers, ociv1_annotations):
    ociv1_annotations['org.pkgbox.artifact'] = True

    with pytest.raises(errors.PBValidationError) as err:
        Manifest(
                2,
                ociv1_config,
                ociv1_layers,
                ociv1_annotations
        )

    assert err.value.data.get('annotations["org.pkgbox.artifact"]') is not None
