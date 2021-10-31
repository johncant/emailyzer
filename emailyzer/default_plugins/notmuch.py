from emailyzer import base
import pluggy


hookimpl = pluggy.HookimplMarker("emailyzer")


class Plugin(base.Plugin):
    def name(self):
        return "Notmuch"

    def display_objects(self):
        return []


class DummyDisplayObject(base.AbstractDisplayObject):
    def name(self):
        return "foo"

    def display_objects(self):
        return []


class DummyCollection(base.EmailCollection):
    pass


class NotmuchDatabase(base.Mailbox):
    pass


class NotmuchDefaultDatabase(NotmuchDatabase):

    def display_objects(self):
        return [DummyDisplayObject()]

    def name(self):
        return "NotMuchMail default database"

    def meta_dataframe():
        raise NotImplementedError()


@hookimpl
def plugin_display_object():
    return Plugin()


@hookimpl
def email_collections():
    return [NotmuchDefaultDatabase()]
