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


def get_race_data(year, total_rounds, total_points, total_wins):
    df = pd.DataFrame()

    for race_id in range(1, total_rounds + 1):
        url = f"https://ergast.com/api/f1/{year}/{race_id}/results.json"
        response = requests.get(url).json()

        races = response['MRData']['RaceTable']['Races']

        if not races:
            continue

        race_data = races[0]['Results']
        race_df = pd.json_normalize(race_data)

        race_df['Race ID'] = race_id
        race_df['Year'] = year
        race_df['FastestLap.Time.time'] = race_df.get('FastestLap.Time.time', None)
        race_df['FastestLap.AverageSpeed.speed'] = race_df.get('FastestLap.AverageSpeed.speed', None)

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

        race_df['Total Points'] = race_df['Driver ID'].map(total_points).fillna(0) + race_df['Points']
        race_df['Wins'] = 0
        race_df.loc[race_df['Position'] == '1', 'Wins'] = 1

        race_df['Total Wins'] = race_df['Driver ID'].map(total_wins).fillna(0) + race_df['Wins']
        for i in range(len(race_df)):
            driver_id = race_df.loc[i, 'Driver ID']
            points = race_df.loc[i, 'Total Points']
            wins = race_df.loc[i, 'Total Wins']

            total_points[driver_id] = points
            total_wins[driver_id] = wins

        df = pd.concat([df, race_df], ignore_index=True)

    return df, total_points, total_wins


def main():
    points_and_wins_until_2017 = pd.read_csv('driver_data/driver_points_and_wins.csv')
    total_points = points_and_wins_until_2017.set_index('Driver ID')['Total Points Until 2017'].to_dict()
    total_wins = points_and_wins_until_2017.set_index('Driver ID')['Total Wins Until 2017'].to_dict()

    for year in range(2018, 2024):
        total_rounds = get_rounds(year)
        race_results, total_points, total_wins = get_race_data(year, total_rounds, total_points, total_wins)
        race_results.to_csv(f"race_data/{year}_race_results.csv", index=False)


if __name__ == "__main__":
    main()
