import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Fantasy Point Values
PASSING_YARDS = 0.04
RUSHING_YARDS = 0.1
RECEIVING_YARDS = 0.1
RECEPTIONS = 1
RUSHING_TD = 6
PASSING_TD = 4
RECEIVING_TD = 6
FUMBLE = -2
INTERCEPTION = - 2

def prepare_data(player_stats, defense_stats, position, points):
   relevant_data = {}
   #relevant_data['nextGameFantasyPoints'] = None
   # Set defensive stats based on the player's position
   if position == "QB":
        # Consider all defensive stats for QBs
        relevant_data['defense'] = defense_stats
        relevant_data['player'] = {
            'FantasyPointsAverage': player_stats.get('FantasyPointsAverage'),
            'Completions': player_stats.get('Completions'),
            'Attempts': player_stats.get('Attempts'),
            'Yards': player_stats.get('Yards'),
            'Average': player_stats.get('Average'),
            'Touchdowns': player_stats.get('Touchdowns'),
            'Interceptions': player_stats.get('Interceptions'),
            'Sacks': player_stats.get('Sacks'),
            'Sack Yards': player_stats.get('Sack Yards'),
            'Rating': player_stats.get('Rating'),
            'Rushing Attempts': player_stats.get('Rushing Attempts'),
            'Rushing Yards': player_stats.get('Rushing Yards'),
            'Rushing Average': player_stats.get('Rushing Average'),
            'Rushing Touchdowns': player_stats.get('Rushing Touchdowns'),
            'Fumbles': player_stats.get('Fumbles'),
            'Fumbles Lost': player_stats.get('Fumbles Lost'),
        }
        relevant_data['fantasyPointAverage'] = points

   elif position in ["RB", "FB"]:
        # RB and FB should consider rushing, receiving, fumble, and scoring stats
        relevant_data['defense'] = {
            'rushing_stats': defense_stats.get('rushing'),
            'receiving_stats': defense_stats.get('receiving'),
            'fumble_stats': defense_stats.get('fumbles'),
            'scoring_stats': defense_stats.get('scoring')
        }
        relevant_data['player'] = {
            'FantasyPointsAverage': player_stats.get('FantasyPointsAverage'),
            'Rushing Attempts': player_stats.get('Rushing Attempts'),
            'Rushing Yards': player_stats.get('Rushing Yards'),
            'Rushing Average': player_stats.get('Rushing Average'),
            'Longest Run': player_stats.get('Longest Run'),
            'Rushing Touchdowns': player_stats.get('Rushing Touchdowns'),
            'Receptions': player_stats.get('Receptions'),
            'Receiving Yards': player_stats.get('Receiving Yards'),
            'Receiving Average': player_stats.get('Receiving Average'),
            'Longest Reception': player_stats.get('Longest Reception'),
            'Receiving Touchdowns': player_stats.get('Receiving Touchdowns'),
            'Fumbles': player_stats.get('Fumbles'),
            'Fumbles Lost': player_stats.get('Fumbles Lost'),
        }

   elif position in ["WR", "TE"]:
        # WR and TE should consider rushing, receiving, fumble, and scoring stats
        relevant_data['defense'] = {
            'rushing_stats': defense_stats.get('rushing'),
            'receiving_stats': defense_stats.get('receiving'),
            'fumble_stats': defense_stats.get('fumble'),
            'scoring_stats': defense_stats.get('scoring')
        }
        relevant_data['player'] = {
            'FantasyPointsAverage': player_stats.get('FantasyPointsAverage'),
            'Receptions': player_stats.get('Receptions'),
            'Receiving Yards': player_stats.get('Receiving Yards'),
            'Receiving Average': player_stats.get('Receiving Average'),
            'Longest Reception': player_stats.get('Longest Reception'),
            'Receiving Touchdowns': player_stats.get('Receiving Touchdowns'),
            'Rushing Attempts': player_stats.get('Rushing Attempts'),
            'Rushing Yards': player_stats.get('Rushing Yards'),
            'Rushing Average': player_stats.get('Rushing Average'),
            'Longest Run': player_stats.get('Longest Run'),
            'Rushing Touchdowns': player_stats.get('Rushing Touchdowns'),
            'Fumbles': player_stats.get('Fumbles'),
            'Fumbles Lost': player_stats.get('Fumbles Lost'),
        }

   return relevant_data



