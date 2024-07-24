import pytest

from pkgbox import errors
from pkgbox.oci.v1 import Descriptor, Digest, MediaType


def test_init_basic_ok():
    o = Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10)
    
    assert str(o.media_type) == 'application/vnd.oci.image.layer.v1.tar'
    assert str(o.digest) == 'sha1:8843d7f92416211de9ebb963ff4ce28125932878'
    assert o.size == 10
    assert o.urls == []
    assert o.annotations == {}


def test_init_full_ok():
    o = Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10,
                   ['https://github.com/odra/pkgbox'],
                   {'org.pkgbox.artifact': 'true'})
    
    assert str(o.media_type) == 'application/vnd.oci.image.layer.v1.tar'
    assert str(o.digest) == 'sha1:8843d7f92416211de9ebb963ff4ce28125932878'
    assert o.size == 10
    assert o.urls == ['https://github.com/odra/pkgbox']
    assert o.annotations == {'org.pkgbox.artifact': 'true'}


def test_init_urls_err():
    with pytest.raises(errors.PBValidationError):
        Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10,
                   ['https:://github.com/odra/pkgbox'])


def test_init_annotations_key_err():
    with pytest.raises(errors.PBValidationError):
        Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10,
                   ['https://github.com/odra/pkgbox'],
                   {'http://org.pkgbox.artifact': 'true'})


def test_init_annotations_key_err():
    with pytest.raises(errors.PBValidationError):
        Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10,
                   ['https://github.com/odra/pkgbox'],
                   {'org.pkgbox.artifact': True})


def test_init_mediatype_err():
    with pytest.raises(errors.PBValidationError):
        Descriptor(MediaType.from_str('application/vnd.oci.image.layer.v1.tar+xml'),
                   Digest.from_str('sha1:8843d7f92416211de9ebb963ff4ce28125932878'),
                   10)
