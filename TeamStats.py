import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import csv

def data(columns: list) -> dict:

    wins = {}
    with open("Games 2022.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            team_name = row[2]  # "team"
            team_score = int(row[18])
            opponent_score = int(row[19])
            
            # Initialize the record if the team isn't already in the dictionary.
            if team_name not in wins:
                wins[team_name] = [0, 0, 0] + [0] * len(columns)
            
            # Update games played
            wins[team_name][0] += 1
            
            # Update wins/draws/losses (losses are implied if not win/draw)
            if team_score > opponent_score:
                wins[team_name][1] += 1
            elif team_score == opponent_score:
                wins[team_name][2] += 1
            # You can choose to store losses separately if desired.
            
            # Update extra columns: 'columns' should list the CSV column indices for extra data.
            for i, col_idx in enumerate(columns):
                try:
                    extra_data = int(row[col_idx])
                except ValueError:
                    extra_data = 0  
                wins[team_name][3 + i] += extra_data

    return wins

def mat_data(wins: dict, columns: list, column_names: list):

    num_plots = len(columns)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))  
    axes = axes.flatten()

    for j, (col_idx, col_name) in enumerate(zip(columns, column_names)):
        x_points, y_points = [], []

        for team in wins.values():
            if team[0] > 10:  
                win_percentage = round(100 * team[1] / team[0], 5)
                avg_extra_data = round(team[3 + j] / (team[0] if team[0] != 0 else 1))  
                x_points.append(win_percentage)
                y_points.append(avg_extra_data)

        # Perform linear regression
        slope, intercept, r, p, std_err = stats.linregress(x_points, y_points)
        
        def regression_func(x):
            return slope * x + intercept

        mymodel = list(map(regression_func, x_points))

        # Plot data
        ax = axes[j]
        ax.scatter(x_points, y_points, label="Data Points", color="blue")
        ax.plot(x_points, mymodel, color='red', label="Regression Line")
        ax.set_xlabel("Win Rate (%)")
        ax.set_ylabel(f"Avg {col_name} Per Game")
        ax.set_title(f"Win Rate vs. {col_name}")
        ax.legend()
        ax.grid(True)

        # Display statistics as text inside the plot
        text_str = (
            f"Correlation (r): {r:.4f}\n"
            f"P-value: {p:.5f}\n"
            f"Std. Error: {std_err:.2f}\n"
            f"Equation: y = {slope:.2f}x + {intercept:.2f}"
        )
        '''sumx2 = 0
        sumx = 0
        sumy2 = 0
        sumy = 0
        sumxy = 0
        if col_name == "FTM":  # Only print debug info for FTM
            print("\nDebug: Win Rate vs. FTM")
            for i in range(len(x_points)):  # Print first 10 pairs
                print(f"Win %: {x_points[i]:.2f}, Avg FTM: {y_points[i]:.2f}")
                sumx2 += x_points[i]**2
                sumx += x_points[i]
                sumy2 += y_points[i]**2
                sumy += y_points[i]
                sumxy += x_points[i]*y_points[i]

            sxx = sumx2 - ((sumx)**2 / len(x_points))
            syy = sumy2 - ((sumy)**2 / len(x_points))
            sxy = sumxy - ((sumx*sumy)/ len(x_points))
            import math
            print(sxy/(math.sqrt(sxx*syy)))
'''
        ax.text(
            0.95, 0.05, text_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
        )

    plt.tight_layout()
    plt.show()

column_and_names = {}
columns_to_analyze = [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]
column_names = ["FGM_2", "FGM_3", "FTM", "STL", "DREB", "F_personal"]
# 39.7, FGM_2, 5.86, 16.08, 11.33, 12.97, 3.18, 7.82, 15.93, 0.69, 25.32, 11.51, 16.42
# [ 3,  4,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 17]
# [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
# [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

wins = data(columns_to_analyze)

from EloModel import elo_dict

for team in wins.items():
    try:
        team[1].append(elo_dict[team[0]])
    except:
        pass

from PatRankings import rankings

for team in wins.items():
    try:
        team[1].append(rankings[team[0]])
    except:
        pass

def team_stats(team_name, team2_name):
    x = []
    for i in range(13):
        x.append(wins[team_name][i+3]/wins[team_name][0])
    #x.append(wins[team_name][8])
    #x.append(wins[team_name][9])
    for i in range(13):
        x.append(wins[team2_name][i+3]/wins[team2_name][0])
    #x.append(wins[team2_name][8])
    #x.append(wins[team2_name][9])
    return x

def team_stats1(team_name):
    x = []
    for i in range(13):
        x.append(wins[team_name][i+3]/wins[team_name][0])
    return x

def more_than_3():
    x = []
    for team in wins.items():
        if team[1][0] > 3:
            x.append(team[0])
    return x
