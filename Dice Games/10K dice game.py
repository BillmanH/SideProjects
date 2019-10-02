from __future__ import division
import numpy as np
from collections import Counter


def roll_all_dice(dice, dice_sides=6):
    '''dice is an array of ints from 1-6'''
    for die in range(len(dice)):
        dice[die] = np.random.randint(1, dice_sides)
    return dice


def find_groups(dice):
    '''Prints combos'''
    diceCounter = Counter(dice)
    if max(diceCounter.values()) < 3:
        print "no combos"
    elif diceCounter.values().count(5):
        print "five: " + str(diceCounter[0])
    elif diceCounter.values().count(4):
        print "four: " + str(diceCounter[0])
    elif diceCounter.values().count(3) == 1:
        print "three: " + str(diceCounter.keys()[0])
    elif diceCounter.values().count(3) == 2:
        print "three: " + str(diceCounter.items()[0])
        print "three: " + str(diceCounter.items()[1])


def find_threePair():
    [val == 2 for val in diceCounter.values()]


find_groups(roll_all_dice(dice))
