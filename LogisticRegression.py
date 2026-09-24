import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import csv
import TeamStats
from EloModel import elo_dict  
from MatchupStats import games

c_scores = []

x = []
y = []

with open("Games 2022 wins.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    
    while True:
        try:
            row = next(csv_reader) # Team 1 stats
            row2 = next(csv_reader) # Team 2 stats
            stats = TeamStats.team_stats(row[2],row2[2])
            y.append(int(row[3])) # Binary Team 1 Wins
            x.append(stats)
            
        except StopIteration:
            break

x = np.array(x)
y = np.array(y)

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

x_train = x
x_test = x

y_train = y
y_test = y

# Solver options: 'liblinear', newton-cg', 'lbfgs', 'sag', and 'saga'
model = LogisticRegression(solver="liblinear", penalty="l1",random_state=0, max_iter=1000)
model.fit(x_train , y_train)

from sklearn.calibration import CalibratedClassifierCV

model = CalibratedClassifierCV(model, cv=5, method='sigmoid')  
model.fit(x_train, y_train)

p_pred = model.predict_proba(x_test)
y_pred = model.predict(x_test)
score_ = model.score(x_test , y_test)
conf_m = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(report)
print(score_)
cm = confusion_matrix(y_test, model.predict(x_test))

print(cm)


from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve, auc, accuracy_score, roc_auc_score

scores = cross_val_score(model, x_train, y_train, cv=10, scoring='accuracy')
print(f"Average Cross-Validation Score: {scores.mean():.4f}")


from scipy.stats import chi2

from EloModel import elo_dict

chi_squared_total = 0
degrees_of_freedom = 0

prob = model.predict_proba([TeamStats.team_stats("rhode_island_rams" , "north_carolina_tar_heels")])
print(prob[0][1], prob[0][0])
# Returns [a,b], if [team1, team2], then a is the probability that team1 loses and b is the probability that team1 wins 
prob = model.predict_proba([TeamStats.team_stats("nc_state_wolfpack" , "rhode_island_rams")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("nc_state_wolfpack" , "north_carolina_tar_heels")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("liberty_flames" , "bucknell_bison")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("drexel_dragons" , "delaware_blue_hens")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("massachusetts_minutewomen" , "princeton_tigers")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("buffalo_bulls" , "stony_brook_seawolves")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("fairfield_stags" , "towson_tigers")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("uconn_huskies" , "campbell_fighting_camels")])
print(prob[0][1], prob[0][0])
prob = model.predict_proba([TeamStats.team_stats("american_university_eagles" , "columbia_lions")])
print(prob[0][1], prob[0][0])

print(report)

alpha = 0.83

def predict_combined(team, opponent, model, alpha=0.83):

    rating_team = elo_dict[team]
    rating_opponent = elo_dict[opponent]
    p_elo = 1 / (1 + 10 ** ((rating_opponent - rating_team) / 400))
    
    p_logistic = model.predict_proba([TeamStats.team_stats(team, opponent)])[0][1]
    
    p_combined = alpha * p_elo + (1 - alpha) * p_logistic
    return p_combined, p_elo, p_logistic

y_pred_combined = []

with open("Games 2022 wins.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    
    while True:
        try:
            row = next(csv_reader) # Team 1 stats
            row2 = next(csv_reader) # Team 2 stats
            stats = TeamStats.team_stats(row[2],row2[2])
            p_combined, _, _ = predict_combined(row[2], row2[2], model)
            y_pred_combined.append(1 if p_combined > 0.5 else 0)
        except StopIteration:
            break
    

# Generate and print the classification report
report_combined = classification_report(y_test, y_pred_combined)
print("Combined Model Classification Report:\n", report_combined)

# Generate and print the confusion matrix
cm_combined = confusion_matrix(y_test, y_pred_combined)
print("Combined Model Confusion Matrix:\n", cm_combined)

# Generate and print the accuracy score
accuracy_combined = accuracy_score(y_test, y_pred_combined)
print("Combined Model Accuracy:", accuracy_combined)

from sklearn.model_selection import KFold
import numpy as np

# Define a function to perform cross-validation on the combined model
def cross_validate_combined_model(x, y, model, n_splits=10, alpha=0.83):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    cv_scores = []
    
    team_pairs = []
    # Extract team pairs from your data source
    with open("Games 2022 wins.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        
        while True:
            try:
                row = next(csv_reader)  # Team 1 stats
                row2 = next(csv_reader)  # Team 2 stats
                team_pairs.append((row[2], row2[2]))  # Store team names
            except StopIteration:
                break
    
    # Perform k-fold cross-validation
    for train_index, test_index in kf.split(x):
        # Train the logistic regression model on the training fold
        x_train_fold, x_test_fold = x[train_index], x[test_index]
        y_train_fold, y_test_fold = y[train_index], y[test_index]
        
        # Fit the logistic regression model
        model_fold = CalibratedClassifierCV(LogisticRegression(solver="liblinear", penalty="l1", 
                                         random_state=0, max_iter=1000), 
                                         cv=5, method='sigmoid')
        model_fold.fit(x_train_fold, y_train_fold)
        
        # Get the test pairs
        test_pairs = [team_pairs[i] for i in test_index]
        
        # Make predictions using the combined model
        y_pred_fold = []
        for team, opponent in test_pairs:
            p_combined, _, _ = predict_combined(team, opponent, model_fold, alpha)
            y_pred_fold.append(1 if p_combined > 0.5 else 0)
        
        # Calculate accuracy for this fold
        accuracy = accuracy_score(y_test_fold, y_pred_fold)
        cv_scores.append(accuracy)
    
    return cv_scores

# Run cross-validation
cv_scores_combined = cross_validate_combined_model(x, y, model)

# Print results
print(f"Cross-validation scores for combined model: {cv_scores_combined}")
print(f"Average cross-validation score: {np.mean(cv_scores_combined):.4f}")
print(f"Standard deviation of CV scores: {np.std(cv_scores_combined):.4f}")

matchups = [
    ("rhode_island_rams", "north_carolina_tar_heels"),
    ("nc_state_wolfpack", "rhode_island_rams"),
    ("nc_state_wolfpack", "north_carolina_tar_heels"),
    ("liberty_flames", "bucknell_bison"),
    ("drexel_dragons", "delaware_blue_hens"),
    ("massachusetts_minutewomen", "princeton_tigers"),
    ("buffalo_bulls", "stony_brook_seawolves"),
    ("fairfield_stags", "towson_tigers"),
    ("uconn_huskies", "campbell_fighting_camels"),
    ("american_university_eagles", "columbia_lions")
]

# Evaluate and print the combined probabilities for each matchup.
print("Combined Model Predictions (alpha = 0.83):\n")
for team, opponent in matchups:
    p_comb, p_elo, p_log = predict_combined(team, opponent, model, alpha=alpha)
    print(f"{team} vs {opponent}:")
    print(f"  Combined win probability for {team}: {p_comb * 100:.2f}%")
    print(f"  ELO win probability:                  {p_elo * 100:.2f}%")
    print(f"  Logistic win probability:             {p_log * 100:.2f}%\n")

alpha = 0.83

def predict_combined(team, opponent, model, alpha=0.83):

    rating_team = elo_dict[team]
    rating_opponent = elo_dict[opponent]
    p_elo = 1 / (1 + 10 ** ((rating_opponent - rating_team) / 400))
    
    p_logistic = model.predict_proba([TeamStats.team_stats(team, opponent)])[0][1]
    
    p_combined = alpha * p_elo + (1 - alpha) * p_logistic
    return p_combined

y_true = []
y_pred_probs = []

with open("Games 2022 wins.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header row.

    while True:
        try:
            row1 = next(reader)   # Team 1's data
            row2 = next(reader)   # Team 2's data
        except StopIteration:
            break
        
        team1 = row1[2]
        team2 = row2[2]
        true_outcome = int(row1[3]) 
        
        y_true.append(true_outcome)
        
        prob = predict_combined(team1, team2, model, alpha=alpha)
        y_pred_probs.append(prob)

y_true = np.array(y_true)
y_pred_probs = np.array(y_pred_probs)

y_pred = (y_pred_probs >= 0.5).astype(int)

accuracy = accuracy_score(y_true, y_pred)
conf_matrix = confusion_matrix(y_true, y_pred)
class_report = classification_report(y_true, y_pred)
roc_auc = roc_auc_score(y_true, y_pred_probs)
fpr, tpr, thresholds = roc_curve(y_true, y_pred_probs)


print("Accuracy:", accuracy)
print("\nConfusion Matrix:\n", conf_matrix)
print("\nClassification Report:\n", class_report)
print("ROC AUC:", roc_auc)

roc_auc = auc(fpr, tpr)

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import defaultdict
import csv

def predict_combined(team, opponent, model, alpha=0.83):
    rating_team = elo_dict[team]
    rating_opponent = elo_dict[opponent]
    p_elo = 1 / (1 + 10 ** ((rating_opponent - rating_team) / 400))
    p_logistic = model.predict_proba([TeamStats.team_stats(team, opponent)])[0][1]
    p_combined = alpha * p_elo + (1 - alpha) * p_logistic
    return p_combined

def calculate_model_win_rates(teams, model, alpha=0.83):
    team_stats = defaultdict(lambda: {'predicted_wins': 0, 'games': 0})
    
    for team in teams:
        for opponent in teams:
            if team == opponent:
                continue
            
            team_stats[team]['games'] += 1
            win_prob = predict_combined(team, opponent, model, alpha)
            team_stats[team]['predicted_wins'] += win_prob
    
    win_rates = {
        team: stats['predicted_wins'] / stats['games'] if stats['games'] > 0 else 0
        for team, stats in team_stats.items()
    }
    
    ranked_teams = sorted(win_rates.items(), key=lambda x: x[1], reverse=True)
    return ranked_teams

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
ranked_teams = calculate_model_win_rates(teams, model, alpha=0.83)

regions = ["North", "South", "West"]
for region in regions:
    for (team, win_rate) in ranked_teams:
        if team in list(team_region.keys()) and region == team_region[team]:
            print(team, win_rate, region)
print("Team Rankings by Model-Predicted Win Rate:")

