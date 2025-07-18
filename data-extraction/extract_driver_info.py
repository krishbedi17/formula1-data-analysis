import pandas as pd
import requests
import os


def get_driver_information(year):
    url = f"http://ergast.com/api/f1/{year}/drivers.json"
    response = requests.get(url)
    if response.status_code == 200:
        driver_data = response.json().get('MRData', {}).get('DriverTable', {}).get('Drivers', [])
        if driver_data:
            driver_df = pd.json_normalize(driver_data)
            driver_df = driver_df[[
                'driverId', 'givenName', 'familyName', 'permanentNumber', 'code', 'dateOfBirth', 'nationality'
            ]]

            driver_df.rename(columns={
                'driverId': 'Driver ID',
                'givenName': 'Driver First Name',
                'familyName': 'Driver Last Name',
                'permanentNumber': 'Permanent Number',
                'code': 'Driver Code',
                'dateOfBirth': 'Date of Birth',
                'nationality': 'Nationality'
            }, inplace=True)
            return driver_df
        else:
            print(f"No data available for the year {year}.")
            return pd.DataFrame()

    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


def main():
    # Create directories if they don't exist
    os.makedirs("../data/raw/driver_data", exist_ok=True)
    
    for i in range(2018, 2024):
        info = get_driver_information(i)
        info.to_csv(f"../data/raw/driver_data/{i}_driver_data.csv", index=False)


if __name__ == "__main__":
    main()