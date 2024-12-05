import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the data (replace with the correct path to your dataset)
data = pd.read_csv('merged_data/merged_data.csv')  # Replace with the correct path to your dataset

# Data Preprocessing
def preprocess_data(df):
    # Create a copy of the dataframe
    df_processed = df.copy()

    # Select relevant features for prediction
    numeric_columns = [
        'Quali Position', 'Race Position', 'Points',
        'Fastest Lap Avg Speed (kph)', 'Total Points',
        'Total Wins', 'AirTemp', 'Humidity', 'TrackTemp', 'WindSpeed'
    ]

    # Convert columns to numeric, coercing errors to NaN
    for col in numeric_columns:
        df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')

    # Handle missing values (fill with the median)
    for col in numeric_columns:
        df_processed[col] = df_processed[col].fillna(df_processed[col].median())

    # Encode categorical variables (Driver ID and Constructor ID)
    le_driver = LabelEncoder()
    le_constructor = LabelEncoder()

    df_processed['Driver ID'] = le_driver.fit_transform(df_processed['Driver ID'].astype(str))
    df_processed['Constructor ID'] = le_constructor.fit_transform(df_processed['Constructor ID'].astype(str))

    return df_processed, le_driver  # Return the LabelEncoder for Driver ID

# Preprocess the data
processed_data, le_driver = preprocess_data(data)

# Add back the Year column
processed_data['Year'] = data['Year']

# Create a mapping of Driver ID to Driver First Name
driver_name_mapping = dict(zip(data['Driver ID'], data['Driver First Name']))

# Separate training and test data (using 2018-2022 for training and 2023 for testing)
train_data = processed_data[processed_data['Year'] < 2023]
test_data = processed_data[processed_data['Year'] == 2023]

# Define features (X) and target (y)
X_train = train_data[[
    'Driver ID', 'Constructor ID', 'Quali Position',
    'Race Position', 'Fastest Lap Avg Speed (kph)',
    'Total Points', 'Total Wins',
    'AirTemp', 'Humidity', 'TrackTemp', 'WindSpeed', 'Year'
]]
y_train = train_data['Points']

X_test = test_data[[
    'Driver ID', 'Constructor ID', 'Quali Position',
    'Race Position', 'Fastest Lap Avg Speed (kph)',
    'Total Points', 'Total Wins',
    'AirTemp', 'Humidity', 'TrackTemp', 'WindSpeed', 'Year'
]]
y_test = test_data['Points']

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train_scaled, y_train)

# Predict and evaluate
y_pred_rf = rf_regressor.predict(X_test_scaled)

# Cap the predicted points at a maximum of 25 (maximum points in F1 race)
y_pred_rf = np.clip(y_pred_rf, 0, 25)  # Ensure no predicted points are higher than 25

# Evaluation Metrics for Random Forest
print("Random Forest Regression Evaluation Metrics:")
print("Mean Squared Error:", mean_squared_error(y_test, y_pred_rf))
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred_rf))
print("R-squared Score:", r2_score(y_test, y_pred_rf))

# Feature Importance Visualization (Random Forest)
plt.figure(figsize=(10, 6))
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf_regressor.feature_importances_
}).sort_values('importance', ascending=False)

sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Feature Importance for F1 Points Prediction (Random Forest)')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.tight_layout()
plt.show()

# Scatter plot of actual vs predicted points (Random Forest)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Points')
plt.ylabel('Predicted Points')
plt.title('Actual vs Predicted Points (Random Forest)')
plt.tight_layout()
plt.show()

# ------------------------------
# Predict the Winning Driver for 2023
# ------------------------------
# Get the predicted points for 2023
test_data.loc[:, 'Predicted Points'] = rf_regressor.predict(X_test_scaled)  # Fix SettingWithCopyWarning

# Cap the predicted points at a maximum of 25 (in case it's not already capped)
test_data['Predicted Points'] = np.clip(test_data['Predicted Points'], 0, 25)

# Print the Driver ID and Driver Name for all drivers in 2023 with predicted points
print("\nDriver ID and Driver Name with Predicted Points for 2023:")
for index, row in test_data.iterrows():
    driver_id = row['Driver ID']
    driver_name = driver_name_mapping[le_driver.inverse_transform([driver_id])[0]]  # Inverse transform the encoded driver ID
    predicted_points = row['Predicted Points']
    print(f"Driver ID: {driver_id}, Driver Name: {driver_name}, Predicted Points: {predicted_points}")

# ----------------------------
# Plot the predicted points
# ----------------------------
plt.figure(figsize=(10, 6))
sns.barplot(x='Driver ID', y='Predicted Points', data=test_data.sort_values('Predicted Points', ascending=False))
plt.title('Predicted Points for 2023 Drivers')
plt.xlabel('Driver ID')
plt.ylabel('Predicted Points')
plt.tight_layout()
plt.show()
