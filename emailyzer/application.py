from dataclasses import dataclass, field
from typing import List, Sequence
from emailyzer.base import Plugin, AbstractDisplayObject, EmailCollection
from emailyzer.plugins import import_plugins, PluginManager


@dataclass
class Plugins(AbstractDisplayObject):
    plugin_manager: PluginManager

    def name(self) -> str:
        return "Plugins"

    def display_objects(self) -> List[AbstractDisplayObject]:
        return self.plugin_manager.hook.plugin_display_object()


@dataclass
class EmailCollections(AbstractDisplayObject):
    email_collections: List[EmailCollection]

    def name(self) -> str:
        return "Email Collections"

    def display_objects(self) -> Sequence[AbstractDisplayObject]:
        return self.email_collections


@dataclass
class Application(AbstractDisplayObject):
    email_collections: List[EmailCollection] = field(default_factory=lambda: [])
    plugin_manager: PluginManager = field(default_factory=import_plugins)

    def __post_init__(self) -> None:
        for collections in self.plugin_manager.hook.email_collections():
            for c in collections:
                self.email_collections.append(c)

    def name(self) -> str:
        return "Emailyzer"

    def display_objects(self) -> Sequence[AbstractDisplayObject]:
        return [
            EmailCollections(self.email_collections),
            Plugins(plugin_manager=self.plugin_manager)
        ]

