from emailyzer import base
import pluggy


hookimpl = pluggy.HookimplMarker("emailyzer")


@hookimpl
def display_object_get_frame_opts(display_object, container, closer):
    if isinstance(display_object, base.EmailCollection):
        print("TODO - implement dashboard")


class Plugin(base.Plugin):
    def name(self):
        return "Dashboard"

    def display_objects(self):
        return []


@hookimpl
def plugin_display_object():
    return Plugin()
