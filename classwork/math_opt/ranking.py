import pandas as pd
import numpy as np

dfp = pd.read_pickle(r"C:\Users\jonat\GSE 524\data\ncaa.pkl")
name = ['jebucher']

# construct A matrix
    # diagonal entries are the number of games played by team i
    # off diagonal is -1 * (how many games played against team j)

# construct b-vector
    # ith element is the point margin for the team

# Ax = b for x (ranking for each team, high is better)

# Normalize the array

def cfb_rank(df) -> list:
    """
    Computes college football team rankings

    Args:
        df (DataFrame): a Pandas DataFrame with 5 columns:
            - team (str)
            - wins (int)
            - losses (int)
            - pointdiff (int)
            - opponents (array)

    Returns:
        list of length three:
            - dataframe with two sorted columns, 'team', and 'score'
            - A matrix
            - b vector 
    """

    # find how many entries in dataframe
    n = len(df)

    a = np.zeros((n, n))

    b = np.zeros((n, 1))

    for i in range(n):
        # fill diagonal with the number of games played by team i
        a[i, i] = len(df.loc[i, 'opponents'])

        # fill b vector with the point margin for team i
        b[i] = df.loc[i, 'pointdiff']

        # fill the rest of the row with opponents played
        for j in df.loc[i, 'opponents']:

            a[i,j] -= 1

    # solve linear system for rankings
    x = np.linalg.solve(a, b)

    # normalize
    x_bar = x.mean()
    x -= x_bar

    # create return dataframe
    return_df = pd.DataFrame()
    return_df['team'] = df['team']
    return_df['score'] = x

    # sort the values to be in descending order
    return_df.sort_values('score', ascending = False, inplace = True)

    return (return_df, a, b)

test_df = cfb_rank(dfp)[0]
print(test_df[:5])

