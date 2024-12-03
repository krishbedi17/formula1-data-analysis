import requests
from bs4 import BeautifulSoup
import pandas as pd

# F1 Circuit Locations (add more if necessary)
f1_circuits = {
    "Bahrain": "BH/Sakhir",
    "Monaco": "MC/MonteCarlo",
    "Silverstone": "GB/England/Silverstone",
    "Monza": "IT/Milan/Monza",
    "Spa-Francorchamps": "BE/Walloon/Francorchamps",
    "Barcelona": "ES/Catalunya/Barcelona",
    # Add more circuits here as needed
}


# Function to get historical weather data from Weather Underground
def get_weather_data(location, date):
    weather_data = []

    # Construct the URL for the weather data based on location and date
    base_url = f"https://www.wunderground.com/history/daily/{location}/date/"

    # Format date to match YYYY-MM-DD
    date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    url = base_url + date_str

    # Send the GET request to fetch data
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the relevant data for temperature and precipitation
        try:
            temp = soup.find('span', {'class': 'wu-value wu-value-to'}).text  # Temperature
            precip = soup.find('span', {'class': 'wu-value wu-value-to'}).text  # Precipitation (if available)

            weather_data.append({
                'Date': date_str,
                'Temperature (°C)': temp,
                'Precipitation (mm)': precip
            })
        except AttributeError:
            print(f"Data not available for {date_str} in {location}")
    else:
        print(f"Failed to retrieve data for {date_str} in {location}")

    return weather_data


# Function to get weather for all F1 circuits for a given race date
def get_f1_weather_data_for_race(circuits, date):
    all_weather_data = []

    # Loop over each circuit and fetch weather data
    for circuit_name, location in circuits.items():
        print(f"Fetching weather data for {circuit_name}...")
        weather_data = get_weather_data(location, date)

        # Add circuit name to the weather data
        for entry in weather_data:
            entry['Circuit'] = circuit_name

        # Add to all weather data
        all_weather_data.extend(weather_data)

    # Return the weather data in DataFrame format
    return pd.DataFrame(all_weather_data)


# Example usage:
race_date = "2023-03-05"  # Example race date (change to your desired race date)
weather_data_df = get_f1_weather_data_for_race(f1_circuits, race_date)

# Display the results
if not weather_data_df.empty:
    print(weather_data_df)
    weather_data_df.to_csv('f1_weather_data.csv', index=False)
else:
    print("No weather data found.")
