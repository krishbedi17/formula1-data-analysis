import os
import pandas as pd
import requests


def get_pit_stops(year, round):
    url = f"http://ergast.com/api/f1/{year}/{round}/pitstops.json"
    response = requests.get(url)

    if response.status_code == 200:
        pit_stop_data = response.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])
        if pit_stop_data:
            race = pit_stop_data[0]
            pitStops = race.get('PitStops', [])
            if pitStops:
                for result in pitStops:
                    result['Round'] = round

                pit_stop_df = pd.json_normalize(pitStops)
                pit_stop_df = pit_stop_df[[
                    'driverId', 'stop', 'lap', 'time', 'duration'
                ]]

                pit_stop_df.rename(columns={
                    'driverId': 'Driver ID',
                    'stop': 'Stop',
                    'lap': 'Lap',
                    'time': 'Time',
                    'duration': 'Duration'
                }, inplace=True)

                return pit_stop_df
        else:
            print(f"No data available for the year {year}, round {round}.")
            return pd.DataFrame()

    else:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()


def main():
    output_dir = "pit_stops_data"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(2018, 2024):
        filename = f"season_schedule/{i}_season_schedule.csv"
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue

        df = pd.read_csv(filename)
        round_count = df['Round'].count()

        season_results = []

        for j in range(1, round_count + 1):
            results = get_pit_stops(i, j)
            if not results.empty:
                season_results.append(results)

        if season_results:
            season_df = pd.concat(season_results, ignore_index=True)
            season_df.to_csv(f"{output_dir}/{i}_pit_stops.csv", index=False)
        else:
            print(f"No pit stop results found for season {i}.")


main()
