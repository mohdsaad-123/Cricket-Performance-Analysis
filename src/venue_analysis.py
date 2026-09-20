def get_venue_matches(matches, venue):
    venue_data = matches[matches["venue"] == venue]

    return len(venue_data)


def get_venue_wins(matches, venue, team):
    venue_data = matches[
        (matches["venue"] == venue) &
        (matches["winner"] == team)
    ]

    return len(venue_data)


def get_venue_teams(matches, venue):
    venue_data = matches[matches["venue"] == venue]

    teams = set(venue_data["team1"]) | set(venue_data["team2"])

    return list(teams)


def get_venue_total_runs(deliveries, matches, venue):
    venue_matches = matches[matches["venue"] == venue]

    match_ids = venue_matches["id"]

    venue_deliveries = deliveries[
        deliveries["match_id"].isin(match_ids)
    ]

    return venue_deliveries["total_runs"].sum()