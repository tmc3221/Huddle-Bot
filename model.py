from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd

def train_model(df):
    if isinstance(df, dict):
        df = pd.DataFrame(df)

    # Shift fantasy points to create the target for "next game" points prediction
    df['nextGameFantasyPoints'] = df['fantasyPointAverage'].shift(-1)
    
    # Remove the last row because it has no target (the next game is not available)
    df = df.dropna(subset=['nextGameFantasyPoints'])
    
    # Separate the features (X) and the target (y)
    X = df.drop(columns=['fantasyPointAverage', 'nextGameFantasyPoints'])
    y = df['nextGameFantasyPoints']
    
    # Convert categorical columns to strings and handle missing values
    categorical_cols = ['defense', 'player']
    for col in categorical_cols:
        X[col] = X[col].astype(str)
        X[col].fillna("Unknown", inplace=True)

    # Create the preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), X.select_dtypes(exclude=['object']).columns),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )
    
    # Create the complete pipeline with preprocessing and model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the pipeline
    pipeline.fit(X_train, y_train)
    
    return pipeline, X_test, y_test


def make_predictions(model, player_data):
    if isinstance(player_data, dict):
        player_data = pd.DataFrame([player_data])  # Convert dict to DataFrame
    
    # Ensure player_data has the same structure as the model expects
    categorical_cols = ['defense', 'player']
    for col in categorical_cols:
        if col in player_data.columns:
            player_data[col] = player_data[col].astype(str)
        else:
            player_data[col] = "Unknown"  # If missing, fill with "Unknown"
    
    # Make predictions
    predicted_next_game_points = model.predict(player_data)
    return predicted_next_game_points

def prepare_cleaned_data(player_stats, defense_stats, position):
    # Prepare cleaned data to match model expectations
    relevant_data = {}
    if position == "QB":
        relevant_data.update(defense_stats)  # Assuming defense_stats are already cleaned
        relevant_data.update(player_stats)  # Assuming player_stats are already cleaned
    elif position in ["RB", "FB", "WR", "TE"]:
        relevant_data.update(defense_stats)  # Similar for RB, FB, WR, TE
        relevant_data.update(player_stats)

    return pd.DataFrame([relevant_data])  # Convert to DataFrame for model input