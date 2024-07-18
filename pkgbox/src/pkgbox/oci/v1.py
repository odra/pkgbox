"""
This module contains dataclasses definitons for the
OCI V1 Image Specification.
"""
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from pkgbox import errors


@dataclass
class MediaType:
    """
    Upstream URL: https://github.com/opencontainers/image-spec/blob/v1.0/media-types.md

    Represent an OCI MeidaType and follows rfc6838.
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
        p = '(^[a-zA-Z0-9]+)\/([a-zA-Z0-9\.]+)\+?([a-zA-Z0-9]+)?'
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
        return cls(*data.split(':'))



@dataclass
class Descriptor:
    """
    https://github.com/opencontainers/image-spec/blob/v1.0/descriptor.md#properties

    Represents an OCI descriptor.
    """
    media_type: MediaType
    digest: Digest
    size: int
    urls: Optional[List[str]]
    annotations: Optional[Dict[str, str]]

    def __post_init__(self) -> None:
        """
        Post initialization method, used for field validaton.
        """
        allowed_media_types = {
            'application/vnd.oci.descriptor.v1+json': True,
            'application/vnd.oci.layout.header.v1+json': True,
            'application/vnd.oci.image.index.v1+json': True,
            'application/vnd.oci.image.manifest.v1+json': True,
            'application/vnd.oci.image.config.v1+json': True,
            'application/vnd.oci.image.layer.v1.tar': True,
            'application/vnd.oci.image.layer.v1.tar+gzip': True,
            'application/vnd.oci.image.layer.nondistributable.v1.tar': True,
            'application/vnd.oci.image.layer.nondistributable.v1.tar+gzip': True
        }

        if not allowed_media_types.get(str(media_type)):
            raise errors.PBValidationError()


@dataclass
class Manifest:
    """
    A dataclass that represents an OCI Image Manifest.
    """
    schema_version: str = field(init=False)
    name: str
    tag: str
    architecture: str
    layers: List[Descriptor]
    history: List[str]
    signatures: Any
    digest: Digest

    def __post_init__(self) -> None:
        """
        Post initialization setup, invoked after the class is instantiated.
        """
        self.schema_version = 1
