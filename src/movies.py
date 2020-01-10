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
movies_initial_df = movie_df[m1 & m2].copy().reset_index()

# renaming a few columns for ease of use
movies_initial_df.rename(columns = {'worlwide_gross_income': 'ww_gross', 
                        'usa_gross_income': 'usa_gross',
                        'date_published': 'release_date',
                        'actors': 'cast',
                        'reviews_from_users': 'user_reviews',
                        'reviews_from_critics': 'critics_reviews'}, inplace = True)

# Converting some strings to ints and datetimes
movies_initial_df['budget'] = movies_initial_df['budget'].apply(mf.get_dollars)
movies_initial_df['usa_gross'] = movies_initial_df['usa_gross'].apply(mf.get_dollars)
movies_initial_df['ww_gross'] = movies_initial_df['ww_gross'].apply(mf.get_dollars)
movies_initial_df['release_date'] = pd.to_datetime(movies_initial_df['release_date'])

# Break out genre into three columns
movies_initial_df['genre'] = [x.split(', ') for x in movies_initial_df['genre']]
genre_df = pd.DataFrame(movies_initial_df['genre'].values.tolist(), columns = ['genre1', 'genre2', 'genre3'])
movies_initial_df = movies_initial_df.join(genre_df, how = 'left')

# Get the set of unique genres
g1 = []
for x in movies_initial_df['genre']:
    for i in x:
        g1.append(i)
genres = set(g1)

# Set up dummy columns for set of genres
for genre in genres:
    col_name = 'is_' + genre
    movies_initial_df[col_name] = movies_initial_df.apply(lambda row: mf.genre_col(genre, row['genre']), axis = 1)

# calculate performance metric (ww_gross / budget)
m1 = movies_initial_df['budget'] != 'Not US'
m2 = movies_initial_df['release_date'] >= dt.datetime(1970, 1, 1)
movies_clean_df = movies_initial_df[m1 & m2].copy()
movies_clean_df['perf_ratio'] = pd.to_numeric(movies_clean_df['ww_gross'] / movies_clean_df['budget'])
success_threshold = 3
movies_clean_df['is_success'] = [1 if x >= success_threshold else 0 for x in movies_clean_df['perf_ratio']]

# Adjust budget, ww_gross, and usa_gross for inflation
movies_clean_df['budget_IA'] = movies_clean_df.apply(lambda row: mf.inflation_adjustment(row['budget'], row['release_date']), 
                                axis = 1)
movies_clean_df['ww_gross_IA'] = movies_clean_df.apply(lambda row: mf.inflation_adjustment(row['ww_gross'], row['release_date']), 
                                axis = 1)
movies_clean_df['usa_gross_IA'] = movies_clean_df.apply(lambda row: mf.inflation_adjustment(row['usa_gross'], row['release_date']), 
                                axis = 1)
movies_clean_df['profit'] = movies_clean_df['ww_gross_IA'] - movies_clean_df['budget_IA']                            

