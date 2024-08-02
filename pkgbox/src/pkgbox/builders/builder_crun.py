import os
import path
import uuid
import shutil
from types import Any, Dict


class CrunBuilder:
    """
    Builder that uses the "crun" CLI to run builds.

    Methods used to build a packaged use a "build_" prefix in its name.
    """
    build_dir: path.Pathlib
    crun_cfg: path.Pathlib

    def __init__(self, build_dir: path.Pathlib, crun_cfg: path.PathLib) -> None:
        """
        Create a new  builder instance.
        """
        self.build_dir = build_dir
        self.crun_cfg = crun_cfg

    def build_prepare(self, build_id: str = None) -> None:
        """
        Prepare a build to run.

        A `build_id` can be passed to be used as the build's
        unique name. It will use a uuid4 string if none is provided.
        """
        if build_id is None:
            build_id = str(uuid.uuid4())
        
        os.makedirs(f'{self.build_dir}/builds/{build_id}', exist_ok=True)
        shutil.copy(self.crun_cfg, f'{self.build_dir}/builds/{build_id}/config.json')
        os.makedirs(f'{self.build_dir}/builds/{build_id}/rootfs', exist_ok=True)

    def build_run(self) -> None:
        """
        """
        pass

    def build_post(self) -> None:
        """
        """
        pass

    def info(self, build_id: str):
        pass
