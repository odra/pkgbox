import pathlib

from . import parser, types


def from_parser(p: parser.ContainerfileParser) -> types.Containerfile:
    """
    Create a new Containerfile dataclass object from a ContainerfileParser
    object.
    """
    return types.Containerfile(p.baseimage,
                               [types.Instruction(i['instruction'], i['value']) for i in p.structure],
                               labels=p.labels,
                               build_args=dict({}, **p.build_args, **p.args),
                               env_vars=p.envs)


def from_str(content: str) -> types.Containerfile:
    """
    Create a new Containerfile from a string.
    """
    p = parser.ContainerfileParser()
    p.content = content

    return from_parser(p)


def from_path(path: pathlib.Path) -> types.Containerfile:
    """
    Create a new Containerfile object from a file path.
    """

    p = parser.from_path(path)

    return from_parser(p)
