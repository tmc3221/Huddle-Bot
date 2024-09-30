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
    combined_data = data_loader.load_csvs_from_zip(zip_path)

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

    # Generate recommendations based on predictions
    print("Generating recommendations...")
    player_names = X_test['player_name']  # Assuming there's a 'player_name' column in X_test
    prediction_results = {name: pred for name, pred in zip(player_names, predictions)}
    recs = recommendations.generate_recommendations(prediction_results)

    # Print recommendations
    print("Recommendations:")
    for rec in recs:
        print(rec)

if __name__ == "__main__":
    zip_path = 'archive.zip'  # Specify the path to your zipped CSV files
    main(zip_path)
