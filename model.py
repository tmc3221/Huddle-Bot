from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd

def train_model(df):
    # Separate the target variable (FantasyPoints) and features (X)
    X = df.drop(columns=['FantasyPoints'])
    y = df['FantasyPoints']
    
    # List of categorical columns
    categorical_cols = ['Player', 'Team', 'Opponent', 'Location', 'InjuryStatus']
    
    # One-hot encode categorical features and apply imputation to numeric columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), X.select_dtypes(exclude=['object']).columns),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
    
    # Create a pipeline with preprocessing and the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the pipeline
    pipeline.fit(X_train, y_train)
    
    return pipeline, X_test, y_test

def make_predictions(model, new_data):
    # Use the trained model to make predictions on new data
    return model.predict(new_data)