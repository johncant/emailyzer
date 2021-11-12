from emailyzer.base import (
    AbstractDisplayObject,
    EmailCollection,
    Plugin as BasePlugin
)
from emailyzer.gui_base import Opener, Closer
import pluggy
from tkinter import (
    X, Y, BOTH, BOTTOM, TOP, LEFT, RIGHT, VERTICAL, END
)
from tkinter import ttk, Menu
from typing import Optional, Tuple, Dict, Sequence, cast
import pandas as pd
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)


hookimpl = pluggy.HookimplMarker("emailyzer")


class Dashboard(EmailCollection):
    def __init__(self, email_collection: EmailCollection) -> None:
        self.impl = email_collection

    def name(self) -> str:
        return self.impl.name()

    def meta_dataframe(self) -> pd.DataFrame:
        return self.impl.meta_dataframe()

    def display_objects(self) -> Sequence[AbstractDisplayObject]:
        return []


class TopRecipientsTable(ttk.Frame):
    def __init__(self, container: ttk.Widget, ts: pd.Series):
        super().__init__(container)
        self.ts = ts
        self.build_view()
        self.populate_view()

    def build_view(self) -> None:
        self.scrollbar = ttk.Scrollbar(self)
        self.treeview = ttk.Treeview(
            self,
            columns=('sender', 'count'), show='headings',
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.treeview.yview)
        self.treeview.heading('sender', text='Sender')
        self.treeview.heading('count', text='Number of emails')
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.treeview.pack(side=LEFT, fill=BOTH, expand=1)

    def populate_view(self) -> None:
        for sender, count in self.ts.iteritems():
            self.treeview.insert('', END, values=(sender, count))


class DashboardView(ttk.Frame):

    @classmethod
    def build_with_options(
                cls,
                ec: Dashboard,
                container: ttk.Widget,
                closer: Closer,
            ) -> Optional[Tuple[ttk.Widget, Dict]]:

        dash = cls(
            ec,
            container,
            closer
        )
        return dash, {"text": ec.name()}

    def plot_time_series(self, master: ttk.Widget, df_meta: pd.DataFrame) -> ttk.Widget:

        ts = (
            df_meta.assign(date=df_meta['Date'].dt.date)
            .groupby(by='date')['id'].count()
        )

        print(ts)

        frame = ttk.Frame(master)
        # the figure that will contain the plot
        fig = Figure(figsize = (5, 5), dpi = 100)
  
        # adding the subplot
        ax = fig.add_subplot(111)

        print(ax)
      
        ts.plot(ax=ax)
      
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
        toolbar.update()
     
        toolbar.pack(fill=X, side=BOTTOM)
        canvas.get_tk_widget().pack(expand=True, fill=BOTH, side=TOP)

        return frame

    def plot_recipients(self, master: ttk.Widget, df_meta: pd.DataFrame) -> ttk.Widget:
        top_recipients = (
            df_meta
            .groupby(by=['From'])['id']
            .count()
            .sort_values(ascending=False)
        )
        return TopRecipientsTable(master, top_recipients)

    def __init__(
                self,
                ec: EmailCollection,
                container: ttk.Widget,
                _closer: Closer
            ) -> None:

        super().__init__(container)
        self.paned_window = ttk.PanedWindow(self, orient=VERTICAL)

        # Data
        df_meta = ec.meta_dataframe()

        ts_display = self.plot_time_series(self.paned_window, df_meta)
        recipients_display = self.plot_recipients(self.paned_window, df_meta)

        ts_display.pack(expand=1, fill=BOTH, side=TOP)
        recipients_display.pack(expand=1, fill=BOTH)

        self.paned_window.add(ts_display)
        self.paned_window.add(recipients_display)

        self.paned_window.pack(expand=1, fill=BOTH)
        self.pack(expand=1, fill=BOTH)


@hookimpl
def display_object_get_frame_opts(
            display_object: AbstractDisplayObject,
            container: ttk.Widget,
            closer: Closer,
        ) -> Optional[Tuple[ttk.Widget, Dict]]:

    if isinstance(display_object, EmailCollection):
        display_object = Dashboard(display_object)

    if isinstance(display_object, Dashboard):
        return DashboardView.build_with_options(
            display_object, container, closer
        )

    return None


class Plugin(BasePlugin):
    def name(self) -> str:
        return "Dashboard"

    def display_objects(self) -> Sequence[AbstractDisplayObject]:
        return []


@hookimpl
def plugin_display_object() -> Plugin:
    return Plugin()


@hookimpl
def populate_context_menu(menu: Menu, display_object: AbstractDisplayObject, opener: Opener) -> None:


    if isinstance(display_object, EmailCollection):
        emc = cast(EmailCollection, display_object)

        def open_dashboard() -> None:
            opener.open(Dashboard(emc))

        menu.add_command(label="Dashboard", command=open_dashboard)
