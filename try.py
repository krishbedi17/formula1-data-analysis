import requests
import pandas as pd
import time


# Function to fetch weather data
def fetch_weather_data(api_key, city, start_date, end_date):
    """
    Fetch weather data from WeatherAPI for a given city and date range.
    """
    url = "http://api.weatherapi.com/v1/history.json"

    weather_data = []
    current_date = start_date

    while current_date <= end_date:
        response = requests.get(url, params={
            "key": api_key,
            "q": city,
            "dt": current_date.strftime('%Y-%m-%d')
        })

        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "date": current_date,
                "city": city,
                "temperature": data['forecast']['forecastday'][0]['day']['avgtemp_c'],
                "humidity": data['forecast']['forecastday'][0]['day']['avghumidity'],
                "weather": data['forecast']['forecastday'][0]['day']['condition']['text']
            })
        else:
            print(f"Failed to fetch data for {current_date}: {response.text}")

        # Increment the date by 1 day
        current_date += pd.Timedelta(days=1)
        time.sleep(1)  # Rate limiting

    return weather_data


# Main function
if __name__ == "__main__":
    # Use your WeatherAPI key
    API_KEY = "your_weatherapi_key"

    # Input city name and date range
    CITY = "Vancouver"
    START_DATE = pd.Timestamp("2024-01-01")
    END_DATE = pd.Timestamp("2024-01-07")

    # Fetch weather data
    weather_data = fetch_weather_data(API_KEY, CITY, START_DATE, END_DATE)

    # Save data to a CSV file
    if weather_data:
        df = pd.DataFrame(weather_data)
        df.to_csv(f"{CITY}_weather_data.csv", index=False)
        print(f"Weather data saved to {CITY}_weather_data.csv")
    else:
        print("No data fetched.")
