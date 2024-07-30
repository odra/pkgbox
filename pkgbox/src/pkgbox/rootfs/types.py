import pathlib
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from pkgbox import errors


BASE_DIRS: List[str] = [
    'bin',
    'boot',
    'dev',
    'etc',
    'home',
    'lib',
    'lib64',
    'media',
    'mnt',
    'opt',
    'proc',
    'root',
    'run',
    'sbin',
    'srv',
    'sys',
    'tmp',
    'usr',
    'var'
]


@dataclass
class RootFS:
    """
    Dataclass that representes a rootfs structure.
    """
    path: pathlib.Path
    data: Dict[str, Any] = field(default_factory=dict)
    digest: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        """
        Check if two RootFS objects are the same by
        comparing its digest property.
        """
        if not isinstance(other, RootFS):
            raise errors.PBError('Comparing RootFS with a non RootFS object')

        return self.digest == other.digest

    def __ne__(self, other: object) -> bool:
        """
        Check if two RootFS objects are not the same by
        comparing its digest property.
        """
        if not isinstance(other, RootFS):
            raise errors.PBError('Comparing RootFS with a non RootFS object')

        return self.digest != other.digest
