# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:20:57 2019

@author: user
"""

import pandas as pd

#read data from github
url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/KLSE_news.csv'
news = pd.read_csv(url, sep=',')

#extract date
news['extracted_date'] = news.date.str.extract(r'(\d{2}\s[A-Z][a-z]{2},\s\d{4})')

#extract code
news['extracted_code'] = news['code'].str[-4:]
news = news.sort_values('extracted_code',ascending = True).drop_duplicates(['news'], keep = 'first')

#remove news that before 25 Feb 2019
news['extracted_date'] = pd.to_datetime(news['extracted_date'])
res = news[~(news['extracted_date']<'25 Feb, 2019')]

#drop unwanted variables
res = res.drop('code', axis = 1)
res = res.drop('date', axis = 1)

#rearrange variables
col = ['extracted_code', 'extracted_date', 'news']
res = res[col]

res.to_csv("news_clean.csv", index = False, encoding = 'utf-8-sig')
