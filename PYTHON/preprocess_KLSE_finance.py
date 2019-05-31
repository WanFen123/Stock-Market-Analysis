# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:14:46 2019

@author: user
"""

import pandas as pd
import re
import numpy as np

url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/KLSE_finance.csv'
appended_data = pd.read_csv(url, sep=',')

#to extract code from 'name' variable
codeList = []
for each in appended_data['name']:
    code1 = re.findall(r"\(([0-9]+)\)", each)
    codeList.append(code1)

code = pd.DataFrame({'code': codeList})
code.code = code.code.apply(lambda y: np.nan if len(y)==0 else y)

codeList1 = []
for j in codeList:
    if j == []:
        j = ['nan']
    else:
        j = j
    codeList1.append(j)
flat_list = [item for sublist in codeList1 for item in sublist]

#add variable 'code' to dataframe
appended_data['code'] = flat_list
#remove variable 'name' from dataframe
appended_data = appended_data.drop('name', axis = 1)

#separate category into variable sector_main and sector
new = appended_data['category'].str.split('-', n = 1, expand = True)
appended_data['Sector_main'] = new[1]
appended_data['sector'] = new[0]
#remove variable 'category' from dataframe
appended_data = appended_data.drop('category', axis = 1)


#separate 52w into 52w_high and 52w_low
week52 = appended_data['52w'].str.split('-', n=1, expand = True)
appended_data['52w_low'] = week52[0]
appended_data['52w_high'] = week52[1]
appended_data = appended_data.drop('52w', axis = 1)


#remove 'M' from Market_Cap variable and change the variable name
appended_data['Market_Cap'] = appended_data['Market_Cap'].map(lambda x: x.rstrip('M')) 
appended_data.rename(columns={'Market_Cap' : 'Market_Cap (M)'}, inplace = True)

#separate RSI into RSI_status and RSI_value
RSI = appended_data['RSI'].str.split(' ', n = 1, expand = True)
appended_data['RSI_status'] = RSI[0]
appended_data['RSI_value'] = RSI[1]
appended_data = appended_data.drop('RSI', axis = 1)

#separate stochastic into stochastic_status and stochastic_value
stochastic = appended_data['Stochastic'].str.split(' ', n = 1, expand = True)
appended_data['Stochastic_status'] = stochastic[0]
appended_data['Stochastic_value'] = stochastic[1]
appended_data = appended_data.drop('Stochastic', axis = 1)

#rearrange columns
#print(appended_data.columns.values)
cols =['full name', 'code', 'Sector_main', 'sector', '52w_low', '52w_high', 'ROE', 'P/E', 'EPS', 'DPS', 'DY', 'PTBV', 'RPS', 'PSR', 'Market_Cap (M)', 'RSI_status', 'RSI_value', 'Stochastic_status', 'Stochastic_value']
appended_data = appended_data[cols]

#write to csv
appended_data.to_csv('KLSE_clean.csv', index = False)