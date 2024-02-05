from typing import List, TextIO
from dataclasses import dataclass, field

from .instructions.base import BaseInstruction


@dataclass
class Containerfile:
    """
    Containerfile data class to parse
    and store Containerfile instructions.
    """
    data: str
    instructions: List[BaseInstruction] = field(init=False)

    def __post_init__(self) -> None:
        self.instructions = []


def load(f: TextIO) -> Containerfile:
    """
    Load and parse a Containerfile instance from a 
    file-like object.
    """
    return Containerfile('\n'.join(f.read().splitlines()))


def loads(data: str) -> Containerfile:
    """
    Load and parse a Containerfile instance from
    a string.
    """
    return Containerfile('\n'.join(data.splitlines()))
