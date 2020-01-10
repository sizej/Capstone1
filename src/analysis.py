import scipy.stats as stats
from statsmodels.stats.weightstats import ztest
import pandas as pd 
import numpy as np 
import movie_func as mf 
import matplotlib.pyplot as plt
from movies import genres
from hypo_test import HypoZtest


movies_clean_df = pd.read_csv('data/clean_movies.csv')


# pie chart for fun
lbl = ['Not September', 'September']
data = [1,0]
fig, ax = plt.subplots(1, 1, figsize = (8, 6))
ax.pie(data)
ax.set_title('G-Rated Movies Release Month since 1990')
ax.legend(lbl, loc = 'lower left')
plt.tight_layout(pad = 2)
plt.savefig('images/forkayla.jpeg')
plt.close('all')

# what percentage of most profitable week attributable to top 2....
m1 = movies_clean_df['release_week'] == 50
week_50_profit = sum(movies_clean_df['ww_gross_IA'][m1]) - sum(movies_clean_df['budget_IA'][m1])
avatar = movies_clean_df['title'] == 'Avatar'
star_wars = movies_clean_df['title'] == 'Star Wars: Episode VII - The Force Awakens'
top_2_profit = sum(movies_clean_df['ww_gross_IA'][avatar | star_wars]) - sum(movies_clean_df['budget_IA'][avatar | star_wars])
print(top_2_profit / week_50_profit)

# by decade....
start = 1970
end = 2010
m1 = movies_clean_df['release_decade'] >= start
dec = movies_clean_df[m1].groupby(['release_decade', 'is_prime']).agg({'title': 'count',
                                    'is_success': 'sum'}).reset_index()
dec['success_rate'] = dec['is_success'] / dec['title']

decades = np.linspace(start, end, (end - start)/10 + 1)

fig, ax = plt.subplots(1, 1, figsize = (8,6))
ax.plot(decades, dec['success_rate'][dec['is_prime'] == 1], color = 'b', label = 'Prime', alpha = 0.5)
ax.plot(decades, dec['success_rate'][dec['is_prime'] == 0], color = 'r', label = 'Not Prime', alpha = 0.5)
ax.legend()
plt.savefig('images/decades.jpeg')
plt.close()

# by year.....
start = 1970
end = 2019
m1 = movies_clean_df['release_year'] >= start
dec = movies_clean_df[m1].groupby(['release_year', 'is_prime']).agg({'title': 'count',
                                    'is_success': 'sum'}).reset_index()
dec['success_rate'] = dec['is_success'] / dec['title']

decades = np.linspace(start, end, (end - start) + 1)
releases = [dec['title'][dec['release_year'] == year].sum() for year in dec['release_year'].unique()]
fig, ax = plt.subplots(1, 2, figsize = (12,6))
ax[0].plot(decades, dec['success_rate'][dec['is_prime'] == 1], color = 'b', label = 'Prime', alpha = 0.5)
ax[0].plot(decades, dec['success_rate'][dec['is_prime'] == 0], color = 'r', label = 'Not Prime', alpha = 0.5)
ax[0].legend()
ax[0].set_title('Success Rate, Prime v Not Prime')
ax[0].set_ylim(0, 1)
ax[1].bar(decades, releases, color = 'b', alpha = 0.5, label = 'Films per year')
ax[1].legend()
plt.tight_layout(pad = 2)
plt.savefig('images/years_sr_supply.jpeg')
plt.close()

# hypothesis test #1 - does prime window mattter
alpha = 0.05
m1 = movies_clean_df['is_prime'] == 1
prime_results = movies_clean_df['is_success'][m1]
m2 = movies_clean_df['is_prime'] == 0
not_prime_results = movies_clean_df['is_success'][m2]
prime_ztest = HypoZtest(prime_results, not_prime_results, val = 0, alpha = 0.05, alt = 'larger')
print(f'Prime v Not Prime Results: {prime_ztest.result}.')

# hypothesis test #2 - does a lot of competition matter - 2 comparisons low v mid, high v mid
competitor_df = movies_clean_df.groupby(['release_year', 'release_week']).agg({'competitors': 'mean'})
high_comp_threshold = 13
low_comp_threshold = 5
m1 = competitor_df['competitors'] <= low_comp_threshold
m2 = competitor_df['competitors'] >= high_comp_threshold
low_comp_count = competitor_df[m1].count()
high_comp_count = competitor_df[m2].count()
med_comp_count = competitor_df[-m1 & -m2].count()
all_count = competitor_df.count()
print(low_comp_count/all_count, high_comp_count / all_count)

fig, ax = plt.subplots(1, 1, figsize = (8,6))
ax.hist(competitor_df['competitors'], bins = 25, color = 'b', alpha = 0.5, align = 'mid')
ax.axvline(low_comp_threshold, color = 'r', linestyle = '--', linewidth = 2)
ax.axvline(high_comp_threshold, color = 'r', linestyle = '--', linewidth = 2)
ax.set_title('Weeks with Competitors since 1970')
plt.savefig('images/competitor_hist.jpeg')
plt.close()

