import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nfl_player_data(player_name):
    # Format the player name to create the URL-friendly version
    formatted_name = player_name.lower().replace(' ', '-')
    url = f"https://www.nfl.com/players/{formatted_name}/stats/"

    # Fetch the player page
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Could not fetch data for {player_name}. Status code: {response.status_code}")

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the statistics table
    stats_table = soup.find('table', {'class': 'd3-o-table'})

    if not stats_table:
        raise ValueError(f"No statistics found for {player_name}. Check if the player exists.")

    rows = stats_table.find_all('tr')

    player_data_list = []
    for row in rows:
        # Extract relevant statistics; update according to the actual HTML structure
        cols = row.find_all('td')
        if len(cols) == 0:
            continue  # Skip empty rows

        season = cols[0].text.strip()  # Assuming season is in the first column
        games_played = cols[1].text.strip()  # Example: games played in the second column
        passing_yards = cols[2].text.strip()  # Example: passing yards in the third column
        touchdowns = cols[3].text.strip()  # Example: touchdowns in the fourth column
        
        # Add more statistics as needed
        player_data = {
            'Player': player_name,
            'Season': season,
            'GamesPlayed': games_played,
            'PassingYards': passing_yards,
            'Touchdowns': touchdowns,
            # Add all other statistics...
        }

        player_data_list.append(player_data)

    return pd.DataFrame(player_data_list)

def main():
    player_name = input("Enter the NFL player's name for prediction: ")
    try:
        player_data = scrape_nfl_player_data(player_name)
        print(player_data)
        # Assuming you have a function to prepare the data for the model
        # prepared_data = prepare_data(player_data)
        
        # Example prediction
        # prediction = make_predictions(trained_model, prepared_data)
        
        # Print the prediction
        # print(f"Predicted Fantasy Points for {player_name}: {prediction}")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
