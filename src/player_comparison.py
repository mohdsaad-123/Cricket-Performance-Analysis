def compare_players(deliveries, player1, player2):

    players = [player1, player2]

    comparison = []

    for player in players:

        player_data = deliveries[
            deliveries["batter"] == player
        ]

        runs = player_data["batsman_runs"].sum()

        matches = player_data["match_id"].nunique()

        dismissals = player_data[
            player_data["player_dismissed"] == player
        ].shape[0]

        if dismissals == 0:
            average = runs
        else:
            average = runs / dismissals

        balls_faced = player_data[
            player_data["extras_type"] != "wides"
        ].shape[0]

        if balls_faced == 0:
            strike_rate = 0
        else:
            strike_rate = (runs / balls_faced) * 100

        fours = (
            player_data["batsman_runs"] == 4
        ).sum()

        sixes = (
            player_data["batsman_runs"] == 6
        ).sum()

        comparison.append({
            "player": player,
            "matches": matches,
            "runs": runs,
            "average": round(average, 2),
            "strike_rate": round(strike_rate, 2),
            "fours": fours,
            "sixes": sixes
        })

    return comparison