# Get the separate sets by high, mid, low competitive sets
alpha = 0.025
m1 = movies_clean_df['competitors'] <= low_comp_threshold
m2 = movies_clean_df['competitors'] >= high_comp_threshold
high_comp_results = movies_clean_df['is_success'][m2]
low_comp_results = movies_clean_df['is_success'][m1]
mid_comp_results = movies_clean_df['is_success'][-m1 & -m2]
low_comp_ztest = HypoZtest(low_comp_results, mid_comp_results, val = 0, alpha = alpha, alt = 'larger')
high_comp_ztest = HypoZtest(high_comp_results, mid_comp_results, val = 0, alpha = alpha, alt = 'smaller')
print(f'Low Comp Results: {low_comp_ztest.result}.')
print(f'High Comp Results: {high_comp_ztest.result}.')

# Break out 2000s for separate hypo test
m1 = movies_clean_df['release_year'] >= 2000
movies_2000s_df = movies_clean_df[m1].copy()
competitor_df = movies_2000s_df.groupby(['release_year', 'release_week']).agg({'competitors': 'mean'})
high_comp_threshold = 16
low_comp_threshold = 9
low_mask = movies_2000s_df['competitors'] <= low_comp_threshold
high_mask = movies_2000s_df['competitors'] >= high_comp_threshold
low_comp_count = movies_2000s_df['is_success'][low_mask].count()
high_comp_count = movies_2000s_df['is_success'][high_mask].count()
print(low_comp_count, high_comp_count, movies_2000s_df['competitors'].count() - low_comp_count - high_comp_count)


fig, ax = plt.subplots(1, 1, figsize = (8,6))
competitor_df = movies_2000s_df.groupby(['release_year', 'release_week']).agg({'competitors': 'mean'})
ax.hist(competitor_df['competitors'], bins = 24, color = 'b', alpha = 0.5, align = 'mid')
ax.axvline(low_comp_threshold, color = 'r', linestyle = '--', linewidth = 2)
ax.axvline(high_comp_threshold, color = 'r', linestyle = '--', linewidth = 2)
ax.set_title('Weeks with Competitors since 2000')
plt.savefig('images/competitor_hist_2000.jpeg')
plt.close()

# Get the separate sets by high, mid, low competitive sets
alpha = 0.025
high_comp_results = movies_2000s_df['is_success'][high_mask]
low_comp_results = movies_2000s_df['is_success'][low_mask]
mid_comp_results = movies_2000s_df['is_success'][-low_mask & -high_mask]
low_comp_2000s_ztest = HypoZtest(low_comp_results, mid_comp_results, val = 0, alpha = alpha, alt = 'larger')
high_comp_2000s_ztest = HypoZtest(high_comp_results, mid_comp_results, val = 0, alpha = alpha, alt = 'smaller')
print(f'2000s Low Comp Results: {low_comp_2000s_ztest.result}.')
print(f'2000s High Comp Results: {high_comp_2000s_ztest.result}.')

# performance by genre, prime v not prime
g_dict = {}
for genre in genres:
    c = 'is_' + genre
    m1 = movies_clean_df[c] == 1
    m2 = movies_clean_df['is_prime'] == 1
    m3 = movies_clean_df['is_prime'] == 0
    if movies_clean_df['title'][m1].count() > 0:
        g_dict[genre] = {'prime': sum(movies_clean_df['is_success'][m1 & m2]) / 
                                    len(movies_clean_df['title'][m1 & m2]),
                        'not_prime': sum(movies_clean_df['is_success'][m1 & m3]) / 
                                    len(movies_clean_df['title'][m1 & m3]),
                        'mean_budget': np.mean(movies_clean_df['budget_IA'][m1])}

fig, ax = plt.subplots(1, 1, figsize = (12, 8))
xloc = np.arange(len(g_dict))
width = 0.4
ax.bar(xloc, [x['prime'] for x in g_dict.values()], width = width, color = 'b', alpha = 0.5, label = 'Prime')
ax.bar(xloc + width, [x['not_prime'] for x in g_dict.values()], width = width, color = 'r', alpha = 0.5, label = 'Not Prime')
ax.set_xticks(xloc)
ax.set_xticklabels(genres, rotation = 45)
ax.legend()
ax.set_title('Success Rate by Genre - Prime v Not Prime')
plt.tight_layout(pad = 2)
plt.savefig('images/genre_bar.jpeg')
plt.close()

