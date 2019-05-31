# Stock-Market-Analysis
This repository contains the steps involved in constructing a predictive model for stock prediction. <br/>
There are totally 6 milestones in this project, each milestone will be discussed in the following part.

## Data Sources
There are 4 data sources used in this project. 
1. The time series stock data is crawled from **The Star Online** website using https://www.thestar.com.my/business/marketwatch/stocks. 
2. The financial statistics and news of a company are crawled from **KLSE Screener** website using 
https://www.klsescreener.com/v2/financial-reports and https://www.klsescreener.com/v2/news respectively.
3. The financial report or annual report of a company is crawled from **malaysiastock.biz** website using https://www.malaysiastock.biz/Annual-Report.aspx 
    
## Milestone 1
Data collection is the first step to start a project. <br/>
The data used in this project is acquired by applying web crawling using Python. 
1. Use **crawler_stock_price.py** to collect the time series stock price data from The Star Online website.
2. Use **crawler_klse_finance.py** to collect the financial statistics of a company from KLSE Screener website.
3. Use **crawler_news.py** to collect the news headlines regarding a company from KLSE Screener website.
4. Use **auto_download_pdf.py** to automatically download PDF Financial Report from malaysiastock.biz website.
5. Use **pdfcrawler_bypage.py** to extract the financial statements from PDF Financial Report.

## Milestone 2
A star schema data warehouse is constructued using the 4 crawled data sources mentionned above.

## Milestone 3
Data cleaning and correlation analysis between stocks are carried out.
1. Data cleaning for stock price dataset is implemented with *45_days_price.csv* and *45_days_sector.csv* dataset using **preprocess_stock_price.py**. The *45_days_price.csv* is the compilation of 45 days stock price data crawled from The Star Online website while the *45_days_sector.csv* is the information regarding market and sector of stocks.

2. Data cleaning for KLSE financial statistics is implemented with *KLSE_finance.csv* dataset using **preprocess_KLSE_finance.py**. The *KLSE_finance.csv* is the compilation of the financial statistics released in February, March and April 2019.

3. Data cleaning for KLSE news is implemented with *KLSE_news.csv* dataset using **preprocess_KLSE_news.py**. 

4. A correlation analysis between stocks is carried out with *45_days_price.csv* dataset using **correlation_analysis.py**. The result can be obtained from *correlation_results.xlsx* excel file.

## Milestone 4
Technical analysis and fundamental analysis are carried out in this milestone. <br/>
A qualitative analysis is carried out with news headlines regarding stocks. <br/>
Lastly, the relationship between stock price and news headlines is examined by plotting graphs.

1. Technical Analysis <br/>
The *price_complete.csv* dataset is used in technical analysis to illustrate the **Bollinger Band** and **Candlestick Chart** for each stock. The Bollinger Band of each stock is plotted using **bollinger_band.py** and it is saved to a PDF file. The Candlestick Chart of each stock is plotted using **candlestick_chart.py** and it is saved to a PDF file.

2. Fundamental Analysis <br/>
The dataset used in fundemental analysis include KLSE financial statistics and malaysiastock.biz financial report. <br/>
**KLSE Financial Statistics** <br/>
The *KLSE_clean.csv* dataset is used in exploring and investigating the stock using **KLSE_exploration.py**. <br/>
**PDF Financial Report** <br/>
The *PDF.csv* dataset is used in exploring and investigating the stock using **PDF_exploration.py**. <br/>

3. Qualitative Analysis
A qualitative analysis is carried out using news headlines. The *processed_news.csv* dataset is explored using **news_exploration.py**.

## Milestone 5
Two models are implemented in Milestone 5 using SAS Enterprise Miner - Decision Tree and Logistic Regression. Before implementing, all the data sources are combined into one complete dataset. The *all_combine_stock_news.csv* and *full_financial_statistics.csv* datasets are merged together using **data_combine.py**. The final dataset is uploaded with the name *Final_Dataset.csv*.
