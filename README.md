# World Cup Match Predictor

A machine learning app that predicts the outcome of international soccer matches using 150 years of historical data.

## What It Does
Select any two international teams and get a predicted match outcome — home win, away win, or draw — powered by a model trained on 49,000 matches dating back to 1872.

## Tech Stack
- Python
- pandas
- scikit-learn
- Streamlit
- pickle

## How It Works
Historical match data from Kaggle was used to engineer 5 features per team: win percentage, average goals scored, average goals conceded, competitive match flag, and home/away venue. Two models were trained and compared — Logistic Regression (60% accuracy) and Random Forest (55%). Logistic Regression was selected as the final model.

## How To Run
1. Clone the repo
2. Install dependencies: `pip3 install pandas scikit-learn streamlit`
3. Run: `python3 -m streamlit run app.py`

## Data Source
Kaggle — International football results from 1872 to 2025