import os
import pathlib
import hashlib
import tarfile
from typing import Any, Dict

import dictdiffer
import canonicaljson

from . import types
from pkgbox import errors


def initialize(path: pathlib.Path) -> types.RootFS:
    """
    Initializes a new rootfs object in a give path,
    updating the rootfs object properties accordingly.
    """
    rootfs = types.RootFS(path)

    try:
        os.makedirs(str(rootfs.path), exist_ok=True)
    except OSError as e:
        raise errors.PBError(e.strerror, e.errno)

    for base_dir in types.BASE_DIRS:
        os.makedirs(f'{path}/{base_dir}', exist_ok=True)

    rootfs.data = read(rootfs)
    rootfs.digest = as_digest(rootfs)

    return rootfs


def read(rootfs: types.RootFS) -> Dict[str, Any]:
    """
    Read a rootfs dir and return a dictionary with the mapped
    data.

    Directories are stored as dicts and files as a `pathlib.Path` object.
    """
    path = str(rootfs.path)
    data = {}

    for root, dirs, files in os.walk(path):
        current_directory = data

        for directory in os.path.relpath(root, path).split(os.path.sep):
            if directory == '.':
                continue
            full_path = f'{path}/{directory}'
            current_directory = current_directory.setdefault(directory, {})

        for filename in files:
            file_path = os.path.join(root, filename)
            current_directory[filename] = pathlib.Path(file_path)

    return data


def as_json(rootfs: types.RootFS, pretty: bool = False) -> str:
    """
    Return the canonical json representation of a rootfs dict structure.
    """
    # register a callback function to deal with pathlib.Path objects
    def cb(p: pathlib.Path) -> str:
        return str(p)
    canonicaljson.register_preserialisation_callback(pathlib.Path, cb)

    if pretty:
        return canonicaljson.encode_pretty_printed_json(rootfs.data).decode()

    return canonicaljson.encode_canonical_json(rootfs.data).decode()


def as_digest(rootfs: types.RootFS) -> str:
    """
    Return the sha256 digest representation of the rootfs' json data,
    file content is not considered.
    """
    json_data = as_json(rootfs)

    return hashlib.sha256(json_data.encode()).hexdigest()


def diff(rootfs1: types.RootFS, rootfs2: types.RootFS) -> Dict[str, Any]:
    """
    Diffs two rootfs objects and return a dict containig the difference.
    """
    output = {}

    for ctx, field, values in dictdiffer.diff(rootfs1.data, rootfs2.data):
        item = output.setdefault(ctx, [])

        for value in values:
            k, v = value
            item.append(_diff_parse(f'{field}/{k}', v))

    return output


def _diff_parse(field, values, p=''):
    if not p:
        p = f'{field}'
        if not p.startswith('/'):
            p = f'/{p}'

    if type(values) is not dict or len(values) == 0:
        return p

    for k, v in values.items():
        if isinstance(v, dict):
            return _diff_parse(v, p + f'/{k}')
        else:
            return f'{p}/{k}'


def archive(rootfs: types.RootFS, dest: pathlib.Path):
    with tarfile.open(str(dest), "w:gz") as tar:
        for root, dirs, files in os.walk(str(rootfs.path)):
            arcname = os.path.relpath(root, start=str(rootfs.path))
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.join(arcname, file))
