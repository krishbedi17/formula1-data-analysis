import os
import pandas as pd

# File paths for race and new pit stop data
years = [2018, 2019, 2020, 2021, 2022]
race_file_paths = [f"race_data/{year}_race_results.csv" for year in years]
pit_stop_file_path = f"pit_stops_average_data/2018_pit_stops_average.csv"

team_collision_counts = {}
team_total_races = {}
pit_stop_stats = {}

for file_path in race_file_paths:
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)

        print(f"Processing file: {file_path}")
        data['Status'] = data['Status'].str.lower()

        valid_data = data[~data['Status'].str.contains('collision|accident|finished|lap', na=False)]

        for team in valid_data['Constructor ID'].unique():
            team_race_count = valid_data[valid_data['Constructor ID'] == team].shape[0]
            total_race_count = data[data['Constructor ID'] == team].shape[0]
            if team in team_collision_counts:
                team_collision_counts[team] += team_race_count
                team_total_races[team] += total_race_count
            else:
                team_collision_counts[team] = team_race_count
                team_total_races[team] = total_race_count
    else:
        print(f"File {file_path} not found!")

if os.path.exists(pit_stop_file_path):
    pit_stop_data = pd.read_csv(pit_stop_file_path)
    print(f"Processing pit stop file: {pit_stop_file_path}")

    if 'Driver ID' in pit_stop_data.columns and 'Average Duration' in pit_stop_data.columns:
        for driver_id in pit_stop_data['Driver ID'].unique():
            driver_pit_data = pit_stop_data[pit_stop_data['Driver ID'] == driver_id]

            driver_row = data[data['Driver ID'] == driver_id]
            if not driver_row.empty:
                team = driver_row['Constructor ID'].iloc[0]

                avg_pit_stop_duration = driver_pit_data['Average Duration'].iloc[0]

                if team in pit_stop_stats:
                    pit_stop_stats[team]['total_pit_stops'] += 1
                    pit_stop_stats[team]['total_pit_time'] += avg_pit_stop_duration
                else:
                    pit_stop_stats[team] = {
                        'total_pit_stops': 1,
                        'total_pit_time': avg_pit_stop_duration
                    }
    else:
        print(f"Required columns not found in {pit_stop_file_path}. Skipping this file.")
else:
    print(f"Pit stop data file {pit_stop_file_path} not found!")

team_probability_of_error = {}

for team in team_collision_counts:
    total_races = team_total_races.get(team, 0)
    problematic_races = team_collision_counts.get(team, 0)

    pit_stops = pit_stop_stats.get(team, {'total_pit_stops': 0, 'total_pit_time': 0})
    avg_pit_time = pit_stops['total_pit_time'] / pit_stops['total_pit_stops'] if pit_stops['total_pit_stops'] > 0 else 0

    error_from_races = problematic_races / total_races if total_races > 0 else 0
    pit_stop_penalty = avg_pit_time / 20.0

    team_probability_of_error[team] = 1 - error_from_races

team_probability_df = pd.DataFrame(
    [
        {'Constructor ID': team, 'Probability_of_Error': probability,
         'Avg_Pit_Stop_Time': pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})['total_pit_time'] /
                              pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})[
                                  'total_pit_stops'] if
         pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})['total_pit_stops'] > 0 else 0}
        for team, probability in team_probability_of_error.items()
    ]
)

print(team_probability_df)

team_probability_df.to_csv('race_error/team_error_probabilities.csv', index=False)
