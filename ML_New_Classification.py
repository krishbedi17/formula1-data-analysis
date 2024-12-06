import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingRegressor, VotingClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def main():
    # Load the preprocessed dataset
    merge_data = pd.read_csv('merged_data/changed_merged_data.csv')

    # Define features and target
    selected_columns = [
        "TempCategory", "HumidityCategory", "RainfallCategory", "WindSpeedCategory",
        "WindDirectionCategory", "Constructor ID_Encoded", "Driver ID_Encoded", "Circuit ID_Encoded",
        "Quali Position", "Total Points", "Total Wins", "Driver Error", "Constructor Confidence"
    ]

    # Create Race Position Category
    merge_data['Race Position Category'] = pd.cut(
        merge_data['Race Position'], bins=[0, 3, 10, 20], labels=['Top 3', 'Top 10', 'Other']
    )

    # merge_data.to_csv("Before_model.csv", index=False)

    # Drop rows with missing target or features
    merge_data = merge_data.dropna(subset=['Race Position Category'] + selected_columns)

    # Split dataset into training and testing sets
    train_data = merge_data[merge_data['Year'].between(2018, 2022)]
    test_data = merge_data[merge_data['Year'] == 2023]

    X_train = train_data[selected_columns]
    y_train = train_data['Race Position Category']
    X_test = test_data[selected_columns]
    y_test = test_data['Race Position Category']

    clf1 = DecisionTreeClassifier(max_depth=15, min_samples_split=5, random_state=42)
    clf2 = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=10, min_samples_leaf=2, random_state=42)
    clf3 = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    clf4 = KNeighborsClassifier(n_neighbors=5)
    clf5 = SVC(kernel='rbf', probability=True, random_state=42)

    # Define Voting Classifier
    voting_clf = VotingClassifier(
        estimators=[
            ('dt', clf1),
            ('rf', clf2),
            ('gb', clf3),
            ('knn', clf4),
            ('svc', clf5)
        ],
        voting='hard'  # Use soft voting for probability-based averaging
    )

    # Train the ensemble
    voting_clf.fit(X_train, y_train)

    # Make predictions
    y_pred = voting_clf.predict(X_test)

    # print(f"Best parameters for Random Forest: {grid_search_rf.best_params_}")
    # Evaluate the model
    # print("Classification Report:\n", classification_report(y_test, y_pred))
    # print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Initialize the Random Forest Classifier
    # rf_classifier = RandomForestClassifier(
    #     n_estimators=200,  # Number of trees
    #     max_depth=10,  # Maximum depth of the tree
    #     min_samples_split=5,  # Minimum samples required to split a node
    #     min_samples_leaf=2,  # Minimum samples required at a leaf node
    #     # class_weight={'Top 3': 2, 'Top 10': 1.5, 'Other': 1},
    #     random_state=42  # Seed for reproducibility
    # )
    #
    # # Train the classifier
    # rf_classifier.fit(X_train, y_train)
    #
    # # Predict on the test set
    # y_pred = rf_classifier.predict(X_test)
    #
    # Evaluate the model
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Add predictions to the test dataset
    test_data['Predicted Race Position Category'] = y_pred
    #
    # # Save predictions to a CSV file
    test_data.to_csv('ML_Outputs/classifier_predictions.csv', index=False)
    print("Predictions saved to 'ML_Outputs/classifier_predictions.csv'.")


main()