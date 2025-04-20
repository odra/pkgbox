from typing import Dict

from .types import Plugin, PluginTypes


class PluginMgr:
    """
    Plugin manager class, responsible for loading plugins
    when running pkgbox.

    The internal plugin dict splits each plugin by context/category:
    - runtime
    - spec
    - storage
    """
    plugins: Dict[str, Dict[str, PluginTypes]]
    
    def __init__(self) -> None:
        """
        Initializes a new manager, with an empty plugin dict.
        """
        self.plugins = {
            'runtime': {},
            'spec': {},
            'storage': {}
        }

    def validate(self, plugin: Plugin) -> None:
        """
        Validate a plugin.

        This is used by the `load` method before loading a 
        plugin into the manager.

        Raise an `PBError` exception in case the validation reports an error.
        """

    def load(self, ctx: str, plugin: Plugin) -> None:
        """
        Add and load a plugin implementation to the Plugin Manager.
        """

    def is_loaded(self, ctx: str, name: str) -> bool:
        """
        Check if a plugin is loaded in the Plugin Manager.
        """
        return name in self.plugins.get(ctx, {})
