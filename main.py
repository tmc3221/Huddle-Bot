# main.py

import data_loader
import feature_engineering
import model
import evaluate_model
import recommendations
import pandas as pd

def main(zip_path):
    # Load data
    print("Loading data...")
    combined_data = data_loader.load_csv_from_file(zip_path)

    # Perform feature engineering
    print("Performing feature engineering...")
    engineered_data = feature_engineering.feature_engineering(combined_data)

    # Train model
    print("Training the model...")
    trained_model, X_test, y_test = model.train_model(engineered_data)

    # Make predictions
    print("Making predictions...")
    predictions = model.make_predictions(trained_model, X_test)

    # Evaluate the model
    print("Evaluating the model...")
    mse = evaluate_model.evaluate_model(y_test, predictions)
    print(f"Mean Squared Error: {mse:.2f}")

    # Generate recommendations based on predictions
    print("Generating recommendations...")

    # Get player names from X_test
    player_names = X_test['Player']  # Ensure 'Player' is available in X_test

    # Map player names to predictions
    prediction_results = {name: pred for name, pred in zip(player_names, predictions)}

    # Print recommendations sorted by predicted fantasy points in descending order
    print("Recommendations:")
    sorted_recs = sorted(prediction_results.items(), key=lambda item: item[1], reverse=True)
    for i, (player, points) in enumerate(sorted_recs, 1):
        print(f"{i}: {player} with {points:.2f} predicted Fantasy Points")

if __name__ == "__main__":
    zip_path = 'test_player_stats.csv'  # Specify the path to your test CSV file
    main(zip_path)
