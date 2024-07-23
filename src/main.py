# Libraries
import streamlit as st
import asyncio

# Local Modules
from data import load_history, remove_old_games_from_history
from utils import filter_games
from api import get_live_games, get_team_history, get_standings
from views import display_team_history

history_data = load_history()
live_games = filter_games(get_live_games())
remove_old_games_from_history(history_data)


def get_team_position(standings, team_id):
    for league in standings:
        for standing in league.get('league', {}).get('standings', []):
            for team in standing:
                if team['team']['id'] == team_id:
                    return team['rank']
    return None


st.set_page_config(layout='wide')
st.sidebar.title("Jogos ao Vivo")

if live_games:
    selected_game = None
    for game in live_games:
        game_label = f"{game['teams']['home']['name']} x {game['teams']['away']['name']}"
        if st.sidebar.button(game_label):
            selected_game = game_label
    for game in live_games:
        if f"{game['teams']['home']['name']} x {game['teams']['away']['name']}" == selected_game:
            fixture = game['fixture']
            home_team = game['teams']['home']
            away_team = game['teams']['away']

            home_team_id = home_team['id']
            away_team_id = away_team['id']
            home_team_name = home_team['name']
            away_team_name = away_team['name']

            # Get standings
            league_id = game['league']['id']
            season = game['league']['season']
            standings = get_standings(league_id, season)

            # Get team positions
            home_team_position = get_team_position(standings, home_team_id)
            away_team_position = get_team_position(standings, away_team_id)

            status = game['fixture']['status']
            time_elapsed = status['elapsed']
            status_description = status['short']

            if status_description == 'HT':
                status_text = "INTERVALO"
            elif status_description == '2H':
                status_text = f"{time_elapsed} mins"
            else:
                status_text = status_description

            if home_team_position:
                st.title(f"{home_team_name} ({home_team_position}°) x {away_team_name} ({away_team_position}°) - {status_text}")
            else:
                st.title(f"{home_team_name} x {away_team_name} - {status_text}")

            goals = game['goals']
            home_score = goals['home']
            away_score = goals['away']
            st.header(f"{home_score} x {away_score}")

            home_team_history = get_team_history(home_team_name, home_team_id)
            away_team_history = get_team_history(away_team_name, away_team_id)

            # home_team_avg_goals = calculate_average_goals(home_team_history, home_team_name)
            # away_team_avg_goals = calculate_average_goals(away_team_history, away_team_name)
            # st.subheader(f"Soma Total das Médias: {round(home_team_avg_goals + away_team_avg_goals, 1)}")
            # st.write(f"Média de Gols {home_team_name}: {home_team_avg_goals}")
            # st.write(f"Média de Gols {away_team_name}: {away_team_avg_goals}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Histórico {home_team_name}:")
                asyncio.run(display_team_history(home_team_id, home_team_name))

            with col2:
                st.subheader(f"Histórico {away_team_name}:")
                asyncio.run(display_team_history(away_team_id, away_team_name))

else:
    st.sidebar.write("Nenhum jogo ao vivo no momento")