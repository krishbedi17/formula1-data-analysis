import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


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

    merge_data.to_csv("Before_model.csv", index=False)

    # Drop rows with missing target or features
    merge_data = merge_data.dropna(subset=['Race Position Category'] + selected_columns)

    # Split dataset into training and testing sets
    train_data = merge_data[merge_data['Year'].between(2018, 2022)]
    test_data = merge_data[merge_data['Year'] == 2023]

    X_train = train_data[selected_columns]
    y_train = train_data['Race Position Category']
    X_test = test_data[selected_columns]
    y_test = test_data['Race Position Category']

    # Initialize the Random Forest Classifier
    rf_classifier = RandomForestClassifier(
        n_estimators=200,  # Number of trees
        max_depth=15,  # Maximum depth of the tree
        min_samples_split=5,  # Minimum samples required to split a node
        min_samples_leaf=2,  # Minimum samples required at a leaf node
        random_state=42  # Seed for reproducibility
    )

    # Train the classifier
    rf_classifier.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf_classifier.predict(X_test)

    # Evaluate the model
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Add predictions to the test dataset
    test_data['Predicted Race Position Category'] = y_pred

    # Save predictions to a CSV file
    test_data.to_csv('ML_Outputs/classifier_predictions.csv', index=False)
    print("Predictions saved to 'ML_Outputs/classifier_predictions.csv'.")


if __name__ == "__main__":
    main()
