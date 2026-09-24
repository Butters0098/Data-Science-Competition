import csv

# Dictionary to hold matchup stats for each team.
# Structure:
# {
#   "TeamA": {
#         "OpponentX": {"total_matchups": count, "total_wins": wins},
#         "OpponentY": {"total_matchups": count, "total_wins": wins},
#         ...
#   },
#   "TeamB": { ... },
#   ...
# }
matchup_stats = {}

with open("Games 2022 wins.csv", "r") as file:
    reader = csv.DictReader(file)
    # Process two rows at a time—each pair represents one game
    while True:
        try:
            row1 = next(reader)  # Team 1's stats
            row2 = next(reader)  # Team 2's stats
        except StopIteration:
            break

        # Extract team names and win indicators.
        # Adjust the column names if they differ in your file.
        team1 = row1["team"]
        team2 = row2["team"]
        win1 = int(row1["win"])  # 1 if team1 wins, 0 otherwise
        win2 = int(row2["win"])  # 1 if team2 wins, 0 otherwise

        # Update matchup stats for team1 against team2
        if team1 not in matchup_stats:
            matchup_stats[team1] = {}
        if team2 not in matchup_stats[team1]:
            matchup_stats[team1][team2] = {"total_matchups": 0, "total_wins": 0}
        matchup_stats[team1][team2]["total_matchups"] += 1
        matchup_stats[team1][team2]["total_wins"] += win1

        # Update matchup stats for team2 against team1
        if team2 not in matchup_stats:
            matchup_stats[team2] = {}
        if team1 not in matchup_stats[team2]:
            matchup_stats[team2][team1] = {"total_matchups": 0, "total_wins": 0}
        matchup_stats[team2][team1]["total_matchups"] += 1
        matchup_stats[team2][team1]["total_wins"] += win2

# Create a dictionary to hold only matchups that have more than one game,
# along with the winning percentage for each matchup.
games = {}

for team, opponents in matchup_stats.items():
    temp = []
    for opponent, stats in opponents.items():
        if stats["total_matchups"] > 2:
            win_pct = stats["total_wins"] / stats["total_matchups"]
            temp.append([opponent, stats["total_matchups"], stats["total_wins"], win_pct])
    if temp:
        games[team] = temp

# Print the resulting dictionary in a readable format.
