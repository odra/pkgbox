import pathlib

from . import mgr, types


def from_path(path: str) -> types.RootFS:
    """
    Initializes a new rootfs object from a filesystem path.
    """
    _path = pathlib.Path(path)

    return mgr.initialize(_path)
