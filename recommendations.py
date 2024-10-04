# recommendations.py
# Generates recommendations for top fantasy scorers

def generate_recommendations(prediction_results):
    # Sort players by predicted FantasyPoints in descending order
    sorted_predictions = sorted(prediction_results.items(), key=lambda x: x[1], reverse=True)

    # Get top 5 predicted players
    top_scorers = sorted_predictions[:5]

    # Create recommendations list
    recommendations = [f"{player}: {score:.2f} predicted Fantasy Points" for player, score in top_scorers]

    return recommendations
