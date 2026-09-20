def get_top_run_scorers(deliveries, top_n=10):

    top_scorers = (
        deliveries
        .groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    top_scorers.columns = ["player", "runs"]

    return top_scorers


def get_top_wicket_takers(deliveries, top_n=10):

    wickets = deliveries[
        deliveries["is_wicket"] == 1
    ]

    top_wicket_takers = (
        wickets
        .groupby("bowler")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="wickets")
    )

    return top_wicket_takers


def get_top_sixes(deliveries, top_n=10):

    sixes = deliveries[
        deliveries["batsman_runs"] == 6
    ]

    top_six_hitters = (
        sixes
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="sixes")
    )

    return top_six_hitters


def get_top_fours(deliveries, top_n=10):

    fours = deliveries[
        deliveries["batsman_runs"] == 4
    ]

    top_four_hitters = (
        fours
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="fours")
    )

    return top_four_hitters