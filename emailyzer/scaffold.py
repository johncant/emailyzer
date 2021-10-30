from emailyzer.base import (
    AbstractDisplayObject,
    EmailCollection,
    Mailbox
)
# Testing

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

    def meta_dataframe():
        raise NotImplementedError()
