# -*- coding: utf-8 -*-
"""
Created on Fri May 31 21:45:31 2019

@author: user
"""

import pandas as pd
import talib as ta
import numpy as np

#load data from github
url1 = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/all_combine_stock_news.csv'
stock = pd.read_csv(url1, sep=',')

#stock.columns
col = ['Date', 'name', 'code', 'Sector_main', 'sector', 'open', 'high', 'low', 'price', 'volume', 'polarity', 'sentiment']
stock = stock[col]
stock = stock.replace('-', stock.replace(['-'], [None]))
stock.fillna(value = pd.np.nan, inplace = True)
stock['name'] = stock['name'].str.lstrip()
stock['high'] = stock['high'].astype(float)
stock['low'] = stock['low'].astype(float)
stock['volume'] = stock['volume'].astype(float)
stock = stock[stock['price'].notnull()]

#fill in value for nan in open, high, low variables
stock['open'] = stock['open'].fillna(stock['price']*0.995)
stock['high'] = stock['high'].fillna(stock['price']*1.005)
stock['low'] = stock['low'].fillna(stock['price']*0.99)
stock['polarity'] = stock['polarity'].fillna(0)
stock['sentiment'] = stock['sentiment'].fillna('neutral')

#groupby stock
namelist = []
stock_name = stock.groupby('name')
for name, group in stock_name:
    namelist.append(group)

#technical indicators
for each in namelist:
    try:
     each['EMA10'] = ta.EMA(each['price'].values, timeperiod=10)
     each['ATR'] = ta.ATR(each['high'].values, each['low'].values, each['price'].values, timeperiod=14)
     each['ADX'] = ta.ADX(each['high'].values, each['low'].values, each['price'].values, timeperiod=14)
     each['RSI'] = ta.RSI(each['price'].values, timeperiod=14)
     macd, macdsignal, macdhist = ta.MACD(each['price'].values, fastperiod=12, slowperiod=26, signalperiod=9)
     each['MACD'] = macd
     each['MACDsignal'] = macdsignal
     each['ClgtEMA10'] = np.where(each['price'] > each['EMA10'], 1, -1)
     each['MACDSIGgtMACD'] = np.where(each['MACDsignal'] > each['MACD'], 1, -1)
     each['Return'] = each['price'].pct_change(1).shift(-1)
     #set target variable
     each['target'] = np.where(each['Return'] > 0, 1, 0)
    except:
        pass

#join all dataframes together
result = pd.concat(namelist, axis = 0)
col1 = ['Date', 'name', 'code', 'price', 'volume', 'polarity', 'EMA10', 'ADX', 'ATR', 'MACD','MACDsignal','ClgtEMA10', 'MACDSIGgtMACD', 'RSI', 'target']
result = result[col1]

#load data from github
url2 = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/full_financial_statistics.csv'
pdf_klse = pd.read_csv(url2, sep=',')

#rearrange data
col = ['code', 'Sector_main','sector','EPS','P/E','DY','DPS', 'Market_Cap (M)','debt_ratio','debt-equity_ratio','risk']
pdf_klse_selected = pdf_klse[col]
pdf_klse_selected['Sector_main'] = pdf_klse_selected['Sector_main'].str.lstrip()

#merge two dataset together
full = pd.merge(result, pdf_klse_selected, on=['code'])

#full.columns
col2 = ['Date','name','code','Sector_main','sector','price','volume','EMA10','ADX','ATR','MACD','MACDsignal','ClgtEMA10','MACDSIGgtMACD','RSI','EPS','P/E','DY','DPS','Market_Cap (M)','debt_ratio','debt-equity_ratio','polarity','risk','target']
full = full[col2]
full = full.dropna()
full.to_csv('Final_Dataset.csv', sep=',', index=False)

#in case you want to select stock from main market only
main_market = full.loc[full['Sector_main'] == 'Main Market']
sector = main_market.groupby('sector')
sectorlist = []
for name, group in sector:
    sectorlist.append(group)
    
    for n in sectorlist:
        dataframe = pd.DataFrame(n)
        name = dataframe['sector'].iloc[0]
        filename = name + '.csv'
        dataframe.to_csv(filename)
