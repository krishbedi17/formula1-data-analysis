import pandas as pd
import requests


def get_driver_points_until_2017(driver_id):
    total_points_until_2017 = 0
    total_wins_until_2017 = 0
    season_points = {2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0}  # Dictionary to store points for each season
    season_wins = {2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0}  # Dictionary to store wins for each season
    points_until_2017 = 0  # To track the points up until 2017

    total_points_after_2017 = 0
    total_wins_after_2017 = 0

    url = f"http://ergast.com/api/f1/drivers/{driver_id}/driverStandings.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        standings_list = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])

        for standing in standings_list:
            season = int(standing.get("season", 0))
            driver_standings = standing.get("DriverStandings", [])
            if driver_standings:
                points = float(driver_standings[0].get("points", 0))
                wins = int(driver_standings[0].get("wins", 0))

                if season <= 2017:  # Accumulate points and wins until 2017
                    points_until_2017 += points
                    total_wins_until_2017 += wins
                elif 2018 <= season <= 2023:  # Store points and wins for seasons 2018-2023
                    season_points[season] = points
                    season_wins[season] = wins
                    total_points_after_2017 += points
                    total_wins_after_2017 += wins

        # Return all the stats, including points until 2017
        return {
            "Driver ID": driver_id,
            "Total Points": points_until_2017 + total_points_after_2017,
            "Total Wins After 2017": total_wins_after_2017,
            "Total Points Until 2017": points_until_2017,
            "Total Wins Until 2017": total_wins_until_2017,
            "Season Points": season_points,
            "Season Wins": season_wins
        }
    else:
        print(f"Failed to fetch data for {driver_id}. HTTP Status Code: {response.status_code}")
        return {
            "Driver ID": driver_id,
            "Total Points Until 2017": 0,
            "Total Points": 0,
            "Total Wins": 0,
            "Season Points": {},
            "Season Wins": {}
        }


def main():
    data = pd.read_csv("race_error/driver_error_probabilities.csv")
    driver_ids = data['Driver ID'].tolist()
    results = []
    for driver_id in driver_ids:
        driver_stats = get_driver_points_until_2017(driver_id)
        results.append(driver_stats)

    results_df = pd.DataFrame(results)
    results_df.to_csv("driver_data/driver_points_and_wins.csv", index=False)


main()
