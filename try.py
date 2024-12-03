import requests
import pandas as pd
from setuptools.command.egg_info import overwrite_arg

#2018 - 21
#2019 - 21
#2020 - 17
#2021 - 22
#2022 - 22
#2023 - 23

df = pd.DataFrame()
for i in range(1, 22):
    url = f"https://ergast.com/api/f1/2018/{i}/results.json"

    response = requests.get(url).json()
    races = response['MRData']['RaceTable']['Races']

    race_data = races[0]['Results']
    race_df = pd.json_normalize(race_data)

    race_df['raceID'] = i
    race_df = race_df[[
        'raceID', 'position', 'Driver.familyName', 'Driver.givenName',
        'Constructor.name', 'points', 'FastestLap.Time.time', 'FastestLap.AverageSpeed.speed'
    ]]

    race_df.rename(columns={
        'raceID': 'Race ID',
        'position': 'Position',
        'Driver.familyName': 'Last Name',
        'Driver.givenName': 'First Name',
        'Constructor.name': 'Constructor',
        'points': 'Points',
        'FastestLap.Time.time': 'Fastest Lap Time',
        'FastestLap.AverageSpeed.speed': 'Fastest Lap Avg Speed (kph)'
    }, inplace=True)
    df = pd.concat([df,race_df],ignore_index=True)

df.to_csv("2018_data_with_race_names.csv", index=False)