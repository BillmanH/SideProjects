''' model evaluation and validation '''

# people with social networking account
# what is the range:
set1 = [21180, 78600]

set1[1] - set1[0]

set2 = [7350, 116020]

set2[1] - set2[0]

# add mark Zukerberg to set1
set1 = [21180, 10000000]

set1[1] - set1[0]

# cuto off the lower and upper tails of the data:
sample = [38946,
          43420,
          49191,
          50557,
          52580,
          53595,
          54135,
          60181,
          10000000]

median = int(np.median(sample))
sample[:sample.index(median)]

# find the midrange (Q3-Q1)
# or Inter Quartile Range:
median = np.percentile(sample, 50)
Q1 = np.percentile(sample, 25)
Q3 = np.percentile(sample, 75)

IQR = Q3 - Q1

# get the interquatrile range


def is_outlier(x):
    if (x < Q1 - (1.5*IQR)) or (x > Q3 + (1.5*IQR)):
        return True
    else:
        return False


for x in [60000, 80000, 100000, 200000]:
    print is_outlier(x)

sample = [33219,
          36254,
          38801,
          46335,
          46840,
          47596,
          55130,
          56863,
          78070,
          88830]

mean = np.mean(sample)

deviation = [round(x-mean, 4) for x in sample]
np.mean(deviation)
print format(np.mean(deviation), 'f')

abs_deviation = [abs(round(x-mean, 4)) for x in sample]
print format(np.mean(abs_deviation), 'f')

sqrd_deviation = [round(x-mean, 4)**2 for x in sample]
print format(np.mean(sqrd_deviation), 'f')
math.np.mean(sqrd_deviation)

sample = [38946,
          43420,
          49191,
          50430,
          50557,
          52580,
          53595,
          54135,
          60181,
          62076]
sqrd_deviation = [(x-mean)**2 for x in sample]
avrg = sum([(x-mean)**2 for x in sample])/len(sample)
math.sqrt(np.mean(avrg))
# this version didn't work. I wonder why?

# correct answer:
np.std(sample)


# final quiz
sample = [59147.29,
          61379.14,
          55683.19,
          56272.76,
          52055.88,
          47696.74,
          60577.53,
          49793.44,
          35562.29,
          58586.76,
          47091.37,
          36906.96,
          53479.66,
          67834.74,
          53018.8,
          60375.11,
          36566.91,
          52905.58,
          51063.31,
          65431.26,
          57071.83,
          30060.59,
          42619.62,
          52984.77,
          57871.28,
          41274.37,
          24497.78,
          47939.82,
          42755.52,
          57189.35,
          37216.45,
          44742.99,
          47119.04,
          59269.48,
          53336.8,
          39719.54,
          69473.2,
          39831.55,
          58300.7,
          41726.66,
          40283.35,
          59652.4,
          40326.61,
          28167.31,
          51420.36,
          55294.22,
          48116.14,
          36780.47,
          53628.89,
          48782.09,
          33615.77,
          41881.34,
          64745.33,
          53482.58,
          48838.54,
          57031.73,
          62821.03,
          60627.78,
          46568.52,
          38977.05,
          43250.62,
          67502.5,
          54696.18,
          43003.14,
          29156.83,
          61230.07,
          56749.93,
          48373.77,
          52428.26,
          29961.91,
          54524.28,
          83017.28,
          49290.55,
          56375.66,
          64032.27,
          52947.6,
          61210.22,
          54438.94,
          48825.68,
          54118.71,
          45305.73,
          42361.59,
          52852.52,
          62933.52,
          64330.23,
          48922.74,
          27211.96,
          62409.65,
          28981.92,
          64913.67,
          55766,
          50748.04,
          43990.34,
          61828.33,
          45434.02,
          45369.16,
          54710.71,
          62222.43,
          44764.32,
          50973.48]

np.std(sample)

sample = [18, 20, 23, 22, 21, 17, 18, 21, 15]
