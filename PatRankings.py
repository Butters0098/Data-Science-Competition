import pandas as pd

df = pd.read_csv("Games 2022.csv")  
region_df = pd.read_csv("Team Region Groups.csv")

df["team_score_calc"] = (
    (2 * df["FGM_2"]) - (0.5 * (df["FGA_2"] - df["FGM_2"])) +
    (3 * df["FGM_3"]) - (0.5 * (df["FGA_3"] - df["FGM_3"])) +
    (1 * df["FTM"]) - (0.5 * (df["FTA"] - df["FTM"])) +
    (1.5 * (df["OREB"] + df["DREB"])) +
    (2 * df["AST"]) + (3 * df["STL"]) + (2 * df["BLK"]) -
    (2 * df["TOV"]) - (1 * df["F_personal"])
)

avg_team_rankings = df.groupby("team")["team_score_calc"].mean().reset_index()

avg_team_rankings = avg_team_rankings.sort_values(by="team_score_calc", ascending=False).reset_index(drop=True)
avg_team_rankings["Rank"] = avg_team_rankings.index + 1

avg_ranked_teams_with_region = avg_team_rankings.merge(region_df, on="team", how="inner")

avg_team_rankings = avg_team_rankings.to_dict()


rankings = {}


for i in range(len(avg_team_rankings["team"])):
    rankings.update({avg_team_rankings["team"][i]:avg_team_rankings["team_score_calc"][i]})
