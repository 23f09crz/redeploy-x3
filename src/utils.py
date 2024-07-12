import streamlit as st


def calculate_average_goals(team_history, team_name, limit=10):
    try:
        valid_games = [game for game in team_history if
                       game['goals']['home'] is not None and game['goals']['away'] is not None]
        total_goals = sum(
            game['goals']['home'] if game['teams']['home']['name'] == team_name else game['goals']['away'] for game in
            valid_games[:limit])
        return total_goals / limit
    except Exception as e:
        st.error(f"Erro ao calcular média de gols: {e}")
        return "Não foi possível calcular a média"


def filter_games(games):
    filtered_games = []
    for game in games:
        status = game['fixture']['status']
        time_elapsed = status['elapsed']
        if status['short'] == "HT" or (status['short'] == '2H' and time_elapsed < 71):
            filtered_games.append(game)
    return filtered_games
