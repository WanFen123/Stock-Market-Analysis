# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 23:42:36 2019

@author: user
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# open web page
browser = webdriver.Chrome()  
browser.implicitly_wait(10)
url='https://www.klsescreener.com/v2/'
browser.get(url)
screen_button=browser.find_element_by_id('submit')
screen_button.click()

#wait until the browser load after clicking the screen button and obtain the new web source
wait=WebDriverWait(browser,10)
element=wait.until(
            EC.presence_of_element_located((By.CLASS_NAME,"table-responsive")))
html=browser.page_source
soup = BeautifulSoup(html, "html.parser")
#print(soup.prettify())

#locate the result table
stock_table=soup.find(id="result")

#create a list for codes
links = []
for a in stock_table:
    rowsodd = stock_table.find_all(attrs={'class':'list odd'})
    rowseven = stock_table.find_all(attrs={'class':'list even'})
    for item in rowsodd:
        stock_code =item.find('td',attrs={'title':'Code'}).text
        links.append(stock_code)
    for item in rowseven:
        stock_code =item.find('td',attrs={'title':'Code'}).text
        links.append(stock_code)

#remove duplicates
mylinks = list(dict.fromkeys(links))

#add the code to form news urls
company_links = []
for n in mylinks:
    link = 'https://www.klsescreener.com/v2/news/stock/' + n
    company_links.append(link)

#extract news and respective date
df=pd.DataFrame([])
for l in company_links:
    company_news = []
    company_date=[]
    code = l
    page = requests.get(l)
    soup = BeautifulSoup(page.text, 'html.parser')
    news_table=soup.find(id="section")
    for b in news_table.find_all('h2',{"class":"figcaption"}):
    #print(b.get_text())
        company_news.append(b.get_text())
        
    for c in news_table.find_all('div',{"class":"item-title-secondary subtitle"}):
        company_date.append(c.get_text())
    dataframe=pd.DataFrame({'code':code, 'date':company_date,'news':company_news})
    df=df.append(dataframe)
    
#save to csv
#set directory by yourself
df.to_csv("news_1.csv",index=False,sep=',')


























#to read chinese character in csv file
import csv

codeList = []
dateList = []
newsList = []

with open('news.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    Nrow = 0
    for row in reader:
        if Nrow >= 1:
            code.append(row[0])
            date.append(row[1])
            news.append(row[2])
        Nrow = Nrow + 1
#print(code)
#print(date)
#print(news)
              
dataframe = pd.DataFrame({'code':code, 'date':date, 'news_headline':news})
dataframe.to_csv('news_readable.csv', index = False, sep = ',', encoding = 'utf-8-sig')
