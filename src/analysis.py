
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
m1 = m_df2['release_week'] == 50
week_50_profit = sum(m_df2['ww_gross_IA'][m1]) - sum(m_df2['budget_IA'][m1])
avatar = m_df2['title'] == 'Avatar'
star_wars = m_df2['title'] == 'Star Wars: Episode VII - The Force Awakens'
top_2_profit = sum(m_df2['ww_gross_IA'][avatar | star_wars]) - sum(m_df2['budget_IA'][avatar | star_wars])
print(top_2_profit / week_50_profit)

# by decade....
start = 1940
end = 2010
m1 = m_df2['release_decade'] >= start
dec = m_df2[m1].groupby(['release_decade', 'is_prime']).agg({'title': 'count',
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
m1 = m_df2['release_year'] >= start
dec = m_df2[m1].groupby(['release_year', 'is_prime']).agg({'title': 'count',
                                    'is_success': 'sum'}).reset_index()
dec['success_rate'] = dec['is_success'] / dec['title']

decades = np.linspace(start, end, (end - start) + 1)

fig, ax = plt.subplots(1, 1, figsize = (8,6))
ax.plot(decades, dec['success_rate'][dec['is_prime'] == 1], color = 'b', label = 'Prime', alpha = 0.5)
ax.plot(decades, dec['success_rate'][dec['is_prime'] == 0], color = 'r', label = 'Not Prime', alpha = 0.5)
ax.legend()
ax.set_title('Success Rate, Prime v Not Prime')
ax.set_ylim(0, 1)
plt.savefig('images/years.jpeg')
plt.close()


# scatter plot of perf_ratio and budget_IA
# DONT USE THIS.....
# fig, ax = plt.subplots(1, 1, figsize = (10,7))
# ax.scatter(m_df2['perf_ratio'], m_df2['budget_IA'])
# ax.set_xlim(0, 10)
# ax.set_ylim(0, 100000000)
# plt.savefig('images/perf_scatter.jpeg')
# plt.close()

# performance by genre, prime v not prime
g_dict = {}
for genre in genres:
    c = 'is_' + genre
    m1 = m_df2[c] == 1
    m2 = m_df2['is_prime'] == 1
    m3 = m_df2['is_prime'] == 0
    g_dict[genre] = {'prime': sum(m_df2['is_success'][m1 & m2]) / 
                                len(m_df2['title'][m1 & m2]),
                    'not_prime': sum(m_df2['is_success'][m1 & m3]) / 
                                len(m_df2['title'][m1 & m3])}

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

if __name__ == '__main__':
    pass