import matplotlib.pyplot as plt


def _show_bar_chart(data, title, xlabel, ylabel):
    if data.empty:
        return

    plt.figure(figsize=(10, 5))
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def show_top_run_scorers(deliveries):
    runs = (
        deliveries.groupby("batter")["batsman_runs"]
        .sum().sort_values(ascending=False).head(10)
    )
    _show_bar_chart(runs, "Top 10 Run Scorers", "Player", "Runs")


def show_top_wicket_takers(deliveries):
    wickets = deliveries[
        (deliveries["is_wicket"] == 1) &
        (~deliveries["dismissal_kind"].isin(
            ["run out", "retired hurt", "obstructing the field"]
        ))
    ]
    wicket_counts = (
        wickets.groupby("bowler").size()
        .sort_values(ascending=False).head(10)
    )
    _show_bar_chart(wicket_counts, "Top 10 Wicket Takers", "Player", "Wickets")


def show_most_sixes(deliveries):
    six_counts = (
        deliveries[deliveries["batsman_runs"] == 6]
        .groupby("batter").size()
        .sort_values(ascending=False).head(10)
    )
    _show_bar_chart(six_counts, "Top 10 Players by Sixes", "Player", "Sixes")


def show_most_fours(deliveries):
    four_counts = (
        deliveries[deliveries["batsman_runs"] == 4]
        .groupby("batter").size()
        .sort_values(ascending=False).head(10)
    )
    _show_bar_chart(four_counts, "Top 10 Players by Fours", "Player", "Fours")


def show_team_runs(deliveries):
    team_runs = (
        deliveries.groupby("batting_team")["total_runs"]
        .sum().sort_values(ascending=False).head(10)
    )
    _show_bar_chart(team_runs, "Top Teams by Total Runs", "Team", "Runs")
