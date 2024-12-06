import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def main():
    # Load the preprocessed dataset
    merge_data = pd.read_csv('merged_data/changed_merged_data.csv')

    # Define features and target
    selected_columns = [
        "TempCategory", "HumidityCategory", "RainfallCategory", "WindSpeedCategory",
        "WindDirectionCategory", "Constructor ID_Encoded", "Driver ID_Encoded", "Circuit ID_Encoded",
        "Quali Position", "Total Points", "Total Wins", "Driver Error", "Constructor Confidence"
    ]
    target = 'Points'

    merge_data = merge_data.dropna(
        subset=[target, 'Quali Position', 'Driver Error'])


    # Split the dataset into training and testing sets
    train_data = merge_data[merge_data['Year'].between(2018, 2022)]
    test_data = merge_data[merge_data['Year'] == 2023]


    X_train = train_data[selected_columns]
    y_train = train_data[target]
    X_test = test_data[selected_columns]
    y_test = test_data[target]

    # Initialize the Random Forest Regressor
    rf_model = RandomForestRegressor(
        n_estimators=200,       # Number of trees in the forest
        max_depth=15,           # Maximum depth of the tree
        min_samples_split=5,    # Minimum number of samples required to split an internal node
        min_samples_leaf=2,     # Minimum number of samples required to be at a leaf node
        random_state=42         # Seed for reproducibility
    )

    # Train the model
    rf_model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf_model.predict(X_test)

    # Evaluate the model
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"Random Forest RMSE: {rmse:.2f}")

    # Add predictions to the test dataset
    test_data['Predicted Race Position'] = y_pred

    # Save predictions to a CSV file
    test_data.to_csv('ML_Outputs/rf_predictions.csv', index=False)
    print("Predictions saved to 'ML_Outputs/rf_predictions.csv'.")

if __name__ == "__main__":
    main()