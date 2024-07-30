import os
import shutil
import pathlib
from unittest.mock import patch, mock_open

import pytest

from pkgbox import errors
from pkgbox.rootfs import mgr, types


def test_initialize_ok(testdir, uid):
    path = pathlib.Path(f'{testdir}/{uid}')
    rootfs = mgr.initialize(path)

    assert rootfs.path == path
    assert rootfs.digest == '5bf67f0f33f44ae801871e79bd489d26819b2dfbef06ba46cc2edde1630c27b3'
    for base_dir in types.BASE_DIRS:
        assert os.path.isdir(f'{path}/{base_dir}')

    shutil.rmtree(str(path))


def test_initialize_error(testdir, uid):
    path = pathlib.Path(f'{testdir}/{uid}')

    with patch('os.makedirs', mock_open()) as mock_file:
        mock_file.side_effect = OSError("File not found")

        with pytest.raises(errors.PBError):
            mgr.initialize(path)

    assert not os.path.exists(str(path))


def test_diff_ok(testdir, uid):
    path1 = pathlib.Path(f'{testdir}/{uid}-1')
    path2 = pathlib.Path(f'{testdir}/{uid}-2')

    rootfs1 = mgr.initialize(path1)
    rootfs2 = mgr.initialize(path2)

    os.makedirs(f'{path2}/opt/newdir', exist_ok=True)
    rootfs2.data = mgr.read(rootfs2)

    diff = mgr.diff(rootfs1, rootfs2)

    assert diff['add'] == ['/opt/newdir']


def test_diff_empty_ok(testdir, uid):
    path1 = pathlib.Path(f'{testdir}/{uid}-1')
    path2 = pathlib.Path(f'{testdir}/{uid}-2')

    rootfs1 = mgr.initialize(path1)
    rootfs2 = mgr.initialize(path2)

    diff = mgr.diff(rootfs1, rootfs2)

    assert diff == {}
