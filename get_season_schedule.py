import pandas as pd
import requests

def get_season_schedule(year):
    url = f"http://ergast.com/api/f1/{year}.json"
    response = requests.get(url)
    if response.status_code == 200:
        schedule = response.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])
        if schedule:
            schedule_df = pd.json_normalize(schedule)
            schedule_df = schedule_df[[
                'round', 'raceName', 'Circuit.circuitId', 'Circuit.circuitName',
                'Circuit.Location.locality', 'Circuit.Location.country',
                'Circuit.Location.lat', 'Circuit.Location.long', 'date', 'time'
            ]]

            # Rename columns for better readability
            schedule_df.rename(columns={
                'round': 'Round',
                'raceName': 'Race Name',
                'Circuit.circuitId': 'Circuit ID',
                'Circuit.circuitName': 'Circuit Name',
                'Circuit.Location.locality': 'Locality',
                'Circuit.Location.country': 'Country',
                'Circuit.Location.lat': 'Latitude',
                'Circuit.Location.long': 'Longitude',
                'date': 'Date',
                'time': 'Time'
            }, inplace=True)

            return schedule_df

    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


def main():
    for i in range(2018, 2024):
        schedule = get_season_schedule(i)
        schedule.to_csv(f"season_schedule/{i}_season_schedule.csv", index=False)

main()