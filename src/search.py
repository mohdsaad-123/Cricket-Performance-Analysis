
def search_player(deliveries):

    players = sorted(
        set(deliveries["batter"].dropna())
    )

    while True:

        search = input(
            "\nSearch player name: "
        ).strip().lower()

        results = [
            player
            for player in players
            if search in player.lower()
        ]

        if not results:
            print("\nNo players found. Try again.")
            continue

        print("\nMatching Players")
        print("-------------------------")

        for i, player in enumerate(results, start=1):
            print(f"{i}. {player}")

        while True:

            choice = input(
                "\nSelect player number: "
            ).strip()

            try:

                choice = int(choice)

                if 1 <= choice <= len(results):
                    return results[choice - 1]

                print(
                    f"\nPlease enter a number between 1 and {len(results)}."
                )

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )


def search_team(matches):

    teams = sorted(
        set(matches["team1"].dropna()) |
        set(matches["team2"].dropna())
    )

    while True:

        search = input(
            "\nSearch team name: "
        ).strip().lower()

        results = [
            team
            for team in teams
            if search in team.lower()
        ]

        if not results:
            print("\nNo teams found. Try again.")
            continue

        print("\nMatching Teams")
        print("-------------------------")

        for i, team in enumerate(results, start=1):
            print(f"{i}. {team}")

        while True:

            choice = input(
                "\nSelect team number: "
            ).strip()

            try:

                choice = int(choice)

                if 1 <= choice <= len(results):
                    return results[choice - 1]

                print(
                    f"\nPlease enter a number between 1 and {len(results)}."
                )

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )


def search_venue(matches):

    venues = sorted(
        set(matches["venue"].dropna())
    )

    while True:

        search = input(
            "\nSearch venue name: "
        ).strip().lower()

        results = [
            venue
            for venue in venues
            if search in venue.lower()
        ]

        if not results:
            print("\nNo venues found. Try again.")
            continue

        print("\nMatching Venues")
        print("-------------------------")

        for i, venue in enumerate(results, start=1):
            print(f"{i}. {venue}")

        while True:

            choice = input(
                "\nSelect venue number: "
            ).strip()

            try:

                choice = int(choice)

                if 1 <= choice <= len(results):
                    return results[choice - 1]

                print(
                    f"\nPlease enter a number between 1 and {len(results)}."
                )

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )


