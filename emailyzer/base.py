from abc import ABC, abstractmethod


class AbstractDisplayObject(ABC):
    @abstractmethod
    def display_objects(self):
        pass

    @abstractmethod
    def name(self):
        pass


class Message(ABC):
    pass


class EmailCollection(ABC):
    @abstractmethod
    def meta_dataframe(self):
        pass


class Mailbox(AbstractDisplayObject, EmailCollection):
    pass


class Filter(AbstractDisplayObject):
    pass


class Calendar(AbstractDisplayObject):
    pass


class Plugin(AbstractDisplayObject):
    pass
