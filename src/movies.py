import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import movie_func as mf
import datetime as dt 

plt.style.use('fivethirtyeight')

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
m_df2['is_success_25'] = [1 if x >= 2.5 else 0 for x in m_df2['perf_ratio']]
m_df2['is_success_4'] = [1 if x >= 4 else 0 for x in m_df2['perf_ratio']]

# Adjust budget, ww_gross, and usa_gross for inflation
m_df2['budget_IA'] = m_df2.apply(lambda row: mf.inflation_adjustment(row['budget'], row['release_date']), 
                                axis = 1)
m_df2['ww_gross_IA'] = m_df2.apply(lambda row: mf.inflation_adjustment(row['ww_gross'], row['release_date']), 
                                axis = 1)
m_df2['usa_gross_IA'] = m_df2.apply(lambda row: mf.inflation_adjustment(row['usa_gross'], row['release_date']), 
                                axis = 1)                            

# get some columns to breakdown movies across various times
# by month, week, etc.
m_df2['release_month'] = [x.month for x in m_df2['release_date']]
m_df2['release_week'] = [x.timetuple().tm_yday // 7 for x in m_df2['release_date']]
# 10 films released on/about NYE, move to week 51
m_df2['release_week'] = [x if x != 52 else 51 for x in m_df2['release_week']]

# Group by release week or release month and compare success rate
rel_week_df = m_df2.groupby('release_week').agg({'is_success_25': 'sum',
                                                'is_success_4': 'sum',
                                                'title': 'count',
                                                'budget_IA': 'sum',
                                                'ww_gross_IA': 'sum'})
rwd_cols = {'is_success_25': 'successes_25',
            'is_success_4': 'successes_4',
            'title': 'supply',
            'budget_IA': 'total_budget',
            'ww_gross_IA': 'total_ww_gross'}
rel_week_df.rename(columns = rwd_cols, inplace = True)

rel_week_df['success_rate_25'] = rel_week_df['successes_25'] / rel_week_df['supply']
rel_week_df['success_rate_4'] = rel_week_df['successes_4'] / rel_week_df['supply']

# Create a stacked bar chart of film success by month
fig, ax = plt.subplots(1,1, figsize = (8,6))
xloc = np.arange(len(rel_week_df['success_rate_25']))
ax.plot(xloc, rel_week_df['success_rate_25'], label = '250% Success Rate')
ax.plot(xloc, rel_week_df['success_rate_4'], label = '400% Success Rate')
ax.legend()
plt.savefig('images/test.jpeg')

fig, ax = plt.subplots(1,1, figsize = (12,5))
ax.bar(xloc, rel_week_df['successes_25'], color = 'blue')
ax.bar(xloc, rel_week_df['supply'], color = 'orange', bottom = rel_week_df['successes_25'])
plt.savefig('images/stack_test.jpeg')


if __name__ == '__main__':
    pass