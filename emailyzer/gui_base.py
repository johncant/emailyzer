from tkinter import ttk
from abc import ABC, abstractmethod
from emailyzer.base import AbstractDisplayObject


class Opener(ABC):
    @abstractmethod
    def open(self, obj : AbstractDisplayObject) -> None:
        pass


class Closer(ABC):
    @abstractmethod
    def close_child(self, child: ttk.Widget) -> None:
        pass
