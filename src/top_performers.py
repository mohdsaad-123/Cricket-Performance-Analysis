def get_top_run_scorers(deliveries, top_n=10):

    runs = (
        deliveries
        .groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    runs.columns = [
        "Player",
        "Runs"
    ]

    return runs


def get_top_wicket_takers(deliveries, top_n=10):

    wickets = deliveries[
        (deliveries["is_wicket"] == 1) &
        (~deliveries["dismissal_kind"].isin(
            [
                "run out",
                "retired hurt",
                "obstructing the field"
            ]
        ))
    ]

    wicket_counts = (
        wickets
        .groupby("bowler")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    wicket_counts.columns = [
        "Player",
        "Wickets"
    ]

    return wicket_counts


def get_most_sixes(deliveries, top_n=10):

    sixes = deliveries[
        deliveries["batsman_runs"] == 6
    ]

    six_counts = (
        sixes
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    six_counts.columns = [
        "Player",
        "Sixes"
    ]

    return six_counts


def get_most_fours(deliveries, top_n=10):

    fours = deliveries[
        deliveries["batsman_runs"] == 4
    ]

    four_counts = (
        fours
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    four_counts.columns = [
        "Player",
        "Fours"
    ]

    return four_counts