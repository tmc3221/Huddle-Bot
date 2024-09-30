# Creates additional features needed for the model
def feature_engineering(df):
    # Rolling averages for Fantasy Points
    df['3WkAvgFantasyPoints'] = df['FantasyPoints'].rolling(window=3).mean()
    df['5WkAvgFantasyPoints'] = df['FantasyPoints'].rolling(window=5).mean()
    
    # Adding Injury Status
    df['InjuryStatus'] = df['Player'].map(injury_data)  # Assuming injury_data is a dictionary {player_name: injury_status}
    df['InjuryStatus'].fillna('Healthy', inplace=True)  # Fill missing values with 'Healthy'

    # Adding Defensive Ratings from the weekly team data
    df['DefensiveRating'] = df['Opponent'].map(defensive_ratings)
    df['DefensiveRating'].fillna(df['DefensiveRating'].mean(), inplace=True)  # Fill missing values with the average rating

    # Adding features from weekly player data
    for col in ['pass_attempts', 'complete_pass', 'incomplete_pass', 'passing_yards', 'pass_td', 'interception']:
        df[col + '_recent'] = df['Player'].map(weekly_player_data.set_index('player_name')[col])  # Get recent performance metrics

    # Additional features based on weekly team data
    for col in ['total_snaps', 'yards_gained', 'touchdown', 'total_points']:
        df[col + '_team'] = df['Opponent'].map(weekly_team_data.set_index('team')[col])  # Get opponent's recent performance

    # Example of additional features
    df['FantasyPointsPerGame'] = df['FantasyPoints'] / df['GamesPlayed']
    df['IsHomeGame'] = df['Location'].apply(lambda x: 1 if x == 'Home' else 0)  # Binary feature for home games

    # Adding injury counts and historical performance
    df['CareerInjuries'] = df['Player'].map(injury_data.get('career_injuries', {})) 
    df['VacatedTargets'] = df['Player'].map(injury_data.get('vacated_targets', {}))  # Vacated targets

    return df