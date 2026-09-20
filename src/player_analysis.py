def get_player_runs(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]
    return player_data["batsman_runs"].sum()


def get_player_matches(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]
    return player_data["match_id"].nunique()


def get_player_average(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]

    total_runs = player_data["batsman_runs"].sum()
    dismissals = player_data["player_dismissed"].eq(player).sum()

    if dismissals == 0:
        return total_runs

    return total_runs / dismissals


def get_player_strike_rate(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]

    total_runs = player_data["batsman_runs"].sum()

    balls_faced = player_data[
        player_data["extras_type"] != "wides"
    ].shape[0]

    if balls_faced == 0:
        return 0

    return (total_runs / balls_faced) * 100


def get_player_fours(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]
    return (player_data["batsman_runs"] == 4).sum()


def get_player_sixes(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]
    return (player_data["batsman_runs"] == 6).sum()


def get_player_highest_score(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]

    innings_scores = (
        player_data
        .groupby("match_id")["batsman_runs"]
        .sum()
    )

    if innings_scores.empty:
        return 0

    return innings_scores.max()


def get_player_fifties(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]

    innings_scores = (
        player_data
        .groupby("match_id")["batsman_runs"]
        .sum()
    )

    return ((innings_scores >= 50) & (innings_scores < 100)).sum()


def get_player_hundreds(deliveries, player):
    player_data = deliveries[deliveries["batter"] == player]

    innings_scores = (
        player_data
        .groupby("match_id")["batsman_runs"]
        .sum()
    )

    return (innings_scores >= 100).sum()