# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:58:49 2019

@author: user
"""

import pandas as pd

#import dataset
url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/KLSE_clean.csv'
df = pd.read_csv(url, sep = ',')

#chose those required indicator in investigating the stock performance and risk
data = df[['full name', 'code', 'Sector_main', 'sector', 'EPS', 'P/E', 'DY', 'DPS', 'RSI_status', 'Stochastic_status', 'Market_Cap (M)']]

#investigate EPS variable
data['EPS'].describe()
EPSlist = []
#divide EPS into 3 category : good(2), normal(1), bad(0)
for i in data['EPS']:
    if i < 0:
        EPSlist.append(0)
    elif (i >= 0 and i <= 2.17):
        EPSlist.append(1)
    else:
        EPSlist.append(2)

#investigate P/E variable
data['P/E'].describe()
PElist = []
#divide P/E into 3 category : good(2), normal(1), bad(0)
for j in data['P/E']:
    if j < 0:
        PElist.append(0)
    elif (j >= 0 and j <= 10):
        PElist.append(1)
    else:
        PElist.append(2)

#investigate DY variable
data['DY'].describe()
DYlist = []
#divide DY into 2 category : attractive (1), less attractive (0)
for k in data['DY']:
    if k == 0:
        DYlist.append(0)
    else:
        DYlist.append(1)

#investigate DPS variable
data['DPS'].describe()
DPSlist = []
#divide DPS into 2 category : attractive (1), less attractive (0)
for l in data['DPS']:
    if i == 0:
        DPSlist.append(0)
    else:
        DPSlist.append(1)

#investigate Market_Cap variable
data['Market_Cap (M)'] = data['Market_Cap (M)'].astype('float64')
data['Market_Cap (M)'].describe()
MarketCaplist = []
#divide Market_Cap into 3 category : mature(2), growth (1), small (0)
for m in data['Market_Cap (M)']:
    if m < 59.7:
        MarketCaplist.append(0)
    elif (m >= 59.7 and m < 564.75):
        MarketCaplist.append(1)
    else:
        MarketCaplist.append(2)

#form a new dataset to compare company condition
cond = pd.DataFrame({'EPS':EPSlist, 'PE':PElist, 'DY':DYlist, 'DPS':DPSlist, 'MarketCap':MarketCaplist}, dtype = 'float')
cond['total'] = cond.sum(axis=1)

risklist = []
#divide into 3 category : high risk, medium risk and low risk
for each in cond['total']:
    if each >= 6:
        risklist.append('low')
    elif (each >=3 and each < 6):
        risklist.append('medium')
    else:
        risklist.append('high')
        
#append risklist back to original data
data['risk'] = risklist

#visualize
data['risk'].describe()
data['risk'].value_counts().plot(kind='bar')

#save data
data.to_csv('KLSE_risk.csv', index=False)
