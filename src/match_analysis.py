def get_match_details(matches, match_id):

    match = matches[
        matches["id"] == match_id
    ]

    if match.empty:
        return None

    return match.iloc[0]


def get_match_winner(matches, match_id):

    match = matches[
        matches["id"] == match_id
    ]

    if match.empty:
        return None

    return match.iloc[0]["winner"]


def get_match_venue(matches, match_id):

    match = matches[
        matches["id"] == match_id
    ]

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


def get_best_batsman(deliveries, match_id):

    match_data = deliveries[
        deliveries["match_id"] == match_id
    ]

    if match_data.empty:
        return None

    batsman_runs = (
        match_data
        .groupby("batter")["batsman_runs"]
        .sum()
    )

    if batsman_runs.empty:
        return None

    player = batsman_runs.idxmax()
    runs = batsman_runs.max()

    return player, runs


def get_best_bowler(deliveries, match_id):

    match_data = deliveries[
        deliveries["match_id"] == match_id
    ]

    if match_data.empty:
        return None

    wickets = match_data[
        (match_data["is_wicket"] == 1) &
        (~match_data["dismissal_kind"].isin(
            [
                "run out",
                "retired hurt",
                "obstructing the field"
            ]
        ))
    ]

    if wickets.empty:
        return None

    bowler_wickets = (
        wickets
        .groupby("bowler")
        .size()
    )

    player = bowler_wickets.idxmax()
    wicket_count = bowler_wickets.max()

    return player, wicket_count