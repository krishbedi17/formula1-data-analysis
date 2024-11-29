import pandas as pd
import os

# List of file paths for the years you want to analyze
years = [2018, 2019, 2020, 2021, 2022]  # Modify as needed
file_paths = [f"{year}_data_with_race_names.csv" for year in years]

# Initialize a dictionary to hold the collision counts and total races for each driver
collision_counts = {}
total_races = {}

# Loop over the files
for file_path in file_paths:
    # Load the data
    if os.path.exists(file_path):  # Check if the file exists
        data = pd.read_csv(file_path)

        # Check the columns to make sure 'Status' and 'DriverNumber' exist
        print(f"Processing file: {file_path}")
        print(data.columns)

        # Convert the 'Status' column to lowercase to handle case insensitivity
        data['Status'] = data['Status'].str.lower()

        # Filter rows where Status contains 'collision' or 'accident'
        collision_data = data[data['Status'].str.contains('collision|accident', na=False)]

        # Group by 'DriverNumber' and count collisions/accidents
        for driver in collision_data['BroadcastName'].unique():
            # Count collisions for this driver in the current year
            driver_collision_count = collision_data[collision_data['BroadcastName'] == driver].shape[0]

            # Update total races count for the driver
            driver_race_count = data[data['BroadcastName'] == driver].shape[0]

            # Update the total collision count and total races count
            if driver in collision_counts:
                collision_counts[driver] += driver_collision_count
                total_races[driver] += driver_race_count
            else:
                collision_counts[driver] = driver_collision_count
                total_races[driver] = driver_race_count
    else:
        print(f"File {file_path} not found!")

# Calculate the probability of error for each driver
probability_of_error = {}

for driver in collision_counts:
    total = total_races[driver]
    collisions = collision_counts[driver]
    if total > 0:
        probability_of_error[driver] = collisions / total
    else:
        probability_of_error[driver] = 0

# Convert to a DataFrame for easy viewing
probability_df = pd.DataFrame(list(probability_of_error.items()), columns=['BroadcastName', 'Probability_of_Error'])

# Display the results
print(probability_df)

# Optionally, you can save the results to a CSV file
probability_df.to_csv('driver_error_probabilities.csv', index=False)
