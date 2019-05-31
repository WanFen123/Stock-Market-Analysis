# -*- coding: utf-8 -*-
"""
Created on Fri May 31 21:09:53 2019

@author: user
"""

import pandas as pd

#load data from github
url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/PDF.csv'
df = pd.read_csv(url, sep=',')

#convert company name to uppercase
df['company'] = df['company'].str.upper()

#remove whitespace at the beginning of string
df.company = df.company.str.lstrip()

#sort the company name in alphabetical order
df = df.sort_values(by=['company'], ascending = [True])

#new column name for dataset df
col = ['company', 'code','ta', 'tl', 'te', 'net_o', 'net_i', 'net_f']
df.columns = col

#create a new column 'debt_ratio' and a new column 'debt-equity_ratio'
df['debt_ratio'] = df['tl'] / df['ta']
df['debt-equity_ratio'] = df['tl'] / df['te']

#condition to categorize a company stock is low risk, medium risk or high risk
debt_condition1 = []
for each in df['debt_ratio']:
    if each > 1:
        debt_condition1.append('high')
    else:
        debt_condition1.append('low')

debt_condition2 = []
for i in df['debt-equity_ratio']:
    if i > 1:
        debt_condition2.append('high')
    else:
        debt_condition2.append('low')

#add two lists to the dataframe
df['debt_ratio_cond'] = debt_condition1
df['debt_equity_ratio_cond'] = debt_condition2

#set overall financial condition to each company
df.loc[(df.debt_ratio_cond == 'low') & (df.debt_equity_ratio_cond == 'low'), 'risk'] = 'low'
df.loc[(df.debt_ratio_cond == 'low') & (df.debt_equity_ratio_cond == 'high'), 'risk'] = 'medium'
df.loc[(df.debt_ratio_cond == 'high') & (df.debt_equity_ratio_cond == 'low'), 'risk'] = 'medium'
df.loc[(df.debt_ratio_cond == 'high') & (df.debt_equity_ratio_cond == 'high'), 'risk'] = 'high'

#visualize
df['risk'].value_counts().plot(kind='bar')

#save data
df.to_csv('PDF_risk.csv', index=False)
