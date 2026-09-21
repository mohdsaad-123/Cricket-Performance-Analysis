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
    get_player_hundreds
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
    get_match_winner,
    get_match_venue,
    get_match_scorecard
)

from src.venue_analysis import (
    get_venue_matches,
    get_venue_teams,
    get_venue_total_runs
)

from src.performance_trends import (
    get_team_season_performance,
    get_player_season_runs,
    get_team_season_runs
)

from src.top_performers import (
    get_top_run_scorers,
    get_top_wicket_takers,
    get_top_sixes,
    get_top_fours
)

from src.visualizations import (
    plot_player_season_runs,
    plot_team_season_runs,
    plot_top_run_scorers,
    plot_top_wicket_takers
)

from src.dataset_summary import get_dataset_summary

from src.player_comparison import compare_players


# =========================================================
# LOAD DATASET
# =========================================================

matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")


# =========================================================
# CLEAN DATASET
# =========================================================

matches = clean_matches(matches)
deliveries = clean_deliveries(deliveries)


# =========================================================
# BASIC VARIABLES
# =========================================================

player = "V Kohli"

team = "Royal Challengers Bengaluru"

match_id = matches["id"].iloc[0]

venue = matches["venue"].iloc[0]


# =========================================================
# PLAYER ANALYSIS
# =========================================================

print("\nPLAYER ANALYSIS")
print("-------------------------")

print("Player:", player)
print("Total Runs:", get_player_runs(deliveries, player))
print("Matches Played:", get_player_matches(deliveries, player))
print("Batting Average:", round(get_player_average(deliveries, player), 2))
print("Strike Rate:", round(get_player_strike_rate(deliveries, player), 2))
print("Fours:", get_player_fours(deliveries, player))
print("Sixes:", get_player_sixes(deliveries, player))
print("Highest Score:", get_player_highest_score(deliveries, player))
print("50s:", get_player_fifties(deliveries, player))
print("100s:", get_player_hundreds(deliveries, player))


# =========================================================
# TEAM ANALYSIS
# =========================================================

print("\nTEAM ANALYSIS")
print("-------------------------")

print("Team:", team)
print("Matches:", get_team_matches(matches, team))
print("Wins:", get_team_wins(matches, team))
print("Losses:", get_team_losses(matches, team))
print(
    "Win Percentage:",
    round(get_team_win_percentage(matches, team), 2)
)
print("Runs:", get_team_runs(deliveries, team))
print("Wickets:", get_team_wickets(deliveries, team))


# =========================================================
# MATCH ANALYSIS
# =========================================================

print("\nMATCH ANALYSIS")
print("-------------------------")

print("Match ID:", match_id)
print("Winner:", get_match_winner(matches, match_id))
print("Venue:", get_match_venue(matches, match_id))

print("\nScorecard:")
print(get_match_scorecard(deliveries, match_id))


# =========================================================
# VENUE ANALYSIS
# =========================================================

print("\nVENUE ANALYSIS")
print("-------------------------")

print("Venue:", venue)
print("Matches:", get_venue_matches(matches, venue))
print("Teams:", get_venue_teams(matches, venue))
print(
    "Total Runs:",
    get_venue_total_runs(deliveries, matches, venue)
)


# =========================================================
# PERFORMANCE TRENDS
# =========================================================

print("\nPERFORMANCE TRENDS")
print("-------------------------")

print("\nTeam Season Performance:")
print(
    get_team_season_performance(matches, team)
)

print("\nPlayer Season Runs:")
player_season_runs = get_player_season_runs(
    deliveries,
    matches,
    player
)

print(player_season_runs)

print("\nTeam Season Runs:")
team_season_runs = get_team_season_runs(
    deliveries,
    matches,
    team
)

print(team_season_runs)


# =========================================================
# TOP PERFORMERS
# =========================================================

print("\nTOP PERFORMERS")
print("-------------------------")

print("\nTop Run Scorers:")
top_run_scorers = get_top_run_scorers(
    deliveries
)

print(top_run_scorers)

print("\nTop Wicket Takers:")
top_wicket_takers = get_top_wicket_takers(
    deliveries
)

print(top_wicket_takers)

print("\nMost Sixes:")
print(get_top_sixes(deliveries))

print("\nMost Fours:")
print(get_top_fours(deliveries))


# =========================================================
# DATASET SUMMARY
# =========================================================

print("\nDATASET SUMMARY")
print("-------------------------")

dataset_summary = get_dataset_summary(
    matches,
    deliveries
)

for key, value in dataset_summary.items():
    print(f"{key}: {value}")


# =========================================================
# PLAYER COMPARISON
# =========================================================

player1 = "V Kohli"
player2 = "RG Sharma"

print("\nPLAYER COMPARISON")
print("-------------------------")

comparison = compare_players(
    deliveries,
    player1,
    player2
)

comparison_df = pd.DataFrame(comparison)

print(comparison_df)


# =========================================================
# VISUALIZATIONS
# =========================================================

print("\nVISUALIZATIONS")
print("-------------------------")

print("Opening Player Season Runs graph...")
plot_player_season_runs(
    player_season_runs,
    player
)

print("Opening Team Season Runs graph...")
plot_team_season_runs(
    team_season_runs,
    team
)

print("Opening Top Run Scorers graph...")
plot_top_run_scorers(
    top_run_scorers
)

print("Opening Top Wicket Takers graph...")
plot_top_wicket_takers(
    top_wicket_takers
)