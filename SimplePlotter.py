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
            team1_name, team2_name = row[2], row[3]
            team1_score, team2_score = int(row[18]), int(row[19])  # Assuming scores are in these columns

            # Initialize teams if not present
            if team1_name not in wins:
                wins[team1_name] = [0, 0, 0] + [0] * len(columns)
            if team2_name not in wins:
                wins[team2_name] = [0, 0, 0] + [0] * len(columns)

            # Update games played
            wins[team1_name][0] += 1
            wins[team2_name][0] += 1

            # Determine winner
            if team1_score > team2_score:
                wins[team1_name][1] += 1
            elif team1_score < team2_score:
                wins[team2_name][1] += 1
            else:
                wins[team1_name][2] += 1
                wins[team2_name][2] += 1

            # Extra data processing (avoid errors if column data is missing)
            for i, col in enumerate(columns):
                try:
                    extra_data = int(row[col])
                except ValueError:
                    extra_data = 0  # Default to 0 if data is missing

                wins[team1_name][3 + i] += extra_data
                wins[team2_name][3 + i] += extra_data

    return wins

def mat_data(wins: dict, columns: list, column_names: list):

    num_plots = len(columns)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))  # 2 rows, 3 columns for 6 plots
    axes = axes.flatten()

    for j, (col_idx, col_name) in enumerate(zip(columns, column_names)):
        x_points, y_points = [], []

        for team in wins.values():
            if team[0] > 10:  # Only consider teams with more than 3 games
                win_percentage = round(100 * team[1] / team[0], 5)
                avg_extra_data = round(team[3 + j] / (team[0] if team[0] != 0 else 1))  # Avoid division by zero
                x_points.append(win_percentage)
                y_points.append(avg_extra_data)

        # Perform linear regression
        slope, intercept, r, p, std_err = stats.linregress(x_points, y_points)
        
        def regression_func(x):
            return slope * x + intercept

        mymodel = list(map(regression_func, x_points))

        # Plot data
        ax = axes[j]
        ax.scatter(x_points, y_points, label="Data Points", color="#053061", marker="x")
        ax.plot(x_points, mymodel, color='red', label="Regression Line")
        ax.set_xlabel("Win Rate (%)")
        ax.set_ylabel(f"Avg {col_name} Per Game")
        ax.set_title(f"Win Rate vs. {col_name}")
        ax.legend()

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
# Columns 4 to 9 correspond to: ["FGA_2", "FGM_2", "FGA_3", "FGM_3", "FTA", "FTM"]
columns = [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]
feature_names = []
with open("Games 2022.csv", "r") as file:
    csv_reader = csv.reader(file)
    row = next(csv_reader)
    for i, name in enumerate(row):
        if i in columns:
            feature_names.append(name)

'''with open("Games 2022.csv", "r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    
    for i in range(20):
        column_and_names.update({i: header[i]})
columns_to_analyze = []
column_names = []
for i in range(15,20):
    columns_to_analyze.append(i)
    column_names.append(column_and_names[i])'''
    
print(columns)
print(columns)
# Run the functions
wins = data(columns)
print(wins)
mat_data(wins, columns[:6], feature_names[:6])

