# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:22:41 2019

@author: user
"""

# import package
from selenium import webdriver

browser = webdriver.Chrome() # open web page
browser.implicitly_wait(10) # wait for web page to load

company_names = [] # save company names in a list
# crawl all company names from A-Z
for i in range(65,91):
    url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet='+chr(i)
    browser.get(url)
    
    name_list = browser.find_elements_by_xpath('//table[@class="market-trans"]//tr[@class="linedlist"]/td/a')
    for name in name_list:
        if name.text!='':
            name_text = name.text.replace("&","%26") 
            company_names.append(name_text)

# crawl all company names in 0-9
url1 = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet=0-9'
browser.get(url1)
name1_list = browser.find_elements_by_xpath('//table[@class="market-trans"]//tr[@class="linedlist"]/td/a')
for name1 in name1_list:
    if name1.text!='':
        name1_text = name1.text.replace("&","%26") 
        company_names.append(name1_text)

#print(company_names)
browser.close()

# save as links for crawling all the information
company_links = []
for n in company_names:
    link = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=' + n
    company_links.append(link)
#print(company_links)

# import packages
from lxml import html
import requests

class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]
        date = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        time = tree.xpath('//span[@id="slcontent_0_ileft_0_timetxt"]/text()')[0]
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        low = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        high = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        vol = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buy_vol = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sell_vol = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]

        name_list.append(name)
        #print(name)
        code_list.append(code[3:])
        #print(code[3:])
        price_list.append(price)
        #print(price)
        date_list.append(date[10:21])
        #print(date[10:21])
        time_list.append(time)
        #print(time)
        open_price_list.append(open_price)
        #print(open_price)
        low_list.append(low)
        #print(low)
        high_list.append(high)
        #print(high)
        vol_list.append(vol)
        #print(vol)
        buy_vol_list.append(buy_vol)
        #print(buy_vol)
        sell_vol_list.append(sell_vol)
        #print(sell_vol)
        
        return

# create list for all the variables
name_list = []
code_list = []
price_list = []
date_list = []
time_list = []
open_price_list = []
low_list = []
high_list = []
vol_list = []
buy_vol_list = []
sell_vol_list = []
  
for l in company_links:
    crawler = AppCrawler(l, 0)
    crawler.crawl()

import pandas as pd

na = name_list
co = code_list
da = date_list
ti = time_list
op = open_price_list
lo = low_list
hi = high_list
pr = price_list
vo = vol_list
bv = buy_vol_list
sv = sell_vol_list

dataframe = pd.DataFrame({'name':na,'code':co,'date':da,'time':ti,'open':op,'low':lo,'high':hi,'price':pr,'volume':vo,'buy/volume':bv,'sell/volume':sv})

# save data
# set directory by yourself
dataframe.to_csv("Price_Day1.csv", index=False, sep=',')
