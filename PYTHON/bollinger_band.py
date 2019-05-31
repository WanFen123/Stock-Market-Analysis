# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:16:05 2019

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#load data from github
url= 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/price_complete.csv'
stock = pd.read_csv(url, sep=',')

#sort data by date
stock['date'] = pd.to_datetime(stock['date'])
stock['Date'] = stock['date'].dt.date
stock = stock.drop(['date'], axis = 1)
stock = stock.sort_values(by='Date')
stock['name'] = stock['name'].str.lstrip()

#pivot table
len(stock['name'].unique())    #check how many distinct stock
stock_pivot = pd.pivot_table(stock, index = 'Date', columns = 'name', values = 'price')

#Bollinger Band function
def Bollinger_Bands(stock_price, window_size, num_std_dev):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_std_dev)
    lower_band = rolling_mean - (rolling_std*num_std_dev)
    return rolling_mean.tolist(), rolling_std.tolist(), upper_band.tolist(), lower_band.tolist()

#select a company to check its volatility
date = stock_pivot.index.values.tolist()
col = stock_pivot.columns.tolist()

#initiate a pdf file to store all the graphs
pdf = PdfPages('bollinger_bands.pdf')
#plot the graph
for company in col:
    try:
        df = pd.DataFrame({'Date':date})  
        df['rolling_mean'], df['rolling_std'], df['upper_band'], df['lower_band'] = Bollinger_Bands(stock_pivot[company], window_size = 10, num_std_dev = 2)
        df = df.set_index('Date')
        df= df.dropna(axis = 0)
        title = company
        #visualize the bollinger band
        fig = plt.figure(figsize=(8,6))
        ax1 = fig.add_subplot(111, xlabel='Date', ylabel='Close')

        df['rolling_mean'].plot(ax = ax1, color= 'purple', lw = 1, label = 'middle band')
        df['upper_band'].plot(ax = ax1, color = 'g', lw = 1, label = 'upper band')
        df['lower_band'].plot(ax = ax1, color = 'r', lw = 1, label = 'lower band')

        plt.xticks(rotation=45)
        plt.title(title)
        ax1.legend()
        pdf.savefig()
    except:
        pass

#close pdf file when finish plotting the graphs
pdf.close()
