import os
import pandas as pd
import requests

def convert_duration_to_seconds(duration):
    if pd.isna(duration):
        return 0

    if ':' in duration:
        seconds, milliseconds = duration.split(':')
        seconds = float(seconds)
        milliseconds, garbage = milliseconds.split('.')
        milliseconds = float(milliseconds) / 1000
        total_seconds = seconds + milliseconds
    else:
        seconds, milliseconds = duration.split('.')
        seconds = float(seconds)
        milliseconds = float(milliseconds) / 1000
        total_seconds = seconds + milliseconds

    return total_seconds


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
                    'driverId', 'stop', 'lap', 'time', 'duration', 'Round'
                ]]

                pit_stop_df.rename(columns={
                    'driverId': 'Driver ID',
                    'stop': 'Stop',
                    'lap': 'Lap',
                    'time': 'Time',
                    'duration': 'Duration'
                }, inplace=True)
                pit_stop_df['DuraNumeric'] = pit_stop_df['Duration'].apply(convert_duration_to_seconds)
                pit_stop_df.drop(columns=['Time', 'Duration'], inplace=True)
                pit_stop_df.rename(columns={'DuraNumeric': 'Duration'}, inplace=True)
                return pit_stop_df
        else:
            print(f"No data available for the year {year}, round {round}.")
            return pd.DataFrame()

    else:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()


def main():
    output_dir = "pit_stops_data"
    output_file = "avg_pit_stops_2018_to_2023.csv"
    os.makedirs(output_dir, exist_ok=True)

    all_pit_stops = []

    for i in range(2018, 2024):
        filename = f"season_schedule/{i}_season_schedule.csv"
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue

        df = pd.read_csv(filename)
        round_count = df['Round'].count()

        for j in range(1, round_count + 1):
            pit_stops = get_pit_stops(i, j)
            if not pit_stops.empty:
                avg_pit_stop = pit_stops.groupby(['Round', 'Driver ID'])['Duration'].agg(Mean ='mean', StdDev = 'std').reset_index()
                avg_pit_stop['StdDev'] = avg_pit_stop['StdDev'].fillna(0)
                avg_pit_stop['Year'] = i
                all_pit_stops.append(avg_pit_stop)

    if all_pit_stops:
        avg_pit_stops_df = pd.concat(all_pit_stops, ignore_index=True)
        avg_pit_stops_df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("No pit stop data to save.")


main()
