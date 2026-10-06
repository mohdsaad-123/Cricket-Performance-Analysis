def get_dataset_summary(matches, deliveries):

    summary = {
        "Total Matches": matches["id"].nunique(),
        "Total Deliveries": len(deliveries),
        "Total Seasons": matches["season"].nunique(),
        "Total Teams": len(
            set(matches["team1"]) | set(matches["team2"])
        ),
        "Total Venues": matches["venue"].nunique(),
        "Total Players": len(
            set(deliveries["batter"]) |
            set(deliveries["bowler"])
        ),
        "Total Runs": deliveries["total_runs"].sum(),
        "Total Wickets": deliveries["is_wicket"].sum()
    }

    return summary