import os
import pandas as pd

years = [2018, 2019, 2020, 2021, 2022]
file_paths = [f"race_data/{year}_race_results.csv" for year in years]
team_collision_counts = {}
team_total_races = {}

for file_path in file_paths:
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)

        print(f"Processing file: {file_path}")
        # print(data.columns)

        data['Status'] = data['Status'].str.lower()

        valid_data = data[~data['Status'].str.contains('collision|accident|finished|lap', na=False)]

        for team in valid_data['Constructor'].unique():
            team_race_count = valid_data[valid_data['Constructor'] == team].shape[0]
            total_race_count = data[data['Constructor'] == team].shape[0]
            if team in team_collision_counts:
                team_collision_counts[team] += team_race_count
                team_total_races[team] += total_race_count
            else:
                team_collision_counts[team] = team_race_count
                team_total_races[team] = total_race_count
    else:
        print(f"File {file_path} not found!")

team_probability_of_error = {}

for team in team_collision_counts:
    total = team_total_races[team]
    races = team_collision_counts[team]
    if total > 0:
        team_probability_of_error[team] = races / total
    else:
        team_probability_of_error[team] = 0

team_probability_df = pd.DataFrame(list(team_probability_of_error.items()), columns=['Constructor', 'Probability_of_Error'])

# print(team_probability_df)

team_probability_df.to_csv('team_error_probabilities.csv', index=False)
