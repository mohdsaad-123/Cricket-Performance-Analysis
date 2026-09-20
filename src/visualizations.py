import matplotlib.pyplot as plt


def plot_player_season_runs(performance, player):

    plt.figure(figsize=(10, 5))

    plt.plot(
        performance["season"],
        performance["batsman_runs"],
        marker="o"
    )

    plt.title(f"{player} - Season-wise Runs")
    plt.xlabel("Season")
    plt.ylabel("Runs")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_team_season_runs(performance, team):

    plt.figure(figsize=(10, 5))

    plt.plot(
        performance["season"],
        performance["total_runs"],
        marker="o"
    )

    plt.title(f"{team} - Season-wise Runs")
    plt.xlabel("Season")
    plt.ylabel("Runs")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_top_run_scorers(top_scorers):

    plt.figure(figsize=(10, 5))

    plt.bar(
        top_scorers["player"],
        top_scorers["runs"]
    )

    plt.title("Top Run Scorers")
    plt.xlabel("Player")
    plt.ylabel("Runs")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_top_wicket_takers(top_wicket_takers):

    plt.figure(figsize=(10, 5))

    plt.bar(
        top_wicket_takers["bowler"],
        top_wicket_takers["wickets"]
    )

    plt.title("Top Wicket Takers")
    plt.xlabel("Player")
    plt.ylabel("Wickets")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()