# get some columns to breakdown movies across various times
# by decade, year, month, week, etc.
movies_clean_df['release_decade'] = [x.year // 10 * 10 for x in movies_clean_df['release_date']]
movies_clean_df['release_year'] = [x.year for x in movies_clean_df['release_date']]
movies_clean_df['release_month'] = [x.month for x in movies_clean_df['release_date']]
movies_clean_df['release_week'] = [x.timetuple().tm_yday // 7 for x in movies_clean_df['release_date']]
# 10 films released on/about NYE, move to week 51
movies_clean_df['release_week'] = [x if x != 52 else 51 for x in movies_clean_df['release_week']]


# Group by release week or release month and compare success rate
rel_week_df = movies_clean_df.groupby('release_week').agg({'is_success': 'sum',
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
rel_week_df['success_rate_norm'] = rel_week_df['success_rate'] / mean_success_rate
rel_week_df['mean_budget'] = rel_week_df['total_budget'] / rel_week_df['supply']
mean_budget = sum(rel_week_df['total_budget']) / sum(rel_week_df['supply'])
rel_week_df['mean_budget_norm'] = rel_week_df['mean_budget'] / mean_budget
mean_supply = sum(rel_week_df['supply']) / len(rel_week_df['supply'])
rel_week_df['supply_norm'] = rel_week_df['supply'] / mean_supply

# Charts for intro/background
# Revenue by week
fig, ax = plt.subplots(1, 1, figsize = (8,6))
x = np.arange(52)
ax.bar(x, rel_week_df['total_ww_gross'], color = 'b', alpha = 0.5, label = 'WW Gross Revenue')
ax.set_title('Worldwide Gross Revenue by Week')
ax.set_yticklabels([f'${x:0.0f}B' for x in np.linspace(0, 30, 7)])
plt.tight_layout(pad = 1)
plt.savefig('images/revenue.jpeg')
plt.close()
# Budget by week
fig, ax = plt.subplots(1, 1, figsize = (8,6))
x = np.arange(52)
ax.bar(x, rel_week_df['total_budget'], color = 'b', alpha = 0.5, label = 'Total Budget')
ax.set_title('Total Budget by Week')
ax.set_yticklabels([f'${x:0.0f}M' for x in np.linspace(0, 800, 9)])
plt.tight_layout(pad = 1)
plt.savefig('images/budget.jpeg')
plt.close()
# Profit by week
fig, ax = plt.subplots(1, 1, figsize = (8,6))
x = np.arange(52)
ax.bar(x, rel_week_df['total_ww_gross'] - rel_week_df['total_budget'], color = 'b', alpha = 0.5, label = 'Profit')
ax.set_title('Total "Profit" by Week')
ax.set_yticklabels([f'${x:0.0f}B' for x in np.linspace(0, 25, 6)])
plt.tight_layout(pad = 1)
plt.savefig('images/profit.jpeg')
plt.close()

# get side-by-side comparison of success_rate, mean_budget, and supply
pw_starts = [19.5, 46.5]
pw_ends = [32.5, 51.5]
xloc = np.arange(len(rel_week_df['supply']))
c = ['r' if ((pw_starts[0] < x < pw_ends[0]) or (pw_starts[1] < x < pw_ends[1])) else 'b' for x in xloc]
fig, ax = plt.subplots(3,1, figsize = (14, 10))
ax[0].bar(xloc, rel_week_df['success_rate'], color = c, alpha = 0.5, label = 'Success Rate')
ax[0].set_title('Success Rate')
ax[0].axhline(sum(rel_week_df['successes']) / sum(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
ax[1].bar(xloc, rel_week_df['mean_budget'], color = c, alpha = 0.5, label = 'Mean Budget')
ax[1].set_title('Mean Budget per Film')
ax[1].set_yticklabels([f'${x:0.0f}M' for x in np.linspace(0, 60, 4)])
ax[1].axhline(sum(rel_week_df['total_budget']) / sum(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
ax[2].bar(xloc, rel_week_df['supply'], color = c, alpha = 0.5, label = 'Count of Films Released')
ax[2].set_title('Count of Films Released')
ax[2].axhline(sum(rel_week_df['supply']) / len(rel_week_df['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
plt.tight_layout(pad = 2)
plt.savefig('images/comparison_hilite.jpeg')
plt.close()

# Add an is_prime flag
movies_clean_df['is_prime'] = movies_clean_df.apply(lambda row: mf.determine_prime(row['release_week'], pw_starts, pw_ends), axis = 1)

# create competitive films column (films released week before and week after)
movies_clean_df['competitors'] = movies_clean_df.apply(lambda row: mf.competitor_count(row['release_week'], row['release_year'], movies_clean_df), axis = 1)

movies_clean_df.to_csv('data/clean_movies.csv')

if __name__ == '__main__':
    pass