# split out big budget films for separate analysis
fig, ax = plt.subplots(1, 1, figsize = (12,8))
xloc = np.arange(len(g_dict))
width = 0.6
ax.bar(xloc, [x['mean_budget'] for x in g_dict.values()], width = width, color = 'b', alpha = 0.5, label = 'Mean Budget')
ax.set_xticks(xloc)
ax.set_xticklabels([g for g in g_dict], rotation = 45)
ax.set_yticklabels([f'${x:0.0f}M' for x in np.linspace(0, 80, 5)])
ax.legend()
ax.set_title('Mean Budget by Genre')
plt.tight_layout(pad = 2)
plt.savefig('images/genre_budget.jpeg')
plt.close()


# get a scatter plot of competitors v success_rate
comp_df = movies_clean_df.groupby(['release_year', 'release_week']).agg({'competitors': 'mean',
                                                                'is_success': 'sum',
                                                                'title': 'count'}).reset_index()
comp_df['success_rate'] = comp_df['is_success'] / comp_df['title']
fig, ax = plt.subplots(1, 1, figsize = (8,6))
ax.scatter(comp_df['competitors'], comp_df['success_rate'])
plt.savefig('images/comp_scatter.jpeg')
plt.close()

# filter down to just big-budget films
m1 = movies_2000s_df['budget_IA'] >= np.percentile(movies_2000s_df['budget_IA'], 75)
big_budget_df = movies_2000s_df[m1].copy()
big_budget_df['competitors'] = big_budget_df.apply(lambda row: mf.competitor_count(row['release_week'], row['release_year'], big_budget_df), axis = 1)
rel_week_big_budg = big_budget_df.groupby('release_week').agg({'is_success': 'sum',
                                                                'title': 'count',
                                                                'budget_IA': 'mean'})
rwd_cols = {'is_success': 'successes',
            'title': 'supply',
            'budget_IA': 'mean_budget'}
rel_week_big_budg.rename(columns = rwd_cols, inplace = True)
rel_week_big_budg['success_rate'] = rel_week_big_budg['successes'] / rel_week_big_budg['supply']
pw_starts = [19.5, 46.5]
pw_ends = [32.5, 51.5]
xloc = np.arange(len(rel_week_big_budg['supply']))
c = ['r' if ((pw_starts[0] < x < pw_ends[0]) or (pw_starts[1] < x < pw_ends[1])) else 'b' for x in xloc]
fig, ax = plt.subplots(3,1, figsize = (14, 10))
ax[0].bar(xloc, rel_week_big_budg['success_rate'], color = c, alpha = 0.5, label = 'Success Rate')
ax[0].set_title('Success Rate')
ax[0].axhline(sum(rel_week_big_budg['successes']) / sum(rel_week_big_budg['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[0].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
ax[1].bar(xloc, rel_week_big_budg['mean_budget'], color = c, alpha = 0.5, label = 'Mean Budget')
ax[1].set_title('Mean Budget per Film')
ax[1].set_yticklabels([f'${x:0.0f}M' for x in np.linspace(0, 150, 4)])
ax[1].axhline(rel_week_big_budg['mean_budget'].mean(), color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[1].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
ax[2].bar(xloc, rel_week_big_budg['supply'], color = c, alpha = 0.5, label = 'Count of Films Released')
ax[2].set_title('Count of Films Released')
ax[2].axhline(sum(rel_week_big_budg['supply']) / len(rel_week_big_budg['supply']), color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_starts[0], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_ends[0], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_starts[1], color = 'r', linestyle = '--', linewidth = 2)
ax[2].axvline(pw_ends[1], color = 'r', linestyle = '--', linewidth = 2)
plt.tight_layout(pad = 2)
plt.savefig('images/big_budg_comparison_hilite.jpeg')
plt.close()

# hypo test A - prime v not prime
alpha = 0.05
m1 = big_budget_df['is_prime'] == 1
prime_results = big_budget_df['is_success'][m1]
m2 = big_budget_df['is_prime'] == 0
not_prime_results = big_budget_df['is_success'][m2]
big_budg_prime_ztest = HypoZtest(prime_results, not_prime_results, alpha  = alpha, val = 0, alt = 'larger')
print(f'Big Budget Prime v Not Prime Results: {big_budg_prime_ztest.result}.')

# hypo test B - low, high v mid
alpha = 0.025
low_comp_threshold = 1
high_comp_threshold = 5
low_mask = big_budget_df['competitors'] <= low_comp_threshold
high_mask = big_budget_df['competitors'] >= high_comp_threshold
low_comp_results = big_budget_df['is_success'][low_mask]
high_comp_results = big_budget_df['is_success'][high_mask]
mid_comp_results = big_budget_df['is_success'][-low_mask & -high_mask]
big_budg_low_comp_ztest = HypoZtest(low_comp_results, mid_comp_results, alpha = 0.025, alt = 'larger')
big_budg_high_comp_ztest = HypoZtest(high_comp_results, mid_comp_results, alpha = 0.025, alt = 'smaller')
print(f'Big Budget Low Comp Results: {big_budg_low_comp_ztest.result}.')
print(f'Big Budget High Comp Results: {big_budg_high_comp_ztest.result}.')

if __name__ == '__main__':
    pass