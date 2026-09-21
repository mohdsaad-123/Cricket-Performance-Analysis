import matplotlib.pyplot as plt


# ===================================
# TOP RUN SCORERS
# ===================================

def show_top_run_scorers(deliveries):

    runs = (
        deliveries
        .groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    runs.plot(
        kind="bar"
    )

    plt.title(
        "Top 10 Run Scorers"
    )

    plt.xlabel(
        "Player"
    )

    plt.ylabel(
        "Runs"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ===================================
# TOP WICKET TAKERS
# ===================================

def show_top_wicket_takers(deliveries):

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
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    wicket_counts.plot(
        kind="bar"
    )

    plt.title(
        "Top 10 Wicket Takers"
    )

    plt.xlabel(
        "Player"
    )

    plt.ylabel(
        "Wickets"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ===================================
# MOST SIXES
# ===================================

def show_most_sixes(deliveries):

    sixes = deliveries[
        deliveries["batsman_runs"] == 6
    ]

    six_counts = (
        sixes
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    six_counts.plot(
        kind="bar"
    )

    plt.title(
        "Top 10 Players by Sixes"
    )

    plt.xlabel(
        "Player"
    )

    plt.ylabel(
        "Sixes"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ===================================
# MOST FOURS
# ===================================

def show_most_fours(deliveries):

    fours = deliveries[
        deliveries["batsman_runs"] == 4
    ]

    four_counts = (
        fours
        .groupby("batter")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    four_counts.plot(
        kind="bar"
    )

    plt.title(
        "Top 10 Players by Fours"
    )

    plt.xlabel(
        "Player"
    )

    plt.ylabel(
        "Fours"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ===================================
# TEAM RUNS
# ===================================

def show_team_runs(deliveries):

    team_runs = (
        deliveries
        .groupby("batting_team")["total_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))

    team_runs.plot(
        kind="bar"
    )

    plt.title(
        "Top Teams by Total Runs"
    )

    plt.xlabel(
        "Team"
    )

    plt.ylabel(
        "Runs"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ===================================
# VISUALIZATION MENU
# ===================================

def show_visualizations(
    matches,
    deliveries
):

    while True:

        print(
            "\n========== VISUALIZATIONS =========="
        )

        print(
            "1. Top Run Scorers"
        )

        print(
            "2. Top Wicket Takers"
        )

        print(
            "3. Most Sixes"
        )

        print(
            "4. Most Fours"
        )

        print(
            "5. Team Total Runs"
        )

        print(
            "0. Return to Main Menu"
        )

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            show_top_run_scorers(
                deliveries
            )

        elif choice == "2":

            show_top_wicket_takers(
                deliveries
            )

        elif choice == "3":

            show_most_sixes(
                deliveries
            )

        elif choice == "4":

            show_most_fours(
                deliveries
            )

        elif choice == "5":

            show_team_runs(
                deliveries
            )

        elif choice == "0":

            break

        else:

            print(
                "\nInvalid choice."
            )