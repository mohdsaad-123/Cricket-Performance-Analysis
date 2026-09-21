import pandas as pd

from src.data_cleaning import (
    clean_matches,
    clean_deliveries
)

from src.player_analysis import (
    get_player_runs,
    get_player_matches,
    get_player_average,
    get_player_strike_rate,
    get_player_fours,
    get_player_sixes,
    get_player_highest_score,
    get_player_fifties,
    get_player_hundreds
)

from src.player_comparison import (
    compare_players
)

from src.team_analysis import (
    get_team_matches,
    get_team_wins,
    get_team_losses,
    get_team_win_percentage,
    get_team_runs,
    get_team_wickets
)

from src.match_analysis import (
    get_match_details,
    get_match_scorecard,
    get_best_batsman,
    get_best_bowler
)

from src.venue_analysis import (
    get_venue_matches,
    get_venue_wins,
    get_venue_runs,
    get_venue_average_runs,
    get_most_common_team
)

from src.performance_trends import (
    get_team_season_performance,
    get_player_season_runs,
    get_team_season_runs
)

from src.top_performers import (
    get_top_run_scorers,
    get_top_wicket_takers,
    get_most_sixes,
    get_most_fours
)

from src.search import (
    search_player,
    search_team,
    search_venue
)

from src.dataset_summary import (
    get_dataset_summary
)

from src.ui import (
    show_header,
    show_menu,
    get_menu_choice,
    show_player_analysis,
    show_team_analysis,
    show_dataframe,
    show_message,
    show_error,
    show_success,
    pause
)


# ===================================
# LOAD DATASET
# ===================================

matches = pd.read_csv(
    "data/matches.csv"
)

deliveries = pd.read_csv(
    "data/deliveries.csv"
)


# ===================================
# CLEAN DATASET
# ===================================

matches = clean_matches(
    matches
)

deliveries = clean_deliveries(
    deliveries
)


# ===================================
# OPTION 1
# PLAYER ANALYSIS
# ===================================

def player_analysis():

    player = search_player(
        deliveries
    )

    if player is None:
        return

    player_data = deliveries[
        deliveries["batter"] == player
    ]

    if player_data.empty:

        show_error(
            "Player not found."
        )

        return

    runs = get_player_runs(
        deliveries,
        player
    )

    matches_played = get_player_matches(
        deliveries,
        player
    )

    average = get_player_average(
        deliveries,
        player
    )

    strike_rate = get_player_strike_rate(
        deliveries,
        player
    )

    fours = get_player_fours(
        deliveries,
        player
    )

    sixes = get_player_sixes(
        deliveries,
        player
    )

    highest_score = get_player_highest_score(
        deliveries,
        player
    )

    fifties = get_player_fifties(
        deliveries,
        player
    )

    hundreds = get_player_hundreds(
        deliveries,
        player
    )

    show_player_analysis(
        player,
        runs,
        matches_played,
        round(average, 2),
        round(strike_rate, 2),
        fours,
        sixes,
        highest_score,
        fifties,
        hundreds
    )

    pause()


# ===================================
# OPTION 2
# PLAYER COMPARISON
# ===================================

def player_comparison():

    show_message(
        "Select Player 1"
    )

    player1 = search_player(
        deliveries
    )

    if player1 is None:
        return

    show_message(
        "Select Player 2"
    )

    player2 = search_player(
        deliveries
    )

    if player2 is None:
        return

    comparison = compare_players(
        deliveries,
        player1,
        player2
    )

    comparison_df = pd.DataFrame(
        comparison
    )

    if comparison_df.empty:

        show_error(
            "No player data found."
        )

        pause()

        return

    show_dataframe(
        comparison_df,
        "Player Comparison"
    )

    pause()


# ===================================
# OPTION 3
# TEAM ANALYSIS
# ===================================

def team_analysis():

    team = search_team(
        matches
    )

    if team is None:
        return

    total_matches = get_team_matches(
        matches,
        team
    )

    wins = get_team_wins(
        matches,
        team
    )

    losses = get_team_losses(
        matches,
        team
    )

    win_percentage = get_team_win_percentage(
        matches,
        team
    )

    total_runs = get_team_runs(
        deliveries,
        team
    )

    total_wickets = get_team_wickets(
        deliveries,
        team
    )

    show_team_analysis(
        team,
        total_matches,
        wins,
        losses,
        round(win_percentage, 2),
        total_runs,
        total_wickets
    )

    pause()


