"""
This module contains dataclasses definitons for the
OCI V1 Image Specification.
"""
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import common
from pkgbox import errors


LAYER_MEDIA_TYPES: Dict[str, bool] = {
    'application/vnd.oci.image.layer.v1.tar': True,
    'application/vnd.oci.image.layer.v1.tar+gzip': True,
    'application/vnd.oci.image.layer.nondistributable.v1.tar': True,
    'application/vnd.oci.image.layer.nondistributable.v1.tar+gzip': True    
}

CONFIG_MEDIA_TYPES: Dict[str, bool] = {
    'application/vnd.oci.descriptor.v1+json': True,
    'application/vnd.oci.layout.header.v1+json': True,
    'application/vnd.oci.image.index.v1+json': True,
    'application/vnd.oci.image.manifest.v1+json': True,
    'application/vnd.oci.image.config.v1+json': True
}

MEDIA_TYPES: Dict[str, bool] = dict(**LAYER_MEDIA_TYPES, **CONFIG_MEDIA_TYPES)


def validate_annotations(annotations: Dict[str, str]) -> None:
    """
    Validate annotations from OCI resources.

    Raises `pkgbox.errors.PBValidationError` in case it fails its
    validation process.
    """
    for k, v in annotations.items():
        # fail if key is not a valid reverse domain name
        if not common.is_valid_rdn(k):
            raise errors.PBValidationError(**{f'annotations["{k}"]': 'invalid RDN format'})
        # fail using an oci  reverse domain name with an improper key
        if common.is_reserved_rdn(k, validate=False) and not common.is_reserved_rdn(k):
            raise errors.PBValidationError(**{f'annotations["{k}"]': 'invalid OCI reserved RDN key'})
        # fail if annotation value is not a string
        if not isinstance(v, str):
            raise errors.PBValidationError(**{f'annotations["{k}"]': 'value is not a string'})


@dataclass
class MediaType:
    """
    Upstream URL: https://github.com/opencontainers/image-spec/blob/v1.0/media-types.md

    Represent an OCI MediaType and follows rfc6838.
    """
    top: str
    sub: str
    structure: Optional[str]

    def __str__(self) -> str:
        """
        Return the original media type formated string according to RFC6838.
        """
        if self.structure is None:
            return f'{self.top}/{self.sub}'
        
        return f'{self.top}/{self.sub}+{self.structure}' 

    def __eq__(self, other: object) -> bool:
        """
        Compare if the current object (self) is equal to `other`.

        It will compare properties if `other` is a MediaType instance,
        compare str(self) it `other` is a string and return false
        otherwise.
        """
        if isinstance(other, MediaType):
            return self.top == other.top and self.sub == other.sub and self.structure == other.structure

        if isinstance(other, str):
            return str(self) == other

        return False

    def __ne__(self, other: object) -> bool:
        """
        Compare if `self` is not equal to `other`.

        See `__eq__` documentation for details.
        """
        return not self == other

    @classmethod
    def from_str(cls, data: str) -> 'MediaType':
        """
        Create a new object from a RFC6838 media type string.
        """
        if not MEDIA_TYPES.get(data):
            raise errors.PBValidationError(media_type=f'unsupported media type: {data}')

        p = r'(^[a-zA-Z0-9]+)\/([a-zA-Z0-9\.]+)\+?([a-zA-Z0-9]+)?'
        m = re.match(p, data)

        return cls(*m.groups())


@dataclass
class Digest:
    """
    Upstream URL: https://github.com/opencontainers/image-spec/blob/v1.0/descriptor.md#digests

    Represents a descriptor digest, storing the hash algorithm type and a digest value.
    """
    alg: str
    value: str

    def __str__(self) -> str:
        """
        Return the "original" value fo the digest as `{self.alg}:{self.value}
        """
        return f'{self.alg}:{self.value}'
 
    def __eq__(self, other: object) -> bool:
        """
        Compares two digests, it can also be used to compare a digest value string
        directly.

        If using a string it should be formated as `$ALG:$DATA`.

        Return false if any other type is used as `other`.
        """
        if isinstance(other, Digest):
            return self.alg == other.alg and self.value == other.value

        if isinstance(other, str):
            return str(self) == other

        return False

    def __ne__(self, other: object) -> bool:
        """
        Compares if the object is not equal to `other`.

        See `__eq__` docs.
        """
        return not self == other

    @classmethod
    def from_str(cls, data: str) -> 'Digest':
        """
        Create a new Digest class from an OCI digest string expecting the following formats:

        - $HASH_ALGORITHM:$CONTENT_DIGEST
        """
        parts = data.split(':')

        if len(parts) != 2:
            raise errors.PBValidationError(digest='failed to parse digest string')

        return cls(*parts)


@dataclass
class Descriptor:
    """
    https://github.com/opencontainers/image-spec/blob/v1.0/descriptor.md#properties

    Represents an OCI descriptor.
    """
    media_type: MediaType
    digest: Digest
    size: int
    urls: List[str] = field(default_factory=lambda: list())
    annotations: Dict[str, str] = field(default_factory=lambda: dict())

    def __post_init__(self) -> None:
        """
        Post initialization method, used for field validaton.
        """ 
        if not MEDIA_TYPES.get(str(self.media_type)):
            raise errors.PBValidationError(**{'digest.media_type': f'unsupported media type: {self.media_type}'})

        url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for url in self.urls:
            if re.match(url_pattern, url) is None:
                raise errors.PBValidationError(**{'url': f'invalid url format: {url}'})
        
        validate_annotations(self.annotations)
        
@dataclass
class Manifest:
    """
    Upstream documentation: https://github.com/opencontainers/image-spec/blob/v1.0/manifest.md

    A dataclass that represents an OCI Image Manifest.
    """
    schema_version: int
    config: Descriptor
    layers: List[Descriptor]
    annotations: Optional[Dict[str, str]] = field(default_factory=lambda: dict())
    
    def __post_init__(self) -> None:
        """
        Post initialization setup, invoked after the class is instantiated.

        Used for field validation.
        """
        if self.schema_version != 2:
            raise errors.PBValidationError(**{'schema_version': f'unsupported value: {self.schema_version}'})

        if str(self.config.media_type) != 'application/vnd.oci.image.config.v1+json':
            raise errors.PBValidationError(**{'config.media_type': f'unsupported config media type: {self.config.media_type}'})

        for idx, layer in enumerate(self.layers):
            if not LAYER_MEDIA_TYPES.get(str(layer.media_type)):
                raise errors.PBValidationError(**{f'layers[{idx}].media_type': f'unsupported layer media type: {layer.media_type}'})

        validate_annotations(self.annotations)
