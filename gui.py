"""
Cricket Performance Analysis System - Tkinter GUI
=================================================

Run it from the project folder:

    python gui.py

Every button on the main menu opens a window that calls the same functions
from the src/ folder that main.py uses (get_player_runs, compare_players,
get_team_wins, get_top_run_scorers, ...).
"""

import numbers
import os
import sys
import tkinter as tk
import tkinter.font as tkfont
import traceback
import warnings
from tkinter import messagebox, ttk

import pandas as pd

import matplotlib

# Charts are shown INSIDE Tkinter windows (see open_chart), so matplotlib must
# not open windows of its own. "Agg" is matplotlib's no-window backend.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from src.data_cleaning import clean_matches, clean_deliveries

from src.player_analysis import (
    get_player_runs,
    get_player_matches,
    get_player_average,
    get_player_strike_rate,
    get_player_fours,
    get_player_sixes,
    get_player_highest_score,
    get_player_fifties,
    get_player_hundreds,
)

from src.player_comparison import compare_players

from src.team_analysis import (
    get_team_matches,
    get_team_wins,
    get_team_losses,
    get_team_win_percentage,
    get_team_runs,
    get_team_wickets,
)

from src.match_analysis import (
    get_match_details,
    get_match_winner,
    get_match_venue,
    get_match_scorecard,
    get_best_batsman,
    get_best_bowler,
)

from src.venue_analysis import (
    get_venue_matches,
    get_venue_wins,
    get_venue_runs,
    get_venue_average_runs,
    get_most_common_team,
)

from src.performance_trends import (
    get_team_season_performance,
    get_player_season_runs,
    get_team_season_runs,
)

from src.top_performers import (
    get_top_run_scorers,
    get_top_wicket_takers,
    get_most_sixes,
    get_most_fours,
)

from src.visualizations import (
    show_top_run_scorers,
    show_top_wicket_takers,
    show_most_sixes,
    show_most_fours,
    show_team_runs,
)

from src.dataset_summary import get_dataset_summary


# ===================================
# SETTINGS
# ===================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

TITLE_FONT = ("Arial", 22, "bold")
HEADING_FONT = ("Arial", 12, "bold")
LABEL_FONT = ("Arial", 10, "bold")


# ===================================
# MAIN WINDOW + DATASET
# ===================================

root = tk.Tk()
root.withdraw()  # stay hidden until the data is loaded


def show_unexpected_error(exc_type, exc_value, exc_traceback):
    """Show any error from a button click in a message box (instead of only the console)."""
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    messagebox.showerror("Something went wrong", f"{exc_type.__name__}: {exc_value}")


root.report_callback_exception = show_unexpected_error

try:
    matches = clean_matches(pd.read_csv(os.path.join(DATA_DIR, "matches.csv")))
    deliveries = clean_deliveries(pd.read_csv(os.path.join(DATA_DIR, "deliveries.csv")))
except Exception as error:
    messagebox.showerror(
        "Could not load the dataset",
        "Make sure data/matches.csv and data/deliveries.csv exist.\n\n" + str(error),
    )
    root.destroy()
    sys.exit(1)

# Lists used by the search boxes (built the same way as in src/search.py)
PLAYERS = sorted(set(deliveries["batter"].dropna()))
TEAMS = sorted(set(matches["team1"].dropna()) | set(matches["team2"].dropna()))
VENUES = sorted(set(matches["venue"].dropna()))


# ===================================
# HELPERS
# ===================================

def fmt(value):
    """Turn any value into clean table text: 8014 -> 8,014 and 55.1666 -> 55.17."""
    if value is None:
        return "-"
    if isinstance(value, str):
        return value
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    if pd.isna(value):
        return "-"
    if isinstance(value, numbers.Integral):
        return f"{value:,}"
    if isinstance(value, numbers.Real):
        return f"{value:,.2f}"
    return str(value)


_open_windows = {}


