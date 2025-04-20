from typing import Any, Dict, Protocol, Union
from dataclasses import dataclass


class RuntimePlugin(Protocol):
    """
    Runtime plugin protocol for implementations to define
    how to run instructions.
    """


class SpecPlugin(Protocol):
    """
    Spec plugin protocol for implementations to define
    how to parse build specifications (containerfile, rpm spec, file, etc).
    """ 


class StoragePlugin(Protocol):
    """
    Storage plugin protocol that defines methods for
    storing/reading OCI artifacts.
    """


PluginTypes = Union[RuntimePlugin, SpecPlugin, StoragePlugin]


@dataclass
class Plugin:
    """
    Data class to represent a plugin that can be used.

    It contains a name and an impl class.
    """
    name: str
    impl: PluginTypes

    def __str__(self) -> str:
        """
        Return the plugin name when str(instance) is called.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Return the full path of the plugin class implementation
        when repr(instance) is called. 
        """
        module_path = self.impl.__module__
        cls_name = self.impl.__class__.__name__

        return f'{module_path}.{cls_name}'
