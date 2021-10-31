from abc import ABC, ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass, field
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Tk
from typing import List
from emailyzer.application import Application


class Opener(ABC):
    @abstractmethod
    def open(self, obj):
        pass


def default_display_object_frame(self, container):
    options = {
        "text": self.name()
    }
    frame = ttk.Frame(container)
    label = ttk.Label(frame, text=self.name())
    label.grid()
    

    return frame, options



# Views and controllers
class ApplicationTreeView(ttk.Treeview):
    def __init__(self):
        super().__init__(columns=["name"], show='tree')
        self.heading("name", text="Objects")


class ApplicationTreeController:
    def __init__(self, model, view, opener):
        self.model = model
        self.view = view
        self.opener = opener
        self.mapping = {}

        self.populate_view(self.model)

    def populate_view(self, model, parent=None):

        if parent == self.model:
            tree_parent_id = ""
        else:
            tree_parent_id = id(parent)

        if model != self.model:

            iid = str(id(model))
            self.mapping[iid] = model

            self.view.insert(
                tree_parent_id,
                tk.END,
                values=(model.name(),),
                iid=iid,
                open=False,
            )

        for obj in model.display_objects():
            self.populate_view(obj, model)

        self.view.bind('<<TreeviewSelect>>', self.item_selected)

    def item_selected(self, event):
        for iid in self.view.selection():
            obj = self.mapping[iid]

            self.opener.open(obj)


class ApplicationWindow(Tk):

    def build_tree(self):
        self.tree = ApplicationTreeView()
        self.tree_controller = ApplicationTreeController(
            self.application,
            self.tree,
            opener=self
        )
        self.tree.pack(expand=False, fill='both', side='left')

    def build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', side='left')

    def build_window(self):
        self.title("Emailyzer")
        self.attributes("-zoomed", True)
        self.build_tree()
        self.build_notebook()

    def display_object_frame_opts(self, obj):
        pm = self.application.plugin_manager
        frame_opts = pm.hook.display_object_get_frame_opts(
            display_object=obj,
            container=self.notebook,
        )

        if frame_opts is None:
            frame_opts = default_display_object_frame(
                obj,
                container=self.notebook
            )

        return frame_opts

    def open(self, display_obj, analyzer=None):
        frame, opts = self.display_object_frame_opts(
            display_obj
        )

        self.notebook.add(frame, **opts)

    def __init__(self, application : Application):
        super().__init__()
        self.application = application
        self.build_window()

    def run(self):
        pass


def main():
    application = Application()
    ApplicationWindow(application).mainloop()


if __name__ == '__main__':
    main()
