import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, accuracy_score

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
                'Q1 Time', 'Q2 Time', 'Q3 Time', 'Points', 'Fastest Lap Time', 'Quali Position', 'Total Points',
                'Total Wins']
    print(train_data.count())
    train_data = train_data.dropna(subset=['Points', 'Driver ID'])
    test_data = test_data.dropna(subset=['Points', 'Driver ID'])
    print(train_data.count())
    return
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
    y_train = train_data['Points']  # Target (output) - Points scored by the driver

    X_test = test_data[features]  # Features for testing
    y_test = test_data['Points']  # Target for testing

    # Train the model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model performance using mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")

    # Add predictions to the test data
    test_data['Predicted Points Scored'] = y_pred

    # Initialize variables for winner prediction
    actual_winners = []
    predicted_winners = []

    # Feed the model round by round and predict the points scored
    print("Round-by-Round Predicted Points for 2023:")

    # Iterate over the test data by race (round)
    for round_num, round_data in test_data.groupby('Round'):
        print(f"\nPredictions for Race {round_num}:")

        # Find the actual winner (Race Position == 1)
        actual_winner = round_data[round_data['Race Position'] == 1]['Driver ID'].iloc[0]
        actual_winners.append(actual_winner)

        predicted_winner = round_data.loc[round_data['Predicted Points Scored'].idxmax()]['Driver ID']
        predicted_winners.append(predicted_winner)

        for _, driver_data in round_data.iterrows():
            driver_id = driver_data['Driver ID']
            predicted_points = driver_data['Predicted Points Scored']
            print(f"Driver ID: {driver_id}, Predicted Points: {predicted_points:.2f}")

    accuracy = accuracy_score(actual_winners, predicted_winners)
    print(f"\nAccuracy of predicting race winners: {accuracy * 100:.2f}%")


main()