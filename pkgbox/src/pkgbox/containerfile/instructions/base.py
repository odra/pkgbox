from typing import Any

from pkgbox import image
from .meta import BaseInstruction


class From(BaseInstruction):
    """
    This class represents a Containerfile `FROM` instruction by
    implementing the required methods from
    `pkgbox.containerfile.instructions.meta.BaseInstruction`.

    It will pull an image's manifest together with its layers
    and apply it in the target rootfs directory which is passed
    to the __call__ method.
    """
    image: str

    def __init__(self, image: str) -> None:
        """
        Create a new object instance.

        Data is used as the container image name
        to be pulled.
        """
        self.image = image

    @classmethod
    def from_str(cls, data: str) -> 'From':
        """
        Create a new `From` object instance from a
        Containerfile `FROM...` instruction.
        """
        return cls(data.split(' ')[1])

    def as_containerfile(self) -> str:
        """
        Return the original containerfile insruction.
        """
        return f'FROM {self.image}'

    def __call__(self, **kwargs: Any) -> None:
        """
        Run the instruction.

        `**kwargs` should contain the following keys:
          - basedir: the path of the base directory to download the layer/manifest to
          - rootfs: the rootfs path to extract and apply the layer to
        """
        img = image.from_str(image_name)
        manifest = image.info(img)
        #TODO: error handling
        dest = pathlib.Path(kwargs['basedir'])

        image.fetch(img, manifest, dest)

        # TODO: apply layer into a rootfs dir
        rootfs = kwargs['rootfs']
