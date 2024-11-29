import fastf1
import pandas as pd

weather_df = pd.DataFrame()

for i in range(1, 18):
    try:
        session = fastf1.get_session(2020, i, 'R')
        session.load()

        # Get the average or representative weather data for the race
        race_weather = session.weather_data.mean()
        race_weather['raceID'] = i
        race_weather['year']=2020
        # Convert to DataFrame and append
        race_weather_df = pd.DataFrame([race_weather])
        weather_df = pd.concat([weather_df, race_weather_df], ignore_index=True)
        print(i)
    except Exception as e:
        print(f"Could not load weather data for Round {i}: {e}")

weather_df.to_csv("2020_weather_data.csv", index=False)