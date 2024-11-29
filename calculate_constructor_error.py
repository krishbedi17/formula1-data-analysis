import pandas as pd
import os

# List of file paths for the years you want to analyze
years = [2018, 2019, 2020, 2021, 2022]  # Modify as needed
file_paths = [f"{year}_data_with_race_names.csv" for year in years]

# Initialize dictionaries to hold the collision counts and total races for each team
team_collision_counts = {}
team_total_races = {}

# Loop over the files
for file_path in file_paths:
    # Load the data
    if os.path.exists(file_path):  # Check if the file exists
        data = pd.read_csv(file_path)

        # Check the columns to make sure 'Status' and 'Team' exist
        print(f"Processing file: {file_path}")
        print(data.columns)

        # Convert the 'Status' column to lowercase to handle case insensitivity
        data['Status'] = data['Status'].str.lower()

        # Filter out rows where Status contains 'collision', 'accident', 'finished', or anything with 'lap'
        # We use ~ to exclude these statuses
        valid_data = data[~data['Status'].str.contains('collision|accident|finished|lap', na=False)]

        # Group by 'Team' and count races for the team
        for team in valid_data['TeamId'].unique():  # Replace 'Team' with the correct column name
            # Count races for this team in the current year
            team_race_count = valid_data[valid_data['TeamId'] == team].shape[0]

            # Update total races count for the team
            total_race_count = data[data['TeamId'] == team].shape[0]

            # Update the total collision count and total races count for the team
            if team in team_collision_counts:
                team_collision_counts[team] += team_race_count
                team_total_races[team] += total_race_count
            else:
                team_collision_counts[team] = team_race_count
                team_total_races[team] = total_race_count
    else:
        print(f"File {file_path} not found!")

# Calculate the probability of error for each team
team_probability_of_error = {}

for team in team_collision_counts:
    total = team_total_races[team]
    races = team_collision_counts[team]  # Counting all valid races for the team
    if total > 0:
        team_probability_of_error[team] = races / total
    else:
        team_probability_of_error[team] = 0

# Convert to a DataFrame for easy viewing
team_probability_df = pd.DataFrame(list(team_probability_of_error.items()), columns=['TeamId', 'Probability_of_Error'])

# Display the results
print(team_probability_df)

# Optionally, you can save the results to a CSV file
team_probability_df.to_csv('team_error_probabilities.csv', index=False)
