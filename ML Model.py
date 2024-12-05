# # # Import necessary libraries
# # import pandas as pd
# # from sklearn.model_selection import train_test_split
# # from sklearn.impute import SimpleImputer
# # from sklearn.ensemble import RandomForestRegressor
# # from sklearn.preprocessing import StandardScaler
# # from sklearn.pipeline import make_pipeline
# #
# # # Load the merged dataset (replace with actual path to dataset)
# # merged_data = pd.read_csv('merged_data/merged_data.csv')
# #
# # # Select relevant columns for features and target
# # selected_columns = [
# #     'Quali Position', 'AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed',
# #     'Points', 'Total Points', 'Total Wins'
# # ]
# #
# # # Target variable
# # target = 'Race Position'
# #
# # # Filter the dataset to include only selected columns and drop rows with missing target values
# # cleaned_data = merged_data[selected_columns + [target]].dropna(subset=[target])
# #
# # # Define features (X) and target (y)
# # X_cleaned = cleaned_data[selected_columns]
# # y_cleaned = cleaned_data[target]
# #
# # # Split data into train and test sets
# # X_train, X_test, y_train, y_test = train_test_split(X_cleaned, y_cleaned, test_size=0.2, random_state=42)
# #
# # # Impute missing values in features
# # # imputer = SimpleImputer()
# # # X_train_imputed = imputer.fit_transform(X_train)
# # # X_test_imputed = imputer.transform(X_test)
# #
# # # Impute missing values in the target column
# # # y_train_cleaned_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
# # # y_test_cleaned_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()
# #
# # # Manually set hyperparameters
# # n_estimators = 200  # Number of trees in the forest
# # max_depth = 15       # Maximum depth of the trees
# # min_samples_split = 5 # Minimum number of samples required to split an internal node
# # min_samples_leaf = 2  # Minimum number of samples required to be at a leaf node
# #
# # # Initialize and train the RandomForestRegressor model with the chosen hyperparameters
# # model = make_pipeline(
# #     StandardScaler(),
# #     RandomForestRegressor(
# #         n_estimators=n_estimators,
# #         max_depth=max_depth,
# #         min_samples_split=min_samples_split,
# #         min_samples_leaf=min_samples_leaf,
# #         random_state=42
# #     )
# # )
# #
# # # Fit the model
# # model.fit(X_train, y_train)
# #
# # # Make predictions with the trained model
# # y_pred = model.predict(X_test)
# #
# # # Evaluate the model by checking the predicted race positions against actual positions
# # test_data_cleaned = X_test.copy()
# # test_data_cleaned['Predicted Race Position'] = y_pred
# #
# # # Merge predictions with actual race positions from the dataset
# # merged_standings = test_data_cleaned[['Predicted Race Position']].merge(
# #     merged_data[['Driver ID', 'Race Position']], left_index=True, right_index=True, how='left'
# # )
# #
# # # Calculate prediction accuracy (rounded predictions)
# # merged_standings['Correct Prediction'] = merged_standings['Predicted Race Position'].round() == merged_standings['Race Position']
# #
# # # Calculate accuracy
# # correct_predictions = merged_standings['Correct Prediction'].sum()
# # total_predictions = len(merged_standings)
# # accuracy = (correct_predictions / total_predictions) * 100
# #
# # # Display the results
# # print(f"Accuracy of Model: {accuracy}%")
# # print(merged_standings.to_csv("hello.csv"))
#
# # Import necessary libraries
# import pandas as pd
# from pyspark.ml.classification import DecisionTreeClassifier
# from pyspark.ml.regression import DecisionTreeRegressor, RandomForestRegressionModel
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingClassifier, VotingRegressor
# from sklearn.neighbors import KNeighborsRegressor
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import make_pipeline
# from sklearn.svm import SVC, SVR
#
# # Load the merged dataset (replace with actual path to dataset)
# merged_data = pd.read_csv('merged_data/merged_data.csv')
#
# # Select relevant columns for features and target
# selected_columns = [
#     'Quali Position', 'AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed',
#     'Points', 'Total Points', 'Total Wins'
# ]
#
# # Target variable
# target = 'Race Position'
#
# # Filter the dataset to include only selected columns
# cleaned_data = merged_data[selected_columns + [target, 'Year']].dropna(subset=[target])
#
# # Split the data into training and testing based on the Year column
# train_data = cleaned_data[cleaned_data['Year'].between(2018, 2022)]  # Data for years 2018-2022
# test_data = cleaned_data[cleaned_data['Year'] == 2023]  # Data for the year 2023
#
# # Define features (X) and target (y) for training
# X_train = train_data[selected_columns]
# y_train = train_data[target]
#
# # Define features (X) and target (y) for testing
# X_test = test_data[selected_columns]
# y_test = test_data[target]
#
# # Initialize the RandomForestRegressor model with manually set hyperparameters
# n_estimators = 200  # Number of trees in the forest
# max_depth = 15       # Maximum depth of the trees
# min_samples_split = 5 # Minimum number of samples required to split an internal node
# min_samples_leaf = 2  # Minimum number of samples required to be at a leaf node
#
# # Initialize and train the model with the chosen hyperparameters
# model = make_pipeline(
#     StandardScaler(),
#     RandomForestRegressor(
#         n_estimators=n_estimators,
#         max_depth=max_depth,
#         min_samples_split=min_samples_split,
#         min_samples_leaf=min_samples_leaf,
#         random_state=42
#     )
# )
# # Initialize classifiers for the Voting Classifier
# clf1 = DecisionTreeRegressor(max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
# clf2 = RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
# clf3 = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
# clf4 = KNeighborsRegressor(n_neighbors=5)
# clf5 = SVR(C=1.0, epsilon=0.1)
#
# # Create a Voting Regressor (using 'hard' voting means majority prediction)
# voting_clf = VotingRegressor(estimators=[
#     ('dt', clf1),
#     ('rf', clf2),
#     ('gb', clf3),
#     ('knn', clf4),
#     ('svr', clf5)
# ])
#
# # Train the Voting Classifier
# voting_clf.fit(X_train, y_train)
#
# # # Fit the model on training data (2018-2022)
# # model.fit(X_train, y_train)
#
# # # Make predictions for the 2023 data
# # y_pred = model.predict(X_test)
# y_pred = voting_clf.predict(X_test)
#
# # Evaluate the model by checking the predicted race positions against actual positions
# test_data_cleaned = X_test.copy()
# test_data_cleaned['Predicted Race Position'] = y_pred
#
# # Merge predictions with actual race positions from the dataset
# merged_standings = test_data_cleaned[['Predicted Race Position']].merge(
#     test_data['Race Position'], left_index=True, right_index=True, how='left'
# )
#
# # Calculate prediction accuracy (rounded predictions)
# merged_standings['Correct Prediction'] = merged_standings['Predicted Race Position'].round() == merged_standings['Race Position']
#
# # Calculate accuracy
# correct_predictions = merged_standings['Correct Prediction'].sum()
# total_predictions = len(merged_standings)
# accuracy = (correct_predictions / total_predictions) * 100
#
# # Display the results
# print(f"Accuracy of Model on 2023 data: {accuracy}%")
# # Optionally, save the results to a CSV file
# merged_standings.to_csv("predictions_2023.csv", index=False)
# Import necessary libraries
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
# from sklearn.neighbors import KNeighborsRegressor
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import make_pipeline
# from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor
#
# points_system = {
#     1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
#     6: 8, 7: 6, 8: 4, 9: 2, 10: 1
# }
#
#
# def get_points(predicted_position):
#     # Return points for the predicted position, or 0 if position is > 10 (no points)
#     return points_system.get(predicted_position, 0)
#
# # Load the merged dataset (replace with actual path to dataset)
# merged_data = pd.read_csv('merged_data/changed_merged_data.csv')
#
# # Select relevant columns for features and target
# selected_columns = [
#     'Quali Position', 'AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed',
#     'Points', 'Total Points', 'Total Wins','Q1 Time','Q2 Time','Q3 Time'
# ]
#
# # Target variable
# target = 'Race Position'
#
# # Filter the dataset to include only selected columns
# cleaned_data = merged_data[selected_columns + [target, 'Year']].dropna(subset=[target,'Quali Position'])
# # nan_rows = cleaned_data[cleaned_data.isna().any(axis=1)]
# # nan_rows.to_csv("nan.csv")
# # Split the data into training and testing based on the Year column
# train_data = cleaned_data[cleaned_data['Year'].between(2018, 2022)]  # Data for years 2018-2022
# test_data = cleaned_data[cleaned_data['Year'] == 2023]  # Data for the year 2023
#
# # Define features (X) and target (y) for training
# X_train = train_data[selected_columns]
# y_train = train_data[target]
#
# # Define features (X) and target (y) for testing
# X_test = test_data[selected_columns]
# y_test = test_data[target]
#
# # Initialize individual regression models with hyperparameters
# clf1 = DecisionTreeRegressor(max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
# clf2 = RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
# clf3 = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
# clf4 = KNeighborsRegressor(n_neighbors=5)
# clf5 = SVR(C=1.0, epsilon=0.1)
#
# # Create a Voting Regressor (using 'hard' voting means majority prediction)
# voting_clf = VotingRegressor(estimators=[
#      ('dt', clf1),
#     ('rf', clf2),
#       ('gb', clf3),
#      # ('knn', clf4),
#     # ('svr', clf5)
# ])
#
# # Initialize pipeline with StandardScaler and Voting Regressor
# model = make_pipeline(StandardScaler(), voting_clf)
#
# # Train the model on the training data (2018-2022)
# model.fit(X_train, y_train)
#
# # Make predictions for the 2023 data
# y_pred = model.predict(X_test)
#
# # Evaluate the model by checking the predicted race positions against actual positions
# test_data_cleaned = X_test.copy()
# test_data_cleaned['Predicted Race Position'] = y_pred
#
# # Merge predictions with actual race positions from the dataset
# merged_standings = test_data_cleaned[['Predicted Race Position']].merge(
#     test_data[[ 'Race Position']], left_index=True, right_index=True, how='left'
# )
#
# # Calculate prediction accuracy (rounded predictions)
# merged_standings['Correct Prediction'] = merged_standings['Predicted Race Position'].round() == merged_standings['Race Position']
#
# # Calculate accuracy
# correct_predictions = merged_standings['Correct Prediction'].sum()
# total_predictions = len(merged_standings)
# accuracy = (correct_predictions / total_predictions) * 100
#
# merged_standings['Predicted Points'] = merged_standings['Predicted Race Position'].round().apply(get_points)
#
# # Display the results
# print(f"Accuracy of Model on 2023 data: {accuracy}%")
#
# # Optionally, save the results to a CSV file
# merged_standings.to_csv("predictions_2023.csv", index=False)
#
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

