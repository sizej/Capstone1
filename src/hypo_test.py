from statsmodels.stats.weightstats import ztest 
import numpy as np 


class HypoZtest(object):
    '''
    A class that will perform and house the results of a z-test
    '''

    def __init__(self, arr1, arr2, alpha = 0.05, val = 0, alt = 'two-sided'):
        self.x1 = arr1
        self.x2 = arr2
        self.alpha = alpha
        self.val = val
        self.alt = alt
        self.run_test()
        
    def run_test(self):
        self.z_score, self.test_statistic = ztest(self.x1, self.x2, self.val, self.alt)
        if self.test_statistic <= self.alpha:
            self.result = 'reject H0'
        else:
            self.result = 'cannot reject H0'
