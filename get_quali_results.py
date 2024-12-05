import pandas as pd
import requests
from statsmodels.graphics.tukeyplot import results


def get_quali_results(year, round):
    url = f"http://ergast.com/api/f1/{year}/{round}/qualifying.json"
    response = requests.get(url)
    if response.status_code == 200:
        quali_data = response.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])
        if quali_data:
            race = quali_data[0]  # Assuming there's only one race for the given year and round
            quali_results = race.get('QualifyingResults', [])

            if quali_results:
                for result in quali_results:
                    result['Round'] = round + 1

                quali_df = pd.json_normalize(quali_results)

                # Filter the relevant columns
                quali_df = quali_df[[
                    'Round', 'Driver.givenName', 'Driver.familyName', 'Constructor.name', 'position', 'Q1', 'Q2', 'Q3'
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
            print(f"No data available for the year {year}.")
            return pd.DataFrame()

    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


def main():
    # results = []
    for i in range(2018, 2024):
        filename = f"season_schedule/{i}_season_schedule.csv"
        df = pd.read_csv(filename)
        round_count = df['Round'].count()

        season_results = []

        for j in range(round_count):
            results = get_quali_results(i, j)
            if not results.empty:
                season_results.append(results)


        if season_results:
            season_df = pd.concat(season_results, ignore_index=True)
            # Save the combined results to a CSV file
            season_df.to_csv(f"quali_data/{i}_quali_results.csv", index=False)
        else:
            print(f"No qualifying results found for season {i}.")



main()