""""
First day in WestWellLab
author: Baoting Zhang
date:   2018-07-17
feature:  all test functions set
"""
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s