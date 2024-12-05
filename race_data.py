import requests
import pandas as pd


def get_rounds(year):
    if year == 2018:
        return 21
    elif year == 2019:
        return 21
    elif year == 2020:
        return 17
    elif year == 2021:
        return 22
    elif year == 2022:
        return 22
    elif year == 2023:
        return 23


def get_race_data(year, total_rounds, points_until_2017):
    df = pd.DataFrame()
    total_points = points_until_2017.set_index('Driver ID')['Total Points Until 2017'].to_dict()

    for race_id in range(1, total_rounds + 1):  # Loop through all races for the year
        if year == 2021 & race_id == 12:
            continue
        url = f"https://ergast.com/api/f1/{year}/{race_id}/results.json"
        response = requests.get(url).json()

        races = response['MRData']['RaceTable']['Races']

        race_data = races[0]['Results']
        race_df = pd.json_normalize(race_data)

        race_df['Race ID'] = race_id


        race_df['Year'] = year
        race_df = race_df[[
            'Race ID', 'Year', 'position', 'Driver.driverId', 'Driver.familyName', 'Driver.givenName',
            'Constructor.name', 'Constructor.constructorId', 'points', 'status', 'FastestLap.Time.time',
            'FastestLap.AverageSpeed.speed'
        ]]

        race_df.rename(columns={
            'position': 'Position',
            'Driver.driverId': 'Driver ID',
            'Driver.familyName': 'Last Name',
            'Driver.givenName': 'First Name',
            'Constructor.constructorId': 'Constructor ID',
            'Constructor.name': 'Constructor',
            'points': 'Points',
            'status': 'Status',
            'FastestLap.Time.time': 'Fastest Lap Time',
            'FastestLap.AverageSpeed.speed': 'Fastest Lap Avg Speed (kph)'
        }, inplace=True)

        race_df['Points'] = pd.to_numeric(race_df['Points'], errors='coerce').fillna(0)

        race_df['Total Points Until 2017'] = race_df['Driver ID'].map(total_points)
        race_df['Total Points Until 2017'] = race_df['Total Points Until 2017'].fillna(0)
        race_df['Total Points'] = race_df['Total Points Until 2017'] + race_df['Points']

        for i in range(len(race_df)):
            driver_id = race_df.loc[i, 'Driver ID']
            points = race_df.loc[i, 'Total Points']
            total_points[driver_id] = points

        df = pd.concat([df, race_df], ignore_index=True)

    return df



def main():
    points_until_2017 = pd.read_csv('driver_data/driver_points_and_wins.csv')

    for year in range(2018, 2024):
        total_rounds = get_rounds(year)
        race_results = get_race_data(year, total_rounds, points_until_2017)
        points_until_2017['Total Points Until 2017'] = race_results['Total Points']
        race_results = race_results.drop(columns=['Total Points Until 2017'])
        race_results.to_csv(f"race_data/{year}_race_results.csv", index=False)



if __name__ == "__main__":
    main()
