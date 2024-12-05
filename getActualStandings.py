import requests
import pandas as pd


def get_driver_standings(year):
    """Fetch driver standings for a given year using the Ergast API."""
    url = f"https://ergast.com/api/f1/{year}/driverStandings.json"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        standings_list = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])

        if standings_list:
            # Get the first (and only) standings list for the season
            driver_standings = standings_list[0].get("DriverStandings", [])

            # Extract relevant details for each driver
            standings_data = []
            for entry in driver_standings:
                driver_info = entry.get("Driver", {})
                constructor_info = entry.get("Constructors", [{}])[0]  # Assuming one constructor per driver

                standings_data.append({
                    "Position": entry.get("position"),
                    "Driver ID": driver_info.get("driverId"),
                    "Driver Name": f"{driver_info.get('givenName')} {driver_info.get('familyName')}",
                    "Nationality": driver_info.get("nationality"),
                    "Constructor": constructor_info.get("name"),
                    "Points": entry.get("points"),
                    "Wins": entry.get("wins")
                })

            # Convert to DataFrame
            standings_df = pd.DataFrame(standings_data)
            return standings_df

        else:
            print(f"No standings data found for year {year}.")
            return pd.DataFrame()

    else:
        print(f"Failed to fetch standings for year {year}. Status code: {response.status_code}")
        return pd.DataFrame()


# Fetch and save 2023 standings
year = 2023
standings_2023 = get_driver_standings(year)

if not standings_2023.empty:
    print("2023 Driver Standings:")
    print(standings_2023)
    standings_2023.to_csv(f"{year}_driver_standings.csv", index=False)
else:
    print("No data available.")
