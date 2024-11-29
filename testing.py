import  fastf1 as f1
import pandas as pd
import numpy as np
# session = fastf1.get_session(2021, 1, 'R')
# session.load()  # Important to load session data
# print("\nSession Results Columns:")
# print(session.results.to_csv("Hello1.csv"))

df = pd.DataFrame()
for i in range(1,22):
    session = f1.get_session(2018, i, 'R')
    session.load()
    df = pd.concat([df, session.results], ignore_index=True)
    df['raceID'] = i

df.to_csv("2018_data.csv", index=False)

