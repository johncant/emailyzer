from emailyzer import base
import pluggy
from pandas import DataFrame
from typing import List


hookimpl = pluggy.HookimplMarker("emailyzer")


class Plugin(base.Plugin):
    def name(self) -> str:
        return "Notmuch"

    def display_objects(self) -> List[base.AbstractDisplayObject]:
        return []


class DummyDisplayObject(base.AbstractDisplayObject):
    def name(self) -> str:
        return "foo"

    def display_objects(self) -> List[base.AbstractDisplayObject]:
        return []


class DummyCollection(base.EmailCollection):
    pass


class NotmuchDatabase(base.Mailbox):
    pass


class NotmuchDefaultDatabase(NotmuchDatabase):

    def display_objects(self) -> List[base.AbstractDisplayObject]:
        return [DummyDisplayObject()]

    def name(self) -> str:
        return "NotMuchMail default database"

    def meta_dataframe(self) -> DataFrame:
        raise NotImplementedError()


@hookimpl
def plugin_display_object() -> base.Plugin:
    return Plugin()


@hookimpl
def email_collections() -> List[base.EmailCollection]:
    return [NotmuchDefaultDatabase()]
