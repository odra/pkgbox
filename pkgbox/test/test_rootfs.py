import os
import shutil
import pathlib
from unittest.mock import patch, mock_open

import pytest

from pkgbox import errors, rootfs
from pkgbox.rootfs import types



def test_from_path_ok(testdir, uid):
    path = f'{testdir}/{uid}'
    r = rootfs.from_path(path)

    assert r.path == pathlib.Path(path)
    assert r.digest == '5bf67f0f33f44ae801871e79bd489d26819b2dfbef06ba46cc2edde1630c27b3'
    for base_dir in types.BASE_DIRS:
        assert os.path.isdir(f'{path}/{base_dir}')

    shutil.rmtree(path)


def test_initialize_error(testdir, uid):
    path = f'{testdir}/{uid}'

    with patch('os.makedirs', mock_open()) as mock_file:
        mock_file.side_effect = OSError("File not found")

        with pytest.raises(errors.PBError):
            rootfs.from_path(path)

    assert not os.path.exists(str(path))
