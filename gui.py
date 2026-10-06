
import os
import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd

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

from src.search import find_players, find_teams, find_venues
from src.dataset_summary import get_dataset_summary

from src.visualizations import (
    show_top_run_scorers,
    show_top_wicket_takers,
    show_most_sixes,
    show_most_fours,
    show_team_runs,
)


# =========================================================
# DATA LOADING
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

matches = clean_matches(
    pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
)

deliveries = clean_deliveries(
    pd.read_csv(os.path.join(DATA_DIR, "deliveries.csv"))
)


# =========================================================
# MAIN APPLICATION
# =========================================================

class CricketApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Cricket Performance Analysis System")
        self.root.geometry("1050x720")
        self.root.minsize(900, 620)

        # -------------------------------------------------
        # COLORS
        # -------------------------------------------------

        self.bg_color = "#F5F7FA"
        self.white = "#FFFFFF"

        self.primary = "#1F3A5F"
        self.primary_hover = "#294D7A"

        self.accent = "#3F72AF"
        self.accent_light = "#E8F0F8"

        self.text_dark = "#1F2937"
        self.text_light = "#667085"

        self.border = "#D9E1EA"
        self.exit_color = "#B94A48"
        self.exit_hover = "#A13F3D"

        # -------------------------------------------------
        # FONTS
        # -------------------------------------------------

        self.title_font = ("Arial", 23, "bold")
        self.subtitle_font = ("Arial", 11)
        self.section_font = ("Arial", 15, "bold")
        self.button_font = ("Arial", 10, "bold")
        self.normal_font = ("Arial", 10)

        self.root.configure(
            bg=self.bg_color
        )

        self.setup_styles()
        self.build_main_window()

    # =====================================================
    # STYLES
    # =====================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Buttons
        style.configure(
            "TButton",
            font=self.button_font,
            padding=8,
            background=self.primary,
            foreground=self.white,
            borderwidth=0,
        )

        style.map(
            "TButton",
            background=[
                ("active", self.primary_hover),
                ("pressed", self.primary_hover),
            ],
            foreground=[
                ("active", self.white),
            ],
        )

        # Entry
        style.configure(
            "TEntry",
            padding=6,
            fieldbackground=self.white,
            foreground=self.text_dark,
        )

        # Treeview
        style.configure(
            "Treeview",
            background=self.white,
            foreground=self.text_dark,
            fieldbackground=self.white,
            rowheight=28,
            font=("Arial", 10),
        )

        style.configure(
            "Treeview.Heading",
            background=self.primary,
            foreground=self.white,
            font=("Arial", 10, "bold"),
            padding=7,
        )

        style.map(
            "Treeview",
            background=[
                ("selected", self.accent),
            ],
            foreground=[
                ("selected", self.white),
            ],
        )

    # =====================================================
    # MAIN WINDOW
    # =====================================================

    def build_main_window(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=self.primary,
            padx=25,
            pady=22,
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="🏏  CRICKET PERFORMANCE ANALYSIS SYSTEM",
            font=self.title_font,
            fg=self.white,
            bg=self.primary,
        ).pack()

        tk.Label(
            header,
            text="IPL Data Analysis & Performance Insights",
            font=self.subtitle_font,
            fg="#DCE6F2",
            bg=self.primary,
        ).pack(
            pady=(5, 0)
        )

        # -------------------------------------------------
        # DATASET CARDS
        # -------------------------------------------------

        info_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
        )

        info_frame.pack(
            fill="x",
            padx=35,
            pady=(22, 15),
        )

        self.create_info_card(
            info_frame,
            "MATCHES",
            f"{len(matches):,}",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
        )

        self.create_info_card(
            info_frame,
            "DELIVERIES",
            f"{len(deliveries):,}",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
        )

        self.create_info_card(
            info_frame,
            "SEASONS",
            f"{matches['season'].nunique():,}",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
        )

        self.create_info_card(
            info_frame,
            "TEAMS",
            f"{len(find_teams(matches)):,}",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
        )

        # -------------------------------------------------
        # SECTION TITLE
        # -------------------------------------------------

        tk.Label(
            self.root,
            text="Analysis Modules",
            font=self.section_font,
            fg=self.text_dark,
            bg=self.bg_color,
        ).pack(
            pady=(5, 10)
        )

        # -------------------------------------------------
        # BUTTON GRID
        # -------------------------------------------------

        button_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
            padx=35,
        )

        button_frame.pack(
            fill="both",
            expand=True,
        )

        options = [
            ("Player Analysis", self.player_analysis),
            ("Player Comparison", self.player_comparison),
            ("Team Analysis", self.team_analysis),
            ("Match Analysis", self.match_analysis),
            ("Venue Analysis", self.venue_analysis),
            ("Performance Trends", self.performance_trends),
            ("Top Performers", self.top_performers),
            ("Visualizations", self.visualizations),
            ("Dataset Summary", self.dataset_summary),
        ]

        for index, (text, command) in enumerate(options):

            row, column = divmod(
                index,
                3
            )

            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.button_font,
                fg=self.primary,
                bg=self.white,
                activeforeground=self.white,
                activebackground=self.primary,
                relief="flat",
                bd=0,
                cursor="hand2",
                highlightbackground=self.border,
                highlightthickness=1,
            )

            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=7,
                pady=7,
                ipady=10,
            )

            self.add_hover_effect(
                button,
                self.white,
                self.accent_light,
            )

        for column in range(3):

            button_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        for row in range(3):

            button_frame.grid_rowconfigure(
                row,
                weight=1,
            )

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        exit_button = tk.Button(
            self.root,
            text="Exit Application",
            command=self.root.destroy,
            font=("Arial", 10, "bold"),
            fg=self.white,
            bg=self.exit_color,
            activeforeground=self.white,
            activebackground=self.exit_hover,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=7,
        )

        exit_button.pack(
            pady=(10, 20)
        )

        self.add_hover_effect(
            exit_button,
            self.exit_color,
            self.exit_hover,
        )

    # =====================================================
    # INFO CARD
    # =====================================================

    def create_info_card(
        self,
        parent,
        title,
        value
    ):

        frame = tk.Frame(
            parent,
            bg=self.white,
            padx=15,
            pady=10,
            highlightbackground=self.border,
            highlightthickness=1,
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 9, "bold"),
            fg=self.text_light,
            bg=self.white,
        ).pack()

        tk.Label(
            frame,
            text=value,
            font=("Arial", 16, "bold"),
            fg=self.primary,
            bg=self.white,
        ).pack(
            pady=(2, 0)
        )

        return frame

    # =====================================================
    # HOVER EFFECT
    # =====================================================

    def add_hover_effect(
        self,
        widget,
        normal_color,
        hover_color
    ):

        widget.bind(
            "<Enter>",
            lambda event:
            widget.configure(
                bg=hover_color
            ),
        )

        widget.bind(
            "<Leave>",
            lambda event:
            widget.configure(
                bg=normal_color
            ),
        )

    # =====================================================
    # CHILD WINDOW SETUP
    # =====================================================

    def setup_child_window(
        self,
        window
    ):

        window.configure(
            bg=self.bg_color
        )

        window.transient(
            self.root
        )

    # =====================================================
    # SELECTION WINDOW
    # =====================================================

    def selection_window(
        self,
        title,
        items,
        callback
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            title
        )

        window.geometry(
            "540x570"
        )

        window.minsize(
            480,
            500
        )

        self.setup_child_window(
            window
        )

        window.grab_set()

        tk.Label(
            window,
            text=title,
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(18, 5)
        )

        tk.Label(
            window,
            text="Search and select an item",
            font=self.normal_font,
            fg=self.text_light,
            bg=self.bg_color,
        ).pack(
            pady=(0, 12)
        )

        # Search
        search_var = tk.StringVar()

        search_frame = tk.Frame(
            window,
            bg=self.bg_color,
        )

        search_frame.pack(
            fill="x",
            padx=25
        )

        search_entry = ttk.Entry(
            search_frame,
            textvariable=search_var,
        )

        search_entry.pack(
            fill="x"
        )

        # List
        list_frame = tk.Frame(
            window,
            bg=self.bg_color,
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15,
        )

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=None,
        )

        listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            bg=self.white,
            fg=self.text_dark,
            selectbackground=self.accent,
            selectforeground=self.white,
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.border,
        )

        scrollbar.config(
            command=listbox.yview
        )

        listbox.config(
            yscrollcommand=scrollbar.set
        )

        listbox.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        # Refresh list
        def refresh(*_):

            query = search_var.get().strip().lower()

            filtered = [
                item
                for item in items
                if query in str(item).lower()
            ]

            listbox.delete(
                0,
                tk.END
            )

            for item in filtered:

                listbox.insert(
                    tk.END,
                    item
                )

        # Select
        def select():

            selection = listbox.curselection()

            if not selection:

                messagebox.showwarning(
                    "Selection Required",
                    "Please select an item.",
                    parent=window,
                )

                return

            selected_item = listbox.get(
                selection[0]
            )

            window.destroy()

            try:

                callback(
                    selected_item
                )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    f"Unable to process the selection.\n\n{error}",
                    parent=self.root,
                )

        search_var.trace_add(
            "write",
            refresh
        )

        listbox.bind(
            "<Double-Button-1>",
            lambda _: select()
        )

        # Buttons
        button_frame = tk.Frame(
            window,
            bg=self.bg_color,
        )

        button_frame.pack(
            pady=(0, 18)
        )

        select_button = tk.Button(
            button_frame,
            text="Select",
            command=select,
            font=("Arial", 10, "bold"),
            fg=self.white,
            bg=self.primary,
            activeforeground=self.white,
            activebackground=self.primary_hover,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=7,
        )

        select_button.pack(
            side="left",
            padx=5
        )

        close_button = tk.Button(
            button_frame,
            text="Close",
            command=window.destroy,
            font=("Arial", 10, "bold"),
            fg=self.primary,
            bg=self.white,
            activeforeground=self.white,
            activebackground=self.accent_light,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=7,
            highlightbackground=self.border,
            highlightthickness=1,
        )

        close_button.pack(
            side="left",
            padx=5
        )

        self.add_hover_effect(
            select_button,
            self.primary,
            self.primary_hover,
        )

        self.add_hover_effect(
            close_button,
            self.white,
            self.accent_light,
        )

        search_entry.focus()

        refresh()

    # =====================================================
    # TABLE WINDOW
    # =====================================================

    def show_table(
        self,
        title,
        dataframe
    ):

        if dataframe is None or dataframe.empty:

            messagebox.showinfo(
                title,
                "No data available.",
                parent=self.root,
            )

            return

        window = tk.Toplevel(
            self.root
        )

        window.title(
            title
        )

        window.geometry(
            "900x550"
        )

        window.minsize(
            700,
            400
        )

        self.setup_child_window(
            window
        )

        tk.Label(
            window,
            text=title,
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(15, 10)
        )

        frame = tk.Frame(
            window,
            bg=self.bg_color,
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        columns = [
            str(column)
            for column in dataframe.columns
        ]

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
        )

        y_scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview,
        )

        x_scroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview,
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
        )

        for column in columns:

            tree.heading(
                column,
                text=column,
            )

            tree.column(
                column,
                width=140,
                anchor="center",
            )

        for row in dataframe.itertuples(
            index=False,
            name=None,
        ):

            formatted_row = []

            for value in row:

                if isinstance(value, float):

                    formatted_row.append(
                        f"{value:.2f}"
                    )

                else:

                    formatted_row.append(
                        str(value)
                    )

            tree.insert(
                "",
                "end",
                values=formatted_row,
            )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        frame.grid_rowconfigure(
            0,
            weight=1
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=(0, 15),
            ipadx=20,
        )

    # =====================================================
    # STATISTICS WINDOW
    # =====================================================

    def show_stats(
        self,
        title,
        stats
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            title
        )

        window.geometry(
            "600x560"
        )

        window.minsize(
            500,
            450
        )

        self.setup_child_window(
            window
        )

        tk.Label(
            window,
            text=title,
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(18, 12)
        )

        container = tk.Frame(
            window,
            bg=self.bg_color,
            padx=25,
            pady=5,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        for row, (label, value) in enumerate(
            stats.items()
        ):

            card = tk.Frame(
                container,
                bg=self.white,
                highlightbackground=self.border,
                highlightthickness=1,
                padx=12,
                pady=9,
            )

            card.grid(
                row=row,
                column=0,
                sticky="ew",
                pady=4,
            )

            tk.Label(
                card,
                text=label,
                font=("Arial", 10, "bold"),
                fg=self.text_dark,
                bg=self.white,
                anchor="w",
            ).pack(
                side="left",
                fill="x",
                expand=True,
            )

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 10, "bold"),
                fg=self.primary,
                bg=self.white,
                anchor="e",
            ).pack(
                side="right",
            )

        container.grid_columnconfigure(
            0,
            weight=1
        )

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=(5, 18),
            ipadx=20,
        )

    # =====================================================
    # PLAYER ANALYSIS
    # =====================================================

    def player_analysis(self):

        players = find_players(
            deliveries
        )

        def analyze(player):

            stats = {

                "Matches Played":
                    get_player_matches(
                        deliveries,
                        player,
                    ),

                "Total Runs":
                    get_player_runs(
                        deliveries,
                        player,
                    ),

                "Batting Average":
                    round(
                        get_player_average(
                            deliveries,
                            player,
                        ),
                        2,
                    ),

                "Strike Rate":
                    round(
                        get_player_strike_rate(
                            deliveries,
                            player,
                        ),
                        2,
                    ),

                "Fours":
                    get_player_fours(
                        deliveries,
                        player,
                    ),

                "Sixes":
                    get_player_sixes(
                        deliveries,
                        player,
                    ),

                "Highest Score":
                    get_player_highest_score(
                        deliveries,
                        player,
                    ),

                "50s":
                    get_player_fifties(
                        deliveries,
                        player,
                    ),

                "100s":
                    get_player_hundreds(
                        deliveries,
                        player,
                    ),
            }

            self.show_stats(
                f"Player Analysis - {player}",
                stats,
            )

        self.selection_window(
            "Select Player",
            players,
            analyze,
        )

    # =====================================================
    # PLAYER COMPARISON
    # =====================================================

    def player_comparison(self):

        players = find_players(
            deliveries
        )

        def select_first(player1):

            remaining = [
                player
                for player in players
                if player != player1
            ]

            def select_second(player2):

                comparison = pd.DataFrame(
                    compare_players(
                        deliveries,
                        player1,
                        player2,
                    )
                )

                if not comparison.empty:

                    comparison.columns = [
                        "Player",
                        "Matches",
                        "Runs",
                        "Average",
                        "Strike Rate",
                        "Fours",
                        "Sixes",
                    ]

                self.show_table(
                    "Player Comparison",
                    comparison,
                )

            self.selection_window(
                f"Select Player 2 (Player 1: {player1})",
                remaining,
                select_second,
            )

        self.selection_window(
            "Select Player 1",
            players,
            select_first,
        )

    # =====================================================
    # TEAM ANALYSIS
    # =====================================================

    def team_analysis(self):

        teams = find_teams(
            matches
        )

        def analyze(team):

            stats = {

                "Matches":
                    get_team_matches(
                        matches,
                        team,
                    ),

                "Wins":
                    get_team_wins(
                        matches,
                        team,
                    ),

                "Losses":
                    get_team_losses(
                        matches,
                        team,
                    ),

                "Win Percentage":
                    f"{get_team_win_percentage(matches, team):.2f}%",

                "Total Runs":
                    get_team_runs(
                        deliveries,
                        team,
                    ),

                "Wickets":
                    get_team_wickets(
                        deliveries,
                        team,
                    ),
            }

            self.show_stats(
                f"Team Analysis - {team}",
                stats,
            )

        self.selection_window(
            "Select Team",
            teams,
            analyze,
        )

    # =====================================================
    # MATCH ANALYSIS
    # =====================================================

    def match_analysis(self):

        available = matches.copy()

        match_choices = {

            f'{row.id} | {row.team1} vs {row.team2} | '
            f'{row.date.strftime("%Y-%m-%d")}':
            row.id

            for row in available.itertuples(
                index=False
            )
        }

        def analyze(choice):

            match_id = match_choices[
                choice
            ]

            details = get_match_details(
                matches,
                match_id,
            )

            scorecard = get_match_scorecard(
                deliveries,
                match_id,
            )

            best_batsman = get_best_batsman(
                deliveries,
                match_id,
            )

            best_bowler = get_best_bowler(
                deliveries,
                match_id,
            )

            player_of_match = details.get(
                "player_of_match",
                "Not Available",
            )

            stats = {

                "Teams":
                    f"{details['team1']} vs {details['team2']}",

                "Date":
                    details["date"].strftime(
                        "%Y-%m-%d"
                    ),

                "Venue":
                    details["venue"],

                "Winner":
                    details["winner"],

                "Player of Match":
                    player_of_match,

                "Best Batsman":
                    (
                        f"{best_batsman[0]} "
                        f"({best_batsman[1]} runs)"
                        if best_batsman
                        else "Not Available"
                    ),

                "Best Bowler":
                    (
                        f"{best_bowler[0]} "
                        f"({best_bowler[1]} wickets)"
                        if best_bowler
                        else "Not Available"
                    ),
            }

            self.show_stats(
                f"Match Analysis - {match_id}",
                stats,
            )

            if scorecard is not None:

                self.show_table(
                    "Match Scorecard",
                    scorecard,
                )

        self.selection_window(
            "Select Match",
            list(match_choices.keys()),
            analyze,
        )

    # =====================================================
    # VENUE ANALYSIS
    # =====================================================

    def venue_analysis(self):

        venues = find_venues(
            matches
        )

        def analyze(venue):

            average_runs = get_venue_average_runs(
                deliveries,
                matches,
                venue,
            )

            stats = {

                "Matches":
                    get_venue_matches(
                        matches,
                        venue,
                    ),

                "Matches with Result":
                    get_venue_wins(
                        matches,
                        venue,
                    ),

                "Total Runs":
                    get_venue_runs(
                        deliveries,
                        matches,
                        venue,
                    ),

                "Average Runs per Match":
                    round(
                        average_runs,
                        2,
                    ),

                "Most Common Team":
                    get_most_common_team(
                        deliveries,
                        matches,
                        venue,
                    ),
            }

            self.show_stats(
                f"Venue Analysis - {venue}",
                stats,
            )

        self.selection_window(
            "Select Venue",
            venues,
            analyze,
        )

    # =====================================================
    # PERFORMANCE TRENDS
    # =====================================================

    def performance_trends(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Performance Trends"
        )

        window.geometry(
            "480x360"
        )

        self.setup_child_window(
            window
        )

        window.grab_set()

        tk.Label(
            window,
            text="Performance Trends",
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            window,
            text="Choose the type of seasonal analysis",
            font=self.normal_font,
            fg=self.text_light,
            bg=self.bg_color,
        ).pack(
            pady=(0, 15)
        )

        def choose_team_performance():

            window.destroy()

            self.selection_window(
                "Select Team",
                find_teams(matches),
                lambda team:
                self.show_table(
                    f"{team} - Season Performance",
                    get_team_season_performance(
                        matches,
                        team,
                    ),
                ),
            )

        def choose_player_runs():

            window.destroy()

            self.selection_window(
                "Select Player",
                find_players(deliveries),
                lambda player:
                self.show_table(
                    f"{player} - Season Runs",
                    get_player_season_runs(
                        deliveries,
                        matches,
                        player,
                    ),
                ),
            )

        def choose_team_runs():

            window.destroy()

            self.selection_window(
                "Select Team",
                find_teams(matches),
                lambda team:
                self.show_table(
                    f"{team} - Season Runs",
                    get_team_season_runs(
                        deliveries,
                        matches,
                        team,
                    ),
                ),
            )

        buttons = [
            (
                "Team Season Performance",
                choose_team_performance,
            ),
            (
                "Player Season Runs",
                choose_player_runs,
            ),
            (
                "Team Season Runs",
                choose_team_runs,
            ),
        ]

        for text, command in buttons:

            ttk.Button(
                window,
                text=text,
                command=command,
            ).pack(
                fill="x",
                padx=55,
                pady=7,
                ipady=5,
            )

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=15,
            ipadx=20,
        )

    # =====================================================
    # TOP PERFORMERS
    # =====================================================

    def top_performers(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Top Performers"
        )

        window.geometry(
            "430x400"
        )

        self.setup_child_window(
            window
        )

        window.grab_set()

        tk.Label(
            window,
            text="Top Performers",
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            window,
            text="Leading players in different categories",
            font=self.normal_font,
            fg=self.text_light,
            bg=self.bg_color,
        ).pack(
            pady=(0, 15)
        )

        options = [
            (
                "Top Run Scorers",
                get_top_run_scorers(deliveries),
            ),
            (
                "Top Wicket Takers",
                get_top_wicket_takers(deliveries),
            ),
            (
                "Most Sixes",
                get_most_sixes(deliveries),
            ),
            (
                "Most Fours",
                get_most_fours(deliveries),
            ),
        ]

        for title, dataframe in options:

            ttk.Button(
                window,
                text=title,
                command=lambda
                t=title,
                d=dataframe:
                self.show_table(t, d),
            ).pack(
                fill="x",
                padx=55,
                pady=6,
                ipady=4,
            )

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=15,
            ipadx=20,
        )

    # =====================================================
    # VISUALIZATIONS
    # =====================================================

    def visualizations(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Visualizations"
        )

        window.geometry(
            "430x440"
        )

        self.setup_child_window(
            window
        )

        window.grab_set()

        tk.Label(
            window,
            text="Visualizations",
            font=self.section_font,
            fg=self.primary,
            bg=self.bg_color,
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            window,
            text="Generate graphical insights from the dataset",
            font=self.normal_font,
            fg=self.text_light,
            bg=self.bg_color,
        ).pack(
            pady=(0, 15)
        )

        charts = [
            (
                "Top Run Scorers",
                show_top_run_scorers,
            ),
            (
                "Top Wicket Takers",
                show_top_wicket_takers,
            ),
            (
                "Most Sixes",
                show_most_sixes,
            ),
            (
                "Most Fours",
                show_most_fours,
            ),
            (
                "Team Total Runs",
                show_team_runs,
            ),
        ]

        for title, function in charts:

            ttk.Button(
                window,
                text=title,
                command=lambda fn=function:
                fn(deliveries),
            ).pack(
                fill="x",
                padx=55,
                pady=6,
                ipady=4,
            )

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=15,
            ipadx=20,
        )

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def dataset_summary(self):

        summary = get_dataset_summary(
            matches,
            deliveries,
        )

        self.show_stats(
            "Dataset Summary",
            summary,
        )


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CricketApp(
        root
    )

    root.mainloop()
