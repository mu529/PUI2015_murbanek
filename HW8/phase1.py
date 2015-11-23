# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 22:48:04 2015

@author: murbanek
"""
import geopandas as gp
import pandas as pd
import numpy as np
import os
import json
import pylab as pl
s = json.load( open(os.getenv('PUI2015')+'/fbb_matplotlibrc.json') )
pl.rcParams.update(s)
#%pylab inline

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

plutom = gp.GeoDataFrame.from_file(os.getenv('PUI2015')+'/data/mn_mappluto_15v1/Manhattan/MNMapPLUTO.shp')
plutom = plutom[['BoroCode','BldgArea','ResArea','UnitsRes','YearBuilt','YearAlter1', 'YearAlter2']]


plutob = gp.GeoDataFrame.from_file(os.getenv('PUI2015')+'/data/bk_mappluto_15v1/Brooklyn/BKMapPLUTO.shp')
plutob = plutob[['BoroCode','BldgArea','ResArea','UnitsRes','YearBuilt','YearAlter1', 'YearAlter2']]

pluto = pd.concat([plutom,plutob])

del plutob
del plutom

pluto = pluto[pluto['YearBuilt']!=0]
pluto['LatestYear'] = 0

def maxyear(y):
    return max(y['YearAlter1'],y['YearAlter2'])

def avgunit(z):
    if z['UnitsRes'] <= 0:
        return np.nan
    else:
        return np.divide(z['ResArea'],z['UnitsRes'])

pluto['LatestYear'] = pluto.apply(maxyear,axis=1)
pluto['AvgUnitSize'] = pluto.apply(avgunit,axis=1)
# need cut out nonsense
# pluto renovations as the other color!

plutorenov = pluto[pluto['LatestYear']!=0]
plutobuilt = pluto[pluto['YearBuilt']!=0]


# print(pluto[pluto['LatestYear']>1995]['AvgUnitSize'].median())

import matplotlib.pyplot as plt
# %matplotlib inline

fig = plt.figure(figsize = (10,8))
ax1 = fig.add_subplot(111)
ax1.scatter(np.unique(plutobuilt['YearBuilt']), plutobuilt.groupby('YearBuilt')['AvgUnitSize'].mean(), c='b', label='New Buildings')
ax1.scatter(np.unique(plutorenov['LatestYear']), plutorenov.groupby('LatestYear')['AvgUnitSize'].mean(), c='r', label='Renovations')
plt.legend(loc='upper left', fontsize=18);
plt.xlim(1880, 2020)
plt.ylim(0, 3500)
plt.xlabel('Year', fontsize = 16)
plt.ylabel('Avg Sq Ft', fontsize = 16)
plt.title('Average Residential Unit Size\n Original versus Renovations, Manhattan + Brooklyn', fontsize = 24)
plt.savefig('foo.png')