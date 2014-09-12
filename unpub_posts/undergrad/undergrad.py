
from __future__ import division
from pylab import *
from pandas import read_csv

# ``uw`` from [1] and tuition from [2]
#
# [1]:https://registrar.wisc.edu/enrollment-reports-and-student-statistics%20.htm
# [2]:http://www.uwsa.edu/budplan/tuition/tuitionHistory.pdf

uw = read_csv('uw-all.csv')
undergrads = uw['U-grad']
profs = uw['Prof']
year = uw['Fall']

undergrads = asarray(undergrads, dtype=float)
profs = asarray(profs, dtype=float)

# stripping, converting from string to int
year = asarray(year, dtype='|S4')
year = asarray(year, dtype=int)

# reading tuition
tuition = read_csv('tuiton.csv')
year_tuition = tuition['Year']
tuition = tuition['Tuition']
tuition = asarray(tuition)

# cutting to 1967
undergrads = undergrads[argwhere(year >= year_tuition.min()).flat[:]]
profs      =      profs[argwhere(year >= year_tuition.min()).flat[:]]
year_tuition = flipud(year_tuition)
tuition      = flipud(tuition)

# normalizing
undergrads /= undergrads.max()
undergrads -= 0.4
profs      /= profs.max()

fig, ax1 = subplots()
grid()
ax1.plot(year_tuition, profs, label='Professors')
ax1.plot(year_tuition, undergrads, 'g', label='Undergraduates')
legend(loc='upper left')
ax1.set_ylabel('Number of people, normalized to maximum')

ax2 = ax1.twinx()
ax2.set_ylabel('Dollars')
ax2.plot(year_tuition, tuition, 'r', label='Tuition')
legend(loc='lower right')
show()
