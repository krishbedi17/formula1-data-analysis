# import pandas as pd
# from pyspark.ml.regression import DecisionTreeRegressionModel
# from pyspark.mllib.tree import DecisionTree
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
#
# def time_to_seconds(time_str):
#     if isinstance(time_str, str):
#         parts = time_str.split(':')
#         if len(parts) == 2:  # MM:SS.MS format
#             minutes, seconds = parts
#             total_seconds = int(minutes) * 60 + float(seconds)
#         elif len(parts) == 3:  # HH:MM:SS.MS format
#             hours, minutes, seconds = parts
#             total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
#         else:
#             total_seconds = float(time_str)  # If it's already in seconds
#         return total_seconds
#     return time_str
#
# def main():
#     df = pd.read_csv('merged_data/merged_data.csv')
#
#     # Split data based on years: Training on 2018-2022 and testing on 2023
#     train_data = df[df['Year'] < 2023]
#     test_data = df[df['Year'] == 2023]
#
#     # Drop rows with NaN values in the target or feature columns
#     features = ['AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindDirection', 'WindSpeed',
#                 'Q1 Time', 'Q2 Time', 'Q3 Time', 'Points', 'Fastest Lap Time', 'Quali Position', 'Total Points', 'Total Wins']
#     train_data = train_data.dropna(subset=features + ['Points', 'Driver ID'])
#     test_data = test_data.dropna(subset=features + ['Points', 'Driver ID'])
#
#     # Convert time columns to seconds
#     time_columns = ['Q1 Time', 'Q2 Time', 'Q3 Time', 'Fastest Lap Time']
#     for col in time_columns:
#         train_data.loc[:, col] = train_data[col].apply(time_to_seconds)
#         test_data.loc[:, col] = test_data[col].apply(time_to_seconds)
#
#     # Feature scaling
#     scaler = StandardScaler()
#     train_data[features] = scaler.fit_transform(train_data[features])
#     test_data[features] = scaler.transform(test_data[features])
#
#     # Set the features and target for training and testing
#     X_train = train_data[features]  # Features (input)
#     y_train = train_data['Points']  # Target (output) - Points scored by the driver
#
#     X_test = test_data[features]  # Features for testing
#     y_test = test_data['Points']  # Target for testing
#
#     # Train the model
#     model = DecisionTree()
#     model.fit(X_train, y_train)
#
#     # Make predictions
#     y_pred = model.predict(X_test)
#
#     # Evaluate the model performance using mean squared error
#     mse = mean_squared_error(y_test, y_pred)
#     print(f"Mean Squared Error: {mse:.2f}")
#
#     # Add predictions to the test data
#     test_data['Predicted Points Scored'] = y_pred
#
#     # Group by driver ID and sum the predicted points
#     driver_points = test_data.groupby('Driver ID')['Predicted Points Scored'].sum().reset_index()
#
#     # Sort drivers by total predicted points in descending order
#     driver_points = driver_points.sort_values(by='Predicted Points Scored', ascending=False)
#
#     # Print out driver IDs and their predicted total points
#     print("Driver ID and Total Predicted Points for 2023:")
#     for index, row in driver_points.iterrows():
#         print(f"{row['Driver ID']}: {row['Predicted Points Scored']:.2f} points")
#
# if __name__ == "__main__":
#     main()

import pandas as pd
from scipy.stats import spearmanr, kendalltau
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def get_accuracy(predicted_driver, predicted_position, actual_driver, actual_position, score):
    if predicted_driver == actual_driver and predicted_position == actual_position:
        return score + 1
    return score


def time_to_seconds(time_str):
    if isinstance(time_str, str):
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS.MS format
            minutes, seconds = parts
            total_seconds = int(minutes) * 60 + float(seconds)
        elif len(parts) == 3:  # HH:MM:SS.MS format
            hours, minutes, seconds = parts
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        else:
            total_seconds = float(time_str)  # If it's already in seconds
        return total_seconds
    return time_str


def main():
    # Load the dataset
    df = pd.read_csv('merged_data/merged_data.csv')

    # Split data based on years: Training on 2018-2022 and testing on 2023
    train_data = df[df['Year'] < 2023]
    test_data = df[df['Year'] == 2023]

    # Drop rows with NaN values in the target or feature columns
    features = ['AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindDirection', 'WindSpeed',
                'Q1 Time', 'Q2 Time', 'Q3 Time', 'Fastest Lap Time', 'Quali Position', 'Total Points',
                'Total Wins']

    train_data = train_data.dropna(subset=['Race Position', 'Driver ID'])
    test_data = test_data.dropna(subset=['Race Position', 'Driver ID'])

    # Convert time columns to seconds
    time_columns = ['Q1 Time', 'Q2 Time', 'Q3 Time', 'Fastest Lap Time']
    for col in time_columns:
        train_data.loc[:, col] = train_data[col].apply(time_to_seconds)
        test_data.loc[:, col] = test_data[col].apply(time_to_seconds)

    # Feature scaling
    scaler = StandardScaler()
    train_data[features] = scaler.fit_transform(train_data[features])
    test_data[features] = scaler.transform(test_data[features])

    # Set the features and target for training and testing
    X_train = train_data[features]  # Features (input)
    y_train = train_data['Race Position']  # Target (output) - Race position

    X_test = test_data[features]  # Features for testing
    y_test = test_data['Race Position']  # Target for testing

    # Train the model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Add predictions to the test data
    test_data['Predicted Race Position'] = y_pred

    # Define scoring system
    scoring_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

    # Calculate total points for each driver at the end of the season
    test_data['Predicted Points Scored'] = test_data['Predicted Race Position'].apply(
        lambda pos: scoring_system.get(pos, 0)
    )

    season_standings = test_data.groupby('Driver ID')['Predicted Points Scored'].sum().reset_index()
    season_standings = season_standings.sort_values(by='Predicted Points Scored', ascending=False)
    act_standings =  pd.read_csv("2023_driver_standings.csv")
    print(act_standings)
    # Display season standings
    print("\nSeason Standings - Total Predicted Points:")
    score = 0
    for index, row in season_standings.iterrows():
        # score = get_accuracy(row['Driver ID'],row['Predicted Race Position'] , act_standings['Driver ID'],act_standings['Position'], score)
        print(f"Driver ID: {row['Driver ID']}, Total Predicted Points: {row['Predicted Points Scored']:.2f}")

    # print(f"acc score: {score/20:.2f}")


if __name__ == "__main__":
    main()
