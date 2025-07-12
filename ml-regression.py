import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def main():
    merge_data = pd.read_csv('merged_data/changed_merged_data.csv')

    selected_columns = [
        "TempCategory", "HumidityCategory", "RainfallCategory", "WindSpeedCategory",
        "WindDirectionCategory", "Constructor ID_Encoded", "Driver ID_Encoded", "Circuit ID_Encoded",
        "Quali Position", "Total Points", "Total Wins", "Driver Confidence", "Constructor Confidence"
    ]
    target = 'Points'

    merge_data = merge_data.dropna(
        subset=[target, 'Quali Position', 'Driver Error'])


    train_data = merge_data[merge_data['Year'].between(2018, 2022)]
    test_data = merge_data[merge_data['Year'] == 2023]


    X_train = train_data[selected_columns]
    y_train = train_data[target]
    X_test = test_data[selected_columns]
    y_test = test_data[target]

    rf_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )


    rf_model.fit(X_train, y_train)


    y_pred = rf_model.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"Random Forest RMSE: {rmse:.2f}")

    test_data['Predicted Race Position'] = y_pred

    test_data.to_csv('model-predictions/rf_predictions.csv', index=False)
    print("Predictions saved to 'ML_Outputs/rf_predictions.csv'.")

if __name__ == "__main__":
    main()