# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:36:59 2019

@author: user
"""

import pandas as pd
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

#load data from github
url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/price_complete.csv'
stock = pd.read_csv(url, sep=',')

#preprocessing for the usage of plotting candlestick charts
stock['date'] = pd.to_datetime(stock['date'])
stock = stock.sort_values(by='date')
col = ['name','date','open','high','low','price']
stock = stock[col]
stock = stock.replace('-', stock.replace(['-'], [None]))
stock.fillna(value = pd.np.nan, inplace = True)
stock['name'] = stock['name'].str.lstrip()
stock['open'] = stock['open'].astype(float)
stock['high'] = stock['high'].astype(float)
stock['low'] = stock['low'].astype(float)

#group stock by name
stock_byname = stock.groupby('name')
namelist = []
for name, group in stock_byname:
    namelist.append(group)

#open a pdf file to store each candlestick chart
pdf = PdfPages('candlestick_charts.pdf')

#plot candlestick chart for each stock
for each in namelist:
    try:
        each['date'] = [mdates.date2num(d) for d in each['date']]
        quotes = [tuple(x) for x in each[['date', 'open', 'high', 'low', 'price']].values]
        title = each['name'].iloc[0]
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, quotes, width=0.5, colorup='g', colordown='r')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(title)
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        plt.autoscale(tight=True)
        pdf.savefig()
    except:
        pass

#close pdf file
pdf.close()
