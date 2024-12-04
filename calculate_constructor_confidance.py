from statistics import mean

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def load_race_data(year):
    return pd.read_csv(f"race_data/{year}_race_results.csv")


def data_join_for_pitStop(year, avg_pit_stops_df):
    race_df = load_race_data(year)
    race_df = race_df[['Race ID','Driver ID','Constructor']]
    merged_df = pd.merge(race_df, avg_pit_stops_df,
                         left_on=['Driver ID', 'Race ID'],
                         right_on=['Driver ID', 'Round'],
                         how='inner')
    merged_df = merged_df.drop(columns=['Race ID'])
    return merged_df

def getIntermediate(mean,stddev):
    if stddev == 0:
        return mean
    else:
        return mean*stddev


def main():
    avg_pit_stops_df =  pd.read_csv("avg_pit_stops_2018_to_2023.csv")

    merged_data = []
    status_impact_values ={
        "Engine": -1.0,
        "Gearbox": -1.0,
        "Transmission": -1.0,
        "Clutch": -1.0,
        "Hydraulics": -1.0,
        "Electrical": -1.0,
        "Radiator": -1.0,
        "Suspension": -1.0,
        "Brakes": -1.0,
        "Differential": -1.0,
        "Overheating": -0.9,
        "Mechanical": -0.9,
        "Tyre": -0.8,
        "Driver Seat": -0.8,
        "Puncture": -0.8,
        "Driveshaft": -1.0,
        "Fuel pressure": -0.9,
        "Water pressure": -0.9,
        "Refuelling": -0.8,
        "Wheel": -0.9,
        "Throttle": -0.8,
        "Steering": -0.9,
        "Technical": -0.9,
        "Electronics": -1.0,
        "Broken wing": -0.7,
        "Heat shield fire": -1.0,
        "Exhaust": -0.9,
        "Oil leak": -0.8,
        "Wheel rim": -0.7,
        "Water leak": -0.7,
        "Fuel pump": -0.9,
        "Track rod": -0.8,
        "Oil pressure": -0.8,
        "Engine fire": -1.0,
        "Tyre puncture": -0.8,
        "Out of fuel": -1.0,
        "Front wing": -0.8,
        "Wheel nut": -0.7,
        "Pneumatics": -0.8,
        "Rear wing": -0.7,
        "Fire": -1.0,
        "Wheel bearing": -0.7,
        "Physical": -0.7,
        "Fuel system": -0.9,
        "Oil line": -0.9,
        "Fuel rig": -0.8,
        "Launch control": -0.7,
        "Fuel": -0.8,
        "Power loss": -0.9,
        "Vibrations": -0.7,
        "107% Rule": -1.0,
        "Drivetrain": -1.0,
        "Ignition": -0.9,
        "Chassis": -1.0,
        "Battery": -0.8,
        "Stalled": -0.9,
        "Halfshaft": -1.0,
        "Crankshaft": -1.0,
        "Safety concerns": -0.9,
        "Not restarted": -0.9,
        "Alternator": -0.8,
        "Underweight": -1.0,
        "Safety belt": -0.8,
        "Oil pump": -0.8,
        "Fuel leak": -0.9,
        "Excluded": -1.0,
        "Did not prequalify": -1.0,
        "Injection": -0.8,
        "Distributor": -0.8,
        "Turbo": -0.8,
        "CV joint": -0.8,
        "Water pump": -0.8,
        "Spark plugs": -0.8,
        "Fuel pipe": -0.8,
        "Oil pipe": -0.8,
        "Axle": -0.8,
        "Water pipe": -0.8,
        "Magneto": -0.9,
        "Supercharger": -0.8,
        "Engine misfire": -1.0,
        "Power Unit": -1.0,
        "ERS": -0.9,
        "Brake duct": -0.7,
        "Seat": -0.7,
        "Undertray": -0.7,
        "Cooling system": -0.9,
        "Finished": 1.0,
        "Disqualified": -0.5,
        "Accident": -0.4,
        "Collision": -0.4,
        "+1 Lap": -0.2,
        "+2 Laps": -0.2,
        "+3 Laps": -0.2,
        "+4 Laps": -0.2,
        "+5 Laps": -0.2,
        "+6 Laps": -0.2,
        "+7 Laps": -0.2,
        "+8 Laps": -0.2,
        "+9 Laps": -0.2,
        "Spun off": -0.4,
        "Retired": -0.3,
        "+11 Laps": -0.1,
        "+17 Laps": -0.1,
        "+13 Laps": -0.1,
        "Withdrew": -0.5,
        "+12 Laps": -0.1,
        "+26 Laps": -0.1,
        "Not classified": -0.5,
        "Injured": -0.5,
        "Safety": -0.3,
        "Did not qualify": -0.5,
        "Injury": -0.5,
        "+10 Laps": -0.1,
        "Safety concerns": -0.3,
        "Driver unwell": 0,
        "Fatal accident": 0,
        "Eye injury": 0,
        "+14 Laps": -0.1,
        "+15 Laps": -0.1,
        "+25 Laps": -0.1,
        "+18 Laps": -0.1,
        "+22 Laps": -0.1,
        "+16 Laps": -0.1,
        "+24 Laps": -0.1,
        "+29 Laps": -0.1,
        "+23 Laps": -0.1,
        "+21 Laps": -0.1,
        "+44 Laps": -0.1,
        "+30 Laps": -0.1,
        "+19 Laps": -0.1,
        "+46 Laps": -0.1,
        "+20 Laps": -0.1,
        "+42 Laps": -0.1,
        "Collision damage": 0,
        "Damage": -0.3,
        "Debris": 0,
        "Illness": 0
    }

    for year in range(2018, 2023):
        merged_df = data_join_for_pitStop(year, avg_pit_stops_df)
        merged_data.append(merged_df)

    merged_df = pd.concat(merged_data)
    merged_df = merged_df.groupby(['Constructor','Round','Year'])[['Mean','StdDev']].mean().reset_index()
    calculate_intermediate = np.vectorize(getIntermediate)
    merged_df['intermediate'] = calculate_intermediate(merged_df['Mean'],merged_df['StdDev'])
    merged_df['PitStopComponent'] = 1.0/merged_df['intermediate']
    scaler = MinMaxScaler()
    merged_df['PitStopComponent'] = scaler.fit_transform(merged_df[['PitStopComponent']])
    merged_df['PitStopComponent'] = (merged_df['PitStopComponent'] * 100).round(3)

    race_data_status = []
    for year in range(2018, 2023):
        race_df = load_race_data(year)
        race_df = race_df[['Race ID','Constructor','Status']]
        race_df['Year'] = year
        race_data_status.append(race_df)
    race_data = pd.concat(race_data_status)
    race_data["status_value"] = race_data["Status"].apply(lambda status: status_impact_values.get(status, 0))
    status_component_df = race_data.groupby(['Constructor', 'Race ID','Year'])['status_value'].sum().reset_index()
    status_component_df['StatusComponent'] = scaler.fit_transform(status_component_df[['status_value']])
    merged_df = pd.merge(status_component_df,merged_df,
                         left_on=['Constructor', 'Race ID','Year'],
                         right_on=['Constructor', 'Round','Year'], how='inner')
    # merged_df = merged_df.join(race_data_status,
    #                      left_on=['Driver ID', 'Race ID'],
    #                      right_on=['Driver ID', 'Round'],
    #                      how='inner')
    merged_df['ConstructorConfidance'] = merged_df['PitStopComponent']*merged_df['status_value']
    merged_df.to_csv("constructor_confidance.csv", index=False)
    # # Save the final merged data to a new CSV
    # final_df.to_csv("merged_race_data_with_avg_pit_stops_2018_to_2022.csv", index=False)
    # print("Merged data saved to merged_race_data_with_avg_pit_stops_2018_to_2022.csv")

main()
