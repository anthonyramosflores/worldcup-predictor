from model import get_win_percentage, get_avg_goals_scored, get_avg_goals_conceded
from model import get_win_percentage, get_avg_goals_scored, get_avg_goals_conceded, get_result
import pandas as pd
import pickle
import streamlit as st

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("World CUp Match Predictor")

results = pd.read_csv('results.csv')
results['date'] = pd.to_datetime(results['date'])
results['result'] = results.apply(get_result, axis=1)
teams = sorted(results['home_team'].unique())

home_team = st.selectbox("Select Home Team", teams)
away_team = st.selectbox("Select Away Team", teams)

if st.button("Predict"):
    date = pd.Timestamp.today()

    features = {
        'home_win_pct': get_win_percentage(home_team, date, results),
        'away_win_pct': get_win_percentage(away_team, date, results),
        'home_goals_scored': get_avg_goals_scored(home_team, date, results),
        'away_goals_scored': get_avg_goals_scored(away_team, date, results),
        'home_goals_conceded': get_avg_goals_conceded(home_team, date, results),
        'away_goals_conceded': get_avg_goals_conceded(away_team, date, results),
        'is_competitive': 1,
        'is_home': 1
    }

    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]

    labels = {0: f"{home_team} wins", 1: "Draw", 2: f"{away_team} wins"}
    st.success(f"Prediction: {labels[prediction]}")

