import fastf1
import pandas as pd

df = pd.DataFrame()
schedule = fastf1.get_event_schedule(2020)

for i in range(1, 18):
    try:
        session = fastf1.get_session(2020, i, 'R')
        session.load()

        lap_data = session.laps
        rows = []
        for driver in lap_data['Driver'].unique():
            fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            if fastest_lap is not None and not fastest_lap.empty:
                fastest_lap_time = fastest_lap.LapTime
            else:
                fastest_lap_time = pd.NA
            rows.append({"Driver": driver, "FastestLap": fastest_lap_time})

        round_df = pd.DataFrame(rows)

        # best_bottas = session.laps.pick_driver('BOT').pick_fastest()
        event_name = schedule[schedule['RoundNumber'] == i]['EventName'].iloc[0]
        event_name = event_name.replace('Grand Prix', '').strip()

        # Add race metadata
        round_df['RaceID'] = i
        round_df['year'] = 2020
        round_df['EventName'] = event_name

        df = pd.concat([df, round_df], ignore_index=True)

        print(f"Round {i} data loaded successfully.")

    except Exception as e:
        print(f"Could not load data for Round {i}: {e}")

df.to_csv("2020_fastestlap.csv", index=False)