def open_window(key, title, width, height):
    """
    Create a feature window. If that window is already open, bring it to the
    front instead and return None (so the caller knows to stop).
    """
    existing = _open_windows.get(key)

    if existing is not None and existing.winfo_exists():
        existing.deiconify()
        existing.lift()
        existing.focus_force()
        return None

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.minsize(width * 2 // 3, height * 2 // 3)

    _open_windows[key] = win

    return win


def open_chart(title, chart_function):
    """
    Run one of the chart functions from src/visualizations.py and show the
    figure it draws inside a Tkinter window (with matplotlib's zoom/save toolbar).
    """
    with warnings.catch_warnings():
        # The chart functions end with plt.show(). With the no-window "Agg"
        # backend that only prints a harmless warning, so hide it.
        warnings.simplefilter("ignore")
        chart_function(deliveries)

    figure = plt.gcf()
    figure.set_size_inches(9, 4.8)
    figure.set_layout_engine("tight")  # keeps labels inside the window when it is resized

    win = tk.Toplevel(root)
    win.title(title)

    canvas = FigureCanvasTkAgg(figure, master=win)
    toolbar = NavigationToolbar2Tk(canvas, win, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side="bottom", fill="x")
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    canvas.draw()

    def close_chart():
        plt.close(figure)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", close_chart)


# ===================================
# REUSABLE WIDGETS
# ===================================

class SearchList(ttk.Frame):
    """
    A search box with a list underneath it.

    This replaces search_player / search_team / search_venue from src/search.py.
    Those functions call input() and wait for typing in the terminal, so they
    cannot be used inside a window. The matching rule is the same: a
    case-insensitive "contains" search.
    """

    def __init__(self, parent, items, label, on_submit=None, height=12):
        super().__init__(parent)

        self.items = list(items)
        self.shown = []
        self.on_submit = on_submit

        self.label = ttk.Label(self, text=label, font=LABEL_FONT)
        self.label.pack(anchor="w")

        self.query = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.query)
        self.entry.pack(fill="x", pady=(4, 4))

        holder = ttk.Frame(self)
        holder.pack(fill="both", expand=True)

        # exportselection=False keeps the selection when another list is used
        self.listbox = tk.Listbox(
            holder, height=height, exportselection=False, activestyle="none"
        )
        scrollbar = ttk.Scrollbar(holder, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status = ttk.Label(self, foreground="gray")
        self.status.pack(anchor="w", pady=(4, 0))

        self.query.trace_add("write", self.refresh)
        self.entry.bind("<Down>", self._focus_list)
        self.entry.bind("<Return>", self._entry_return)
        self.listbox.bind("<Double-Button-1>", self._submit)
        self.listbox.bind("<Return>", self._submit)

        self.refresh()

    def refresh(self, *_):
        text = self.query.get().strip().lower()

        self.shown = [item for item in self.items if text in item.lower()]

        self.listbox.delete(0, tk.END)
        for item in self.shown:
            self.listbox.insert(tk.END, item)

        if len(self.shown) == 1:  # only one match: select it for the user
            self.listbox.selection_set(0)

        self.status.config(text=f"{len(self.shown)} of {len(self.items)} shown")

    def get(self):
        """The item selected in the list, or None."""
        selection = self.listbox.curselection()

        if selection:
            return self.shown[selection[0]]

        return None

    def set_items(self, items, label=None):
        self.items = list(items)

        if label is not None:
            self.label.config(text=label)

        self.query.set("")
        self.refresh()

    def _focus_list(self, _event=None):
        if self.shown:
            self.listbox.focus_set()

            if not self.listbox.curselection():
                self.listbox.selection_set(0)
                self.listbox.activate(0)

        return "break"

    def _entry_return(self, _event=None):
        if self.get() is not None:
            self._submit()
        else:
            self._focus_list()

        return "break"

    def _submit(self, _event=None):
        if self.on_submit is not None:
            self.on_submit()


class Table(ttk.Frame):
    """A read-only table that can be refilled with new columns and rows."""

    def __init__(self, parent, height=10, hscroll=False):
        super().__init__(parent)

        self.tree = ttk.Treeview(
            self, show="headings", height=height, selectmode="browse"
        )
        vertical = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vertical.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")

        if hscroll:
            horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=horizontal.set)
            horizontal.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._font = tkfont.nametofont("TkDefaultFont")

    def show(self, columns, rows, iids=None):
        """
        columns: list of heading names
        rows:    list of tuples, one value per column
        iids:    optional list of row ids (used to know which row was clicked)
        """
        text_rows = [[fmt(cell) for cell in row] for row in rows]
        column_ids = [f"c{i}" for i in range(len(columns))]

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = column_ids

        for i, (column_id, name) in enumerate(zip(column_ids, columns)):
            self.tree.heading(column_id, text=str(name))

            # size each column to fit its longest text
            cells = [row[i] for row in text_rows[:300]]
            widest = max([self._font.measure(str(name))] + [self._font.measure(c) for c in cells])

            self.tree.column(
                column_id,
                width=min(widest + 30, 420),
                minwidth=60,
                anchor="w" if i == 0 else "center",
                stretch=True,
            )

        for n, row in enumerate(text_rows):
            self.tree.insert(
                "", "end", iid=None if iids is None else iids[n], values=row
            )


