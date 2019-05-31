# -*- coding: utf-8 -*-
"""
Created on Fri May 31 21:21:16 2019

@author: user
"""

import pandas as pd
from textblob import TextBlob
from snownlp import SnowNLP

url = 'https://raw.githubusercontent.com/WanFen123/Stock-Market-Analysis/master/DATA/processed_news.csv'
data = pd.read_csv(url, sep=',')

#function to detect chinese news headlines
def is_chinese(word):
    for ch in word:
        if (ch >= '\u4e00' and ch <= '\u9fff'):
            return True
    return False

#apply function
valuelist = []
for i in data['news']:
    valuelist.append(is_chinese(i))
data['is chinese?'] = valuelist

#visualize the number of chinese news headlines and english news headlines
#in total there are 2920 english news headlines and 1722 chinese news headlines
data['is chinese?'].value_counts()
data['is chinese?'].value_counts().plot(kind='bar')

#create a new dataframe for english news headlines
en_news = data.loc[data['is chinese?'] == False]

#calculate polarity for each english news headlines
polaritylist = []
for j in en_news['news']:
    polaritylist.append(TextBlob(j).sentiment[0])
en_news['polarity'] = polaritylist    

def f(row):
    if row['polarity'] > 0:
        senti = 'positive'
    elif row['polarity'] < 0:
        senti = 'negative'
    else:
        senti = 'neutral'
    return senti

en_news['sentiment'] = en_news.apply(f, axis = 1)

#visualize number of positive, negative and neutral news headlines
#in total, there are 1849 neutral, 718 positive and 353 negative news headlines
en_news['sentiment'].value_counts()
en_news['sentiment'].value_counts().plot(kind='bar')

#create a new dataframe for chinese news headlines
ch_news = data.loc[data['is chinese?'] == True]

#calculate polarity for each chinese news headlines
polaritylist1 = []
for l in ch_news['news']:
    polaritylist1.append(SnowNLP(l).sentiments)
ch_news['polarity'] = polaritylist1

def g(row):
    if row['polarity'] > 0.5:
        senti = 'positive'
    elif row['polarity'] < 0.5:
        senti = 'negative'
    else:
        senti = 'neutral'
    return senti

ch_news['sentiment'] = ch_news.apply(g, axis = 1)

#visualize number of positive, negative and neutral chinese news headlines
#in total, there are 1015 positive and 707 negative chinese news headlines
ch_news['sentiment'].value_counts()
ch_news['sentiment'].value_counts().plot(kind='bar')

#combine chinese and english news headlines
news = ch_news.append(en_news)

#aggregate the polarity of news for each day for each stock
news_clean= news.groupby(['extracted_code','extracted_date']).mean()

#organize the dataframe
news_clean.reset_index(inplace=True)
news_clean = news_clean.drop(['is chinese?'], axis=1)
news_clean['sentiment'] = news_clean.apply(f, axis = 1)
news_clean['sentiment'].value_counts()
news_clean['sentiment'].value_counts().plot(kind='bar')

#save data
news_clean.to_csv('news.csv')