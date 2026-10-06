def find_players(deliveries, query=""):
    players = sorted(set(deliveries["batter"].dropna()))
    query = query.strip().lower()
    return [player for player in players if query in player.lower()]


def find_teams(matches, query=""):
    teams = sorted(
        set(matches["team1"].dropna()) |
        set(matches["team2"].dropna())
    )
    query = query.strip().lower()
    return [team for team in teams if query in team.lower()]


def find_venues(matches, query=""):
    venues = sorted(set(matches["venue"].dropna()))
    query = query.strip().lower()
    return [venue for venue in venues if query in venue.lower()]