def scrape_defensive_data(opponent, defensive_data):
    # Define URLs for the defensive stats
    urls = {
        'passing': 'https://www.nfl.com/stats/team-stats/defense/passing/2024/reg/all',
        'rushing': 'https://www.nfl.com/stats/team-stats/defense/rushing/2024/reg/all',
        'receiving': 'https://www.nfl.com/stats/team-stats/defense/receiving/2024/reg/all',
        'scoring': 'https://www.nfl.com/stats/team-stats/defense/scoring/2024/reg/all',
        'fumbles': 'https://www.nfl.com/stats/team-stats/defense/fumbles/2024/reg/all',
        'interceptions': 'https://www.nfl.com/stats/team-stats/defense/interceptions/2024/reg/all'
    }

    # Create a dictionary to store the opponent's stats
    opponent_stats = {'Team': opponent}

    for stat_type, url in urls.items():
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Could not fetch {stat_type} data. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing the stats
        table = soup.find('table', {'class': 'd3-o-table'})
        if not table:
            raise ValueError(f"No statistics found for {stat_type}. Check if the URL is correct.")

        rows = table.find_all('tr')[1:]  # Skip header row

        for row in rows:
            cols = row.find_all('td')
            # print("Type: " + stat_type)
            # print(f"Number of columns in row: {len(cols)}")
            if len(cols) == 0:
                continue
            
            team_name = cols[0].text.strip()
            
            normalized_team_name = team_name.lower().split(" ")[0]
            normalized_opponent = opponent.lower() + "\n"

            #print(normalized_opponent == normalized_team_name)
            
            # Check if the team name matches the opponent
            if normalized_team_name == normalized_opponent:
                # Extract the required statistics based on their position
                stats = {}
                
                if stat_type == 'passing':
                    stats.update({
                        'Att': cols[1].text.strip(),
                        'Cmp': cols[2].text.strip(),
                        'Cmp %': cols[3].text.strip(),
                        'Yds/Att': cols[4].text.strip(),
                        'Yds': cols[5].text.strip(),
                        'TD': cols[6].text.strip(),
                        'INT': cols[7].text.strip(),
                        'Rate': cols[8].text.strip(),
                        '1st': cols[9].text.strip(),
                        '1st%': cols[10].text.strip(),
                        '20+': cols[11].text.strip(),
                        '40+': cols[12].text.strip(),
                        'Lng': cols[13].text.strip(),
                        'Sck': cols[14].text.strip(),
                    })
                elif stat_type == 'rushing':
                    stats.update({
                        'Att': cols[1].text.strip(),
                        'Rush Yds': cols[2].text.strip(),
                        'YPC': cols[3].text.strip(),
                        'TD': cols[4].text.strip(),
                        '20+': cols[5].text.strip(),
                        '40+': cols[6].text.strip(),
                        'Lng': cols[7].text.strip(),
                        'Rush 1st': cols[8].text.strip(),
                        'Rush 1st%': cols[9].text.strip(),
                        'Rush FUM': cols[10].text.strip(),
                    })
                elif stat_type == 'receiving':
                    stats.update({
                        'Rec': cols[1].text.strip(),
                        'Yds': cols[2].text.strip(),
                        'Yds/Rec': cols[3].text.strip(),
                        'TD': cols[4].text.strip(),
                        '20+': cols[5].text.strip(),
                        '40+': cols[6].text.strip(),
                        'Lng': cols[7].text.strip(),
                        'Rec 1st': cols[8].text.strip(),
                        'Rec 1st%': cols[9].text.strip(),
                        'Rec FUM': cols[10].text.strip(),
                        'PDef': cols[11].text.strip(),
                    })
                elif stat_type == 'scoring':
                    stats.update({
                        'FR TD': cols[1].text.strip(),
                        'SFTY': cols[2].text.strip(),
                        'INT TD': cols[3].text.strip(),
                    })
                elif stat_type == 'fumbles':
                    stats.update({
                        'FF': cols[1].text.strip(),
                        'FR': cols[2].text.strip(),
                        'FR TD': cols[3].text.strip(),
                        'Rec FUM': cols[4].text.strip(),
                        'Rush FUM': cols[5].text.strip(),
                    })
                elif stat_type == 'interceptions':
                    stats.update({
                        'INT': cols[1].text.strip(),
                        'INT TD': cols[2].text.strip(),
                        'INT Yds': cols[3].text.strip(),
                        'Lng': cols[4].text.strip(),
                    })

                #defensive_data[stat_type] = pd.DataFrame([stats])  # Create a DataFrame with one row
                opponent_df = pd.DataFrame([stats])
                defensive_data = pd.concat([defensive_data, opponent_df], ignore_index=True)
                break  # Exit loop after finding the opponent
    return defensive_data

def find_opponent(team_schedule, recent):
    # Get most recent week from schedule
    if not team_schedule:
        raise ValueError("The team schedule is empty or not available.")
    
    opponent = team_schedule[int(recent)]

    return opponent, int(recent)

