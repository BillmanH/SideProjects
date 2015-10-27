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
d1 = range(1,7)
d2 = range(1,7)
all_rolls = [[[a,b] for a in d1] for b in d2]

success_rolls = [[1 for x in row if sum(x) in outcomes] for row in all_rolls]
total_meet_criteria = sum([sum(row) for row in success_rolls])
total_possibilities = sum([len(row) for row in all_rolls])

probability_of_outcome = total_meet_criteria/total_possibilities
Fraction(probability_of_outcome).limit_denominator()

#for a given roll, what is the probability that the values of the dice add to 2
success_rolls = [[1 for x in row if sum(x)==2] for row in all_rolls]

#For a given roll, what is the probability the black die displays 2 and the white die displays 1?
success_rolls = [[1 for x in row if (x[0]==2) & (x[1]==1)] for row in all_rolls]

#For a given roll, what is the probability that the values of the dice add to 3?
success_rolls = [[1 for x in row if sum(x)==3] for row in all_rolls]

#You are given two dice to roll. One is black with six sides; the other is white with four sides.
success_rolls = [[1 for x in row if sum(x)==2] for row in all_rolls]
d2 = range(1,5)

#You are given two six-sided dice to roll.
#For a given roll, what is the probability that the values of the dice add to 8?
success_rolls = [[1 for x in row if sum(x)==8] for row in all_rolls]

#You are given two dice to roll. One is black with six sides; the other is white with four sides.
#For a given roll, what is the probability that the values of the dice add to 8 or less?
d2 = range(1,5)
outcomes = range(8,0,-1)
all_rolls = [[[a,b] for a in d1] for b in d2]
success_rolls = [[1 for x in row if sum(x) in outcomes] for row in all_rolls]

#You are given two six-sided dice to roll.
#For a given roll, what is the probability at least one die displays 1?
d2 = range(1,7)
all_rolls = [[[a,b] for a in d1] for b in d2]
success_rolls = [[1 for x in row if (x[0]==1) | (x[1]==1)] for row in all_rolls]

#You are given two dice to roll. One is black with six sides; the other is white with four sides.
#For a given roll, what is the probability that the black die displays an even number 
#and the white die displays 1?
d2 = range(1,5)
outcomes = [2,4,6]
all_rolls = [[[a,b] for a in d1] for b in d2]
success_rolls = [[1 for x in row if (x[0] in outcomes) & (x[1]==1)] for row in all_rolls]

#You are given two six-sided dice to roll.
#For a given roll, what is the probability that the dice both display 5?
success_rolls = [[1 for x in row if (x[0]==5) & (x[1]==5)] for row in all_rolls]
