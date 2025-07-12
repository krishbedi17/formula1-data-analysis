import fastf1
import pandas as pd
import os


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


def get_in(year, round):
    weather_df = pd.DataFrame()
    schedule = fastf1.get_event_schedule(year)
    for i in range(1, round):
        try:
            session = fastf1.get_session(year, i, 'R')
            session.load()

            # Retrieve event name and location
            event_name = schedule[schedule['RoundNumber'] == i]['EventName'].iloc[0]
            location = schedule[schedule['RoundNumber'] == i]['Location'].iloc[0]
            event_name = event_name.replace('Grand Prix', '').strip()

            # Create a single row with appropriate aggregations
            race_weather = {
                'raceID': i,
                'year': year,
                'EventName': event_name,
                'Location': location,
                'AirTemp': session.weather_data['AirTemp'].mean(),
                'Humidity': session.weather_data['Humidity'].mean(),
                'Pressure': session.weather_data['Pressure'].mean(),
                'Rainfall': session.weather_data['Rainfall'].mean(),
                'TrackTemp': session.weather_data['TrackTemp'].mean(),
                'WindDirection': session.weather_data['WindDirection'].mean(),
                'WindSpeed': session.weather_data['WindSpeed'].mean()
            }

            race_weather_df = pd.DataFrame([race_weather])
            weather_df = pd.concat([weather_df, race_weather_df], ignore_index=True)
            print(f"Round {i} weather data loaded successfully.")

        except Exception as e:
            print(f"Could not load weather data for Round {i}: {e}")

    return weather_df


def main():
    # Create directories if they don't exist
    os.makedirs("../data/raw/weather_data", exist_ok=True)
    
    for year in range(2018, 2024):
        round = get_rounds(year)
        weather_df = get_in(year, round)
        if not weather_df.empty:
            weather_df.to_csv(f"../data/raw/weather_data/{year}_weather_data.csv", index=False)


if __name__ == "__main__":
    main()