def lookup_window(key, title, noun, items, build_rows):
    """
    Shared layout for Player / Team / Venue analysis:
    search list on the left, "Statistic | Value" table on the right.
    build_rows(item) returns the list of (statistic, value) pairs.
    """
    win = open_window(key, title, 820, 520)
    if win is None:
        return

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    left = ttk.Frame(body)
    left.pack(side="left", fill="y", padx=(0, 14))

    right = ttk.Frame(body)
    right.pack(side="left", fill="both", expand=True)

    heading = ttk.Label(
        right,
        text=f"Pick a {noun} on the left, then press Show Statistics.",
        font=HEADING_FONT,
        wraplength=460,
        justify="left",
    )
    heading.pack(anchor="w", pady=(0, 8))

    table = Table(right, height=12)
    table.pack(fill="both", expand=True)

    def show_statistics():
        item = picker.get()

        if item is None:
            messagebox.showwarning(
                "Nothing selected",
                f"Please search for a {noun} and pick one from the list.",
                parent=win,
            )
            return

        heading.config(text=f"{title} - {item}")
        table.show(["Statistic", "Value"], build_rows(item))

    picker = SearchList(left, items, f"Search {noun}", on_submit=show_statistics)
    picker.pack(fill="both", expand=True)

    ttk.Button(left, text="Show Statistics", command=show_statistics).pack(
        fill="x", pady=(10, 0)
    )

    picker.entry.focus_set()


# ===================================
# OPTION 1 - PLAYER ANALYSIS
# ===================================

def player_analysis():

    def build_rows(player):
        return [
            ("Matches Played", get_player_matches(deliveries, player)),
            ("Total Runs", get_player_runs(deliveries, player)),
            ("Batting Average", round(get_player_average(deliveries, player), 2)),
            ("Strike Rate", round(get_player_strike_rate(deliveries, player), 2)),
            ("Fours", get_player_fours(deliveries, player)),
            ("Sixes", get_player_sixes(deliveries, player)),
            ("Highest Score", get_player_highest_score(deliveries, player)),
            ("50s", get_player_fifties(deliveries, player)),
            ("100s", get_player_hundreds(deliveries, player)),
        ]

    lookup_window(
        "player_analysis", "Player Analysis", "player", PLAYERS, build_rows
    )


# ===================================
# OPTION 2 - PLAYER COMPARISON
# ===================================

