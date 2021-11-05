from emailyzer import base
from emailyzer.gui_base import Opener, Closer
import pluggy
from tkinter import ttk
from typing import Optional, Tuple, Dict, Sequence


hookimpl = pluggy.HookimplMarker("emailyzer")


@hookimpl
def display_object_get_frame_opts(
            display_object: base.AbstractDisplayObject,
            container: ttk.Widget,
            closer: Closer,
        ) -> Optional[Tuple[ttk.Widget, Dict]]:

    if isinstance(display_object, base.EmailCollection):
        print("TODO - implement dashboard")

    return None


class Plugin(base.Plugin):
    def name(self) -> str:
        return "Dashboard"

    def display_objects(self) -> Sequence[base.AbstractDisplayObject]:
        return []


@hookimpl
def plugin_display_object() -> base.Plugin:
    return Plugin()