# ===================================
# OPTION 4
# MATCH ANALYSIS
# ===================================

def match_analysis():

    show_message(
        "Select a match from the available matches below."
    )

    available_matches = matches.head(
        20
    ).copy()

    table_data = []

    for row in available_matches.itertuples(
        index=False
    ):

        table_data.append(
            {
                "Number": len(table_data) + 1,
                "Match ID": row.id,
                "Team 1": row.team1,
                "Team 2": row.team2,
                "Date": row.date
            }
        )

    match_list = pd.DataFrame(
        table_data
    )

    show_dataframe(
        match_list,
        "Available Matches"
    )

    try:

        choice = int(
            input(
                "\nEnter match number: "
            )
        )

    except ValueError:

        show_error(
            "Please enter a valid match number."
        )

        pause()

        return

    if (
        choice < 1
        or
        choice > len(available_matches)
    ):

        show_error(
            "Invalid match number."
        )

        pause()

        return

    selected_row = available_matches.iloc[
        choice - 1
    ]

    match_id = selected_row["id"]

    details = get_match_details(
        matches,
        match_id
    )

    if details is not None:

        details_data = {
            "Match ID": match_id,

            "Team 1": details.get(
                "team1",
                "Unknown"
            ),

            "Team 2": details.get(
                "team2",
                "Unknown"
            ),

            "Date": details.get(
                "date",
                "Unknown"
            ),

            "Venue": details.get(
                "venue",
                "Unknown"
            ),

            "Winner": details.get(
                "winner",
                "Unknown"
            ),

            "Man of the Match": details.get(
                "player_of_match",
                "Unknown"
            )
        }

        details_df = pd.DataFrame(
            [details_data]
        )

        show_dataframe(
            details_df,
            "Match Details"
        )

    best_batsman = get_best_batsman(
        deliveries,
        match_id
    )

    if best_batsman is not None:

        player, runs = best_batsman

        show_message(
            f"Best Batsman: {player} ({runs} runs)"
        )

    best_bowler = get_best_bowler(
        deliveries,
        match_id
    )

    if best_bowler is not None:

        player, wickets = best_bowler

        show_message(
            f"Best Bowler: {player} ({wickets} wickets)"
        )

    scorecard = get_match_scorecard(
        deliveries,
        match_id
    )

    if scorecard is not None:

        show_dataframe(
            scorecard,
            "Match Scorecard"
        )

    pause()


# ===================================
# OPTION 5
# VENUE ANALYSIS
# ===================================