def player_comparison():
    win = open_window("player_comparison", "Player Comparison", 900, 660)
    if win is None:
        return

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    def compare():
        player1 = pick1.get()
        player2 = pick2.get()

        if player1 is None or player2 is None:
            messagebox.showwarning(
                "Nothing selected",
                "Please pick a player in BOTH lists.",
                parent=win,
            )
            return

        if player1 == player2:
            messagebox.showwarning(
                "Same player",
                "Please pick two different players.",
                parent=win,
            )
            return

        comparison = pd.DataFrame(compare_players(deliveries, player1, player2))
        first = comparison.iloc[0]
        second = comparison.iloc[1]

        stats = [
            ("Matches", "matches"),
            ("Runs", "runs"),
            ("Average", "average"),
            ("Strike Rate", "strike_rate"),
            ("Fours", "fours"),
            ("Sixes", "sixes"),
        ]

        rows = []
        for label, column in stats:
            if column == "matches" or first[column] == second[column]:
                leader = "-"
            elif first[column] > second[column]:
                leader = player1
            else:
                leader = player2

            rows.append((label, first[column], second[column], leader))

        table.show(["Statistic", player1, player2, "Leader"], rows)

    pickers = ttk.Frame(body)
    pickers.pack(fill="x")

    pick1 = SearchList(pickers, PLAYERS, "Search Player 1", height=7)
    pick1.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pick2 = SearchList(pickers, PLAYERS, "Search Player 2", height=7, on_submit=compare)
    pick2.pack(side="left", fill="both", expand=True, padx=(10, 0))

    ttk.Button(body, text="Compare Players", command=compare).pack(pady=12)

    table = Table(body, height=8)
    table.pack(fill="both", expand=True)

    pick1.entry.focus_set()


# ===================================
# OPTION 3 - TEAM ANALYSIS
# ===================================

def team_analysis():

    def build_rows(team):
        return [
            ("Matches", get_team_matches(matches, team)),
            ("Wins", get_team_wins(matches, team)),
            ("Losses", get_team_losses(matches, team)),
            ("Win Percentage", f"{round(get_team_win_percentage(matches, team), 2)}%"),
            ("Total Runs", get_team_runs(deliveries, team)),
            ("Wickets", get_team_wickets(deliveries, team)),
        ]

    lookup_window("team_analysis", "Team Analysis", "team", TEAMS, build_rows)


# ===================================
# OPTION 4 - MATCH ANALYSIS
# ===================================

