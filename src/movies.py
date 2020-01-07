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
success_threshold = 3
m_df2['is_success'] = [1 if x >= success_threshold else 0 for x in m_df2['perf_ratio']]

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
rel_week_df = m_df2.groupby('release_week').agg({'is_success': 'sum',
                                                'title': 'count',
                                                'budget_IA': 'sum',
                                                'ww_gross_IA': 'sum'})
rwd_cols = {'is_success': 'successes',
            'title': 'supply',
            'budget_IA': 'total_budget',
            'ww_gross_IA': 'total_ww_gross'}
rel_week_df.rename(columns = rwd_cols, inplace = True)
rel_week_df['success_rate'] = rel_week_df['successes'] / rel_week_df['supply']
mean_success_rate = sum(rel_week_df['successes']) / sum(rel_week_df['supply'])
rel_week_df['marg_success_rate'] = rel_week_df['success_rate'] / mean_success_rate
rel_week_df['mean_budget'] = rel_week_df['total_budget'] / rel_week_df['supply']
ave_budget = sum(rel_week_df['total_budget']) / sum(rel_week_df['supply'])
rel_week_df['mean_budget_norm'] = rel_week_df['mean_budget'] / ave_budget
mean_supply = sum(rel_week_df['supply']) / len(rel_week_df['supply'])
rel_week_df['supply_norm'] = rel_week_df['supply'] / mean_supply


# get side-by-side comparison of success_rate, mean_budget, and supply
fig, ax = plt.subplots(3,1, figsize = (14, 10))
xloc = np.arange(len(rel_week_df['supply']))
ax[0].bar(xloc, rel_week_df['success_rate'], color = 'b', alpha = 0.5, label = 'Success Rate')
ax[0].set_title('Success Rate')
ax[0].axhline(sum(rel_week_df['successes']) / sum(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(19.5, color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(32.5, color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(46.5, color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(51.5, color = 'r', linestyle = '--', linewidth = 2)
ax[1].bar(xloc, rel_week_df['mean_budget'], color = 'b', alpha = 0.5, label = 'Mean Budget')
ax[1].set_title('Mean Budget per Film')
ax[1].axhline(sum(rel_week_df['total_budget']) / sum(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(19.5, color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(32.5, color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(46.5, color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(51.5, color = 'r', linestyle = '--', linewidth = 2)
ax[2].bar(xloc, rel_week_df['supply'], color = 'b', alpha = 0.5, label = 'Count of Films Released')
ax[2].set_title('Count of Films Released')
ax[2].axhline(sum(rel_week_df['supply']) / len(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(19.5, color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(32.5, color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(46.5, color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(51.5, color = 'r', linestyle = '--', linewidth = 2)
plt.tight_layout(pad = 2)
plt.savefig('images/comparison.jpeg')
plt.close()

# Calculate the differences between success and budget/supply
diff1 = rel_week_df['marg_success_rate'] - rel_week_df['mean_budget_norm'] 
c1 = ['g' if x > 0 else 'r' for x in diff1]
diff2 = rel_week_df['marg_success_rate'] - rel_week_df['supply_norm']
c2 = ['g' if x > 0 else 'r' for x in diff2]

# Create a horizontal bar chart for the differences....
fig, ax = plt.subplots(1,2, figsize = (10,14))
xloc = np.arange(len(rel_week_df['mean_budget_norm']))
ax[0].barh(xloc[::-1], diff1[::-1], align = 'center', alpha = 0.4, color = c1, label = 'Success v Budget')
ax[1].barh(xloc[::-1], diff2[::-1], align = 'center', alpha = 0.4, color = c2, label = 'Success v Supply')
plt.legend()
plt.savefig('images/differences.jpeg')
plt.close()


if __name__ == '__main__':
    pass