def scrape_nfl_player_data(player_name):
    # Format the player name to create the URL
    formatted_name = player_name.lower().replace(' ', '-')
    url = f"https://www.nfl.com/players/{formatted_name}/stats/"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Could not fetch data for {player_name}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the team name section
    team_section = soup.find('a', {'class': 'nfl-o-cta--link'})  # Adjust class based on actual HTML structure
    if not team_section:
        raise ValueError(f"Could not find team information for {player_name}.")
    
    team_name = team_section.text.strip()
    #print(f"Team: {team_name}")
    with open('data/teams.json', 'r') as file:
        nfl_schedule = json.load(file)

    # Find the team's schedule
    team_schedule = nfl_schedule.get(team_name)
    if team_schedule is None:
        raise ValueError(f"No schedule found for team: {team_name}")
    
    # Find the table containing recent games stats
    stats_table = soup.find('table', {'class': 'd3-o-table'})
    
    if not stats_table:
        raise ValueError(f"No statistics found for {player_name}. Check if the player exists.")

    rows = stats_table.find_all('tr')
    recent_games_data = []

    position_element = soup.find('span', class_='nfl-c-player-header__position')
    player_position = position_element.text.strip() if position_element else "Position not found"

    for row in rows[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        # Extracting the required statistics based on their position
         # QB Stats
        if player_position == "QB":
            game_data = {
                'Week': cols[0].text.strip(),
                'Opponent': cols[1].text.strip(),
                'Result': cols[2].text.strip(),
                'Completions': cols[3].text.strip(),
                'Attempts': cols[4].text.strip(),
                'Yards': cols[5].text.strip(),
                'Average': cols[6].text.strip(),
                'Touchdowns': cols[7].text.strip(),
                'Interceptions': cols[8].text.strip(),
                'Sacks': cols[9].text.strip(),
                'Sack Yards': cols[10].text.strip(),
                'Rating': cols[11].text.strip(),
                'Rushing Attempts': cols[12].text.strip(),
                'Rushing Yards': cols[13].text.strip(),
                'Rushing Average': cols[14].text.strip(),
                'Rushing Touchdowns': cols[15].text.strip(),
                'Fumbles': cols[16].text.strip(),
                'Fumbles Lost': cols[17].text.strip(),
            }
        # RB/FB Stats
        elif player_position in ["RB", "FB"]:
            game_data = {
                'Week': cols[0].text.strip(),
                'Opponent': cols[1].text.strip(),
                'Result': cols[2].text.strip(),
                'Rushing Attempts': cols[3].text.strip(),
                'Rushing Yards': cols[4].text.strip(),
                'Rushing Average': cols[5].text.strip(),
                'Longest Run': cols[6].text.strip(),
                'Rushing Touchdowns': cols[7].text.strip(),
                'Receptions': cols[8].text.strip(),
                'Receiving Yards': cols[9].text.strip(),
                'Receiving Average': cols[10].text.strip(),
                'Longest Reception': cols[11].text.strip(),
                'Receiving Touchdowns': cols[12].text.strip(),
                'Fumbles': cols[13].text.strip(),
                'Fumbles Lost': cols[14].text.strip(),
            }
        # TE/WR Stats
        elif player_position in ["TE", "WR"]:
            game_data = {
                'Week': cols[0].text.strip(),
                'Opponent': cols[1].text.strip(),
                'Result': cols[2].text.strip(),
                'Receptions': cols[3].text.strip(),
                'Receiving Yards': cols[4].text.strip(),
                'Receiving Average': cols[5].text.strip(),
                'Longest Reception': cols[6].text.strip(),
                'Receiving Touchdowns': cols[7].text.strip(),
                'Rushing Attempts': cols[8].text.strip(),
                'Rushing Yards': cols[9].text.strip(),
                'Rushing Average': cols[10].text.strip(),
                'Longest Run': cols[11].text.strip(),
                'Rushing Touchdowns': cols[12].text.strip(),
                'Fumbles': cols[13].text.strip(),
                'Fumbles Lost': cols[14].text.strip(),
            }
        # Invalid position
        else:
            raise ValueError(f"{player_name} plays an invalid position ({player_position}). Cannot scrape data.")
        recent = cols[0].text.strip()
        recent_games_data.append(game_data)
        #print(pd.DataFrame(recent_games_data))

    return pd.DataFrame(recent_games_data), team_name, team_schedule, recent, player_position

def calculate_fantasy_average_output(position, player_data, weekNum):
    yard_pts = 0
    passing_td = 0
    ints = 0
    rushing = 0
    rushing_td = 0
    fumbles = 0
    receiving_yard = 0
    receiving_tds = 0
    reception = 0

    # Fill na
    player_data = player_data.fillna(0)
    player_data = player_data.replace('', 0).infer_objects(copy=False)
    
    # Find position
    if position == "QB":
        for i in range(weekNum):
            yard_pts += int(player_data['Yards'].get(i)) * PASSING_YARDS
            #print(yard_pts)
            passing_td += int(player_data['Touchdowns'].get(i)) * PASSING_TD
            #print(passing_td)
            ints += int(player_data['Interceptions'].get(i)) * INTERCEPTION
            #print(ints)
            rushing += int(player_data['Rushing Yards'].get(i)) * RUSHING_YARDS
            #print(rushing)
            rushing_td += int(player_data['Rushing Touchdowns'].get(i)) * RUSHING_TD
            #print(rushing_td)
            fumbles += int(player_data['Fumbles Lost'].get(i)) * FUMBLE
            #print(fumbles)
        
        return (yard_pts + passing_td + ints + rushing + rushing_td
        + fumbles) / weekNum
        #player_data['FantasyPointsAverage'] = average_pts
    elif position in ["RB", "FB"]:
        rushing = player_data.get('Rushing Yards') * RUSHING_YARDS
        rushing_td = player_data.get('Rushing Touchdowns') * RUSHING_TD
        fumbles = player_data.get('Fumbles Lost') * FUMBLE
        reception = player_data.get('Receptions') * RECEPTIONS
        receiving_yard = player_data.get('Receiving Yards') * RECEIVING_YARDS
        receiving_tds = player_data.get('Receiving Touchdowns') * RECEIVING_TD

        average_pts = (reception + receiving_yard + receiving_tds + rushing + rushing_td
        + fumbles) / weekNum
        player_data['FantasyPointsAverage'] = average_pts
    elif position in ["WR", "TE"]:
        rushing = player_data.get('Rushing Yards') * RUSHING_YARDS
        rushing_td = player_data.get('Rushing Touchdowns') * RUSHING_TD
        fumbles = player_data.get('Fumbles Lost') * FUMBLE
        reception = player_data.get('Receptions') * RECEPTIONS
        receiving_yard = player_data.get('Receiving Yards') * RECEIVING_YARDS
        receiving_tds = player_data.get('Receiving Touchdowns') * RECEIVING_TD

        average_pts = (reception + receiving_yard + receiving_tds + rushing + rushing_td
        + fumbles) / weekNum
        player_data['FantasyPointsAverage'] = average_pts


def collect(player_name):

    # Read the schedule from the JSON file
    with open('data/teams.json', 'r') as file:
        nfl_schedule = json.load(file)

    try:
        player_data, team_name, team_schedule, recent, position = scrape_nfl_player_data(player_name)
        pd.set_option('display.max_rows', None)  # Display all rows
        pd.set_option('display.max_columns', None)  # Display all columns
        #print(player_data)
        #print(player_data)
        opponent, weekNum = find_opponent(team_schedule, recent)
        points = calculate_fantasy_average_output(position, player_data, weekNum)
        # Find the opponent
        #print(opponent)

        defensive_data = pd.DataFrame()

        for i in range(weekNum):
            defensive_data = scrape_defensive_data(find_opponent(team_schedule, i)[0], defensive_data)

        upcoming_defensive_data = pd.DataFrame()
        upcoming_defensive_data = scrape_defensive_data(opponent, upcoming_defensive_data)

        upcoming_defensive_data = upcoming_defensive_data.fillna(0)
        upcoming_defensive_data = upcoming_defensive_data.replace('', 0).infer_objects(copy=False)
        defensive_data = defensive_data.fillna(0)
        defensive_data = defensive_data.replace('', 0).infer_objects(copy=False)
        
        
        '''print("Defensive Passing Data:")
        print(defensive_data['passing'])
        print("\nDefensive Rushing Data:")
        print(defensive_data['rushing'])
        print("\nDefensive Receiving Data:")
        print(defensive_data['receiving'])
        print("\nDefensive Scoring Data:")
        print(defensive_data['scoring'])
        print("\nDefensive Fumbles Data:")
        print(defensive_data['fumbles'])
        print("\nDefensive Interceptions Data:")
        print(defensive_data['interceptions'])'''

        defensive_data['passing'].to_csv('project-docs/defensive_passing_data.csv', index=False)
        defensive_data['rushing'].to_csv('project-docs/defensive_rushing_data.csv', index=False)
        defensive_data['receiving'].to_csv('project-docs/defensive_receiving_data.csv', index=False)
        defensive_data['scoring'].to_csv('project-docs/defensive_scoring_data.csv', index=False)
        defensive_data['fumbles'].to_csv('project-docs/defensive_fumbles_data.csv', index=False)
        defensive_data['interceptions'].to_csv('project-docs/defensive_interceptions_data.csv', index=False)

        # Clean/Prepare the data
        return prepare_data(player_data, defensive_data, position, points)
    
    except Exception as e:
        print(e)