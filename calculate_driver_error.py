import pandas as pd
import os

years = [2018, 2019, 2020, 2021, 2022]
file_paths = [f"race_data/{year}_race_results.csv" for year in years]

collision_counts = {}
total_races = {}
driver_id_mapping = {}

for file_path in file_paths:
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)

        print(f"Processing file: {file_path}")
        print(data.columns)

        # Ensure case consistency in the 'Status' column
        data['Status'] = data['Status'].str.lower()

        # Construct a 'Driver Name' column if 'First Name' and 'Last Name' are present
        if 'First Name' in data.columns and 'Last Name' in data.columns:
            data['Driver Name'] = data['First Name'] + ' ' + data['Last Name']
        else:
            print(f"'First Name' and 'Last Name' columns are missing in {file_path}.")
            continue

        # Use 'Driver Name' for processing
        collision_data = data[data['Status'].str.contains('collision|accident', na=False)]

        for _, row in collision_data.iterrows():
            driver_name = row['Driver Name']
            driver_id = row['Driver ID']

            if driver_name not in driver_id_mapping:
                driver_id_mapping[driver_name] = driver_id

            if driver_name in collision_counts:
                collision_counts[driver_name] += 1
            else:
                collision_counts[driver_name] = 1

        for _, row in data.iterrows():
            driver_name = row['Driver Name']

            if driver_name in total_races:
                total_races[driver_name] += 1
            else:
                total_races[driver_name] = 1
    else:
        print(f"File {file_path} not found!")

probability_of_error = {}

for driver_name in collision_counts:
    total = total_races.get(driver_name, 0)
    collisions = collision_counts[driver_name]
    probability_of_error[driver_name] = {
        "Driver ID": driver_id_mapping.get(driver_name, None),
        "Probability_of_Error": collisions / total if total > 0 else 0,
    }

probability_df = pd.DataFrame(
    [
        {"Driver": driver, "Driver ID": details["Driver ID"], "Probability_of_Error": details["Probability_of_Error"]}
        for driver, details in probability_of_error.items()
    ]
)

print(probability_df)

# Save to CSV
probability_df.to_csv('race_error/driver_error_probabilities.csv', index=False)
