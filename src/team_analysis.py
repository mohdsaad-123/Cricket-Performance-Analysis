def get_team_matches(matches, team):
    team_matches = matches[
        (matches["team1"] == team) |
        (matches["team2"] == team)
    ]

    return team_matches["id"].nunique()


def get_team_wins(matches, team):
    wins = matches[matches["winner"] == team]

    return len(wins)


def get_team_losses(matches, team):
    team_matches = matches[
        (matches["team1"] == team) |
        (matches["team2"] == team)
    ]

    losses = team_matches[
        (team_matches["winner"].notna()) &
        (team_matches["winner"] != team)
    ]

    return len(losses)


def get_team_win_percentage(matches, team):
    total_matches = get_team_matches(matches, team)
    wins = get_team_wins(matches, team)

    if total_matches == 0:
        return 0

    return (wins / total_matches) * 100


def get_team_runs(deliveries, team):
    team_data = deliveries[
        deliveries["batting_team"] == team
    ]

    return team_data["total_runs"].sum()


def get_team_wickets(deliveries, team):
    team_data = deliveries[
        deliveries["bowling_team"] == team
    ]

    return team_data["is_wicket"].sum()