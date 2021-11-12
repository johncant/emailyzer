from emailyzer.base import AbstractDisplayObject, Plugin, EmailCollection
from emailyzer.gui_base import Closer, Opener
import pluggy
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Dict, Sequence

#pylint: disable=unused-argument

hookspec = pluggy.HookspecMarker("emailyzer")


@hookspec(firstresult=True)
def display_object_get_frame_opts(
            display_object: AbstractDisplayObject,
            container: ttk.Widget,
            closer: Closer,
        ) -> Optional[Tuple[ttk.Widget, Dict]]:
    pass


@hookspec
def plugin_display_object() -> Plugin:
    pass


@hookspec
def email_collections() -> Sequence[EmailCollection]:
    pass


@hookspec
def populate_context_menu(menu: tk.Menu, display_object: AbstractDisplayObject, opener: Opener) -> None:
    pass
