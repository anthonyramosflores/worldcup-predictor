import pandas as pd

pd.set_option('display.max_columns', None)

df = pd.read_csv('results.csv')
# print(df.head())

df['date'] = pd.to_datetime(df['date'])
df[df['date'] < '2022-01-01'].head()

def get_result(row):
    if row['home_score'] > row['away_score']:
        return 'home_win'
    elif row['away_score'] > row['home_score']:
        return 'away_win'
    else:
        return 'draw'
    
def get_team_result(row, team):
    if row['home_team'] == team:
        if row['result'] == 'home_win':
            return 'win'
        elif row['result'] == 'away_win':
            return 'loss'
        else:
            return 'draw'
    elif row['away_team'] == team:
        if row['result'] == 'away_win':
            return 'win'
        elif row['result'] == 'home_win':
            return 'loss'
        else:
            return 'draw'
    else:
        return None
    
def get_win_percentage(team, date, df, n = 10):
    team_matches = df[
        ((df['home_team'] == team) | (df['away_team'] == team)) &
        (df['date'] < date)
    ].tail(n)

    if len(team_matches) == 0:
        return 0.5
    
    results = team_matches.apply(lambda row: get_team_result(row, team), axis=1)
    wins = (results == 'win').sum()
    return wins / len(team_matches)
    
df['result'] = df.apply(get_result, axis=1)
# print(df[['home_team', 'away_team', 'home_score', 'away_score', 'result']].head())
print(get_win_percentage('San Marino', '2022-01-01', df))