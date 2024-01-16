import json


def display(new_data, new_query):
    final_array = [[]]
    for d in new_data['results']:
        for round in d['rounds']['raw']:
            json_data = json.loads(round)
            match = json_data['matches'][0]
            team1 = match['team1']
            team2 = match['team2']
            date = match['date']
            score = match['score']['ft']
            if team2 == new_query or team1 == new_query:
                final_array.append(f'On {date} the score between {team1} and {team2} was {score}')
    return final_array
