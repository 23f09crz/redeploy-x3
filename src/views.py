import streamlit as st
from datetime import datetime

from api import get_team_history, get_fixture_statistics

corner_kick_img = "img/escanteio.png"


async def display_team_history(team_id, team_name, limit=10):
    team_history = get_team_history(team_name, team_id)
    valid_games = [game for game in team_history if
                   game['goals']['home'] is not None and game['goals']['away'] is not None]
    st.write(f"Últimos {limit} jogos de {team_name}:")

    fixture_ids = [game['fixture']['id'] for game in valid_games[1:limit + 1]]
    statistics = await get_fixture_statistics(fixture_ids)

    for game in valid_games[1:limit + 1]:
        fixture = game['fixture']
        date = datetime.strptime(fixture['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m')
        home_team = game['teams']['home']['name']
        away_team = game['teams']['away']['name']
        home_score = game['goals']['home']
        away_score = game['goals']['away']

        try:
            if home_team == team_name:
                color = 'green' if home_score > 0 else 'red'
                corner_kicks_home = next(
                    (s['value'] for s in statistics[fixture['id']][0]['statistics'] if s['type'] == "Corner Kicks"), 0)
                corner_kicks_away = next(
                    (s['value'] for s in statistics[fixture['id']][1]['statistics'] if s['type'] == "Corner Kicks"), 0)
                st.markdown(
                    f"{date}: {corner_kicks_home} <img src='{corner_kick_img}' width='15' height='15' /> <span style='color:{color}'><b>{home_team} {home_score}</b></span> x {away_score} {away_team} <img src='{corner_kick_img}' width='15' height='15' /> {corner_kicks_away}",
                    unsafe_allow_html=True)
            else:
                color = 'green' if away_score > 0 else 'red'
                corner_kicks_home = next(
                    (s['value'] for s in statistics[fixture['id']][0]['statistics'] if s['type'] == "Corner Kicks"), 0)
                corner_kicks_away = next(
                    (s['value'] for s in statistics[fixture['id']][1]['statistics'] if s['type'] == "Corner Kicks"), 0)
                st.markdown(
                    f"{date}: {corner_kicks_home} <img src='{corner_kick_img}' width='15' height='15' /> {home_team} {home_score} x <span style='color:{color}'><b>{away_team} {away_score}</b></span> <img src='{corner_kick_img}' width='15' height='15' /> {corner_kicks_away}",
                    unsafe_allow_html=True
                )
        except (IndexError, KeyError):
            if home_team == team_name:
                color = 'green' if home_score > 0 else 'red'
                st.markdown(
                    f"{date}: <span style='color:{color}'><b>{home_team} {home_score}</b></span> - {away_score} {away_team}",
                    unsafe_allow_html=True)
            else:
                color = 'green' if away_score > 0 else 'red'
                st.markdown(
                    f"{date}: {home_team} {home_score} - <span style='color:{color}'><b>{away_score} {away_team}</b></span>",
                    unsafe_allow_html=True)