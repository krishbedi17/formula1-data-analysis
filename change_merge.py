import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, StandardScaler


def check_data(value):
    if value == "" or pd.isna(value):
        return 0
    return 1



# Define categorization functions
def categorize_temperature(temp):
    if temp < 15:
        return "Cold"
    elif 15 <= temp < 25:
        return "Warm"
    else:
        return "Hot"

def categorize_humidity(humidity):
    if humidity < 30:
        return "Dry"
    elif 30 <= humidity < 60:
        return "Moderate"
    else:
        return "Humid"

def categorize_rainfall(rainfall):
    return "Wet" if rainfall else "Dry"

def categorize_wind_speed(speed):
    if speed < 1:
        return "Calm"
    elif 1 <= speed < 3:
        return "Breezy"
    elif 3 <= speed < 5:
        return "Windy"
    else:
        return "Strong Winds"

def categorize_wind_direction(direction):
    if 0 <= direction < 45 or 315 <= direction <= 360:
        return "North"
    elif 45 <= direction < 135:
        return "East"
    elif 135 <= direction < 225:
        return "South"
    else:
        return "West"

def main():
    merge_data = pd.read_csv('merged_data/merged_data.csv')
    merge_data['Q1 Time'] = merge_data['Q1 Time'].apply(check_data)
    merge_data['Q2 Time'] = merge_data['Q2 Time'].apply(check_data)
    merge_data['Q3 Time'] = merge_data['Q3 Time'].apply(check_data)

    merge_data["TempCategory"] = merge_data["AirTemp"].apply(categorize_temperature)
    merge_data["HumidityCategory"] = merge_data["Humidity"].apply(categorize_humidity)
    merge_data["RainfallCategory"] = merge_data["Rainfall"].apply(categorize_rainfall)
    merge_data["WindSpeedCategory"] = merge_data["WindSpeed"].apply(categorize_wind_speed)
    merge_data["WindDirectionCategory"] = merge_data["WindDirection"].apply(categorize_wind_direction)

    # Encode categorical columns using Label Encoding
    categorical_columns = ["TempCategory", "HumidityCategory", "RainfallCategory", "WindSpeedCategory", "WindDirectionCategory"]



    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        merge_data[col] = le.fit_transform(merge_data[col])
        label_encoders[col] = le  # Store the encoder for later use if needed

    for col in ["Constructor ID", "Driver ID", "Circuit ID"]:
        le = LabelEncoder()
        merge_data[f"{col}_Encoded"] = le.fit_transform(merge_data[col])  # Create new column with encoded values
        label_encoders[col] = le

        continuous_features = [ "Total Points", "Total Wins"]

        # Apply StandardScaler to continuous features
        scaler = StandardScaler()
        merge_data[continuous_features] = scaler.fit_transform(merge_data[continuous_features])

    merge_data.to_csv('merged_data/changed_merged_data.csv', index=False)

main()
