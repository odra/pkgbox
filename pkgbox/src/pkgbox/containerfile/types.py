import re
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from pkgbox import errors


EPHEMERAL_INSTRUCTIONS: Dict[str, bool] = {
    "ARG": True,
    "ENV": True,
    "LABEL": True
}


@dataclass
class Instruction:
    """
    Dataclass that represents a Containerfile
    instruction.
    """
    name: str
    value: str
    digest: str = field(init=False)

    def __post_init__(self) -> None:
        """
        Post initialization method that sets the digest object property based on 
        the values of `name` and `value`.
        """

        raw = f'{self.name}{self.value}'.encode()
        hashed = hashlib.sha256(raw).hexdigest()

        self.digest = f'sha256:{hashed}'

    def __str__(self) -> str:
        """
        Return the "original" instruction string used in the Containerfile.

        It is using quotes because if only adds one space between the instruction
        name and its value which may not always be the case in the original
        Containerfile.
        """
        return f'{self.name} {self.value}'

    def is_ephemeral(self) -> bool:
        """
        This method identifies the instruction generates
        rootfs changes when executed or not.

        Instructions such as "ARG" or "ENV" are examples of
        instructions that do not generate rootfs changes.
        """
        return EPHEMERAL_INSTRUCTIONS.get(self.name) is not None


@dataclass
class Containerfile:
    """
    Containerfile dataclass to store parsed
    Containerfile data.
    """
    base_image: str
    instructions: List[Instruction]
    labels: Dict[str, str] = field(default_factory=dict)
    build_args: Dict[str, Optional[str]] = field(default_factory=dict)
    env_vars: Dict[str, Optional[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Post initialization special method
        to validate the object's properties.
        """
        if self.base_image is None:
            raise errors.PBValidationError(base_image='failed to read "FROM" instruction')

        image_pattern = r'^([a-zA-Z0-9\.\_\-]+)/(([a-zA-Z0-9\.\_\-]+)/)?([a-zA-Z0-9\.\_\-]+):([a-zA-Z0-9\_\-]+)'
        if re.match(image_pattern, self.base_image) is None:
            raise errors.PBValidationError(base_image=f'invalid base_image format: {self.base_image}')

        for build_arg in self.build_args.keys():
            if len(build_arg) < 1:
                raise errors.PBValidationError(**{f'build_args["{build_arg}"]': 'key name too short'})

        for label in self.labels.keys():
            if len(label) < 1:
                raise errors.PBValidationError(**{f'labels["{label}"]': 'key name too short'})

        for env_var in self.env_vars.keys():
            if len(env_var) < 1:
                raise errors.PBValidationError(**{f'env_vars["{env_var}"]': 'key name too short'})
