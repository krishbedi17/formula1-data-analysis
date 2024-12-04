import pandas as pd

file_path = '/Users/DELL/Documents/GitHub/F1-Race-Predictor/2022_weather_data/part-00000-bc8144dd-cce0-47d9-a4b9-a22a2ba122da-c000.csv.gz'

# Read the compressed CSV file into a Pandas DataFrame
df = pd.read_csv(file_path, compression='gzip')

# # Ensure the 'Date' column is in datetime format for accurate sorting
# df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by the 'Date' column
df_sorted = df.sort_values(by='Round')

# Display the sorted DataFrame
print(df_sorted)

# # Optionally, save the sorted DataFrame to a new file
# output_path = '/Users/DELL/Documents/GitHub/F1-Race-Predictor/2018_weather_data/sorted_weather_data.csv'
# df_sorted.to_csv(output_path, index=False)
