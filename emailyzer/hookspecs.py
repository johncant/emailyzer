import pluggy


hookspec = pluggy.HookspecMarker("emailyzer")


@hookspec(firstresult=True)
def display_object_get_frame_opts(display_object, container):
    pass


@hookspec
def plugin_display_object():
    pass


@hookspec
def email_collections():
    pass