def match_analysis():
    win = open_window("match_analysis", "Match Analysis", 1100, 640)
    if win is None:
        return

    # newest matches first; one lower-case text per match makes filtering quick
    match_list = matches.sort_values("date", ascending=False)
    search_text = (
        match_list["id"].astype(str) + " "
        + match_list["season"].astype(str) + " "
        + match_list["team1"].fillna("") + " "
        + match_list["team2"].fillna("") + " "
        + match_list["venue"].fillna("") + " "
        + match_list["city"].fillna("")
    ).str.lower()

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    left = ttk.Frame(body)
    left.pack(side="left", fill="both", expand=True, padx=(0, 14))

    right = ttk.Frame(body)
    right.pack(side="left", fill="both", expand=True)

    # ---- left: filterable list of all matches ----

    ttk.Label(
        left, text="Filter by team, season, venue, city or match ID", font=LABEL_FONT
    ).pack(anchor="w")

    filter_text = tk.StringVar()
    ttk.Entry(left, textvariable=filter_text).pack(fill="x", pady=(4, 6))

    match_table = Table(left, height=20, hscroll=True)
    match_table.pack(fill="both", expand=True)

    count_label = ttk.Label(left, foreground="gray")
    count_label.pack(anchor="w", pady=(4, 0))

    # ---- right: details of the selected match ----

    heading = ttk.Label(
        right,
        text="Select a match from the list",
        font=HEADING_FONT,
        wraplength=440,
        justify="left",
    )
    heading.pack(anchor="w", pady=(0, 8))

    details_table = Table(right, height=10)
    details_table.pack(fill="x")

    ttk.Label(right, text="Scorecard (total runs)", font=LABEL_FONT).pack(
        anchor="w", pady=(14, 4)
    )

    scorecard_table = Table(right, height=3)
    scorecard_table.pack(fill="x")

    def show_match(match_id):
        details = get_match_details(matches, match_id)
        if details is None:
            return

        winner = get_match_winner(matches, match_id)
        venue = get_match_venue(matches, match_id)
        best_batsman = get_best_batsman(deliveries, match_id)
        best_bowler = get_best_bowler(deliveries, match_id)
        scorecard = get_match_scorecard(deliveries, match_id)

        team1 = details.get("team1", "Unknown")
        team2 = details.get("team2", "Unknown")

        heading.config(text=f"{team1} vs {team2}")

        details_table.show(
            ["Statistic", "Value"],
            [
                ("Match ID", str(match_id)),
                ("Season", details.get("season", "Unknown")),
                ("Team 1", team1),
                ("Team 2", team2),
                ("Date", details.get("date", "Unknown")),
                ("Venue", venue),
                ("Winner", "No result" if pd.isna(winner) else winner),
                ("Man of the Match", details.get("player_of_match", "Unknown")),
                (
                    "Best Batsman",
                    "-" if best_batsman is None
                    else f"{best_batsman[0]} ({best_batsman[1]} runs)",
                ),
                (
                    "Best Bowler",
                    "-" if best_bowler is None
                    else f"{best_bowler[0]} ({best_bowler[1]} wickets)",
                ),
            ],
        )

        if scorecard is None:
            scorecard_rows = [("No ball-by-ball data for this match", "-")]
        else:
            scorecard_rows = list(scorecard.itertuples(index=False, name=None))

        scorecard_table.show(["Team", "Runs"], scorecard_rows)

    def on_match_selected(_event=None):
        selected = match_table.tree.selection()

        if selected:
            show_match(int(selected[0]))

    def fill_list(*_):
        text = filter_text.get().strip().lower()

        if text:
            shown = match_list[search_text.str.contains(text, regex=False)]
        else:
            shown = match_list

        rows = [
            (str(m.id), m.date, m.team1, m.team2) for m in shown.itertuples()
        ]
        ids = [str(m.id) for m in shown.itertuples()]

        match_table.show(["Match ID", "Date", "Team 1", "Team 2"], rows, iids=ids)
        count_label.config(text=f"{len(shown)} of {len(match_list)} matches shown")

        if ids:  # preview the first match straight away
            match_table.tree.selection_set(ids[0])
            match_table.tree.focus(ids[0])
            match_table.tree.see(ids[0])

    match_table.tree.bind("<<TreeviewSelect>>", on_match_selected)
    filter_text.trace_add("write", fill_list)

    fill_list()


# ===================================
# OPTION 5 - VENUE ANALYSIS
# ===================================

def venue_analysis():

    def build_rows(venue):
        return [
            ("Matches Played", get_venue_matches(matches, venue)),
            ("Total Runs", get_venue_runs(deliveries, matches, venue)),
            ("Average Runs per Match", get_venue_average_runs(deliveries, matches, venue)),
            ("Matches with Recorded Winner", get_venue_wins(matches, venue)),
            ("Most Common Team", get_most_common_team(deliveries, matches, venue)),
        ]

    lookup_window("venue_analysis", "Venue Analysis", "venue", VENUES, build_rows)


# ===================================
# OPTION 6 - PERFORMANCE TRENDS
# ===================================

TREND_OPTIONS = [
    "Team Season Performance",
    "Player Season Runs",
    "Team Season Runs",
]

TREND_HEADINGS = {
    "season": "Season",
    "matches": "Matches",
    "wins": "Wins",
    "win_percentage": "Win %",
    "batsman_runs": "Runs",
    "total_runs": "Runs",
}


