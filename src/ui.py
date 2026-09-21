from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


# ===================================
# HEADER
# ===================================

def show_header():

    console.print(
        Panel(
            "[bold white]CRICKET PERFORMANCE ANALYSIS SYSTEM[/bold white]\n"
            "[dim]IPL Data Analysis & Performance Insights[/dim]",
            expand=False
        )
    )


# ===================================
# MAIN MENU
# ===================================

def show_menu():

    table = Table(
        title="Main Menu",
        show_header=True
    )

    table.add_column("Option", justify="center")
    table.add_column("Analysis")

    table.add_row("1", "Player Analysis")
    table.add_row("2", "Player Comparison")
    table.add_row("3", "Team Analysis")
    table.add_row("4", "Match Analysis")
    table.add_row("5", "Venue Analysis")
    table.add_row("6", "Performance Trends")
    table.add_row("7", "Top Performers")
    table.add_row("8", "Visualizations")
    table.add_row("9", "Dataset Summary")
    table.add_row("0", "Exit")

    console.print(table)


# ===================================
# GET MENU CHOICE
# ===================================

def get_menu_choice():

    return console.input(
        "\n[bold]Enter your choice:[/bold] "
    )


# ===================================
# PLAYER ANALYSIS
# ===================================

def show_player_analysis(
    player,
    runs,
    matches,
    average,
    strike_rate,
    fours,
    sixes,
    highest_score,
    fifties,
    hundreds
):

    table = Table(
        title=f"Player Analysis - {player}",
        show_header=True
    )

    table.add_column("Statistic")
    table.add_column("Value", justify="center")

    table.add_row("Matches Played", str(matches))
    table.add_row("Total Runs", str(runs))
    table.add_row("Batting Average", str(average))
    table.add_row("Strike Rate", str(strike_rate))
    table.add_row("Fours", str(fours))
    table.add_row("Sixes", str(sixes))
    table.add_row("Highest Score", str(highest_score))
    table.add_row("50s", str(fifties))
    table.add_row("100s", str(hundreds))

    console.print(table)


# ===================================
# TEAM ANALYSIS
# ===================================

def show_team_analysis(
    team,
    matches,
    wins,
    losses,
    win_percentage,
    runs,
    wickets
):

    table = Table(
        title=f"Team Analysis - {team}",
        show_header=True
    )

    table.add_column("Statistic")
    table.add_column("Value", justify="center")

    table.add_row("Matches", str(matches))
    table.add_row("Wins", str(wins))
    table.add_row("Losses", str(losses))
    table.add_row("Win Percentage", str(win_percentage))
    table.add_row("Total Runs", str(runs))
    table.add_row("Wickets", str(wickets))

    console.print(table)


# ===================================
# DATAFRAME TABLE
# ===================================

def show_dataframe(dataframe, title):

    if dataframe is None or dataframe.empty:

        console.print(
            Panel(
                "[yellow]No data available.[/yellow]",
                title=title
            )
        )

        return

    table = Table(
        title=title,
        show_header=True
    )

    for column in dataframe.columns:

        table.add_column(
            str(column)
        )

    for row in dataframe.itertuples(index=False):

        table.add_row(
            *[
                str(value)
                for value in row
            ]
        )

    console.print(table)


# ===================================
# SIMPLE MESSAGE
# ===================================

def show_message(message):

    console.print(
        Panel(
            str(message)
        )
    )


# ===================================
# ERROR MESSAGE
# ===================================

def show_error(message):

    console.print(
        Panel(
            f"[red]{message}[/red]",
            title="Error"
        )
    )


# ===================================
# SUCCESS MESSAGE
# ===================================

def show_success(message):

    console.print(
        Panel(
            f"[green]{message}[/green]"
        )
    )


# ===================================
# RETURN TO MENU
# ===================================

def pause():

    console.input(
        "\n[dim]Press Enter to return to Main Menu...[/dim]"
    )