# -*- coding: utf-8 -*-
"""
Created on Mon May 11 18:26:02 2015

@author: Paco
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels as sm
import pylab as pl
import seaborn as sns

'''
VOLAT.DES
  1. date                     1947.01 to 1993.06
  2. sp500                    S&P 500 index
  3. divyld                   dividend yield, annualized rate
  4. i3                       3 mo. T-bill annualized rate
  5. ip                       index of industrial production
  6. pcsp                     pct chg, sp500, ann rate
  7. rsp500                   return on sp500: pcsp + divyld
  8. pcip                     pct chg, IP, ann. rate
  9. ci3                      i3 - i3[t-1]
 10. ci3_1                    ci3[t-1]
 11. ci3_2                    ci3[t-2]
 12. pcip_1                   pcip[t-1]
 13. pcip_2                   pcip[t-2]
 14. pcip_3                   pcip[t-3]
 15. pcsp_1                   pcip[t-1]
 16. pcsp_2                   pcip[t-2]
 17. pcsp_3                   pcip[t-3]
''' 
##################
#Q21
##################
columns = ['date',
'sp500',                    
'divyld',                   
'i3',                       
'ip',                       
'pcsp',                     
'rsp500',                   
'pcip',                     
'ci3',                      
'ci3_1',                    
'ci3_2',                   
'pcip_1',                   
'pcip_2',                   
'pcip_3',                   
'pcsp_1',                   
'pcsp_2',                   
'pcsp_3']

data_df = pd.read_fwf('data/VOLAT.raw',names=columns)
data_df = data_df.copy().replace('.',0)
data_df = data_df.copy().astype(float)

#timeseries
pl.figure()
pl.plot(data_df.iloc[:,0],data_df.iloc[:,5])
pl.show()

##################
#Q23
##################
# Une distribution constante a travers le temps doit etre
# conservée pour pouvoir faire l'etude d'une serie temporelle
# stationnaire.

##################
#Q23
##################
#Test de racine unitaire
# On estime la regression par les moindres carrés 
# puis on teste l'hypothèse H0 : p=0 avec un test de student
dlog=np.log(data_df.ix[:,5]-np.min(data_df.ix[:,5])+1) - np.log(data_df.ix[:,14]-np.min(data_df.ix[:,14])+1)
res=sm.api.OLS(dlog,sm.api.add_constant(np.log(data_df.ix[:,14]-np.min(data_df.ix[:,14])+1))).fit()
print res.summary()

logsp500=np.log(data_df.iloc[:,5] - np.min(data_df.iloc[:,5])+1)
print sm.tsa.stattools.adfuller(logsp500)[:2]

##################
#Q24
##################
#ACF et PACF pour pcsp
fig, axes = pl.subplots(2,1)
fig.subplots_adjust(hspace=.7)
fig=sm.graphics.tsaplots.plot_acf(data_df.iloc[:,5],ax=axes[0])
axes[0].set_title("Autocorrelogramme de Pcsp")
fig=sm.graphics.tsaplots.plot_pacf(data_df.iloc[:,5], ax=axes[1])
axes[1].set_title("Autocorrelogramme partiel de Pcsp")

#ACF et PACF pour divyld
fig, axes = pl.subplots(2,1)
fig.subplots_adjust(hspace=.7)
fig=sm.graphics.tsaplots.plot_acf(data_df.iloc[:,2],ax=axes[0])
axes[0].set_title("Autocorrelogramme de Divyld")
fig=sm.graphics.tsaplots.plot_pacf(data_df.iloc[:,2], ax=axes[1])
axes[1].set_title("Autocorrelogramme partiel de Divyld")

#Les autocorrelogrammes montrent qu'il a de la 
#saisonnalité dans une des séries. De plus, La fonction 
#d'auto-correlation n'est pas nulle sur tous les termes, 
#il y a donc de l'autocorrélation

##################
#Q25
##################
for p in range(0,data_df.shape[1]-1):
    ar=sm.tsa.ar_model.AR(np.array(data_df.ix[:,p])).fit()
    print 'p: '+str(p)
    print 'AIC: '+str(ar.aic)
    print 'BIC: '+str(ar.bic)
    print 'params: '+str(ar.params)
    print ''

##################
#Q26
##################
res=sm.api.OLS(data_df.ix[:,5],data_df.ix[:,[5,8]]).fit()
print(res.summary())


