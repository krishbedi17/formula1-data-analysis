import pandas as pd
import requests


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

def get_quali_results(year, round):
    url = f"http://ergast.com/api/f1/{year}/{round}/qualifying.json"
    response = requests.get(url)
    if response.status_code == 200:
        quali_data = response.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])

        if quali_data:
            quali_results = quali_data[0].get('QualifyingResults', [])
            if quali_results:
                for result in quali_results:
                    result['Round'] = round
                    result['Driver Id'] = result['Driver']['driverId']

                quali_df = pd.json_normalize(quali_results)
                quali_df['Q2'] = quali_df.get('time', None)
                quali_df['Q3'] = quali_df.get('time', None)

                quali_df = quali_df[[
                    'Round', 'Driver Id', 'Driver.givenName', 'Driver.familyName', 'Constructor.name', 'position', 'Q1',
                    'Q2', 'Q3'
                ]]

                # Rename the columns for clarity
                quali_df.rename(columns={
                    'Driver.givenName': 'Driver First Name',
                    'Driver.familyName': 'Driver Last Name',
                    'Constructor.name': 'Constructor Name',
                    'position': 'Position',
                    'Q1': 'Q1 Time',
                    'Q2': 'Q2 Time',
                    'Q3': 'Q3 Time'
                }, inplace=True)

                return quali_df
            else:
                print(f"No qualifying results available for Year: {year}, Round: {round}.")
                return pd.DataFrame()
        else:
            print(f"No race data available for Year: {year}, Round: {round}.")
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data for Year: {year}, Round: {round}. HTTP Status Code: {response.status_code}")
        return pd.DataFrame()


def main():
    for i in range(2018, 2024):
        filename = f"season_schedule/{i}_season_schedule.csv"
        round_count = get_rounds(i)

        season_results = []

        for j in range(1, round_count + 1):  # Ensure the round count is inclusive
            print(f"Fetching qualifying data for Year: {i}, Round: {j}")
            results = get_quali_results(i, j)
            if not results.empty:
                season_results.append(results)

        if season_results:
            season_df = pd.concat(season_results, ignore_index=True)
            season_df.to_csv(f"quali_data/{i}_quali_results.csv", index=False)
        else:
            print(f"No qualifying results found for season {i}.")


main()
