import pandas as pd
import os

years = [2018, 2019, 2020, 2021, 2022]
file_paths = [f"race_data/{year}_race_results.csv" for year in years]

collision_counts = {}
total_races = {}

for file_path in file_paths:
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)

        print(f"Processing file: {file_path}")
        print(data.columns)

        data['Status'] = data['Status'].str.lower()

        if 'Driver ID' in data.columns:
            driver_column = 'Driver ID'
        elif 'First Name' in data.columns and 'Last Name' in data.columns:
            data['Driver Name'] = data['First Name'] + ' ' + data['Last Name']
            driver_column = 'Driver Name'
        else:
            print(f"Driver identification columns not found in {file_path}. Skipping this file.")
            continue

        collision_data = data[data['Status'].str.contains('collision|accident', na=False)]

        for driver in collision_data[driver_column].unique():
            driver_collision_count = collision_data[collision_data[driver_column] == driver].shape[0]
            driver_race_count = data[data[driver_column] == driver].shape[0]

            if driver in collision_counts:
                collision_counts[driver] += driver_collision_count
                total_races[driver] += driver_race_count
            else:
                collision_counts[driver] = driver_collision_count
                total_races[driver] = driver_race_count
    else:
        print(f"File {file_path} not found!")

probability_of_error = {}

for driver in collision_counts:
    total = total_races[driver]
    collisions = collision_counts[driver]
    probability_of_error[driver] = collisions / total if total > 0 else 0

probability_df = pd.DataFrame(list(probability_of_error.items()), columns=['Driver', 'Probability_of_Error'])

print(probability_df)

probability_df.to_csv('driver_error_probabilities.csv', index=False)
