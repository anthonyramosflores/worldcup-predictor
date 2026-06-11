import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# allows us to see all columns in the dataframe when printing
pd.set_option('display.max_columns', None)

# read in the data
df = pd.read_csv('results.csv')

# code commented out for now
# print(df.head())

# parsing dates and filtering for matches before 2022-01-01 to focus on historical data
df['date'] = pd.to_datetime(df['date'])
df[df['date'] < '2022-01-01'].head()

# get_result determines the outcome of a match based on the home and away scores
def get_result(row):
    if row['home_score'] > row['away_score']:
        return 'home_win'
    elif row['away_score'] > row['home_score']:
        return 'away_win'
    else:
        return 'draw'
    
# get_team_result determines the result of a match for a specific team (win, loss, draw)
# based on the overall match result
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
    
# get_win_percentage calculates the win percentage for a given team up to a certain date
# based on the last n matches
def get_win_percentage(team, date, data, n = 10):
    team_matches = data[
        ((data['home_team'] == team) | (data['away_team'] == team)) &
        (data['date'] < date)
    ].tail(n)

    if len(team_matches) == 0:
        return 0.5
    
    results = team_matches.apply(lambda row: get_team_result(row, team), axis=1)
    wins = (results == 'win').sum()
    return wins / len(team_matches)

# get_avg_goals_scored calculates the average goals scored by a team in their last n matches before a given date
def get_avg_goals_scored(team, date, df, n = 10):
    team_matches = df[
        ((df['home_team'] == team) | (df['away_team'] == team)) &
        (df['date'] < date)
    ].tail(n)

    if len(team_matches) == 0:
        return 0

    # for each row, get the goals score by the team

    results = team_matches.apply(lambda row: row['home_score'] if row['home_team'] == team else row['away_score'], axis=1)
    return results.mean() 

# get average goals conceded 
def get_avg_goals_conceded(team, date, df, n = 10):
    team_matches = df[
        ((df['home_team'] == team) | (df['away_team'] == team)) & 
        (df['date'] < date)
    ].tail(n)

    if len(team_matches) == 0:
        return 0;

    results = team_matches.apply(lambda row: row['away_score'] if row['home_team'] == team else row['home_score'], axis = 1)
    return results.mean()

# training row
def build_training_row(row, df):
    home_team = row['home_team']
    away_team = row['away_team']
    date = row['date']

    return {
        'home_win_pct': get_win_percentage(home_team, date, df),
        'away_win_pct': get_win_percentage(away_team, date, df),
        'home_goals_scored': get_avg_goals_scored(home_team, date, df),
        'away_goals_scored': get_avg_goals_scored(away_team, date, df),
        'home_goals_conceded': get_avg_goals_conceded(home_team, date, df),
        'away_goals_conceded': get_avg_goals_conceded(away_team, date, df),
        'is_competitive': row['is_competitive'],
        'is_home': row['is_home'],
        'result': row['result']
    }

# apply the get_result function to each row of the dataframe to create a new 'result' column
df['result'] = df.apply(get_result, axis=1)
df['is_competitive'] =(df['tournament'] != 'Friendly').astype(int)
df['is_home'] = (~df['neutral']).astype(int)

full_df = df.copy()
df = df[df['tournament'].str.contains('FIFA World Cup')]
# print(len(df))

#print(df[['neutral', 'is_home']].head(10))
# sample_df = df.head(500)
# training_data = df.apply(lambda row: build_training_row(row, full_df), axis=1, result_type='expand')
# training_data.to_csv('training_data.csv', index=False)
training_data = pd.read_csv('training_data.csv')
training_data['target'] = training_data['result'].map({'home_win': 0, 'draw': 1, 'away_win': 2})

x = training_data.drop(columns=['result', 'target'])
y = training_data['target']

print(x.shape)
print(y.value_counts())

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")