# main.py

import data_loader
import model
import evaluate_model
import recommendations
import pandas as pd
import collect

def main():
    player_name = input("Enter the NFL player's name for prediction: ")

    # Step 1: Collect and clean data (Filter out unrelevant data)
    cleaned_data = collect.collect(player_name)

    # Step 2: Load the model
    loaded_model, X_test, y_test = model.train_model(cleaned_data)

    # Step 3: Make prediction
    predictions = model.make_predictions(loaded_model, cleaned_data)

    print(predictions)

    # Step



if __name__ == "__main__":
    main()
