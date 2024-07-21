import json
import os
import time
def load_history():
    history_path = 'historico.json'
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            os.remove(history_path)  # Delete the corrupt file
            return {}  # Return an empty dictionary if the file is corrupt
    return {}

def save_history(data):
    with open('historico.json', 'w') as file:
        json.dump(data, file, indent=4)

def remove_old_games_from_history(data):
    for team_id in list(data.keys()):
        data[team_id]['response'] = [game for game in data[team_id]['response'] if game['fixture']['status']['elapsed'] is None or game['fixture']['status']['elapsed'] > 70]
    save_history(data)

def load_fixture_statistics():
    stats_path = 'fixture_statistics.json'
    if os.path.exists(stats_path):
        try:
            with open(stats_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            os.remove(stats_path)  # Delete the corrupt file
            return {}  # Return an empty dictionary if the file is corrupt
    return {}

def save_fixture_statistics(data):
    with open('fixture_statistics.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_standings():
    standings_path = 'standings.json'
    if os.path.exists(standings_path):
        try:
            with open(standings_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}  # Return an empty dictionary if the file is corrupt
    return {}

def save_standings(data):
    with open('standings.json', 'w') as file:
        json.dump(data, file, indent=4)
def remove_old_fixture_statistics(data):
    # You might want to define what constitutes an "old" fixture
    # For example, removing fixtures older than a week
    current_time = int(time.time())
    one_week = 7 * 24 * 60 * 60  # 7 days in seconds

    for fixture_id in list(data.keys()):
        fixture_time = data[fixture_id][0]['fixture']['timestamp']
        if current_time - fixture_time > one_week:
            del data[fixture_id]

    save_fixture_statistics(data)



