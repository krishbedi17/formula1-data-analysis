import  fastf1
import pandas as pd
import numpy as np
# session = fastf1.get_session(2021, 1, 'R')
# session.load()  # Important to load session data
# print("\nSession Results Columns:")
# print(session.results.to_csv("Hello1.csv"))

df = pd.DataFrame()
schedule = fastf1.get_event_schedule(2018)

# Loop over the races in the 2018 season (Rounds 1 to 21)
for i in range(1, 22):
    try:
        session = fastf1.get_session(2018, i, 'R')
        session.load()
        event_name = schedule[schedule['RoundNumber'] == i]['EventName'].iloc[0]
        location = schedule[schedule['RoundNumber'] == i]['Location'].iloc[0]
        event_name = event_name.replace('Grand Prix', '').strip()

        session_results = session.results.copy()
        session_results['raceID'] = i
        session_results['year'] = 2018
        session_results['EventName'] = event_name
        session_results['Location'] = location

        df = pd.concat([df, session_results], ignore_index=True)

        print(f"Round {i} data loaded successfully.")

    except Exception as e:
        print(f"Could not load data for Round {i}: {e}")

# Save the results to a CSV file
df.to_csv("2018_data_with_race_names.csv", index=False)

