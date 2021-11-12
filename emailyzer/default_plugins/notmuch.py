from emailyzer import base
import pluggy
from pandas import DataFrame
from typing import List
import notmuch
import pandas as pd
from tqdm import tqdm
from functools import lru_cache
from more_itertools import take


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
    def __init__(self, db: notmuch.Database):
        self.db = db

    def display_objects(self) -> List[base.AbstractDisplayObject]:
        return [DummyDisplayObject()]

    @lru_cache
    def meta_dataframe(self) -> DataFrame:
        all_messages = notmuch.Query(self.db, "").search_messages()

        df_meta = pd.DataFrame(take(1000, tqdm(
            {
                "Date": m.get_date(),
                "id": m.get_message_id(),
                "properties": list(m.get_properties()),
                "tags": list(m.get_tags()),
                "thread_id": m.get_thread_id(),
                **{
                    k: m.get_header(k) for k in ["From", "To", "Subject", "CC"]
                }
            }
            for m in all_messages
        )))

        df_meta['Date'] = pd.to_datetime(df_meta['Date'], unit='s')

        return df_meta


class NotmuchDefaultDatabase(NotmuchDatabase):
    def __init__(self) -> None:
        db = notmuch.Database()
        super().__init__(db)

    def name(self) -> str:
        return "NotMuchMail default database"


@hookimpl
def plugin_display_object() -> base.Plugin:
    return Plugin()


@hookimpl
def email_collections() -> List[base.EmailCollection]:
    return [NotmuchDefaultDatabase()]
