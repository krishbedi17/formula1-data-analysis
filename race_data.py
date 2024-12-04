import requests
import pandas as pd
#2018 - 21
#2019 - 21
#2020 - 17
#2021 - 22
#2022 - 22
#2023 - 23

def get_rounds(year):
    if(2018):
        return 22
    elif(2019):
        return 22
    elif (2020):
        return 18
    elif (2021):
        return 23
    elif (2022):
        return 22
    elif (2023):
        return 24

def get_race_data(year,round):
    df = pd.DataFrame()
    for i in range(1, round):
        url = f"https://ergast.com/api/f1/2018/{i}/results.json"

        response = requests.get(url).json()
        races = response['MRData']['RaceTable']['Races']

        race_data = races[0]['Results']
        race_df = pd.json_normalize(race_data)

        race_df['raceID'] = i
        race_df['year'] = year
        race_df = race_df[[
            'raceID', 'position', 'Driver.driverId', 'Driver.familyName', 'Driver.givenName',
            'Constructor.name','Constructor.constructorId', 'points', 'FastestLap.Time.time', 'FastestLap.AverageSpeed.speed'
        ]]

        race_df.rename(columns={
            'raceID': 'Race ID',
            'year': 'Year',
            'position': 'Position',
            'Driver.driverId': 'Driver ID',
            'Driver.familyName': 'Last Name',
            'Driver.givenName': 'First Name',
            'Constructor.constructorId': 'Constructor ID',
            'Constructor.name': 'Constructor',
            'points': 'Points',
            'FastestLap.Time.time': 'Fastest Lap Time',
            'FastestLap.AverageSpeed.speed': 'Fastest Lap Avg Speed (kph)'
        }, inplace=True)
        df = pd.concat([df,race_df],ignore_index=True)

    df.to_csv(f"race_data/{year}_race_results.csv", index=False)



def main():
    for i in range(2018,2024):
       rounds = get_rounds(i)
       get_race_data(i,rounds)


main()