'''
Mode = the value in which the frequecy is highest
'the most common value'

Median = the value in the middle of the distribution
'''
from __future__ import division
import numpy as np
from collections import Counter

# what is the mode
x = [2, 5, 5, 9, 8, 3]

# using a Counter:
c = Counter(x)
c.most_common(1)  # returns a (list of) set (item, num times occured)

c.most_common(1)[0][0]  # first item in the first item is 5

# mean
Nur = [58350, 63120, 44640, 56380, 72250]
sum(x)/len(x)

Geo = [48670, 57320, 38150, 41290, 53160, 500000]
sum(Geo)/len(Geo)
