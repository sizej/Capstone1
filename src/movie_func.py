def get_dollars(s):
    '''
    Function to strip out dollar signs/other currency signs and conver
    to int
    '''
    if s[0] == '$':
        return int(s[s.find(' ') + 1:])
    else:
        return 'Not US'


if __name__ == '__main__':
    pass