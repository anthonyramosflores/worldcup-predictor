import pandas as pd

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

# get_avg_goals_scored calculates the average goals scored by a team in their last n matches before a given date
def get_avg_goals_score(team, date, df, n = 10):
    team_matches = df[
        ((df['home_team'] == team) | (df['away_team'] == team)) &
        (df['date'] < date)
    ].tail(n)

    if len(team_matches) == 0:
        return 0

    # for each row, get the goals score by the team

    results = team_matches.apply(lambda row: row['home_score'] if row['home_team'] == team else row['away_score'], axis=1)
    return results.mean() 
    

# apply the get_result function to each row of the dataframe to create a new 'result' column
df['result'] = df.apply(get_result, axis=1)

# Code commented out for now
# print(df[['home_team', 'away_team', 'home_score', 'away_score', 'result']].head())

# code commented out for now, used for testing
# print(get_win_percentage('San Merino', '2022-01-01', df))

print(get_avg_goals_score('Brazil', '2022-11-01', df))