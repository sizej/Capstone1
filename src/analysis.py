


dec = m_df2.groupby('release_decade').agg({'title': 'count',
                                    'is_success': 'sum'})
dec['success_rate'] = dec['is_success'] / dec['title']





if __name__ == '__main__':
    pass