def venue_analysis():

    show_message(
        "Select a venue from the available venues below."
    )

    venues = (
        matches["venue"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    if venues.empty:

        show_error(
            "No venues found in the dataset."
        )

        pause()

        return

    venue_data = []

    for index, venue in enumerate(
        venues,
        start=1
    ):

        venue_data.append(
            {
                "Number": index,
                "Venue": venue
            }
        )

    venue_list = pd.DataFrame(
        venue_data
    )

    show_dataframe(
        venue_list,
        "Available Venues"
    )

    try:

        choice = int(
            input(
                "\nEnter venue number: "
            )
        )

    except ValueError:

        show_error(
            "Please enter a valid venue number."
        )

        pause()

        return

    if (
        choice < 1
        or
        choice > len(venues)
    ):

        show_error(
            "Invalid venue number."
        )

        pause()

        return

    venue = venues.iloc[
        choice - 1
    ]

    total_matches = get_venue_matches(
        matches,
        venue
    )

    total_wins = get_venue_wins(
        matches,
        venue
    )

    total_runs = get_venue_runs(
        deliveries,
        matches,
        venue
    )

    average_runs = get_venue_average_runs(
        deliveries,
        matches,
        venue
    )

    common_team = get_most_common_team(
        deliveries,
        matches,
        venue
    )

    analysis = pd.DataFrame(
        {
            "Statistic": [
                "Matches Played",
                "Total Runs",
                "Average Runs per Match",
                "Matches with Recorded Winner",
                "Most Common Team"
            ],

            "Value": [
                total_matches,
                total_runs,
                average_runs,
                total_wins,
                common_team
            ]
        }
    )

    show_dataframe(
        analysis,
        f"Venue Analysis - {venue}"
    )

    pause()


# ===================================
# OPTION 6
# PERFORMANCE TRENDS
# ===================================

def performance_trends():

    show_message(
        "Select a Performance Trends option."
    )

    print(
        "\n1. Team Season Performance"
    )

    print(
        "2. Player Season Runs"
    )

    print(
        "3. Team Season Runs"
    )

    choice = input(
        "\nEnter choice: "
    )

    if choice == "1":

        team = search_team(
            matches
        )

        if team is None:
            return

        result = get_team_season_performance(
            matches,
            team
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            f"{team} - Season Performance"
        )

    elif choice == "2":

        player = search_player(
            deliveries
        )

        if player is None:
            return

        result = get_player_season_runs(
            deliveries,
            matches,
            player
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            f"{player} - Season Runs"
        )

    elif choice == "3":

        team = search_team(
            matches
        )

        if team is None:
            return

        result = get_team_season_runs(
            deliveries,
            matches,
            team
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            f"{team} - Season Runs"
        )

    else:

        show_error(
            "Invalid choice."
        )

    pause()


# ===================================
# OPTION 7
# TOP PERFORMERS
# ===================================

def top_performers():

    show_message(
        "Select a Top Performers option."
    )

    print(
        "\n1. Top Run Scorers"
    )

    print(
        "2. Top Wicket Takers"
    )

    print(
        "3. Most Sixes"
    )

    print(
        "4. Most Fours"
    )

    choice = input(
        "\nEnter choice: "
    )

    if choice == "1":

        result = get_top_run_scorers(
            deliveries
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            "Top Run Scorers"
        )

    elif choice == "2":

        result = get_top_wicket_takers(
            deliveries
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            "Top Wicket Takers"
        )

    elif choice == "3":

        result = get_most_sixes(
            deliveries
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            "Most Sixes"
        )

    elif choice == "4":

        result = get_most_fours(
            deliveries
        )

        result_df = pd.DataFrame(
            result
        )

        show_dataframe(
            result_df,
            "Most Fours"
        )

    else:

        show_error(
            "Invalid choice."
        )

    pause()


# ===================================
# OPTION 8
# VISUALIZATIONS
# ===================================

def visualizations():

    show_message(
        "Select a visualization from the available graphs."
    )

    from src.visualizations import (
        show_visualizations
    )

    show_visualizations(
        matches,
        deliveries
    )

    pause()


# ===================================
# OPTION 9
# DATASET SUMMARY
# ===================================

def dataset_summary():

    result = get_dataset_summary(
        matches,
        deliveries
    )

    if isinstance(
        result,
        pd.DataFrame
    ):

        show_dataframe(
            result,
            "Dataset Summary"
        )

    elif isinstance(
        result,
        dict
    ):

        summary_df = pd.DataFrame(
            {
                "Statistic": result.keys(),
                "Value": result.values()
            }
        )

        show_dataframe(
            summary_df,
            "Dataset Summary"
        )

    else:

        show_message(
            result
        )

    pause()


# ===================================
# MAIN PROGRAM
# ===================================

show_header()

while True:

    show_menu()

    choice = get_menu_choice()

    if choice == "1":

        player_analysis()

    elif choice == "2":

        player_comparison()

    elif choice == "3":

        team_analysis()

    elif choice == "4":

        match_analysis()

    elif choice == "5":

        venue_analysis()

    elif choice == "6":

        performance_trends()

    elif choice == "7":

        top_performers()

    elif choice == "8":

        visualizations()

    elif choice == "9":

        dataset_summary()

    elif choice == "0":

        show_success(
            "Thank you for using "
            "Cricket Performance Analysis System!"
        )

        break

    else:

        show_error(
            "Invalid choice. "
            "Please select an option from 0 to 9."
        )