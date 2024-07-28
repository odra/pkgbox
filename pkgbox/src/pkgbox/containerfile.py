"""
This module contains data types and utilities
to handle and parse Containerfile content.
"""
import pathlib
from typing import Any

from dockerfile_parse import DockerfileParser, util


class ContainerfileParser(DockerfileParser):
    """
    A class that inherits `dockerfile_parse.DockerfileParser`
    to handle for force cached content to be handled in
    a specific way.
    """
    def __init__(self, *args: Any, **kwargs Any) -> None:
        """
        Create a new object instance, forcing the
        parent class parser to used the cached content.
        """
        super().__init__(*args, **kwargs)
        self.cache_content = True

    @property
    def content(self) -> str:
        """
        Overwrites the parent method to return
        the cached content.
        """
        return self.cached_content

    @content.setter
    def content(self, content: str) -> None:
        """
        Overwrites the parent method to not do any file
        operations, so content can be loaded from a
        string.
        """
        self.cached_content = util.b2u(content)


def from_filepath(path: pathlib.Path) -> ContainerfileParser:
    """
    Return a parser object from a given path, where path
    should be the location of a Containerfile.
    """
    parser = ContainerfileParser()

    with open(path.resolve(), 'r') as f:
        parser.content = f.read()

    return parser
