import requests
import pandas as pd

def get_race_results(year, rounds):
    season_df = pd.DataFrame()
    for i in range(1, rounds + 1):
        url = f"https://ergast.com/api/f1/{year}/{i}/results.json"
        response = requests.get(url).json()
        races = response['MRData']['RaceTable']['Races']

        if not races:
            print(f"No data for race {i}")
            continue

        race_data = races[0]['Results']
        race_df = pd.json_normalize(race_data)
        race_df['raceID'] = i
        race_df['year'] = year

        # Prepare columns with safe extraction
        def safe_extract_fastest_lap_time(row):
            try:
                if isinstance(row.get('FastestLap'), dict):
                    return row['FastestLap'].get('Time', {}).get('time')
            except:
                pass
            return None

        def safe_extract_fastest_lap_speed(row):
            try:
                if isinstance(row.get('FastestLap'), dict):
                    return row['FastestLap'].get('AverageSpeed', {}).get('speed')
            except:
                pass
            return None

        # Add new columns safely
        race_df['fastest_lap_time'] = race_df.apply(safe_extract_fastest_lap_time, axis=1)
        race_df['fastest_lap_speed'] = race_df.apply(safe_extract_fastest_lap_speed, axis=1)

        # Select and rename columns
        columns_to_select = [
            'raceID',
            'position',
            'Driver.familyName',
            'Driver.givenName',
            'Constructor.name',
            'points',
            'fastest_lap_time',
            'fastest_lap_speed',
            'status',
            'Driver.code',
            'Driver.driverId'
        ]

        # Only select columns that exist in the DataFrame
        existing_columns = [col for col in columns_to_select if col in race_df.columns]
        race_df = race_df[existing_columns]

        race_df.rename(columns={
            'raceID': 'Race ID',
            'position': 'Position',
            'Driver.familyName': 'Last Name',
            'Driver.givenName': 'First Name',
            'Constructor.name': 'Constructor',
            'points': 'Points',
            'fastest_lap_time': 'Fastest Lap Time',
            'fastest_lap_speed': 'Fastest Lap Avg Speed (kph)',
            'status': 'Status',
            'Driver.code': 'Driver Code',
            'Driver.driverId': 'Driver ID'
        }, inplace=True)

        season_df = pd.concat([season_df, race_df], ignore_index=True)
    return season_df

def main():
    for i in range(2018, 2024):
        filename = f"season_schedule/{i}_season_schedule.csv"
        df = pd.read_csv(filename)
        round_count = df['Round'].count()

        results = get_race_results(i, round_count)
        if results.empty:
            print(f"No qualifying results found for season {i}.")
        else:
            results.to_csv(f"race_data/{i}_race_results.csv", index=False)

main()