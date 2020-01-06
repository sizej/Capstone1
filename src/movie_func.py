import pandas as pd 
import numpy as np 

def get_dollars(s):
    '''
    Function to strip out dollar signs/other currency signs and conver
    to int
    '''
    if s[0] == '$':
        return int(s[s.find(' ') + 1:])
    else:
        return 'Not US'

inflation_df = pd.read_csv('/Users/size/DSI/repos/Capstone1/data/CPIAUCNS.csv')
inflation_df['DATE'] = pd.to_datetime(inflation_df['DATE'])
inflation_df['CPI_mult'] = inflation_df['CPIAUCNS'].iloc[-1] / inflation_df['CPIAUCNS']
end_date = max(inflation_df['DATE'])

def inflation_adjustment(amt, date, end = end_date):
    #breakpoint()
    if date < end:
        idx = min(np.where(inflation_df['DATE'] >= date)[0])
        adj = inflation_df['CPI_mult'][idx]
        return (idx, amt * adj)
    else:
        return (0,amt)
        
if __name__ == '__main__':
    pass