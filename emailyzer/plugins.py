from pluggy import PluginManager
from emailyzer import hookspecs
from emailyzer import default_plugins


# Untested
def import_plugins() -> PluginManager:

    pm = PluginManager("emailyzer")

    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints("emailyzer")
    pm.register(default_plugins.notmuch)
    pm.register(default_plugins.dashboard)

    return pm