def performance_trends():
    win = open_window("performance_trends", "Performance Trends", 1100, 660)
    if win is None:
        return

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    left = ttk.Frame(body)
    left.pack(side="left", fill="y", padx=(0, 14))

    right = ttk.Frame(body)
    right.pack(side="left", fill="both", expand=True)

    # ---- right: chart on top, table underneath ----

    figure = Figure(figsize=(6.5, 3.4), dpi=100, layout="tight")
    axes = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=right)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_hint(message):
        axes.clear()
        axes.set_axis_off()
        axes.text(0.5, 0.5, message, ha="center", va="center", transform=axes.transAxes)
        canvas.draw()

    show_hint("Choose a trend, pick a team or player,\nthen press Show Trend")

    table = Table(right, height=6)
    table.pack(fill="x", pady=(10, 0))

    def draw_chart(option, name, data):
        axes.clear()
        axes.set_axis_on()

        seasons = data["season"].astype(str).tolist()

        if option == "Team Season Performance":
            axes.plot(seasons, data["win_percentage"], marker="o")
            axes.set_ylabel("Win %")
            axes.set_ylim(0, 100)
        else:
            column = "batsman_runs" if option == "Player Season Runs" else "total_runs"
            axes.bar(seasons, data[column])
            axes.set_ylabel("Runs")

        axes.set_title(f"{name} - {option}")
        axes.set_xlabel("Season")
        axes.tick_params(axis="x", labelrotation=45)
        for label in axes.get_xticklabels():
            label.set_horizontalalignment("right")
        axes.grid(axis="y", alpha=0.3)

        canvas.draw()

    def show_trend():
        option = trend_type.get()
        name = picker.get()

        if name is None:
            messagebox.showwarning(
                "Nothing selected",
                "Please search and pick from the list first.",
                parent=win,
            )
            return

        if option == "Team Season Performance":
            data = get_team_season_performance(matches, name)
        elif option == "Player Season Runs":
            data = get_player_season_runs(deliveries, matches, name)
        else:
            data = get_team_season_runs(deliveries, matches, name)

        if data.empty:
            show_hint("No data found")
            table.show(["Season"], [])
            return

        draw_chart(option, name, data)

        table.show(
            [TREND_HEADINGS.get(column, column) for column in data.columns],
            list(data.itertuples(index=False, name=None)),
        )

    def change_trend(_event=None):
        if trend_type.get() == "Player Season Runs":
            picker.set_items(PLAYERS, "Search player")
        else:
            picker.set_items(TEAMS, "Search team")

    # ---- left: controls ----

    ttk.Label(left, text="Trend", font=LABEL_FONT).pack(anchor="w")

    trend_type = ttk.Combobox(left, values=TREND_OPTIONS, state="readonly", width=28)
    trend_type.current(0)
    trend_type.pack(fill="x", pady=(4, 12))
    trend_type.bind("<<ComboboxSelected>>", change_trend)

    picker = SearchList(left, TEAMS, "Search team", on_submit=show_trend)
    picker.pack(fill="both", expand=True)

    ttk.Button(left, text="Show Trend", command=show_trend).pack(fill="x", pady=(10, 0))

    picker.entry.focus_set()


# ===================================
# OPTION 7 - TOP PERFORMERS
# ===================================

TOP_OPTIONS = {
    "Top Run Scorers": get_top_run_scorers,
    "Top Wicket Takers": get_top_wicket_takers,
    "Most Sixes": get_most_sixes,
    "Most Fours": get_most_fours,
}


def top_performers():
    win = open_window("top_performers", "Top Performers", 560, 560)
    if win is None:
        return

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    controls = ttk.Frame(body)
    controls.pack(fill="x", pady=(0, 10))

    def refresh(_event=None):
        try:
            count = int(top_n.get())
        except ValueError:
            count = 10

        count = max(1, min(count, 100))
        top_n.set(str(count))

        result = TOP_OPTIONS[category.get()](deliveries, count)

        rows = [
            (rank, player, value)
            for rank, (player, value) in enumerate(result.itertuples(index=False), start=1)
        ]

        table.show(["Rank", "Player", result.columns[1]], rows)

    ttk.Label(controls, text="Category", font=LABEL_FONT).pack(side="left")

    category = ttk.Combobox(
        controls, values=list(TOP_OPTIONS), state="readonly", width=22
    )
    category.current(0)
    category.pack(side="left", padx=(6, 20))
    category.bind("<<ComboboxSelected>>", refresh)

    ttk.Label(controls, text="Show top", font=LABEL_FONT).pack(side="left")

    top_n = tk.StringVar(value="10")
    spinbox = ttk.Spinbox(
        controls, from_=1, to=100, width=5, textvariable=top_n, command=refresh
    )
    spinbox.pack(side="left", padx=6)
    spinbox.bind("<Return>", refresh)
    spinbox.bind("<FocusOut>", refresh)

    table = Table(body, height=15)
    table.pack(fill="both", expand=True)

    refresh()


