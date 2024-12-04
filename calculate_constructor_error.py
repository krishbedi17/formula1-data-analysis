import os
import pandas as pd

# File paths for race and new pit stop data
years = [2018, 2019, 2020, 2021, 2022]
race_file_paths = [f"race_data/{year}_race_results.csv" for year in years]
pit_stop_file_path = f"pit_stops_average_data/2018_pit_stops_average.csv"  # New pit stop file

team_collision_counts = {}
team_total_races = {}
pit_stop_stats = {}

# Process race data
for file_path in race_file_paths:
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)

        print(f"Processing file: {file_path}")
        data['Status'] = data['Status'].str.lower()

        # Filter out irrelevant statuses (e.g., finished, lap) to focus on problematic statuses
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

# Process the new pit stop file (Average Duration per Driver)
if os.path.exists(pit_stop_file_path):
    pit_stop_data = pd.read_csv(pit_stop_file_path)
    print(f"Processing pit stop file: {pit_stop_file_path}")

    # Ensure 'Driver ID' and 'Average Duration' columns exist
    if 'Driver ID' in pit_stop_data.columns and 'Average Duration' in pit_stop_data.columns:
        # Link each driver's average pit stop duration with their constructor
        for driver_id in pit_stop_data['Driver ID'].unique():
            driver_pit_data = pit_stop_data[pit_stop_data['Driver ID'] == driver_id]

            # Get the constructor for the driver
            driver_row = data[data['Driver ID'] == driver_id]
            if not driver_row.empty:
                team = driver_row['Constructor'].iloc[0]

                # Add pit stop data to pit_stop_stats dictionary
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

# Calculate probability of error (factoring in pit stops)
team_probability_of_error = {}

for team in team_collision_counts:
    total_races = team_total_races.get(team, 0)
    problematic_races = team_collision_counts.get(team, 0)

    # Adjust error probability using pit stop data if available
    pit_stops = pit_stop_stats.get(team, {'total_pit_stops': 0, 'total_pit_time': 0})
    avg_pit_time = pit_stops['total_pit_time'] / pit_stops['total_pit_stops'] if pit_stops['total_pit_stops'] > 0 else 0

    # Combine race error and pit stop inefficiency (e.g., weight them equally or based on a formula)
    error_from_races = problematic_races / total_races if total_races > 0 else 0
    pit_stop_penalty = avg_pit_time / 20.0  # Assuming 20 seconds as an ideal pit stop time

    # Combine the two to calculate adjusted probability of error
    team_probability_of_error[team] = error_from_races + pit_stop_penalty

# Create DataFrame and save
team_probability_df = pd.DataFrame(
    [
        {'Constructor': team, 'Probability_of_Error': probability,
         'Avg_Pit_Stop_Time': pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})['total_pit_time'] /
                              pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})[
                                  'total_pit_stops'] if
         pit_stop_stats.get(team, {'total_pit_time': 0, 'total_pit_stops': 0})['total_pit_stops'] > 0 else 0}
        for team, probability in team_probability_of_error.items()
    ]
)

print(team_probability_df)

team_probability_df.to_csv('team_error_probabilities_with_pit_stops.csv', index=False)
