# feature_engineering.py
# Creates additional features needed for the model

# feature_engineering.py

def feature_engineering(df):
    # Calculate rolling averages for Fantasy Points
    df['3WkAvgFantasyPoints'] = df['FantasyPoints'].rolling(window=3, min_periods=1).mean()
    df['5WkAvgFantasyPoints'] = df['FantasyPoints'].rolling(window=5, min_periods=1).mean()

    # Example of other simple features you can add
    df['FantasyPointsPerGame'] = df['FantasyPoints'] / df['GamesPlayed']
    df['IsHomeGame'] = df['Location'].apply(lambda x: 1 if x == 'Home' else 0)

    # Handle missing values for new features
    df.fillna(0, inplace=True)
    
    return df

