import pandas as pd

def get_venue_matches(matches, venue):

    venue_matches = matches[
        matches["venue"] == venue
    ]

    return len(venue_matches)


def get_venue_wins(matches, venue):

    venue_matches = matches[
        matches["venue"] == venue
    ]

    if venue_matches.empty:
        return 0

    return venue_matches["winner"].notna().sum()


def get_venue_runs(deliveries, matches, venue):

    venue_matches = matches[
        matches["venue"] == venue
    ]

    if venue_matches.empty:
        return 0

    match_ids = venue_matches["id"].tolist()

    venue_deliveries = deliveries[
        deliveries["match_id"].isin(match_ids)
    ]

    if venue_deliveries.empty:
        return 0

    return int(
        venue_deliveries["total_runs"].sum()
    )


def get_venue_average_runs(
    deliveries,
    matches,
    venue
):

    total_matches = get_venue_matches(
        matches,
        venue
    )

    total_runs = get_venue_runs(
        deliveries,
        matches,
        venue
    )

    if total_matches == 0:
        return 0

    return round(
        total_runs / total_matches,
        2
    )


def get_most_common_team(
    deliveries,
    matches,
    venue
):

    venue_matches = matches[
        matches["venue"] == venue
    ]

    if venue_matches.empty:
        return "Unknown"

    teams = pd.concat(
        [
            venue_matches["team1"],
            venue_matches["team2"]
        ]
    )

    if teams.empty:
        return "Unknown"

    return teams.value_counts().idxmax()