from abc import ABC, abstractmethod
from typing import Sequence, Dict
from pandas import DataFrame


class AbstractDisplayObject(ABC):
    @abstractmethod
    def display_objects(self) -> Sequence["AbstractDisplayObject"]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class Message(ABC):
    pass


class EmailCollection(AbstractDisplayObject):
    @abstractmethod
    def meta_dataframe(self) -> DataFrame:
        pass


class Mailbox(EmailCollection):
    pass


class Filter(AbstractDisplayObject):
    pass


class Calendar(AbstractDisplayObject):
    pass


class Plugin(AbstractDisplayObject):
    pass
