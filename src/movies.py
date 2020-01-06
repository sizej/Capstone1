import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import movie_func as mf
import datetime as dt 

# import movies csv and filter down by following criteria:
# 1. Has a USA gross income
# 2. Has a budget
# 3. Produced by a major or mid-major studio (this could also be
#  done with budget minimum or gross income minimum [though this would
#  require an inflation adjusted figure])

movie_df = pd.read_csv('/Users/size/DSI/repos/Capstone1/data/movies.csv')
m1 = movie_df['usa_gross_income'].notna()
m2 = movie_df['budget'].notna()
m_df = movie_df[m1 & m2].copy().reset_index()

# renaming a few columns for ease of use
m_df.rename(columns = {'worlwide_gross_income': 'ww_gross', 
                        'usa_gross_income': 'usa_gross',
                        'date_published': 'release_date',
                        'actors': 'cast',
                        'reviews_from_users': 'user_reviews',
                        'reviews_from_critics': 'critics_reviews'}, inplace = True)

# Converting some strings to ints and datetimes
m_df['budget'] = m_df['budget'].apply(mf.get_dollars)
m_df['usa_gross'] = m_df['usa_gross'].apply(mf.get_dollars)
m_df['ww_gross'] = m_df['ww_gross'].apply(mf.get_dollars)
m_df['release_date'] = pd.to_datetime(m_df['release_date'])

# Break out genre into three columns
m_df['genre'] = [x.split(', ') for x in m_df['genre']]
genre_df = pd.DataFrame(m_df['genre'].values.tolist(), columns = ['genre1', 'genre2', 'genre3'])
m_df = m_df.join(genre_df, how = 'left')

# Get the set of unique genres
g1 = []
for x in m_df['genre']:
    for i in x:
        g1.append(i)
genres = set(g1)

# calculate performance metric (ww_gross / budget)
m_df2 = m_df[m_df['budget'] != 'Not US'].copy()
m_df2['perf_ratio'] = m_df2['ww_gross'] / m_df2['budget']
# Adjust budget, ww_gross, and usa_gross for inflation
m_df2['budget_IA'] = m_df2.apply(lambda row: mf.inflation_adjustment(row['budget'], row['release_date']), 
                                axis = 1)

# get some columns to breakdown movies across various times
# by month, week, etc.
m_df2['release_month'] = [x.month for x in m_df2['release_date']]
m_df2['release_week'] = [x.timetuple().tm_yday // 7 for x in m_df2['release_date']]



if __name__ == '__main__':
    pass