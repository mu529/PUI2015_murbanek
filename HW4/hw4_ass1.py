# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:41:20 2015

@author: MU03179
"""

import pandas as pd
import numpy as np
import pylab as pl
import scipy.stats

bikedata=pd.read_csv('C:/Users/mu03179/Desktop/NYU/PUI_project/201509-citibike-tripdata.csv')
print bikedata.columns

bikedata['ageM'] = 2015-bikedata['birth year'][(bikedata['usertype'] == 'Subscriber') & (bikedata['gender'] == 1)]
bikedata['ageF'] = 2015-bikedata['birth year'][(bikedata['usertype'] == 'Subscriber') & (bikedata['gender'] == 2)]

bins = np.arange(15, 80, 2)
bikedata.ageM.groupby(pd.cut(bikedata.ageM, bins)).agg([np.count_nonzero]).plot(kind='bar', title='Age distribution of Male trips')
bikedata.ageF.groupby(pd.cut(bikedata.ageF, bins)).agg([np.count_nonzero]).plot(kind='bar', title='Age distribution of Female trips')

"""
from FBB's lab code

csM=bikedata.ageM.groupby(bikedata.cut(df.ageM, bins)).agg([np.count_nonzero]).cumsum()
csF=bikedata.ageF.groupby(pd.cut(bikedata.ageF, bins)).agg([np.count_nonzero]).cumsum()

print np.abs(csM / csM.max()-csF / csF.max())

pl.plot(bins[:-1] + 5, csM / csM.max(), label = "M")
pl.plot(bins[:-1] + 5, csF / csF.max(), label = "F")
pl.legend()
"""

ks=scipy.stats.ks_2samp(bikedata.ageM, bikedata.ageF)
if ks[0] <= 1.36:
    print 'KS statistic of ' + str(ks[0]) + ' is below 1.36; We cannot reject H0'
else:
    print 'KS statistic of ' + str(ks[0]) + ' is above 1.36; We cannot reject H0' 

"""
If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions of the two samples are the same.
-- SciPy documentation
"""


# Since Pearsons correlation test must be on same-length arrays, my best guess
# is to create bins for each age bracket and correlate the size of the bins
binsM = bikedata.ageM.groupby(pd.cut(bikedata.ageM, bins)).agg([np.count_nonzero])
binsF = bikedata.ageF.groupby(pd.cut(bikedata.ageF, bins)).agg([np.count_nonzero])
print 'Correlation coefficient of ' + str(scipy.stats.pearsonr(binsM,binsF)[0])
print 'P value of ' + str(scipy.stats.pearsonr(binsM,binsF)[1])

# begin second part of problem - compare day and night ages
# defining night as trips beginng between 20:00 and 06:59

bikedata.starthour = bikedata.starttime.str[-8:-6].astype(int)
bikedata['ageD'] = 2015-bikedata['birth year'][(bikedata.starthour <= 19) & (bikedata.starthour >= 7)]
bikedata['ageN'] = 2015-bikedata['birth year'][(bikedata.starthour <= 6)]
bikedata['ageN'] = 2015-bikedata['birth year'][(bikedata.starthour >= 20)]

bikedata.ageD.groupby(pd.cut(bikedata.ageD, bins)).agg([np.count_nonzero]).plot(kind='bar', title='Age distribution of day trips')
bikedata.ageN.groupby(pd.cut(bikedata.ageN, bins)).agg([np.count_nonzero]).plot(kind='bar', title='Age distribution of night trips')

csD=bikedata.ageD.groupby(pd.cut(bikedata.ageD, bins)).agg([np.count_nonzero]).cumsum()

csN=bikedata.ageN.groupby(pd.cut(bikedata.ageN, bins)).agg([np.count_nonzero]).cumsum()

print np.abs(csD / csD.max()-csN / csN.max())

pl.plot(bins[:-1] + 5, csD / csD.max(), label = "Day")
pl.plot(bins[:-1] + 5, csN / csN.max(), label = "Night")
pl.legend()
pl.title('Compare CDF of night versus day ages')

ks=scipy.stats.ks_2samp(bikedata.ageD, bikedata.ageN)

if ks[0] <= 1.36:
    print 'KS statistic of ' + str(ks[0]) + ' is below 1.36; We cannot reject H0'
else:
    print 'KS statistic of ' + str(ks[0]) + ' is above 1.36; We cannot reject H0' 

binsD = bikedata.ageD.groupby(pd.cut(bikedata.ageD, bins)).agg([np.count_nonzero])
binsN = bikedata.ageN.groupby(pd.cut(bikedata.ageN, bins)).agg([np.count_nonzero])
print 'Correlation coefficient of ' + str(scipy.stats.pearsonr(binsD,binsN)[0])
print 'P value of ' + str(scipy.stats.pearsonr(binsD,binsN)[1])