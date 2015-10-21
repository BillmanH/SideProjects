from __future__ import division
from fractions import Fraction

import numpy as np

#I assign a variable for each dice
d1 = range(1,7)
d2 = range(1,7) #this creates a six sided die.

#then a model is created for stats
all_rolls = [[[a,b] for a in d1] for b in d2]

#probability of rolling a combination
outcome = 6

#create a binary list for each value
success_rolls = [[1 for x in row if sum(x)==outcome] for row in all_rolls]

total_meet_criteria = sum([sum(row) for row in success_rolls])
total_possibilities = sum([len(row) for row in all_rolls])

#answer for single guess:
probability_of_outcome = total_meet_criteria/total_possibilities
Fraction(probability_of_outcome).limit_denominator()


#answer for list of possible outcomes
outcomes = range(6,0,-1)

[for outcome in outcomes]
