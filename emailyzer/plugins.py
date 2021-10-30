import sys
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


# Untested
def import_plugins():

    for ep in entry_points(group='emailyzer.plugins'):
        plugin = ep.load()
        plugin()

