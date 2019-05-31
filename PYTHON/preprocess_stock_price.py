# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:53:08 2019

@author: user
"""

import pandas as pd

#read data from github
url_stock = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/45_days_price.csv'
url_sector = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/45_days_sector.csv'
stock = pd.read_csv(url_stock, sep=',')
sector = pd.read_csv(url_sector, sep=',')

# merge price and sector
stock = pd.merge(stock, sector.drop(['code'],axis=1), on = 'name', how = 'left')

#drop unwanted variables
stock = stock.drop(['time', 'buy/volume', 'sell/volume'], axis = 1)

#rearrange variable
col = ['name', 'code', 'Sector_main', 'sector', 'date', 'open','high','low', 'price', 'volume']
stock = stock[col]

#save data to a specific directory
stock.to_csv('price_complete.csv', index = False, sep = ',')

# just check how many missing value each variable, using 'x' indicate missing
df1 = stock
df1 = df1.replace('-','x')
df1 = df1.fillna('x')
(df1 == 'x').astype(int).sum(axis=0)