points_system = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}

def get_points(predicted_position):
    # Return points for the predicted position, or 0 if position is > 10 (no points)
    return points_system.get(predicted_position, 0)

# Load the merged dataset (replace with actual path to dataset)
merged_data = pd.read_csv('merged_data/changed_merged_data.csv')

# Select relevant columns for features and target
selected_columns = [
    'Quali Position', 'AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed',
     'Total Points', 'Total Wins', 'Q1 Time', 'Q2 Time', 'Q3 Time'
]

# Target variable
target = 'Race Position'

# Filter the dataset to include only selected columns
cleaned_data = merged_data[selected_columns + [target, 'Year', 'Driver ID', 'Constructor ID']].dropna(subset=[target, 'Quali Position'])

# Split the data into training and testing based on the Year column
train_data = cleaned_data[cleaned_data['Year'].between(2018, 2022)]  # Data for years 2018-2022
test_data = cleaned_data[cleaned_data['Year'] == 2023]  # Data for the year 2023

# Define features (X) and target (y) for training
X_train = train_data[selected_columns]
y_train = train_data[target]

# Define features (X) and target (y) for testing
X_test = test_data[selected_columns]
y_test = test_data[target]

# Initialize individual regression models with hyperparameters
clf1 = DecisionTreeRegressor(max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
clf2 = RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42)
clf3 = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
clf4 = KNeighborsRegressor(n_neighbors=5)
clf5 = SVR(C=1.0, epsilon=0.1)

