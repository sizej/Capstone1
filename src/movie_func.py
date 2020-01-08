import pandas as pd 
import numpy as np 

def genre_col(g_name, g):
    '''
    Looks at the genre column and returns 1 if g_name is in genre
    '''
    if g_name in g:
        return 1
    else:
        return 0

def weekly_plot(col):
    '''
    Creates 52 plot of some column
    '''
    pass

def get_dollars(s):
    '''
    Function to strip out dollar signs/other currency signs and conver
    to int
    '''
    if s[0] == '$':
        return int(s[s.find(' ') + 1:])
    else:
        return 'Not US'

# pulls in CPI data for inflation adjustment
inflation_df = pd.read_csv('/Users/size/DSI/repos/Capstone1/data/CPIAUCNS.csv')
inflation_df['DATE'] = pd.to_datetime(inflation_df['DATE'])
inflation_df['CPI_mult'] = inflation_df['CPIAUCNS'].iloc[-1] / inflation_df['CPIAUCNS']
end_date = max(inflation_df['DATE'])

def inflation_adjustment(amt, date, end = end_date):
    '''
    Adjusts a value for inflation, indexing at last measured CPI (i.e. Nov 2019)
    '''
    if date < end:
        idx = min(np.where(inflation_df['DATE'] >= date)[0])
        adj = inflation_df['CPI_mult'][idx]
        return amt * adj
    else:
        return amt

def determine_prime(week, starts, ends):
    '''
    Determines if date falls inside of a 'prime' window
    '''
    for i in range(len(starts)):
        if starts[i] <= week <= ends[i]:
            return 1
    return 0

def competitor_count(week, year, df):
    '''
    Returns the competitive set for a film, given the release week and release year.
    Competitive set is defined as count of movies that came out the same week, one week,
    before, and one week after
    '''
    if 0 < week < 51:
        weeks = [week - 1, week, week + 1]
        m1 = df['release_week'].isin(weeks)
        m2 = df['release_year'] == year
        return df['title'][m1 & m2].count() - 1
    elif week == 0:
        m1a = df['release_week'] == 51
        m1b = df['release_year'] == year - 1
        m1 = m1a & m1b
        m2a = df['release_week'].isin([0,1])
        m2b = df['release_year'] == year
        m2 = m2a & m2b
        return df['title'][m1 | m2].count() - 1
    elif week == 51:
        m1a = df['release_week'] == 0
        m1b = df['release_year'] == year + 1
        m1 = m1a & m1b
        m2a = df['release_week'].isin([50,51])
        m2b = df['release_year'] == year
        m2 = m2a & m2b
        return df['title'][m1 | m2].count() - 1
        
if __name__ == '__main__':
    pass