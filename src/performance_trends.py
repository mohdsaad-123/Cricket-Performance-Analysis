def get_team_season_performance(matches, team):

    team_names = [team]

    if team == "Royal Challengers Bengaluru":
        team_names.append("Royal Challengers Bangalore")

    team_matches = matches[
        matches["team1"].isin(team_names) |
        matches["team2"].isin(team_names)
    ]

    performance = (
        team_matches
        .groupby("season")
        .agg(
            matches=("id", "count"),
            wins=("winner", lambda x: x.isin(team_names).sum())
        )
        .reset_index()
    )

    performance["win_percentage"] = (
        performance["wins"] / performance["matches"] * 100
    )

    return performance


def get_player_season_runs(deliveries, matches, player):

    player_data = deliveries[
        deliveries["batter"] == player
    ]

    player_data = player_data.merge(
        matches[["id", "season"]],
        left_on="match_id",
        right_on="id",
        how="left"
    )

    performance = (
        player_data
        .groupby("season")["batsman_runs"]
        .sum()
        .reset_index()
    )

    return performance


def get_team_season_runs(deliveries, matches, team):

    team_names = [team]

    if team == "Royal Challengers Bengaluru":
        team_names.append("Royal Challengers Bangalore")

    team_data = deliveries[
        deliveries["batting_team"].isin(team_names)
    ]

    team_data = team_data.merge(
        matches[["id", "season"]],
        left_on="match_id",
        right_on="id",
        how="left"
    )

    performance = (
        team_data
        .groupby("season")["total_runs"]
        .sum()
        .reset_index()
    )

    return performance