# Create a Voting Regressor (using 'hard' voting means majority prediction)
voting_clf = VotingRegressor(estimators=[
    ('dt', clf1),
    ('rf', clf2),
    ('gb', clf3),
])

# Initialize pipeline with StandardScaler and Voting Regressor
model = make_pipeline(StandardScaler(), voting_clf)

# Train the model on the training data (2018-2022)
model.fit(X_train, y_train)

# Make predictions for the 2023 data
y_pred = model.predict(X_test)

# Evaluate the model by checking the predicted race positions against actual positions
test_data_cleaned = X_test.copy()
test_data_cleaned['Predicted Race Position'] = y_pred

# Merge predictions with actual race positions and driver & constructor IDs from the dataset
merged_standings = test_data_cleaned[['Predicted Race Position']].merge(
    test_data[['Race Position', 'Driver ID', 'Constructor ID']], left_index=True, right_index=True, how='left'
)

# Calculate prediction accuracy (rounded predictions)
merged_standings['Correct Prediction'] = merged_standings['Predicted Race Position'].round() == merged_standings['Race Position']

# Calculate accuracy
correct_predictions = merged_standings['Correct Prediction'].sum()
total_predictions = len(merged_standings)
accuracy = (correct_predictions / total_predictions) * 100

# Apply points system to predicted race positions
merged_standings['Predicted Points'] = merged_standings['Predicted Race Position'].round().apply(get_points)
merged_standings.to_csv('merged_standings.csv', index=False)

# Sum predicted points grouped by Driver ID
driver_points = merged_standings.groupby('Driver ID')['Predicted Points'].sum().reset_index().sort_values('Predicted Points', ascending=False)

# Sum predicted points grouped by Constructor ID
constructor_points = merged_standings.groupby('Constructor ID')['Predicted Points'].sum().reset_index().sort_values('Predicted Points', ascending=False)

# Display the summed points for each driver and constructor
print(driver_points)
print(constructor_points)

# Save the driver points and constructor points to CSV files
driver_points.to_csv("driver_points_2023.csv", index=False)
constructor_points.to_csv("constructor_points_2023.csv", index=False)

# Optionally, display the results
print(f"Accuracy of Model on 2023 data: {accuracy}%")
