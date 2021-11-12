import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Tuple, cast

from emailyzer.application import Application
from emailyzer.base import AbstractDisplayObject
from emailyzer.gui_base import Closer, Opener


class DefaultDisplayObjectFrame(ttk.Frame):
    def __init__(
                self,
                display_object: AbstractDisplayObject,
                container: ttk.Widget, closer: Closer
            ) -> None:
        super().__init__(container)

        self.display_object = display_object
        self.closer = closer
        self.container = container

        self.build_ui()

    def build_ui(self) -> None:
        inner_frame = ttk.Frame(self)

        inner_frame.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        title = ttk.Label(inner_frame, text=self.display_object.name())
        title.config(font=('Helvatical bold', 20))
        title.pack(expand=False, anchor='n', pady=10)

        desc = ttk.Label(inner_frame, text="Not yet implemented")
        desc.pack(expand=False, anchor='s', pady=10)

        close = ttk.Button(inner_frame, text="Close", command=self.close)
        close.pack(expand=False, anchor='s', pady=10)

    def close(self) -> None:
        self.closer.close_child(self)
        self.destroy()


def default_display_object_frame(
            display_object: AbstractDisplayObject,
            container: ttk.Widget,
            closer: Closer
        ) -> Tuple[ttk.Widget, Dict]:

    options = {
        "text": display_object.name()
    }

    frame = DefaultDisplayObjectFrame(
        container=container, display_object=display_object, closer=closer
    )

    return frame, options


# Views and controllers
class ApplicationTreeView(ttk.Treeview):
    def __init__(self, master: ttk.Widget) -> None:
        super().__init__(master, columns=["name"], show='tree')
        self.heading("name", text="Objects")


class ApplicationTreeController:
    def __init__(
                self,
                model: AbstractDisplayObject,
                view: ttk.Treeview,
                opener: Opener) -> None:
        self.model = model
        self.view = view
        self.opener = opener
        self.mapping: Dict[str, AbstractDisplayObject] = {}

        self.populate_view(self.model)

    def populate_view(
                self,
                model: AbstractDisplayObject,
                parent: AbstractDisplayObject=None
            ) -> None:

        tree_parent_id: str = ""

        if parent != self.model:
            tree_parent_id = str(id(parent))

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
        self.view.bind("<Button-3>", self.context_menu)

    def context_menu(self, event: tk.Event) -> None:
        item = self.view.identify('item', event.x, event.y)
        obj = self.mapping[item]

        menu = tk.Menu(self.view, tearoff=0)

        # Poor abstraction leads to hacks
        app = cast(Application, self.model)

        app.plugin_manager.hook.populate_context_menu(
            menu=menu,
            display_object=obj,
            opener=self.opener
        )

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
        

    def item_selected(self, _event: tk.Event) -> None:
        for iid in self.view.selection():
            obj = self.mapping[iid]

            self.opener.open(obj)


class ApplicationWindow(tk.Tk, Opener, Closer):

    def build_tree(self, master) -> ttk.Widget:
        tree = ApplicationTreeView(master)
        ApplicationTreeController(
            self.application,
            tree,
            opener=self
        )
        tree.pack(expand=False, fill='both', side='left')
        return tree

    def build_notebook(self, master) -> None:
        notebook = ttk.Notebook(master)
        notebook.pack(expand=True, fill='both', side='right')
        return notebook

    def build_window(self) -> None:
        self.title("Emailyzer")
        self.attributes("-zoomed", True)
        panedwindow = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panedwindow.pack(expand=True, fill=tk.BOTH)
        tree = self.build_tree(panedwindow)
        notebook = self.build_notebook(panedwindow)
        panedwindow.add(tree)
        panedwindow.add(notebook)

        self.notebook = notebook

    def display_object_frame_opts(
                self,
                obj: AbstractDisplayObject
            )  -> Tuple[ttk.Widget, Dict]:
        pm = self.application.plugin_manager
        frame_opts = pm.hook.display_object_get_frame_opts(
            display_object=obj,
            container=self.notebook,
            closer=self,
        )

        if frame_opts is None:
            frame_opts = default_display_object_frame(
                display_object=obj,
                container=self.notebook,
                closer=self,
            )

        return frame_opts

    def open(
                self,
                obj: AbstractDisplayObject,
             ) -> None:

        iid = id(obj)

        if iid in self.notebook_tabs:
            tab_id = self.notebook_tabs[iid]
            self.notebook.select(tab_id)
        else:
            frame, opts = self.display_object_frame_opts(obj)

            self.notebook.add(frame, **opts)
            self.notebook.select(frame)
            self.notebook_tabs[id(obj)] = frame

    def close_child(self, child: ttk.Widget) -> None:
        iids = [k for k, v in self.notebook_tabs.items() if v == child]
        self.notebook.forget(child)

        for iid in iids:
            del self.notebook_tabs[iid]

    def __init__(self, application : Application) -> None:
        super().__init__()
        self.application = application
        self.build_window()
        self.notebook_tabs: Dict[int, ttk.Widget] = {}

    def run(self) -> None:
        pass


def main() -> None:
    application = Application()
    ApplicationWindow(application).mainloop()


if __name__ == '__main__':
    main()
