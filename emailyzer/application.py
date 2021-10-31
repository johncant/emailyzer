from dataclasses import dataclass, field
from typing import List
from emailyzer.base import Plugin, AbstractDisplayObject, EmailCollection
from emailyzer.plugins import import_plugins, PluginManager


def test_objects():
    # Hardcoded defaults for testing

    return [NotmuchDefaultDatabase()]


@dataclass
class Plugins(AbstractDisplayObject):
    plugin_manager: PluginManager

    def name(self):
        return "Plugins"

    def display_objects(self):
        return self.plugin_manager.hook.plugin_display_object()


@dataclass
class EmailCollections(AbstractDisplayObject):
    email_collections: List[EmailCollection]

    def name(self):
        return "Email Collections"

    def display_objects(self):
        return self.email_collections


@dataclass
class Application(AbstractDisplayObject):
    email_collections: List[EmailCollection] = field(default_factory=lambda: [])
    plugin_manager: PluginManager = field(default_factory=import_plugins)

    def __post_init__(self):
        for collections in self.plugin_manager.hook.email_collections():
            for c in collections:
                self.email_collections.append(c)

    def name(self):
        return "Emailyzer"

    def display_objects(self):
        return [
            EmailCollections(self.email_collections),
            Plugins(plugin_manager=self.plugin_manager)
        ]

