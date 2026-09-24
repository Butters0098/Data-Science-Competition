import csv
import matplotlib.pyplot as plt

elo_dict = {}  # {Team Name: Elo}
total = 0
effective = 0

with open("Games 2022.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header

    while True:
        try:
            row1 = next(csv_reader)
            team1_name = row1[2].strip()
            team1_score = int(row1[18])

            row2 = next(csv_reader)
            team2_name = row2[2].strip()
            team2_score = int(row2[18])

            if team1_name not in elo_dict:
                elo_dict[team1_name] = 1500
            if team2_name not in elo_dict:
                elo_dict[team2_name] = 1500

            rating_1 = elo_dict[team1_name]
            rating_2 = elo_dict[team2_name]
            prob_1_win = 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))
            prob_2_win = 1 - prob_1_win

            if team1_score > team2_score:
                s_1, s_2 = 1, 0
            elif team2_score > team1_score:
                s_1, s_2 = 0, 1
            else:
                s_1, s_2 = 0.5, 0.5 

            elo_dict[team1_name] = rating_1 + 33 * (s_1 - prob_1_win)
            elo_dict[team2_name] = rating_2 + 33 * (s_2 - prob_2_win)
        except StopIteration:
            break


with open("Games 2022.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header

    while True:
        try:
            row1 = next(csv_reader)
            team1_name = row1[2]
            team1_score = int(row1[18])

            row2 = next(csv_reader)
            team2_name = row2[2]
            team2_score = int(row2[18])

            if team1_name in elo_dict and team2_name in elo_dict:
                team1_rank = elo_dict[team1_name]
                team2_rank = elo_dict[team2_name]

                if (team1_score > team2_score and team1_rank > team2_rank) or \
                   (team2_score > team1_score and team2_rank > team1_rank):
                    effective += 1
                total += 1
        except StopIteration:
            break


team_region = {}

with open("Team Region Groups.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    
    while True:
        try:
            row = next(csv_reader) 
            team_region.update({row[0]: row[1]})
            
        except StopIteration:
            break
        
teams = list(elo_dict.keys()) 
'''
regions = ["North", "South", "West"]
sorted_teams = sorted(elo_dict.items(), key=lambda x: x[1], reverse=True)  # Sort by Elo rating

for region in regions:
    for team, elo in sorted_teams:
        if team in team_region and team_region[team] == region:
            print(team, elo, region)
            
'''

def calculate_elo_win_percentages(teams):
    model_win_percents = {}

    for team in teams:
        total_games = 0
        total_wins = 0

        for opponent in teams:
            if team == opponent:
                continue  # Skip self-matchups
            
            rating_1 = elo_dict[team1_name]
            rating_2 = elo_dict[team2_name]

            prob = 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))
            total_games += 1
            total_wins += prob  # Sum of predicted win probabilities

        if total_games > 0:
            model_win_percents[team] = total_wins / total_games  # Average predicted win probability

    return model_win_percents
team_win_prob = {}  # {Team Name: (sum of expected win rates, match count)}

with open("Games 2022.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header

    while True:
        try:
            row1 = next(csv_reader)
            team1_name = row1[2].strip()
            team2_name = next(csv_reader)[2].strip()

            if team1_name in elo_dict and team2_name in elo_dict:
                rating_1 = elo_dict[team1_name]
                rating_2 = elo_dict[team2_name]
                prob_1_win = 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))
                prob_2_win = 1 - prob_1_win

                # Store win probabilities for each team
                if team1_name not in team_win_prob:
                    team_win_prob[team1_name] = [0, 0]
                if team2_name not in team_win_prob:
                    team_win_prob[team2_name] = [0, 0]

                team_win_prob[team1_name][0] += prob_1_win
                team_win_prob[team1_name][1] += 1
                team_win_prob[team2_name][0] += prob_2_win
                team_win_prob[team2_name][1] += 1

        except StopIteration:
            break

elo_win_rates = {team: (win_prob[0] / win_prob[1]) for team, win_prob in team_win_prob.items()}

'''rating_1 = elo_dict["american_university_eagles"]
rating_2 = elo_dict["columbia_lions"]
prob_1_win = 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))
print(prob_1_win*100, 100*(1-prob_1_win))
'''
'''
region_elo_dict = {}
with open("Team Region Groups.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    
    while True:
        try:
            row = next(csv_reader)
            region_elo_dict.update({row[0]: [row[1], elo_dict[row[0]]]})

        except StopIteration:
            break
sorted_region_elo_desc = sorted(region_elo_dict.items(), key=lambda item: item[1][1], reverse=True)

# Print the sorted result (as a list of tuples)
print(sorted_region_elo_desc)
        
north = []
for team in region_elo_dict:
    if region_elo_dict[team][0] == "North":
        pass'''