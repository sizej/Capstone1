import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import movie_func as mf

# import movies csv and filter down by following criteria:
# 1. Has a USA gross income
# 2. Has a budget
# 3. Produced by a major or mid-major studio (this could also be
#  done with budget minimum or gross income minimum [though this would
#  require an inflation adjusted figure])

movie_df = pd.read_csv('/Users/size/DSI/repos/Capstone1/data/movies.csv')
m1 = movie_df['usa_gross_income'].notna()
m2 = movie_df['budget'].notna()
m_df = movie_df[m1 & m2].copy()

# renaming a few columns for ease of use
m_df.rename(columns = {'worlwide_gross_income': 'ww_gross', 
                        'usa_gross_income': 'usa_gross',
                        'date_published': 'release_date',
                        'reviews_from_users': 'user_reviews',
                        'reviews_from_critics': 'critics_reviews'}, inplace = True)

# Converting some strings to ints and datetimes
m_df['budget'] = m_df['budget'].apply(mf.get_dollars)
m_df['usa_gross'] = m_df['usa_gross'].apply(mf.get_dollars)
m_df['ww_gross'] = m_df['ww_gross'].apply(mf.get_dollars)
m_df['release_date'] = pd.to_datetime(m_df['release_date'])

# Break out genre into three columns

if __name__ == '__main__':
    pass