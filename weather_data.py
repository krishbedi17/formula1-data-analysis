import fastf1
import pandas as pd

weather_df = pd.DataFrame()
schedule = fastf1.get_event_schedule(2021)

for i in range(1, 23):
    try:
        session = fastf1.get_session(2021, i, 'R')
        session.load()

        # Retrieve event name and location
        event_name = schedule[schedule['RoundNumber'] == i]['EventName'].iloc[0]
        location = schedule[schedule['RoundNumber'] == i]['Location'].iloc[0]
        event_name = event_name.replace('Grand Prix', '').strip()

        # Create a single row with appropriate aggregations
        race_weather = {
            'raceID': i,
            'year': 2021,
            'EventName': event_name,
            'Location': location,
            'AirTemp': session.weather_data['AirTemp'].mean(),
            'Humidity': session.weather_data['Humidity'].mean(),
            'Pressure': session.weather_data['Pressure'].mean(),
            'Rainfall': session.weather_data['Rainfall'].mean() ,
            'TrackTemp': session.weather_data['TrackTemp'].mean(),
            'WindDirection': session.weather_data['WindDirection'].mean(),
            'WindSpeed': session.weather_data['WindSpeed'].mean()
        }

        race_weather_df = pd.DataFrame([race_weather])
        weather_df = pd.concat([weather_df, race_weather_df], ignore_index=True)
        print(f"Round {i} weather data loaded successfully.")

    except Exception as e:
        print(f"Could not load weather data for Round {i}: {e}")

weather_df.to_csv("2021_weather_data.csv", index=False)