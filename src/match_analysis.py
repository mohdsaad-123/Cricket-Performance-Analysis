def get_match_details(matches, match_id):
    match = matches[matches["id"] == match_id]

    if match.empty:
        return None

    return match.iloc[0]


def get_match_winner(matches, match_id):
    match = matches[matches["id"] == match_id]

    if match.empty:
        return None

    return match.iloc[0]["winner"]


def get_match_venue(matches, match_id):
    match = matches[matches["id"] == match_id]

    if match.empty:
        return None

    return match.iloc[0]["venue"]


def get_match_scorecard(deliveries, match_id):
    match_data = deliveries[
        deliveries["match_id"] == match_id
    ]

    if match_data.empty:
        return None

    scorecard = (
        match_data
        .groupby("batting_team")["total_runs"]
        .sum()
        .reset_index()
    )

    return scorecard