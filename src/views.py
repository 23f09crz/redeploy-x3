import streamlit as st
from datetime import datetime

from api import get_team_history

def get_result_emoji(team, home_score, away_score):
    if home_score > away_score:
        return "✅" if team == "home" else "❌"
    elif home_score < away_score:
        return "❌" if team == "home" else "✅"
    else:
        return "⏸"

async def display_team_history(team_id, team_name, limit=10):
    team_history = get_team_history(team_name, team_id)
    valid_games = [game for game in team_history if
                   game['goals']['home'] is not None and game['goals']['away'] is not None]
    st.write(f"Últimos {limit} jogos de {team_name}:")

    fixture_ids = [game['fixture']['id'] for game in valid_games[1:limit + 1]]

    for game in valid_games[1:limit + 1]:
        fixture = game['fixture']
        date = datetime.strptime(fixture['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m')
        home_team = game['teams']['home']['name']
        away_team = game['teams']['away']['name']
        home_score = game['goals']['home']
        away_score = game['goals']['away']

        if home_team == team_name:
            color = 'green' if home_score > 0 else 'red'
            result_emoji = get_result_emoji("home", home_score, away_score)
            st.markdown(
                f"{date}: {result_emoji} <span style='color:{color}'><b>{home_team} {home_score}</b></span> x {away_score} {away_team}",
                unsafe_allow_html=True)
        else:
            color = 'green' if away_score > 0 else 'red'
            result_emoji = get_result_emoji("away", home_score, away_score)
            st.markdown(
                f"{date}: {result_emoji} {home_team} {home_score} x <span style='color:{color}'><b>{away_team} {away_score}</b></span>",
                unsafe_allow_html=True
            )