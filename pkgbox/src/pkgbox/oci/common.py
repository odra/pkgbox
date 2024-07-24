"""
This module contains common types and functions
for OCI image spec data validation.
"""
import re
from typing import Dict


OCI_RDNS_PREFIX: str = 'org.opencontainers'
OCI_RDNS_KEYS: Dict[str, str] = {
    'created': True,
    'url': True,
    'source': True,
    'version': True,
    'revision': True,
    'vendor': True,
    'title': True,
    'description': True,
    'documentation': True,
    'authors': True,
    'licenses': True,
    'ref.name': True
}


def is_valid_rdn(rdn: str) -> bool:
    """
    `RDN` stands for "Reverse Domain Name".

    Validates if `rdn` is a valid
    Reverse domain name (rdns for short).

    This function validates the provided `rdn` is using the
    expected string format and nothing else.
    """
    pattern = r'(^[a-zA-Z]{2,})\.([a-z-A-Z0-9\-\_\.]+)$'
    
    return re.match(pattern, rdn) is not None


def is_reserved_rdn(rdn: str, validate: bool = True) -> bool:
    """
    `RDN` stands for "Reverse Domain Name".

    Identify if `rdn` is an OCI reserved one.

    It will check if the whole domain name is a valid OCI one if
    `validate` is True; It will just check if the provided
    `rdn` is prefixed as `org.opencontainers.image` otherwise.

    See: https://github.com/opencontainers/image-spec/blob/v1.0.0/annotations.md#rules
    """
    if not rdn.startswith(OCI_RDNS_PREFIX):
        return False

    if not validate:
        return True

    suffix = rdn.replace(f'{OCI_RDNS_PREFIX}.image.', '')

    return OCI_RDNS_KEYS.get(suffix) is not None
