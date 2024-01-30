from dataclasses import dataclass


@dataclass
class Containerfile:
    data: str


def load(f) -> Containerfile:
    return Containerfile('\n'.join(f.read().splitlines()))


def loads(data: str) -> Containerfile:
    return Containerfile('\n'.join(data.splitlines()))