# ===================================
# OPTION 8 - VISUALIZATIONS
# ===================================

CHARTS = [
    ("Top 10 Run Scorers", show_top_run_scorers),
    ("Top 10 Wicket Takers", show_top_wicket_takers),
    ("Top 10 Players by Sixes", show_most_sixes),
    ("Top 10 Players by Fours", show_most_fours),
    ("Team Total Runs", show_team_runs),
]


def visualizations():
    win = open_window("visualizations", "Visualizations", 360, 380)
    if win is None:
        return

    body = ttk.Frame(win, padding=20)
    body.pack(fill="both", expand=True)

    ttk.Label(body, text="Choose a chart", font=HEADING_FONT).pack(pady=(0, 14))

    for text, chart_function in CHARTS:
        ttk.Button(
            body,
            text=text,
            command=lambda t=text, f=chart_function: open_chart(t, f),
        ).pack(fill="x", pady=5, ipady=6)


# ===================================
# OPTION 9 - DATASET SUMMARY
# ===================================

def dataset_summary():
    win = open_window("dataset_summary", "Dataset Summary", 460, 380)
    if win is None:
        return

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    ttk.Label(body, text="Dataset Summary", font=HEADING_FONT).pack(
        anchor="w", pady=(0, 8)
    )

    table = Table(body, height=9)
    table.pack(fill="both", expand=True)

    table.show(["Statistic", "Value"], list(get_dataset_summary(matches, deliveries).items()))


# ===================================
# MAIN MENU
# ===================================

def exit_app():
    plt.close("all")
    root.destroy()


root.title("Cricket Performance Analysis System")
root.geometry("800x680")
root.protocol("WM_DELETE_WINDOW", exit_app)

tk.Label(
    root,
    text="CRICKET PERFORMANCE ANALYSIS SYSTEM",
    font=TITLE_FONT,
).pack(pady=(25, 5))

tk.Label(
    root,
    text="IPL Data Analysis & Performance Insights",
    font=("Arial", 12),
).pack(pady=5)

MENU = [
    ("Player Analysis", player_analysis),
    ("Player Comparison", player_comparison),
    ("Team Analysis", team_analysis),
    ("Match Analysis", match_analysis),
    ("Venue Analysis", venue_analysis),
    ("Performance Trends", performance_trends),
    ("Top Performers", top_performers),
    ("Visualizations", visualizations),
    ("Dataset Summary", dataset_summary),
]

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

for index, (text, command) in enumerate(MENU):
    row, column = divmod(index, 2)

    # a lone last button is centred across both columns
    span = 2 if index == len(MENU) - 1 and len(MENU) % 2 == 1 else 1

    tk.Button(
        button_frame,
        text=text,
        width=25,
        height=2,
        command=command,
    ).grid(row=row, column=column, columnspan=span, padx=10, pady=8)

tk.Button(
    root,
    text="Exit",
    width=20,
    height=2,
    command=exit_app,
).pack(pady=(10, 5))

tk.Label(
    root,
    text=f"Dataset loaded: {len(matches):,} matches, {len(deliveries):,} deliveries",
    font=("Arial", 9),
    fg="gray",
).pack(side="bottom", pady=8)

root.deiconify()


# ===================================
# START GUI
# ===================================

if __name__ == "__main__":
    root.mainloop()