import numpy as np
import pandas as pd



def main():
    for i in range(2018, 2024):
        pit_df = pd.read_csv(f"pit_stops_data/{i}_pit_stops.csv")
        pit_df = pit_df[['Driver ID', 'Duration']]
        pit_df['Duration'] = pd.to_numeric(pit_df['Duration'], errors='coerce')
        pit_df = pit_df.dropna(subset=['Duration'])
        pit_df_avg = pit_df.groupby(['Driver ID'])['Duration'].aggregate(np.average)
        print(f"Averages for {i}:")
        print(pit_df_avg.to_csv(f"pit_stops_average_data/{i}_pit_stops_average.csv"))


main()
