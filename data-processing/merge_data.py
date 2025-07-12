import pandas as pd


def main():
    driver_merged = pd.DataFrame()
    quali_merged = pd.DataFrame()
    race_merged = pd.DataFrame()
    weather_merged = pd.DataFrame()
    pit_stops_merged = pd.read_csv('avg_pit_stops_2018_to_2023.csv', header=0)
    schedule_merged = pd.DataFrame()

    driver_error = pd.read_csv('race_error/driver_error_probabilities.csv', header=0)
    driver_error['Probability_of_Error'] = 1 - driver_error['Probability_of_Error']
    constructor_error = pd.read_csv('race_error/team_error_probabilities.csv', header=0)


    for year in range(2018,2024):
        driver_yearly = pd.read_csv(f"driver_data/{year}_driver_data.csv")
        driver_yearly['year'] = year
        driver_merged = pd.concat([driver_merged, driver_yearly])
        quali_yearly = pd.read_csv(f"quali_data/{year}_quali_results.csv")
        quali_yearly['year'] = year
        quali_merged = pd.concat([quali_merged, quali_yearly])

        race_yearly = pd.read_csv(f"race_data/{year}_race_results.csv")
        race_merged = pd.concat([race_merged, race_yearly])

        weather_yearly = pd.read_csv(f"weather_data/{year}_weather_data.csv")
        weather_merged = pd.concat([weather_merged, weather_yearly])

        schedule_yearly = pd.read_csv(f"season_schedule/{year}_season_schedule.csv")
        schedule_yearly['year'] = year
        schedule_merged = pd.concat([schedule_merged, schedule_yearly])




    driver_merged.to_csv(f"merged_data/driver_merged.csv", index=False)
    quali_merged.to_csv(f"merged_data/quali_merged.csv", index=False)
    race_merged.to_csv(f"merged_data/race_merged.csv", index=False)
    weather_merged.to_csv(f"merged_data/weather_merged.csv", index=False)
    pit_stops_merged.to_csv(f"merged_data/pit_stops_merged.csv", index=False)
    schedule_merged.to_csv(f"merged_data/schedule_merged.csv", index=False)

    quali_merged = quali_merged.rename(columns={
        'Driver Id': 'Driver ID',
        'year': 'Year',
        'Position': 'Quali Position',
    })

    race_merged = race_merged.rename(columns={
        'Race ID': 'Round',
        'Position' : 'Race Position',
    })

    weather_merged = weather_merged.rename(columns={
        'raceID': 'Round',
        'year': 'Year',
    })
    #
    schedule_merged = schedule_merged.rename(columns={
        'year': 'Year',
        'Time' : 'Race Time',
    })

    driver_error = driver_error.rename(columns={
        'Probability_of_Error': 'Driver Confidence',
    })

    constructor_error = constructor_error.rename(columns={
        'Probability_of_Error': 'Constructor Confidence'
    })

    merged_data = quali_merged
    merged_data = pd.merge(merged_data, race_merged, on=['Driver ID', 'Year', 'Round'], how='outer')
    merged_data = pd.merge(merged_data, weather_merged, on=['Year', 'Round'], how='outer')
    merged_data = pd.merge(merged_data, pit_stops_merged, on=['Driver ID', 'Year', 'Round'], how='outer')
    merged_data = pd.merge(merged_data, schedule_merged, on=['Year', 'Round'], how='outer')
    merged_data = pd.merge(merged_data, driver_error, on=['Driver ID'], how='outer')
    merged_data = pd.merge(merged_data, constructor_error, on=['Constructor ID'], how='outer')

    merged_data = merged_data.sort_values(by=['Year', 'Round', 'Race Position'], ascending=[True, True, True])
    merged_data = merged_data.reset_index(drop=True)
    merged_data = merged_data.drop(columns=['Wins', 'Constructor Name', 'Constructor', 'EventName', 'Location', 'Time'])

    merged_data.to_csv("merged_data/merged_data.csv", index=False)

main()


