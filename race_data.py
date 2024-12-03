#2018 - 21
#2019 - 21
#2020 - 17
#2021 - 22

#2022 - 22
#2023 - 23
import requests
import pandas as pd

year = 2023
season_df = pd.DataFrame()

for i in range(1, 24):
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

    race_df = race_df[[
        'raceID', 'position', 'Driver.familyName', 'Driver.givenName',
        'Constructor.name', 'points', 'FastestLap.Time.time', 'FastestLap.AverageSpeed.speed',
        'status','Driver.code'
    ]]
    if 'FastestLap' in race_df.columns:
        race_df['FastestLap.Time.time'] = race_df['FastestLap'].apply(
            lambda x: x.get('Time', {}).get('time') if isinstance(x, dict) else None)
        race_df['FastestLap.AverageSpeed.speed'] = race_df['FastestLap'].apply(
            lambda x: x.get('AverageSpeed', {}).get('speed') if isinstance(x, dict) else None)

    race_df.rename(columns={
        'raceID': 'Race ID',
        'position': 'Position',
        'Driver.familyName': 'Last Name',
        'Driver.givenName': 'First Name',
        'Constructor.name': 'Constructor',
        'points': 'Points',
        'FastestLap.Time.time': 'Fastest Lap Time',
        'FastestLap.AverageSpeed.speed': 'Fastest Lap Avg Speed (kph)',
        'status' : 'Status',
        'Driver.code' : 'Driver Code'
    }, inplace=True)

    season_df = pd.concat([season_df, race_df], ignore_index=True)

season_df.to_csv(f"race_data/{year}_race_data.csv", index=False)