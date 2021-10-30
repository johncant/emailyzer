from abc import ABC, ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass, field
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Tk
from typing import List


# Base

class AbstractDisplayObject(ABC):
    @abstractmethod
    def display_objects(self):
        pass

    @abstractmethod
    def name(self):
        pass


class Message(AbstractDisplayObject):
    pass


class EmailCollection(ABC):
    pass


class Mailbox(AbstractDisplayObject, EmailCollection):
    pass


class Filter(AbstractDisplayObject):
    pass


class Calendar(AbstractDisplayObject):
    pass


# Concrete


class DummyDisplayObject(AbstractDisplayObject):
    def name(self):
        return "foo"

    def display_objects(self):
        return []


class DummyCollection(EmailCollection):
    pass


class NotmuchDatabase(Mailbox):
    pass


class NotmuchDefaultDatabase(NotmuchDatabase):

    def display_objects(self):
        return [DummyDisplayObject()]

    def name(self):
        return "NotMuchMail default database"


def test_objects():
    # Hardcoded defaults for testing

    return [NotmuchDefaultDatabase()]


@dataclass
class Application:

    def name(self):
        "Emailyzer"

    def display_objects(self):
        return test_objects()


class ApplicationTreeView(ttk.Treeview):
    def __init__(self):
        super().__init__(columns=["name"], show='tree')
        self.heading("name", text="Objects")


class ApplicationTreeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.populate_view(self.model)

    def populate_view(self, model, parent=None):

        if parent == self.model:
            tree_parent_id = ""
        else:
            tree_parent_id = id(parent)

        if model != self.model:

            self.view.insert(
                tree_parent_id,
                tk.END,
                values=(model.name(),),
                iid=id(model),
                open=False,
            )

        for obj in model.display_objects():
            self.populate_view(obj, model)


class ApplicationWindow(Tk):

    def build_tree(self):
        self.tree = ApplicationTreeView()
        self.tree_controller = ApplicationTreeController(
            self.application,
            self.tree
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
